#!/usr/bin/env python3
"""
Background job script for full regeneration of master training data.

Usage:
    python regenerate_full_job.py --job-id <job_id> --league nba
"""

import sys
import os
import argparse
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bson import ObjectId
from nba_app.core.mongo import Mongo
from nba_app.core.services.training_data import TrainingDataService


def main():
    parser = argparse.ArgumentParser(description='Full regeneration of master training data')
    parser.add_argument('--job-id', type=str, required=True,
                        help='Job ID for progress tracking')
    parser.add_argument('--league', type=str, default='nba',
                        help='League ID (default: nba)')
    parser.add_argument('--no-player', action='store_true',
                        help='Skip player-level features')

    args = parser.parse_args()

    job_id = args.job_id
    league = args.league
    no_player = args.no_player

    # Connect to MongoDB
    mongo = Mongo()
    db = mongo.db

    try:
        print(f"Starting full master training regeneration")
        print(f"Job ID: {job_id}")
        print(f"League: {league}")
        print(f"No player features: {no_player}")

        # Use the core service
        service = TrainingDataService(db=db, league=league, job_id=job_id)
        game_count, csv_path, feature_list = service.regenerate_full(
            no_player=no_player
        )

        # Mark job as completed
        db.jobs_nba.update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {
                'status': 'completed',
                'progress': 100,
                'message': f'Completed! Generated {game_count} games with {len(feature_list)} features',
                'result': {
                    'game_count': game_count,
                    'feature_count': len(feature_list),
                    'csv_path': csv_path
                },
                'updated_at': datetime.utcnow()
            }}
        )

        print(f"Completed! Generated {game_count} games with {len(feature_list)} features")
        print(f"Master training saved to: {csv_path}")

    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"Error: {error_msg}")
        traceback.print_exc()

        # Mark job as failed
        db.jobs_nba.update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {
                'status': 'failed',
                'error': error_msg,
                'message': f'Failed: {error_msg}',
                'updated_at': datetime.utcnow()
            }}
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
