#!/usr/bin/env python3
"""Test the pred_margin fix directly in stacking tool."""

import sys
import os
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
from agents.tools.stacking_tool import StackingTrainer

def test_stacking_with_pred_margin():
    """Test that pred_margin is included when requested as meta-feature."""
    
    print("=== TESTING STACKING TOOL WITH PRED_MARGIN ===")
    
    # Create mock DataFrame that simulates master training data
    df = pd.DataFrame({
        'Year': [2023, 2023, 2023],
        'Month': [1, 1, 1],
        'Day': [1, 2, 3],
        'Home': ['TeamA', 'TeamB', 'TeamC'],
        'Away': ['TeamX', 'TeamY', 'TeamZ'],
        'game_id': ['game1', 'game2', 'game3'],
        'SeasonStartYear': [2022, 2022, 2022],
        'HomeWon': [1, 0, 1],
        'pred_margin': [5.1, -2.3, 8.7],  # This should be included
        'elo|none|raw|diff': [120.5, -45.2, 200.1],
        'pace|season|avg|diff': [3.2, -1.1, 5.5]
    })
    
    # Mock base models info
    base_models_info = [
        {
            'run_id': 'test_model_1',
            'model': None,  # We'll mock predictions
            'scaler': None,
            'feature_names': ['elo|none|raw|diff']
        }
    ]
    
    # Create stacking trainer
    trainer = StackingTrainer()
    
    # Test the _generate_stacking_data method directly
    try:
        stacking_df = trainer._generate_stacking_data(
            df=df,
            base_models_info=base_models_info,
            meta_features=['pred_margin'],  # Explicitly request pred_margin
            use_disagree=False,
            use_conf=False,
            calibration_years=[]  # Add missing parameter
        )
        
        print(f"✅ Stacking dataset created successfully!")
        print(f"Columns in stacking dataset: {list(stacking_df.columns)}")
        
        # Check if pred_margin is included
        if 'pred_margin' in stacking_df.columns:
            print("✅ SUCCESS: pred_margin is included in stacking dataset!")
            
            # Show some sample values
            pred_margin_values = stacking_df['pred_margin'].values
            print(f"Sample pred_margin values: {pred_margin_values}")
        else:
            print("❌ FAILURE: pred_margin is still missing from stacking dataset!")
            
        # Show all columns except HomeWon
        feature_cols = [c for c in stacking_df.columns if c != 'HomeWon']
        print(f"\\nFeature columns ({len(feature_cols)}): {feature_cols}")
        
    except Exception as e:
        print(f"❌ Error during stacking: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_stacking_with_pred_margin()
