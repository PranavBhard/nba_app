#!/usr/bin/env python3
"""
ESPN NBA API Data Fetcher

Fetches game and player stats from ESPN API and stores them in MongoDB.
Uses official ESPN API endpoints instead of web scraping.

Usage:
    python espn_api.py                              # Fetch yesterday's games + players
    python espn_api.py --dates 20210930,20230614   # Fetch date range
    python espn_api.py --team-only                  # Only team stats
    python espn_api.py --players-only               # Only player stats
    python espn_api.py --refresh-players            # Upsert players_nba metadata
    python espn_api.py --refresh-venues              # Refresh venue locations from nba_venues.json
    python espn_api.py --audit-venues                # Find and remove duplicate venue_guid values
    python espn_api.py --player-injuries            # Compute and update injured players for all games
    python espn_api.py --dry-run                    # Don't update, just print
"""

import sys
import os

# Add parent directory to path so we can import nba_app
# Script is in nba_app/cli/, so we need to go up two levels to find the nba_app package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import argparse
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta, datetime
from threading import Lock
from typing import Dict, List, Optional, Tuple
from pytz import timezone, utc
from nba_app.core.mongo import Mongo
from nba_app.core.league_config import load_league_config
from nba_app.tools.geo import get_geocoder, geocode_venue

# Threading constants for batch processing
THREADING_THRESHOLD = 2500  # Min games to trigger threaded processing
CHUNK_SIZE = 500  # Games per thread
MAX_WORKERS = 10  # Concurrent API request threads

mongo = Mongo()
_raw_db = mongo.db


class LeagueDbProxy:
    """
    Database proxy mapping NBA-coded collection attribute access (db.stats_nba, ...)
    to the active league's configured collections.

    This keeps the CLI implementation largely unchanged while enabling
    `--league cbb` (or future leagues).
    """

    _NBA_ATTR_TO_KEY = {
        # Backwards-compat: old NBA-specific attribute names
        "stats_nba": "games",
        "stats_nba_players": "player_stats",
        "players_nba": "players",
        "teams_nba": "teams",
        "nba_venues": "venues",
        "nba_rosters": "rosters",
        "model_config_nba": "model_config_classifier",
        "model_config_points_nba": "model_config_points",
        "master_training_data_nba": "master_training_metadata",
        "cached_league_stats": "cached_league_stats",
        "nba_cached_elo_ratings": "elo_cache",
        "experiment_runs": "experiment_runs",
        "jobs_nba": "jobs",
        # Normalized names (preferred for new code)
        "games": "games",
        "player_stats": "player_stats",
        "players": "players",
        "teams": "teams",
        "venues": "venues",
        "rosters": "rosters",
        "model_config_classifier": "model_config_classifier",
        "model_config_points": "model_config_points",
        "master_training_metadata": "master_training_metadata",
        "elo_cache": "elo_cache",
        "jobs": "jobs",
    }

    def __init__(self, db, league):
        self._db = db
        self._league = league

    def __getitem__(self, name: str):
        return self._db[name]

    def __getattr__(self, name: str):
        key = self._NBA_ATTR_TO_KEY.get(name)
        if key is not None:
            coll_name = self._league.collections.get(key)
            if coll_name:
                return self._db[coll_name]
        return getattr(self._db, name)


def _get_league(league_id: str = None):
    league_id = (league_id or os.environ.get("LEAGUE_ID") or "nba").strip().lower()
    return load_league_config(league_id)


_ACTIVE_LEAGUE = _get_league("nba")
db = LeagueDbProxy(_raw_db, _ACTIVE_LEAGUE)

# ESPN endpoints are league-configured. We build them dynamically per request.

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def parse_espn_utc_to_eastern(date_str: str) -> Optional[datetime]:
    """Parse ESPN UTC date string and convert to Eastern time.

    ESPN returns dates in UTC format like "2026-01-14T00:30Z" or "2026-01-14T00:30:00Z".
    We need to convert to Eastern time to properly match game dates.

    Args:
        date_str: UTC date string from ESPN API

    Returns:
        datetime in Eastern timezone, or None if parsing fails
    """
    if not date_str:
        return None
    try:
        dt_utc = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        eastern = timezone(_ACTIVE_LEAGUE.timezone if _ACTIVE_LEAGUE else 'America/New_York')
        return dt_utc.astimezone(eastern)
    except (ValueError, TypeError):
        return None


def parse_date_range(date_str: str) -> List[date]:
    """Parse comma-separated date range into list of dates."""
    dates = []
    parts = date_str.split(',')
    if len(parts) == 1:
        # Single date
        try:
            d = datetime.strptime(parts[0].strip(), '%Y%m%d').date()
            dates.append(d)
        except ValueError:
            raise ValueError(f"Invalid date format: {parts[0]}. Use YYYYMMDD")
    elif len(parts) == 2:
        # Date range
        try:
            start = datetime.strptime(parts[0].strip(), '%Y%m%d').date()
            end = datetime.strptime(parts[1].strip(), '%Y%m%d').date()
            current = start
            while current <= end:
                dates.append(current)
                current += timedelta(days=1)
        except ValueError as e:
            raise ValueError(f"Invalid date format in range. Use YYYYMMDD,YYYYMMDD")
    else:
        raise ValueError("Invalid date format. Use YYYYMMDD or YYYYMMDD,YYYYMMDD")
    
    return dates


