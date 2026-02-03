#!/usr/bin/env python3
"""
Script to compute and cache Elo ratings to MongoDB.

Usage:
    # Cache all seasons
    python cli/cache_elo_ratings.py

    # Cache specific seasons
    python cli/cache_elo_ratings.py --seasons 2023-2024 2024-2025

    # View cache stats
    python cli/cache_elo_ratings.py --stats

    # View current team ratings
    python cli/cache_elo_ratings.py --current

    # Clear cache
    python cli/cache_elo_ratings.py --clear

    # Clear specific seasons
    python cli/cache_elo_ratings.py --clear --seasons 2023-2024
"""

import sys
import os
import argparse
from datetime import datetime

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.core.mongo import Mongo
from nba_app.core.stats.elo_cache import EloCache


def print_header(title: str):
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_stats(stats: dict):
    """Print cache statistics."""
    print(f"\n  Total Ratings: {stats['total_ratings']:,}")
    print(f"  Teams: {stats['teams']}")
    print(f"  Seasons: {', '.join(stats['seasons']) if stats['seasons'] else 'None'}")

    if stats['date_range'] and stats['date_range']['min']:
        print(f"  Date Range: {stats['date_range']['min']} to {stats['date_range']['max']}")

    if stats['last_updated']:
        print(f"  Last Updated: {stats['last_updated']}")


def print_current_ratings(ratings: dict, top_n: int = 30):
    """Print current team ratings."""
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    print(f"\n  {'Rank':<6} {'Team':<30} {'Elo':>8}")
    print(f"  {'-'*6} {'-'*30} {'-'*8}")

    for idx, (team, elo) in enumerate(sorted_ratings[:top_n], 1):
        print(f"  {idx:<6} {team:<30} {elo:>8.1f}")

    if len(sorted_ratings) > top_n:
        print(f"\n  ... and {len(sorted_ratings) - top_n} more teams")


def run_cache(elo_cache: EloCache, seasons: list = None):
    """Run the elo caching process."""
    start_time = datetime.now()

    def progress_callback(stage, current, total, message):
        if stage == 'fetch':
            print(f"\r  {message}", end='', flush=True)
            if current == total:
                print()
        elif stage == 'compute':
            pct = (current / total * 100) if total > 0 else 0
            print(f"\r  Computing Elo: {current:,}/{total:,} games ({pct:.1f}%)", end='', flush=True)
            if current == total:
                print()
        elif stage == 'cache':
            pct = (current / total * 100) if total > 0 else 0
            print(f"\r  Caching to MongoDB: {current:,}/{total:,} ratings ({pct:.1f}%)", end='', flush=True)
            if current == total:
                print()

    print("\n  Starting Elo cache computation...")
    if seasons:
        print(f"  Seasons: {', '.join(seasons)}")
    else:
        print("  Seasons: All")

    result = elo_cache.compute_and_cache_all(seasons=seasons, progress_callback=progress_callback)

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n  ✅ Caching complete!")
    print(f"\n  Results:")
    print(f"    Games Processed: {result['games_processed']:,}")
    print(f"    Ratings Cached: {result['ratings_cached']:,}")
    print(f"    Teams: {result['teams']}")
    print(f"    Seasons: {', '.join(result['seasons']) if result['seasons'] else 'None'}")

    if result['date_range'] and result['date_range']['min']:
        print(f"    Date Range: {result['date_range']['min']} to {result['date_range']['max']}")

    print(f"    Time Elapsed: {elapsed:.1f} seconds")

    # Show top teams
    if result.get('current_ratings'):
        print("\n  Top 10 Teams by Current Elo:")
        sorted_ratings = sorted(result['current_ratings'].items(), key=lambda x: x[1], reverse=True)
        for idx, (team, elo) in enumerate(sorted_ratings[:10], 1):
            print(f"    {idx}. {team}: {elo:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description='Compute and cache Elo ratings to MongoDB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python cli/cache_elo_ratings.py                    # Cache all seasons
    python cli/cache_elo_ratings.py --seasons 2024-2025  # Cache specific season
    python cli/cache_elo_ratings.py --stats            # View cache stats
    python cli/cache_elo_ratings.py --current          # View current ratings
    python cli/cache_elo_ratings.py --clear            # Clear all cache
        """
    )

    parser.add_argument(
        '--seasons', '-s',
        nargs='+',
        help='Specific seasons to process (e.g., 2023-2024 2024-2025)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show cache statistics'
    )
    parser.add_argument(
        '--current',
        action='store_true',
        help='Show current team Elo ratings'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear the cache (use with --seasons to clear specific seasons)'
    )
    parser.add_argument(
        '--top', '-n',
        type=int,
        default=30,
        help='Number of teams to show for --current (default: 30)'
    )

    args = parser.parse_args()

    # Connect to MongoDB
    print_header("NBA Elo Cache Manager")
    print("\nConnecting to MongoDB...")

    try:
        mongo = Mongo()
        elo_cache = EloCache(mongo.db)
        print("Connected.")
    except Exception as e:
        print(f"\n❌ Failed to connect to MongoDB: {e}")
        sys.exit(1)

    # Handle different commands
    if args.stats:
        print("\nCache Statistics:")
        stats = elo_cache.get_cache_stats()
        print_stats(stats)

    elif args.current:
        print("\nCurrent Team Elo Ratings:")
        ratings = elo_cache.get_all_current_elos()
        if ratings:
            print_current_ratings(ratings, args.top)
        else:
            print("\n  No ratings cached. Run without flags to populate cache.")

    elif args.clear:
        if args.seasons:
            print(f"\nClearing cache for seasons: {', '.join(args.seasons)}")
        else:
            print("\nClearing entire cache...")

        deleted = elo_cache.clear_cache(seasons=args.seasons)
        print(f"\n  ✅ Deleted {deleted:,} documents")

    else:
        # Default: run caching
        print("\nRunning Elo Cache Population...")
        run_cache(elo_cache, seasons=args.seasons)

    print()


if __name__ == '__main__':
    main()
