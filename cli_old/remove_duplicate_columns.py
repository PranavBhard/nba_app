#!/usr/bin/env python3
"""
Script to remove duplicate column headers from MASTER_TRAINING.csv.

This script:
1. Reads the existing MASTER_TRAINING.csv
2. Identifies duplicate column names
3. Removes duplicate columns (keeps first occurrence)
4. Writes cleaned CSV back to the same file (with backup)
"""

import os
import sys
import csv
import shutil
from collections import Counter
from datetime import datetime

# Get the master training CSV path (same logic as master_training_data.py)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Script is in nba_app/cli/, so go up two levels to get to NBA/ (project root)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(script_dir))  # NBA/
_PARENT_ROOT = os.path.dirname(_PROJECT_ROOT)  # Parent of NBA/ (MB2024Desktop/)
# According to master_training_data.py, master_training is in _PARENT_ROOT, but actually it's in _PROJECT_ROOT
# Let's check both locations
MASTER_TRAINING_PATH = os.path.join(_PROJECT_ROOT, 'master_training', 'MASTER_TRAINING.csv')
if not os.path.exists(MASTER_TRAINING_PATH):
    # Try parent root location (as per master_training_data.py logic)
    MASTER_TRAINING_PATH = os.path.join(_PARENT_ROOT, 'master_training', 'MASTER_TRAINING.csv')

# Allow override via command line argument
if len(sys.argv) > 1:
    MASTER_TRAINING_PATH = sys.argv[1]


def remove_duplicate_columns(csv_path: str, backup: bool = True) -> dict:
    """
    Remove duplicate columns from CSV file.
    
    Args:
        csv_path: Path to CSV file
        backup: If True, create a backup before modifying
        
    Returns:
        Dict with stats about removed duplicates
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at: {csv_path}")
        return None
    
    # Create backup
    if backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = csv_path.replace('.csv', f'_backup_{timestamp}.csv')
        print(f"Creating backup: {backup_path}")
        shutil.copy2(csv_path, backup_path)
    
    # Read CSV headers
    print(f"Reading CSV: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    # Find duplicate headers
    header_counts = Counter(headers)
    duplicates = {header: count for header, count in header_counts.items() if count > 1}
    
    if not duplicates:
        print("No duplicate headers found. CSV is already clean.")
        return {
            'total_headers': len(headers),
            'unique_headers': len(set(headers)),
            'duplicates_removed': 0,
            'duplicate_headers': {}
        }
    
    print(f"\nFound {len(duplicates)} duplicate header(s):")
    for header, count in sorted(duplicates.items()):
        print(f"  '{header}': appears {count} times")
    
    # Build mapping: keep first occurrence of each header, skip subsequent duplicates
    seen = set()
    keep_indices = []
    duplicate_indices = []
    
    for i, header in enumerate(headers):
        if header not in seen:
            seen.add(header)
            keep_indices.append(i)
        else:
            duplicate_indices.append(i)
            print(f"  Removing duplicate column {i}: '{header}'")
    
    # Write cleaned CSV
    print(f"\nWriting cleaned CSV (keeping {len(keep_indices)} columns, removing {len(duplicate_indices)} duplicates)...")
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write cleaned headers
        cleaned_headers = [headers[i] for i in keep_indices]
        writer.writerow(cleaned_headers)
        
        # Write cleaned rows
        for row in rows:
            cleaned_row = [row[i] if i < len(row) else '' for i in keep_indices]
            writer.writerow(cleaned_row)
    
    print(f"✓ Successfully removed {len(duplicate_indices)} duplicate column(s)")
    print(f"  Original columns: {len(headers)}")
    print(f"  Cleaned columns: {len(cleaned_headers)}")
    
    return {
        'total_headers': len(headers),
        'unique_headers': len(set(headers)),
        'duplicates_removed': len(duplicate_indices),
        'duplicate_headers': duplicates,
        'removed_indices': duplicate_indices
    }


if __name__ == '__main__':
    print("=" * 80)
    print("Remove Duplicate Columns from MASTER_TRAINING.csv")
    print("=" * 80)
    print()
    
    result = remove_duplicate_columns(MASTER_TRAINING_PATH, backup=True)
    
    if result:
        print()
        print("=" * 80)
        print("Summary:")
        print(f"  Total headers: {result['total_headers']}")
        print(f"  Unique headers: {result['unique_headers']}")
        print(f"  Duplicates removed: {result['duplicates_removed']}")
        print("=" * 80)
        print()
        print("Done!")