def get_scoreboard(date_obj: date, league_id: str = None) -> Optional[Dict]:
    """Fetch scoreboard for a specific date (league-aware).

    Uses scoreboard_site_template which returns all games (including groups=50 for CBB).
    Returns the raw API response with events at the top level.
    """
    global _ACTIVE_LEAGUE
    if league_id:
        _ACTIVE_LEAGUE = _get_league(league_id)
    date_str = date_obj.strftime('%Y%m%d')
    url = _ACTIVE_LEAGUE.espn_endpoint("scoreboard_site_template").format(YYYYMMDD=date_str)
    print(f"[ESPN API] get_scoreboard URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"[ESPN API] get_scoreboard response keys: {list(data.keys()) if data else 'None'}")
        return data
    except Exception as e:
        print(f"Error fetching scoreboard for {date_obj}: {e}")
        return None


def get_game_summary(game_id: str, league_id: str = None) -> Optional[Dict]:
    """Fetch detailed game summary for a specific game (league-aware)."""
    global _ACTIVE_LEAGUE
    if league_id:
        _ACTIVE_LEAGUE = _get_league(league_id)
    url = _ACTIVE_LEAGUE.espn_endpoint("game_summary_template").format(game_id=game_id)
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching game summary for {game_id}: {e}")
        return None


def get_matchups_with_venue(year: int, month: int, day: int, league_id: str = None) -> List[Dict]:
    """
    Fetch matchups for a date with venue information.

    Uses ESPN API to get game details including venue_guid for each matchup.
    This is used for predictions where we need venue info for travel features.

    Args:
        year, month, day: Date to fetch matchups for

    Returns:
        List of dicts with keys: home_team, away_team, game_id, venue_guid
    """
    date_obj = date(year, month, day)
    scoreboard = get_scoreboard(date_obj, league_id=league_id)

    if not scoreboard:
        return []

    matchups = []

    # Site endpoint returns events at top level
    events = scoreboard.get('events', [])

    for event in events:
        game_id = event.get('id')
        if not game_id:
            continue

        # Extract teams from event - site endpoint nests competitors under competitions
        competitions = event.get('competitions', [])
        if not competitions:
            continue
        competitors = competitions[0].get('competitors', [])

        home_team = None
        away_team = None
        for comp in competitors:
            # Site endpoint has team info nested under 'team'
            team_info = comp.get('team', {})
            abbrev = team_info.get('abbreviation', comp.get('abbreviation', '')).upper()
            if comp.get('homeAway') == 'home':
                home_team = abbrev
            else:
                away_team = abbrev

        if not home_team or not away_team:
            continue

        # Fetch game summary to get venue_guid
        game_summary = get_game_summary(game_id, league_id=league_id)
        venue_guid = None
        if game_summary:
            game_info = game_summary.get('gameInfo', {})
            venue = game_info.get('venue', {})
            venue_guid = venue.get('guid')

            # Verify the game_id matches (sanity check)
            header = game_summary.get('header', {})
            summary_game_id = header.get('id')
            if summary_game_id and str(summary_game_id) != str(game_id):
                print(f"  WARNING: game_id mismatch for {away_team}@{home_team}: "
                      f"scoreboard={game_id}, summary={summary_game_id}")

        matchups.append({
            'home_team': home_team,
            'away_team': away_team,
            'game_id': game_id,
            'venue_guid': venue_guid
        })

    return matchups


def extract_team_stats(team_data: Dict, boxscore: Dict) -> Dict:
    """Extract team stats from boxscore data."""
    stats = {}
    
    # Find team in boxscore
    team_id = team_data.get('id')
    team_stats = None
    for team in boxscore.get('teams', []):
        if team.get('team', {}).get('id') == team_id:
            team_stats = team.get('statistics', [])
            break
    
    if not team_stats:
        return stats
    
    # Map ESPN stat names to our field names
    stat_map = {
        'fieldGoalsMade-fieldGoalsAttempted': ('FG_made', 'FG_att'),
        'fieldGoalPct': 'FGp',
        'threePointFieldGoalsMade-threePointFieldGoalsAttempted': ('three_made', 'three_att'),
        'threePointFieldGoalPct': 'three_percent',
        'freeThrowsMade-freeThrowsAttempted': ('FT_made', 'FT_att'),
        'freeThrowPct': 'FTp',
        'totalRebounds': 'total_reb',
        'offensiveRebounds': 'off_reb',
        'defensiveRebounds': 'def_reb',
        'assists': 'assists',
        'steals': 'steals',
        'blocks': 'blocks',
        'turnovers': 'TO',
        'turnoverPoints': 'pts_off_TO',
        'fastBreakPoints': 'fast_break_pts',
        'pointsInPaint': 'pts_in_paint',
        'fouls': 'PF',
    }
    
    for stat in team_stats:
        name = stat.get('name')
        display_value = stat.get('displayValue', '')
        
        if name in stat_map:
            mapping = stat_map[name]
            if isinstance(mapping, tuple):
                # Split "made-attempted" format
                if '-' in display_value:
                    parts = display_value.split('-')
                    if len(parts) == 2:
                        stats[mapping[0]] = int(parts[0])
                        stats[mapping[1]] = int(parts[1])
            else:
                # Single value
                if name == 'fieldGoalPct' or name == 'threePointFieldGoalPct' or name == 'freeThrowPct':
                    # Percentage - remove % and convert
                    pct_str = display_value.replace('%', '').strip()
                    if pct_str:
                        stats[mapping] = float(pct_str) / 100.0
                else:
                    # Integer value
                    if display_value.isdigit():
                        stats[mapping] = int(display_value)
    
    # Calculate shooting_metric
    if 'FG_made' in stats and 'FG_att' in stats and stats['FG_att'] > 0:
        stats['shooting_metric'] = (stats['FG_made'] + (0.5 * stats.get('three_made', 0))) / float(stats['FG_att'])
    
    # Calculate TO_metric and off_reb_metric (need possessions)
    # These will be calculated later when we have both teams' data
    
    return stats


def extract_season_series(game_summary: Dict) -> Optional[Dict]:
    """Extract season series information."""
    seasonseries = game_summary.get('seasonseries', [])
    if not seasonseries:
        return None
    
    # Get the first (most relevant) series entry
    series = seasonseries[0]
    return {
        'type': series.get('type'),
        'title': series.get('title'),
        'description': series.get('description'),
        'summary': series.get('summary'),
        'series_label': series.get('seriesLabel')
    }


def extract_venue_info(game_summary: Dict) -> Optional[Dict]:
    """Extract venue information and store in nba_venues collection."""
    game_info = game_summary.get('gameInfo', {})
    venue = game_info.get('venue')
    
    if not venue:
        return None
    
    venue_guid = venue.get('guid')
    if not venue_guid:
        return None
    
    venue_data = {
        'venue_guid': venue_guid,
        'id': venue.get('id'),
        'fullName': venue.get('fullName'),
        'shortName': venue.get('shortName'),
        'address': venue.get('address', {}),
        'grass': venue.get('grass', False),
        'images': venue.get('images', [])
    }
    
    return venue_data


def extract_injuries(game_summary: Dict, home_team_abbrev: str, away_team_abbrev: str) -> Dict:
    """
    Extract injuries from game summary API response.
    
    Args:
        game_summary: Full game summary response from ESPN API
        home_team_abbrev: Home team abbreviation (e.g., 'MIL')
        away_team_abbrev: Away team abbreviation (e.g., 'DET')
        
    Returns:
        Dict with 'home' and 'away' keys, each containing list of player IDs
    """
    injuries_data = game_summary.get('injuries', [])
    
    home_injuries = []
    away_injuries = []
    
    for team_injury_group in injuries_data:
        team_info = team_injury_group.get('team', {})
        team_abbrev = team_info.get('abbreviation', '').upper()
        injuries_list = team_injury_group.get('injuries', [])
        
        # Extract player IDs from injuries
        player_ids = []
        for injury in injuries_list:
            athlete = injury.get('athlete', {})
            player_id = athlete.get('id')
            if player_id:
                # Convert to string for consistency
                player_ids.append(str(player_id))
        
        # Assign to home or away based on team abbreviation
        if team_abbrev == home_team_abbrev.upper():
            home_injuries = player_ids
        elif team_abbrev == away_team_abbrev.upper():
            away_injuries = player_ids
    
    return {
        'home': home_injuries,
        'away': away_injuries
    }


def extract_odds(game_summary: Dict) -> Optional[Dict]:
    """Extract odds from game summary pickcenter and format as pregame_lines.

    ESPN provides odds data in the 'pickcenter' array of the game summary response.
    """
    pickcenter = game_summary.get('pickcenter', [])
    if not pickcenter:
        return None

    # Use first provider's odds (usually DraftKings)
    odds = pickcenter[0]
    pregame_lines = {}

    # Extract overUnder
    if odds.get('overUnder') is not None:
        pregame_lines['over_under'] = odds['overUnder']

    # Extract spread (home team spread)
    if odds.get('spread') is not None:
        pregame_lines['spread'] = odds['spread']

    # Extract moneylines from homeTeamOdds/awayTeamOdds
    home_odds = odds.get('homeTeamOdds', {})
    if home_odds and home_odds.get('moneyLine') is not None:
        pregame_lines['home_ml'] = home_odds['moneyLine']

    away_odds = odds.get('awayTeamOdds', {})
    if away_odds and away_odds.get('moneyLine') is not None:
        pregame_lines['away_ml'] = away_odds['moneyLine']

    return pregame_lines if pregame_lines else None


def parse_gametime(event_date_str: str) -> Optional[datetime]:
    """Parse event date string (already in UTC) and return as UTC datetime.
    
    The date field from ESPN API is already in UTC. We parse and store it as-is.
    """
    if not event_date_str:
        return None
    
    try:
        # Try parsing with fromisoformat first (handles ISO 8601 format with timezone)
        try:
            # Replace 'Z' with '+00:00' for UTC
            iso_str = event_date_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(iso_str)
            # Ensure it's UTC timezone-aware
            if dt.tzinfo is None:
                dt = utc.localize(dt)
            elif dt.tzinfo != utc:
                # Convert to UTC if it has a different timezone
                dt = dt.astimezone(utc)
            return dt
        except (ValueError, AttributeError):
            # Fallback: parse manually
            pass
        
        # Manual parsing fallback
        if 'T' in event_date_str:
            # Has time component
            date_part = event_date_str.split('T')[0]
            time_part = event_date_str.split('T')[1]
            
            # Remove timezone indicators (Z, +00:00, etc.) - date is already UTC
            if time_part.endswith('Z'):
                time_part = time_part[:-1]
            elif '+' in time_part:
                time_part = time_part.split('+')[0]
            elif '-' in time_part and time_part.count('-') > 1:
                # Check if last part is timezone offset (has :)
                parts = time_part.rsplit('-', 1)
                if len(parts) == 2 and ':' in parts[1]:
                    time_part = parts[0]
            
            # Parse the datetime
            dt_str = f"{date_part}T{time_part}"
            try:
                dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
            
            # Localize to UTC (date is already in UTC)
            dt_utc = utc.localize(dt)
            return dt_utc
        else:
            # Just date, assume midnight UTC
            dt = datetime.strptime(event_date_str, '%Y-%m-%d')
            dt_utc = utc.localize(dt)
            return dt_utc
        
    except Exception as e:
        print(f"  Warning: Could not parse gametime '{event_date_str}': {e}")
        return None


def extract_player_stats(player_data: Dict, game_id: str, game_date: str, team_name: str, home: bool, opponent: str, stat_group: Dict, season: str = None, team_id: str = None, opponent_id: str = None) -> Dict:
    """Extract player stats from API response.

    Args:
        player_data: Player data from ESPN API
        game_id: ESPN game ID
        game_date: Game date string (YYYY-MM-DD)
        team_name: Team abbreviation
        home: Whether this is the home team
        opponent: Opponent team abbreviation
        stat_group: Stat group containing keys and athlete data
        season: Season string (e.g., '2024-2025'). If not provided, calculated from game_date.
        team_id: ESPN team ID (included when league.include_team_id is True)
        opponent_id: ESPN opponent team ID (included when league.include_team_id is True)
    """
    athlete = player_data.get('athlete', {})
    stats_array = player_data.get('stats', [])

    player_id = athlete.get('id')
    if not player_id:
        return None

    # Map stat keys to our field names - get from stat_group
    stat_keys = stat_group.get('keys', [])
    stat_values = stats_array

    # Use provided season or calculate from game_date as fallback
    if not season:
        game_date_obj = datetime.strptime(game_date, '%Y-%m-%d').date()
        cutover_month = (_ACTIVE_LEAGUE.season_rules.get('season_cutover_month', 8) if _ACTIVE_LEAGUE else 8)
        if game_date_obj.month > cutover_month:
            season = f'{game_date_obj.year}-{game_date_obj.year+1}'
        else:
            season = f'{game_date_obj.year-1}-{game_date_obj.year}'

    player_stats = {
        'player_id': str(player_id),
        'game_id': game_id,
        'date': game_date,
        'season': season,
        'team': team_name,
        'home': home,
        'opponent': opponent,
        'starter': player_data.get('starter', False),
        'active': player_data.get('active', True),
        'didNotPlay': player_data.get('didNotPlay', False),
        'guid': athlete.get('guid'),
        'short_name': athlete.get('shortName'),
        'player_name': athlete.get('displayName'),
        # Note: headshot and position are stored in players collection, not player_stats
    }

    # Store headshot in players collection (not player_stats) if present
    headshot_url = athlete.get('headshot', {}).get('href') if athlete.get('headshot') else None
    if headshot_url:
        player_stats['_headshot_for_players'] = headshot_url  # Temporary field for caller to handle

    # Store position in players collection (not player_stats) if present
    pos_name = athlete.get('position', {}).get('name') if athlete.get('position') else None
    pos_display_name = athlete.get('position', {}).get('displayName') if athlete.get('position') else None
    if pos_name or pos_display_name:
        player_stats['_position_for_players'] = {
            'pos_name': pos_name,
            'pos_display_name': pos_display_name
        }  # Temporary field for caller to handle

    # Include team_id fields when league config specifies
    if team_id is not None:
        player_stats['team_id'] = str(team_id)
    if opponent_id is not None:
        player_stats['opponent_id'] = str(opponent_id)
    
    # Extract stats - use key names matching the existing collection format
    stats_dict = {}
    if stat_keys and stat_values:
        for key, value in zip(stat_keys, stat_values):
            if key == 'minutes':
                # Parse "47" or "47:00" format
                if ':' in str(value):
                    parts = str(value).split(':')
                    stats_dict['min'] = int(parts[0]) + int(parts[1]) / 60.0
                else:
                    try:
                        stats_dict['min'] = float(value)
                    except:
                        stats_dict['min'] = 0
            elif key == 'points':
                stats_dict['pts'] = int(value) if str(value).isdigit() else 0
            elif key == 'fieldGoalsMade-fieldGoalsAttempted':
                if '-' in str(value):
                    parts = str(value).split('-')
                    stats_dict['fg_made'] = int(parts[0]) if parts[0].isdigit() else 0
                    stats_dict['fg_att'] = int(parts[1]) if parts[1].isdigit() else 0
            elif key == 'threePointFieldGoalsMade-threePointFieldGoalsAttempted':
                if '-' in str(value):
                    parts = str(value).split('-')
                    stats_dict['three_made'] = int(parts[0]) if parts[0].isdigit() else 0
                    stats_dict['three_att'] = int(parts[1]) if parts[1].isdigit() else 0
            elif key == 'freeThrowsMade-freeThrowsAttempted':
                if '-' in str(value):
                    parts = str(value).split('-')
                    stats_dict['ft_made'] = int(parts[0]) if parts[0].isdigit() else 0
                    stats_dict['ft_att'] = int(parts[1]) if parts[1].isdigit() else 0
            elif key == 'rebounds':
                stats_dict['reb'] = int(value) if str(value).isdigit() else 0
            elif key == 'offensiveRebounds':
                stats_dict['oreb'] = int(value) if str(value).isdigit() else 0
            elif key == 'defensiveRebounds':
                stats_dict['dreb'] = int(value) if str(value).isdigit() else 0
            elif key == 'assists':
                stats_dict['ast'] = int(value) if str(value).isdigit() else 0
            elif key == 'turnovers':
                stats_dict['to'] = int(value) if str(value).isdigit() else 0
            elif key == 'steals':
                stats_dict['stl'] = int(value) if str(value).isdigit() else 0
            elif key == 'blocks':
                stats_dict['blk'] = int(value) if str(value).isdigit() else 0
            elif key == 'fouls':
                stats_dict['pf'] = int(value) if str(value).isdigit() else 0
            elif key == 'plusMinus':
                # Remove + or - sign
                pm_str = str(value).replace('+', '').replace('-', '')
                if pm_str.lstrip('-').isdigit():
                    stats_dict['plus_minus'] = int(pm_str) if not str(value).startswith('-') else -int(pm_str)
    
    player_stats['stats'] = stats_dict
    
    return player_stats


def process_game(game_id: str, game_date: date, team_only: bool, players_only: bool, dry_run: bool, event: Optional[Dict] = None) -> Tuple[bool, int]:
    """Process a single game: fetch data and store in MongoDB.
    
    Args:
        game_id: ESPN game ID
        game_date: Date of the game
        team_only: Only process team stats
        players_only: Only process player stats
        dry_run: Don't update database
        event: Optional event data from scoreboard (for odds and gametime)
    """
    game_summary = get_game_summary(game_id)
    if not game_summary:
        return False, 0
    
    # Extract basic game info
    header = game_summary.get('header', {})
    competitions0 = header.get('competitions', [{}])[0]
    competitors = competitions0.get('competitors', [])

    # If the game isn't completed yet, do NOT write placeholder outcomes/scores.
    # The web UI's game list uses presence of these fields to indicate "pulled".
    status_type = (competitions0.get('status') or {}).get('type') or {}
    is_completed = bool(status_type.get('completed', False))
    
    if len(competitors) != 2:
        print(f"  Warning: Game {game_id} has {len(competitors)} competitors, skipping")
        return False, 0
    
    # Determine home/away
    home_team = None
    away_team = None
    home_score = 0
    away_score = 0
    home_linescores = []
    away_linescores = []
    
    for comp in competitors:
        if comp.get('homeAway') == 'home':
            home_team = comp.get('team', {})
            home_score = int(comp.get('score', 0) or 0)
            home_linescores = comp.get('linescores', [])
        else:
            away_team = comp.get('team', {})
            away_score = int(comp.get('score', 0) or 0)
            away_linescores = comp.get('linescores', [])
    
    if not home_team or not away_team:
        print(f"  Warning: Could not determine home/away for game {game_id}")
        return False, 0
    
    # Use abbreviation (3-letter code) for team names
    home_name = home_team.get('abbreviation', '').upper()
    away_name = away_team.get('abbreviation', '').upper()
    
    if not home_name or not away_name:
        print(f"  Warning: Missing team abbreviations for game {game_id}")
        return False, 0

    if not is_completed:
        # Skip until final so we don't upsert homeWon=false and points=0 for scheduled games.
        detail = status_type.get('shortDetail') or status_type.get('detail') or status_type.get('description') or 'Not completed'
        print(f"  Skipping {away_name}@{home_name} ({game_id}): game not completed yet ({detail})")
        return False, 0
    
    date_str = game_date.strftime('%Y-%m-%d')
    year, month, day = game_date.year, game_date.month, game_date.day

    # Extract ESPN-provided season year from API response
    # ESPN provides season as ending year (e.g., 2026 for '2025-2026' season)
    # This is more reliable than date-based calculation for COVID/lockout years
    def _extract_espn_season_year() -> Optional[int]:
        # Try competitions0.season (NBA scoreboard format - integer)
        comp_season = competitions0.get('season')
        if isinstance(comp_season, int):
            return comp_season
        if isinstance(comp_season, str) and comp_season.isdigit():
            return int(comp_season)

        # Try header.season.year (game summary format - dict with year)
        header_season = header.get('season')
        if isinstance(header_season, dict):
            season_year = header_season.get('year')
            if isinstance(season_year, int):
                return season_year
            if isinstance(season_year, str) and season_year.isdigit():
                return int(season_year)

        # Try competitions0.season as dict (alternative format)
        if isinstance(comp_season, dict):
            season_year = comp_season.get('year')
            if isinstance(season_year, int):
                return season_year
            if isinstance(season_year, str) and season_year.isdigit():
                return int(season_year)

        return None

    espn_season_year = _extract_espn_season_year()

    if espn_season_year:
        # ESPN provides ending year, so season is "{year-1}-{year}"
        season = f'{espn_season_year - 1}-{espn_season_year}'
    else:
        # Fallback to date-based calculation using league config
        cutover_month = (_ACTIVE_LEAGUE.season_rules.get('season_cutover_month', 8) if _ACTIVE_LEAGUE else 8)
        if month > cutover_month:
            season = f'{year}-{year+1}'
        else:
            season = f'{year-1}-{year}'

    # Determine game type (league-configurable; uses ESPN season.type + season.slug when present).
    # ESPN shapes vary: season.type may be an int or an object with {id,type,name,abbreviation}.
    def _extract_season_type_info() -> Tuple[Optional[int], Optional[str], Optional[str], Optional[str]]:
        # Prefer competition season if present, else header season
        season_obj = competitions0.get('season') or header.get('season') or {}
        if not isinstance(season_obj, dict):
            season_obj = {}

        slug = season_obj.get('slug')

        t = season_obj.get('type')
        type_id = None
        type_name = None
        type_abbrev = None

        if isinstance(t, dict):
            # CBB scoreboard often provides this richer object
            raw_type = t.get('type') if t.get('type') is not None else t.get('id')
            try:
                type_id = int(raw_type) if raw_type is not None else None
            except Exception:
                type_id = None
            type_name = t.get('name')
            type_abbrev = t.get('abbreviation')
        else:
            try:
                type_id = int(t) if t is not None else None
            except Exception:
                type_id = None

        # If slug wasn't present on season_obj, sometimes it lives in header.season.slug
        if not slug:
            s2 = header.get('season') if isinstance(header.get('season'), dict) else {}
            slug = (s2 or {}).get('slug') if isinstance(s2, dict) else None

        return type_id, (str(slug) if slug is not None else None), (str(type_name) if type_name is not None else None), (str(type_abbrev) if type_abbrev is not None else None)

    def _extract_tournament_info() -> Tuple[Optional[bool], Optional[Dict]]:
        # Best-effort: different endpoints nest tournament info differently.
        candidates = [
            competitions0.get('tournament'),
            header.get('tournament'),
            game_summary.get('tournament'),
        ]
        for c in candidates:
            if isinstance(c, dict):
                is_t = c.get('isTournament')
                if isinstance(is_t, bool):
                    return is_t, c
            if isinstance(c, bool):
                return c, None

        # Direct boolean flag
        for c in [competitions0.get('isTournament'), header.get('isTournament')]:
            if isinstance(c, bool):
                return c, None
        return None, None

    season_type_id, season_type_slug, season_type_name, season_type_abbrev = _extract_season_type_info()
    is_tournament, tournament_obj = _extract_tournament_info()

    # League-configurable mapping: season.game_type_map
    season_cfg = (_ACTIVE_LEAGUE.season_rules if _ACTIVE_LEAGUE else {}) or {}
    game_type_map = season_cfg.get('game_type_map') or {}
    game_type = None
    if season_type_id is not None:
        game_type = game_type_map.get(season_type_id) or game_type_map.get(str(season_type_id))

    # Fallback mapping if config missing
    if not game_type:
        if season_type_id == 1:
            game_type = 'preseason'
        elif season_type_id == 3:
            game_type = 'playoffs' if (_ACTIVE_LEAGUE and _ACTIVE_LEAGUE.league_id == 'nba') else 'postseason'
        else:
            game_type = 'regseason'

    # Optional: play-in text override (NBA only by default)
    if bool(season_cfg.get('playin_text_override', False)):
        text_fields = [
            str(header.get('name') or ''),
            str(header.get('shortName') or ''),
            str(competitions0.get('type') or ''),
            str((competitions0.get('status') or {}).get('type', {}).get('detail') or ''),
        ]
        text_blob = ' '.join([t for t in text_fields if t]).lower()
        if 'play-in' in text_blob:
            game_type = 'playin'

    # Optional: for CBB postseason games, allow a tournament-specific game_type.
    if is_tournament is True and season_type_id == 3:
        tournament_game_type = season_cfg.get('postseason_tournament_game_type')
        if isinstance(tournament_game_type, str) and tournament_game_type.strip():
            game_type = tournament_game_type.strip()
    
    # Extract venue info
    venue_data = extract_venue_info(game_summary)
    venue_guid = None
    if venue_data:
        venue_guid = venue_data['venue_guid']
        if not dry_run:
            # Upsert venue by venue_guid only (preserve existing fields)
            db.nba_venues.update_one(
                {'venue_guid': venue_guid},
                {'$set': venue_data},
                upsert=True
            )
    
    # Extract season series
    series_data = extract_season_series(game_summary)
    
    # Extract odds from game_summary pickcenter
    pregame_lines = extract_odds(game_summary)
    
    # Extract gametime from seasonseries[0].events where event id matches game_id
    # This is the preferred source as it has the most accurate game time
    gametime = None
    seasonseries = game_summary.get('seasonseries', [])
    if seasonseries and len(seasonseries) > 0:
        first_series = seasonseries[0]
        events = first_series.get('events', [])
        # Find the event where id matches game_id
        for evt in events:
            evt_id = evt.get('id')
            # Handle both string and int comparisons
            if evt_id and (str(evt_id) == str(game_id) or evt_id == game_id):
                event_date_str = evt.get('date')
                if event_date_str:
                    gametime = parse_gametime(event_date_str)
                    break
    
    # Fallback to event (if provided) or from game_summary header
    if not gametime:
        if event:
            event_date_str = event.get('date')
            if event_date_str:
                gametime = parse_gametime(event_date_str)
        else:
            # Try to get date from game_summary header
            header = game_summary.get('header', {})
            competitions = header.get('competitions', [])
            if competitions:
                event_date_str = competitions[0].get('date')
                if event_date_str:
                    gametime = parse_gametime(event_date_str)
    
    # Build game document
    game_data = {
        'game_id': game_id,
        'date': date_str,
        'year': year,
        'month': month,
        'day': day,
        'season': season,
        'espn_season_year': espn_season_year,  # ESPN-provided season year (for audit/debugging)
        'game_type': game_type,
        # Helpful, standardized season/type metadata (especially for CBB)
        'season_type_id': season_type_id,
        'season_type_slug': season_type_slug,
        'season_type_name': season_type_name,
        'season_type_abbrev': season_type_abbrev,
        'isTournament': is_tournament,
        'description': (header.get('name') or header.get('shortName') or 'Regular Season'),
        'homeWon': home_score > away_score,
        'OT': False,  # Will be determined from periods
        'venue_guid': venue_guid,
        'espn_link': f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}",
    }
    
    # Add gametime if available
    if gametime:
        game_data['gametime'] = gametime
    
    # Add series data
    if series_data:
        game_data.update(series_data)
    
    # Add pregame_lines if available
    if pregame_lines:
        game_data['pregame_lines'] = pregame_lines
    
    # Extract team stats from boxscore
    boxscore = game_summary.get('boxscore', {})
    teams = boxscore.get('teams', [])
    
    home_stats = {}
    away_stats = {}
    
    for team in teams:
        team_info = team.get('team', {})
        team_id = team_info.get('id')
        is_home = team.get('homeAway') == 'home'
        
        if team_id == home_team.get('id'):
            home_stats = extract_team_stats(team_info, {'teams': [team]})
            home_stats['team_id'] = str(team_id) if team_id is not None else None
            home_stats['name'] = home_name
            home_stats['points'] = home_score
        elif team_id == away_team.get('id'):
            away_stats = extract_team_stats(team_info, {'teams': [team]})
            away_stats['team_id'] = str(team_id) if team_id is not None else None
            away_stats['name'] = away_name
            away_stats['points'] = away_score
    
    # Calculate TO_metric and off_reb_metric (need possessions)
    if 'FG_att' in home_stats and 'FG_att' in away_stats:
        possessions_home = home_stats['FG_att'] - home_stats.get('off_reb', 0) + home_stats.get('TO', 0) + (0.4 * home_stats.get('FT_att', 0))
        possessions_away = away_stats['FG_att'] - away_stats.get('off_reb', 0) + away_stats.get('TO', 0) + (0.4 * away_stats.get('FT_att', 0))
        possessions = (possessions_home + possessions_away) / 2.0
        
        if possessions > 0:
            home_stats['TO_metric'] = home_stats.get('TO', 0) / float(possessions)
            away_stats['TO_metric'] = away_stats.get('TO', 0) / float(possessions)
        
        if 'off_reb' in home_stats and 'def_reb' in away_stats:
            total_reb = home_stats.get('off_reb', 0) + away_stats.get('def_reb', 0)
            if total_reb > 0:
                home_stats['off_reb_metric'] = home_stats.get('off_reb', 0) / float(total_reb)
        
        if 'off_reb' in away_stats and 'def_reb' in home_stats:
            total_reb = away_stats.get('off_reb', 0) + home_stats.get('def_reb', 0)
            if total_reb > 0:
                away_stats['off_reb_metric'] = away_stats.get('off_reb', 0) / float(total_reb)
    
    # Extract period scores from linescores
    # Note: ESPN API returns 'displayValue' (not 'value') for quarter scores
    if home_linescores and away_linescores:
        home_stats['points1q'] = int(home_linescores[0].get('displayValue', 0)) if len(home_linescores) > 0 else 0
        home_stats['points2q'] = int(home_linescores[1].get('displayValue', 0)) if len(home_linescores) > 1 else 0
        home_stats['points3q'] = int(home_linescores[2].get('displayValue', 0)) if len(home_linescores) > 2 else 0
        home_stats['points4q'] = int(home_linescores[3].get('displayValue', 0)) if len(home_linescores) > 3 else 0

        away_stats['points1q'] = int(away_linescores[0].get('displayValue', 0)) if len(away_linescores) > 0 else 0
        away_stats['points2q'] = int(away_linescores[1].get('displayValue', 0)) if len(away_linescores) > 1 else 0
        away_stats['points3q'] = int(away_linescores[2].get('displayValue', 0)) if len(away_linescores) > 2 else 0
        away_stats['points4q'] = int(away_linescores[3].get('displayValue', 0)) if len(away_linescores) > 3 else 0

        # Check for OT periods
        ot_periods = len(home_linescores) - 4
        if ot_periods > 0:
            game_data['OT'] = True
            home_ot = sum(int(home_linescores[i].get('displayValue', 0)) for i in range(4, len(home_linescores)))
            away_ot = sum(int(away_linescores[i].get('displayValue', 0)) for i in range(4, len(away_linescores)))
            home_stats['pointsOT'] = home_ot
            away_stats['pointsOT'] = away_ot
        else:
            game_data['OT'] = False
            home_stats['pointsOT'] = 0
            away_stats['pointsOT'] = 0
    
    game_data['homeTeam'] = home_stats
    game_data['awayTeam'] = away_stats

    # Store team stats
    if not players_only and not dry_run:
        query = {
            'game_id': game_id
        }
        # Convert nested objects to dot notation to preserve existing nested fields
        # Using $set with nested objects like {homeTeam: {...}} replaces the ENTIRE
        # nested object. Dot notation like {'homeTeam.points': 100} merges instead.
        flat_update = {}
        for key, value in game_data.items():
            if key in ('homeTeam', 'awayTeam') and isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    flat_update[f'{key}.{nested_key}'] = nested_value
            else:
                flat_update[key] = value

        update_doc = {'$set': flat_update}
        db.stats_nba.update_one(query, update_doc, upsert=True)
    
    if dry_run:
        print(f"  [DRY RUN] Would store game: {away_name} @ {home_name} ({away_score}-{home_score})")
    else:
        print(f"  ✓ Stored game: {away_name} @ {home_name} ({away_score}-{home_score})")
    
    # Extract and store player stats
    player_count = 0
    if not team_only:
        players = boxscore.get('players', [])

        # Get team IDs for player stats (when league config includes them)
        home_team_id = home_team.get('id')
        away_team_id = away_team.get('id')
        include_team_ids = _ACTIVE_LEAGUE.include_team_id if _ACTIVE_LEAGUE else False

        for team_player_data in players:
            team_info = team_player_data.get('team', {})
            team_id = team_info.get('id')
            is_home = team_id == home_team_id
            team_name = home_name if is_home else away_name
            opponent = away_name if is_home else home_name  # Opponent is the other team
            opponent_team_id = away_team_id if is_home else home_team_id

            # Get statistics array for this team
            statistics = team_player_data.get('statistics', [])
            if not statistics:
                continue

            # Each statistic object contains athletes
            for stat_group in statistics:
                athletes = stat_group.get('athletes', [])
                for athlete_data in athletes:
                    # Pass team_id/opponent_id only when league config includes them
                    player_stats = extract_player_stats(
                        athlete_data, game_id, date_str, team_name, is_home, opponent, stat_group,
                        season=season,
                        team_id=team_id if include_team_ids else None,
                        opponent_id=opponent_team_id if include_team_ids else None
                    )
                    if player_stats:
                        # Always insert all players, even if they didn't play (stats may be empty)
                        # This allows us to track who was on the roster but didn't play
                        if not dry_run:
                            # Extract headshot and position for players collection (stored there, not in player_stats)
                            headshot_url = player_stats.pop('_headshot_for_players', None)
                            position_data = player_stats.pop('_position_for_players', None)

                            query = {
                                'game_id': game_id,
                                'player_id': player_stats['player_id']
                            }
                            db.stats_nba_players.update_one(query, {'$set': player_stats}, upsert=True)

                            # Update players collection with headshot and position if present
                            # Use upsert=True to create player entry if it doesn't exist
                            # Only include non-null values to avoid overwriting with nulls
                            players_update = {
                                'player_id': player_stats['player_id'],
                                'player_name': player_stats.get('player_name'),
                            }
                            if headshot_url:
                                players_update['headshot'] = headshot_url
                            if position_data:
                                if position_data.get('pos_name'):
                                    players_update['pos_name'] = position_data['pos_name']
                                if position_data.get('pos_display_name'):
                                    players_update['pos_display_name'] = position_data['pos_display_name']

                            # Use league-aware players collection
                            players_collection_name = _ACTIVE_LEAGUE.collections.get('players', 'players_nba') if _ACTIVE_LEAGUE else 'players_nba'
                            db[players_collection_name].update_one(
                                {'player_id': player_stats['player_id']},
                                {'$set': players_update},
                                upsert=True  # Create player if doesn't exist
                            )
                        player_count += 1
    
    if not team_only:
        if dry_run:
            print(f"    [DRY RUN] Would store {player_count} player stats")
        else:
            print(f"    ✓ Stored {player_count} player stats")
    
    return True, player_count


