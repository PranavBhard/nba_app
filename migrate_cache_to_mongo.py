#!/usr/bin/env python3
"""
Migration script to populate model_config_nba collection from cached JSON files.
"""

import sys
import os
import json
import hashlib
from datetime import datetime

# Add parent directory to path (go up to find nba_app package)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.cli.Mongo import Mongo
import pandas as pd

def generate_feature_set_hash(features: list) -> str:
    """Generate MD5 hash of sorted feature list."""
    features_sorted = sorted(features)
    features_str = ','.join(features_sorted)
    return hashlib.md5(features_str.encode()).hexdigest()

def sanitize_nan(value):
    """Convert NaN, Infinity, and -Infinity to None for JSON serialization."""
    if isinstance(value, (float,)):
        import math
        if math.isnan(value):
            return None
        elif math.isinf(value):
            return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

def get_features_from_csv(csv_path: str) -> list:
    """Extract feature names from training CSV."""
    try:
        # Handle relative paths
        if not os.path.isabs(csv_path):
            csv_path = os.path.join(os.path.dirname(__file__), csv_path)
        
        if not os.path.exists(csv_path):
            print(f"Warning: CSV file not found: {csv_path}")
            return None
        
        df = pd.read_csv(csv_path, nrows=0)  # Read only headers
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        return feature_cols
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
        return None

