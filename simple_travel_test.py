#!/usr/bin/env python3
"""
Simple test to verify travel features without complex imports
"""
import sys
import os

# Add current directory to front of Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Direct import without package prefix
try:
    import cli.master_training_data
    
    print("Testing get_all_possible_features...")
    features = cli.master_training_data.get_all_possible_features(no_player=False)
    
    # Check for travel|days_2 features specifically
    travel_days_2_features = [f for f in features if 'travel|days_2' in f]
    
    print(f'\nTravel|days_2 features found: {len(travel_days_2_features)}')
    for f in sorted(travel_days_2_features):
        print(f'  {f}')
    
    # Check for all travel features
    all_travel_features = [f for f in features if 'travel|' in f]
    print(f'\nAll travel features found: {len(all_travel_features)}')
    
    # Success message
    if travel_days_2_features:
        print('\n✅ SUCCESS: travel|days_2 features are now included!')
    else:
        print('\n❌ ISSUE: travel|days_2 features not found')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
