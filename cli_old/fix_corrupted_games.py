#!/usr/bin/env python
"""
Script to identify and re-scrape corrupted games in stats_nba.

Corrupted games are those that have quarter point fields (points1q, etc.)
but are missing base stats (FG_made, FG_att, assists, etc.) due to a bug
where $set with nested objects replaced entire homeTeam/awayTeam dicts.
"""
import argparse
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from nba_app.core.mongo import Mongo
from nba_app.cli_old.espn_api import process_game

# Expected base fields that should exist in a properly scraped game
EXPECTED_BASE_FIELDS = [
    "FG_made", "FG_att", "FGp", "three_made", "three_att", "FT_made", "FT_att",
    "total_reb", "off_reb", "def_reb", "assists", "steals", "blocks", "TO"
]

QUARTER_FIELDS = ["points1q", "points2q", "points3q", "points4q", "pointsOT"]


def find_corrupted_games(db):
    """Find games that have quarter fields but are missing base stats."""
    stats_nba = db.stats_nba

    # Find games with quarter fields
    games_with_quarters = list(stats_nba.find(
        {"homeTeam.points1q": {"$exists": True}},
        {"game_id": 1, "homeTeam": 1, "awayTeam": 1, "year": 1, "month": 1, "day": 1, "date": 1}
    ))

    corrupted = []

    for g in games_with_quarters:
        home_keys = set(g.get("homeTeam", {}).keys())
        away_keys = set(g.get("awayTeam", {}).keys())

        home_missing = [f for f in EXPECTED_BASE_FIELDS if f not in home_keys]
        away_missing = [f for f in EXPECTED_BASE_FIELDS if f not in away_keys]

        if home_missing or away_missing:
            corrupted.append({
                "game_id": g["game_id"],
                "year": g.get("year"),
                "month": g.get("month"),
                "day": g.get("day"),
                "date": g.get("date"),
                "home_missing": len(home_missing),
                "away_missing": len(away_missing)
            })

    return corrupted


def process_single_game(game_info, team_only, players_only, dry_run, progress_lock, progress):
    """Process a single corrupted game."""
    game_id = game_info["game_id"]

    # Build date from year/month/day or date string
    try:
        if game_info.get("year") and game_info.get("month") and game_info.get("day"):
            game_date = date(game_info["year"], game_info["month"], game_info["day"])
        elif game_info.get("date"):
            # Parse date string (e.g., "2023-01-15")
            parts = game_info["date"].split("-")
            game_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
        else:
            print(f"  WARNING: No date for game_id {game_id}, skipping")
            return False
    except Exception as e:
        print(f"  WARNING: Could not parse date for game_id {game_id}: {e}")
        return False

    try:
        success, player_count = process_game(
            game_id=game_id,
            game_date=game_date,
            team_only=team_only,
            players_only=players_only,
            dry_run=dry_run
        )

        with progress_lock:
            progress["processed"] += 1
            if progress["processed"] % 50 == 0:
                print(f"  Progress: {progress['processed']}/{progress['total']} games processed")

        return success
    except Exception as e:
        print(f"  ERROR processing game_id {game_id}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Fix corrupted games in stats_nba collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fix_corrupted_games.py                    # Re-scrape all corrupted games
  python fix_corrupted_games.py --dry-run          # Show what would be done
  python fix_corrupted_games.py --team-only        # Only fetch team stats
  python fix_corrupted_games.py --limit 100        # Process first 100 corrupted games
  python fix_corrupted_games.py --workers 4        # Use 4 parallel workers
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Don\'t update database, just print what would be updated'
    )

    parser.add_argument(
        '--team-only',
        action='store_true',
        help='Only fetch team stats (skip player stats)'
    )

    parser.add_argument(
        '--players-only',
        action='store_true',
        help='Only fetch player stats (skip team stats)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of games to process'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )

    parser.add_argument(
        '--list-only',
        action='store_true',
        help='Only list corrupted games without processing'
    )

    args = parser.parse_args()

    if args.team_only and args.players_only:
        print("Error: Cannot use --team-only and --players-only together")
        return

    db = Mongo().db

    print("Finding corrupted games...")
    corrupted = find_corrupted_games(db)

    print(f"\nFound {len(corrupted)} corrupted games")

    if not corrupted:
        print("No corrupted games found!")
        return

    # Show year breakdown
    years = {}
    for g in corrupted:
        y = g.get("year", "unknown")
        years[y] = years.get(y, 0) + 1

    print("\nCorrupted games by year:")
    for y in sorted(years.keys(), key=lambda x: str(x)):
        print(f"  {y}: {years[y]}")

    if args.list_only:
        print("\nSample corrupted game_ids:")
        for g in corrupted[:20]:
            print(f"  {g['game_id']} ({g.get('year')}-{g.get('month')}-{g.get('day')})")
        return

    # Apply limit if specified
    if args.limit:
        corrupted = corrupted[:args.limit]
        print(f"\nProcessing first {args.limit} corrupted games")

    if args.dry_run:
        print("\n[DRY RUN] Would re-scrape the following games:")
        for g in corrupted[:10]:
            print(f"  {g['game_id']}")
        if len(corrupted) > 10:
            print(f"  ... and {len(corrupted) - 10} more")
        return

    print(f"\nRe-scraping {len(corrupted)} corrupted games with {args.workers} workers...")

    progress_lock = Lock()
    progress = {"processed": 0, "total": len(corrupted)}

    success_count = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                process_single_game,
                game_info,
                args.team_only,
                args.players_only,
                False,
                progress_lock,
                progress
            ): game_info["game_id"]
            for game_info in corrupted
        }

        for future in as_completed(futures):
            game_id = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"  ERROR with game_id {game_id}: {e}")

    print(f"\nCompleted: {success_count}/{len(corrupted)} games re-scraped successfully")

    # Verify fix
    print("\nVerifying fix...")
    remaining = find_corrupted_games(db)
    print(f"Remaining corrupted games: {len(remaining)}")


if __name__ == '__main__':
    main()