def refresh_players_metadata(dry_run: bool = False):
    """Refresh players_nba collection with metadata from stats_nba_players.

    Note: headshot and position are NOT included here - they are stored/updated
    directly in the players collection during game sync, not aggregated from player_stats.
    """
    print("Refreshing players_nba metadata...")

    # Get unique players from stats_nba_players
    # Note: headshot and position are intentionally excluded - they're managed separately in players collection
    pipeline = [
        {
            '$group': {
                '_id': '$player_id',
                'player_name': {'$first': '$player_name'},
                'short_name': {'$first': '$short_name'},
                'guid': {'$first': '$guid'},
                'last_game_date': {'$max': '$date'},
            }
        }
    ]

    players = list(db.stats_nba_players.aggregate(pipeline))

    if dry_run:
        print(f"  [DRY RUN] Would upsert {len(players)} players")
        for p in players[:5]:  # Show first 5
            print(f"    - {p.get('player_name')} (ID: {p.get('_id')})")
        if len(players) > 5:
            print(f"    ... and {len(players) - 5} more")
    else:
        for player in players:
            # Construct ESPN link from player name
            player_name = player.get('player_name', '')
            player_slug = player_name.lower().replace(' ', '-').replace("'", '').replace('.', '')
            espn_link = f"https://www.espn.com/nba/player/_/id/{player['_id']}/{player_slug}"

            # Note: headshot and position are NOT included - they're updated separately during game sync
            player_doc = {
                'player_id': player['_id'],
                'player_name': player.get('player_name'),
                'short_name': player.get('short_name'),
                'guid': player.get('guid'),
                'last_game_date': player.get('last_game_date'),
                'espn_link': espn_link,
                'updated_at': datetime.now()
            }

            db.players_nba.update_one(
                {'player_id': player['_id']},
                {'$set': player_doc, '$setOnInsert': {'created_at': datetime.now()}},
                upsert=True
            )

        print(f"  ✓ Upserted {len(players)} players")


