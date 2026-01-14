"""
Player Filtering Utilities - Shared logic for building player lists for predictions

⚠️ CRITICAL: PREDICTION-ONLY MODULE ⚠️

This module is specifically designed for PREDICTION workflows, NOT training data generation.

## Data Source Distinction:

### TRAINING (DO NOT USE THIS MODULE):
- Uses: stats_nba.homeTeam.injured_players and stats_nba.awayTeam.injured_players
- These are HISTORICAL snapshots captured when games were actually played
- Represents ground truth for "who was actually injured when this game happened"
- Handled by: StatHandlerV2.getInjuryFeatures() and per_calculator with game_doc.injured_players

### PREDICTION (USE THIS MODULE):
- Uses: nba_rosters.roster[].injured and nba_rosters.roster[].starter flags
- These are USER-EDITABLE via the game_details UI toggles
- Gets updated in real-time for upcoming game predictions
- Used by: web/app.py predict() endpoint and agents/matchup_predict.py

## When to use this module:
✅ Web app prediction endpoints (api/predict)
✅ Agent prediction tools (matchup_predict.py)
❌ Training data generation (NBAModel.create_training_data)
❌ Feature calculation for historical games (StatHandlerV2, per_calculator)

This module provides unified player filtering logic used by both the web app and agents
for real-time prediction workflows. Handles roster loading, injury status, and starter
identification from the nba_rosters collection.
"""

from typing import Dict, List, Optional, Tuple


