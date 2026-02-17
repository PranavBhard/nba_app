#!/usr/bin/env python3
"""Test script to verify the pred_margin fix works."""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd

def test_stacking_logic():
    """Test the fixed stacking tool logic."""
    
    # Simulate the fixed logic
    meta_features = ['pred_margin']  # User requested pred_margin
    
    # Simulate DataFrame columns (from master training data)
    df_columns = [
        'Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'SeasonStartYear',
        'HomeWon', 'pred_home_points', 'pred_away_points', 'pred_margin', 
        'pred_point_total', 'elo|none|raw|diff', 'pace|season|avg|diff'
    ]
    
    print("=== TESTING FIXED STACKING LOGIC ===")
    print(f"Requested meta features: {meta_features}")
    print(f"DataFrame has pred_margin: {'pred_margin' in df_columns}")
    
    # Test first location (lines 680-689)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'SeasonStartYear']
    target_cols = ['HomeWon']
    excluded_cols = meta_cols + target_cols
    
    # FIXED: Exclude prediction columns EXCEPT those explicitly requested as meta-features
    pred_cols = ['pred_home_points', 'pred_away_points', 'pred_point_total']
    # Only exclude pred_margin if NOT explicitly requested as meta-feature
    if 'pred_margin' not in meta_features:
        pred_cols.append('pred_margin')
    excluded_cols.extend([c for c in pred_cols if c in df_columns])
    
    print(f"\nFirst location - Excluded columns: {excluded_cols}")
    print(f"pred_margin excluded: {'pred_margin' in excluded_cols}")
    
    # Test second location (lines 777-786)
    available_features = set(df_columns)
    meta_cols2 = ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'SeasonStartYear']
    target_cols2 = ['HomeWon']
    
    # FIXED: Exclude prediction columns EXCEPT those explicitly requested as meta-features
    pred_cols_exclude = ['pred_home_points', 'pred_away_points', 'pred_point_total']
    # Only exclude pred_margin if NOT explicitly requested as meta-feature
    if 'pred_margin' not in meta_features:
        pred_cols_exclude.append('pred_margin')
    excluded_cols2 = set(meta_cols2 + target_cols2 + [c for c in pred_cols_exclude if c in df_columns])
    
    print(f"\nSecond location - Excluded columns: {excluded_cols2}")
    print(f"pred_margin excluded: {'pred_margin' in excluded_cols2}")
    
    # Test if pred_margin would be included
    for feat_name in meta_features:
        if feat_name in excluded_cols2:
            print(f"❌ Meta-feature '{feat_name}' would be excluded")
        elif feat_name in available_features:
            print(f"✅ Meta-feature '{feat_name}' would be included")
        else:
            print(f"❌ Meta-feature '{feat_name}' not found in dataset")

if __name__ == "__main__":
    test_stacking_logic()
