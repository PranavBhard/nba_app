"""
Data Schema Tool - Documents MongoDB collection schemas
"""

import sys
import os

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def get_data_schema() -> dict:
    """
    Get comprehensive schema documentation for all MongoDB collections.
    
    Returns:
        Dictionary with collection schemas, field definitions, time fields, and joins
    """
    schema = {
        'collections': {
            'stats_nba': {
                'description': 'Team-level game statistics and outcomes',
                'primary_key': '_id',
                'time_fields': ['date', 'year', 'month', 'day'],
                'fields': {
                    '_id': {'type': 'ObjectId', 'description': 'MongoDB document ID'},
                    'game_id': {'type': 'string', 'description': 'ESPN game ID', 'unique': True},
                    'date': {'type': 'string', 'format': 'YYYY-MM-DD', 'description': 'Game date'},
                    'year': {'type': 'int', 'description': 'Calendar year'},
                    'month': {'type': 'int', 'description': 'Month (1-12)'},
                    'day': {'type': 'int', 'description': 'Day of month'},
                    'season': {'type': 'string', 'format': 'YYYY-YYYY', 'description': 'NBA season (e.g., "2024-2025")'},
                    'game_type': {'type': 'string', 'values': ['regseason', 'preseason', 'playoff'], 'description': 'Game type'},
                    'homeWon': {'type': 'bool', 'description': 'Whether home team won'},
                    'OT': {'type': 'bool', 'description': 'Whether game went to overtime'},
                    'description': {'type': 'string', 'description': 'Game description'},
                    'espn_link': {'type': 'string', 'description': 'ESPN game link'},
                    'player_stats_migrated': {'type': 'bool', 'description': 'Whether player stats have been migrated'},
                    'homeTeam': {
                        'type': 'object',
                        'description': 'Home team statistics',
                        'fields': {
                            'name': {'type': 'string', 'description': 'Team abbreviation (e.g., "LAL", "NY")'},
                            'FG_made': {'type': 'float', 'description': 'Field goals made'},
                            'FG_att': {'type': 'float', 'description': 'Field goal attempts'},
                            'FGp': {'type': 'float', 'description': 'Field goal percentage'},
                            'three_made': {'type': 'float', 'description': 'Three-pointers made'},
                            'three_att': {'type': 'float', 'description': 'Three-point attempts'},
                            'three_percent': {'type': 'float', 'description': 'Three-point percentage'},
                            'FT_made': {'type': 'float', 'description': 'Free throws made'},
                            'FT_att': {'type': 'float', 'description': 'Free throw attempts'},
                            'FTp': {'type': 'float', 'description': 'Free throw percentage'},
                            'total_reb': {'type': 'float', 'description': 'Total rebounds'},
                            'off_reb': {'type': 'float', 'description': 'Offensive rebounds'},
                            'def_reb': {'type': 'float', 'description': 'Defensive rebounds'},
                            'assists': {'type': 'float', 'description': 'Assists'},
                            'steals': {'type': 'float', 'description': 'Steals'},
                            'blocks': {'type': 'float', 'description': 'Blocks'},
                            'TO': {'type': 'float', 'description': 'Turnovers'},
                            'pts_off_TO': {'type': 'float', 'description': 'Points off turnovers'},
                            'fast_break_pts': {'type': 'float', 'description': 'Fast break points'},
                            'pts_in_paint': {'type': 'float', 'description': 'Points in paint'},
                            'PF': {'type': 'float', 'description': 'Personal fouls'},
                            'points': {'type': 'float', 'description': 'Total points'},
                            'points1q': {'type': 'float', 'description': 'First quarter points'},
                            'points2q': {'type': 'float', 'description': 'Second quarter points'},
                            'points3q': {'type': 'float', 'description': 'Third quarter points'},
                            'points4q': {'type': 'float', 'description': 'Fourth quarter points'},
                            'pointsOT': {'type': 'float', 'description': 'Overtime points'},
                            'shooting_metric': {'type': 'float', 'description': 'Shooting efficiency metric'},
                            'TO_metric': {'type': 'float', 'description': 'Turnover metric'},
                            'off_reb_metric': {'type': 'float', 'description': 'Offensive rebound metric'}
                        }
                    },
                    'awayTeam': {
                        'type': 'object',
                        'description': 'Away team statistics',
                        'fields': 'Same structure as homeTeam'
                    }
                },
                'indexes': ['game_id', 'date', 'season', 'year'],
                'joins': {
                    'stats_nba_players': {'on': 'game_id', 'type': 'one-to-many'},
                    'players_nba': {'on': 'game_id (via stats_nba_players)', 'type': 'many-to-many'}
                }
            },
            'stats_nba_players': {
                'description': 'Player-level game statistics',
                'primary_key': '_id',
                'time_fields': ['date'],
                'fields': {
                    '_id': {'type': 'ObjectId', 'description': 'MongoDB document ID'},
                    'game_id': {'type': 'string', 'description': 'ESPN game ID', 'indexed': True},
                    'player_id': {'type': 'string', 'description': 'ESPN player ID', 'indexed': True},
                    'date': {'type': 'string', 'format': 'YYYY-MM-DD', 'description': 'Game date'},
                    'season': {'type': 'string', 'format': 'YYYY-YYYY', 'description': 'NBA season'},
                    'team': {'type': 'string', 'description': 'Team abbreviation'},
                    'home': {'type': 'bool', 'description': 'Whether player was on home team'},
                    'opponent': {'type': 'string', 'description': 'Opponent team abbreviation'},
                    'starter': {'type': 'bool', 'description': 'Whether player started'},
                    'pos_display_name': {'type': 'string', 'values': ['Guard', 'Forward', 'Center'], 'description': 'Position category'},
                    'pos_name': {'type': 'string', 'description': 'Specific position (e.g., "PG", "SG")'},
                    'player_name': {'type': 'string', 'description': 'Player full name'},
                    'stats': {
                        'type': 'object',
                        'description': 'Player game statistics',
                        'fields': {
                            'min': {'type': 'int', 'description': 'Minutes played'},
                            'pts': {'type': 'int', 'description': 'Points'},
                            'fg_made': {'type': 'int', 'description': 'Field goals made'},
                            'fg_att': {'type': 'int', 'description': 'Field goal attempts'},
                            'three_made': {'type': 'int', 'description': 'Three-pointers made'},
                            'three_att': {'type': 'int', 'description': 'Three-point attempts'},
                            'ft_made': {'type': 'int', 'description': 'Free throws made'},
                            'ft_att': {'type': 'int', 'description': 'Free throw attempts'},
                            'reb': {'type': 'int', 'description': 'Total rebounds'},
                            'ast': {'type': 'int', 'description': 'Assists'},
                            'stl': {'type': 'int', 'description': 'Steals'},
                            'blk': {'type': 'int', 'description': 'Blocks'},
                            'oreb': {'type': 'int', 'description': 'Offensive rebounds'},
                            'dreb': {'type': 'int', 'description': 'Defensive rebounds'},
                            'pf': {'type': 'int', 'description': 'Personal fouls'},
                            'to': {'type': 'int', 'description': 'Turnovers'},
                            'plus_minus': {'type': 'int', 'description': 'Plus/minus'}
                        }
                    }
                },
                'indexes': ['game_id', 'player_id', 'date', 'season', 'team'],
                'joins': {
                    'stats_nba': {'on': 'game_id', 'type': 'many-to-one'},
                    'players_nba': {'on': 'player_id', 'type': 'many-to-one'},
                    'nba_rosters': {'on': 'player_id + season + team', 'type': 'many-to-one'}
                }
            },
            'players_nba': {
                'description': 'Player metadata and injury information',
                'primary_key': '_id',
                'time_fields': [],
                'fields': {
                    '_id': {'type': 'ObjectId', 'description': 'MongoDB document ID'},
                    'player_id': {'type': 'string', 'description': 'ESPN player ID', 'unique': True, 'indexed': True},
                    'player_name': {'type': 'string', 'description': 'Player full name'},
                    'headshot': {'type': 'string', 'description': 'URL to player headshot'},
                    'pos_name': {'type': 'string', 'description': 'Position abbreviation (e.g., "PG")'},
                    'pos_display_name': {'type': 'string', 'values': ['Guard', 'Forward', 'Center'], 'description': 'Position category'},
                    'team': {'type': 'string', 'description': 'Current team abbreviation'},
                    'injury_status': {'type': 'string', 'values': ['Out', 'GTD', 'Day-To-Day', None], 'description': 'Injury status'},
                    'injury_details': {'type': 'string', 'description': 'Injury description'},
                    'updated_at': {'type': 'datetime', 'description': 'Last update timestamp'}
                },
                'indexes': ['player_id', 'team'],
                'joins': {
                    'stats_nba_players': {'on': 'player_id', 'type': 'one-to-many'},
                    'nba_rosters': {'on': 'player_id', 'type': 'one-to-many'}
                }
            },
            'nba_rosters': {
                'description': 'Team rosters per season with starter and injury status',
                'primary_key': '_id',
                'composite_key': ['season', 'team'],
                'time_fields': ['updated_at'],
                'fields': {
                    '_id': {'type': 'ObjectId', 'description': 'MongoDB document ID'},
                    'season': {'type': 'string', 'format': 'YYYY-YYYY', 'description': 'NBA season', 'indexed': True},
                    'team': {'type': 'string', 'description': 'Team abbreviation', 'indexed': True},
                    'roster': {
                        'type': 'array',
                        'description': 'List of players on roster',
                        'item_fields': {
                            'player_id': {'type': 'string', 'description': 'ESPN player ID'},
                            'starter': {'type': 'bool', 'description': 'Whether player is a starter'},
                            'injured': {'type': 'bool', 'description': 'Whether player is injured'}
                        }
                    },
                    'updated_at': {'type': 'datetime', 'description': 'Last update timestamp'}
                },
                'indexes': ['season', 'team', ['season', 'team']],
                'joins': {
                    'stats_nba_players': {'on': 'player_id + season + team', 'type': 'one-to-many'},
                    'players_nba': {'on': 'player_id', 'type': 'one-to-many'}
                }
            }
        },
        'relationships': {
            'game_to_players': {
                'from': 'stats_nba',
                'to': 'stats_nba_players',
                'on': 'game_id',
                'type': 'one-to-many',
                'description': 'Each game has many player stat records'
            },
            'player_to_games': {
                'from': 'stats_nba_players',
                'to': 'stats_nba',
                'on': 'game_id',
                'type': 'many-to-one',
                'description': 'Each player stat record belongs to one game'
            },
            'player_to_metadata': {
                'from': 'stats_nba_players',
                'to': 'players_nba',
                'on': 'player_id',
                'type': 'many-to-one',
                'description': 'Each player stat record links to player metadata'
            },
            'roster_to_players': {
                'from': 'nba_rosters',
                'to': 'stats_nba_players',
                'on': 'player_id + season + team',
                'type': 'one-to-many',
                'description': 'Roster entries link to player game stats'
            }
        },
        'notes': {
            'time_ordering': 'Games are ordered by date (YYYY-MM-DD). Seasons span from October to June (e.g., 2024-2025 season runs from Oct 2024 to Jun 2025).',
            'leakage_warning': 'NEVER use post-game statistics when calculating features for a game. Always use statistics from games BEFORE the target game date.',
            'feature_calculation': 'Features are calculated using StatHandlerV2 and PERCalculator classes, which aggregate statistics across time windows (season, months_N, games_N, days_N).',
            'data_quality': 'Some games may have player_stats_migrated=false. Always check this field before using player-level features.'
        }
    }
    
    return schema

