"""
Dataset Augmenter Tool - Merge new feature columns with existing datasets
"""

import sys
import os
import pandas as pd
import hashlib
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.cli.Mongo import Mongo
from nba_app.cli.master_training_data import MASTER_TRAINING_PATH


class DatasetAugmenter:
    """Augments existing datasets with new feature columns"""
    
    def __init__(self, db=None):
        """
        Initialize DatasetAugmenter.
        
        Args:
            db: MongoDB database instance (optional)
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        # Cache directory for augmented datasets
        self.cache_dir = os.path.join(parent_dir, 'model_output', 'dataset_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def augment_dataset(
        self,
        master_features: List[str],
        new_feature_csv_path: str,
        date_range: Optional[Dict] = None
    ) -> Dict:
        """
        Merge new feature columns with existing dataset from master training.
        
        Args:
            master_features: List of existing feature names to include from master training
            new_feature_csv_path: Path to CSV file with new feature columns (must include metadata: Year, Month, Day, Home, Away, HomeWon)
            date_range: Optional dict with 'begin_year', 'end_year', 'begin_date', 'end_date' to filter master data
            
        Returns:
            Dict with:
                - dataset_id: Unique identifier for the augmented dataset
                - csv_path: Path to augmented CSV file
                - schema: Dataset schema
                - row_count: Number of rows
                - feature_count: Number of features (excluding metadata)
        """
        # Validate new feature CSV exists
        if not os.path.exists(new_feature_csv_path):
            raise ValueError(f"New feature CSV not found: {new_feature_csv_path}")
        
        # Load new feature CSV
        try:
            new_df = pd.read_csv(new_feature_csv_path)
        except Exception as e:
            raise ValueError(f"Failed to read new feature CSV: {e}")
        
        # Validate required metadata columns
        required_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
        missing_cols = [col for col in required_cols if col not in new_df.columns]
        if missing_cols:
            raise ValueError(f"New feature CSV missing required metadata columns: {missing_cols}")
        
        # Get new feature columns (exclude metadata)
        new_feature_cols = [c for c in new_df.columns if c not in required_cols]
        if not new_feature_cols:
            raise ValueError("New feature CSV has no feature columns (only metadata)")
        
        # Load master training CSV
        if not os.path.exists(MASTER_TRAINING_PATH):
            raise ValueError(f"Master training CSV not found: {MASTER_TRAINING_PATH}")
        
        try:
            master_df = pd.read_csv(MASTER_TRAINING_PATH)
        except Exception as e:
            raise ValueError(f"Failed to read master training CSV: {e}")
        
        # Apply date/year filters to master
        if date_range:
            if 'begin_year' in date_range:
                master_df = master_df[master_df['Year'] >= date_range['begin_year']]
            if 'end_year' in date_range:
                master_df = master_df[master_df['Year'] <= date_range['end_year']]
            if 'begin_date' in date_range:
                master_df['Date'] = pd.to_datetime(master_df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1))
                begin_dt = pd.to_datetime(date_range['begin_date'])
                master_df = master_df[master_df['Date'] >= begin_dt]
                master_df = master_df.drop('Date', axis=1)
            if 'end_date' in date_range:
                if 'Date' not in master_df.columns:
                    master_df['Date'] = pd.to_datetime(master_df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1))
                end_dt = pd.to_datetime(date_range['end_date'])
                master_df = master_df[master_df['Date'] <= end_dt]
                master_df = master_df.drop('Date', axis=1)
        
        # Extract requested features from master
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
        master_feature_cols = [c for c in master_df.columns if c not in meta_cols]
        
        # Filter to requested master features
        requested_master_features = [f for f in master_features if f in master_feature_cols]
        missing_master_features = [f for f in master_features if f not in master_feature_cols]
        
        if missing_master_features:
            print(f"  [WARNING] {len(missing_master_features)} requested master features not found: {missing_master_features[:5]}...")
        
        # Select columns from master
        master_selected_cols = meta_cols + requested_master_features
        master_subset = master_df[master_selected_cols].copy()
        
        # Merge on (Year, Month, Day, Home, Away)
        merge_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        
        # Prepare new feature DataFrame for merge (only metadata + new features)
        new_feature_subset = new_df[merge_cols + new_feature_cols + ['HomeWon']].copy()
        
        # Perform merge
        merged_df = master_subset.merge(
            new_feature_subset,
            on=merge_cols,
            how='inner',  # Only keep games that exist in both
            suffixes=('', '_new')
        )
        
        # Check for merge issues
        if len(merged_df) == 0:
            raise ValueError(
                "Merge resulted in 0 rows. Check that games in new feature CSV match games in master training "
                "(same Year, Month, Day, Home, Away values)."
            )
        
        # Handle HomeWon column (should be from master, but verify)
        if 'HomeWon_new' in merged_df.columns:
            # Both have HomeWon, use master's version
            merged_df = merged_df.drop('HomeWon_new', axis=1)
        
        # Check for missing games
        master_game_count = len(master_subset)
        merged_game_count = len(merged_df)
        if merged_game_count < master_game_count:
            missing_count = master_game_count - merged_game_count
            print(f"  [WARNING] {missing_count} games from master training not found in new feature CSV")
        
        # Ensure HomeWon is the last column
        feature_cols = [c for c in merged_df.columns if c not in meta_cols]
        col_order = meta_cols[:-1] + feature_cols + ['HomeWon']  # HomeWon last
        merged_df = merged_df[col_order]
        
        # Generate dataset ID
        dataset_spec_str = f"{sorted(master_features)}|{sorted(new_feature_cols)}|{date_range}|{new_feature_csv_path}"
        dataset_id = hashlib.md5(dataset_spec_str.encode()).hexdigest()[:16]
        
        # Save augmented dataset
        cache_file = os.path.join(self.cache_dir, f'dataset_{dataset_id}.csv')
        merged_df.to_csv(cache_file, index=False)
        
        # Generate schema
        schema = {
            'metadata_columns': meta_cols,
            'master_features': requested_master_features,
            'new_features': new_feature_cols,
            'total_features': len(requested_master_features) + len(new_feature_cols),
            'row_count': len(merged_df)
        }
        
        print(f"  [INFO] Augmented dataset created: {len(merged_df)} rows, {schema['total_features']} features")
        print(f"  [INFO] Master features: {len(requested_master_features)}, New features: {len(new_feature_cols)}")
        
        from nba_app.agents.utils.json_compression import encode_tool_output
        
        return encode_tool_output({
            'dataset_id': dataset_id,
            'csv_path': cache_file,
            'schema': schema,
            'row_count': len(merged_df),
            'feature_count': schema['total_features']
        })

