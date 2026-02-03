"""
Master Training Data Module for Points Regression

Manages a master training CSV file containing ALL possible features for points regression.
This allows fast feature extraction for training without recalculating features.
"""

import os
import csv
import pandas as pd
from datetime import datetime, date
from typing import Optional, Dict, List, Tuple
from nba_app.core.mongo import Mongo
from nba_app.core.models.points_regression import PointsRegressionTrainer
from nba_app.cli_old.points_regression_features import ALL_POINTS_FEATURES


# Get project root (assuming this file is in nba_app/cli/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Consolidated: place master training (points) in parent ../master_training/
_PARENT_ROOT = os.path.dirname(_PROJECT_ROOT)
MASTER_TRAINING_POINTS_PATH = os.path.join(_PARENT_ROOT, 'master_training', 'MASTER_TRAINING_points.csv')
MASTER_POINTS_COLLECTION = 'master_training_data_points_nba'


def get_all_possible_points_features() -> List[str]:
    """
    Get all possible features that should be included in the master points training CSV.
    
    Returns:
        List of all feature names
    """
    return sorted(ALL_POINTS_FEATURES)


def get_master_training_points_metadata(db) -> Optional[Dict]:
    """
    Get the current master points training data metadata from MongoDB.
    
    Args:
        db: MongoDB database connection
        
    Returns:
        Metadata dict or None if no master exists
    """
    master_doc = db[MASTER_POINTS_COLLECTION].find_one({'is_master': True})
    return master_doc


def create_or_update_master_points_metadata(
    db,
    file_path: str,
    feature_list: List[str],
    feature_count: int,
    last_date_updated: str,
    options: Dict = None
) -> str:
    """
    Create or update master points training data metadata in MongoDB.
    
    Args:
        db: MongoDB database connection
        file_path: Path to master training CSV file
        feature_list: List of feature names included
        feature_count: Number of features
        last_date_updated: Last date the master was updated (YYYY-MM-DD)
        options: Optional dict with configuration options
        
    Returns:
        MongoDB document ID
    """
    metadata = {
        'is_master': True,
        'file_path': file_path,
        'feature_list': feature_list,
        'feature_count': feature_count,
        'last_date_updated': last_date_updated,
        'options': options or {},
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    # Update existing master or create new one
    result = db[MASTER_POINTS_COLLECTION].update_one(
        {'is_master': True},
        {'$set': metadata},
        upsert=True
    )
    
    return result.upserted_id if result.upserted_id else db[MASTER_POINTS_COLLECTION].find_one({'is_master': True})['_id']


def generate_master_training_points_data(
    query: Dict = None,
    output_path: str = None,
    progress_callback: callable = None,
    limit: int = None
) -> Tuple[str, List[str], int]:
    """
    Generate master points training CSV with ALL possible features.
    
    Args:
        query: MongoDB query filter (uses DEFAULT_QUERY if None)
        output_path: Output path for master CSV (defaults to MASTER_TRAINING_POINTS_PATH)
        progress_callback: Optional callback function(current, total, progress_pct) called during processing
        limit: Optional limit on number of rows to write (for testing/debugging). If None, writes all rows.
        
    Returns:
        Tuple of (csv_path, feature_list, game_count)
    """
    # If limit is specified, modify output path to include "_limit-N" suffix
    if limit is not None and limit > 0:
        if output_path is None:
            # Modify the default path
            base_path = MASTER_TRAINING_POINTS_PATH
            base_name = os.path.splitext(base_path)[0]  # Remove .csv extension
            output_path = f"{base_name}_limit-{limit}.csv"
        else:
            # Modify the provided path
            base_name = os.path.splitext(output_path)[0]  # Remove .csv extension
            output_path = f"{base_name}_limit-{limit}.csv"
    else:
        output_path = output_path or MASTER_TRAINING_POINTS_PATH
    
    print(f"[Step 1/4] Setting up output directory...")
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"  Output will be saved to: {output_path}")
    
    print(f"[Step 2/4] Loading feature definitions...")
    # Get all possible features
    all_features = get_all_possible_points_features()
    print(f"  Total features to generate: {len(all_features)}")
    
    print(f"[Step 3/4] Creating training data...")
    # Create PointsRegressionTrainer (injury features will be auto-detected when selected_features=None)
    db = Mongo().db
    trainer = PointsRegressionTrainer(db=db)
    
    # Create training data with all features (None = use all features, including injuries)
    # Pass progress_callback and limit through to trainer
    df = trainer.create_training_data(query=query, selected_features=None, progress_callback=progress_callback, limit=limit)
    
    # Get actual feature names from the DataFrame
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'home_points', 'away_points']
    actual_features = [col for col in df.columns if col not in meta_cols]
    
    print(f"[Step 4/4] Saving to CSV...")
    # Save to CSV (limit already applied in create_training_data)
    df.to_csv(output_path, index=False)
    if limit is not None and limit > 0:
        print(f"  Saved {len(df)} rows to {output_path} (limited to {limit} games)")
    else:
        print(f"  Saved {len(df)} rows to {output_path}")
    
    game_count = len(df)
    
    return output_path, actual_features, game_count