def refresh_venues_location(dry_run: bool = False):
    """Refresh nba_venues collection with location data from nba_venues.json."""
    print("Refreshing nba_venues location data...")
    
    # Load venue location data from JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'nba_venues.json')
    
    if not os.path.exists(json_path):
        print(f"  Error: {json_path} not found")
        return
    
    with open(json_path, 'r') as f:
        venue_locations = json.load(f)
    
    print(f"  Loaded {len(venue_locations)} venues from JSON")
    
    matched_count = 0
    unmatched_count = 0
    matched_venues = []
    unmatched_venues = []
    
    # Get all venues from database
    db_venues = list(db.nba_venues.find({}, {'venue_guid': 1, 'fullName': 1}))
    print(f"  Found {len(db_venues)} venues in database")
    
    # Create a lookup dict by fullName
    location_lookup = {v['fullName']: v for v in venue_locations}
    
    for db_venue in db_venues:
        full_name = db_venue.get('fullName')
        venue_guid = db_venue.get('venue_guid')
        
        if not full_name or not venue_guid:
            continue
        
        # Try to find matching location data
        location_data = location_lookup.get(full_name)
        
        if location_data and 'lat' in location_data and 'lon' in location_data:
            location = {
                'lat': location_data['lat'],
                'lon': location_data['lon']
            }
            
            if not dry_run:
                db.nba_venues.update_one(
                    {'venue_guid': venue_guid},
                    {'$set': {'location': location}}
                )
            
            matched_count += 1
            matched_venues.append(full_name)
        else:
            unmatched_count += 1
            unmatched_venues.append(full_name)
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Results:")
    print(f"  Matched: {matched_count}")
    if matched_venues:
        print(f"    Venues matched:")
        for v in matched_venues[:10]:
            print(f"      - {v}")
        if len(matched_venues) > 10:
            print(f"      ... and {len(matched_venues) - 10} more")
    
    print(f"  Unmatched: {unmatched_count}")
    if unmatched_venues:
        print(f"    Venues not matched:")
        for v in unmatched_venues[:10]:
            print(f"      - {v}")
        if len(unmatched_venues) > 10:
            print(f"      ... and {len(unmatched_venues) - 10} more")


