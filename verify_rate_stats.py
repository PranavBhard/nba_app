#!/usr/bin/env python3
"""
Verify that all rate stats follow the correct rules:
- "avg" = calculate stat for each game, then average those values
- "raw" = aggregate all games first, then calculate stat from aggregated totals
"""

import pandas as pd
import sys

# Read the CSV
file_path = '/Users/pranav/Desktop/MB2024Desktop/NBA/master_training/MASTER_TRAINING_limit-500.csv'
df = pd.read_csv(file_path)

# Rate stats (from StatHandlerV2.py)
rate_stats = {
    'effective_fg_perc', 'true_shooting_perc', 'three_perc',
    'off_rtg', 'def_rtg', 'assists_ratio', 'TO_metric', 'ast_to_ratio'
}

print("=" * 80)
print("VERIFYING RATE STAT CALCULATION RULES")
print("=" * 80)
print()

# Find all rate stat features
rate_features = []
for col in df.columns:
    # Extract base stat name (before first |)
    base_name = col.split('|')[0]
    if base_name in rate_stats:
        rate_features.append((col, base_name))

print(f"Found {len(rate_features)} rate stat features\n")

# Group by stat and check raw vs avg
issues = []
for base_stat in rate_stats:
    stat_features = [f for f, b in rate_features if b == base_stat]
    raw_features = [f for f in stat_features if '|raw|' in f]
    avg_features = [f for f in stat_features if '|avg|' in f]
    
    if raw_features or avg_features:
        print(f"{base_stat}:")
        print(f"  Raw features: {len(raw_features)}")
        print(f"  Avg features: {len(avg_features)}")
        
        # Check if raw features are all zero
        for rf in raw_features:
            if rf in df.columns:
                non_zero = (df[rf] != 0).sum()
                if non_zero == 0:
                    issues.append(f"{rf} is all zeros (should aggregate first, then calculate)")
                    print(f"    ⚠️  {rf}: ALL ZEROS")
                else:
                    print(f"    ✓ {rf}: {non_zero}/{len(df)} non-zero values")
        
        # Check if avg features have values
        for af in avg_features:
            if af in df.columns:
                non_zero = (df[af] != 0).sum()
                print(f"    ✓ {af}: {non_zero}/{len(df)} non-zero values")
        print()

# Check specific ast_to_ratio issue
print("=" * 80)
print("SPECIFIC CHECK: ast_to_ratio")
print("=" * 80)
ast_to_ratio_cols = [c for c in df.columns if 'ast_to_ratio' in c]
print(f"Found {len(ast_to_ratio_cols)} ast_to_ratio columns:\n")

for col in ast_to_ratio_cols:
    non_zero = (df[col] != 0).sum()
    calc_type = 'raw' if '|raw|' in col else 'avg' if '|avg|' in col else 'unknown'
    print(f"  {col}")
    print(f"    Type: {calc_type}")
    print(f"    Non-zero: {non_zero}/{len(df)}")
    if non_zero > 0:
        print(f"    Min: {df[col].min():.6f}, Max: {df[col].max():.6f}, Mean: {df[col].mean():.6f}")
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
if issues:
    print("✗ ISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ All rate stats appear to be calculated correctly")
print()

