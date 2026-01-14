"""
StatHandlerV2.py - Enhanced stat handler with exponential weighting and absolute values

Improvements over StatHandler:
- Exponential decay weighting for historical averages
- Option to return absolute values alongside differentials
- Cleaner interface for rest/fatigue calculations
- Pace and volatility features
- Games played so far (reliability signal)
- Era normalization support
"""

import math
import numpy as np
from datetime import date, datetime, timedelta
from collections import defaultdict
from nba_app.cli.collection_to_dict import import_collection
from nba_app.cli.db_query_funcs import (
    getTeamSeasonGamesFromDate,
    getTeamLastNMonthsSeasonGames,
    getTeamLastNDaysSeasonGames
)
from nba_app.cli.Mongo import Mongo
from nba_app.cli.feature_name_parser import parse_feature_name


class StatHandlerV2:
    """
    Enhanced stat handler with exponential weighting and absolute value support.
    """
    
    def __init__(
        self,
        statistics: list,
        include_absolute: bool = False,
        use_exponential_weighting: bool = False,
        exponential_lambda: float = 0.1,
        preloaded_games: list = None,
        league_averages: dict = None,
        db = None,
        lazy_load: bool = False
    ):
        """
        Initialize StatHandlerV2.
        
        Args:
            statistics: List of stat tokens to compute
            include_absolute: If True, return absolute values alongside diffs for key stats
            use_exponential_weighting: If True, apply exponential decay to averages
            exponential_lambda: Decay rate for exponential weighting
            preloaded_games: Optional preloaded game data to avoid redundant DB calls
            league_averages: Optional dict of {season: {stat: value}} for era normalization
            db: Optional MongoDB database connection for venue lookups
            lazy_load: If True and preloaded_games is None, skip loading all games upfront.
                      Games will be queried on-demand from DB as needed (for prediction use cases).
                      If False, loads all games upfront (for training use cases).
        """
        self.statistics = statistics
        self.include_absolute = include_absolute
        self.use_exponential_weighting = use_exponential_weighting
        self.exponential_lambda = exponential_lambda
        self.league_averages = league_averages or {}
        self.db = db
        self.lazy_load = lazy_load
        self._venue_cache = {}  # Cache venue locations to avoid repeated DB queries
        
        # Injury feature caches (preloaded to avoid per-game DB queries)
        self._injury_player_stats_cache = {}  # dict[(team, season, date_str)] -> dict[player_id] -> stats
        self._injury_max_mpg_cache = {}  # dict[(team, season, date_str)] -> float
        self._injury_rotation_mpg_cache = {}  # dict[(team, season, date_str)] -> float
        self._injury_preloaded_players = {}  # dict[(team, season)] -> list of player records
        self._injury_cache_loaded = False
        
        # Cache for get_team_games_before_date to avoid repeated iterations
        self._team_games_cache = {}  # dict[(team, season, date_str)] -> list of games
        
        # Load all games into memory (or use preloaded data, or skip for lazy loading)
        if preloaded_games is not None:
            self.all_games = preloaded_games
            self.games_home = self.all_games[0]
            self.games_away = self.all_games[1]
        elif lazy_load:
            # Don't load all games upfront - will query on-demand
            self.all_games = None
            self.games_home = None
            self.games_away = None
        else:
            # Default behavior: load all games
            self.all_games = import_collection('stats_nba')
            self.games_home = self.all_games[0]
            self.games_away = self.all_games[1]
    
    def avg(self, ls: list) -> float:
        """Simple average."""
        return sum(ls) / float(len(ls)) if ls else 0
    
    def std(self, ls: list) -> float:
        """Standard deviation."""
        if len(ls) < 2:
            return 0
        mean = self.avg(ls)
        variance = sum((x - mean) ** 2 for x in ls) / float(len(ls) - 1)
        return math.sqrt(variance)
    
    def preload_venue_cache(self):
        """Preload all venue locations into memory cache."""
        if self.db is None:
            return
        
        venues = list(self.db.nba_venues.find(
            {},
            {'venue_guid': 1, 'location.lat': 1, 'location.lon': 1, 'location.long': 1}
        ))
        
        for venue in venues:
            venue_guid = venue.get('venue_guid')
            location = venue.get('location', {})
            if venue_guid and location:
                lat = location.get('lat')
                # Support both 'lon' and 'long' keys from DB
                lon = location.get('lon') if 'lon' in location else location.get('long')
                if lat is not None and lon is not None:
                    self._venue_cache[venue_guid] = (lat, lon)
        
        print(f"Preloaded {len(self._venue_cache)} venue locations into cache")
    
    def preload_injury_cache(self, games: list = None):
        """
        Preload player stats for injury feature calculations to avoid per-game DB queries.
        
        Args:
            games: Optional list of game documents. If None, will query all games from DB.
                  Should include 'homeTeam.name', 'awayTeam.name', 'season', 'date' fields.
        """
        if self.db is None:
            return
        
        if games is None:
            # Query all games from DB
            games = list(self.db.stats_nba.find(
                {'homeTeam.points': {'$exists': True, '$gt': 0}},
                {'homeTeam.name': 1, 'awayTeam.name': 1, 'season': 1, 'date': 1}
            ))
        
        # Extract all unique (team, season) combinations
        team_seasons = set()
        for game in games:
            home_team = game.get('homeTeam', {}).get('name')
            away_team = game.get('awayTeam', {}).get('name')
            season = game.get('season')
            if home_team and season:
                team_seasons.add((home_team, season))
            if away_team and season:
                team_seasons.add((away_team, season))
        
        print(f"Preloading injury cache for {len(team_seasons)} team-season combinations...")
        
        # Load all player records for these teams/seasons
        for team, season in team_seasons:
            player_records = list(self.db.stats_nba_players.find(
                {
                    'team': team,
                    'season': season,
                    'stats.min': {'$gt': 0}  # Only games where player actually played
                },
                {
                    'player_id': 1,
                    'team': 1,
                    'season': 1,
                    'date': 1,
                    'stats.min': 1
                }
            ).sort('date', 1))
            
            self._injury_preloaded_players[(team, season)] = player_records
        
        total_records = sum(len(records) for records in self._injury_preloaded_players.values())
        print(f"  Preloaded {total_records} player records for {len(team_seasons)} team-seasons")
        self._injury_cache_loaded = True
    
    def _get_venue_location(self, venue_guid: str) -> tuple:
        """
        Get venue location (lat, lon) from cache or database.
        
        Returns:
            Tuple of (lat, lon) or (None, None) if not found
        """
        
        # Check cache first
        if venue_guid in self._venue_cache:
            return self._venue_cache[venue_guid]
        
        # If no DB connection, return None
        if self.db is None:
            return None, None
        
        # Query database (fallback if not preloaded)
        venue = self.db.nba_venues.find_one(
            {'venue_guid': venue_guid},
            {'location.lat': 1, 'location.lon': 1, 'location.long': 1}
        )
        
        if venue and venue.get('location'):
            lat = venue['location'].get('lat')
            # Support both 'lon' and 'long'
            lon = venue['location'].get('lon') if 'lon' in venue['location'] else venue['location'].get('long')
            self._venue_cache[venue_guid] = (lat, lon)
            return lat, lon
        
        # Cache None to avoid repeated queries
        self._venue_cache[venue_guid] = (None, None)
        return None, None
    
    def _calculate_travel_distance(self, team: str, year: int, month: int, day: int, 
                                   season: str, n_days: int) -> float:
        """
        Calculate total travel distance for a team over the last n_days.
        
        Uses haversine formula to compute distance between venues.
        Uses cached games_home/games_away to avoid DB queries.
        """
        import logging
        logger = logging.getLogger(__name__)
        if self.db is None:
            logger.debug(f"[TRAVEL] DB is None, returning 0.0 for travel distance ({team}, last {n_days} days)")
            return 0.0
        
        target_date = date(year, month, day)
        start_date = target_date - timedelta(days=n_days)
        
        # Get games in the date range - use helper method if lazy loading, otherwise use preloaded structure
        if self.games_home is None or self.games_away is None:
            # Lazy loading: use _get_team_games_last_n_days helper
            all_team_games = self._get_team_games_last_n_days(team, year, month, day, season, n_days)
            games = [g for g in all_team_games if g.get('game_type', 'regseason') != 'preseason']
        else:
            # Use preloaded data structure
            games = []
            if season in self.games_home:
                for date_str, teams_dict in self.games_home[season].items():
                    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if game_date < start_date or game_date >= target_date:
                        continue
                    
                    for team_name, game in teams_dict.items():
                        if team_name == team:
                            game_type = game.get('game_type', 'regseason')
                            if game_type != 'preseason':
                                games.append(game)
            
            if season in self.games_away:
                for date_str, teams_dict in self.games_away[season].items():
                    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if game_date < start_date or game_date >= target_date:
                        continue
                    
                    for team_name, game in teams_dict.items():
                        if team_name == team:
                            game_type = game.get('game_type', 'regseason')
                            if game_type != 'preseason':
                                games.append(game)
            
            # Sort by date
            games.sort(key=lambda g: g.get('date', ''))
        
        if not games:
            logger.debug(f"[TRAVEL] No games for {team} in last {n_days} days before {year}-{month:02d}-{day:02d} ({season})")
            return 0.0
        
        total_distance = 0.0
        prev_venue_guid = None
        prev_lat = None
        prev_lon = None
        games_with_guid = 0
        games_with_coords = 0
        
        for game in games:
            # Try multiple possible keys for venue identifier
            current_venue_guid = (
                game.get('venue_guid') or
                game.get('venueGuid') or
                game.get('arena_guid') or
                game.get('arenaId') or
                (game.get('venue') or {}).get('venue_guid') or
                (game.get('venue') or {}).get('guid')
            )
            if not current_venue_guid:
                logger.debug(f"[TRAVEL] Missing venue id for game {game.get('game_id')} on {game.get('date')} for {team}. Available keys: {list(game.keys())}")
                continue
            games_with_guid += 1
            
            # Get venue location
            lat, lon = self._get_venue_location(current_venue_guid)
            
            if lat is None or lon is None:
                logger.debug(f"[TRAVEL] No coords for venue {current_venue_guid} (team={team})")
                continue
            games_with_coords += 1
            
            # If we have a previous venue, calculate distance
            if prev_venue_guid and prev_lat is not None and prev_lon is not None:
                # Only calculate distance if it's a different venue
                if current_venue_guid != prev_venue_guid:
                    distance = self._haversine_distance(prev_lat, prev_lon, lat, lon)
                    total_distance += distance
            
            # Update previous venue
            prev_venue_guid = current_venue_guid
            prev_lat = lat
            prev_lon = lon
        
        logger.debug(f"[TRAVEL] {team} last{n_days}: games={len(games)}, with_guid={games_with_guid}, with_coords={games_with_coords}, total_miles={total_distance:.1f}")
        return total_distance
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth.
        
        Returns distance in miles.
        """
        # Earth radius in miles
        R = 3958.8
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def weighted_avg(self, values: list, dates: list, reference_date: date) -> float:
        """
        Compute exponentially weighted average.
        
        Args:
            values: List of stat values
            dates: List of game dates (as strings 'YYYY-MM-DD')
            reference_date: The matchup date
            
        Returns:
            Weighted average with more recent games weighted higher
        
        Uses exponential decay: weight = exp(-lambda * days_ago)
        """
        if not values or not dates or len(values) != len(dates):
            return 0.0
        
        if not self.use_exponential_weighting:
            return self.avg(values)
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for val, date_str in zip(values, dates):
            try:
                game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                days_ago = (reference_date - game_date).days
                
                if days_ago < 0:
                    continue  # Skip future dates
                
                weight = math.exp(-self.exponential_lambda * days_ago)
                total_weighted += val * weight
                total_weight += weight
            except (ValueError, TypeError):
                continue
        
        return total_weighted / total_weight if total_weight > 0 else 0.0
    
    def get_team_games_before_date(self, team: str, year: int, month: int, day: int, season: str) -> list:
        """
        Get all regular season games for a team before a given date.
        
        Returns:
            List of game documents sorted by date
        """
        # Use cache to avoid repeated iterations
        date_str = f"{year}-{month:02d}-{day:02d}"
        cache_key = (team, season, date_str)
        
        if cache_key in self._team_games_cache:
            return self._team_games_cache[cache_key]
        
        target_date = date(year, month, day)
        games = []
        
        # If using lazy loading and games aren't preloaded, query from DB
        if self.games_home is None or self.games_away is None:
            if self.db is None:
                raise ValueError("DB connection required for lazy loading. Provide db parameter to StatHandlerV2.")
            
            # Query games for this team and season before the target date
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            query = {
                'season': season,
                'date': {'$lt': target_date_str},
                'game_type': {'$nin': ['preseason', 'allstar']},
                '$or': [
                    {'homeTeam.name': team},
                    {'awayTeam.name': team}
                ],
                'homeTeam.points': {'$exists': True, '$gt': 0},
                'awayTeam.points': {'$exists': True, '$gt': 0}
            }
            
            # Query all fields - we need stat fields from homeTeam/awayTeam which are nested
            # For predictions, we're only querying ~100-200 games, so this is fine
            db_games = list(self.db.stats_nba.find(query).sort('date', 1))
            
            # Log when query returns 0 games (only first occurrence per team/season/date to diagnose "no games" issue)
            if len(db_games) == 0:
                if not hasattr(self, '_debug_logged_queries'):
                    self._debug_logged_queries = set()
                cache_key = (team, season, target_date_str)
                if cache_key not in self._debug_logged_queries:
                    self._debug_logged_queries.add(cache_key)
                    # Check if games exist for this team/season (without date filter)
                    test_query = {
                        'season': season,
                        '$or': [{'homeTeam.name': team}, {'awayTeam.name': team}],
                        'homeTeam.points': {'$exists': True, '$gt': 0}
                    }
                    sample_games = list(self.db.stats_nba.find(test_query).limit(3))
                    import logging
                    if sample_games:
                        sample_dates = [g.get('date') for g in sample_games]
                        logging.warning(
                            f"get_team_games_before_date: 0 games for {team} in {season} before {target_date_str}. "
                            f"Found {len(sample_games)} games in season (dates: {sample_dates})"
                        )
                    else:
                        logging.warning(
                            f"get_team_games_before_date: 0 games for {team} in {season}. "
                            f"No games found for this team/season combination."
                        )
            
            # Convert to format matching preloaded structure (add _id as string)
            # Validate that games have the necessary structure
            for game in db_games:
                game['_id'] = str(game['_id'])
                # Verify game has the required structure
                if 'homeTeam' in game and 'awayTeam' in game and 'date' in game:
                    games.append(game)
        else:
            # Use preloaded data structure
            if season in self.games_home:
                for date_str, teams_dict in self.games_home[season].items():
                    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if game_date >= target_date:
                        continue
                    
                    for team_name, game in teams_dict.items():
                        if team_name == team:
                            game_type = game.get('game_type', 'regseason')
                            if game_type != 'preseason' and game.get('season') == season:
                                games.append(game)
            
            if season in self.games_away:
                for date_str, teams_dict in self.games_away[season].items():
                    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if game_date >= target_date:
                        continue
                    
                    for team_name, game in teams_dict.items():
                        if team_name == team:
                            game_type = game.get('game_type', 'regseason')
                            if game_type != 'preseason' and game.get('season') == season:
                                games.append(game)
        
        # Sort by date
        games.sort(key=lambda g: g['date'])
        
        # Cache the result
        self._team_games_cache[cache_key] = games
        return games
    
    def _get_team_games_last_n_months(self, team: str, year: int, month: int, day: int, season: str, n_months: int) -> list:
        """
        Get team games in the last N months (for lazy loading compatibility).
        
        Returns list of games sorted by date.
        """
        if self.games_home is None or self.games_away is None:
            # Query from DB
            if self.db is None:
                raise ValueError("DB connection required for lazy loading.")
            
            from dateutil import relativedelta
            from datetime import datetime as dt
            target_date = dt(year, month, day).date()
            begin_date = target_date - relativedelta.relativedelta(months=n_months)
            
            query = {
                'season': season,
                'date': {'$gte': begin_date.strftime('%Y-%m-%d'), '$lt': target_date.strftime('%Y-%m-%d')},
                'game_type': {'$nin': ['preseason', 'allstar']},
                '$or': [
                    {'homeTeam.name': team},
                    {'awayTeam.name': team}
                ]
            }
            
            # Query all fields - we need stat fields from homeTeam/awayTeam
            games = list(self.db.stats_nba.find(query).sort('date', 1))
            for game in games:
                game['_id'] = str(game['_id'])
            return games
        else:
            # Use preloaded data via existing function
            from nba_app.cli.db_query_funcs import getTeamLastNMonthsSeasonGames
            return getTeamLastNMonthsSeasonGames(team, year, month, day, season, n_months, self.all_games)
    
    def _get_team_games_last_n_days(self, team: str, year: int, month: int, day: int, season: str, n_days: int) -> list:
        """
        Get team games in the last N days (for lazy loading compatibility).
        
        Returns list of games sorted by date.
        """
        if self.games_home is None or self.games_away is None:
            # Query from DB
            if self.db is None:
                raise ValueError("DB connection required for lazy loading.")
            
            from datetime import timedelta
            from datetime import datetime as dt
            target_date = dt(year, month, day).date()
            begin_date = target_date - timedelta(days=n_days)
            
            query = {
                'season': season,
                'date': {'$gte': begin_date.strftime('%Y-%m-%d'), '$lt': target_date.strftime('%Y-%m-%d')},
                'game_type': {'$nin': ['preseason', 'allstar']},
                '$or': [
                    {'homeTeam.name': team},
                    {'awayTeam.name': team}
                ]
            }
            
            # Query all fields - we need stat fields from homeTeam/awayTeam
            games = list(self.db.stats_nba.find(query).sort('date', 1))
            for game in games:
                game['_id'] = str(game['_id'])
            return games
        else:
            # Use preloaded data via existing function
            from nba_app.cli.db_query_funcs import getTeamLastNDaysSeasonGames
            return getTeamLastNDaysSeasonGames(team, year, month, day, season, n_days, self.all_games)
    
    def get_schedule_context(self, team: str, year: int, month: int, day: int, season: str) -> dict:
        """
        Compute schedule-related features for a team.
        
        Returns:
            Dict with games_last_3_days, games_last_5_days, is_b2b
        """
        target_date = date(year, month, day)
        games = self.get_team_games_before_date(team, year, month, day, season)
        
        games_last_3_days = 0
        games_last_5_days = 0
        is_b2b = False
        
        # Check last few games
        recent_games = [g for g in games if 
                       (target_date - datetime.strptime(g['date'], '%Y-%m-%d').date()).days <= 5]
        
        if recent_games:
            last_game_date = datetime.strptime(recent_games[-1]['date'], '%Y-%m-%d').date()
            days_since_last = (target_date - last_game_date).days
            
            # Check for back-to-back
            if days_since_last == 1:
                is_b2b = True
            
            # Count games in last 3 and 5 days
            for game in recent_games:
                game_date = datetime.strptime(game['date'], '%Y-%m-%d').date()
                days_ago = (target_date - game_date).days
                if days_ago <= 3:
                    games_last_3_days += 1
                if days_ago <= 5:
                    games_last_5_days += 1
        
        return {
            'games_last_3_days': games_last_3_days,
            'games_last_5_days': games_last_5_days,
            'is_b2b': is_b2b
        }
    
    def get_games_played_so_far(self, team: str, year: int, month: int, day: int, season: str) -> int:
        """Get the number of regular season games played by a team before a given date."""
        games = self.get_team_games_before_date(team, year, month, day, season)
        return len(games)
    
    def getStatAvgDiffs(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int = None,
        month: int = None,
        day: int = None,
        point_regression: bool = False,
        include_absolute: bool = False,
        is_key_stat_func: callable = None,
        calc_weight_map: dict = None
    ):
        """
        Compute stat differentials for a matchup.
        
        Args:
            HOME: Home team name
            AWAY: Away team name
            season: NBA season string
            year, month, day: Game date
            point_regression: If True, return per-team features instead of diffs
            Note: Enhanced features (pace, volatility, schedule) are always included (team-level only)
            calc_weight_map: Optional dict mapping stat_token -> 'raw' or 'avg'.
                           If provided, maps stat tokens (e.g., 'effective_fg_percSznAvg') to calc_weight.
                           This will be converted to base_stat_name -> calc_weight for _get_all_stats_batch.
            
        Returns:
            List of feature values, or 'SOME BS' if insufficient data
        """
        stats = []
        szn_home_games = None
        szn_away_games = None
        reference_date = date(year, month, day)
        
        # Cache for games used for volatility/pace
        home_games_10 = None
        away_games_10 = None
        
        # Build calc_weight_map from stat_token to base_stat_name
        # calc_weight_map maps stat_token -> calc_weight, we need base_stat_name -> calc_weight
        base_stat_calc_weight_map = {}
        if calc_weight_map:
            for stat_idx, stat in enumerate(self.statistics):
                if stat in calc_weight_map:
                    # Parse stat token to get base_stat_name
                    normalized = 'Normalized' in stat
                    stat_clean = stat.replace('Normalized', '')
                    stat_clean_no_szn = stat_clean.replace('SznAvg', '')
                    stat_clean_no_side = stat_clean_no_szn.replace('_side', '')
                    months = 'Months_' in stat_clean_no_side
                    stat_days = 'Days_' in stat_clean_no_side
                    stat_games = 'Games_' in stat_clean_no_side
                    
                    # Extract base stat name
                    base_stat_name = stat_clean_no_side
                    if months:
                        base_stat_name = stat_clean_no_side.split('Months_')[0]
                    elif stat_days:
                        base_stat_name = stat_clean_no_side.split('Days_')[0]
                    elif stat_games:
                        base_stat_name = stat_clean_no_side.split('Games_')[0]
                    
                    base_stat_calc_weight_map[base_stat_name] = calc_weight_map[stat]
        
        # Group stats by game window to batch compute them
        # This avoids iterating through games multiple times for stats that share the same window
        # Store results in a dict to maintain original order
        stat_results = {}  # stat -> (home_val, away_val)
        stats_by_window = {}  # (window_type, window_param) -> list of (stat_idx, stat, stat_clean, side_stat)
        
        for stat_idx, stat in enumerate(self.statistics):
            # Parse stat token
            normalized = 'Normalized' in stat
            stat_clean = stat.replace('Normalized', '')
            season_avg = 'SznAvg' in stat_clean
            stat_clean_no_szn = stat_clean.replace('SznAvg', '')
            side_stat = '_side' in stat_clean_no_szn
            stat_clean_no_side = stat_clean_no_szn.replace('_side', '')
            months = 'Months_' in stat_clean_no_side
            stat_days = 'Days_' in stat_clean_no_side
            stat_games = 'Games_' in stat_clean_no_side
            
            # Extract base stat name by removing window suffixes
            # e.g., "pointsMonths_1" -> "points", "effective_fg_percGames_10" -> "effective_fg_perc"
            base_stat_name = stat_clean_no_side
            if months:
                # Remove "Months_X" suffix
                base_stat_name = stat_clean_no_side.split('Months_')[0]
            elif stat_days:
                # Remove "Days_X" suffix
                base_stat_name = stat_clean_no_side.split('Days_')[0]
            elif stat_games:
                # Remove "Games_X" suffix
                base_stat_name = stat_clean_no_side.split('Games_')[0]
            # If no window suffix, base_stat_name is already correct
            
            # Determine window type and parameter
            if season_avg or (not months and not stat_days and not stat_games):
                window_key = ('season', None)
            elif months:
                months_num = int(stat_clean_no_side.split('Months_')[1].split('_')[0])
                window_key = ('months', months_num)
            elif stat_days:
                days_num = int(stat_clean_no_side.split('Days_')[1].split('_')[0])
                window_key = ('days', days_num)
            elif stat_games:
                games_num = int(stat_clean_no_side.split('Games_')[1].split('_')[0])
                window_key = ('games', games_num)
                # Cache for enhanced features
                if games_num == 10:
                    if home_games_10 is None:
                        szn_home = self.get_team_games_before_date(HOME, year, month, day, season)
                        szn_away = self.get_team_games_before_date(AWAY, year, month, day, season)
                        home_games_10 = szn_home[-10:] if len(szn_home) >= 10 else szn_home
                        away_games_10 = szn_away[-10:] if len(szn_away) >= 10 else szn_away
            else:
                window_key = ('season', None)
            
            if window_key not in stats_by_window:
                stats_by_window[window_key] = []
            # Store base_stat_name instead of stat_clean_final so database lookup uses correct field name
            stats_by_window[window_key].append((stat_idx, stat, base_stat_name, side_stat))
        
        # Get season games once if needed
        if ('season', None) in stats_by_window and szn_home_games is None:
            szn_home_games = self.get_team_games_before_date(HOME, year, month, day, season)
            szn_away_games = self.get_team_games_before_date(AWAY, year, month, day, season)
        
        # Process each window group
        for window_key, stat_list in stats_by_window.items():
            window_type, window_param = window_key
            
            # Get games for this window
            if window_type == 'season':
                home_games = szn_home_games
                away_games = szn_away_games
            elif window_type == 'months':
                home_games = self._get_team_games_last_n_months(HOME, year, month, day, season, window_param)
                away_games = self._get_team_games_last_n_months(AWAY, year, month, day, season, window_param)
            elif window_type == 'days':
                home_games = self._get_team_games_last_n_days(HOME, year, month, day, season, window_param)
                away_games = self._get_team_games_last_n_days(AWAY, year, month, day, season, window_param)
            elif window_type == 'games':
                home_games = self.get_team_games_before_date(HOME, year, month, day, season)[-window_param:]
                away_games = self.get_team_games_before_date(AWAY, year, month, day, season)[-window_param:]
            
            if not home_games or not away_games:
                # Log why games are missing (only if not in October or November to avoid spam at season start)
                import logging
                logger = logging.getLogger(__name__)
                window_type_str = f"{window_type}({window_param})" if window_param else window_type
                # Only log warning if not in October (month 10) or November (month 11) to avoid spam at beginning of season
                if month not in [10, 11]:
                    if not home_games:
                        logger.warning(f"[FEAT] No {window_type_str} games found for {HOME} before {year}-{month:02d}-{day:02d} (season {season})")
                    if not away_games:
                        logger.warning(f"[FEAT] No {window_type_str} games found for {AWAY} before {year}-{month:02d}-{day:02d} (season {season})")
                # Fill with zeros for all stats in this window
                for stat_idx, stat_name, _, _ in stat_list:
                    stat_results[stat_idx] = (0.0, 0.0)
                    logger.debug(f"[FEAT] Set {stat_name} to 0.0 due to missing {window_type_str} games")
                continue
            
            # Batch compute all stats for this window
            # Separate side stats from regular stats
            regular_stats = [s for s in stat_list if not s[3]]
            side_stats = [s for s in stat_list if s[3]]
            
            # Compute regular stats in batch
            if regular_stats:
                # Separate _net stats from regular stats
                regular_non_net_stats = [s for s in regular_stats if '_net' not in s[2]]
                regular_net_stats = [s for s in regular_stats if '_net' in s[2]]
                
                # Process non-net stats
                if regular_non_net_stats:
                    home_stat_names = [s[2] for s in regular_non_net_stats]  # s[2] is base_stat_name
                    away_stat_names = [s[2] for s in regular_non_net_stats]
                    home_results = self._get_all_stats_batch(HOME, home_games, home_stat_names, reference_date, False, window_key, base_stat_calc_weight_map)
                    away_results = self._get_all_stats_batch(AWAY, away_games, away_stat_names, reference_date, False, window_key, base_stat_calc_weight_map)
                    
                    for stat_idx, original_stat, base_stat_name, _ in regular_non_net_stats:
                        home_val = home_results.get(base_stat_name, 0.0)
                        away_val = away_results.get(base_stat_name, 0.0)
                        stat_results[stat_idx] = (home_val, away_val)
                
                # Process _net stats (team stat - opponent defensive stat)
                if regular_net_stats:
                    # Map _net stat names to their base stat and opponent defensive stat
                    net_stat_map = {
                        'effective_fg_perc_net': ('effective_fg_perc', 'opp_effective_fg_perc'),
                        'true_shooting_perc_net': ('true_shooting_perc', 'opp_true_shooting_perc'),
                        'three_perc_net': ('three_perc', 'opp_three_perc'),
                        'off_rtg_net': ('off_rtg', 'def_rtg'),  # team's off_rtg - opponent's def_rtg (what team allowed)
                        'assists_ratio_net': ('assists_ratio', 'opp_assists_ratio'),
                        'points_net': ('points', 'opp_points'),  # team's points - opponent's points (what team allowed)
                    }
                    
                    for stat_idx, original_stat, base_stat_name, _ in regular_net_stats:
                        if base_stat_name in net_stat_map:
                            team_stat_name, opp_def_stat_name = net_stat_map[base_stat_name]
                            
                            # Get calc_weight for this stat
                            calc_weight = 'avg'
                            if base_stat_calc_weight_map:
                                calc_weight = base_stat_calc_weight_map.get(team_stat_name, 'avg')
                            
                            # Get team's offensive stat
                            # Use _get_all_stats_batch for consistency with calc_weight handling
                            home_team_results = self._get_all_stats_batch(HOME, home_games, [team_stat_name], reference_date, False, window_key, {team_stat_name: calc_weight} if base_stat_calc_weight_map else None)
                            away_team_results = self._get_all_stats_batch(AWAY, away_games, [team_stat_name], reference_date, False, window_key, {team_stat_name: calc_weight} if base_stat_calc_weight_map else None)
                            
                            home_team_stat = home_team_results.get(team_stat_name, 0.0)
                            away_team_stat = away_team_results.get(team_stat_name, 0.0)
                            
                            # Get opponent's defensive stat (what opponents allowed)
                            # For home team: what home's opponents allowed = what home allowed to opponents
                            # For away team: what away's opponents allowed = what away allowed to opponents
                            home_opp_results = self._get_all_stats_batch(HOME, home_games, [opp_def_stat_name], reference_date, False, window_key, {opp_def_stat_name: calc_weight} if base_stat_calc_weight_map else None)
                            away_opp_results = self._get_all_stats_batch(AWAY, away_games, [opp_def_stat_name], reference_date, False, window_key, {opp_def_stat_name: calc_weight} if base_stat_calc_weight_map else None)
                            
                            home_opp_def_stat = home_opp_results.get(opp_def_stat_name, 0.0)
                            away_opp_def_stat = away_opp_results.get(opp_def_stat_name, 0.0)
                            
                            # Calculate net: team stat - opponent defensive stat
                            home_net = home_team_stat - home_opp_def_stat
                            away_net = away_team_stat - away_opp_def_stat
                            
                            stat_results[stat_idx] = (home_net, away_net)
                        else:
                            # Fallback: treat as regular stat
                            stat_results[stat_idx] = (0.0, 0.0)
                    
                    # Log if stat is 0 and we have games (means stat field doesn't exist in DB)
                    if home_val == 0.0 and home_games:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"[FEAT] {original_stat}: home_val=0.0 for {HOME} despite {len(home_games)} {window_key} games (field '{base_stat_name}' not found or all zeros)")
                    if away_val == 0.0 and away_games:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"[FEAT] {original_stat}: away_val=0.0 for {AWAY} despite {len(away_games)} {window_key} games (field '{base_stat_name}' not found or all zeros)")
            
            # Compute side stats (these are the same as regular stats, just different token)
            # For side stats, we need to filter to only games where team played at that side
            if side_stats:
                home_stat_names = [s[2] for s in side_stats]  # s[2] is base_stat_name
                away_stat_names = [s[2] for s in side_stats]
                
                # Filter to only home games for HOME team's side stats
                home_side_games = [g for g in home_games if g.get('homeTeam', {}).get('name') == HOME]
                # Filter to only away games for AWAY team's side stats  
                away_side_games = [g for g in away_games if g.get('awayTeam', {}).get('name') == AWAY]
                
                home_results = self._get_all_stats_batch(HOME, home_side_games, home_stat_names, reference_date, True, window_key, base_stat_calc_weight_map)
                away_results = self._get_all_stats_batch(AWAY, away_side_games, away_stat_names, reference_date, True, window_key, base_stat_calc_weight_map)
                
                for stat_idx, original_stat, base_stat_name, _ in side_stats:
                    home_val = home_results.get(base_stat_name, 0.0)
                    away_val = away_results.get(base_stat_name, 0.0)
                    stat_results[stat_idx] = (home_val, away_val)
                    
                    # Log if stat is 0 and we have games (means stat field doesn't exist in DB)
                    if home_val == 0.0 and home_games:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"[FEAT] {original_stat}: home_val=0.0 for {HOME} despite {len(home_games)} {window_key} games (field '{base_stat_name}' not found or all zeros)")
                    if away_val == 0.0 and away_games:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"[FEAT] {original_stat}: away_val=0.0 for {AWAY} despite {len(away_games)} {window_key} games (field '{base_stat_name}' not found or all zeros)")
        
        # Reconstruct stats in original order, with optional absolute values
        for stat_idx in range(len(self.statistics)):
            if stat_idx in stat_results:
                home_val, away_val = stat_results[stat_idx]
                stat_name = self.statistics[stat_idx]
                
                if point_regression:
                    stats.append(home_val)
                    stats.append(away_val)
                else:
                    # Add differential
                    stats.append(home_val - away_val)
                    
                    # Add absolute values for key stats if requested
                    if include_absolute and is_key_stat_func and is_key_stat_func(stat_name):
                        stats.append(home_val)
                        stats.append(away_val)
            else:
                # Fallback (shouldn't happen)
                stats.append(0.0)
                if include_absolute and is_key_stat_func and is_key_stat_func(self.statistics[stat_idx]):
                    stats.append(0.0)
                    stats.append(0.0)
        
        # Enhanced features are no longer included in getStatAvgDiffs
        # They are calculated directly via calculate_feature() in the new architecture
        # This function is only used for old format compatibility
        
        return stats
    
    def _get_stat(self, team: str, games: list, stat_name: str, reference_date: date, calc_weight: str = None) -> float:
        """
        Get a stat value for a team from a list of games.
        
        Args:
            team: Team name
            games: List of game documents
            stat_name: Stat name to compute
            reference_date: Reference date for weighted averages
            calc_weight: Optional 'raw' or 'avg'. If 'raw', aggregate first then calculate.
                        If 'avg' or None, calculate per-game then average.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        if not games:
            logger.debug(f"[FEAT] _get_stat: No games provided for {team}, stat '{stat_name}' -> 0.0")
            return 0.0
        
        # If calc_weight is 'raw', use aggregate-first approach
        if calc_weight == 'raw':
            computed_from_aggregate = self._compute_derived_stat_from_aggregate(stat_name, games, team)
            if computed_from_aggregate is not None:
                logger.debug(f"[FEAT] _get_stat: Stat '{stat_name}' computed from aggregated raw stats (raw calc_weight) for {team}")
                return computed_from_aggregate
            else:
                logger.debug(f"[FEAT] _get_stat: Could not compute '{stat_name}' from aggregate for {team}")
                return 0.0
        
        # Otherwise, use per-game then average approach (default)
        values = []
        dates = []
        found_count = 0
        
        for game in games:
            if game['homeTeam']['name'] == team:
                team_data = game['homeTeam']
            elif game['awayTeam']['name'] == team:
                team_data = game['awayTeam']
            else:
                continue
            
            # First try to get the stat directly from the DB
            if stat_name in team_data:
                value = team_data.get(stat_name)
                if value is not None:
                    values.append(value)
                    dates.append(game['date'])
                    found_count += 1
            else:
                # If not found, try to compute it from raw stats (derived stats)
                # Pass the full game document for 'wins' calculation
                computed_value = self._compute_derived_stat(stat_name, team_data, game)
                if computed_value is not None:
                    values.append(computed_value)
                    dates.append(game['date'])
                    found_count += 1
        
        if not values:
            # Try to compute from aggregated raw stats if this is a derived stat (fallback)
            computed_from_aggregate = self._compute_derived_stat_from_aggregate(stat_name, games, team)
            if computed_from_aggregate is not None:
                logger.debug(f"[FEAT] _get_stat: Stat '{stat_name}' computed from aggregated raw stats (fallback) for {team}")
                return computed_from_aggregate
            
            # Downgrade to debug to avoid noisy warnings for non-DB fields (e.g., 'b2b')
            logger.debug(f"[FEAT] _get_stat: Stat '{stat_name}' not found in DB for {team} (checked {len(games)} games, found in {found_count}). Sample dates: {[g.get('date') for g in games[:3]]}")
            return 0.0
        
        if found_count < len(games):
            logger.debug(f"[FEAT] _get_stat: Stat '{stat_name}' found in {found_count}/{len(games)} games for {team}")
        
        if self.use_exponential_weighting:
            return self.weighted_avg(values, dates, reference_date)
        else:
            return self.avg(values)
    
    def _compute_derived_stat(self, stat_name: str, team_data: dict, game: dict = None) -> float:
        """
        Compute a derived stat from raw stats in team_data for a single game.
        
        Args:
            stat_name: Name of the derived stat to compute
            team_data: Team data dictionary from a game document
            game: Optional full game document (needed for 'wins' calculation)
            
        Returns:
            Computed stat value, or None if it can't be computed
        """
        if stat_name == 'three_perc':
            three_made = team_data.get('three_made', 0)
            three_att = team_data.get('three_att', 0)
            if three_att > 0:
                return (three_made / three_att) * 100  # Convert to percentage
            return None
        
        elif stat_name == 'effective_fg_perc':
            fg_made = team_data.get('FG_made', 0)
            fg_att = team_data.get('FG_att', 0)
            three_made = team_data.get('three_made', 0)
            if fg_att > 0:
                return ((fg_made + 0.5 * three_made) / fg_att) * 100  # Convert to percentage
            return None
        
        elif stat_name == 'true_shooting_perc':
            points = team_data.get('points', 0)
            fg_att = team_data.get('FG_att', 0)
            ft_att = team_data.get('FT_att', 0)
            denominator = 2 * (fg_att + 0.44 * ft_att)
            if denominator > 0:
                return (points / denominator) * 100  # Convert to percentage
            return None
        
        elif stat_name == 'TO_metric':
            to = team_data.get('TO', 0)
            fg_att = team_data.get('FG_att', 0)
            ft_att = team_data.get('FT_att', 0)
            denominator = fg_att + 0.44 * ft_att + to
            if denominator > 0:
                return 100 * to / denominator
            return None
        
        elif stat_name == 'ast_to_ratio':
            assists = team_data.get('assists', 0)
            to = team_data.get('TO', 0)
            if to > 0:
                return assists / to
            return None
        
        elif stat_name == 'opp_effective_fg_perc' and game is not None:
            # Compute opponent eFG% from opponent raw stats for this single game
            team_name = team_data.get('name')
            if not team_name:
                return None
            if game.get('homeTeam', {}).get('name') == team_name:
                opp = game.get('awayTeam', {})
            else:
                opp = game.get('homeTeam', {})
            fg_made = opp.get('FG_made', 0)
            fg_att = opp.get('FG_att', 0)
            three_made = opp.get('three_made', 0)
            if fg_att > 0:
                return ((fg_made + 0.5 * three_made) / fg_att) * 100
            return None
        
        elif stat_name == 'wins' and game is not None:
            # Calculate if this team won the game
            # Need to know if team is home or away
            team_name = team_data.get('name')
            if team_name is None:
                return None
            
            is_home = game.get('homeTeam', {}).get('name') == team_name
            home_won = game.get('homeWon', False)
            
            # Team wins if: (is home and home won) OR (is away and home didn't win)
            if (is_home and home_won) or (not is_home and not home_won):
                return 1.0
            else:
                return 0.0
        
        # Return None if this is not a derived stat we know how to compute
        return None
    
    def _compute_derived_stat_from_aggregate(self, stat_name: str, games: list, team: str) -> float:
        """
        Compute a derived stat from aggregated raw stats across multiple games.
        This is used as a fallback when individual game values aren't available.
        Also handles advanced stats that need to be computed from aggregates (off_rtg, def_rtg, etc.).
        
        Args:
            stat_name: Name of the derived stat to compute
            games: List of game documents
            team: Team name
            
        Returns:
            Computed stat value, or None if it can't be computed
        """
        if not games:
            return None
        
        # Handle wins - count wins across games
        if stat_name == 'wins':
            wins = 0
            for game in games:
                is_home = game.get('homeTeam', {}).get('name') == team
                home_won = game.get('homeWon', False)
                if (is_home and home_won) or (not is_home and not home_won):
                    wins += 1
            return float(wins)
        
        # Handle advanced stats that need full aggregation
        if stat_name in ['off_rtg', 'def_rtg', 'assists_ratio', 'TO_metric', 'ast_to_ratio', 'effective_fg_perc', 'true_shooting_perc', 'three_perc', 
                         'opp_effective_fg_perc', 'opp_true_shooting_perc', 'opp_three_perc', 'opp_assists_ratio', 'opp_points']:
            # Aggregate team stats and opponent stats
            team_agg = defaultdict(float)
            team_against_agg = defaultdict(float)
            
            for game in games:
                if game['homeTeam']['name'] == team:
                    team_data = game['homeTeam']
                    opp_data = game['awayTeam']
                elif game['awayTeam']['name'] == team:
                    team_data = game['awayTeam']
                    opp_data = game['homeTeam']
                else:
                    continue
                
                # Aggregate team stats
                for key, value in team_data.items():
                    if isinstance(value, (int, float)):
                        team_agg[key] += value
                
                # Aggregate opponent stats (for defensive stats)
                for key, value in opp_data.items():
                    if isinstance(value, (int, float)):
                        team_against_agg[key] += value
            
            # Use existing advanced stats computation
            adv_stats = self._compute_advanced_stats(team_agg, team_against_agg, len(games))
            
            # Map stat names (handle aliases and opponent eFG)
            if stat_name == 'effective_fg_perc':
                return adv_stats.get('efg', None)
            if stat_name == 'assists_ratio':
                # Calculate assists_ratio: 100 * (assists / (((total_min / 5) * FG_made) - FG_made))
                # Note: total_min = 48 min per game unless "OT" is true, then 53 min
                assists = team_agg.get('assists', 0)
                fg_made = team_agg.get('FG_made', 0)
                if fg_made > 0:
                    # Calculate total_min across all games
                    total_min = 0
                    for game in games:
                        # Check if game has OT
                        is_ot = game.get('OT', False)
                        total_min += 53 if is_ot else 48
                    assists_ratio = 100 * (assists / (((total_min / 5) * fg_made) - fg_made)) if ((total_min / 5) * fg_made) - fg_made > 0 else 0
                    return assists_ratio
                return None
            if stat_name == 'opp_effective_fg_perc':
                opp_fg_att = team_against_agg.get('FG_att', 0)
                if opp_fg_att > 0:
                    opp_efg = ((team_against_agg.get('FG_made', 0) + 0.5 * team_against_agg.get('three_made', 0)) / opp_fg_att) * 100
                    return opp_efg
                return None
            
            # Compute opponent true shooting percentage (what opponents shot against this team)
            if stat_name == 'opp_true_shooting_perc':
                opp_pts = team_against_agg.get('points', 0)
                opp_fga = team_against_agg.get('FG_att', 0)
                opp_fta = team_against_agg.get('FT_att', 0)
                if opp_fga + 0.44 * opp_fta > 0:
                    opp_ts = (opp_pts / (2 * (opp_fga + 0.44 * opp_fta))) * 100
                    return opp_ts
                return None
            
            # Compute opponent three point percentage (what opponents shot from 3 against this team)
            if stat_name == 'opp_three_perc':
                opp_three_att = team_against_agg.get('three_att', 0)
                if opp_three_att > 0:
                    opp_three_pct = (team_against_agg.get('three_made', 0) / opp_three_att) * 100
                    return opp_three_pct
                return None
            
            # Compute opponent assists ratio (what opponents' assists ratio was against this team)
            if stat_name == 'opp_assists_ratio':
                # Calculate using same formula: 100 * (assists / (((total_min / 5) * FG_made) - FG_made))
                opp_ast = team_against_agg.get('assists', 0)
                opp_fg_made = team_against_agg.get('FG_made', 0)
                if opp_fg_made > 0:
                    # Calculate total_min across all games
                    total_min = 0
                    for game in games:
                        is_ot = game.get('OT', False)
                        total_min += 53 if is_ot else 48
                    opp_ast_ratio = 100 * (opp_ast / (((total_min / 5) * opp_fg_made) - opp_fg_made)) if ((total_min / 5) * opp_fg_made) - opp_fg_made > 0 else 0
                    return opp_ast_ratio
                return None
            
            # Compute TO_metric: 100 * TO / (FG_att + 0.44*FT_att + TO)
            if stat_name == 'TO_metric':
                to = team_agg.get('TO', 0)
                fga = team_agg.get('FG_att', 0)
                fta = team_agg.get('FT_att', 0)
                denominator = fga + 0.44 * fta + to
                if denominator > 0:
                    return 100 * to / denominator
                return None
            
            # Compute ast_to_ratio: assists/TO
            if stat_name == 'ast_to_ratio':
                assists = team_agg.get('assists', 0)
                to = team_agg.get('TO', 0)
                if to > 0:
                    return assists / to
                return None
            
            # Compute three_perc: (three_made / three_att) * 100
            if stat_name == 'three_perc':
                three_made = team_agg.get('three_made', 0)
                three_att = team_agg.get('three_att', 0)
                if three_att > 0:
                    return (three_made / three_att) * 100
                return None
            
            # Compute true_shooting_perc: (points / (2 * (FG_att + 0.44 * FT_att))) * 100
            if stat_name == 'true_shooting_perc':
                points = team_agg.get('points', 0)
                fg_att = team_agg.get('FG_att', 0)
                ft_att = team_agg.get('FT_att', 0)
                denominator = 2 * (fg_att + 0.44 * ft_att)
                if denominator > 0:
                    return (points / denominator) * 100
                return None
            
            # Compute opponent points (what opponents scored against this team)
            if stat_name == 'opp_points':
                opp_pts = team_against_agg.get('points', 0)
                if len(games) > 0:
                    # Return points per game
                    return opp_pts / len(games)
                return None
            if stat_name in adv_stats:
                return adv_stats.get(stat_name, None)
        
        # Aggregate raw stats for percentage calculations
        total_three_made = 0
        total_three_att = 0
        total_fg_made = 0
        total_fg_att = 0
        total_points = 0
        total_ft_att = 0
        
        for game in games:
            if game['homeTeam']['name'] == team:
                team_data = game['homeTeam']
            elif game['awayTeam']['name'] == team:
                team_data = game['awayTeam']
            else:
                continue
            
            total_three_made += team_data.get('three_made', 0)
            total_three_att += team_data.get('three_att', 0)
            total_fg_made += team_data.get('FG_made', 0)
            total_fg_att += team_data.get('FG_att', 0)
            total_points += team_data.get('points', 0)
            total_ft_att += team_data.get('FT_att', 0)
        
        if stat_name == 'three_perc':
            if total_three_att > 0:
                return (total_three_made / total_three_att) * 100
            return None
        
        elif stat_name == 'true_shooting_perc':
            denominator = 2 * (total_fg_att + 0.44 * total_ft_att)
            if denominator > 0:
                return (total_points / denominator) * 100
            return None
        
        return None
    
    def _get_all_stats_batch(self, team: str, games: list, stat_names: list, reference_date: date, is_side_stat: bool = False, window_key: tuple = None, calc_weight_map: dict = None) -> dict:
        """
        Batch compute multiple stats for a team by iterating through games only once.
        This is much faster than calling _get_stat multiple times.
        
        Args:
            team: Team name
            games: List of game documents
            stat_names: List of stat names to compute
            reference_date: Reference date for weighted averages
            is_side_stat: If True, compute side-specific stats (only count games where team is home/away)
            calc_weight_map: Optional dict mapping stat_name -> 'raw' or 'avg'. 
                            If 'raw', aggregate first then calculate (for complex stats like efg).
                            If 'avg' or not specified, calculate per-game then average.
            
        Returns:
            Dict mapping stat_name -> computed value
        """
        if not games or not stat_names:
            if games:  # Have games but no stat names requested
                return {stat: 0.0 for stat in stat_names}
            else:  # No games
                import logging
                logger = logging.getLogger(__name__)
                window_str = f" {window_key}" if window_key else ""
                logger.debug(f"[FEAT] _get_all_stats_batch: No games provided for {team} (window{window_str})")
                return {stat: 0.0 for stat in stat_names}
        
        if calc_weight_map is None:
            calc_weight_map = {}
        
        # Separate stats by calc_weight method
        raw_stats = [stat for stat in stat_names if calc_weight_map.get(stat) == 'raw']
        avg_stats = [stat for stat in stat_names if calc_weight_map.get(stat) != 'raw']
        
        # For 'raw' stats, compute directly from aggregate (skip per-game calculation)
        results = {}
        import logging
        logger = logging.getLogger(__name__)
        window_str = f" (window {window_key})" if window_key else ""
        
        for stat_name in raw_stats:
            # Compute from aggregated raw stats directly
            computed_from_aggregate = self._compute_derived_stat_from_aggregate(stat_name, games, team)
            if computed_from_aggregate is not None:
                results[stat_name] = computed_from_aggregate
                logger.debug(f"[FEAT] {stat_name}: Computed from aggregated raw stats (raw calc_weight) for {team}{window_str}")
            else:
                results[stat_name] = 0.0
                logger.debug(f"[FEAT] {stat_name}: Could not compute from aggregate for {team}{window_str}")
        
        # For 'avg' stats (or default), use per-game then average approach
        if avg_stats:
            # Initialize storage for each stat
            stat_values = {stat: [] for stat in avg_stats}
            stat_dates = {stat: [] for stat in avg_stats}
            stat_found_count = {stat: 0 for stat in avg_stats}  # Track how many games had this stat
            
            # Single pass through games to extract all stat values
            for game in games:
                is_home_team = game['homeTeam']['name'] == team
                is_away_team = game['awayTeam']['name'] == team
                
                # For side stats, filter to only games where team is home (when called for home stats)
                # or away (when called for away stats). The caller should pass filtered games, but
                # we'll be defensive and check here too.
                if is_side_stat:
                    # Side stats: only count games where team played at the specified side
                    # This depends on how the function is called - if it's for "home_side", only count home games
                    # The caller should already filter, but we verify the team is on the correct side
                    if not (is_home_team or is_away_team):
                        continue
                
                if is_home_team:
                    team_data = game['homeTeam']
                elif is_away_team:
                    team_data = game['awayTeam']
                else:
                    continue
                
                game_date = game['date']
                
                # Extract all stat values for this game
                for stat_name in avg_stats:
                    # First try to get the stat directly from the DB
                    if stat_name in team_data:
                        value = team_data.get(stat_name)
                        if value is not None:
                            stat_values[stat_name].append(value)
                            stat_dates[stat_name].append(game_date)
                            stat_found_count[stat_name] += 1
                    else:
                        # If not found, try to compute it from raw stats (derived stats)
                        # Pass the full game document for 'wins' calculation
                        computed_value = self._compute_derived_stat(stat_name, team_data, game)
                        if computed_value is not None:
                            stat_values[stat_name].append(computed_value)
                            stat_dates[stat_name].append(game_date)
                            stat_found_count[stat_name] += 1
            
            # Compute averages for all avg_stats
            for stat_name in avg_stats:
                values = stat_values[stat_name]
                dates = stat_dates[stat_name]
                found_count = stat_found_count[stat_name]
                
                if not values:
                    # Try to compute from aggregated raw stats if this is a derived stat (fallback)
                    computed_from_aggregate = self._compute_derived_stat_from_aggregate(stat_name, games, team)
                    if computed_from_aggregate is not None:
                        results[stat_name] = computed_from_aggregate
                        logger.debug(f"[FEAT] {stat_name}: Computed from aggregated raw stats (fallback) for {team}{window_str}")
                    else:
                        results[stat_name] = 0.0
                        # Downgrade missing-field notice to debug to avoid noisy logs for non-DB fields
                        if len(games) > 0 and found_count == 0:
                            logger.debug(f"[FEAT] {stat_name}: Field not found in DB for {team} ({found_count}/{len(games)} games){window_str}. All games checked: {[g.get('date') for g in games[:5]]}")
                        elif found_count < len(games):
                            logger.debug(f"[FEAT] {stat_name}: Found in {found_count}/{len(games)} games for {team}{window_str}")
                elif self.use_exponential_weighting:
                    results[stat_name] = self.weighted_avg(values, dates, reference_date)
                else:
                    results[stat_name] = self.avg(values)
        
        return results
    
    def _get_side_stat(self, team: str, games: list, stat_name: str, reference_date: date) -> float:
        """Get a side-specific stat (home/away) for a team."""
        if not games:
            return 0.0
        
        values = []
        dates = []
        
        for game in games:
            if game['homeTeam']['name'] == team:
                team_data = game['homeTeam']
            elif game['awayTeam']['name'] == team:
                team_data = game['awayTeam']
            else:
                continue
            
            # Get side-specific value
            side_value = team_data.get(stat_name, 0)
            if side_value is not None:
                values.append(side_value)
                dates.append(game['date'])
        
        if self.use_exponential_weighting:
            return self.weighted_avg(values, dates, reference_date)
        else:
            return self.avg(values)
    
    # get_enhanced_features() removed - all enhanced features are now calculated directly
    # via calculate_feature() using new-format feature names (e.g., 'pace|season|avg|home')
    
    def _calculate_pace(self, team: str, games: list) -> float:
        """Calculate average pace (possessions per game) for a team."""
        if not games:
            return 0.0
        
        total_possessions = 0.0
        for game in games:
            if game['homeTeam']['name'] == team:
                team_data = game['homeTeam']
            elif game['awayTeam']['name'] == team:
                team_data = game['awayTeam']
            else:
                continue
            
            # Simple pace calculation: FGA - OReb + TO + 0.44 * FTA
            fga = team_data.get('FG_att', 0)
            oreb = team_data.get('off_reb', 0)
            to = team_data.get('TO', 0)
            fta = team_data.get('FT_att', 0)
            
            possessions = fga - oreb + to + 0.44 * fta
            total_possessions += possessions
        
        return total_possessions / len(games) if games else 0.0
    
    def get_era_normalized_features(self, HOME: str, AWAY: str, season: str, year: int, month: int, day: int) -> dict:
        """
        Compute era-normalized features (relative to league average).
        
        Returns:
            Dict with home/away/diff features
        """
        if season not in self.league_averages:
            return {}
        
        league_avg = self.league_averages[season]
        
        # Get team season averages
        home_games = self.get_team_games_before_date(HOME, year, month, day, season)
        away_games = self.get_team_games_before_date(AWAY, year, month, day, season)
        
        reference_date = date(year, month, day)
        
        home_ppg = self._get_stat(HOME, home_games, 'points', reference_date)
        away_ppg = self._get_stat(AWAY, away_games, 'points', reference_date)
        
        home_off_rtg = self._get_stat(HOME, home_games, 'off_rtg', reference_date)
        away_off_rtg = self._get_stat(AWAY, away_games, 'off_rtg', reference_date)
        
        lg_ppg = league_avg.get('points', 100.0)
        lg_off_rtg = league_avg.get('off_rtg', 100.0)
        
        features = {
            'homePpgRel': home_ppg / lg_ppg if lg_ppg > 0 else 1.0,
            'awayPpgRel': away_ppg / lg_ppg if lg_ppg > 0 else 1.0,
            'homeOffRtgRel': home_off_rtg / lg_off_rtg if lg_off_rtg > 0 else 1.0,
            'awayOffRtgRel': away_off_rtg / lg_off_rtg if lg_off_rtg > 0 else 1.0,
            'ppgRelDiff': (home_ppg / lg_ppg if lg_ppg > 0 else 1.0) - (away_ppg / lg_ppg if lg_ppg > 0 else 1.0),
            'offRtgRelDiff': (home_off_rtg / lg_off_rtg if lg_off_rtg > 0 else 1.0) - (away_off_rtg / lg_off_rtg if lg_off_rtg > 0 else 1.0)
        }
        
        return features
    
    def _aggregate_games(self, games: list, team: str) -> tuple:
        """
        Aggregate stats from a list of games for a team.
        
        Returns:
            Tuple of (team_agg, team_against_agg, team_side_agg, team_side_against_agg, home_games, away_games)
        """
        team_agg = defaultdict(float)
        team_against_agg = defaultdict(float)
        team_side_agg = defaultdict(float)
        team_side_against_agg = defaultdict(float)
        home_games = []
        away_games = []
        
        for game in games:
            if game['homeTeam']['name'] == team:
                team_data = game['homeTeam']
                against_data = game['awayTeam']
                home_games.append(game)
            elif game['awayTeam']['name'] == team:
                team_data = game['awayTeam']
                against_data = game['homeTeam']
                away_games.append(game)
            else:
                continue
            
            # Aggregate team stats
            for key, value in team_data.items():
                if isinstance(value, (int, float)):
                    team_agg[key] += value
            
            # Aggregate against stats
            for key, value in against_data.items():
                if isinstance(value, (int, float)):
                    team_against_agg[key] += value
            
            # Aggregate side-specific stats
            if 'homeTeam' in game and game['homeTeam']['name'] == team:
                for key, value in team_data.items():
                    if isinstance(value, (int, float)) and '_side' in key:
                        team_side_agg[key] += value
                for key, value in against_data.items():
                    if isinstance(value, (int, float)) and '_side' in key:
                        team_side_against_agg[key] += value
        
        return team_agg, team_against_agg, team_side_agg, team_side_against_agg, home_games, away_games
    
    def _compute_advanced_stats(self, team_agg: dict, team_against_agg: dict, games_played: int) -> dict:
        """Compute advanced statistics from aggregated stats."""
        if games_played == 0:
            return {}
        
        # Calculate possessions
        fga = team_agg.get('FG_att', 0)
        oreb = team_agg.get('off_reb', 0)
        to = team_agg.get('TO', 0)
        fta = team_agg.get('FT_att', 0)
        possessions = fga - oreb + to + 0.44 * fta
        
        # Points per game
        ppg = team_agg.get('points', 0) / games_played if games_played > 0 else 0
        
        # Offensive rating
        off_rtg = (team_agg.get('points', 0) / possessions * 100) if possessions > 0 else 0
        
        # Defensive rating
        opp_possessions = team_against_agg.get('FG_att', 0) - team_against_agg.get('off_reb', 0) + team_against_agg.get('TO', 0) + 0.44 * team_against_agg.get('FT_att', 0)
        def_rtg = (team_against_agg.get('points', 0) / opp_possessions * 100) if opp_possessions > 0 else 0
        
        # Effective FG%
        fg_made = team_agg.get('FG_made', 0)
        efg = ((fg_made + 0.5 * team_agg.get('three_made', 0)) / fga * 100) if fga > 0 else 0
        
        # Assist ratio
        ast = team_agg.get('assists', 0)
        ast_ratio = (ast / (fga + 0.44 * fta + ast + to) * 100) if (fga + 0.44 * fta + ast + to) > 0 else 0
        
        # TO metric
        to_metric = (to / possessions * 100) if possessions > 0 else 0
        
        return {
            'ppg': ppg,
            'off_rtg': off_rtg,
            'def_rtg': def_rtg,
            'efg': efg,
            'ast_ratio': ast_ratio,
            'to_metric': to_metric
        }
    
    def _get_stat_diff(self, stat: str, home_games: list, away_games: list, 
                      home_agg: dict, home_against: dict, away_agg: dict, away_against: dict,
                      home_side_agg: dict, home_side_against: dict, away_side_agg: dict, away_side_against: dict,
                      home_side_games: int, away_side_games: int) -> float:
        """
        Calculate stat differential between home and away teams.
        """
        # Check if it's a known advanced stat
        if stat in ['off_rtg', 'def_rtg', 'efg', 'ast_ratio', 'to_metric']:
            home_adv = self._compute_advanced_stats(home_agg, home_against, len(home_games))
            away_adv = self._compute_advanced_stats(away_agg, away_against, len(away_games))
            
            home_val = home_adv.get(stat, 0)
            away_val = away_adv.get(stat, 0)
            
            # Calculate differential (home - away)
            return home_val - away_val
        
        # Check if it's a side-specific stat
        side_stat = '_side' in stat
        if side_stat:
            stat_clean = stat.replace('_side', '')
            
            # Get side-specific values
            home_side_val = home_side_agg.get(stat, 0) / home_side_games if home_side_games > 0 else 0
            away_side_val = away_side_agg.get(stat, 0) / away_side_games if away_side_games > 0 else 0
            
            # Get against values
            home_side_against_val = home_side_against.get(stat, 0) / home_side_games if home_side_games > 0 else 0
            away_side_against_val = away_side_against.get(stat, 0) / away_side_games if away_side_games > 0 else 0
            
            home_diff = home_side_val - home_side_against_val
            away_diff = away_side_val - away_side_against_val
            return home_diff - away_diff
        
        # Known stat in aggregation
        if side_stat:
            home_diff = (home_side_agg[stat] / home_side_games) - (home_side_against[stat] / home_side_games)
            away_diff = (away_side_agg[stat] / away_side_games) - (away_side_against[stat] / away_side_games)
        else:
            home_diff = (home_agg[stat] / len(home_games)) - (home_against[stat] / len(home_games))
            away_diff = (away_agg[stat] / len(away_games)) - (away_against[stat] / len(away_games))
        
        return home_diff - away_diff
    
    # =========================================================================
    # DIRECT FEATURE CALCULATION (NEW ARCHITECTURE)
    # =========================================================================
    
    def calculate_feature(
        self,
        feature_name: str,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int,
        per_calculator=None
    ) -> float:
        """
        Calculate a single feature value directly from its name.
        
        This is the new direct architecture that eliminates stat tokens.
        Features are calculated directly based on their name components.
        
        Args:
            feature_name: Feature name in new format (e.g., 'points|season|avg|diff')
            home_team: Home team name
            away_team: Away team name
            season: NBA season string
            year, month, day: Game date
            per_calculator: Optional PERCalculator instance (for PER features)
            
        Returns:
            Feature value (float), or 0.0 if calculation fails
        """
        # Parse feature name
        components = parse_feature_name(feature_name)
        if not components:
            # Not a standard feature - might be special (elo, rest, etc.)
            return self._calculate_special_feature(feature_name, home_team, away_team, season, year, month, day, per_calculator)
        
        stat_name = components.stat_name
        time_period = components.time_period
        calc_weight = components.calc_weight
        perspective = components.home_away_diff  # 'home', 'away', or 'diff'
        is_side = components.is_side
        
        # All features follow standard stat pattern now - no special handling needed
        
        # Handle PER features
        if stat_name.startswith('player_'):
            return self._calculate_per_feature(feature_name, home_team, away_team, season, year, month, day, per_calculator)
        
        # Handle blend features (stat_name ends with '_blend')
        is_blend = stat_name.endswith('_blend')
        if is_blend:
            base_stat_name = stat_name[:-6]  # Remove '_blend'
            return self._calculate_blend_feature(
                base_stat_name, time_period, calc_weight, perspective, is_side,
                home_team, away_team, season, year, month, day
            )
        
        # Handle enhanced features (pace, travel, b2b, games_played, points with std)
        if stat_name in ['pace', 'travel', 'b2b', 'games_played']:
            return self._calculate_enhanced_feature(feature_name, home_team, away_team, season, year, month, day)
        elif stat_name == 'points' and components.calc_weight == 'std':
            # Points standard deviation (volatility) - special enhanced feature
            return self._calculate_enhanced_feature(feature_name, home_team, away_team, season, year, month, day)
        
        # Handle net features (stat_name ends with '_net')
        is_net = stat_name.endswith('_net')
        if is_net:
            base_stat_name = stat_name[:-4]  # Remove '_net'
            return self._calculate_net_feature(
                base_stat_name, time_period, calc_weight, perspective, is_side,
                home_team, away_team, season, year, month, day
            )
        
        # Handle regular stats (basic and rate)
        return self._calculate_regular_feature(
            stat_name, time_period, calc_weight, perspective, is_side,
            home_team, away_team, season, year, month, day
        )
    
    def _calculate_regular_feature(
        self,
        stat_name: str,
        time_period: str,
        calc_weight: str,
        perspective: str,
        is_side: bool,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int
    ) -> float:
        """
        Calculate a regular stat feature (basic or rate stat).
        
        Args:
            stat_name: Base stat name (e.g., 'points', 'efg', 'off_rtg')
            time_period: Time period (e.g., 'season', 'months_1', 'games_10')
            calc_weight: Calculation method ('raw' or 'avg')
            perspective: 'home', 'away', or 'diff'
            is_side: Whether this is a side-split feature
            home_team, away_team, season, year, month, day: Game context
            
        Returns:
            Feature value
        """
        reference_date = date(year, month, day)
        
        # Get games for home and away teams based on time_period
        home_games = self._get_games_for_time_period(home_team, season, year, month, day, time_period)
        away_games = self._get_games_for_time_period(away_team, season, year, month, day, time_period)
        
        # Filter to side-specific games if needed
        if is_side:
            home_games = [g for g in home_games if g.get('homeTeam', {}).get('name') == home_team]
            away_games = [g for g in away_games if g.get('awayTeam', {}).get('name') == away_team]
        
        # Calculate stat for home team
        home_value = self._calculate_team_stat(
            stat_name, home_team, home_games, calc_weight, reference_date
        )
        
        # Calculate stat for away team
        away_value = self._calculate_team_stat(
            stat_name, away_team, away_games, calc_weight, reference_date
        )
        
        # Return based on perspective
        if perspective == 'home':
            return home_value
        elif perspective == 'away':
            return away_value
        else:  # 'diff'
            return home_value - away_value
    
    def _calculate_team_stat(
        self,
        stat_name: str,
        team: str,
        games: list,
        calc_weight: str,
        reference_date: date
    ) -> float:
        """
        Calculate a stat value for a team from a list of games.
        
        Args:
            stat_name: Stat name (e.g., 'points', 'efg', 'off_rtg')
            team: Team name
            games: List of game documents
            calc_weight: 'raw' or 'avg'
            reference_date: Reference date for weighted averages
            
        Returns:
            Stat value
        """
        if not games:
            return 0.0
        
        # Map stat names to internal names (normalize)
        # Note: Some stats use different names internally vs externally
        stat_name_map = {
            'efg': 'effective_fg_perc',
            'ts': 'true_shooting_perc',
            'three_pct': 'three_perc',
            'reb_total': 'total_reb',
            'turnovers': 'TO_metric',  # Default to TO_metric, but could be TO
            'to_metric': 'TO_metric',  # Allow lowercase version
        }
        internal_stat_name = stat_name_map.get(stat_name, stat_name)
        
        # Special handling for wins (count wins, not average)
        if internal_stat_name == 'wins':
            wins = 0
            for game in games:
                is_home = game.get('homeTeam', {}).get('name') == team
                home_won = game.get('homeWon', False)
                if (is_home and home_won) or (not is_home and not home_won):
                    wins += 1
            if calc_weight == 'raw':
                return float(wins)
            else:  # 'avg' - wins per game (win percentage)
                return float(wins) / len(games) if games else 0.0
        
        # Determine if this is a rate stat
        rate_stats = {
            'effective_fg_perc', 'true_shooting_perc', 'three_perc',
            'off_rtg', 'def_rtg', 'assists_ratio', 'TO_metric', 'ast_to_ratio'
        }
        # Opponent stats are also rate stats that need aggregation
        opponent_stats = {
            'opp_effective_fg_perc', 'opp_true_shooting_perc', 'opp_three_perc',
            'opp_assists_ratio', 'opp_points'
        }
        is_rate_stat = internal_stat_name in rate_stats or internal_stat_name in opponent_stats
        
        # Calculate based on calc_weight
        if calc_weight == 'raw':
            if is_rate_stat:
                # For rate stats with 'raw', aggregate first then calculate
                return self._compute_derived_stat_from_aggregate(internal_stat_name, games, team) or 0.0
            else:
                # For basic stats with 'raw', sum totals
                total = 0.0
                for game in games:
                    if game['homeTeam']['name'] == team:
                        team_data = game['homeTeam']
                    elif game['awayTeam']['name'] == team:
                        team_data = game['awayTeam']
                    else:
                        continue
                    value = team_data.get(internal_stat_name, 0)
                    if value is not None:
                        total += value
                return total
        else:  # calc_weight == 'avg'
            if is_rate_stat:
                # For rate stats with 'avg', calculate per-game then average
                # BUT: Some rate stats (off_rtg, def_rtg, assists_ratio) require aggregation
                # and cannot be calculated per-game. For these, we aggregate first then calculate.
                # Opponent stats also require aggregation since they need team_against_agg.
                aggregation_required_stats = {
                    'off_rtg', 'def_rtg', 'assists_ratio',
                    'opp_effective_fg_perc', 'opp_true_shooting_perc', 'opp_three_perc',
                    'opp_assists_ratio', 'opp_points'
                }
                if internal_stat_name in aggregation_required_stats:
                    # These stats require aggregation - calculate from aggregate
                    computed = self._compute_derived_stat_from_aggregate(internal_stat_name, games, team)
                    return computed if computed is not None else 0.0
                
                # For other rate stats, calculate per-game then average
                values = []
                dates = []
                for game in games:
                    if game['homeTeam']['name'] == team:
                        team_data = game['homeTeam']
                    elif game['awayTeam']['name'] == team:
                        team_data = game['awayTeam']
                    else:
                        continue
                    computed = self._compute_derived_stat(internal_stat_name, team_data, game)
                    if computed is not None:
                        values.append(computed)
                        dates.append(game['date'])
                if values:
                    if self.use_exponential_weighting:
                        return self.weighted_avg(values, dates, reference_date)
                    else:
                        return self.avg(values)
                return 0.0
            else:
                # For basic stats with 'avg', average per-game values
                values = []
                dates = []
                for game in games:
                    if game['homeTeam']['name'] == team:
                        team_data = game['homeTeam']
                    elif game['awayTeam']['name'] == team:
                        team_data = game['awayTeam']
                    else:
                        continue
                    value = team_data.get(internal_stat_name, 0)
                    if value is not None:
                        values.append(value)
                        dates.append(game['date'])
                if values:
                    if self.use_exponential_weighting:
                        return self.weighted_avg(values, dates, reference_date)
                    else:
                        return self.avg(values)
                return 0.0
    
    def _get_games_for_time_period(
        self,
        team: str,
        season: str,
        year: int,
        month: int,
        day: int,
        time_period: str
    ) -> list:
        """
        Get games for a team based on time period.
        
        Args:
            team: Team name
            season: Season string
            year, month, day: Game date
            time_period: 'season', 'months_N', 'games_N', 'days_N', or 'none'
            
        Returns:
            List of game documents
        """
        if time_period == 'season':
            return self.get_team_games_before_date(team, year, month, day, season)
        elif time_period.startswith('months_'):
            n_months = int(time_period.replace('months_', ''))
            return self._get_team_games_last_n_months(team, year, month, day, season, n_months)
        elif time_period.startswith('games_'):
            n_games = int(time_period.replace('games_', ''))
            all_games = self.get_team_games_before_date(team, year, month, day, season)
            return all_games[-n_games:] if len(all_games) >= n_games else all_games
        elif time_period.startswith('days_'):
            n_days = int(time_period.replace('days_', ''))
            return self._get_team_games_last_n_days(team, year, month, day, season, n_days)
        else:  # 'none' or unknown
            return []
    
    def _calculate_net_feature(
        self,
        base_stat_name: str,
        time_period: str,
        calc_weight: str,
        perspective: str,
        is_side: bool,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int
    ) -> float:
        """
        Calculate a net feature (team_stat - team_allowed_stat).
        
        Args:
            base_stat_name: Base stat name without '_net' (e.g., 'points', 'efg')
            time_period, calc_weight, perspective, is_side: Feature components
            home_team, away_team, season, year, month, day: Game context
            
        Returns:
            Net feature value
        """
        reference_date = date(year, month, day)
        
        # Get games
        home_games = self._get_games_for_time_period(home_team, season, year, month, day, time_period)
        away_games = self._get_games_for_time_period(away_team, season, year, month, day, time_period)
        
        # Filter to side-specific games if needed
        if is_side:
            home_games = [g for g in home_games if g.get('homeTeam', {}).get('name') == home_team]
            away_games = [g for g in away_games if g.get('awayTeam', {}).get('name') == away_team]
        
        # Map base stat to team stat and opponent defensive stat
        net_stat_map = {
            'efg': ('effective_fg_perc', 'opp_effective_fg_perc'),
            'ts': ('true_shooting_perc', 'opp_true_shooting_perc'),
            'three_pct': ('three_perc', 'opp_three_perc'),
            'off_rtg': ('off_rtg', 'def_rtg'),  # team's off_rtg - opponent's def_rtg
            'def_rtg': ('def_rtg', 'off_rtg'),  # team's def_rtg - opponent's off_rtg
            'assists_ratio': ('assists_ratio', 'opp_assists_ratio'),
            'points': ('points', 'opp_points'),
        }
        
        if base_stat_name not in net_stat_map:
            return 0.0
        
        team_stat_name, opp_def_stat_name = net_stat_map[base_stat_name]
        
        # Calculate home team net
        home_team_stat = self._calculate_team_stat(team_stat_name, home_team, home_games, calc_weight, reference_date)
        home_opp_stat = self._calculate_team_stat(opp_def_stat_name, home_team, home_games, calc_weight, reference_date)
        home_net = home_team_stat - home_opp_stat
        
        # Calculate away team net
        away_team_stat = self._calculate_team_stat(team_stat_name, away_team, away_games, calc_weight, reference_date)
        away_opp_stat = self._calculate_team_stat(opp_def_stat_name, away_team, away_games, calc_weight, reference_date)
        away_net = away_team_stat - away_opp_stat
        
        # Return based on perspective
        if perspective == 'home':
            return home_net
        elif perspective == 'away':
            return away_net
        else:  # 'diff'
            return home_net - away_net
    
    def _calculate_blend_feature(
        self,
        base_stat_name: str,
        time_period: str,
        calc_weight: str,
        perspective: str,
        is_side: bool,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int
    ) -> float:
        """
        Calculate a blend feature (weighted combination of multiple time periods).

        Format: blend:season:0.75/games_12:0.25

        Args:
            base_stat_name: Base stat name without '_blend' (e.g., 'points_net', 'off_rtg_net', 'efg_net', 'wins')
            time_period: Time period string (e.g., 'blend:season:0.75/games_12:0.25')
            calc_weight: Calculation weight ('avg', 'raw', etc.)
            perspective: 'home', 'away', or 'diff'
            is_side: Whether this is a side-split feature
            home_team, away_team, season, year, month, day: Game context

        Returns:
            Blend feature value
        """
        # Parse blend components from time_period
        blend_components = {}

        if not time_period.startswith('blend:'):
            print(f"Warning: Invalid blend format '{time_period}'. Expected 'blend:period:weight/period:weight'. Returning 0.0")
            return 0.0

        # Format: blend:season:0.75/games_12:0.25
        blend_spec = time_period[6:]  # Remove 'blend:' prefix
        parts = blend_spec.split('/')

        for part in parts:
            if ':' not in part:
                continue
            tp, weight_str = part.split(':', 1)
            try:
                weight = float(weight_str)
                blend_components[tp] = weight
            except ValueError:
                continue

        # Validate weights sum to 1.0 (allow small floating point errors)
        total_weight = sum(blend_components.values())
        if abs(total_weight - 1.0) > 0.01:
            # Normalize weights if they don't sum to 1.0
            if total_weight > 0:
                blend_components = {k: v / total_weight for k, v in blend_components.items()}
        
        if not blend_components:
            return 0.0
        
        # Determine if this is a net feature
        is_net = base_stat_name.endswith('_net')
        
        # Map base_stat_name to the actual stat name for net features
        if is_net:
            # For net features, map to the base stat name (without _net)
            if base_stat_name == 'points_net':
                net_base_stat = 'points'
            elif base_stat_name == 'off_rtg_net':
                net_base_stat = 'off_rtg'
            elif base_stat_name == 'efg_net':
                net_base_stat = 'efg'
            else:
                net_base_stat = base_stat_name.replace('_net', '')
        else:
            net_base_stat = None
        
        # Use calc_weight from parameter, or default to 'avg' if not specified
        if not calc_weight or calc_weight == 'none':
            # Determine default calc_weight based on base_stat_name
            if base_stat_name in ['points_net', 'wins']:
                calc_weight = 'avg'
            elif base_stat_name in ['off_rtg_net', 'efg_net']:
                calc_weight = 'raw'
            else:
                calc_weight = 'avg'
        
        # Calculate weighted blend from all components
        blend_value = 0.0
        for time_period_component, weight in blend_components.items():
            if is_net:
                component_value = self._calculate_net_feature(
                    net_base_stat, time_period_component, calc_weight, perspective, is_side,
                    home_team, away_team, season, year, month, day
                )
            else:
                component_value = self._calculate_regular_feature(
                    base_stat_name, time_period_component, calc_weight, perspective, is_side,
                    home_team, away_team, season, year, month, day
                )
            blend_value += weight * component_value
        
        return blend_value
    
    def _calculate_enhanced_feature(
        self,
        feature_name: str,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int
    ) -> float:
        """
        Calculate an enhanced feature directly from its new-format name.
        No old-format feature names are used - everything is calculated directly.
        
        Args:
            feature_name: Full feature name in new format (e.g., 'pace|season|avg|diff')
            home_team, away_team, season, year, month, day: Game context
            
        Returns:
            Feature value
        """
        components = parse_feature_name(feature_name)
        if not components:
            return 0.0
        
        stat_name = components.stat_name
        time_period = components.time_period
        calc_weight = components.calc_weight
        perspective = components.home_away_diff
        reference_date = date(year, month, day)
        
        # Calculate games_played features
        if stat_name == 'games_played':
            if time_period == 'season':
                home_games = self.get_team_games_before_date(home_team, year, month, day, season)
                away_games = self.get_team_games_before_date(away_team, year, month, day, season)
                home_value = float(len(home_games))
                away_value = float(len(away_games))
            elif time_period.startswith('days_'):
                n_days = int(time_period.replace('days_', ''))
                home_games = self._get_team_games_last_n_days(home_team, year, month, day, season, n_days)
                away_games = self._get_team_games_last_n_days(away_team, year, month, day, season, n_days)
                home_value = float(len(home_games))
                away_value = float(len(away_games))
            else:
                return 0.0
            
            if perspective == 'home':
                return home_value
            elif perspective == 'away':
                return away_value
            else:  # 'diff'
                return home_value - away_value
        
        # Calculate points std (volatility)
        elif stat_name == 'points' and calc_weight == 'std':
            if time_period == 'season':
                home_games = self.get_team_games_before_date(home_team, year, month, day, season)
                away_games = self.get_team_games_before_date(away_team, year, month, day, season)
            else:
                return 0.0
            
            # Extract points for each game
            home_points = []
            for game in home_games:
                if game['homeTeam']['name'] == home_team:
                    home_points.append(game['homeTeam'].get('points', 0))
                elif game['awayTeam']['name'] == home_team:
                    home_points.append(game['awayTeam'].get('points', 0))
            
            away_points = []
            for game in away_games:
                if game['homeTeam']['name'] == away_team:
                    away_points.append(game['homeTeam'].get('points', 0))
                elif game['awayTeam']['name'] == away_team:
                    away_points.append(game['awayTeam'].get('points', 0))
            
            home_std = self.std(home_points) if home_points else 0.0
            away_std = self.std(away_points) if away_points else 0.0
            
            if perspective == 'home':
                return home_std
            elif perspective == 'away':
                return away_std
            else:  # 'diff'
                return home_std - away_std
        
        # Calculate pace features
        elif stat_name == 'pace':
            if time_period == 'season':
                home_games = self.get_team_games_before_date(home_team, year, month, day, season)
                away_games = self.get_team_games_before_date(away_team, year, month, day, season)
            else:
                return 0.0
            
            home_pace = self._calculate_pace(home_team, home_games)
            away_pace = self._calculate_pace(away_team, away_games)
            
            if perspective == 'home':
                return home_pace
            elif perspective == 'away':
                return away_pace
            else:  # 'diff'
                return home_pace - away_pace
        
        # Calculate b2b (back-to-back) features
        elif stat_name == 'b2b':
            # b2b is a binary feature (1 if playing b2b, 0 if not)
            # time_period should be 'none' for b2b
            home_schedule = self.get_schedule_context(home_team, year, month, day, season)
            away_schedule = self.get_schedule_context(away_team, year, month, day, season)
            
            home_b2b = 1.0 if home_schedule['is_b2b'] else 0.0
            away_b2b = 1.0 if away_schedule['is_b2b'] else 0.0
            
            if perspective == 'home':
                return home_b2b
            elif perspective == 'away':
                return away_b2b
            else:  # 'diff'
                return home_b2b - away_b2b
        
        # Calculate travel features
        elif stat_name == 'travel':
            if time_period.startswith('days_'):
                n_days = int(time_period.replace('days_', ''))
                home_travel = self._calculate_travel_distance(home_team, year, month, day, season, n_days)
                away_travel = self._calculate_travel_distance(away_team, year, month, day, season, n_days)
                
                if perspective == 'home':
                    return home_travel
                elif perspective == 'away':
                    return away_travel
                else:  # 'diff'
                    return home_travel - away_travel
        
        return 0.0
    
    def _calculate_special_feature(
        self,
        feature_name: str,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int,
        per_calculator=None
    ) -> float:
        """
        Calculate special features (elo, rest, per_available).
        
        Args:
            feature_name: Full feature name
            home_team, away_team, season, year, month, day: Game context
            per_calculator: Optional PERCalculator instance
            
        Returns:
            Feature value
        """
        components = parse_feature_name(feature_name)
        if not components:
            return 0.0
        
        stat_name = components.stat_name
        perspective = components.home_away_diff
        
        if stat_name == 'elo':
            # Elo is handled separately in NBAModel
            # For now, return 0.0 - this will be calculated in NBAModel
            return 0.0
        elif stat_name == 'rest':
            # Rest is handled separately in NBAModel
            # For now, return 0.0 - this will be calculated in NBAModel
            return 0.0
        elif stat_name == 'per_available':
            # PER available flag - handled separately
            return 0.0
        
        return 0.0
    
    def _calculate_per_feature(
        self,
        feature_name: str,
        home_team: str,
        away_team: str,
        season: str,
        year: int,
        month: int,
        day: int,
        per_calculator=None
    ) -> float:
        """
        Calculate PER features.
        
        Args:
            feature_name: Full feature name (e.g., 'player_team_per|season|avg|diff')
            home_team, away_team, season, year, month, day: Game context
            per_calculator: PERCalculator instance
            
        Returns:
            Feature value
        """
        # PER features are handled separately in NBAModel via _get_per_features
        # For now, return 0.0 - this will be calculated in NBAModel
        return 0.0
    
    # =========================================================================
    # INJURY FEATURE CALCULATIONS
    # =========================================================================
    
    def get_injury_features(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int,
        month: int,
        day: int,
        game_doc: dict = None,
        per_calculator = None,
        recency_decay_k: float = 15.0
    ) -> dict:
        """
        Calculate injury impact features for a game.
        
        Args:
            HOME: Home team name
            AWAY: Away team name
            season: Season string
            year, month, day: Game date
            game_doc: Optional game document (if None, will query)
            per_calculator: Optional PERCalculator instance
            recency_decay_k: Decay constant for recency weighting (default 15)
        
        Returns:
            Dict with injury features (home/away/diff)
        """
        if self.db is None:
            return {}
        
        # Ensure recency_decay_k has a default value if None
        if recency_decay_k is None:
            recency_decay_k = 15.0
        
        game_date = f"{year}-{month:02d}-{day:02d}"
        game_date_obj = date(year, month, day)
        
        # Get game document if not provided
        if game_doc is None:
            game_doc = self.db.stats_nba.find_one({
                'homeTeam.name': HOME,
                'awayTeam.name': AWAY,
                'season': season,
                'date': game_date
            })
        
        if not game_doc:
            return {}
        
        # Priority 1: Use injured_players from game_doc (for training data - historical injury data)
        home_injured_ids = game_doc.get('homeTeam', {}).get('injured_players', [])
        away_injured_ids = game_doc.get('awayTeam', {}).get('injured_players', [])
        
        # Convert to strings for queries
        home_injured_ids = [str(pid) for pid in home_injured_ids] if home_injured_ids else []
        away_injured_ids = [str(pid) for pid in away_injured_ids] if away_injured_ids else []
        
        # Priority 2: If injured_players is not present, use nba_rosters to check injured status (for prediction)
        # This happens when game_doc doesn't have injured_players populated (e.g., future games)
        if not home_injured_ids and not away_injured_ids:
            # Get player lists from stats_nba for each team
            home_player_ids = game_doc.get('homeTeam', {}).get('players', [])
            away_player_ids = game_doc.get('awayTeam', {}).get('players', [])
            
            # Convert to strings for queries
            home_player_ids = [str(pid) for pid in home_player_ids] if home_player_ids else []
            away_player_ids = [str(pid) for pid in away_player_ids] if away_player_ids else []
            
            if self.db is not None:
                try:
                    # Get home team roster
                    home_roster_doc = self.db.nba_rosters.find_one({'season': season, 'team': HOME})
                    if home_roster_doc:
                        home_roster = home_roster_doc.get('roster', [])
                        # Build a map of player_id -> injured status
                        home_roster_map = {str(entry.get('player_id')): entry.get('injured', False) for entry in home_roster}
                        # Find injured players from the players list
                        home_injured_ids = [pid for pid in home_player_ids if home_roster_map.get(pid, False)]
                    
                    # Get away team roster
                    away_roster_doc = self.db.nba_rosters.find_one({'season': season, 'team': AWAY})
                    if away_roster_doc:
                        away_roster = away_roster_doc.get('roster', [])
                        # Build a map of player_id -> injured status
                        away_roster_map = {str(entry.get('player_id')): entry.get('injured', False) for entry in away_roster}
                        # Find injured players from the players list
                        away_injured_ids = [pid for pid in away_player_ids if away_roster_map.get(pid, False)]
                except Exception as e:
                    # If we can't get rosters, fall back to empty lists (injury features will be 0)
                    pass
        
        # Get player names for injured players
        home_injured_names = []
        away_injured_names = []
        if self.db is not None:
            try:
                # Get home team injured player names
                if home_injured_ids:
                    home_player_docs = list(self.db.players_nba.find(
                        {'player_id': {'$in': home_injured_ids}},
                        {'player_id': 1, 'player_name': 1}
                    ))
                    home_injured_names = [doc.get('player_name', 'Unknown') for doc in home_player_docs]
                
                # Get away team injured player names
                if away_injured_ids:
                    away_player_docs = list(self.db.players_nba.find(
                        {'player_id': {'$in': away_injured_ids}},
                        {'player_id': 1, 'player_name': 1}
                    ))
                    away_injured_names = [doc.get('player_name', 'Unknown') for doc in away_player_docs]
            except Exception as e:
                # Silently fail if we can't get player names - features still work
                pass
        
        # Calculate features for each team
        home_features = self._calculate_team_injury_features(
            HOME, season, game_date, game_date_obj, home_injured_ids, per_calculator, recency_decay_k
        )
        away_features = self._calculate_team_injury_features(
            AWAY, season, game_date, game_date_obj, away_injured_ids, per_calculator, recency_decay_k
        )
        
        # Build result dict - only new format features
        features = {}
        
        # Get values directly from home/away features
        home_inj_per_value = home_features.get('injPerValue', 0.0)
        away_inj_per_value = away_features.get('injPerValue', 0.0)
        home_inj_top1_per = home_features.get('injTop1Per', 0.0)
        away_inj_top1_per = away_features.get('injTop1Per', 0.0)
        home_inj_top3_sum = home_features.get('injTop3PerSum', 0.0)
        away_inj_top3_sum = away_features.get('injTop3PerSum', 0.0)
        home_inj_min_lost = home_features.get('injMinLost', 0.0)
        away_inj_min_lost = away_features.get('injMinLost', 0.0)
        home_injury_severity = home_features.get('injurySeverity', 0.0)
        away_injury_severity = away_features.get('injurySeverity', 0.0)
        home_inj_rotation = home_features.get('injRotation', 0.0)
        away_inj_rotation = away_features.get('injRotation', 0.0)
        
        # New format features
        # inj_per features
        features['inj_per|none|weighted_MIN|home'] = home_inj_per_value
        features['inj_per|none|weighted_MIN|away'] = away_inj_per_value
        features['inj_per|none|weighted_MIN|diff'] = home_inj_per_value - away_inj_per_value
        
        features['inj_per|none|top1_avg|home'] = home_inj_top1_per
        features['inj_per|none|top1_avg|away'] = away_inj_top1_per
        features['inj_per|none|top1_avg|diff'] = home_inj_top1_per - away_inj_top1_per
        
        features['inj_per|none|top3_sum|home'] = home_inj_top3_sum
        features['inj_per|none|top3_sum|away'] = away_inj_top3_sum
        features['inj_per|none|top3_sum|diff'] = home_inj_top3_sum - away_inj_top3_sum
        
        # inj_min_lost features
        features['inj_min_lost|none|raw|home'] = home_inj_min_lost
        features['inj_min_lost|none|raw|away'] = away_inj_min_lost
        features['inj_min_lost|none|raw|diff'] = home_inj_min_lost - away_inj_min_lost
        
        # inj_severity features
        features['inj_severity|none|raw|home'] = home_injury_severity
        features['inj_severity|none|raw|away'] = away_injury_severity
        features['inj_severity|none|raw|diff'] = home_injury_severity - away_injury_severity
        
        # Player lists for injury features (for display in feature modal)
        features['_player_lists'] = {
            # injPerValue (weighted PER)
            'inj_per|none|weighted_MIN|home': home_features.get('injPerValue_players', []),
            'inj_per|none|weighted_MIN|away': away_features.get('injPerValue_players', []),
            # injTop1Per (top 1 PER)
            'inj_per|none|top1_avg|home': home_features.get('injTop1Per_players', []),
            'inj_per|none|top1_avg|away': away_features.get('injTop1Per_players', []),
            # injTop3PerSum (top 3 PER sum)
            'inj_per|none|top3_sum|home': home_features.get('injTop3PerSum_players', []),
            'inj_per|none|top3_sum|away': away_features.get('injTop3PerSum_players', []),
            # injMinLost (minutes lost)
            'inj_min_lost|none|raw|home': home_features.get('injMinLost_players', []),
            'inj_min_lost|none|raw|away': away_features.get('injMinLost_players', []),
            # injRotation (rotation count - uses same players as injMinLost)
            'inj_rotation_per|none|raw|home': home_features.get('injRotation_players', []),
            'inj_rotation_per|none|raw|away': away_features.get('injRotation_players', [])
        }
        
        # inj_rotation_per features
        features['inj_rotation_per|none|raw|home'] = home_inj_rotation
        features['inj_rotation_per|none|raw|away'] = away_inj_rotation
        features['inj_rotation_per|none|raw|diff'] = home_inj_rotation - away_inj_rotation
        
        # Injury blend feature: weighted combination of injury metrics
        # Formula: 0.45 * injurySeverity + 0.35 * injTop1Per + 0.20 * injRotation
        # New notation: inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|{perspective}
        blend_weight_severity = 0.45
        blend_weight_top1_per = 0.35
        blend_weight_rotation = 0.20
        
        # Home version
        features['inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home'] = (
            blend_weight_severity * home_injury_severity +
            blend_weight_top1_per * home_inj_top1_per +
            blend_weight_rotation * home_inj_rotation
        )
        
        # Away version
        features['inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away'] = (
            blend_weight_severity * away_injury_severity +
            blend_weight_top1_per * away_inj_top1_per +
            blend_weight_rotation * away_inj_rotation
        )
        
        # Diff version
        features['inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff'] = (
            blend_weight_severity * (home_injury_severity - away_injury_severity) +
            blend_weight_top1_per * (home_inj_top1_per - away_inj_top1_per) +
            blend_weight_rotation * (home_inj_rotation - away_inj_rotation)
        )

        # Add injured player names (for display in UI)
        features['home_injured_players'] = home_injured_names
        features['away_injured_players'] = away_injured_names
        
        return features
    
    def _calculate_team_injury_features(
        self,
        team: str,
        season: str,
        game_date: str,
        game_date_obj: date,
        injured_player_ids: list,
        per_calculator,
        recency_decay_k: float
    ) -> dict:
        """
        Calculate injury features for a single team.
        
        Returns:
            Dict with: injPerValue, injTop1Per, injMinLost, injurySeverity, injRotation
        """
        if not injured_player_ids:
            return {
                'injPerValue': 0.0,
                'injTop1Per': 0.0,
                'injTop3PerSum': 0.0,
                'injMinLost': 0.0,
                'injurySeverity': 0.0,
                'injRotation': 0.0,
                # Player lists for each feature
                'injPerValue_players': [],
                'injTop1Per_players': [],
                'injTop3PerSum_players': [],
                'injMinLost_players': [],
                'injRotation_players': []
            }
        
        # Get player stats (season-to-date, up to but not including game_date)
        player_stats = self._get_player_season_stats(team, season, game_date, injured_player_ids)
        
        if not player_stats:
            return {
                'injPerValue': 0.0,
                'injTop1Per': 0.0,
                'injTop3PerSum': 0.0,
                'injMinLost': 0.0,
                'injurySeverity': 0.0,
                'injRotation': 0.0,
                # Player lists for each feature
                'injPerValue_players': [],
                'injTop1Per_players': [],
                'injTop3PerSum_players': [],
                'injMinLost_players': [],
                'injRotation_players': []
            }
        
        # Filter: only include players whose last game was for this team
        valid_players = []
        for player_id, stats in player_stats.items():
            last_game_team = stats.get('last_game_team')
            if last_game_team == team:
                valid_players.append((player_id, stats))
        
        if not valid_players:
            return {
                'injPerValue': 0.0,
                'injTop1Per': 0.0,
                'injTop3PerSum': 0.0,
                'injMinLost': 0.0,
                'injurySeverity': 0.0,
                'injRotation': 0.0,
                # Player lists for each feature
                'injPerValue_players': [],
                'injTop1Per_players': [],
                'injTop3PerSum_players': [],
                'injMinLost_players': [],
                'injRotation_players': []
            }
        
        # Get PER values if per_calculator is available
        if per_calculator:
            for player_id, stats in valid_players:
                # Get PER for this player (season-to-date)
                per = per_calculator.get_player_per_before_date(
                    player_id, team, season, game_date
                )
                stats['per'] = per if per else 0.0
        
        # Get max MPG on team (for normalization)
        max_mpg = self._get_max_mpg_on_team(team, season, game_date)
        if max_mpg == 0:
            max_mpg = 1.0  # Avoid division by zero
        
        # Calculate rotation players (mpg >= 10)
        rotation_players = [(pid, stats) for pid, stats in valid_players if stats.get('mpg', 0) >= 10]
        
        # Calculate teamRotationMPG (sum of MPG for all rotation players on team)
        team_rotation_mpg = self._get_team_rotation_mpg(team, season, game_date)
        
        # Get player names for injured players
        player_names = {}
        if self.db is not None:
            try:
                player_id_list = [str(pid) for pid, _ in valid_players]
                if player_id_list:
                    player_docs = list(self.db.players_nba.find(
                        {'player_id': {'$in': player_id_list}},
                        {'player_id': 1, 'player_name': 1}
                    ))
                    player_names = {str(doc['player_id']): doc.get('player_name', 'Unknown') for doc in player_docs}
            except Exception:
                pass
        
        # 1. injPerValue: Weighted average of injured players' PERs
        inj_per_values = []
        inj_per_value_players = []
        for player_id, stats in valid_players:
            per = stats.get('per', 0.0)
            mpg = stats.get('mpg', 0.0)
            last_played_date = stats.get('last_played_date')
            
            if per == 0.0 or mpg == 0.0 or last_played_date is None:
                continue
            
            # MPG weight (normalized 0-1)
            mpg_weight = mpg / max_mpg
            
            # Recency weight
            days_since = (game_date_obj - last_played_date).days
            recency_weight = math.exp(-days_since / recency_decay_k)
            
            # Weighted PER contribution
            weighted_per = per * mpg_weight * recency_weight
            inj_per_values.append(weighted_per)
            
            # Add to player list
            inj_per_value_players.append({
                'player_id': str(player_id),
                'player_name': player_names.get(str(player_id), 'Unknown'),
                'per': per,
                'mpg': mpg,
                'weighted_per': weighted_per
            })
        
        inj_per_value = sum(inj_per_values) if inj_per_values else 0.0
        
        # 2. injTop1Per: Highest injured player PER
        injured_pers_with_players = [(stats.get('per', 0.0), player_id, stats) for player_id, stats in valid_players if stats.get('per', 0.0) > 0]
        injured_pers = [per for per, _, _ in injured_pers_with_players]
        inj_top1_per = max(injured_pers) if injured_pers else 0.0
        
        # Find top 1 player
        inj_top1_per_players = []
        if injured_pers_with_players:
            top1_player = max(injured_pers_with_players, key=lambda x: x[0])
            inj_top1_per_players.append({
                'player_id': str(top1_player[1]),
                'player_name': player_names.get(str(top1_player[1]), 'Unknown'),
                'per': top1_player[0],
                'mpg': top1_player[2].get('mpg', 0.0)
            })
        
        # 2b. injTop3PerSum: Sum of top 3 injured player PERs
        inj_top3_per_sum_players = []
        if injured_pers_with_players:
            sorted_pers_with_players = sorted(injured_pers_with_players, key=lambda x: x[0], reverse=True)
            inj_top3_per_sum = sum([per for per, _, _ in sorted_pers_with_players[:3]])
            # Get top 3 players
            for per, player_id, stats in sorted_pers_with_players[:3]:
                inj_top3_per_sum_players.append({
                    'player_id': str(player_id),
                    'player_name': player_names.get(str(player_id), 'Unknown'),
                    'per': per,
                    'mpg': stats.get('mpg', 0.0)
                })
        else:
            inj_top3_per_sum = 0.0
        
        # 3. injMinLost: Sum of MPG for injured rotation players
        inj_min_lost = sum(stats.get('mpg', 0.0) for _, stats in rotation_players)
        inj_min_lost_players = [{
            'player_id': str(player_id),
            'player_name': player_names.get(str(player_id), 'Unknown'),
            'mpg': stats.get('mpg', 0.0),
            'per': stats.get('per', 0.0)
        } for player_id, stats in rotation_players]
        
        # 4. injurySeverity: injMinLost / teamRotationMPG (uses same players as injMinLost)
        injury_severity = inj_min_lost / team_rotation_mpg if team_rotation_mpg > 0 else 0.0
        
        # 5. injRotation: Count of injured rotation players (uses same players as injMinLost)
        inj_rotation = len(rotation_players)
        inj_rotation_players = [{
            'player_id': str(player_id),
            'player_name': player_names.get(str(player_id), 'Unknown'),
            'mpg': stats.get('mpg', 0.0),
            'per': stats.get('per', 0.0)
        } for player_id, stats in rotation_players]
        
        return {
            'injPerValue': inj_per_value,
            'injTop1Per': inj_top1_per,
            'injTop3PerSum': inj_top3_per_sum,
            'injMinLost': inj_min_lost,
            'injurySeverity': injury_severity,
            'injRotation': float(inj_rotation),
            # Player lists for each feature
            'injPerValue_players': inj_per_value_players,
            'injTop1Per_players': inj_top1_per_players,
            'injTop3PerSum_players': inj_top3_per_sum_players,
            'injMinLost_players': inj_min_lost_players,
            'injRotation_players': inj_rotation_players
        }
    
    def _get_player_season_stats(
        self,
        team: str,
        season: str,
        before_date: str,
        player_ids: list
    ) -> dict:
        """
        Get season-to-date stats for players (MPG, last game date/team).
        Only includes games where stats.min > 0.
        
        Returns:
            Dict mapping player_id -> {
                'mpg': float,
                'per': float (will be 0, filled by caller),
                'last_played_date': date,
                'last_game_team': str
            }
        """
        if not player_ids:
            return {}
        
        # Convert player_ids to set for fast lookup
        player_ids_set = set(str(pid) for pid in player_ids)
        
        # Check cache first
        cache_key = (team, season, before_date)
        if cache_key in self._injury_player_stats_cache:
            # Return cached stats, but filter to only requested player_ids
            cached_stats = self._injury_player_stats_cache[cache_key]
            return {pid: cached_stats[pid] for pid in player_ids_set if pid in cached_stats}
        
        # Use preloaded data if available, otherwise query DB
        # Note: We query ALL players on the team (not just requested ones) to maximize cache reuse
        if self._injury_cache_loaded and (team, season) in self._injury_preloaded_players:
            # Filter preloaded records in memory (all players, not just requested ones)
            player_records = [
                r for r in self._injury_preloaded_players[(team, season)]
                if r.get('date', '') < before_date
            ]
        else:
            # Fallback to DB query - query ALL players on team, not just requested ones
            # This allows cache reuse for different player_id lists
            player_records = list(self.db.stats_nba_players.find(
                {
                    'team': team,
                    'season': season,
                    'date': {'$lt': before_date},
                    'stats.min': {'$gt': 0}  # Only games where player actually played
                },
                {
                    'player_id': 1,
                    'team': 1,
                    'date': 1,
                    'stats.min': 1
                }
            ).sort('date', 1))  # Sort by date ascending
        
        if not player_records:
            # Cache empty result
            self._injury_player_stats_cache[cache_key] = {}
            return {}
        
        # Aggregate by player
        player_agg = defaultdict(lambda: {
            'total_minutes': 0.0,
            'games_played': 0,
            'last_played_date': None,
            'last_game_team': None
        })
        
        for record in player_records:
            player_id = str(record.get('player_id'))
            game_date_str = record.get('date')
            minutes = record.get('stats', {}).get('min', 0.0)
            
            if minutes > 0:
                player_agg[player_id]['total_minutes'] += minutes
                player_agg[player_id]['games_played'] += 1
                
                # Track last game
                game_date = datetime.strptime(game_date_str, '%Y-%m-%d').date()
                if (player_agg[player_id]['last_played_date'] is None or 
                    game_date > player_agg[player_id]['last_played_date']):
                    player_agg[player_id]['last_played_date'] = game_date
                    player_agg[player_id]['last_game_team'] = record.get('team')
        
        # Calculate MPG
        result = {}
        for player_id, agg in player_agg.items():
            if agg['games_played'] == 0:
                continue
            
            mpg = agg['total_minutes'] / agg['games_played']
            
            result[player_id] = {
                'mpg': mpg,
                'per': 0.0,  # Will be filled by caller if per_calculator provided
                'last_played_date': agg['last_played_date'],
                'last_game_team': agg['last_game_team']
            }
        
        # Cache the full result (for all players on team, not just requested ones)
        # This allows reuse for other player_id lists
        self._injury_player_stats_cache[cache_key] = result
        
        # Return only requested players
        return {pid: result[pid] for pid in player_ids_set if pid in result}
    
    def _get_max_mpg_on_team(
        self,
        team: str,
        season: str,
        before_date: str
    ) -> float:
        """
        Get maximum MPG among all players on the team (season-to-date).
        """
        # Check cache first
        cache_key = (team, season, before_date)
        if cache_key in self._injury_max_mpg_cache:
            return self._injury_max_mpg_cache[cache_key]
        
        # Use preloaded data if available, otherwise query DB
        if self._injury_cache_loaded and (team, season) in self._injury_preloaded_players:
            # Filter preloaded records in memory
            all_players = [
                r for r in self._injury_preloaded_players[(team, season)]
                if r.get('date', '') < before_date
            ]
        else:
            # Fallback to DB query
            all_players = list(self.db.stats_nba_players.find(
                {
                    'team': team,
                    'season': season,
                    'date': {'$lt': before_date},
                    'stats.min': {'$gt': 0}
                },
                {
                    'player_id': 1,
                    'stats.min': 1
                }
            ))
        
        if not all_players:
            self._injury_max_mpg_cache[cache_key] = 0.0
            return 0.0
        
        # Aggregate by player
        player_mpg = defaultdict(lambda: {'total_min': 0.0, 'games': 0})
        for record in all_players:
            player_id = str(record.get('player_id'))
            minutes = record.get('stats', {}).get('min', 0.0)
            player_mpg[player_id]['total_min'] += minutes
            player_mpg[player_id]['games'] += 1
        
        # Calculate MPG for each player and find max
        max_mpg = 0.0
        for player_id, agg in player_mpg.items():
            if agg['games'] > 0:
                mpg = agg['total_min'] / agg['games']
                max_mpg = max(max_mpg, mpg)
        
        # Cache result
        self._injury_max_mpg_cache[cache_key] = max_mpg
        return max_mpg
    
    def _get_team_rotation_mpg(
        self,
        team: str,
        season: str,
        before_date: str
    ) -> float:
        """
        Get sum of MPG for all rotation players (mpg >= 10) on the team.
        """
        # Check cache first
        cache_key = (team, season, before_date)
        if cache_key in self._injury_rotation_mpg_cache:
            return self._injury_rotation_mpg_cache[cache_key]
        
        # Use preloaded data if available, otherwise query DB
        if self._injury_cache_loaded and (team, season) in self._injury_preloaded_players:
            # Filter preloaded records in memory
            all_players = [
                r for r in self._injury_preloaded_players[(team, season)]
                if r.get('date', '') < before_date
            ]
        else:
            # Fallback to DB query
            all_players = list(self.db.stats_nba_players.find(
                {
                    'team': team,
                    'season': season,
                    'date': {'$lt': before_date},
                    'stats.min': {'$gt': 0}
                },
                {
                    'player_id': 1,
                    'stats.min': 1
                }
            ))
        
        if not all_players:
            self._injury_rotation_mpg_cache[cache_key] = 0.0
            return 0.0
        
        # Aggregate by player
        player_mpg = defaultdict(lambda: {'total_min': 0.0, 'games': 0})
        for record in all_players:
            player_id = str(record.get('player_id'))
            minutes = record.get('stats', {}).get('min', 0.0)
            player_mpg[player_id]['total_min'] += minutes
            player_mpg[player_id]['games'] += 1
        
        # Calculate MPG and sum for rotation players (mpg >= 10)
        total_rotation_mpg = 0.0
        for player_id, agg in player_mpg.items():
            if agg['games'] > 0:
                mpg = agg['total_min'] / agg['games']
                if mpg >= 10.0:
                    total_rotation_mpg += mpg
        
        # Cache result
        self._injury_rotation_mpg_cache[cache_key] = total_rotation_mpg
        return total_rotation_mpg
