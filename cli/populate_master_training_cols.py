#!/usr/bin/env python3
"""
Script to populate additional columns in the master training CSV.

Supports:
- Feature names (e.g., 'points|season|avg|diff') - calculated on-demand
- Metadata columns: 'game_id', 'home_points', 'away_points' - extracted from MongoDB
- Prediction columns: 'pred_home_points', 'pred_away_points', 'pred_margin', 'pred_total' - from selected point model

Usage:
    python cli/populate_master_training_cols.py \
        --columns "game_id,home_points,away_points,points|season|avg|diff" \
        [--overwrite] \
        [--backup] \
        [--master-csv PATH]
    
    python cli/populate_master_training_cols.py \
        --columns "pred_home_points,pred_away_points,pred_margin,pred_total" \
        [--overwrite] \
        [--backup]
"""

import sys
import os
import argparse
import pandas as pd
import shutil
import threading
from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.cli.Mongo import Mongo
from nba_app.cli.NBAModel import NBAModel, get_default_classifier_features
from nba_app.cli.master_training_data import MASTER_TRAINING_PATH
from nba_app.cli.feature_dependencies import resolve_dependencies, categorize_features
import numpy as np


def _infer_nba_model_flags(feature_names: List[str]) -> Dict[str, bool]:
    """
    Infer which heavyweight NBAModel components are actually needed for this feature batch.

    This is important for the master-training "add columns" workflow: we don't want to
    preload player stats / PER calculator when regenerating team-level-only features
    like travel/rest.
    """
    names = [f or "" for f in feature_names]
    names_lower = [f.lower() for f in names]

    def _stat_name(f: str) -> str:
        return f.split("|", 1)[0].lower() if "|" in f else f.lower()

    stat_names = [_stat_name(f) for f in names]

    # Player/PER features
    needs_per = any(
        f.startswith("player_") or f.startswith("per_available") or _stat_name(f).endswith("_per")
        for f in names_lower
    )

    # Injury features
    needs_injuries = any(f.startswith("inj_") for f in names_lower)

    # Elo features
    needs_elo = any(sn.startswith("elo") for sn in stat_names)

    # Preloading all game docs is expensive and (for small team-level batches) unnecessary.
    # Heuristic: preload when batch is large or when we know we need more global context.
    preload_data = (len(feature_names) >= 50) or needs_per or needs_injuries

    return {
        "needs_per": needs_per,
        "needs_injuries": needs_injuries,
        "needs_elo": needs_elo,
        "preload_data": preload_data,
    }


def update_job_progress(job_id: str, progress: int, message: str = None, db=None):
    """
    Update job progress and message.
    
    Args:
        job_id: Job ID
        progress: Progress percentage (0-100)
        message: Optional status message
        db: MongoDB database connection
    """
    if db is None:
        return
    
    update_doc = {
        'progress': max(0, min(100, progress)),
        'updated_at': datetime.utcnow()
    }
    if message:
        update_doc['message'] = message
    
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': update_doc}
    )


def complete_job(job_id: str, message: str = 'Job completed successfully', db=None):
    """Mark job as completed."""
    if db is None:
        return
    
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'completed',
            'progress': 100,
            'message': message,
            'updated_at': datetime.utcnow()
        }}
    )


def fail_job(job_id: str, error: str, message: str = None, db=None):
    """Mark job as failed with error message."""
    if db is None:
        return
    
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'failed',
            'error': error,
            'message': message or f'Job failed: {error}',
            'updated_at': datetime.utcnow()
        }}
    )


def find_features_by_substrings(features: List[str], substrings: List[str], match_mode: str = 'OR') -> List[str]:
    """
    Find features that match any or all of the given substrings.
    
    Args:
        features: List of all feature names to search
        substrings: List of substrings to match against (case-insensitive)
        match_mode: 'OR' to match features containing ANY substring, 'AND' to match features containing ALL substrings
        
    Returns:
        List of matching feature names
    """
    if not substrings:
        return []
    
    # Normalize substrings to lowercase for case-insensitive matching
    substrings_lower = [s.lower().strip() for s in substrings if s.strip()]
    
    if not substrings_lower:
        return []
    
    matching_features = []
    
    for feature in features:
        feature_lower = feature.lower()
        
        if match_mode.upper() == 'AND':
            # AND mode: feature must contain ALL substrings
            if all(substring in feature_lower for substring in substrings_lower):
                matching_features.append(feature)
        else:
            # OR mode (default): feature must contain ANY substring
            if any(substring in feature_lower for substring in substrings_lower):
                matching_features.append(feature)
    
    return matching_features


