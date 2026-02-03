"""
Data Layer - Single point of access for all data operations.

This module provides repository classes for MongoDB collections and
API clients for external data sources.

Architecture:
    Consumer Layer (web/, agents/, cli/)
         │
         ▼
    Core/Services Layer (core/*.py)
         │
         ▼
    Data Layer (core/data/) ◄── YOU ARE HERE
         │
         ├── MongoDB Repositories
         │   ├── GamesRepository (stats_nba)
         │   ├── PlayerStatsRepository (stats_nba_players)
         │   ├── PlayersRepository (players_nba)
         │   ├── RostersRepository (nba_rosters)
         │   ├── TeamsRepository (teams_nba)
         │   ├── ClassifierConfigRepository (model_config_nba)
         │   ├── PointsConfigRepository (model_config_points_nba)
         │   ├── ExperimentRunsRepository (experiment_runs)
         │   ├── LeagueStatsCache (cached_league_stats)
         │   └── EloRatingsCache (nba_cached_elo_ratings)
         │
         └── External API Clients
             └── ESPNClient (ESPN NBA API)

Usage:
    from nba_app.core.data import GamesRepository, ESPNClient
    from nba_app.core.mongo import Mongo

    db = Mongo().db
    games_repo = GamesRepository(db)

    # Find games by date
    games = games_repo.find_by_date('2024-01-15')

    # Fetch from ESPN
    client = ESPNClient()
    live_games = client.get_games_for_date(date.today())
"""

# Base repository
from .base import BaseRepository

# MongoDB Repositories
from .games import GamesRepository
from .players import PlayerStatsRepository, PlayersRepository
from .rosters import RostersRepository, TeamsRepository
from .models import ClassifierConfigRepository, PointsConfigRepository, ExperimentRunsRepository
from .cache import LeagueStatsCache, EloRatingsCache

# External API Clients
from .espn_client import ESPNClient, GameInfo, MatchupInfo

__all__ = [
    # Base
    'BaseRepository',

    # Game data
    'GamesRepository',

    # Player data
    'PlayerStatsRepository',
    'PlayersRepository',

    # Team/roster data
    'RostersRepository',
    'TeamsRepository',

    # Model configs
    'ClassifierConfigRepository',
    'PointsConfigRepository',
    'ExperimentRunsRepository',

    # Cache
    'LeagueStatsCache',
    'EloRatingsCache',

    # ESPN API
    'ESPNClient',
    'GameInfo',
    'MatchupInfo',
]
