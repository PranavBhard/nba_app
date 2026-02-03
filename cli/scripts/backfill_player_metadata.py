#!/usr/bin/env python3
"""
Backfill player metadata (headshot, position) from ESPN API to players collection.

This script:
1. Gets all unique player_ids from player_stats collection
2. Checks which players are missing headshot/position in players collection
3. Fetches metadata from ESPN API for those players
4. Updates the players collection

Usage:
    python -m nba_app.cli.scripts.backfill_player_metadata <league>
    python -m nba_app.cli.scripts.backfill_player_metadata nba
    python -m nba_app.cli.scripts.backfill_player_metadata cbb
    python -m nba_app.cli.scripts.backfill_player_metadata cbb --dry-run
    python -m nba_app.cli.scripts.backfill_player_metadata cbb --limit 100
"""

import argparse
import sys
import os
import requests
import time

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(os.path.dirname(script_dir))
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.core.mongo import Mongo
from nba_app.core.league_config import load_league_config


def fetch_player_from_espn(player_id: str, league_slug: str) -> dict:
    """
    Fetch player metadata from ESPN API.

    Args:
        player_id: ESPN player ID
        league_slug: ESPN league slug (e.g., 'nba', 'mens-college-basketball')

    Returns:
        Dict with headshot, pos_name, pos_display_name (or empty dict on failure)
    """
    # Map league to ESPN sport path
    if league_slug == 'nba':
        sport_path = 'basketball/nba'
    elif league_slug == 'mens-college-basketball':
        sport_path = 'basketball/mens-college-basketball'
    else:
        sport_path = f'basketball/{league_slug}'

    url = f"https://site.api.espn.com/apis/common/v3/sports/{sport_path}/athletes/{player_id}"

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {}

        data = resp.json()
        athlete = data.get('athlete', data)  # Handle both response formats

        result = {}

        # Extract headshot
        headshot = athlete.get('headshot', {})
        if headshot and headshot.get('href'):
            result['headshot'] = headshot['href']

        # Extract position
        position = athlete.get('position', {})
        if position:
            if position.get('name'):
                result['pos_name'] = position['name']
            if position.get('displayName'):
                result['pos_display_name'] = position['displayName']

        # Also get player name if available
        if athlete.get('displayName'):
            result['player_name'] = athlete['displayName']

        return result

    except Exception as e:
        print(f"    Error fetching player {player_id}: {e}")
        return {}


def backfill_player_metadata(league_id: str, dry_run: bool = False, limit: int = None):
    """
    Backfill player metadata from ESPN API.

    Args:
        league_id: League identifier (nba, cbb, etc.)
        dry_run: If True, only show what would be done
        limit: Max players to process (for testing)
    """
    print(f"Backfilling player metadata for league: {league_id}")
    print(f"Dry run: {dry_run}")
    if limit:
        print(f"Limit: {limit} players")
    print()

    # Load league config
    league = load_league_config(league_id)
    db = Mongo().db

    # Get collection names from league config
    player_stats_collection = league.collections.get('player_stats', 'stats_nba_players')
    players_collection = league.collections.get('players', 'players_nba')
    league_slug = league.espn.get('league_slug', 'nba')

    print(f"Player stats collection: {player_stats_collection}")
    print(f"Players collection: {players_collection}")
    print(f"ESPN league slug: {league_slug}")
    print()

    # Step 1: Get all unique player_ids from player_stats
    print("Step 1: Finding unique players in player_stats collection...")

    pipeline = [
        {'$group': {
            '_id': '$player_id',
            'player_name': {'$first': '$player_name'}
        }}
    ]

    all_players = list(db[player_stats_collection].aggregate(pipeline))
    print(f"  Found {len(all_players)} unique players in {player_stats_collection}")

    # Step 2: Find players missing headshot or position in players collection
    print("\nStep 2: Checking which players need metadata...")

    players_to_update = []
    for player in all_players:
        player_id = player['_id']

        # Check if player exists and has metadata
        existing = db[players_collection].find_one(
            {'player_id': player_id},
            {'headshot': 1, 'pos_name': 1, 'pos_display_name': 1}
        )

        needs_update = False
        if not existing:
            needs_update = True
        elif not existing.get('headshot') or not existing.get('pos_name'):
            needs_update = True

        if needs_update:
            players_to_update.append({
                'player_id': player_id,
                'player_name': player.get('player_name', 'Unknown')
            })

    print(f"  Found {len(players_to_update)} players needing metadata update")

    if limit:
        players_to_update = players_to_update[:limit]
        print(f"  Limited to {len(players_to_update)} players")

    if not players_to_update:
        print("\nNo players need updating.")
        return

    # Step 3: Fetch from ESPN API and update
    print(f"\nStep 3: Fetching metadata from ESPN API...")

    updated_count = 0
    failed_count = 0
    skipped_count = 0

    for i, player in enumerate(players_to_update):
        player_id = player['player_id']
        player_name = player['player_name']

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{len(players_to_update)} ({updated_count} updated, {failed_count} failed)")

        if dry_run:
            print(f"  [DRY RUN] Would fetch metadata for {player_name} ({player_id})")
            continue

        # Fetch from ESPN
        metadata = fetch_player_from_espn(str(player_id), league_slug)

        if not metadata:
            failed_count += 1
            continue

        # Only update if we got useful data
        if not metadata.get('headshot') and not metadata.get('pos_name'):
            skipped_count += 1
            continue

        # Update players collection
        update_data = {'player_id': player_id}
        if metadata.get('player_name'):
            update_data['player_name'] = metadata['player_name']
        if metadata.get('headshot'):
            update_data['headshot'] = metadata['headshot']
        if metadata.get('pos_name'):
            update_data['pos_name'] = metadata['pos_name']
        if metadata.get('pos_display_name'):
            update_data['pos_display_name'] = metadata['pos_display_name']

        db[players_collection].update_one(
            {'player_id': player_id},
            {'$set': update_data},
            upsert=True
        )
        updated_count += 1

        # Rate limit to avoid hitting ESPN too hard
        time.sleep(0.1)

    print(f"\nDone!")
    print(f"  Updated: {updated_count}")
    print(f"  Failed (API error): {failed_count}")
    print(f"  Skipped (no data): {skipped_count}")


def main():
    parser = argparse.ArgumentParser(
        description='Backfill player metadata (headshot, position) from ESPN API'
    )
    parser.add_argument('league', help='League identifier (nba, cbb, etc.)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--limit', type=int, default=None,
                       help='Maximum number of players to process')

    args = parser.parse_args()

    backfill_player_metadata(args.league, args.dry_run, args.limit)


if __name__ == '__main__':
    main()
