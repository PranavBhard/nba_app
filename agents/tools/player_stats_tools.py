"""
Player Stats Tools - Get player statistics from database
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

from nba_app.cli.Mongo import Mongo


def get_player_stat(game_id: str, player_id: str, db=None) -> Dict:
    """
    Get player statistics for a specific game.
    
    Args:
        game_id: Game ID (ESPN game identifier)
        player_id: Player ID (ESPN player identifier)
        db: Optional MongoDB database instance
        
    Returns:
        Dict with player game statistics including:
        - player_id: Player ID
        - player_name: Player name
        - game_id: Game ID
        - date: Game date
        - team: Team abbreviation
        - opponent: Opponent team abbreviation
        - home: Whether player was on home team
        - starter: Whether player started
        - stats: Dict with game statistics (pts, reb, ast, etc.)
    """
    if db is None:
        db = Mongo().db
    
    player_game = db.stats_nba_players.find_one({
        'game_id': game_id,
        'player_id': player_id
    })
    
    if not player_game:
        return {'error': f'No stats found for player {player_id} in game {game_id}'}
    
    # Convert to dict and format
    result = {
        'player_id': str(player_game.get('player_id', '')),
        'player_name': player_game.get('player_name', ''),
        'game_id': player_game.get('game_id', ''),
        'date': player_game.get('date', ''),
        'season': player_game.get('season', ''),
        'team': player_game.get('team', ''),
        'opponent': player_game.get('opponent', ''),
        'home': player_game.get('home', False),
        'starter': player_game.get('starter', False),
        'stats': player_game.get('stats', {})
    }
    
    return result


def get_player_season_stats(season: str, player_id: str, db=None) -> Dict:
    """
    Get season averages for a player.
    
    Args:
        season: Season string (YYYY-YYYY format, e.g., '2024-2025')
        player_id: Player ID (ESPN player identifier)
        db: Optional MongoDB database instance
        
    Returns:
        Dict with season statistics including:
        - player_id: Player ID
        - player_name: Player name
        - season: Season string
        - games: Number of games played
        - stats: Dict with season averages (pts, reb, ast, etc.)
    """
    if db is None:
        db = Mongo().db
    
    # Get all games for this player in this season
    games = list(db.stats_nba_players.find({
        'season': season,
        'player_id': player_id,
        'stats.min': {'$gt': 0}  # Only games where player played
    }))
    
    if not games:
        return {'error': f'No games found for player {player_id} in season {season}'}
    
    # Get player name from first game
    player_name = games[0].get('player_name', '')
    
    # Aggregate stats
    total_stats = {}
    game_count = len(games)
    
    stat_keys = ['min', 'pts', 'fg_made', 'fg_att', 'three_made', 'three_att', 
                 'ft_made', 'ft_att', 'reb', 'ast', 'stl', 'blk', 'to', 'pf', 
                 'oreb', 'dreb', 'plus_minus']
    
    for stat_key in stat_keys:
        total = sum(game.get('stats', {}).get(stat_key, 0) or 0 for game in games)
        total_stats[stat_key] = total
    
    # Calculate averages
    avg_stats = {}
    for stat_key in stat_keys:
        if stat_key == 'min':
            avg_stats[stat_key] = total_stats[stat_key] / game_count if game_count > 0 else 0
        else:
            avg_stats[stat_key] = total_stats[stat_key] / game_count if game_count > 0 else 0
    
    # Calculate percentages
    if avg_stats.get('fg_att', 0) > 0:
        avg_stats['fg_percent'] = avg_stats['fg_made'] / avg_stats['fg_att']
    else:
        avg_stats['fg_percent'] = 0.0
    
    if avg_stats.get('three_att', 0) > 0:
        avg_stats['three_percent'] = avg_stats['three_made'] / avg_stats['three_att']
    else:
        avg_stats['three_percent'] = 0.0
    
    if avg_stats.get('ft_att', 0) > 0:
        avg_stats['ft_percent'] = avg_stats['ft_made'] / avg_stats['ft_att']
    else:
        avg_stats['ft_percent'] = 0.0
    
    result = {
        'player_id': str(player_id),
        'player_name': player_name,
        'season': season,
        'games': game_count,
        'stats': avg_stats,
        'total_stats': total_stats
    }
    
    return result


def get_player_last_stats(N: int, player_id: str, db=None) -> List[Dict]:
    """
    Get the last N games for a player.
    
    Args:
        N: Number of previous games to retrieve
        player_id: Player ID (ESPN player identifier)
        db: Optional MongoDB database instance
        
    Returns:
        List of dicts, each containing game statistics for one game.
        Games are sorted by date descending (most recent first).
        Each dict contains:
        - player_id: Player ID
        - player_name: Player name
        - game_id: Game ID
        - date: Game date
        - team: Team abbreviation
        - opponent: Opponent team abbreviation
        - home: Whether player was on home team
        - starter: Whether player started
        - stats: Dict with game statistics
    """
    if db is None:
        db = Mongo().db
    
    # Get last N games for this player (sorted by date descending)
    games = list(db.stats_nba_players.find({
        'player_id': player_id,
        'stats.min': {'$gt': 0}  # Only games where player played
    }).sort('date', -1).limit(N))
    
    if not games:
        return []
    
    # Format results
    results = []
    for game in games:
        result = {
            'player_id': str(game.get('player_id', '')),
            'player_name': game.get('player_name', ''),
            'game_id': game.get('game_id', ''),
            'date': game.get('date', ''),
            'season': game.get('season', ''),
            'team': game.get('team', ''),
            'opponent': game.get('opponent', ''),
            'home': game.get('home', False),
            'starter': game.get('starter', False),
            'stats': game.get('stats', {})
        }
        results.append(result)
    
    return results


def get_player_games_in_season(season: str, player_id: str, team: str = None, db=None) -> List[str]:
    """
    Get list of game IDs where a player played (stats.min > 0) in a season.
    
    Args:
        season: Season string (YYYY-YYYY format, e.g., '2024-2025')
        player_id: Player ID (ESPN player identifier)
        team: Optional team abbreviation (e.g., 'LAL', 'BOS'). If provided, filters to games for that team.
        db: Optional MongoDB database instance
        
    Returns:
        List of game IDs (strings) where the player played, sorted by date ascending (oldest first)
    """
    if db is None:
        db = Mongo().db
    
    query = {
        'season': season,
        'player_id': player_id,
        'stats.min': {'$gt': 0}  # Only games where player played
    }
    
    if team:
        query['team'] = team
    
    # Get games and sort by date ascending
    games = list(db.stats_nba_players.find(
        query,
        {'game_id': 1, 'date': 1}
    ).sort('date', 1))
    
    # Extract game IDs
    game_ids = [str(game.get('game_id', '')) for game in games if game.get('game_id')]
    
    return game_ids