def migrate_cache_file(cache_file: str, mongo_db, is_no_per: bool = False):
    """Migrate a single cache file to MongoDB."""
    print(f"\nProcessing {cache_file}...")
    
    if not os.path.exists(cache_file):
        print(f"Cache file not found: {cache_file}")
        return
    
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    if not cache.get('configs'):
        print("No configs found in cache file")
        return
    
    # Get features from CSV
    training_csv = cache.get('training_csv')
    features = None
    if training_csv:
        features = get_features_from_csv(training_csv)
    
    # If CSV read failed, try to use rated_features from configs (union of all)
    if features is None:
        print("Could not read CSV, using rated_features from configs...")
        all_rated_features = set()
        for config in cache['configs']:
            if config.get('rated_features'):
                all_rated_features.update(config['rated_features'])
        features = sorted(list(all_rated_features)) if all_rated_features else []
        print(f"Extracted {len(features)} features from rated_features")
    
    if not features:
        print("Warning: No features found, skipping migration")
        return
    
    # Generate feature set hash
    feature_set_hash = generate_feature_set_hash(features)
    print(f"Feature set hash: {feature_set_hash[:8]}... ({len(features)} features)")
    
    # Group configs by model_type
    model_configs = {}
    for config in cache['configs']:
        model_type = config.get('model_type')
        if not model_type:
            continue
        
        if model_type not in model_configs:
            model_configs[model_type] = {
                'results': [],
                'best': None,
                'best_acc': -1
            }
        
        model_configs[model_type]['results'].append(config)
        
        # Track best result
        acc = config.get('accuracy_mean', 0.0) or 0.0
        if acc > model_configs[model_type]['best_acc']:
            model_configs[model_type]['best_acc'] = acc
            model_configs[model_type]['best'] = config
    
    # Save each model type
    timestamp_str = cache.get('timestamp', 'unknown')
    try:
        # Parse timestamp (format: YYYYMMDD_HHMMSS)
        trained_at = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
    except:
        trained_at = datetime.utcnow()
    
    saved_count = 0
    for model_type, mt_data in model_configs.items():
        best_result = mt_data['best']
        if not best_result:
            continue
        
        # Build C-values dict
        c_values_dict = None
        best_c_value = None
        best_c_accuracy = None
        
        # Check if this model supports C-values (LogisticRegression, SVM)
        if model_type in ['LogisticRegression', 'SVM']:
            c_values_dict = {}
            for res in mt_data['results']:
                c_val = res.get('c_value')
                acc = res.get('accuracy_mean', 0.0) or 0.0
                if c_val is not None:
                    c_values_dict[c_val] = acc
                    if acc > (best_c_accuracy or -1):
                        best_c_accuracy = acc
                        best_c_value = c_val
        
        # Build feature rankings (use rated_features from best config if available)
        features_ranked = []
        if best_result.get('rated_features'):
            # We don't have F-scores in the cache, so just use order as rank
            for rank, feature_name in enumerate(best_result['rated_features'], 1):
                features_ranked.append({
                    'rank': rank,
                    'name': feature_name,
                    'score': None  # No score available in cache
                })
        
        # Check if config already exists
        existing = mongo_db.model_config_nba.find_one({
            'model_type': model_type,
            'feature_set_hash': feature_set_hash
        })
        
        # Prepare update document
        update_doc = {
            'model_type': model_type,
            'feature_set_hash': feature_set_hash,
            'features': sorted(features),
            'feature_count': len(features),
            'accuracy': sanitize_nan(best_result.get('accuracy_mean', 0.0)),
            'std_dev': sanitize_nan(best_result.get('accuracy_std', 0.0)),
            'brier_score': sanitize_nan(best_result.get('brier_mean', 0.0)),
            'log_loss': sanitize_nan(best_result.get('log_loss_mean', 0.0)),
            'features_ranked': features_ranked,
            'updated_at': datetime.utcnow(),
            'training_stats': {
                'total_games': cache.get('game_count'),
                'include_enhanced_features': True,  # Assume True for cached models
                'include_era_normalization': False,  # Assume False (can't determine from cache)
                'no_per': is_no_per,
                'model_specific_features': False  # Assume False (can't determine from cache)
            }
        }
        
        if c_values_dict:
            c_values_dict_str = {}
            for c_val, acc in c_values_dict.items():
                c_values_dict_str[str(c_val)] = sanitize_nan(acc)
            update_doc['c_values'] = c_values_dict_str
        
        if best_c_value is not None:
            update_doc['best_c_value'] = sanitize_nan(best_c_value)
        if best_c_accuracy is not None:
            update_doc['best_c_accuracy'] = sanitize_nan(best_c_accuracy)
        
        if training_csv:
            update_doc['training_csv'] = training_csv
        
        # Handle selected flag (select best config from cache if it's the best overall)
        if cache.get('best') and cache['best'].get('model_type') == model_type:
            # This is the best config, mark as selected (but unset others first)
            mongo_db.model_config_nba.update_many(
                {'selected': True},
                {'$set': {'selected': False}}
            )
            update_doc['selected'] = True
        elif existing:
            update_doc['selected'] = existing.get('selected', False)
        else:
            # New config: only select if no other selected config exists
            existing_selected = mongo_db.model_config_nba.find_one({'selected': True})
            update_doc['selected'] = (existing_selected is None)
        
        # Preserve custom name if exists
        if existing and existing.get('name'):
            existing_name = existing['name']
            auto_name_prefix = f"{model_type} - {feature_set_hash[:8]}"
            if not existing_name.startswith(auto_name_prefix):
                update_doc['name'] = existing_name
            else:
                update_doc['name'] = f"{model_type} - {feature_set_hash[:8]}"
        else:
            update_doc['name'] = f"{model_type} - {feature_set_hash[:8]}"
        
        # Set trained_at timestamp
        if not existing:
            update_doc['trained_at'] = trained_at
        elif 'trained_at' not in existing:
            update_doc['trained_at'] = trained_at
        
        # Upsert
        result = mongo_db.model_config_nba.update_one(
            {
                'model_type': model_type,
                'feature_set_hash': feature_set_hash
            },
            {'$set': update_doc},
            upsert=True
        )
        
        saved_count += 1
        print(f"  ✓ Saved {model_type} (accuracy: {best_result.get('accuracy_mean', 0):.2f}%)")
    
    print(f"Migrated {saved_count} model configuration(s) from {cache_file}")

def main():
    """Main migration function."""
    print("=" * 60)
    print("Migrating cached model results to MongoDB")
    print("=" * 60)
    
    # Initialize MongoDB
    mongo = Mongo()
    db = mongo.db
    
    # Cache file paths
    cache_file = './model_output/cache_model_config.json'
    cache_file_no_per = './model_output/cache_model_config_no_per.json'
    
    # Migrate both cache files
    if os.path.exists(cache_file):
        migrate_cache_file(cache_file, db, is_no_per=False)
    else:
        print(f"Cache file not found: {cache_file}")
    
    if os.path.exists(cache_file_no_per):
        migrate_cache_file(cache_file_no_per, db, is_no_per=True)
    else:
        print(f"Cache file not found: {cache_file_no_per}")
    
    # Print summary
    total_configs = db.model_config_nba.count_documents({})
    selected_configs = db.model_config_nba.count_documents({'selected': True})
    
    print("\n" + "=" * 60)
    print("Migration complete!")
    print(f"Total configs in MongoDB: {total_configs}")
    print(f"Selected configs: {selected_configs}")
    print("=" * 60)

if __name__ == '__main__':
    main()