def build_player_lists_for_prediction(
    home_team: str,
    away_team: str,
    season: str,
    game_id: Optional[str] = None,
    game_doc: Optional[dict] = None,
    home_injuries: Optional[List[str]] = None,
    away_injuries: Optional[List[str]] = None,
    home_starters: Optional[List[str]] = None,
    away_starters: Optional[List[str]] = None,
    db = None
) -> Dict[str, Dict[str, List[str]]]:
    """
    Build player_filters dict for PREDICTION with injury/starter information.

    ⚠️ PREDICTION-ONLY: This function uses nba_rosters for injury/starter data.
    DO NOT use for training data generation (which requires stats_nba.injured_players).

    This function consolidates the logic for determining which players are playing
    and which are starters, with support for both database-driven defaults and
    custom overrides.

    Priority for player lists:
    1. Use stats_nba.{home/away}Team.players if game has been clicked into
    2. Use nba_rosters roster

    Priority for injury/starter status:
    1. Custom injuries/starters parameters (if provided)
    2. nba_rosters injury/starter flags

    Args:
        home_team: Home team abbreviation (e.g., 'LAL')
        away_team: Away team abbreviation (e.g., 'BOS')
        season: Season string (e.g., '2023-2024')
        game_id: Optional game ID for looking up game document
        game_doc: Optional pre-loaded game document (avoids DB query if already loaded)
        home_injuries: Optional list of home team injured player IDs (strings).
                      If provided, overrides nba_rosters injury status.
        away_injuries: Optional list of away team injured player IDs (strings).
                      If provided, overrides nba_rosters injury status.
        home_starters: Optional list of home team starter player IDs (strings).
                      If provided, overrides nba_rosters starter status.
                      These players will be forced into the playing list if not already present.
        away_starters: Optional list of away team starter player IDs (strings).
                      If provided, overrides nba_rosters starter status.
                      These players will be forced into the playing list if not already present.
        db: MongoDB database instance

    Returns:
        Dict with structure:
        {
            'home_team_abbrev': {
                'playing': [player_id1, player_id2, ...],
                'starters': [starter_id1, starter_id2, ...]
            },
            'away_team_abbrev': {
                'playing': [player_id1, player_id2, ...],
                'starters': [starter_id1, starter_id2, ...]
            }
        }
    """
    if db is None:
        from nba_app.cli.Mongo import Mongo
        db = Mongo().db

    # Initialize custom lists as empty if not provided
    if home_injuries is None:
        home_injuries = []
    if away_injuries is None:
        away_injuries = []
    if home_starters is None:
        home_starters = []
    if away_starters is None:
        away_starters = []

    # Get game document to check if players list is populated
    if game_doc is None and game_id:
        game_doc = db.stats_nba.find_one({'game_id': game_id})

    # Get rosters for injury/starter status (always from nba_rosters)
    home_roster_doc = db.nba_rosters.find_one({'season': season, 'team': home_team})
    away_roster_doc = db.nba_rosters.find_one({'season': season, 'team': away_team})

    # Build roster maps for quick lookup
    home_roster_map = {}
    away_roster_map = {}

    if home_roster_doc:
        for entry in home_roster_doc.get('roster', []):
            player_id = str(entry.get('player_id', ''))
            home_roster_map[player_id] = {
                'injured': entry.get('injured', False),
                'starter': entry.get('starter', False)
            }

    if away_roster_doc:
        for entry in away_roster_doc.get('roster', []):
            player_id = str(entry.get('player_id', ''))
            away_roster_map[player_id] = {
                'injured': entry.get('injured', False),
                'starter': entry.get('starter', False)
            }

    # Determine base player lists
    # Priority 1: Use stats_nba.{home/away}Team.players if populated (game has been clicked into)
    # Priority 2: Use nba_rosters roster
    home_base_players = []
    away_base_players = []

    if game_doc:
        home_players_list = game_doc.get('homeTeam', {}).get('players', [])
        away_players_list = game_doc.get('awayTeam', {}).get('players', [])

        if home_players_list:
            # Game has been clicked into - use stats_nba players list
            home_base_players = [str(pid) for pid in home_players_list]
        elif home_roster_doc:
            # Use nba_rosters roster
            home_base_players = [str(entry.get('player_id', '')) for entry in home_roster_doc.get('roster', [])]

        if away_players_list:
            # Game has been clicked into - use stats_nba players list
            away_base_players = [str(pid) for pid in away_players_list]
        elif away_roster_doc:
            # Use nba_rosters roster
            away_base_players = [str(entry.get('player_id', '')) for entry in away_roster_doc.get('roster', [])]
    else:
        # No game doc - use nba_rosters
        if home_roster_doc:
            home_base_players = [str(entry.get('player_id', '')) for entry in home_roster_doc.get('roster', [])]
        if away_roster_doc:
            away_base_players = [str(entry.get('player_id', '')) for entry in away_roster_doc.get('roster', [])]

    # Build player_filters: filter by injured status and get starters
    # Custom injuries/starters override the defaults from nba_rosters
    home_playing = []
    home_starters_list = []

    for player_id in home_base_players:
        # Check if custom injuries provided - if so, use those; otherwise use nba_rosters
        is_injured = False
        if home_injuries:
            # Custom injuries provided - use those
            is_injured = player_id in [str(p) for p in home_injuries]
        else:
            # Use nba_rosters injured status
            roster_info = home_roster_map.get(player_id, {})
            is_injured = roster_info.get('injured', False)

        if not is_injured:
            home_playing.append(player_id)

            # Check if starter
            is_starter = False
            if home_starters:
                # Custom starters provided - use those
                is_starter = player_id in [str(p) for p in home_starters]
            else:
                # Use nba_rosters starter status
                roster_info = home_roster_map.get(player_id, {})
                is_starter = roster_info.get('starter', False)

            if is_starter:
                home_starters_list.append(player_id)

    away_playing = []
    away_starters_list = []

    for player_id in away_base_players:
        # Check if custom injuries provided - if so, use those; otherwise use nba_rosters
        is_injured = False
        if away_injuries:
            # Custom injuries provided - use those
            is_injured = player_id in [str(p) for p in away_injuries]
        else:
            # Use nba_rosters injured status
            roster_info = away_roster_map.get(player_id, {})
            is_injured = roster_info.get('injured', False)

        if not is_injured:
            away_playing.append(player_id)

            # Check if starter
            is_starter = False
            if away_starters:
                # Custom starters provided - use those
                is_starter = player_id in [str(p) for p in away_starters]
            else:
                # Use nba_rosters starter status
                roster_info = away_roster_map.get(player_id, {})
                is_starter = roster_info.get('starter', False)

            if is_starter:
                away_starters_list.append(player_id)

    # If custom starters provided, ensure they're in playing list and override
    # This handles the case where a custom starter might have been filtered out
    if home_starters:
        home_starters_list = [str(p) for p in home_starters]
        # Ensure starters are in playing list
        for starter_id in home_starters_list:
            if starter_id not in home_playing:
                home_playing.append(starter_id)

    if away_starters:
        away_starters_list = [str(p) for p in away_starters]
        # Ensure starters are in playing list
        for starter_id in away_starters_list:
            if starter_id not in away_playing:
                away_playing.append(starter_id)

    # Create player filters dict
    player_filters = {
        home_team: {
            'playing': home_playing,
            'starters': home_starters_list
        },
        away_team: {
            'playing': away_playing,
            'starters': away_starters_list
        }
    }

    return player_filters
