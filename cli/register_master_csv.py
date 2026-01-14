"""
Script to register an existing master training CSV in MongoDB.

Usage:
    python cli/register_master_csv.py
    OR
    python -m nba_app.cli.register_master_csv (from project root)
"""

import os
import sys

# Add project root to Python path
# Script is in nba_app/cli/, so we need to go up to the parent of nba_app/
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)  # nba_app/
project_root = os.path.dirname(nba_app_dir)  # Parent of nba_app/
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.cli.Mongo import Mongo
from nba_app.cli.master_training_data import register_existing_master_csv, MASTER_TRAINING_PATH


def main():
    """Register existing master CSV in MongoDB."""
    print("=" * 60)
    print("Registering Existing Master Training CSV")
    print("=" * 60)
    
    # Get master path (can be overridden with command line arg)
    master_path = MASTER_TRAINING_PATH
    if len(sys.argv) > 1:
        master_path = sys.argv[1]
        if not os.path.isabs(master_path):
            # Make relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            master_path = os.path.join(project_root, master_path)
    
    print(f"\nMaster CSV path: {master_path}")
    
    if not os.path.exists(master_path):
        print(f"\nERROR: Master CSV not found at: {master_path}")
        print("Please provide the correct path or ensure the file exists.")
        sys.exit(1)
    
    # Connect to MongoDB
    print("\nConnecting to MongoDB...")
    mongo = Mongo()
    db = mongo.db
    print("Connected.")
    
    # Register the master CSV
    try:
        metadata = register_existing_master_csv(db, master_path)
        
        print("\n" + "=" * 60)
        print("SUCCESS: Master training CSV registered!")
        print("=" * 60)
        print(f"\nYou can now use the 'Use Cached Master Training Data' checkbox")
        print(f"in the web app to extract features from this master CSV.")
        print(f"\nMetadata:")
        print(f"  File: {metadata['file_path']}")
        print(f"  Features: {metadata['feature_count']}")
        print(f"  Games: {metadata['game_count']}")
        print(f"  Last Updated: {metadata['last_date_updated']}")
        
    except Exception as e:
        print(f"\nERROR: Failed to register master CSV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

