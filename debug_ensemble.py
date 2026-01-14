#!/usr/bin/env python3
"""Script to examine the selected ensemble model config and master training data."""

import sys
import os
sys.path.append(os.getcwd())

from pymongo import MongoClient
from config import config

class Mongo:
    def __init__(self):
        self.client = MongoClient(config["mongo_conn_str"])
        self.db = self.client.heroku_jrgd55fg

def main():
    mongo = Mongo()
    db = mongo.db
    
    # Get selected model config
    selected_config = db.model_config_nba.find_one({'selected': True})
    
    if not selected_config:
        print("❌ No selected model config found")
        return
    
    print("=== SELECTED MODEL CONFIG ===")
    print(f"Config ID: {selected_config.get('_id')}")
    print(f"Name: {selected_config.get('name')}")
    print(f"Model Type: {selected_config.get('model_type')}")
    print(f"Ensemble: {selected_config.get('ensemble', False)}")
    
    if selected_config.get('ensemble', False):
        print(f"Ensemble Models: {selected_config.get('ensemble_models', [])}")
        print(f"Ensemble Meta Features: {selected_config.get('ensemble_meta_features', [])}")
        print(f"Use Disagree: {selected_config.get('ensemble_use_disagree', False)}")
        print(f"Use Conf: {selected_config.get('ensemble_use_conf', False)}")
    
    print(f"\nFeatures Ranked: {selected_config.get('features_ranked', [])}")
    
    # Check master training data structure
    print("\n=== MASTER TRAINING DATA SAMPLE ===")
    # Try different possible collection names
    collections_to_check = ['master_training_nba', 'master_training', 'training_data']
    
    master_collection = None
    for coll_name in collections_to_check:
        if coll_name in db.list_collection_names():
            master_collection = db[coll_name]
            print(f"Found collection: {coll_name}")
            break
    
    if master_collection:
        sample_doc = master_collection.find_one({})
        
        if sample_doc:
            # Look for pred_margin field
            if 'pred_margin' in sample_doc:
                print(f"✅ pred_margin found in master training data")
                print(f"Sample pred_margin value: {sample_doc['pred_margin']}")
            else:
                print("❌ pred_margin NOT found in master training data")
                
            # Show some available fields that contain 'pred' or 'margin'
            print(f"\nFields containing 'pred' or 'margin':")
            pred_fields = [k for k in sample_doc.keys() if 'pred' in k.lower() or 'margin' in k.lower()]
            for field in pred_fields:
                print(f"  - {field}")
                
            # Show some available fields
            print(f"\nAvailable fields (first 20):")
            fields = [k for k in sample_doc.keys() if not k.startswith('_')][:20]
            for field in fields:
                print(f"  - {field}")
        else:
            print("❌ Master training collection exists but is empty")
    else:
        print("❌ No master training data collection found")
        print(f"Available collections: {db.list_collection_names()}")

if __name__ == "__main__":
    main()