def audit_venues(dry_run: bool = False):
    """Find and remove duplicate venue_guid values in nba_venues collection."""
    print("Auditing nba_venues for duplicate venue_guid values...")
    
    # Find all venues
    all_venues = list(db.nba_venues.find({}))
    print(f"  Found {len(all_venues)} total venues in database")
    
    # Group by venue_guid to find duplicates
    venues_by_guid = {}
    for venue in all_venues:
        venue_guid = venue.get('venue_guid')
        if not venue_guid:
            continue
        
        if venue_guid not in venues_by_guid:
            venues_by_guid[venue_guid] = []
        venues_by_guid[venue_guid].append(venue)
    
    # Find duplicates
    duplicates = {guid: venues for guid, venues in venues_by_guid.items() if len(venues) > 1}
    
    if not duplicates:
        print("  ✓ No duplicate venue_guid values found")
        return
    
    print(f"  Found {len(duplicates)} venue_guid values with duplicates")
    
    total_to_delete = 0
    venues_to_delete = []
    
    for venue_guid, venues in duplicates.items():
        # Determine which one to keep
        # Prefer the one with the most complete data (most fields)
        # If tied, keep the first one
        venues_with_scores = []
        for venue in venues:
            # Count non-None fields as a measure of completeness
            field_count = sum(1 for v in venue.values() if v is not None and v != {})
            venues_with_scores.append((field_count, venue))
        
        # Sort by field count (descending), then by _id for consistency
        venues_with_scores.sort(key=lambda x: (x[0], str(x[1].get('_id', ''))), reverse=True)
        
        # Keep the first one (most complete)
        venue_to_keep = venues_with_scores[0][1]
        venues_to_remove = [v[1] for v in venues_with_scores[1:]]
        
        total_to_delete += len(venues_to_remove)
        
        for venue_to_remove in venues_to_remove:
            venues_to_delete.append({
                'venue_guid': venue_guid,
                '_id': venue_to_remove.get('_id'),
                'fullName': venue_to_remove.get('fullName', 'Unknown'),
                'kept_id': venue_to_keep.get('_id'),
                'kept_fullName': venue_to_keep.get('fullName', 'Unknown')
            })
    
    print(f"\n  Found {total_to_delete} duplicate venue(s) to remove")
    
    if venues_to_delete:
        print(f"\n  Duplicates to {'remove' if not dry_run else '[DRY RUN] would remove'}:")
        for i, dup in enumerate(venues_to_delete[:20], 1):
            print(f"    {i}. venue_guid: {dup['venue_guid']}")
            print(f"       Remove: _id={dup['_id']}, fullName='{dup['fullName']}'")
            print(f"       Keep:   _id={dup['kept_id']}, fullName='{dup['kept_fullName']}'")
        
        if len(venues_to_delete) > 20:
            print(f"    ... and {len(venues_to_delete) - 20} more")
    
    if not dry_run:
        # Delete the duplicates
        deleted_count = 0
        for dup in venues_to_delete:
            result = db.nba_venues.delete_one({'_id': dup['_id']})
            if result.deleted_count > 0:
                deleted_count += 1
        
        print(f"\n  ✓ Removed {deleted_count} duplicate venue(s)")
    else:
        print(f"\n  [DRY RUN] Would remove {total_to_delete} duplicate venue(s)")


def update_venue_locations(dry_run: bool = False):
    """Update venues in nba_venues collection that don't have a location field using Nominatim geocoding."""
    print("=" * 70)
    print("Updating Venue Locations via Geocoding")
    print("=" * 70)
    
    # Find venues without location field
    print("\nFinding venues without location field...")
    venues_without_location = list(db.nba_venues.find(
        {'location': {'$exists': False}},
        {'venue_guid': 1, 'fullName': 1, 'address': 1}
    ))
    
    if not venues_without_location:
        print("✓ All venues already have location data.")
        return
    
    print(f"Found {len(venues_without_location)} venues without location data.\n")
    
    # Initialize geocoder
    geolocator = get_geocoder()
    
    updated_count = 0
    failed_count = 0
    skipped_count = 0
    
    for i, venue in enumerate(venues_without_location, 1):
        venue_guid = venue.get('venue_guid')
        full_name = venue.get('fullName')
        address = venue.get('address') or {}
        
        city = address.get('city', '') if isinstance(address, dict) else ''
        state = address.get('state', '') if isinstance(address, dict) else ''
        
        if not full_name:
            print(f"[{i}/{len(venues_without_location)}] Skipping venue with guid {venue_guid} (no fullName)")
            skipped_count += 1
            continue
        
        # Build query string: "{fullName}, {address.city}, {address.state}"
        query_parts = [full_name]
        if city:
            query_parts.append(city)
        if state:
            query_parts.append(state)
        venue_query = ", ".join(query_parts)
        
        print(f"[{i}/{len(venues_without_location)}] Geocoding: {venue_query}...", end=' ')
        
        # Geocode (with rate limiting - Nominatim allows ~1 request/second)
        if i > 1:
            time.sleep(1.1)  # Add delay between requests to avoid rate limiting
        
        lat, lon = geocode_venue(venue_query, geolocator)
        
        if lat and lon:
            location = {'lat': lat, 'lon': lon}
            
            if dry_run:
                print(f"✓ Would update: lat={lat}, lon={lon}")
            else:
                # Update venue in database
                result = db.nba_venues.update_one(
                    {'venue_guid': venue_guid},
                    {'$set': {'location': location}}
                )
                
                if result.modified_count > 0:
                    print(f"✓ Updated: lat={lat}, lon={lon}")
                    updated_count += 1
                else:
                    print(f"⚠ Update failed (no documents modified)")
                    failed_count += 1
        else:
            print(f"✗ Failed to geocode")
            failed_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    if dry_run:
        print(f"Would update: {updated_count} venues")
    else:
        print(f"Updated: {updated_count} venues")
    print(f"Failed: {failed_count} venues")
    if skipped_count > 0:
        print(f"Skipped: {skipped_count} venues")
    print("=" * 70)


def _parse_game_date(game: Dict) -> Optional[date]:
    """Parse game date from game document."""
    game_date_str = game.get('date')
    if game_date_str:
        try:
            return datetime.strptime(game_date_str, '%Y-%m-%d').date()
        except:
            pass

    # Fallback to year/month/day
    year = game.get('year')
    month = game.get('month')
    day = game.get('day')
    if year and month and day:
        return date(year, month, day)
    return None


