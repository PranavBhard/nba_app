#!/usr/bin/env python3
"""
Script to check MASTER_TRAINING CSV for:
1. _net features getting different values than their non-net counterparts
2. No duplicate features
3. No fully 0 columns
"""

import pandas as pd
import sys
import os

# Get the file path
file_path = '/Users/pranav/Desktop/MB2024Desktop/NBA/master_training/MASTER_TRAINING_limit-500.csv'

if not os.path.exists(file_path):
    print(f"ERROR: File not found: {file_path}")
    sys.exit(1)

print("=" * 80)
print("MASTER TRAINING CSV ANALYSIS")
print("=" * 80)
print(f"File: {file_path}\n")

# Read the CSV
try:
    df = pd.read_csv(file_path)
    print(f"✓ Loaded CSV: {len(df)} rows, {len(df.columns)} columns\n")
except Exception as e:
    print(f"ERROR: Failed to read CSV: {e}")
    sys.exit(1)

# 1. Check for duplicate column names
print("1. CHECKING FOR DUPLICATE COLUMNS")
print("-" * 80)
column_counts = {}
for col in df.columns:
    column_counts[col] = column_counts.get(col, 0) + 1

duplicates = {col: count for col, count in column_counts.items() if count > 1}
if duplicates:
    print(f"✗ FOUND {len(duplicates)} DUPLICATE COLUMN(S):")
    for col, count in duplicates.items():
        print(f"  - '{col}': appears {count} times")
    print()
else:
    print("✓ No duplicate columns found\n")

# 2. Check for fully zero columns
print("2. CHECKING FOR FULLY ZERO COLUMNS")
print("-" * 80)
meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
feature_cols = [col for col in df.columns if col not in meta_cols]

zero_columns = []
for col in feature_cols:
    if df[col].dtype in ['int64', 'float64']:
        if (df[col] == 0).all():
            zero_columns.append(col)

if zero_columns:
    print(f"✗ FOUND {len(zero_columns)} FULLY ZERO COLUMN(S):")
    for col in zero_columns[:20]:  # Show first 20
        print(f"  - {col}")
    if len(zero_columns) > 20:
        print(f"  ... and {len(zero_columns) - 20} more")
    print()
else:
    print("✓ No fully zero columns found\n")

# 3. Compare _net features with their non-net counterparts
print("3. COMPARING _net FEATURES WITH NON-net COUNTERPARTS")
print("-" * 80)

# Find all _net features
net_features = [col for col in feature_cols if '_net' in col]

if not net_features:
    print("✗ No _net features found!")
    print()
else:
    print(f"Found {len(net_features)} _net features\n")
    
    # Group by base stat name (remove _net and time period/calc_weight variations)
    comparisons = []
    
    for net_col in net_features:
        # Extract base stat name by removing _net and everything after the first |
        # e.g., "efg_net|season|raw|diff" -> "efg"
        base_name = net_col.split('_net')[0]
        
        # Find corresponding non-net feature
        # e.g., "efg_net|season|raw|diff" -> "efg|season|raw|diff"
        non_net_col = net_col.replace('_net', '')
        
        if non_net_col in df.columns:
            # Compare values
            net_values = df[net_col]
            non_net_values = df[non_net_col]
            
            # Check if they're identical (within floating point precision)
            are_identical = (net_values == non_net_values).all()
            
            # Calculate difference statistics
            differences = net_values - non_net_values
            max_diff = differences.abs().max()
            mean_diff = differences.abs().mean()
            
            comparisons.append({
                'net_feature': net_col,
                'non_net_feature': non_net_col,
                'identical': are_identical,
                'max_diff': max_diff,
                'mean_diff': mean_diff,
                'num_different': (differences.abs() > 1e-10).sum(),
                'num_total': len(df)
            })
        else:
            print(f"  ⚠️  No corresponding non-net feature found for: {net_col}")
    
    # Report results
    identical_count = sum(1 for c in comparisons if c['identical'])
    different_count = len(comparisons) - identical_count
    
    if identical_count > 0:
        print(f"✗ FOUND {identical_count} _net FEATURE(S) IDENTICAL TO NON-net:")
        for comp in comparisons:
            if comp['identical']:
                print(f"  - {comp['net_feature']} == {comp['non_net_feature']}")
        print()
    
    if different_count > 0:
        print(f"✓ {different_count} _net FEATURE(S) DIFFER FROM NON-net:")
        # Show top 10 with largest differences
        sorted_comps = sorted(comparisons, key=lambda x: x['max_diff'], reverse=True)
        for comp in sorted_comps[:10]:
            if not comp['identical']:
                pct_different = (comp['num_different'] / comp['num_total']) * 100
                print(f"  - {comp['net_feature']}")
                print(f"    vs {comp['non_net_feature']}")
                print(f"    Max diff: {comp['max_diff']:.6f}, Mean diff: {comp['mean_diff']:.6f}")
                print(f"    {comp['num_different']}/{comp['num_total']} ({pct_different:.1f}%) rows differ")
                print()
    
    if len(comparisons) == 0:
        print("⚠️  No valid comparisons found\n")

# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
issues = []
if duplicates:
    issues.append(f"{len(duplicates)} duplicate column(s)")
if zero_columns:
    issues.append(f"{len(zero_columns)} fully zero column(s)")
if 'comparisons' in locals():
    identical_net = sum(1 for c in comparisons if c['identical'])
    if identical_net > 0:
        issues.append(f"{identical_net} _net feature(s) identical to non-net")

if issues:
    print("✗ ISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ ALL CHECKS PASSED!")
    print("  - No duplicate columns")
    print("  - No fully zero columns")
    print("  - All _net features differ from non-net counterparts")
print()

