#!/usr/bin/env python3
"""Script to check master training data for pred_margin and understand ensemble training issue."""

import sys
import os
sys.path.append(os.getcwd())

import pandas as pd

def main():
    print("=== CHECKING MASTER TRAINING DATA ===")
    
    # Look for master training files
    master_path = "../master_training"
    if not os.path.exists(master_path):
        print(f"❌ Master training directory not found: {master_path}")
        return
    
    # Find master training CSV files
    csv_files = [f for f in os.listdir(master_path) if f.endswith('.csv') and 'MASTER' in f.upper()]
    if not csv_files:
        print("❌ No master training CSV files found")
        return
    
    print(f"Found master training files: {csv_files}")
    
    # Check the main master file
    master_file = None
    for f in csv_files:
        if 'MASTER_TRAINING.csv' in f:
            master_file = os.path.join(master_path, f)
            break
    
    if not master_file:
        print("❌ No MASTER_TRAINING.csv found")
        return
    
    print(f"\nChecking: {master_file}")
    
    try:
        # Read just first few rows to check columns
        df_sample = pd.read_csv(master_file, nrows=5)
        
        print(f"\n=== MASTER CSV COLUMN ANALYSIS ===")
        print(f"Total columns: {len(df_sample.columns)}")
        
        # Check for pred_margin specifically
        if 'pred_margin' in df_sample.columns:
            print(f"✅ pred_margin found in master training data!")
            print(f"Sample pred_margin values: {df_sample['pred_margin'].tolist()}")
            
            # Get column index
            pred_margin_idx = df_sample.columns.get_loc('pred_margin')
            print(f"pred_margin column index: {pred_margin_idx}")
        else:
            print(f"❌ pred_margin NOT found in master training CSV")
            
        # Check for prediction-related columns
        pred_cols = [col for col in df_sample.columns if 'pred' in col.lower()]
        if pred_cols:
            print(f"\nPrediction-related columns:")
            for col in pred_cols:
                print(f"  - {col}")
        
        # Show first 20 columns
        print(f"\nFirst 20 columns:")
        for i, col in enumerate(df_sample.columns[:20]):
            print(f"{i+1:2d}. {col}")
            
        # Show some feature columns that might be relevant
        feature_cols = [col for col in df_sample.columns if '|' in col and 'avg' in col][:10]
        if feature_cols:
            print(f"\nSample feature columns:")
            for col in feature_cols:
                print(f"  - {col}")
                
    except Exception as e:
        print(f"❌ Error reading master CSV: {e}")

if __name__ == "__main__":
    main()