def _process_game_chunk(
    chunk: List[Dict],
    chunk_id: int,
    total_chunks: int,
    team_only: bool,
    players_only: bool,
    dry_run: bool,
    progress_lock: Lock,
    progress: Dict,
    job_id: str = None
) -> Tuple[int, int]:
    """Process a chunk of games in a thread.

    Args:
        chunk: List of game documents to process
        chunk_id: ID of this chunk (for logging)
        total_chunks: Total number of chunks
        team_only: Only process team stats
        players_only: Only process player stats
        dry_run: Don't update database
        progress_lock: Lock for updating shared progress
        progress: Shared progress dict
        job_id: Optional job ID for progress tracking in jobs_nba

    Returns:
        Tuple of (games_processed, players_processed)
    """
    # Note: PyMongo's MongoClient is thread-safe and manages its own connection pool,
    # so process_game can safely use the global db from multiple threads

    chunk_games = 0
    chunk_players = 0
    last_job_update_pct = 0  # Track last job update percentage

    for i, game in enumerate(chunk, 1):
        game_id = game.get('game_id')
        if not game_id:
            continue

        game_date = _parse_game_date(game)
        if not game_date:
            continue

        # Update shared progress
        with progress_lock:
            progress['processed'] += 1
            current = progress['processed']
            total = progress['total']
            current_pct = 100 * current / total if total > 0 else 0

        if current % 100 == 0 or current == total:
            print(f"  [Chunk {chunk_id}/{total_chunks}] Progress: {current}/{total} games ({current_pct:.1f}%)")

        try:
            success, player_count = process_game(game_id, game_date, team_only, players_only, dry_run)
            if success:
                chunk_games += 1
                chunk_players += player_count
        except Exception as e:
            # Don't let a single game crash the entire chunk; record for audit.
            print(f"  ERROR processing game {game_id} in chunk {chunk_id}/{total_chunks}: {e}")
            if job_id:
                _record_espn_sync_failure(job_id, str(game_id), str(e))
            continue

        # Update job progress every ~2.5%
        if job_id and (current_pct - last_job_update_pct >= 2.5 or current == total):
            with progress_lock:
                games_done = progress.get('games', 0) + chunk_games
                players_done = progress.get('players', 0) + chunk_players
            _update_espn_sync_job(job_id, current, total, games_done, players_done)
            last_job_update_pct = current_pct

    return chunk_games, chunk_players


def _create_espn_sync_job(total_games: int, team_only: bool, players_only: bool) -> str:
    """Create a job in jobs_nba for tracking ESPN sync progress."""
    job_doc = {
        'type': 'espn_sync',
        'progress': 0,
        'status': 'running',
        'error': None,
        'message': f'Starting ESPN sync for {total_games} games...',
        'metadata': {
            'total_games': total_games,
            'team_only': team_only,
            'players_only': players_only,
            'games_processed': 0,
            'players_processed': 0,
            # Failure tracking (best-effort; capped list sizes to keep job docs small)
            'failed_games': 0,
            'failed_game_ids': [],
            'failed_game_errors': []
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    result = db.jobs_nba.insert_one(job_doc)
    return str(result.inserted_id)


def _record_espn_sync_failure(job_id: str, game_id: str, error: str):
    """Record a per-game failure to jobs_nba (thread-safe best effort)."""
    from bson import ObjectId
    try:
        # Cap arrays to last N entries to avoid oversized job docs
        MAX_FAILURES_STORED = 200
        db.jobs_nba.update_one(
            {'_id': ObjectId(job_id)},
            {
                '$inc': {'metadata.failed_games': 1},
                '$push': {
                    'metadata.failed_game_ids': {
                        '$each': [str(game_id)],
                        '$slice': -MAX_FAILURES_STORED
                    },
                    'metadata.failed_game_errors': {
                        '$each': [{
                            'game_id': str(game_id),
                            'error': str(error),
                            'at': datetime.now().isoformat()
                        }],
                        '$slice': -MAX_FAILURES_STORED
                    }
                },
                '$set': {'updated_at': datetime.now()}
            }
        )
    except Exception:
        # Never let failure-recording break the sync loop
        pass


def _update_espn_sync_job(job_id: str, processed: int, total: int, games_done: int, players_done: int):
    """Update ESPN sync job progress."""
    from bson import ObjectId
    progress = int(100 * processed / total) if total > 0 else 0
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'progress': progress,
            'message': f'Processed {processed}/{total} games ({progress}%)',
            'metadata.games_processed': games_done,
            'metadata.players_processed': players_done,
            'updated_at': datetime.now()
        }}
    )


def _create_espn_dates_job(total_days: int, team_only: bool, players_only: bool) -> str:
    """Create a job in jobs_nba for tracking ESPN date-range pulls."""
    job_doc = {
        'type': 'espn_dates_sync',
        'progress': 0,
        'status': 'running',
        'error': None,
        'message': f'Starting ESPN date-range sync for {total_days} day(s)...',
        'metadata': {
            'total_days': total_days,
            'team_only': team_only,
            'players_only': players_only,
            'days_processed': 0,
            'games_processed': 0,
            'players_processed': 0,
            'games_skipped_date_mismatch': 0,
            # Failure tracking (same shape as espn_sync)
            'failed_games': 0,
            'failed_game_ids': [],
            'failed_game_errors': []
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    result = db.jobs_nba.insert_one(job_doc)
    return str(result.inserted_id)


def _update_espn_dates_job(job_id: str, processed_days: int, total_days: int, games_done: int, players_done: int, skipped: int):
    """Update ESPN date-range sync job progress."""
    from bson import ObjectId
    progress = int(100 * processed_days / total_days) if total_days > 0 else 0
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'progress': progress,
            'message': f'Processed {processed_days}/{total_days} days ({progress}%)',
            'metadata.days_processed': processed_days,
            'metadata.games_processed': games_done,
            'metadata.players_processed': players_done,
            'metadata.games_skipped_date_mismatch': skipped,
            'updated_at': datetime.now()
        }}
    )


def _complete_espn_dates_job(job_id: str, days_done: int, total_days: int, games_done: int, players_done: int, skipped: int):
    """Mark ESPN date-range sync job as completed (include failures count in message)."""
    from bson import ObjectId
    failed_games = 0
    try:
        doc = db.jobs_nba.find_one({'_id': ObjectId(job_id)}, {'metadata.failed_games': 1})
        failed_games = int(((doc or {}).get('metadata') or {}).get('failed_games') or 0)
    except Exception:
        failed_games = 0
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'completed',
            'progress': 100,
            'message': f'Completed: {days_done}/{total_days} days, {games_done} games ({failed_games} failures)',
            'metadata.days_processed': days_done,
            'metadata.games_processed': games_done,
            'metadata.players_processed': players_done,
            'metadata.games_skipped_date_mismatch': skipped,
            'updated_at': datetime.now()
        }}
    )


def _fail_espn_dates_job(job_id: str, error: str):
    """Mark ESPN date-range sync job as failed."""
    from bson import ObjectId
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'failed',
            'error': error,
            'message': f'Failed: {error}',
            'updated_at': datetime.now()
        }}
    )


def _complete_espn_sync_job(job_id: str, games_done: int, players_done: int):
    """Mark ESPN sync job as completed."""
    from bson import ObjectId
    failed_games = 0
    try:
        doc = db.jobs_nba.find_one({'_id': ObjectId(job_id)}, {'metadata.failed_games': 1})
        failed_games = int(((doc or {}).get('metadata') or {}).get('failed_games') or 0)
    except Exception:
        failed_games = 0
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'completed',
            'progress': 100,
            'message': f'Completed: {games_done} games processed ({failed_games} failures)',
            'metadata.games_processed': games_done,
            'metadata.players_processed': players_done,
            'updated_at': datetime.now()
        }}
    )


def _fail_espn_sync_job(job_id: str, error: str):
    """Mark ESPN sync job as failed."""
    from bson import ObjectId
    db.jobs_nba.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {
            'status': 'failed',
            'error': error,
            'message': f'Failed: {error}',
            'updated_at': datetime.now()
        }}
    )


def fetch_all_games(team_only: bool, players_only: bool, dry_run: bool):
    """Fetch all games from stats_nba collection and refresh them.

    For large batches (2500+ games), uses threading with chunks of 500 games
    to improve throughput. Progress is tracked in jobs_nba collection.
    """
    print("Fetching all game_ids from stats_nba collection...")

    # Get all unique game_ids with their dates
    games = list(db.stats_nba.find(
        {'game_id': {'$exists': True, '$ne': None}},
        {'game_id': 1, 'date': 1, 'year': 1, 'month': 1, 'day': 1}
    ))

    if not games:
        print("  No games found in stats_nba collection")
        return

    total_game_count = len(games)
    print(f"  Found {total_game_count} games in database")

    # Use threading for large batches
    if total_game_count >= THREADING_THRESHOLD:
        print(f"  Using threaded processing ({CHUNK_SIZE} games per chunk)...")

        # Create job for tracking (only for threaded processing)
        job_id = None
        if not dry_run:
            job_id = _create_espn_sync_job(total_game_count, team_only, players_only)
            print(f"  Created job: {job_id}")

        # Split into chunks
        chunks = [games[i:i + CHUNK_SIZE] for i in range(0, total_game_count, CHUNK_SIZE)]
        num_chunks = len(chunks)
        print(f"  Created {num_chunks} chunks")

        # Shared progress tracking
        progress_lock = Lock()
        progress = {'processed': 0, 'total': total_game_count, 'games': 0, 'players': 0}

        total_games = 0
        total_players = 0

        # Use ThreadPoolExecutor
        max_workers = min(MAX_WORKERS, num_chunks)
        print(f"  Starting {max_workers} worker threads...")

        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        _process_game_chunk,
                        chunk,
                        chunk_id + 1,
                        num_chunks,
                        team_only,
                        players_only,
                        dry_run,
                        progress_lock,
                        progress,
                        job_id  # Pass job_id for progress updates
                    ): chunk_id
                    for chunk_id, chunk in enumerate(chunks)
                }

                for future in as_completed(futures):
                    chunk_id = futures[future]
                    try:
                        games_processed, players_processed = future.result()
                        total_games += games_processed
                        total_players += players_processed

                        # Update cumulative totals in shared progress
                        with progress_lock:
                            progress['games'] = total_games
                            progress['players'] = total_players
                    except Exception as e:
                        print(f"  ERROR in chunk {chunk_id + 1}: {e}")

            # Mark job complete
            if job_id:
                _complete_espn_sync_job(job_id, total_games, total_players)

        except Exception as e:
            if job_id:
                _fail_espn_sync_job(job_id, str(e))
            raise

        print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary (threaded):")
        print(f"  Games processed: {total_games}")
        if not team_only:
            print(f"  Player stats processed: {total_players}")
        if job_id:
            print(f"  Job ID: {job_id}")

    else:
        # Sequential processing for smaller batches (no job tracking)
        total_games = 0
        total_players = 0

        for i, game in enumerate(games, 1):
            game_id = game.get('game_id')
            if not game_id:
                continue

            game_date = _parse_game_date(game)
            if not game_date:
                print(f"  Warning: Could not determine date for game {game_id}, skipping")
                continue

            print(f"\n[{i}/{total_game_count}] Processing game {game_id} ({game_date})...")

            success, player_count = process_game(game_id, game_date, team_only, players_only, dry_run)
            if success:
                total_games += 1
                total_players += player_count

        print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
        print(f"  Games processed: {total_games}")
        if not team_only:
            print(f"  Player stats processed: {total_players}")