def update_master_training_points_data_incremental(
    db,
    start_date: str,
    end_date: str,
    master_path: str = None,
    progress_callback: callable = None
) -> Tuple[int, str]:
    """
    Incrementally update master points training data with new games between start_date and end_date.
    
    Args:
        db: MongoDB database connection
        start_date: Start date for new games (YYYY-MM-DD, exclusive - games after this date)
        end_date: End date for new games (YYYY-MM-DD, inclusive)
        master_path: Path to master CSV file (defaults to MASTER_TRAINING_POINTS_PATH)
        progress_callback: Optional callback function(current, total, progress_pct)
        
    Returns:
        Tuple of (games_added_count, updated_master_path)
    """
    master_path = master_path or MASTER_TRAINING_POINTS_PATH
    
    # Get master metadata
    master_meta = get_master_training_points_metadata(db)
    if not master_meta:
        raise ValueError("Master points training data does not exist. Generate it first using generate_master_training_points_data()")
    
    # Query for games between start_date and end_date (both inclusive)
    # If start_date == end_date, query for that exact date
    # Otherwise, query for dates > start_date and <= end_date
    if start_date == end_date:
        date_query = {'$eq': start_date}
    else:
        date_query = {
            '$gt': start_date,
            '$lte': end_date
        }
    
    query = {
        'date': date_query,
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']}
    }
    
    # Create trainer (injury features will be auto-detected when selected_features=None)
    trainer = PointsRegressionTrainer(db=db)
    
    # Generate training data for new games only (None = use all features, including injuries)
    new_df = trainer.create_training_data(query=query, selected_features=None)
    
    if len(new_df) == 0:
        # No new games, return existing master
        return 0, master_path
    
    # Read existing master CSV
    try:
        master_df = pd.read_csv(master_path, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions
        try:
            master_df = pd.read_csv(master_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except:
            # Fallback: use csv module
            import csv
            rows = []
            with open(master_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) == len(header):
                        rows.append(row)
            master_df = pd.DataFrame(rows, columns=header)
            # Convert numeric columns
            for col in master_df.columns:
                if col not in ['Home', 'Away']:
                    try:
                        master_df[col] = pd.to_numeric(master_df[col], errors='coerce')
                    except:
                        pass
    
    # Ensure column alignment (new games might have different columns if features changed)
    # Use master's columns as authority
    master_cols = list(master_df.columns)
    new_cols = list(new_df.columns)
    
    # Add missing columns to new_df (fill with 0 or appropriate default)
    for col in master_cols:
        if col not in new_cols:
            new_df[col] = 0
    
    # Reorder new_df columns to match master
    new_df = new_df[master_cols]
    
    # Append new games to master
    combined_df = pd.concat([master_df, new_df], ignore_index=True)
    
    # Remove duplicates (in case of re-runs)
    # Use Year, Month, Day, Home, Away as unique key
    combined_df = combined_df.drop_duplicates(
        subset=['Year', 'Month', 'Day', 'Home', 'Away'],
        keep='last'  # Keep the most recent entry
    )
    
    # Sort by date
    combined_df = combined_df.sort_values(['Year', 'Month', 'Day', 'Home', 'Away'])
    
    # Write updated master CSV
    combined_df.to_csv(master_path, index=False)
    
    # Update metadata
    actual_features = [col for col in master_cols if col not in ['Year', 'Month', 'Day', 'Home', 'Away', 'home_points', 'away_points']]
    create_or_update_master_points_metadata(
        db,
        master_path,
        actual_features,
        len(actual_features),
        end_date,
        master_meta.get('options', {})
    )
    
    return len(new_df), master_path


def extract_features_from_master_points(
    master_path: str,
    requested_features: List[str] = None,
    output_path: str = None
) -> str:
    """
    Extract selected features from master points training CSV.
    
    Args:
        master_path: Path to master training CSV
        requested_features: List of feature names to extract (None = extract all features)
        output_path: Output path for extracted CSV (defaults to temp file)
        
    Returns:
        Path to extracted CSV file
    """
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master points training CSV not found: {master_path}")
    
    # Read master CSV with error handling
    try:
        df = pd.read_csv(master_path, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions
        try:
            df = pd.read_csv(master_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except:
            # Fallback: use csv module
            import csv
            rows = []
            with open(master_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) == len(header):
                        rows.append(row)
            df = pd.DataFrame(rows, columns=header)
            # Convert numeric columns
            for col in df.columns:
                if col not in ['Home', 'Away']:
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        pass
    
    # Meta columns that should always be included
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'home_points', 'away_points']
    
    if requested_features is None or len(requested_features) == 0:
        # Extract all features (just return master as-is or copy it)
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = master_path.replace('MASTER_TRAINING_points.csv', f'extracted_training_points_{timestamp}.csv')
        
        df.to_csv(output_path, index=False)
        return output_path
    
    # Check which requested features exist in master
    available_features = [f for f in requested_features if f in df.columns]
    missing_features = [f for f in requested_features if f not in df.columns]
    
    if missing_features:
        raise ValueError(
            f"Requested features not found in master CSV: {missing_features}. "
            f"Master needs to be regenerated to include all possible features."
        )
    
    # Extract columns: meta + requested features
    columns_to_extract = meta_cols + available_features
    extracted_df = df[columns_to_extract]
    
    # Write extracted CSV
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = master_path.replace('MASTER_TRAINING_points.csv', f'extracted_training_points_{timestamp}.csv')
    
    extracted_df.to_csv(output_path, index=False)
    
    return output_path


def check_master_points_needs_regeneration(
    db,
    requested_features: List[str]
) -> Tuple[bool, List[str]]:
    """
    Check if master points training data needs to be regenerated based on requested features.
    
    Args:
        db: MongoDB database connection
        requested_features: List of requested feature names
        
    Returns:
        Tuple of (needs_regeneration: bool, missing_features: List[str])
    """
    master_meta = get_master_training_points_metadata(db)
    
    if not master_meta:
        # No master exists - needs generation
        return True, requested_features
    
    master_features = set(master_meta.get('feature_list', []))
    requested_set = set(requested_features)
    
    missing_features = list(requested_set - master_features)
    
    if missing_features:
        return True, missing_features
    
    return False, []


def register_existing_master_points_csv(
    db,
    master_path: str = None,
    options: Dict = None
) -> Dict:
    """
    Register an existing master points training CSV file in MongoDB.
    Reads the CSV to extract feature list and latest date.
    
    Args:
        db: MongoDB database connection
        master_path: Path to existing master CSV (defaults to MASTER_TRAINING_POINTS_PATH)
        options: Optional dict with configuration options
        
    Returns:
        Metadata dict that was saved
    """
    master_path = master_path or MASTER_TRAINING_POINTS_PATH
    
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master points training CSV not found: {master_path}")
    
    print(f"Reading existing master points CSV: {master_path}")
    
    # Read CSV to get feature list and latest date
    # Handle potential CSV parsing errors
    try:
        df = pd.read_csv(master_path, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions
        try:
            df = pd.read_csv(master_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except:
            # Last resort: use csv module directly
            import csv
            rows = []
            with open(master_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) == len(header):
                        rows.append(row)
            df = pd.DataFrame(rows, columns=header)
            # Convert numeric columns
            for col in df.columns:
                if col not in ['Home', 'Away']:
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        pass
    
    # Meta columns that are not features
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'home_points', 'away_points']
    
    # Extract feature list
    feature_list = [col for col in df.columns if col not in meta_cols]
    feature_count = len(feature_list)
    
    # Find latest date in CSV
    if len(df) > 0:
        # Get the latest game date
        df_sorted = df.sort_values(['Year', 'Month', 'Day'], ascending=False)
        latest_row = df_sorted.iloc[0]
        last_date_updated = f"{int(latest_row['Year'])}-{int(latest_row['Month']):02d}-{int(latest_row['Day']):02d}"
    else:
        # Empty CSV - use today's date as placeholder
        last_date_updated = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Found {len(df)} games, {feature_count} features, latest date: {last_date_updated}")
    
    # Create/update metadata
    metadata_id = create_or_update_master_points_metadata(
        db,
        master_path,
        feature_list,
        feature_count,
        last_date_updated,
        options
    )
    
    print(f"Registered master points training data in MongoDB (ID: {metadata_id})")
    print(f"  Features: {feature_count}")
    print(f"  Games: {len(df)}")
    print(f"  Last updated: {last_date_updated}")
    
    return {
        'file_path': master_path,
        'feature_list': feature_list,
        'feature_count': feature_count,
        'last_date_updated': last_date_updated,
        'options': options or {},
        'game_count': len(df)
    }
