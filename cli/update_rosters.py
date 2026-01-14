#!/usr/bin/env python3
"""
Update NBA Rosters Collection

Builds rosters for each team from stats_nba_players collection.
Determines starters based on games started by position:
- Top 2 guards (by games started)
- Top 2 forwards (by games started)
- Top 1 center (by games started)

Players with 0 minutes in the season are excluded.
Last team a player played for determines their current team.
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict, Counter

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.cli.Mongo import Mongo
import argparse


def get_position_category(pos_display_name: str) -> Optional[str]:
    """
    Get position category from pos_display_name.
    pos_display_name values in stats_nba_players are: "Guard", "Forward", "Center"
    Returns: 'guard', 'forward', 'center', or None
    """
    if not pos_display_name:
        return None
    
    pos_lower = pos_display_name.lower()
    if pos_lower == 'guard':
        return 'guard'
    elif pos_lower == 'forward':
        return 'forward'
    elif pos_lower == 'center':
        return 'center'
    
    return None


def update_rosters(season: str, db=None, dry_run=False):
    """
    Update nba_rosters collection for a given season.
    
    Each document in nba_rosters represents a unique team + season combination.
    Document structure:
    {
        'season': str,  # e.g., "2024-2025"
        'team': str,    # Team name (e.g., "NY", "LAL")
        'roster': [     # List of players on the roster
            {
                'player_id': str,
                'starter': bool
            },
            ...
        ],
        'updated_at': datetime
    }
    
    Args:
        season: Season string (e.g., "2024-2025")
        db: MongoDB database instance (optional, will create if not provided)
        dry_run: If True, don't actually update the database, just print what would be updated
    """
    if db is None:
        mongo = Mongo()
        db = mongo.db
    
    if dry_run:
        print(f"[DRY RUN] Would update rosters for season: {season}")
    else:
        print(f"Updating rosters for season: {season}")
    
    # Get all players who played in this season (with minutes > 0)
    # Aggregate by player_id to get:
    # - Last team they played for (most recent game)
    # - Total minutes
    # - Games started count
    # - Position (most common position)
    
    # First, get all player-game records for this season with minutes > 0
    player_games = list(db.stats_nba_players.find(
        {
            'season': season,
            'stats.min': {'$gt': 0}
        },
        {
            'player_id': 1,
            'team': 1,
            'date': 1,
            'game_id': 1,  # Need game_id to count unique games
            'stats.min': 1,
            'starter': 1,
            'pos_display_name': 1,
            'player_name': 1
        }
    ).sort('date', 1))  # Sort by date ascending to get last team
    
    # Group by player_id
    # Use dictionaries to track unique game_ids to avoid counting duplicates
    # Store game data: {game_id: {'min': minutes, 'starter': bool}}
    player_data = defaultdict(lambda: {
        'player_id': None,
        'player_name': None,
        'last_team': None,
        'last_date': None,
        'game_data': {},  # Track unique game_ids: {game_id: {'min': minutes, 'starter': bool}}
        'positions': []
    })
    
    for pg in player_games:
        player_id = str(pg.get('player_id', ''))
        if not player_id:
            continue
        
        game_id = pg.get('game_id')
        if not game_id:
            continue  # Skip records without game_id
        
        if player_data[player_id]['player_id'] is None:
            player_data[player_id]['player_id'] = player_id
            player_data[player_id]['player_name'] = pg.get('player_name', '')
        
        # Update last team and date (since sorted by date ascending, last one wins)
        player_data[player_id]['last_team'] = pg.get('team')
        player_data[player_id]['last_date'] = pg.get('date')
        
        # Track unique game_ids - use latest record for each game_id (since sorted by date)
        # This handles duplicate game records by overwriting with the most recent data
        player_data[player_id]['game_data'][game_id] = {
            'min': pg.get('stats', {}).get('min', 0),
            'starter': pg.get('starter', False)
        }
        
        # Collect positions (using pos_display_name which has values: "Guard", "Forward", "Center")
        pos_display_name = pg.get('pos_display_name')
        if pos_display_name:
            player_data[player_id]['positions'].append(pos_display_name)
    
    # After processing all games, calculate totals from unique game_ids
    for player_id, data in player_data.items():
        data['total_games'] = len(data['game_data'])
        data['games_started'] = sum(1 for g in data['game_data'].values() if g.get('starter', False))
        data['total_minutes'] = sum(g.get('min', 0) for g in data['game_data'].values())
        
        # Calculate MPG
        if data['total_games'] > 0:
            data['mpg'] = data['total_minutes'] / data['total_games']
        else:
            data['mpg'] = 0.0
    
    # Convert to list and determine most common position
    # Filter out players with less than 5 MPG or 0 minutes
    player_list = []
    for player_id, data in player_data.items():
        # Skip players with < 5 MPG or 0 minutes
        if data['mpg'] < 5.0 or data['total_minutes'] == 0:
            continue
        # Get most common position
        if data['positions']:
            pos_counter = Counter(data['positions'])
            most_common_pos = pos_counter.most_common(1)[0][0]
        else:
            most_common_pos = None
        
        player_list.append({
            'player_id': data['player_id'],
            'player_name': data['player_name'],
            'last_team': data['last_team'],
            'total_minutes': data['total_minutes'],
            'games_started': data['games_started'],
            'total_games': data['total_games'],
            'most_common_pos': most_common_pos
        })
    
    print(f"Found {len(player_list)} players with minutes > 0 in season {season}")
    
    # Group players by team (using last_team)
    players_by_team = defaultdict(list)
    for player in player_list:
        team = player.get('last_team')
        if not team:
            continue
        
        # Get position category from pos_display_name
        pos_display_name = player.get('most_common_pos')  # This is actually pos_display_name
        pos_category = get_position_category(pos_display_name)
        
        players_by_team[team].append({
            'player_id': str(player['player_id']),
            'player_name': player.get('player_name', ''),
            'position': pos_display_name,  # Store the actual pos_display_name value
            'position_category': pos_category,
            'games_started': player.get('games_started', 0),
            'total_minutes': player.get('total_minutes', 0),
            'total_games': player.get('total_games', 0)
        })
    
    print(f"Found players on {len(players_by_team)} teams")
    
    # For each team, determine starters
    rosters_updated = 0
    for team, players in players_by_team.items():
        # Separate by position category
        guards = [p for p in players if p['position_category'] == 'guard']
        forwards = [p for p in players if p['position_category'] == 'forward']
        centers = [p for p in players if p['position_category'] == 'center']
        other = [p for p in players if p['position_category'] is None]
        
        # Sort by games_started (descending)
        guards.sort(key=lambda x: x['games_started'], reverse=True)
        forwards.sort(key=lambda x: x['games_started'], reverse=True)
        centers.sort(key=lambda x: x['games_started'], reverse=True)
        
        # Debug: Print all guards with their stats (if dry_run or verbose)
        if dry_run and guards:
            print(f"    All {team} guards (sorted by games_started):")
            for i, guard in enumerate(guards, 1):
                print(f"      {i}. {guard['player_name']}: {guard['games_started']} starts / {guard['total_games']} games")
        
        # Determine starters: top 2 guards, top 2 forwards, top 1 center
        starter_ids = set()
        
        # Top 2 guards
        for guard in guards[:2]:
            starter_ids.add(guard['player_id'])
        
        # Top 2 forwards
        for forward in forwards[:2]:
            starter_ids.add(forward['player_id'])
        
        # Top 1 center
        if centers:
            starter_ids.add(centers[0]['player_id'])
        
        # Build roster list
        roster = []
        for player in players:
            roster.append({
                'player_id': player['player_id'],
                'starter': player['player_id'] in starter_ids
            })
        
        starters_count = len([p for p in roster if p['starter']])
        
        if dry_run:
            # Print what would be updated without actually updating
            print(f"  [DRY RUN] {team}: {len(roster)} players, {starters_count} starters")
            starter_names = [p['player_name'] for p in players if p['player_id'] in starter_ids]
            print(f"    Starters: {', '.join(starter_names[:5])}")
        else:
            # Update nba_rosters collection
            # Each document is uniquely identified by season + team combination
            db.nba_rosters.update_one(
                {'season': season, 'team': team},  # Unique key: season + team
                {
                    '$set': {
                        'season': season,
                        'team': team,
                        'roster': roster,
                        'updated_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            print(f"  {team}: {len(roster)} players, {starters_count} starters")
        
        rosters_updated += 1
    
    if dry_run:
        print(f"\n[DRY RUN] Would update {rosters_updated} team rosters for season {season}")
    else:
        print(f"\nUpdated {rosters_updated} team rosters for season {season}")
    return rosters_updated


def main():
    parser = argparse.ArgumentParser(description='Update NBA rosters collection')
    parser.add_argument('--season', type=str, required=True,
                       help='Season string (e.g., "2024-2025")')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without actually updating the database')
    
    args = parser.parse_args()
    
    print("Connecting to MongoDB...")
    mongo = Mongo()
    db = mongo.db
    print("Connected!")
    
    update_rosters(args.season, db, dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n[DRY RUN] No changes were made to the database.")
    else:
        print("\nDone!")


if __name__ == '__main__':
    main()