def update_injured_players_for_all_games(dry_run: bool = False, game_ids: List[str] = None, season: str = None):
    """
    Compute and update injured players for all games in stats_nba.
    
    An injured player is defined as:
    - On the team's roster (player has played for team before and after game date)
    - Did not play in the game (stats.min == 0 or missing)
    - Has at least 1 prior game for this team before the game date
    - Last prior game was within 25 days of the game date
    
    Args:
        dry_run: If True, don't update database
        game_ids: Optional list of specific game IDs to process (for auditing)
        season: Optional season string to filter games (e.g., '2024-2025')
    """
    print("=" * 80)
    print("UPDATE INJURED PLAYERS FOR ALL GAMES")
    print("=" * 80)
    print()
    
    # Step 1: Build precomputed maps from stats_nba_players
    print("Step 1: Building precomputed maps from stats_nba_players...")
    print("  Scanning all player stats...")
    
    player_team_dates = {}  # dict[player_id][team] -> sorted list of dates
    team_players = {}  # dict[team] -> set of player_ids
    game_team_players_played = {}  # dict[(game_id, team)] -> set of player_ids
    player_last_game_info = {}  # dict[player_id] -> {'date': last_date, 'team': team, 'season': season}
    
    # Single scan over stats_nba_players
    player_stats_cursor = db.stats_nba_players.find(
        {'stats.min': {'$gt': 0}},  # Only players who actually played
        {'player_id': 1, 'team': 1, 'date': 1, 'game_id': 1, 'season': 1}
    )
    
    total_player_records = 0
    for player_record in player_stats_cursor:
        total_player_records += 1
        player_id = player_record.get('player_id')
        team = player_record.get('team')
        game_date = player_record.get('date')
        game_id = player_record.get('game_id')
        season = player_record.get('season')
        
        if not player_id or not team or not game_date or not game_id:
            continue
        
        # Build player_team_dates
        if player_id not in player_team_dates:
            player_team_dates[player_id] = {}
        if team not in player_team_dates[player_id]:
            player_team_dates[player_id][team] = []
        
        # Add date if not already present (avoid duplicates)
        if game_date not in player_team_dates[player_id][team]:
            player_team_dates[player_id][team].append(game_date)
        
        # Build team_players
        if team not in team_players:
            team_players[team] = set()
        team_players[team].add(player_id)
        
        # Build game_team_players_played
        key = (game_id, team)
        if key not in game_team_players_played:
            game_team_players_played[key] = set()
        game_team_players_played[key].add(player_id)
        
        # Track last game info for each player (across all teams)
        if player_id not in player_last_game_info:
            player_last_game_info[player_id] = {'date': game_date, 'team': team, 'season': season}
        else:
            # Update if this game is later than the current last game
            current_last_date = player_last_game_info[player_id]['date']
            if game_date > current_last_date:
                player_last_game_info[player_id] = {'date': game_date, 'team': team, 'season': season}
    
    # Sort all date lists
    for player_id in player_team_dates:
        for team in player_team_dates[player_id]:
            player_team_dates[player_id][team].sort()
    
    print(f"  Processed {total_player_records} player records")
    print(f"  Found {len(player_team_dates)} unique players")
    print(f"  Found {len(team_players)} unique teams")
    print(f"  Found {len(game_team_players_played)} game-team combinations")
    print()
    
    # Step 2: Iterate over all games in stats_nba
    print("Step 2: Processing games and computing injured players...")
    
    # Build query
    query = {
        'game_id': {'$exists': True, '$ne': None},
        'homeWon': {'$exists': True},
        'homeTeam.points': {'$exists': True}
    }
    
    # Filter by specific game IDs if provided
    if game_ids:
        query['game_id'] = {'$in': game_ids}
        print(f"  Filtering to {len(game_ids)} specific game IDs: {', '.join(game_ids)}")
    
    # Filter by season if provided
    if season:
        query['season'] = season
        print(f"  Filtering to season: {season}")
    
    games = list(db.stats_nba.find(
        query,
        {'game_id': 1, 'date': 1, 'homeTeam.name': 1, 'awayTeam.name': 1, 'season': 1}
    ))
    
    if not games:
        print("  No games found in stats_nba collection")
        return
    
    print(f"  Found {len(games)} games to process")
    print()
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, game in enumerate(games, 1):
        game_id = game.get('game_id')
        game_date = game.get('date')
        game_season = game.get('season')
        home_team = game.get('homeTeam', {}).get('name')
        away_team = game.get('awayTeam', {}).get('name')
        
        if not game_id or not game_date:
            skipped_count += 1
            continue
        
        if not home_team or not away_team:
            skipped_count += 1
            continue
        
        if i % 100 == 0:
            print(f"  Processing game {i}/{len(games)}...")
        
        try:
            home_injured_players = []
            away_injured_players = []
            
            # Process home team
            roster = set()
            if home_team in team_players:
                for player_id in team_players[home_team]:
                    if player_id in player_team_dates and home_team in player_team_dates[player_id]:
                        dates = player_team_dates[player_id][home_team]
                        if dates:  # Ensure list is not empty
                            first_date = dates[0]
                            last_date = dates[-1]
                            # Inclusive check: game_date between first and last (inclusive)
                            if first_date <= game_date <= last_date:
                                roster.add(player_id)
                            elif first_date <= game_date:
                                # Check if last game played for ANY team was for this team in this season
                                if player_id in player_last_game_info:
                                    last_game_info = player_last_game_info[player_id]
                                    if (last_game_info['team'] == home_team and 
                                        last_game_info['season'] == game_season):
                                        roster.add(player_id)
            
            # Get players who actually played in this game
            played = game_team_players_played.get((game_id, home_team), set())
            
            # Debug output for specific game IDs
            if game_ids and game_id in game_ids:
                print(f"\n  === GAME {game_id} ({away_team} @ {home_team}) ===")
                print(f"  HOME TEAM ({home_team}):")
                print(f"    Roster (players on team on {game_date}): {sorted(list(roster))}")
                print(f"    Played (stats.min > 0): {sorted(list(played))}")
                print(f"    Roster - Played (injured candidates): {sorted(list(roster - played))}")
            
            # Injured candidates = roster - played
            injured_candidates = roster - played
            
            # Filter injured candidates
            for player_id in injured_candidates:
                if player_id not in player_team_dates or home_team not in player_team_dates[player_id]:
                    continue
                
                dates = player_team_dates[player_id][home_team]
                if not dates:
                    continue
                
                # Get all prior game dates (dates < game_date)
                prior_dates = [d for d in dates if d < game_date]
                
                # Check: at least 1 prior game
                if len(prior_dates) == 0:
                    continue
                
                # Check: last prior game within 25 days
                last_prior_date = prior_dates[-1]
                date_diff = (datetime.strptime(game_date, '%Y-%m-%d').date() - 
                           datetime.strptime(last_prior_date, '%Y-%m-%d').date()).days
                
                if date_diff <= 25:
                    home_injured_players.append(player_id)
            
            # Process away team
            roster = set()
            if away_team in team_players:
                for player_id in team_players[away_team]:
                    if player_id in player_team_dates and away_team in player_team_dates[player_id]:
                        dates = player_team_dates[player_id][away_team]
                        if dates:  # Ensure list is not empty
                            first_date = dates[0]
                            last_date = dates[-1]
                            # Inclusive check: game_date between first and last (inclusive)
                            if first_date <= game_date <= last_date:
                                roster.add(player_id)
                            elif first_date <= game_date:
                                # Check if last game played for ANY team was for this team in this season
                                if player_id in player_last_game_info:
                                    last_game_info = player_last_game_info[player_id]
                                    if (last_game_info['team'] == away_team and 
                                        last_game_info['season'] == game_season):
                                        roster.add(player_id)
            
            # Get players who actually played in this game
            played = game_team_players_played.get((game_id, away_team), set())
            
            # Debug output for specific game IDs
            if game_ids and game_id in game_ids:
                print(f"  AWAY TEAM ({away_team}):")
                print(f"    Roster (players on team on {game_date}): {sorted(list(roster))}")
                print(f"    Played (stats.min > 0): {sorted(list(played))}")
                print(f"    Roster - Played (injured candidates): {sorted(list(roster - played))}")
            
            # Injured candidates = roster - played
            injured_candidates = roster - played
            
            # Filter injured candidates
            for player_id in injured_candidates:
                if player_id not in player_team_dates or away_team not in player_team_dates[player_id]:
                    continue
                
                dates = player_team_dates[player_id][away_team]
                if not dates:
                    continue
                
                # Get all prior game dates (dates < game_date)
                prior_dates = [d for d in dates if d < game_date]
                
                # Check: at least 1 prior game
                if len(prior_dates) == 0:
                    continue
                
                # Check: last prior game within 25 days
                last_prior_date = prior_dates[-1]
                date_diff = (datetime.strptime(game_date, '%Y-%m-%d').date() - 
                           datetime.strptime(last_prior_date, '%Y-%m-%d').date()).days
                
                if date_diff <= 25:
                    away_injured_players.append(player_id)
            
            # Debug output: final injured players list
            if game_ids and game_id in game_ids:
                print(f"  FINAL INJURED PLAYERS:")
                print(f"    Home ({home_team}): {sorted(home_injured_players)}")
                print(f"    Away ({away_team}): {sorted(away_injured_players)}")
                print()
            
            # Update game document
            if not dry_run:
                update_doc = {
                    '$set': {
                        'homeTeam.injured_players': home_injured_players,
                        'awayTeam.injured_players': away_injured_players
                    }
                }
                
                result = db.stats_nba.update_one(
                    {'game_id': game_id},
                    update_doc
                )
                
                if result.modified_count > 0:
                    updated_count += 1
            else:
                # Count for dry run
                total_injured = len(home_injured_players) + len(away_injured_players)
                if total_injured > 0:
                    updated_count += 1
        
        except Exception as e:
            print(f"  ERROR processing game {game_id}: {e}")
            error_count += 1
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'[DRY RUN] ' if dry_run else ''}Games processed: {len(games)}")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print()


