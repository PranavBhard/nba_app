"""
Game Tools - Get game information and rosters
"""

import sys
import os
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.core.mongo import Mongo
from nba_app.core.utils import get_season_from_date


def get_game(game_id: str, db=None, games_collection: str = 'stats_nba') -> Dict:
    """
    Get game information.

    Args:
        game_id: Game ID (ESPN game identifier)
        db: Optional MongoDB database instance
        games_collection: Name of the games collection (default: 'stats_nba')

    Returns:
        Dict with game information including:
        - game_id: Game ID
        - date: Game date
        - season: Season string
        - homeTeam: Home team information
        - awayTeam: Away team information
        - homeWon: Whether home team won (if game completed)
        - description: Game description
    """
    if db is None:
        db = Mongo().db

    game = db[games_collection].find_one({'game_id': game_id})

    if not game:
        return {'error': f'Game {game_id} not found'}
    
    # Convert to dict (handle MongoDB document)
    result = {
        'game_id': game.get('game_id', ''),
        'date': game.get('date', ''),
        'season': game.get('season', ''),
        'homeTeam': game.get('homeTeam', {}),
        'awayTeam': game.get('awayTeam', {}),
        'homeWon': game.get('homeWon'),
        'description': game.get('description', ''),
        'game_type': game.get('game_type', ''),
        'espn_link': game.get('espn_link', '')
    }
    
    return result


def get_team_games(team: str, season: str, before_date: str = None, home_only: bool = False, away_only: bool = False, limit: int = None, db=None, games_collection: str = 'stats_nba') -> List[Dict]:
    """
    Get games for a team in a season.

    Args:
        team: Team abbreviation (e.g., 'LAL', 'BOS')
        season: Season string (YYYY-YYYY format)
        before_date: Optional date string (YYYY-MM-DD format). Only return games before this date.
        home_only: If True, only return home games
        away_only: If True, only return away games
        limit: Optional limit on number of games to return
        db: Optional MongoDB database instance
        games_collection: Name of the games collection (default: 'stats_nba')

    Returns:
        List of Dict with game information, sorted by date descending (most recent first)
    """
    if db is None:
        db = Mongo().db

    query = {
        'season': season,
        '$or': [
            {'homeTeam.name': team},
            {'awayTeam.name': team}
        ]
    }
    
    # Add date filter if provided
    if before_date:
        query['date'] = {'$lt': before_date}
    
    # Add home/away filter
    if home_only:
        query['homeTeam.name'] = team
        query.pop('$or')
    elif away_only:
        query['awayTeam.name'] = team
        query.pop('$or')
    
    # Only include completed games (have scores)
    query['homeTeam.points'] = {'$gt': 0}
    query['awayTeam.points'] = {'$gt': 0}
    
    # Exclude preseason and all-star games
    query['game_type'] = {'$nin': ['preseason', 'allstar']}
    
    # Project only needed fields
    projection = {
        'game_id': 1,
        'date': 1,
        'season': 1,
        'homeTeam.name': 1,
        'awayTeam.name': 1,
        'homeTeam.points': 1,
        'awayTeam.points': 1,
        'homeWon': 1
    }
    
    # Sort by date descending (most recent first)
    games = list(db[games_collection].find(query, projection).sort('date', -1))
    
    if limit:
        games = games[:limit]
    
    # Format results
    results = []
    for game in games:
        is_home = game.get('homeTeam', {}).get('name') == team
        opponent = game.get('awayTeam', {}).get('name') if is_home else game.get('homeTeam', {}).get('name')
        won = (is_home and game.get('homeWon', False)) or (not is_home and not game.get('homeWon', False))
        team_points = game.get('homeTeam', {}).get('points') if is_home else game.get('awayTeam', {}).get('points')
        opponent_points = game.get('awayTeam', {}).get('points') if is_home else game.get('homeTeam', {}).get('points')
        
        results.append({
            'game_id': game.get('game_id', ''),
            'date': game.get('date', ''),
            'season': game.get('season', ''),
            'team': team,
            'opponent': opponent,
            'home': is_home,
            'won': won,
            'team_points': team_points,
            'opponent_points': opponent_points
        })
    
    return results


def get_team_last_games(N: int, team: str, season: str = None, before_date: str = None, db=None, games_collection: str = 'stats_nba') -> List[Dict]:
    """
    Get the last N games for a team.

    Args:
        N: Number of games to return
        team: Team abbreviation (e.g., 'LAL', 'BOS')
        season: Optional season string (YYYY-YYYY format). If not provided, uses current season.
        before_date: Optional date string (YYYY-MM-DD format). Only return games before this date.
        db: Optional MongoDB database instance
        games_collection: Name of the games collection (default: 'stats_nba')

    Returns:
        List of Dict with game information, sorted by date descending (most recent first)
    """
    if db is None:
        db = Mongo().db

    # If season not provided, try to infer from current date or before_date
    if not season:
        if before_date:
            try:
                date_obj = datetime.strptime(before_date, '%Y-%m-%d').date()
                season = get_season_from_date(date_obj)
            except:
                season = get_season_from_date(datetime.now())
        else:
            season = get_season_from_date(datetime.now())

    return get_team_games(team, season, before_date=before_date, limit=N, db=db, games_collection=games_collection)


def get_rosters(team: str, season: str = None, db=None, rosters_collection: str = 'nba_rosters', players_collection: str = 'players_nba') -> Dict:
    """
    Get team roster.

    Args:
        team: Team abbreviation (e.g., 'LAL', 'BOS')
        season: Optional season string (YYYY-YYYY format). If not provided, uses current season.
        db: Optional MongoDB database instance
        rosters_collection: Name of the rosters collection (default: 'nba_rosters')
        players_collection: Name of the players collection (default: 'players_nba')

    Returns:
        Dict with roster information including:
        - team: Team abbreviation
        - season: Season string
        - roster: List of players, each with:
          - player_id: Player ID
          - player_name: Player name (from players collection)
          - starter: Whether player is a starter
          - injured: Whether player is injured
    """
    if db is None:
        db = Mongo().db

    # If season not provided, try to infer from current date
    if not season:
        season = get_season_from_date(datetime.now())

    # Get roster from rosters collection
    roster_doc = db[rosters_collection].find_one({
        'season': season,
        'team': team
    })

    if not roster_doc:
        return {'error': f'No roster found for team {team} in season {season}'}

    roster_list = roster_doc.get('roster', [])

    # Get player names from players collection
    player_ids = [str(p.get('player_id', '')) for p in roster_list]
    players = list(db[players_collection].find(
        {'player_id': {'$in': player_ids}},
        {'player_id': 1, 'player_name': 1}
    ))
    
    # Create map of player_id -> player_name
    player_map = {str(p.get('player_id', '')): p.get('player_name', '') for p in players}
    
    # Build roster with names
    roster_with_names = []
    for roster_entry in roster_list:
        player_id = str(roster_entry.get('player_id', ''))
        roster_with_names.append({
            'player_id': player_id,
            'player_name': player_map.get(player_id, ''),
            'starter': roster_entry.get('starter', False),
            'injured': roster_entry.get('injured', False)
        })
    
    result = {
        'team': team,
        'season': season,
        'roster': roster_with_names
    }
    
    return result
