#!/usr/bin/env python3
"""
Script to find all columns in MASTER_TRAINING.csv that have all zeros.
"""

import sys
import os
import pandas as pd

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Path to master training CSV
master_training_path = os.path.join(project_root, 'master_training', 'MASTER_TRAINING.csv')

if not os.path.exists(master_training_path):
    print(f"Error: Master training file not found at {master_training_path}")
    sys.exit(1)

print(f"Loading {master_training_path}...")
df = pd.read_csv(master_training_path)

print(f"Total columns: {len(df.columns)}")
print(f"Total rows: {len(df)}")
print()

# Find columns that are all zeros
zero_columns = []
for col in df.columns:
    # Skip meta columns
    if col in ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']:
        continue
    
    # Check if all values are zero (or NaN converted to 0)
    col_data = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if (col_data == 0).all():
        zero_columns.append(col)

print(f"Found {len(zero_columns)} columns with all zeros:")
print("=" * 80)
for col in sorted(zero_columns):
    print(col)

print()
print("=" * 80)
print(f"Total: {len(zero_columns)} columns")