def fetch_dates(dates: List[date], team_only: bool, players_only: bool, dry_run: bool):
    """Fetch games and players for a list of dates.

    Uses the simpler NBA-specific scoreboard API and validates that each event's
    date (converted from UTC to Eastern) matches the requested date.
    """
    total_games = 0
    total_players = 0
    total_skipped = 0
    latest_date = None

    # Threading for very large date ranges
    use_threading = len(dates) > 500
    job_id = None
    if use_threading:
        print(f"Date range has {len(dates)} days; using threaded processing (50-day chunks, up to 10 workers).")
        if not dry_run:
            job_id = _create_espn_dates_job(len(dates), team_only, players_only)
            print(f"  Created job: {job_id}")

    # Shared progress for threaded mode
    progress_lock = Lock()
    progress = {'days_processed': 0, 'total_days': len(dates), 'games': 0, 'players': 0, 'skipped': 0}

    def process_one_date(game_date: date) -> Tuple[int, int, int, Optional[date]]:
        """Process one date. Returns (games, players, skipped, latest_date)."""
        nonlocal latest_date
        print(f"\nFetching games for {game_date}...")

        date_formatted = game_date.strftime('%Y%m%d')
        url = _ACTIVE_LEAGUE.espn_endpoint("scoreboard_site_template").format(YYYYMMDD=date_formatted)

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            scoreboard = response.json()
        except Exception as e:
            print(f"  Error fetching scoreboard for {game_date}: {e}")
            return 0, 0, 0, None

        events = scoreboard.get('events', [])
        if not events:
            print(f"  No games found for {game_date}")
            return 0, 0, 0, None

        print(f"  Found {len(events)} events from API")

        skipped_this_date = 0
        processed_this_date = 0
        players_this_date = 0

        for event in events:
            game_id = event.get('id')
            if not game_id:
                continue

            event_date_str = event.get('date', '')
            short_name = event.get('shortName', game_id)

            if event_date_str:
                event_dt = parse_espn_utc_to_eastern(event_date_str)
                if event_dt:
                    event_date = event_dt.date()
                    if event_date != game_date:
                        print(f"    Skipping {short_name}: date mismatch (UTC: {event_date_str[:10]} -> ET: {event_date}, requested: {game_date})")
                        skipped_this_date += 1
                        continue
                else:
                    print(f"    Skipping {short_name}: could not parse date {event_date_str}")
                    skipped_this_date += 1
                    continue

            try:
                success, player_count = process_game(game_id, game_date, team_only, players_only, dry_run, event=event)
            except Exception as e:
                print(f"  ERROR processing game {game_id} on {game_date}: {e}")
                if job_id:
                    _record_espn_sync_failure(job_id, str(game_id), str(e))
                continue

            if success:
                processed_this_date += 1
                players_this_date += player_count

        print(f"  Processed: {processed_this_date}, Skipped (wrong date): {skipped_this_date}")
        return processed_this_date, players_this_date, skipped_this_date, game_date

    if use_threading:
        # Chunk into 50-day chunks
        chunks = [dates[i:i + 50] for i in range(0, len(dates), 50)]
        num_chunks = len(chunks)
        max_workers = min(10, num_chunks)

        def process_chunk(chunk_dates: List[date], chunk_idx: int) -> Tuple[int, int, int]:
            chunk_games = 0
            chunk_players = 0
            chunk_skipped = 0
            for d in chunk_dates:
                g, p, s, last_d = process_one_date(d)
                chunk_games += g
                chunk_players += p
                chunk_skipped += s

                with progress_lock:
                    progress['days_processed'] += 1
                    progress['games'] += g
                    progress['players'] += p
                    progress['skipped'] += s
                    days_done = progress['days_processed']
                    total_days = progress['total_days']

                # Update job progress every ~2.5% or at end
                if job_id and (days_done % 25 == 0 or days_done == total_days):
                    _update_espn_dates_job(
                        job_id,
                        processed_days=days_done,
                        total_days=total_days,
                        games_done=progress['games'],
                        players_done=progress['players'],
                        skipped=progress['skipped'],
                    )
            return chunk_games, chunk_players, chunk_skipped

        print(f"  Created {num_chunks} chunks; starting {max_workers} worker threads…")
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(process_chunk, chunk_dates, idx + 1): idx
                    for idx, chunk_dates in enumerate(chunks)
                }
                for future in as_completed(futures):
                    try:
                        g, p, s = future.result()
                        total_games += g
                        total_players += p
                        total_skipped += s
                    except Exception as e:
                        print(f"  ERROR in date-chunk {futures[future] + 1}: {e}")

            if job_id:
                with progress_lock:
                    _complete_espn_dates_job(
                        job_id,
                        days_done=progress['days_processed'],
                        total_days=progress['total_days'],
                        games_done=progress['games'],
                        players_done=progress['players'],
                        skipped=progress['skipped'],
                    )
        except Exception as e:
            if job_id:
                _fail_espn_dates_job(job_id, str(e))
            raise

    else:
        for game_date in dates:
            g, p, s, last_d = process_one_date(game_date)
            total_games += g
            total_players += p
            total_skipped += s
            if last_d and (latest_date is None or last_d > latest_date):
                latest_date = last_d

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Games processed: {total_games}")
    print(f"  Games skipped (date mismatch): {total_skipped}")
    if not team_only:
        print(f"  Player stats processed: {total_players}")


def main():
    parser = argparse.ArgumentParser(
        description='ESPN NBA API Data Fetcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python espn_api.py                              # Fetch yesterday's games + players
  python espn_api.py --dates 20210930,20230614   # Fetch date range
  python espn_api.py --team-only                  # Only team stats
  python espn_api.py --players-only               # Only player stats
  python espn_api.py --no-update-master           # Fetch games without updating master training data
  python espn_api.py --refresh-players            # Upsert players_nba metadata
  python espn_api.py --refresh-venues              # Refresh venue locations from nba_venues.json
  python espn_api.py --audit-venues                # Find and remove duplicate venue_guid values
  python espn_api.py --update-venue-locations      # Geocode venues without location field
  python espn_api.py --dry-run                    # Don't update, just print
  python espn_api.py --all                       # Process all games from stats_nba
        """
    )

    parser.add_argument(
        '--league',
        type=str,
        default=os.environ.get("LEAGUE_ID", "nba"),
        help='League id to use (e.g., nba, cbb). Defaults to LEAGUE_ID env var or "nba".'
    )
    
    parser.add_argument(
        '--dates', '-d',
        type=str,
        help='Comma-separated date range in YYYYMMDD format (e.g., "20210930,20230614"). Default: yesterday'
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
        '--refresh-players',
        action='store_true',
        help='Upsert players_nba metadata from stats_nba_players'
    )
    
    parser.add_argument(
        '--refresh-venues',
        action='store_true',
        help='Refresh nba_venues collection with location data from nba_venues.json'
    )
    
    parser.add_argument(
        '--audit-venues',
        action='store_true',
        help='Find and remove duplicate venue_guid values in nba_venues collection'
    )
    
    parser.add_argument(
        '--update-venue-locations',
        action='store_true',
        help='Update venues in nba_venues collection that don\'t have a location field using Nominatim geocoding'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Don\'t update database, just print what would be updated'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all game_ids from stats_nba collection and refresh them'
    )
    
    parser.add_argument(
        '--player-injuries',
        action='store_true',
        help='Compute and update injured players for all games based on roster vs played analysis'
    )
    
    parser.add_argument(
        '--game-ids',
        type=str,
        help='Comma-separated list of game IDs to process (use with --player-injuries for auditing)'
    )
    
    parser.add_argument(
        '--season',
        type=str,
        help='Season string to filter games (e.g., "2024-2025"). Use with --player-injuries to process only games from that season.'
    )
    
    
    args = parser.parse_args()

    # Activate league (impacts endpoints + DB collections)
    global _ACTIVE_LEAGUE, db
    _ACTIVE_LEAGUE = _get_league(args.league)
    db = LeagueDbProxy(_raw_db, _ACTIVE_LEAGUE)
    
    # Handle refresh-players separately
    if args.refresh_players:
        refresh_players_metadata(dry_run=args.dry_run)
        return
    
    # Handle refresh-venues separately
    if args.refresh_venues:
        refresh_venues_location(dry_run=args.dry_run)
        return
    
    # Handle audit-venues separately
    if args.audit_venues:
        audit_venues(dry_run=args.dry_run)
        return
    
    # Handle update-venue-locations separately
    if args.update_venue_locations:
        update_venue_locations(dry_run=args.dry_run)
        return
    
    # Validate flags
    if args.team_only and args.players_only:
        print("Error: Cannot use --team-only and --players-only together")
        return
    
    # Handle --player-injuries flag
    if args.player_injuries:
        game_ids = None
        if args.game_ids:
            # Parse comma-separated game IDs
            game_ids = [gid.strip() for gid in args.game_ids.split(',') if gid.strip()]
            print(f"Processing {len(game_ids)} specific game IDs: {', '.join(game_ids)}")
        season = args.season
        update_injured_players_for_all_games(args.dry_run, game_ids=game_ids, season=season)
        return
    
    # Handle --all flag
    if args.all:
        fetch_all_games(args.team_only, args.players_only, args.dry_run)
        return
    
    # Determine dates to fetch
    if args.dates:
        try:
            dates = parse_date_range(args.dates)
        except ValueError as e:
            print(f"Error: {e}")
            return
    else:
        # Default: yesterday
        dates = [date.today() - timedelta(days=1)]
    
    # Fetch data (master training updates are now handled separately via generate_master_training.py)
    fetch_dates(dates, args.team_only, args.players_only, args.dry_run)


if __name__ == '__main__':
    main()