def extract_metadata_from_mongodb(
    df: pd.DataFrame,
    columns: List[str],
    db
) -> pd.DataFrame:
    """
    Extract metadata columns (game_id, home_points, away_points) from MongoDB.
    
    Args:
        df: DataFrame with existing master training data
        columns: List of metadata columns to extract
        db: MongoDB database connection
        
    Returns:
        DataFrame with new columns added
    """
    print(f"Loading games from MongoDB for {len(df)} rows...")
    
    # Get date range from dataframe for efficient batch query
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    print(f"  Date range: {min_year}-{max_year}")
    
    # Build lookup maps: load all games in date range once and create lookup by (year, month, day, home, away)
    game_lookup_by_date_teams = {}  # (year, month, day, home, away) -> game doc
    game_lookup_by_id = {}  # game_id -> game doc
    
    # Get game_ids from dataframe if available
    game_ids_in_df = set()
    if 'game_id' in df.columns:
        for game_id in df['game_id'].dropna():
            if game_id and str(game_id).strip():
                game_ids_in_df.add(str(game_id).strip())
    
    # Strategy: Query all games in the date range, then build lookup maps in memory
    # This is much faster than querying per combination
    print("  Loading all games from MongoDB in date range (single batch query)...")
    query = {
        'year': {'$gte': min_year, '$lte': max_year}
    }
    
    # Add game_id filter if we have game_ids (can help with indexing)
    if game_ids_in_df and len(game_ids_in_df) < 50000:  # Only if reasonable number
        query['$or'] = [
            {'year': {'$gte': min_year, '$lte': max_year}},
            {'game_id': {'$in': list(game_ids_in_df)}}
        ]
    
    all_games = list(db.stats_nba.find(query))
    print(f"  Loaded {len(all_games)} games from MongoDB")
    
    # Build lookup maps from loaded games
    print("  Building lookup maps...")
    for game in all_games:
        year = game.get('year')
        month = game.get('month')
        day = game.get('day')
        home_team = game.get('homeTeam', {}).get('name', '')
        away_team = game.get('awayTeam', {}).get('name', '')
        
        if year and month and day and home_team and away_team:
            key = (year, month, day, home_team, away_team)
            game_lookup_by_date_teams[key] = game
        
        # Also index by game_id if available
        game_id = game.get('game_id', '') or ''
        if game_id:
            game_lookup_by_id[game_id] = game
    
    print(f"  Built lookup maps: {len(game_lookup_by_date_teams)} by date/team, {len(game_lookup_by_id)} by game_id")
    
    # Now populate columns using the lookup maps
    print(f"\nPopulating metadata columns: {columns}")
    total_rows = len(df)
    
    # Initialize columns
    for col in columns:
        if col == 'game_id':
            df['game_id'] = ''
        elif col == 'home_points':
            df['home_points'] = 0
        elif col == 'away_points':
            df['away_points'] = 0
    
    # Populate values using lookup maps
    matched_count = 0
    for idx, row in df.iterrows():
        if (idx + 1) % 1000 == 0 or (idx + 1) == total_rows:
            print(f"  Progress: {idx + 1}/{total_rows} rows ({100 * (idx + 1) / total_rows:.1f}%)")
        
        year = int(row['Year'])
        month = int(row['Month'])
        day = int(row['Day'])
        home_team = row['Home']
        away_team = row['Away']
        
        # Try to find game: first by game_id if available, then by date/teams
        game = None
        
        # Try game_id lookup first if game_id exists in row
        if 'game_id' in row and pd.notna(row['game_id']) and row['game_id']:
            game_id = str(row['game_id'])
            game = game_lookup_by_id.get(game_id)
        
        # Fallback to date/team lookup
        if not game:
            key = (year, month, day, home_team, away_team)
            game = game_lookup_by_date_teams.get(key)
        
        if game:
            matched_count += 1
            # Extract requested columns
            for col in columns:
                if col == 'game_id':
                    game_id = game.get('game_id', '') or ''
                    df.at[idx, 'game_id'] = game_id
                elif col == 'home_points':
                    home_points = game.get('homeTeam', {}).get('points', 0) or 0
                    df.at[idx, 'home_points'] = home_points
                elif col == 'away_points':
                    away_points = game.get('awayTeam', {}).get('points', 0) or 0
                    df.at[idx, 'away_points'] = away_points
    
    print(f"\n  Matched {matched_count}/{total_rows} rows ({100 * matched_count / total_rows:.1f}%)")
    
    return df


