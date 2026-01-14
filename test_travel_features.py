#!/usr/bin/env python3
"""
Test script to verify travel features are included in get_all_possible_features
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    # Change working directory to project root
    os.chdir(project_root)
    
    from cli.master_training_data import get_all_possible_features
    
    print("Testing get_all_possible_features...")
    features = get_all_possible_features(no_player=False)
    travel_features = [f for f in features if 'travel' in f]
    
    print(f'\nTravel features found ({len(travel_features)}):')
    for feature in sorted(travel_features):
        print(f'  {feature}')
    
    print(f'\nTotal features: {len(features)}')
    
    # Test a few other features to make sure they're working
    elo_features = [f for f in features if 'elo' in f]
    rest_features = [f for f in features if 'rest' in f and 'travel' not in f]
    
    print(f'\nELO features found ({len(elo_features)}):')
    for feature in sorted(elo_features)[:3]:  # Show first 3
        print(f'  {feature}')
    
    print(f'\nRest features found ({len(rest_features)}):')
    for feature in sorted(rest_features)[:3]:  # Show first 3
        print(f'  {feature}')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
