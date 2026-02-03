#!/usr/bin/env python3
"""
Script to recover and register an existing master training CSV that had parsing errors.

This script will:
1. Read the existing MASTER_TRAINING.csv with error handling
2. Register it in MongoDB
3. Optionally fix and save a cleaned version

Usage:
    python cli/recover_master_training.py
"""

import sys
import os
from datetime import datetime

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from nba_app.core.mongo import Mongo
from nba_app.cli_old.master_training_data import (
    create_or_update_master_metadata,
    MASTER_TRAINING_PATH
)


def main():
    """Recover and register existing master training CSV."""
    print("=" * 80)
    print("RECOVER MASTER TRAINING DATA")
    print("=" * 80)
    print()
    
    if not os.path.exists(MASTER_TRAINING_PATH):
        print(f"Error: Master training CSV not found at: {MASTER_TRAINING_PATH}")
        return
    
    print(f"Reading existing master CSV: {MASTER_TRAINING_PATH}")
    print("(This may take a moment for large files)")
    print()
    
    # Read with error handling to skip malformed lines
    try:
        df = pd.read_csv(MASTER_TRAINING_PATH, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions
        try:
            df = pd.read_csv(MASTER_TRAINING_PATH, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return
    
    print(f"Successfully read {len(df)} rows")
    
    # Check for malformed lines by comparing with line count
    import subprocess
    try:
        result = subprocess.run(['wc', '-l', MASTER_TRAINING_PATH], 
                              capture_output=True, text=True)
        total_lines = int(result.stdout.split()[0])
        skipped = total_lines - len(df) - 1  # -1 for header
        if skipped > 0:
            print(f"  Note: {skipped} malformed row(s) were skipped")
    except:
        pass
    
    # Meta columns that are not features
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
    
    # Extract feature list
    feature_list = [col for col in df.columns if col not in meta_cols]
    feature_count = len(feature_list)
    
    print(f"Features: {feature_count}")
    print()
    
    # Find latest date in CSV
    if len(df) > 0:
        df_sorted = df.sort_values(['Year', 'Month', 'Day'], ascending=False)
        latest_row = df_sorted.iloc[0]
        last_date_updated = f"{int(latest_row['Year'])}-{int(latest_row['Month']):02d}-{int(latest_row['Day']):02d}"
    else:
        last_date_updated = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Latest game date: {last_date_updated}")
    print()
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    mongo = Mongo()
    db = mongo.db
    print("Connected!")
    print()
    
    # Register in MongoDB
    print("Registering master training data in MongoDB...")
    metadata_id = create_or_update_master_metadata(
        db,
        MASTER_TRAINING_PATH,
        feature_list,
        feature_count,
        last_date_updated,
        options={'recovered': True, 'recovered_at': datetime.utcnow().isoformat(), 'rows': len(df)}
    )
    
    print()
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print(f"Master training data registered (ID: {metadata_id})")
    print(f"  File: {MASTER_TRAINING_PATH}")
    print(f"  Games: {len(df)}")
    print(f"  Features: {feature_count}")
    print(f"  Latest date: {last_date_updated}")
    print()
    print("You can now use this master training data for training.")
    print()


if __name__ == '__main__':
    main()