def _process_feature_chunk(
    chunk_df: pd.DataFrame,
    chunk_idx: int,
    feature_names: List[str],
    total_rows: int,
    start_idx: int,
    progress_callback: callable = None
) -> pd.DataFrame:
    """
    Process a chunk of DataFrame rows and calculate features.
    This function is designed to be called in parallel by multiple threads.
    
    Args:
        chunk_df: DataFrame slice with rows to process
        chunk_idx: Index of this chunk (for logging)
        feature_names: List of feature names to calculate
        total_rows: Total number of rows being processed (for progress calculation)
        start_idx: Starting row index for this chunk (for progress calculation)
        progress_callback: Optional callback function to report progress (processed, total)
        
    Returns:
        DataFrame with calculated feature columns
    """
    # Create NBAModel instance for this thread (each thread needs its own instance)
    flags = _infer_nba_model_flags(feature_names)
    model = NBAModel(
        classifier_features=feature_names,  # keep aligned with what's being computed
        include_elo=flags["needs_elo"],
        include_per_features=flags["needs_per"],
        include_injuries=flags["needs_injuries"],
        preload_data=flags["preload_data"]
    )
    model.feature_names = feature_names
    
    # Initialize feature columns if needed
    for feature_name in feature_names:
        if feature_name not in chunk_df.columns:
            chunk_df[feature_name] = 0.0
    
    # Calculate features for each row in the chunk
    chunk_size = len(chunk_df)
    last_reported = 0
    
    # Report progress every N rows (report more frequently for smaller chunks)
    # For chunks of 500, report every 50 rows (10% of chunk)
    report_interval = max(1, chunk_size // 10) if chunk_size > 10 else 1
    
    for row_idx, (idx, row) in enumerate(chunk_df.iterrows()):
        year = int(row['Year'])
        month = int(row['Month'])
        day = int(row['Day'])
        home_team = row['Home']
        away_team = row['Away']
        
        # Determine season from year/month
        if month >= 10:
            season = f"{year}-{year+1}"
        else:
            season = f"{year-1}-{year}"
        
        # Build features dict
        features_dict = model._build_features_dict(
            home_team, away_team, season, year, month, day
        )
        
        # Update feature values
        for feature_name in feature_names:
            if features_dict and feature_name in features_dict:
                value = features_dict[feature_name]
                # Handle NaN/Inf
                if pd.isna(value) or (isinstance(value, float) and (value != value or abs(value) == float('inf'))):
                    value = 0.0
                chunk_df.at[idx, feature_name] = value
        
        # Report progress periodically during chunk processing
        rows_processed_in_chunk = row_idx + 1
        if progress_callback and (rows_processed_in_chunk - last_reported >= report_interval or rows_processed_in_chunk == chunk_size):
            # Calculate absolute progress
            total_processed = start_idx + rows_processed_in_chunk
            # Call callback with number of rows processed since last report
            progress_callback(rows_processed_in_chunk - last_reported, total_rows)
            last_reported = rows_processed_in_chunk
    
    return chunk_df


def calculate_feature_columns_chunked(
    df: pd.DataFrame,
    feature_names: List[str],
    db,
    job_id: str = None,
    chunk_size: int = 500,
    progress_callback: callable = None
) -> pd.DataFrame:
    """
    Calculate multiple feature columns in chunks with parallel processing.
    Uses ThreadPoolExecutor to process chunks in parallel, similar to NBAModel.create_training_data.
    
    Args:
        df: DataFrame with master training data
        feature_names: List of feature names to calculate
        db: MongoDB database connection
        job_id: Optional job ID for progress updates
        chunk_size: Number of rows to process per chunk
        progress_callback: Optional callback function(current, total, progress_pct)
        
    Returns:
        DataFrame with calculated feature columns added
    """
    total_rows = len(df)
    total_chunks = (total_rows + chunk_size - 1) // chunk_size
    
    print(f"Calculating {len(feature_names)} features in {total_chunks} chunks of ~{chunk_size} rows using parallel threads...")
    
    # Update progress: starting chunked processing
    if job_id:
        update_job_progress(job_id, 1, f"[STEP 8/8] Starting chunked processing: {len(feature_names)} features, {total_rows} total rows, {total_chunks} chunks", db)
    
    # Initialize feature columns
    for feature_name in feature_names:
        if feature_name not in df.columns:
            df[feature_name] = 0.0
    
    # Split DataFrame into chunks
    chunk_data = []
    for chunk_idx in range(total_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, total_rows)
        chunk_df = df.iloc[start_idx:end_idx].copy()
        chunk_data.append((chunk_idx, chunk_df, start_idx))
    
    # Thread-safe progress tracker
    progress_lock = threading.Lock()
    progress_state = {
        'processed': 0,
        'last_logged_threshold': 0.0
    }
    
    def log_progress_if_needed(processed, total):
        """Thread-safe progress logging."""
        with progress_lock:
            progress_state['processed'] += processed
            current = progress_state['processed']
            
            # Cap current at total to avoid >100% (handles any double-counting issues)
            current = min(current, total)
            current_progress_pct = (current / total) * 100 if total > 0 else 0
            
            # Update if we cross a 2.5% threshold
            if current_progress_pct >= progress_state['last_logged_threshold'] + 2.5 or current == total:
                progress_state['last_logged_threshold'] = current_progress_pct
                
                if job_id and db is not None:
                    current_feature = feature_names[0] if len(feature_names) == 1 else f"{len(feature_names)} features"
                    message = f"Processing: {current_feature} ({current}/{total} rows, {current_progress_pct:.1f}%)"
                    update_job_progress(job_id, min(int(current_progress_pct), 100), message, db)
    
    # Process chunks in parallel using ThreadPoolExecutor
    chunk_results = []
    
    with ThreadPoolExecutor(max_workers=None) as executor:  # None = use default (CPU count)
        # Submit all chunks
        future_to_chunk = {
            executor.submit(
                _process_feature_chunk,
                chunk_df,
                chunk_idx,
                feature_names,
                total_rows,
                start_idx,
                log_progress_if_needed
            ): (chunk_idx, start_idx)
            for chunk_idx, chunk_df, start_idx in chunk_data
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_chunk):
            chunk_idx, start_idx = future_to_chunk[future]
            try:
                result_chunk_df = future.result()
                chunk_results.append((chunk_idx, result_chunk_df))
                rows_in_chunk = len(result_chunk_df)
                
                # Report progress
                log_progress_if_needed(rows_in_chunk, total_rows)
                
                print(f"  Completed chunk {chunk_idx + 1}/{total_chunks} ({rows_in_chunk} rows processed)")
            except Exception as e:
                print(f"  [Chunk {chunk_idx}] Failed with exception: {e}")
                import traceback
                traceback.print_exc()
                raise
    
    # Sort results by chunk index to maintain order
    chunk_results.sort(key=lambda x: x[0])
    
    # Update main DataFrame with calculated values (optimized: update all features at once per chunk)
    print(f"\nCombining {len(chunk_results)} chunks into main DataFrame...")
    if job_id:
        update_job_progress(job_id, 85, "Combining processed chunks into main DataFrame...", db)
    
    # Optimized: Update all feature columns for each chunk in a single operation
    # This is much faster than nested loops with individual loc assignments
    # Instead of: for each chunk, for each feature: df.loc[index, feature] = value
    # We do: for each chunk: df.loc[index, all_features] = chunk_df[all_features]
    # This reduces operations from (num_chunks * num_features) to just (num_chunks)
    for chunk_idx, result_chunk_df in chunk_results:
        # Update all feature columns at once using a single loc operation
        df.loc[result_chunk_df.index, feature_names] = result_chunk_df[feature_names]
        
        # Progress reporting for large datasets (every 10 chunks or last chunk)
        if (chunk_idx + 1) % 10 == 0 or (chunk_idx + 1) == len(chunk_results):
            if job_id:
                progress_pct = 85 + int((chunk_idx + 1) / len(chunk_results) * 5)  # 85-90%
                update_job_progress(job_id, progress_pct, 
                                  f"Combining chunks: {chunk_idx + 1}/{len(chunk_results)} complete...", db)
    
    # Final progress update (90% - feature calculation complete, but CSV writing still pending)
    if job_id:
        current_feature = feature_names[0] if len(feature_names) == 1 else f"{len(feature_names)} features"
        message = f"Feature calculation complete: {current_feature} ({total_rows}/{total_rows} rows). Preparing to write CSV..."
        update_job_progress(job_id, 90, message, db)
    
    if progress_callback:
        progress_callback(total_rows, total_rows, 100.0)
    
    print(f"  Completed: {total_rows}/{total_rows} rows (100.0%)")
    
    return df


def calculate_feature_column(
    df: pd.DataFrame,
    feature_name: str,
    db
) -> pd.Series:
    """
    Calculate a feature column on-demand using NBAModel.
    
    Args:
        df: DataFrame with master training data
        feature_name: Feature name to calculate (e.g., 'points|season|avg|diff')
        db: MongoDB database connection
        
    Returns:
        Series with feature values
    """
    print(f"Calculating feature: {feature_name}")
    
    # Create NBAModel instance
    flags = _infer_nba_model_flags([feature_name])
    model = NBAModel(
        classifier_features=[feature_name],
        include_elo=flags["needs_elo"],
        include_per_features=flags["needs_per"],
        include_injuries=flags["needs_injuries"],
        preload_data=flags["preload_data"]
    )
    model.feature_names = [feature_name]
    
    # Calculate feature for each row
    feature_values = []
    total_rows = len(df)
    
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0 or (idx + 1) == total_rows:
            print(f"  Progress: {idx + 1}/{total_rows} rows ({100 * (idx + 1) / total_rows:.1f}%)")
        
        year = int(row['Year'])
        month = int(row['Month'])
        day = int(row['Day'])
        home_team = row['Home']
        away_team = row['Away']
        
        # Determine season from year/month
        if month >= 10:
            season = f"{year}-{year+1}"
        else:
            season = f"{year-1}-{year}"
        
        # Build features dict
        features_dict = model._build_features_dict(
            home_team, away_team, season, year, month, day
        )
        
        if features_dict and feature_name in features_dict:
            value = features_dict[feature_name]
            # Handle NaN/Inf
            if pd.isna(value) or (isinstance(value, float) and (value != value or abs(value) == float('inf'))):
                value = 0.0
            feature_values.append(value)
        else:
            feature_values.append(0.0)
    
    return pd.Series(feature_values, index=df.index)


def extract_predictions_from_selected_model(
    df: pd.DataFrame,
    db
) -> pd.DataFrame:
    """
    Extract point predictions from the selected point model config.
    
    Args:
        df: DataFrame with master training data
        db: MongoDB database connection
        
    Returns:
        DataFrame with added columns: pred_home_points, pred_away_points, pred_margin, pred_point_total
    """
    from nba_app.cli.points_regression import PointsRegressionTrainer
    
    print("Loading selected point model config from MongoDB...")
    
    # Query for selected config
    selected_config = db.model_config_points_nba.find_one({'selected': True})
    if not selected_config:
        raise ValueError(
            "No selected point model config found in model_config_points_nba collection. "
            "Please select a point model config in the UI or via MongoDB."
        )
    
    model_path = selected_config.get('model_path')
    if not model_path:
        raise ValueError(
            "Selected point model config does not have 'model_path' field. "
            "The config may be incomplete or the model was not saved properly."
        )
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Selected point model file not found: {model_path}. "
            "The model may have been deleted or moved."
        )
    
    # Extract model name from path (remove .pkl extension)
    model_name = os.path.basename(model_path).replace('.pkl', '')
    
    print(f"  Selected config found: {selected_config.get('name', 'Unnamed')}")
    print(f"  Model path: {model_path}")
    print(f"  Model name: {model_name}")
    
    # Load model using PointsRegressionTrainer
    print(f"\nLoading point model: {model_name}")
    trainer = PointsRegressionTrainer(db=db)
    try:
        trainer.load_model(model_name)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load point model '{model_name}': {e}. "
            "Make sure the model files exist in the artifacts directory."
        ) from e
    
    # CRITICAL: Use feature_names from loaded model to ensure correct feature order
    # The model was trained with features in a specific order (trainer.feature_names)
    # We must use this exact order for predictions to work correctly
    if not hasattr(trainer, 'feature_names') or not trainer.feature_names:
        raise ValueError(
            "Loaded model does not have feature_names. Model may be corrupted or incompatible."
        )
    
    model_feature_names = trainer.feature_names
    print(f"  Model expects {len(model_feature_names)} features")
    
    # Log config features if available (for informational purposes)
    config_features = selected_config.get('features', [])
    if config_features:
        print(f"  Config lists {len(config_features)} features (model uses its saved feature order)")
    
    # Validate that features exist in master CSV
    master_features = set(df.columns)
    missing_features = [f for f in model_feature_names if f not in master_features]
    available_features = [f for f in model_feature_names if f in master_features]
    
    if missing_features:
        print(f"  WARNING: {len(missing_features)} features not found in master CSV:")
        print(f"  Missing features (first 20): {missing_features[:20]}")
        print(f"  Available features: {len(available_features)}/{len(model_feature_names)}")
        print(f"  Missing features will be set to 0.0 for prediction")
    
    if len(available_features) == 0:
        raise ValueError(
            f"None of the required features ({len(model_feature_names)} total) are found in master CSV. "
            "Master CSV must contain the features used to train the point model."
        )
    
    # Prepare features for vectorized prediction
    print(f"\nGenerating predictions for {len(df)} games using vectorized prediction...")
    
    # Build feature matrix with features in the EXACT order expected by the model
    # This order must match trainer.feature_names to ensure correct predictions
    feature_matrix = np.zeros((len(df), len(model_feature_names)))
    for idx, feature_name in enumerate(model_feature_names):
        if feature_name in df.columns:
            feature_matrix[:, idx] = df[feature_name].fillna(0.0).values
        else:
            # Missing feature - already initialized to 0.0, which is the default
            pass
    
    # Check for NaN or infinite values
    if np.any(np.isnan(feature_matrix)) or np.any(np.isinf(feature_matrix)):
        nan_count = np.sum(np.isnan(feature_matrix) | np.isinf(feature_matrix))
        print(f"  WARNING: Found {nan_count} NaN or Inf values in feature matrix. Replacing with 0.0")
        feature_matrix = np.nan_to_num(feature_matrix, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Scale features using trainer's scaler
    try:
        feature_matrix_scaled = trainer.scaler.transform(feature_matrix)
    except Exception as e:
        raise RuntimeError(
            f"Failed to scale features: {e}. "
            "Make sure the scaler was saved correctly with the model."
        ) from e
    
    # Generate predictions based on target type
    target_type = getattr(trainer, 'target_type', 'home_away')
    
    # Determine target type from model structure if not set
    if not hasattr(trainer, 'target_type') or trainer.target_type is None:
        if isinstance(trainer.model, dict) and 'home' in trainer.model and 'away' in trainer.model:
            target_type = 'home_away'
        else:
            target_type = 'margin'
    
    print(f"  Model target type: {target_type}")
    
    # Initialize prediction arrays
    pred_home_points = np.zeros(len(df))
    pred_away_points = np.zeros(len(df))
    pred_margin = np.zeros(len(df))
    pred_point_total = np.zeros(len(df))
    
    try:
        if target_type == 'margin':
            # Margin-only model: single model that predicts margin directly
            pred_margin_all = trainer.model.predict(feature_matrix_scaled)
            pred_margin_all = np.clip(pred_margin_all, -60, 60)  # Clamp to reasonable range
            
            pred_margin[:] = pred_margin_all
            # For margin-only, home/away are None (not predicted)
            pred_home_points[:] = np.nan
            pred_away_points[:] = np.nan
            pred_point_total[:] = np.nan
        else:
            # Home/away models: dict with 'home' and 'away' keys
            if not isinstance(trainer.model, dict) or 'home' not in trainer.model or 'away' not in trainer.model:
                raise ValueError(
                    f"Invalid model structure for target='home_away'. "
                    "Expected dict with 'home' and 'away' keys."
                )
            
            pred_home_all = trainer.model['home'].predict(feature_matrix_scaled)
            pred_away_all = trainer.model['away'].predict(feature_matrix_scaled)
            
            # Clamp to reasonable range
            pred_home_all = np.clip(pred_home_all, 0, 200)
            pred_away_all = np.clip(pred_away_all, 0, 200)
            
            pred_home_points[:] = pred_home_all
            pred_away_points[:] = pred_away_all
            pred_margin[:] = pred_home_all - pred_away_all
            pred_point_total[:] = pred_home_all + pred_away_all
    except Exception as e:
        raise RuntimeError(
            f"Failed to generate predictions: {e}. "
            "Make sure the model structure matches the expected format."
        ) from e
    
    # Add prediction columns to dataframe
    df['pred_home_points'] = pred_home_points
    df['pred_away_points'] = pred_away_points
    df['pred_margin'] = pred_margin
    df['pred_point_total'] = pred_point_total
    
    print(f"  Generated predictions for {len(df)} games")
    if target_type == 'margin':
        print(f"  Margin range: {pred_margin.min():.2f} to {pred_margin.max():.2f}")
    else:
        print(f"  Home points range: {pred_home_points.min():.2f} to {pred_home_points.max():.2f}")
        print(f"  Away points range: {pred_away_points.min():.2f} to {pred_away_points.max():.2f}")
        print(f"  Margin range: {pred_margin.min():.2f} to {pred_margin.max():.2f}")
        print(f"  Total points range: {pred_point_total.min():.2f} to {pred_point_total.max():.2f}")
    
    return df


def populate_columns(
    master_csv_path: str,
    columns: List[str] = None,
    feature_substrings: List[str] = None,
    match_mode: str = 'OR',
    overwrite: bool = False,
    backup: bool = True,
    job_id: str = None,
    chunk_size: int = 500,
    progress_callback: callable = None
) -> str:
    """
    Populate additional columns in master training CSV.
    
    Args:
        master_csv_path: Path to master training CSV
        columns: List of column names to add (optional if feature_substrings provided)
        feature_substrings: List of substrings to match features (optional if columns provided)
        match_mode: 'OR' to match features containing ANY substring, 'AND' to match features containing ALL substrings
        overwrite: If True, overwrite existing columns
        backup: If True, create backup before modifying
        job_id: Optional job ID for progress updates
        chunk_size: Batch size for processing (default: 500 rows)
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Path to updated CSV
    """
    # Connect to MongoDB
    if job_id:
        try:
            mongo = Mongo()
            db = mongo.db
            update_job_progress(job_id, 0, "[STEP 4/8] Connected to MongoDB in populate_columns. Checking CSV...", db=db)
        except Exception as e:
            # If we can't connect, try anyway
            mongo = Mongo()
            db = mongo.db
    else:
        mongo = Mongo()
        db = mongo.db
    
    if job_id:
        update_job_progress(job_id, 0, f"[STEP 5/8] Checking if CSV exists: {master_csv_path}", db=db)
    
    if not os.path.exists(master_csv_path):
        error_msg = f"Master training CSV not found: {master_csv_path}"
        if job_id:
            fail_job(job_id, error_msg, db=db)
        raise FileNotFoundError(error_msg)
    
    if job_id:
        update_job_progress(job_id, 0, "[STEP 6/8] CSV exists. Processing feature_substrings or columns...", db=db)
    
    # If feature_substrings provided, match features by substring
    if feature_substrings:
        print(f"Matching features by substrings: {feature_substrings}")
        # Read CSV to get all features
        df_temp = pd.read_csv(master_csv_path)
        metadata_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'HomeWon', 
                        'home_points', 'away_points', 'pred_home_points', 'pred_away_points', 
                        'pred_margin', 'pred_point_total', 'pred_total']
        all_features = [c for c in df_temp.columns if c not in metadata_cols]
        
        # Match features with match mode
        matching_features = find_features_by_substrings(all_features, feature_substrings, match_mode)
        
        if not matching_features:
            error_msg = f"No features found matching substrings: {feature_substrings}"
            if job_id:
                fail_job(job_id, error_msg, db=db)
            raise ValueError(error_msg)
        
        print(f"  Found {len(matching_features)} matching features")
        columns = matching_features
        
        # Resolve dependencies
        print("Resolving feature dependencies...")
        from nba_app.cli.feature_dependencies import resolve_dependencies
        all_features_set, dependency_map = resolve_dependencies(matching_features, include_transitive=True)
        categorized = categorize_features(matching_features, all_features_set)
        
        print(f"  Requested: {len(categorized['requested'])} features")
        print(f"  Dependencies: {len(categorized['dependencies'])} features")
        print(f"  Total to regenerate: {len(categorized['all'])} features")
        
        # Use all features including dependencies
        columns = categorized['all']
    
    if not columns:
        error_msg = "No columns specified for regeneration"
        if job_id:
            fail_job(job_id, error_msg, db=db)
        raise ValueError(error_msg)
    
    # Update job: starting
    if job_id:
        update_job_progress(job_id, 0, f"[STEP 7/8] Starting column processing. Columns to process: {len(columns)}", db)
    
    # Create backup if requested
    if backup:
        backup_path = f"{master_csv_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Creating backup: {backup_path}")
        shutil.copy2(master_csv_path, backup_path)
    
    # Read existing CSV
    print(f"Reading master training CSV: {master_csv_path}")
    df = pd.read_csv(master_csv_path)
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Separate columns into metadata, prediction, and feature columns
    metadata_cols = []
    prediction_cols = []
    feature_cols = []
    
    # Note: pred_total and pred_point_total are aliases - we generate pred_point_total
    prediction_column_names = ['pred_home_points', 'pred_away_points', 'pred_margin', 'pred_total', 'pred_point_total']
    
    for col in columns:
        if col in ['game_id', 'home_points', 'away_points']:
            metadata_cols.append(col)
        elif col in prediction_column_names:
            prediction_cols.append(col)
        else:
            feature_cols.append(col)
    
    # Check which columns already exist
    existing_cols = [col for col in columns if col in df.columns]
    if existing_cols:
        if overwrite:
            print(f"Overwriting existing columns: {existing_cols}")
        else:
            print(f"Skipping existing columns (use --overwrite to update): {existing_cols}")
            columns = [col for col in columns if col not in existing_cols]
    
    if not columns:
        print("No new columns to add")
        return master_csv_path
    
    # Add metadata columns
    if metadata_cols:
        print(f"\nExtracting metadata columns from MongoDB: {metadata_cols}")
        df = extract_metadata_from_mongodb(df, metadata_cols, db)
    
    # Add prediction columns (all prediction columns are added together)
    if prediction_cols:
        # Check if we need to add any prediction columns
        # We always generate all prediction columns (pred_home_points, pred_away_points, pred_margin, pred_point_total)
        # even if only some are requested, for consistency
        requested_prediction_cols = prediction_cols
        
        # Check existing columns (handle both pred_total and pred_point_total)
        existing_prediction_cols = []
        for col in ['pred_home_points', 'pred_away_points', 'pred_margin', 'pred_point_total']:
            if col in df.columns:
                existing_prediction_cols.append(col)
        # Also check if pred_total exists (it's an alias for pred_point_total)
        if 'pred_total' in df.columns:
            existing_prediction_cols.append('pred_total')
        
        if existing_prediction_cols and not overwrite:
            print(f"Skipping existing prediction columns (use --overwrite to update): {existing_prediction_cols}")
            # Only generate if we're overwriting or if some requested columns don't exist
            # Map pred_total to pred_point_total for checking
            missing_prediction_cols = []
            for col in requested_prediction_cols:
                if col == 'pred_total':
                    if 'pred_point_total' not in df.columns and 'pred_total' not in df.columns:
                        missing_prediction_cols.append(col)
                elif col not in df.columns:
                    missing_prediction_cols.append(col)
            
            if missing_prediction_cols:
                print(f"  But these prediction columns are missing: {missing_prediction_cols}")
                print(f"  Generating all prediction columns...")
                df = extract_predictions_from_selected_model(df, db)
        else:
            print(f"\nExtracting prediction columns from selected point model: {requested_prediction_cols}")
            if overwrite and existing_prediction_cols:
                print(f"  Overwriting existing prediction columns: {existing_prediction_cols}")
            df = extract_predictions_from_selected_model(df, db)
        
        # Handle pred_total alias mapping (function generates pred_point_total)
        # If user requested pred_total, create alias if it doesn't exist
        if 'pred_total' in requested_prediction_cols:
            if 'pred_point_total' in df.columns:
                if 'pred_total' not in df.columns:
                    df['pred_total'] = df['pred_point_total']
                elif overwrite:
                    df['pred_total'] = df['pred_point_total']
    
    # Calculate feature columns
    if feature_cols:
        print(f"\nCalculating feature columns: {len(feature_cols)} features")
        
        # Filter to only features that need calculation
        features_to_calculate = [f for f in feature_cols if f not in df.columns or overwrite]
        
        if features_to_calculate:
            if job_id or chunk_size < len(df):
                # Use chunked processing
                df = calculate_feature_columns_chunked(
                    df, features_to_calculate, db, 
                    job_id=job_id, 
                    chunk_size=chunk_size,
                    progress_callback=progress_callback
                )
            else:
                # Use original per-feature processing (backward compatibility)
                for feature_name in features_to_calculate:
                    if feature_name not in df.columns or overwrite:
                        df[feature_name] = calculate_feature_column(df, feature_name, db)
                        # Update progress after each feature
                        if job_id:
                            features_done = feature_cols.index(feature_name) + 1
                            progress_pct = (features_done / len(feature_cols)) * 100
                            update_job_progress(job_id, int(progress_pct), 
                                              f"Calculated {feature_name} ({features_done}/{len(feature_cols)} features)", db)
    
    # Reorder columns to match expected format:
    # [Year, Month, Day, Home, Away, game_id, ...features..., pred_home_points, pred_away_points, pred_margin, pred_point_total, HomeWon, home_points, away_points]
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    if 'game_id' in df.columns:
        meta_cols.append('game_id')
    
    # Prediction columns (if they exist)
    pred_cols = []
    for pred_col in ['pred_home_points', 'pred_away_points', 'pred_margin', 'pred_point_total', 'pred_total']:
        if pred_col in df.columns and pred_col not in pred_cols:
            pred_cols.append(pred_col)
    
    target_cols = []
    if 'HomeWon' in df.columns:
        target_cols.append('HomeWon')
    if 'home_points' in df.columns:
        target_cols.append('home_points')
    if 'away_points' in df.columns:
        target_cols.append('away_points')
    
    # Feature columns are everything else (exclude metadata, predictions, and targets)
    excluded_cols = meta_cols + pred_cols + target_cols
    feature_cols_in_df = [c for c in df.columns if c not in excluded_cols]
    
    # Reorder
    new_column_order = meta_cols + sorted(feature_cols_in_df) + pred_cols + target_cols
    df = df[new_column_order]
    
    # Write updated CSV
    print(f"\nWriting updated CSV: {master_csv_path}")
    if job_id:
        update_job_progress(job_id, 95, "Writing updated CSV to disk...", db)
    
    # Write to temporary file first, then swap (atomic operation)
    temp_file_path = f"{master_csv_path}.tmp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    df.to_csv(temp_file_path, index=False)
    
    # Swap files
    shutil.move(temp_file_path, master_csv_path)
    
    print(f"  Updated: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Regenerated columns: {len(columns)}")
    
    # Update job: completed
    if job_id:
        complete_job(job_id, f"Successfully regenerated {len(columns)} features", db)
    
    return master_csv_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Populate additional columns in master training CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/populate_master_training_cols.py --columns "game_id,home_points,away_points"
  python cli/populate_master_training_cols.py --columns "points|season|avg|diff" --overwrite
  python cli/populate_master_training_cols.py --columns "pred_home_points,pred_away_points,pred_margin,pred_total"
  python cli/populate_master_training_cols.py --columns "game_id,home_points,away_points" --master-csv /path/to/csv
  python cli/populate_master_training_cols.py --feature-substrings "inj_min_lost,player_per_1" --overwrite --job-id JOB_ID
        """
    )
    
    parser.add_argument(
        '--columns',
        type=str,
        default=None,
        help='Comma-separated list of column names to add (e.g., "game_id,home_points,away_points,points|season|avg|diff,pred_home_points,pred_away_points,pred_margin,pred_total")'
    )
    
    parser.add_argument(
        '--feature-substrings',
        type=str,
        default=None,
        help='Comma-separated list of substrings to match features (e.g., "inj_min_lost,player_per_1"). Matches all features containing any substring.'
    )
    
    parser.add_argument(
        '--match-mode',
        type=str,
        choices=['OR', 'AND'],
        default='OR',
        help='Match mode: OR matches features containing ANY substring, AND matches features containing ALL substrings (default: OR)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing columns if they already exist'
    )
    
    parser.add_argument(
        '--backup',
        action='store_true',
        default=True,
        help='Create backup before modifying (default: True)'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup'
    )
    
    parser.add_argument(
        '--master-csv',
        type=str,
        default=MASTER_TRAINING_PATH,
        help=f'Path to master training CSV (default: {MASTER_TRAINING_PATH})'
    )
    
    parser.add_argument(
        '--job-id',
        type=str,
        default=None,
        help='Job ID for progress updates (optional)'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=500,
        help='Batch size for processing rows (default: 500)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate without regenerating (shows what would be regenerated)'
    )
    
    args = parser.parse_args()
    
    # Connect to MongoDB if job_id provided (do this early for logging)
    db = None
    if args.job_id:
        try:
            mongo = Mongo()
            db = mongo.db
            update_job_progress(args.job_id, 0, "[STEP 1/8] Connected to MongoDB. Validating arguments...", db=db)
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    # Validate arguments
    if not args.columns and not args.feature_substrings:
        error_msg = "Error: Either --columns or --feature-substrings must be specified"
        print(error_msg)
        if args.job_id and db is not None:
            fail_job(args.job_id, error_msg, db=db)
        sys.exit(1)
    
    if args.columns and args.feature_substrings:
        error_msg = "Error: Cannot specify both --columns and --feature-substrings. Use one or the other."
        print(error_msg)
        if args.job_id and db is not None:
            fail_job(args.job_id, error_msg, db=db)
        sys.exit(1)
    
    # Parse columns or feature_substrings
    columns = None
    feature_substrings = None
    
    if args.columns:
        if args.job_id and db is not None:
            update_job_progress(args.job_id, 0, "[STEP 2/8] Parsing columns...", db=db)
        columns = [c.strip() for c in args.columns.split(',') if c.strip()]
        if not columns:
            error_msg = "Error: No columns specified"
            print(error_msg)
            if args.job_id and db is not None:
                fail_job(args.job_id, error_msg, db=db)
            sys.exit(1)
    
    if args.feature_substrings:
        if args.job_id and db is not None:
            update_job_progress(args.job_id, 0, "[STEP 2/8] Parsing feature substrings...", db=db)
        feature_substrings = [s.strip() for s in args.feature_substrings.split(',') if s.strip()]
        if not feature_substrings:
            error_msg = "Error: No feature substrings specified"
            print(error_msg)
            if args.job_id and db is not None:
                fail_job(args.job_id, error_msg, db=db)
            sys.exit(1)
    
    # Handle backup flag
    backup = args.backup and not args.no_backup
    
    try:
        if args.job_id and db is not None:
            update_job_progress(args.job_id, 0, "[STEP 3/8] Calling populate_columns function...", db=db)
        result = populate_columns(
            master_csv_path=args.master_csv,
            columns=columns,
            feature_substrings=feature_substrings,
            match_mode=args.match_mode,
            overwrite=args.overwrite,
            backup=backup if not args.dry_run else False,
            job_id=args.job_id,
            chunk_size=args.chunk_size
        )
        
        if args.dry_run:
            print("\n✓ Dry run completed (no changes made)")
        else:
            print("\n✓ Successfully populated columns")
    except Exception as e:
        error_msg = str(e)
        print(f"\n✗ Error: {error_msg}")
        
        # Mark job as failed if job_id provided
        if args.job_id and db is not None:
            fail_job(args.job_id, error_msg, db=db)
        
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
