"""
Statistics Calculation Module.

This module contains all statistics calculation functionality:
- StatHandlerV2: Main statistics handler for feature calculation
- PERCalculator: Player Efficiency Rating calculations
- EloCache: Elo rating cache and calculations
- League stats caching
"""

# Main statistics handler
from bball.stats.handler import StatHandlerV2

# PER Calculator
from bball.stats.per_calculator import PERCalculator

# Elo cache
from bball.stats.elo_cache import EloCache

# League stats caching
from bball.stats.league_cache import (
    cache_season,
    get_all_seasons,
    get_season_stats_with_fallback,
    get_league_constants,
    get_team_pace,
    ensure_season_cached,
)

__all__ = [
    # Handler
    'StatHandlerV2',
    # PER
    'PERCalculator',
    # Elo
    'EloCache',
    # League cache
    'cache_season',
    'get_all_seasons',
    'get_season_stats_with_fallback',
    'get_league_constants',
    'get_team_pace',
    'ensure_season_cached',
]
