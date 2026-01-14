#!/usr/bin/env python3
"""
Test script to verify ALL travel features are included in get_all_possible_features
"""
import sys
import os

# Add current directory to FRONT of Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from cli.master_training_data import get_all_possible_features
    
    print("Testing get_all_possible_features...")
    features = get_all_possible_features(no_player=False)
    
    # Check for all travel features
    travel_patterns = [
        'travel|days_2|avg',
        'travel|days_5|avg', 
        'travel|days_12|avg'
    ]
    
    found_features = []
    for pattern in travel_patterns:
        matching = [f for f in features if pattern in f]
        found_features.extend(matching)
        print(f'{pattern}: {len(matching)} features')
        for f in sorted(matching)[:3]:  # Show first 3
            print(f'  {f}')
    
    print(f'\nTotal travel features found: {len(found_features)}')
    print(f'Total features overall: {len(features)}')
    
    # Verify all expected travel features are present
    expected_travel_features = [
        'travel|days_2|avg|diff',
        'travel|days_2|avg|home',
        'travel|days_2|avg|away',
        'travel|days_5|avg|diff',
        'travel|days_5|avg|home',
        'travel|days_5|avg|away',
        'travel|days_12|avg|diff',
        'travel|days_12|avg|home',
        'travel|days_12|avg|away',
    ]
    
    missing_expected = [f for f in expected_travel_features if f not in features]
    if missing_expected:
        print(f'\nMISSING expected travel features:')
        for f in missing_expected:
            print(f'  {f}')
    else:
        print('\n✅ All expected travel features are present!')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
