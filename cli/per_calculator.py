#!/usr/bin/env python3
"""
PER Calculator - Player Efficiency Rating computation module

Implements Hollinger's PER formula:
1. uPER (unadjusted PER) - raw per-minute efficiency
2. aPER (pace-adjusted PER) - adjusted for team pace
3. PER (normalized) - scaled so league average = 15

Optimizations:
- Preloads stats_nba_players into memory to avoid 27k+ DB queries
- Caches computed PER features per game to MongoDB

Usage:
    from per_calculator import PERCalculator
    
    # With preloading (fast for batch processing)
    calc = PERCalculator(preload=True)
    
    # Without preloading (for single queries)
    calc = PERCalculator(preload=False)
    
    # Get team PER aggregates for game prediction
    features = calc.get_game_per_features(home_team, away_team, season, game_date)
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
import numpy as np

from nba_app.cli.Mongo import Mongo
from nba_app.cli.cache_league_stats import (
    get_season_stats_with_fallback,
    get_league_constants,
    get_team_pace,
    ensure_season_cached
)


# MongoDB collection for cached PER features
CACHED_PER_COLLECTION = 'cached_per_features'


class PERCalculator:
    """
    Calculate Player Efficiency Rating (PER) using Hollinger's formula.
    
    PER measures a player's per-minute productivity, normalized so that
    the league average is always 15.0.
    
    Supports two modes:
    - preload=True: Loads all player stats into memory for fast batch processing
    - preload=False: Queries DB on demand (slower but uses less memory)
    """
    
    def __init__(self, db=None, preload: bool = True):
        """
        Initialize PER Calculator.
        
        Args:
            db: Optional MongoDB database connection. Creates new if None.
            preload: If True, preload stats_nba_players into memory for fast access
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        # Cache for computed values
        self._league_cache = {}
        self._team_pace_cache = {}
        self._player_per_cache = {}  # {(player_id, team, season, before_date): PER_value} - cache computed PER values
        self._league_aper_cache = {}  # {(season, before_date): lg_aper} - cache league average aPER
        
        # Preloaded data caches
        self._player_stats_cache = None  # {(team, season): [player_games sorted by date]}
        self._team_stats_cache = None    # {(team, season): [game_stats sorted by date]}
        self._per_features_cache = {}    # {game_key: features} - in-memory cache
        self._team_players_agg_cache = {}  # {(team, season, before_date): [aggregated player data]} - cache aggregated results
        
        self._preloaded = False
        if preload:
            self._preload_data()
    
    def _preload_data(self):
        """
        Preload stats_nba_players and stats_nba into memory for fast access.
        This converts 27k+ DB queries into a single load + in-memory filtering.
        """
        print("  Preloading player stats into memory...")
        
        # Load all player stats with relevant fields (no sort - do it in Python to avoid MongoDB memory limit)
        player_stats = list(self.db.stats_nba_players.find(
            {'stats.min': {'$gt': 0}},
            {
                'player_id': 1,
                'player_name': 1,
                'game_id': 1,
                'date': 1,
                'season': 1,
                'team': 1,
                'home': 1,
                'starter': 1,
                'stats': 1
            }
        ))
        
        print(f"    Loaded {len(player_stats)} player-game records")
        
        # Sort in Python (faster and avoids MongoDB 32MB sort limit)
        player_stats.sort(key=lambda x: x.get('date', ''))
        
        # Index by (team, season) for fast lookup
        self._player_stats_cache = defaultdict(list)
        for ps in player_stats:
            key = (ps.get('team'), ps.get('season'))
            self._player_stats_cache[key].append(ps)
        
        # #region agent log
        # Debug: Check date format from MongoDB for Trae Young
        trae_records_from_db = [ps for ps in player_stats if ps.get('player_id') == 4277905]
        if trae_records_from_db:
            sample_dates = []
            for ps in trae_records_from_db[:5]:
                date_val = ps.get('date')
                sample_dates.append({
                    'date': str(date_val),
                    'date_type': str(type(date_val)),
                    'team': ps.get('team'),
                    'season': ps.get('season')
                })
            try:
                import os
                debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
                os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
                with open(debug_log_path, 'a') as f:
                    import json
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'C',
                        'location': 'per_calculator.py:117',
                        'message': 'Trae Young records loaded from DB',
                        'data': {
                            'total_trae_records': len(trae_records_from_db),
                            'sample_records': sample_dates
                        },
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass  # Silently ignore debug log errors
        
        # Debug: Check date format sample from all records
        date_format_samples = []
        for ps in player_stats[:10]:
            date_val = ps.get('date')
            date_format_samples.append({
                'date': str(date_val),
                'date_type': str(type(date_val))
            })
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'C',
                    'location': 'per_calculator.py:120',
                    'message': 'Date format samples from MongoDB',
                    'data': {
                        'total_records_loaded': len(player_stats),
                        'date_samples': date_format_samples
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        print(f"    Indexed into {len(self._player_stats_cache)} team-season combinations")
        
        # Load team stats from stats_nba (no sort - do it in Python)
        print("  Preloading team stats into memory...")
        games = list(self.db.stats_nba.find(
            {'homeTeam.points': {'$gt': 0}, 'awayTeam.points': {'$gt': 0}},
            {
                'game_id': 1,
                'date': 1,
                'season': 1,
                'homeTeam': 1,
                'awayTeam': 1
            }
        ))
        
        print(f"    Loaded {len(games)} games")
        
        # Sort in Python (avoids MongoDB 32MB sort limit)
        games.sort(key=lambda x: x.get('date', ''))
        
        # Index by (team, season) for fast lookup
        self._team_stats_cache = defaultdict(list)
        for game in games:
            home_team = game['homeTeam']['name']
            away_team = game['awayTeam']['name']
            season = game.get('season')
            
            self._team_stats_cache[(home_team, season)].append({
                'game_id': game.get('game_id'),
                'date': game['date'],
                'team_data': game['homeTeam'],
                'is_home': True
            })
            self._team_stats_cache[(away_team, season)].append({
                'game_id': game.get('game_id'),
                'date': game['date'],
                'team_data': game['awayTeam'],
                'is_home': False
            })
        
        print(f"    Indexed into {len(self._team_stats_cache)} team-season combinations")
        
        # Load cached PER features from MongoDB
        self._load_per_cache()
        
        self._preloaded = True
        print("  Preloading complete!")
    
    def _load_per_cache(self):
        """Load cached PER features from MongoDB into memory."""
        cached_docs = list(self.db[CACHED_PER_COLLECTION].find({}))
        
        for doc in cached_docs:
            season = doc.get('season')
            game_features = doc.get('game_features', {})
            for game_key, features in game_features.items():
                self._per_features_cache[f"{season}|{game_key}"] = features
        
        print(f"    Loaded {len(self._per_features_cache)} cached PER feature sets")
    
    def _save_per_cache(self, season: str, game_features: dict):
        """Save computed PER features to MongoDB cache."""
        self.db[CACHED_PER_COLLECTION].update_one(
            {'season': season},
            {
                '$set': {
                    'season': season,
                    'game_features': game_features,
                    'game_count': len(game_features),
                    'updated_at': datetime.utcnow()
                }
            },
            upsert=True
        )
    
    # =========================================================================
    # CORE PER FORMULAS
    # =========================================================================
    
    def compute_uper(
        self,
        player_stats: dict,
        team_stats: dict,
        league_constants: dict
    ) -> float:
        """
        Compute unadjusted PER (uPER) for a single player-game.
        
        This is the raw per-minute efficiency rating before pace adjustment
        and league normalization.
        """
        # Extract player stats
        MP = player_stats.get('min', 0)
        if MP == 0:
            return 0
        
        # Player counting stats
        FG = player_stats.get('fg_made', 0)
        FGA = player_stats.get('fg_att', 0)
        THREE = player_stats.get('three_made', 0)
        FT = player_stats.get('ft_made', 0)
        FTA = player_stats.get('ft_att', 0)
        TRB = player_stats.get('reb', 0)
        ORB = player_stats.get('oreb', 0)
        AST = player_stats.get('ast', 0)
        STL = player_stats.get('stl', 0)
        BLK = player_stats.get('blk', 0)
        TOV = player_stats.get('to', 0)
        PF = player_stats.get('pf', 0)
        
        # Team stats
        team_AST = team_stats.get('assists', 1)
        team_FG = team_stats.get('FG_made', 1)
        
        # Avoid division by zero
        if team_FG == 0:
            team_FG = 1
        
        # League constants
        factor = league_constants.get('factor', 0.5)
        VOP = league_constants.get('VOP', 1.0)
        DRB_pct = league_constants.get('DRB_pct', 0.75)
        lg_FT = league_constants.get('lg_FT', 1)
        lg_PF = league_constants.get('lg_PF', 1)
        lg_FTA = league_constants.get('lg_FTA', 1)
        
        # Compute team AST ratio
        team_ast_ratio = team_AST / team_FG
        
        try:
            # Positive contributions
            three_pts = THREE
            ast_term = (2/3) * AST
            fg_term = (2 - factor * team_ast_ratio) * FG
            ft_term = FT * 0.5 * (1 + (1 - team_ast_ratio) + (2/3) * team_ast_ratio)
            
            # Negative contributions
            tov_term = VOP * TOV
            missed_fg_term = VOP * DRB_pct * (FGA - FG)
            missed_ft_term = VOP * 0.44 * (0.44 + (0.56 * DRB_pct)) * (FTA - FT)
            
            # Rebounding
            drb_term = VOP * (1 - DRB_pct) * (TRB - ORB)
            orb_term = VOP * DRB_pct * ORB
            
            # Defense
            stl_term = VOP * STL
            blk_term = VOP * DRB_pct * BLK
            
            # Fouls
            foul_value = (lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP if lg_PF > 0 else 0
            pf_term = PF * foul_value
            
            uper_numerator = (
                three_pts + ast_term + fg_term + ft_term -
                tov_term - missed_fg_term - missed_ft_term +
                drb_term + orb_term + stl_term + blk_term - pf_term
            )
            
            uper = uper_numerator / MP
            
        except (ZeroDivisionError, TypeError):
            uper = 0
        
        return uper
    
    def compute_aper(self, uper: float, team_pace: float, lg_pace: float) -> float:
        """Compute pace-adjusted PER (aPER)."""
        if team_pace == 0:
            return uper
        return uper * (lg_pace / team_pace)
    
    def compute_per(self, aper: float, lg_aper: float) -> float:
        """
        Compute normalized PER from aPER.
        
        Normalizes aPER so that league average = 15.0.
        Formula: PER = aPER * (15 / lg_aPER)
        
        Args:
            aper: Pace-adjusted PER
            lg_aper: League average aPER for the season
            
        Returns:
            Normalized PER (league average = 15.0)
        """
        if lg_aper == 0:
            return aper  # Fallback if league average not available
        return aper * (15.0 / lg_aper)
    
    def compute_league_average_aper(self, season: str, before_date: Optional[str] = None) -> float:
        """
        Compute league average aPER for a season.
        
        Calculates aPER for all players in the league and returns
        the minutes-weighted average.
        
        Uses cache to avoid expensive recomputation for the same season/date.
        
        Args:
            season: Season string
            before_date: Optional date to compute stats before (YYYY-MM-DD)
                        If None, uses all games in season
            
        Returns:
            League average aPER (minutes-weighted)
        """
        logger = logging.getLogger(__name__)
        
        # Check cache first - this is expensive to compute
        cache_key = (season, before_date)
        if cache_key in self._league_aper_cache:
            return self._league_aper_cache[cache_key]
        
        # Get league constants
        league_constants = get_league_constants(season, self.db)
        if not league_constants:
            logger.warning(f"[PER] Cannot compute lg_aPER: no league constants for {season}")
            self._league_aper_cache[cache_key] = 0.0
            return 0.0
        
        lg_pace = league_constants.get('lg_pace', 95)
        
        # Get all player stats for the season
        # Use preloaded data if available (much faster than DB query)
        if self._preloaded and self._player_stats_cache:
            # Collect player games from preloaded cache
            player_games = []
            for (team, season_key), player_list in self._player_stats_cache.items():
                if season_key == season:
                    # Filter by date if before_date is specified
                    if before_date:
                        player_games.extend([pg for pg in player_list if pg.get('date', '') < before_date])
                    else:
                        player_games.extend(player_list)
        else:
            # Fallback to DB query
            query = {
                'season': season,
                'stats.min': {'$gt': 0}
            }
            if before_date:
                query['date'] = {'$lt': before_date}
            
            player_games = list(self.db.stats_nba_players.find(query))
        
        if not player_games:
            logger.warning(f"[PER] No player games found for {season}")
            self._league_aper_cache[cache_key] = 0.0
            return 0.0
        
        # Aggregate by player
        player_agg = defaultdict(lambda: {
            'total_min': 0,
            'total_pts': 0,
            'total_fg_made': 0,
            'total_fg_att': 0,
            'total_three_made': 0,
            'total_ft_made': 0,
            'total_ft_att': 0,
            'total_reb': 0,
            'total_oreb': 0,
            'total_ast': 0,
            'total_stl': 0,
            'total_blk': 0,
            'total_to': 0,
            'total_pf': 0,
            'team': None
        })
        
        team_stats_agg = defaultdict(lambda: {
            'assists': 0,
            'FG_made': 0
        })
        
        for pg in player_games:
            pid = pg['player_id']
            team = pg.get('team')
            stats = pg.get('stats', {})
            
            min_played = stats.get('min', 0)
            if min_played == 0:
                continue
            
            player_agg[pid]['total_min'] += min_played
            player_agg[pid]['total_pts'] += stats.get('pts', 0)
            player_agg[pid]['total_fg_made'] += stats.get('fg_made', 0)
            player_agg[pid]['total_fg_att'] += stats.get('fg_att', 0)
            player_agg[pid]['total_three_made'] += stats.get('three_made', 0)
            player_agg[pid]['total_ft_made'] += stats.get('ft_made', 0)
            player_agg[pid]['total_ft_att'] += stats.get('ft_att', 0)
            player_agg[pid]['total_reb'] += stats.get('reb', 0)
            player_agg[pid]['total_oreb'] += stats.get('oreb', 0)
            player_agg[pid]['total_ast'] += stats.get('ast', 0)
            player_agg[pid]['total_stl'] += stats.get('stl', 0)
            player_agg[pid]['total_blk'] += stats.get('blk', 0)
            player_agg[pid]['total_to'] += stats.get('to', 0)
            player_agg[pid]['total_pf'] += stats.get('pf', 0)
            if not player_agg[pid]['team']:
                player_agg[pid]['team'] = team
            
            # Note: Team stats will be computed per-team when calculating PER
        
        # Calculate aPER for each player and compute weighted average
        total_minutes = 0
        weighted_aper_sum = 0.0
        
        for pid, player in player_agg.items():
            if player['total_min'] == 0:
                continue
            
            team = player['team']
            if not team:
                continue
            
            # Get team stats for PER calculation (aggregated before date if specified)
            if before_date:
                team_stats = self._get_team_stats_before_date_cached(team, season, before_date)
            else:
                # Get full season team stats
                team_stats = self._get_team_stats_before_date_cached(team, season, '9999-12-31')
            
            # Ensure we have valid team stats
            if team_stats['FG_made'] == 0:
                team_stats['FG_made'] = 1  # Avoid division by zero
            
            # Get team pace
            team_pace = get_team_pace(season, team, self.db)
            if team_pace == 0:
                team_pace = lg_pace
            
            # Aggregate stats for PER calculation
            agg_stats = {
                'min': player['total_min'],
                'pts': player['total_pts'],
                'fg_made': player['total_fg_made'],
                'fg_att': player['total_fg_att'],
                'three_made': player['total_three_made'],
                'ft_made': player['total_ft_made'],
                'ft_att': player['total_ft_att'],
                'reb': player['total_reb'],
                'oreb': player['total_oreb'],
                'ast': player['total_ast'],
                'stl': player['total_stl'],
                'blk': player['total_blk'],
                'to': player['total_to'],
                'pf': player['total_pf']
            }
            
            # Compute uPER and aPER
            uper = self.compute_uper(agg_stats, team_stats, league_constants)
            aper = self.compute_aper(uper, team_pace, lg_pace)
            
            # Add to weighted sum
            total_minutes += player['total_min']
            weighted_aper_sum += aper * player['total_min']
        
        # Return minutes-weighted average
        if total_minutes == 0:
            self._league_aper_cache[cache_key] = 0.0
            return 0.0
        
        lg_aper = weighted_aper_sum / total_minutes
        logger.debug(f"[PER] League average aPER for {season}: {lg_aper:.4f}")
        
        # Cache the result
        self._league_aper_cache[cache_key] = lg_aper
        return lg_aper
    
    # =========================================================================
    # OPTIMIZED DATA ACCESS (uses preloaded cache)
    # =========================================================================
    
    def _get_team_players_before_date_cached(
        self,
        team: str,
        season: str,
        before_date: str,
        min_games: int = 1
    ) -> List[dict]:
        """
        Get aggregated player stats for a team before a date.
        Uses preloaded cache for O(n) in-memory filtering instead of DB query.
        """
        if not self._preloaded:
            # Fall back to DB query
            return self._get_team_players_before_date_db(team, season, before_date, min_games)
        
        # Check cache first
        cache_key = (team, season, before_date, min_games)
        if cache_key in self._team_players_agg_cache:
            return self._team_players_agg_cache[cache_key]
        
        key = (team, season)
        if key not in self._player_stats_cache:
            self._team_players_agg_cache[cache_key] = []
            return []
        
        # #region agent log
        # Debug: Check for specific player (Trae Young = 4277905) in cache
        target_player_id = 4277905
        trae_games_in_cache = [pg for pg in self._player_stats_cache[key] if pg.get('player_id') == target_player_id]
        if trae_games_in_cache:
            try:
                import os
                debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
                os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
                with open(debug_log_path, 'a') as f:
                    import json
                    trae_dates = [str(pg.get('date')) + '|' + str(type(pg.get('date'))) for pg in trae_games_in_cache[:5]]
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'A',
                        'location': 'per_calculator.py:515',
                        'message': 'Trae Young found in cache',
                        'data': {
                            'team': team,
                            'season': season,
                            'before_date': before_date,
                            'before_date_type': str(type(before_date)),
                            'trae_games_count': len(trae_games_in_cache),
                            'trae_dates_sample': trae_dates
                        },
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass  # Silently ignore debug log errors
        # #endregion
        
        # #region agent log
        # Debug: Check date format and comparison
        sample_dates = [str(pg.get('date')) + '|' + str(type(pg.get('date'))) for pg in list(self._player_stats_cache[key])[:5]]
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'per_calculator.py:520',
                    'message': 'Date format check before filtering',
                    'data': {
                        'team': team,
                        'season': season,
                        'before_date': before_date,
                        'before_date_type': str(type(before_date)),
                        'total_players_in_cache': len(self._player_stats_cache[key]),
                        'sample_dates': sample_dates
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        # Filter in memory
        # #region agent log
        # Debug: Check date comparison behavior
        date_comparison_results = []
        for pg in list(self._player_stats_cache[key])[:10]:
            pg_date = pg.get('date')
            date_comparison_results.append({
                'player_id': pg.get('player_id'),
                'date': str(pg_date),
                'date_type': str(type(pg_date)),
                'before_date': before_date,
                'comparison_result': str(pg_date) < str(before_date) if pg_date else 'None',
                'direct_comparison': pg_date < before_date if pg_date else None
            })
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'per_calculator.py:523',
                    'message': 'Date comparison test',
                    'data': {
                        'team': team,
                        'season': season,
                        'before_date': before_date,
                        'comparison_samples': date_comparison_results
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        # #region agent log
        # Debug: Check for None/missing dates before filtering
        none_date_count = sum(1 for pg in self._player_stats_cache[key] if not pg.get('date'))
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'E',
                    'location': 'per_calculator.py:653',
                    'message': 'Checking for None/missing dates',
                    'data': {
                        'team': team,
                        'season': season,
                        'before_date': before_date,
                        'total_records': len(self._player_stats_cache[key]),
                        'none_date_count': none_date_count
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        player_games = [
            pg for pg in self._player_stats_cache[key]
            if pg.get('date') and pg['date'] < before_date
        ]
        
        # #region agent log
        # Debug: Check if Trae Young made it through the filter
        trae_games_after_filter = [pg for pg in player_games if pg.get('player_id') == target_player_id]
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'per_calculator.py:526',
                    'message': 'After date filter',
                    'data': {
                        'team': team,
                        'season': season,
                        'before_date': before_date,
                        'total_player_games_before': len(self._player_stats_cache[key]),
                        'total_player_games_after': len(player_games),
                        'trae_games_in_cache': len(trae_games_in_cache),
                        'trae_games_after_filter': len(trae_games_after_filter)
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        if not player_games:
            self._team_players_agg_cache[cache_key] = []
            return []
        
        # Aggregate by player
        player_agg = defaultdict(lambda: {
            'games': 0,
            'games_5min': 0,  # Games where player played > 5 minutes
            'total_min': 0,
            'total_pts': 0,
            'total_fg_made': 0,
            'total_fg_att': 0,
            'total_three_made': 0,
            'total_ft_made': 0,
            'total_ft_att': 0,
            'total_reb': 0,
            'total_oreb': 0,
            'total_ast': 0,
            'total_stl': 0,
            'total_blk': 0,
            'total_to': 0,
            'total_pf': 0,
            'starter_games': 0,
            'player_name': None
        })
        
        for pg in player_games:
            pid = pg['player_id']
            stats = pg.get('stats', {})
            
            # Skip players with no stats.min or stats.min == 0 (did not play)
            min_played = stats.get('min', 0)
            if not min_played or min_played == 0:
                continue
            
            player_agg[pid]['games'] += 1
            player_agg[pid]['total_min'] += min_played
            # Count games where player played > 5 minutes
            if min_played > 5:
                player_agg[pid]['games_5min'] += 1
            player_agg[pid]['total_pts'] += stats.get('pts', 0)
            player_agg[pid]['total_fg_made'] += stats.get('fg_made', 0)
            player_agg[pid]['total_fg_att'] += stats.get('fg_att', 0)
            player_agg[pid]['total_three_made'] += stats.get('three_made', 0)
            player_agg[pid]['total_ft_made'] += stats.get('ft_made', 0)
            player_agg[pid]['total_ft_att'] += stats.get('ft_att', 0)
            player_agg[pid]['total_reb'] += stats.get('reb', 0)
            player_agg[pid]['total_oreb'] += stats.get('oreb', 0)
            player_agg[pid]['total_ast'] += stats.get('ast', 0)
            player_agg[pid]['total_stl'] += stats.get('stl', 0)
            player_agg[pid]['total_blk'] += stats.get('blk', 0)
            player_agg[pid]['total_to'] += stats.get('to', 0)
            player_agg[pid]['total_pf'] += stats.get('pf', 0)
            if pg.get('starter'):
                player_agg[pid]['starter_games'] += 1
            if not player_agg[pid]['player_name']:
                player_agg[pid]['player_name'] = pg.get('player_name', 'Unknown')
        
        # Convert to list format matching DB aggregation output
        result = []
        for pid, agg in player_agg.items():
            if agg['games'] >= min_games and agg['total_min'] > 0:
                result.append({
                    '_id': pid,
                    'player_name': agg['player_name'],
                    'games': agg['games'],
                    'games_5min': agg['games_5min'],  # Games where player played > 5 minutes
                    'total_min': agg['total_min'],
                    'total_pts': agg['total_pts'],
                    'total_fg_made': agg['total_fg_made'],
                    'total_fg_att': agg['total_fg_att'],
                    'total_three_made': agg['total_three_made'],
                    'total_ft_made': agg['total_ft_made'],
                    'total_ft_att': agg['total_ft_att'],
                    'total_reb': agg['total_reb'],
                    'total_oreb': agg['total_oreb'],
                    'total_ast': agg['total_ast'],
                    'total_stl': agg['total_stl'],
                    'total_blk': agg['total_blk'],
                    'total_to': agg['total_to'],
                    'total_pf': agg['total_pf'],
                    'avg_min': agg['total_min'] / agg['games'],
                    'starter_games': agg['starter_games']
                })
        
        # Sort by total minutes descending
        result.sort(key=lambda x: x['total_min'], reverse=True)
        
        # Cache the result
        self._team_players_agg_cache[cache_key] = result
        return result
    
    def _get_team_players_before_date_db(
        self,
        team: str,
        season: str,
        before_date: str,
        min_games: int = 1
    ) -> List[dict]:
        """Fallback: Get player stats via DB aggregation pipeline."""
        pipeline = [
            {
                '$match': {
                    'team': team,
                    'season': season,
                    'date': {'$lt': before_date},
                    'stats.min': {'$gt': 0}
                }
            },
            {
                '$group': {
                    '_id': '$player_id',
                    'player_name': {'$first': '$player_name'},
                    'games': {'$sum': 1},
                    'games_5min': {'$sum': {'$cond': [{'$gt': ['$stats.min', 5]}, 1, 0]}},  # Games where player played > 5 minutes
                    'total_min': {'$sum': '$stats.min'},
                    'total_pts': {'$sum': '$stats.pts'},
                    'total_fg_made': {'$sum': '$stats.fg_made'},
                    'total_fg_att': {'$sum': '$stats.fg_att'},
                    'total_three_made': {'$sum': '$stats.three_made'},
                    'total_ft_made': {'$sum': '$stats.ft_made'},
                    'total_ft_att': {'$sum': '$stats.ft_att'},
                    'total_reb': {'$sum': '$stats.reb'},
                    'total_oreb': {'$sum': '$stats.oreb'},
                    'total_ast': {'$sum': '$stats.ast'},
                    'total_stl': {'$sum': '$stats.stl'},
                    'total_blk': {'$sum': '$stats.blk'},
                    'total_to': {'$sum': '$stats.to'},
                    'total_pf': {'$sum': '$stats.pf'},
                    'avg_min': {'$avg': '$stats.min'},
                    'starter_games': {'$sum': {'$cond': ['$starter', 1, 0]}}
                }
            },
            {'$match': {'games': {'$gte': min_games}}},
            {'$sort': {'total_min': -1}}
        ]
        return list(self.db.stats_nba_players.aggregate(pipeline))
    
    def _get_team_stats_before_date_cached(
        self,
        team: str,
        season: str,
        before_date: str
    ) -> dict:
        """
        Get aggregated team stats before a date.
        Uses preloaded cache for fast access.
        """
        if not self._preloaded:
            return self._get_team_stats_before_date_db(team, season, before_date)
        
        key = (team, season)
        if key not in self._team_stats_cache:
            return self._empty_team_totals()
        
        # Filter in memory
        team_games = [
            tg for tg in self._team_stats_cache[key]
            if tg['date'] < before_date
        ]
        
        if not team_games:
            return self._empty_team_totals()
        
        # Aggregate
        totals = self._empty_team_totals()
        for tg in team_games:
            td = tg['team_data']
            totals['assists'] += td.get('assists', 0)
            totals['FG_made'] += td.get('FG_made', 0)
            totals['FG_att'] += td.get('FG_att', 0)
            totals['FT_made'] += td.get('FT_made', 0)
            totals['FT_att'] += td.get('FT_att', 0)
            totals['total_reb'] += td.get('total_reb', 0)
            totals['off_reb'] += td.get('off_reb', 0)
            totals['TO'] += td.get('TO', 0)
        
        return totals
    
    def _get_team_stats_before_date_db(self, team: str, season: str, before_date: str) -> dict:
        """Fallback: Get team stats via DB query."""
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'homeTeam.name': team},
                        {'awayTeam.name': team}
                    ],
                    'season': season,
                    'date': {'$lt': before_date}
                }
            }
        ]
        
        games = list(self.db.stats_nba.aggregate(pipeline))
        totals = self._empty_team_totals()
        
        for game in games:
            if game['homeTeam']['name'] == team:
                td = game['homeTeam']
            else:
                td = game['awayTeam']
            
            totals['assists'] += td.get('assists', 0)
            totals['FG_made'] += td.get('FG_made', 0)
            totals['FG_att'] += td.get('FG_att', 0)
            totals['FT_made'] += td.get('FT_made', 0)
            totals['FT_att'] += td.get('FT_att', 0)
            totals['total_reb'] += td.get('total_reb', 0)
            totals['off_reb'] += td.get('off_reb', 0)
            totals['TO'] += td.get('TO', 0)
        
        return totals
    
    def _empty_team_totals(self) -> dict:
        return {
            'assists': 0, 'FG_made': 0, 'FG_att': 0,
            'FT_made': 0, 'FT_att': 0, 'total_reb': 0,
            'off_reb': 0, 'TO': 0
        }
    
    # =========================================================================
    # TEAM PER FEATURES (with caching)
    # =========================================================================
    
    def compute_team_per_features(
        self,
        team: str,
        season: str,
        before_date: str,
        top_n: int = 8,
        player_filters: Optional[Dict] = None,
        injured_players: Optional[List[str]] = None
    ) -> Optional[dict]:
        """
        Compute team-level PER features for game prediction.
        Uses preloaded cache for fast computation.
        
        Args:
            team: Team name
            season: Season string
            before_date: Date before which to compute stats
            top_n: Number of top players to include
            player_filters: Optional dict with keys:
                - 'playing': List of player_ids that are playing (exclude others)
                - 'starters': List of player_ids that are starters
            injured_players: Optional list of injured player IDs (strings). 
                If provided, these players will be excluded from PER calculations.
                Training: Should pass stats_nba.{home/away}Team.injured_players
                Prediction: Should pass injured players from nba_rosters.injured flag
        """
        logger = logging.getLogger(__name__)
        
        # #region agent log
        # Debug: Check if cache key exists and what keys are available
        cache_key_check = (team, season)
        available_keys_sample = list(self._player_stats_cache.keys())[:20] if hasattr(self, '_player_stats_cache') and self._player_stats_cache else []
        matching_keys = [k for k in available_keys_sample if k[1] == season]  # Keys with matching season
        try:
            import os
            debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
            os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
            with open(debug_log_path, 'a') as f:
                import json
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'D',
                    'location': 'per_calculator.py:775',
                    'message': 'Cache key lookup check',
                    'data': {
                        'team': team,
                        'season': season,
                        'cache_key_lookup': str(cache_key_check),
                        'cache_key_exists': cache_key_check in self._player_stats_cache if hasattr(self, '_player_stats_cache') and self._player_stats_cache else False,
                        'available_keys_sample': [str(k) for k in available_keys_sample],
                        'matching_season_keys': [str(k) for k in matching_keys]
                    },
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass  # Silently ignore debug log errors
        # #endregion
        
        # Get all players who have played for this team
        players = self._get_team_players_before_date_cached(team, season, before_date, min_games=1)
        
        # #region agent log
        # Debug: Check if Trae Young is in the returned players
        if players:
            trae_in_players = [p for p in players if p.get('_id') == 4277905 or p.get('_id') == '4277905']
            try:
                import os
                debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
                os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
                with open(debug_log_path, 'a') as f:
                    import json
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'D',
                        'location': 'per_calculator.py:777',
                        'message': 'Players returned from cache lookup',
                        'data': {
                            'team': team,
                            'season': season,
                            'before_date': before_date,
                            'players_count': len(players),
                            'trae_young_in_players': len(trae_in_players) > 0,
                            'trae_player_ids_in_players': [p.get('_id') for p in players if str(p.get('_id', '')) == '4277905'][:3],
                            'sample_player_ids': [str(p.get('_id')) for p in players[:5]]
                        },
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass  # Silently ignore debug log errors
        # #endregion
        
        if not players:
            logger.debug(f"[PER] No players found for {team} before {before_date}")
            return None
        
        initial_player_count = len(players)
        initial_player_ids = {str(p.get('_id', '')) for p in players}
        logger.debug(f"[PER] {team}: Found {initial_player_count} players before {before_date}")
        
        # DEBUG: If player_filters provided, check for mismatches early (before any filtering)
        if player_filters:
            playing_list_check = player_filters.get(team, {}).get('playing', [])
            if playing_list_check:
                playing_set_check = {str(pid) for pid in playing_list_check}
                unmatched_early = playing_set_check - initial_player_ids
                if unmatched_early:
                    logger.warning(
                        f"[PER] {team}: DEBUG - {len(unmatched_early)} players in filter but NOT in initial players list (before any filtering): "
                        f"{list(unmatched_early)[:5]}. This suggests they don't have stats before {before_date} or weren't found by aggregation."
                    )
        
        # Phase 2.1: Filter out injured players if explicitly provided
        # CRITICAL: Injured players are excluded from ALL PER feature calculations:
        # - perAvg, perWeighted, per1/per2/per3, and startersPerAvg
        # This filtering happens BEFORE any PER calculations, ensuring injured players
        # are never included in any PER features
        if injured_players:
            # Convert to set of strings for efficient lookup
            injured_players_set = {str(pid) for pid in injured_players}
            players_before_injury = len(players)
            players = [p for p in players if str(p['_id']) not in injured_players_set]
            players_after_injury = len(players)
            logger.debug(f"[PER] {team}: Filtering out {len(injured_players_set)} injured players: {players_before_injury} -> {players_after_injury}")
            
            # DEBUG: Check if any players were removed by injury filter
            if players_before_injury > players_after_injury:
                removed_by_injury = players_before_injury - players_after_injury
                logger.debug(f"[PER] {team}: Removed {removed_by_injury} injured players from PER calculations")
        
        # Phase 2.2: Filter to roster players if player_filters is provided (prediction mode)
        # This ensures we only consider players who are actually on the roster
        if player_filters:
            player_ids = [p['_id'] for p in players]
            roster_player_ids = set()
            
            if player_ids:
                # Get roster from nba_rosters collection for roster membership
                # nba_rosters uses season + team as unique key
                roster_doc = self.db.nba_rosters.find_one(
                    {'season': season, 'team': team}
                )
                
                if roster_doc:
                    roster = roster_doc.get('roster', [])
                    for roster_entry in roster:
                        roster_player_id = str(roster_entry.get('player_id', ''))
                        roster_player_ids.add(roster_player_id)
                
                # If roster exists, filter to only players in the roster
                if roster_player_ids:
                    players_before_roster = len(players)
                    players = [p for p in players if str(p['_id']) in roster_player_ids]
                    players_after_roster = len(players)
                    logger.debug(f"[PER] {team}: Filtering to {len(roster_player_ids)} players from nba_rosters: {players_before_roster} -> {players_after_roster}")
        
        db_filtered_count = len(players)
        logger.debug(f"[PER] {team}: {db_filtered_count} players after filtering")
        
        if not players:
            logger.warning(f"[PER] {team}: No players remaining after filtering")
            return None
        
        # Store filter sets for later use
        playing_set = None
        starters_set = None
        
        # Phase 2.3: Apply player filters if provided and validate IDs
        if player_filters:
            playing_list = player_filters.get('playing', [])
            starters_list = player_filters.get('starters', [])
            
            if playing_list:
                playing_set = set(playing_list)
                
                # Phase 2.2: Hard ID mismatch check
                # Normalize both to strings to handle type mismatches (player_id can be int or str in DB)
                available_ids = {str(p['_id']) for p in players}
                playing_set_str = {str(pid) for pid in playing_list}
                unmatched = playing_set_str - available_ids
                
                # #region agent log
                # Debug: Log mismatch details
                if unmatched and 4277905 in unmatched:  # Trae Young
                    target_id = 4277905
                    try:
                        import os
                        debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
                        os.makedirs(os.path.dirname(debug_log_path), exist_ok=True)
                        with open(debug_log_path, 'a') as f:
                            import json
                            f.write(json.dumps({
                                'sessionId': 'debug-session',
                                'runId': 'run1',
                                'hypothesisId': 'B',
                                'location': 'per_calculator.py:833',
                                'message': 'Mismatch detected for Trae Young',
                                'data': {
                                    'team': team,
                                    'season': season,
                                    'before_date': before_date,
                                    'playing_list': list(playing_list),
                                    'available_ids': list(available_ids),
                                    'unmatched': list(unmatched),
                                    'players_count': len(players),
                                    'player_ids_in_players': [p['_id'] for p in players[:10]]
                                },
                                'timestamp': int(__import__('time').time() * 1000)
                            }) + '\n')
                    except Exception:
                        pass  # Silently ignore debug log errors
                # #endregion
                
                if unmatched:
                    # Look up player names for unmatched IDs
                    unmatched_list = list(unmatched)
                    player_name_map = {}
                    try:
                        # Query stats_nba_players to get player names
                        unmatched_docs = list(self.db.stats_nba_players.find(
                            {'player_id': {'$in': unmatched_list}},
                            {'player_id': 1, 'player_name': 1}
                        ).limit(20))
                        player_name_map = {doc['player_id']: doc.get('player_name', 'Unknown') for doc in unmatched_docs}
                    except Exception as e:
                        logger.debug(f"Error looking up player names: {e}")
                    
                    # Build player info strings (ID: Name if available, otherwise just ID)
                    player_info_list = []
                    for pid in unmatched_list[:10]:  # Show up to 10
                        name = player_name_map.get(pid, 'Unknown')
                        if name and name != 'Unknown':
                            player_info_list.append(f"{pid} ({name})")
                        else:
                            player_info_list.append(pid)
                    
                    # DEBUG: Check why these players are unmatched
                    debug_info = []
                    for unmatched_id in unmatched_list[:5]:  # Check first 5 unmatched
                        # Check if they have stats before the date
                        stats_check = list(self.db.stats_nba_players.find(
                            {
                                'player_id': unmatched_id,
                                'team': team,
                                'season': season,
                                'date': {'$lt': before_date},
                                'stats.min': {'$gt': 0}
                            },
                            {'date': 1, 'game_id': 1}
                        ).sort('date', -1).limit(3))
                        debug_info.append(f"{unmatched_id}: {len(stats_check)} games before {before_date}")
                        
                        # Check if they're in the initial players list (before filtering)
                        initial_players_check = [p for p in players if str(p.get('_id', '')) == unmatched_id]
                        if initial_players_check:
                            debug_info.append(f"  -> Found in players list after filtering")
                        else:
                            debug_info.append(f"  -> NOT in players list after filtering")
                    
                    # Build detailed warning message
                    warning_msg = (
                        f"[PER] {team}: Some player_filters IDs not found in available players. "
                        f"Game date: {before_date}, Season: {season}. "
                        f"Total unmatched: {len(unmatched)}. "
                        f"Filter had {len(playing_list)} players, available had {len(available_ids)} players. "
                        f"Unmatched IDs: {', '.join(player_info_list)}. "
                        f"DEBUG: {'; '.join(debug_info)}"
                    )
                    if len(unmatched) > 10:
                        warning_msg += f" (showing first 10 of {len(unmatched)})"
                    
                    logger.warning(warning_msg)
                
                # Filter to only players who are playing (normalize _id to string for comparison)
                players = [p for p in players if str(p['_id']) in playing_set_str]
                logger.debug(f"[PER] {team}: {len(players)} players after applying 'playing' filter")
            
            if starters_list:
                starters_set = set(starters_list)
                logger.debug(f"[PER] {team}: {len(starters_set)} starters specified in filter")
        
        # Get league constants
        league_constants = get_league_constants(season, self.db)
        if not league_constants:
            return None
        
        lg_pace = league_constants.get('lg_pace', 95)
        team_pace = get_team_pace(season, team, self.db)
        
        # Get league average aPER for normalization
        # Try to get from cache first, otherwise compute it
        cached_stats = get_season_stats_with_fallback(season, self.db)
        lg_aper = None
        if cached_stats and 'lg_aper' in cached_stats:
            lg_aper = cached_stats['lg_aper']
        else:
            # Compute on-demand (can be slow, but ensures accuracy)
            logger.debug(f"[PER] Computing lg_aPER for {season} (not cached)")
            lg_aper = self.compute_league_average_aper(season, before_date)
            # Cache it for future use (optional optimization)
            if lg_aper > 0 and cached_stats:
                try:
                    self.db.cached_league_stats.update_one(
                        {'season': season},
                        {'$set': {'lg_aper': lg_aper}},
                        upsert=False
                    )
                except Exception as e:
                    logger.debug(f"[PER] Could not cache lg_aper: {e}")
        
        # Fallback: if lg_aper is still 0 or None, don't normalize
        use_normalization = lg_aper is not None and lg_aper > 0
        
        # Get team totals for PER calculation
        team_stats = self._get_team_stats_before_date_cached(team, season, before_date)
        
        player_pers = []
        
        # Process all players (no top_n cutoff - assume player_filters provides correct players)
        for player in players:
            total_min = player['total_min']
            if total_min == 0:
                continue
            
            # Aggregate stats to compute PER
            agg_stats = {
                'min': total_min,
                'pts': player['total_pts'],
                'fg_made': player['total_fg_made'],
                'fg_att': player['total_fg_att'],
                'three_made': player['total_three_made'],
                'ft_made': player['total_ft_made'],
                'ft_att': player['total_ft_att'],
                'reb': player['total_reb'],
                'oreb': player['total_oreb'],
                'ast': player['total_ast'],
                'stl': player['total_stl'],
                'blk': player['total_blk'],
                'to': player['total_to'],
                'pf': player['total_pf']
            }
            
            uper = self.compute_uper(agg_stats, team_stats, league_constants)
            aper = self.compute_aper(uper, team_pace, lg_pace)
            
            # Normalize to PER (league average = 15.0)
            if use_normalization:
                per = self.compute_per(aper, lg_aper)
            else:
                per = aper  # Use aPER if normalization not available
            
            # Determine if player is starter (for individual player dict, not used in startersPerAvg calculation)
            # For prediction (player_filters provided): Use nba_rosters.starter as authority
            # For training (no player_filters): Use historical heuristic from stats_nba_players
            # Determine starter status
            # CRITICAL: When player_filters is provided, use starters from player_filters (not nba_rosters)
            # - Training: player_filters['starters'] comes from stats_nba_players.starter for that game
            # - Prediction: player_filters['starters'] comes from UI (which syncs with nba_rosters.starter)
            if player_filters:
                # Use starter status from player_filters (source of truth)
                # player_filters['starters'] already contains the correct starter list:
                # - Training: Built from stats_nba_players.starter for the specific game
                # - Prediction: Built from UI's player_config (which syncs with nba_rosters)
                starters_set = player_filters.get(team, {}).get('starters', [])
                if starters_set:
                    # player_filters['starters'] is the authority
                    is_starter = str(player['_id']) in {str(sid) for sid in starters_set}
                else:
                    # Fallback: if no starters in player_filters, use historical heuristic
                    is_starter = player['starter_games'] > player['games'] / 2
            else:
                # Training mode (no player_filters): Use historical heuristic
                is_starter = player['starter_games'] > player['games'] / 2
            
            # Calculate minutes per game (MPG) for sorting
            games_5min = player.get('games_5min', 0)
            mpg = total_min / games_5min if games_5min > 0 else 0
            
            player_pers.append({
                'player_id': player['_id'],
                'player_name': player['player_name'],
                'games': player['games'],
                'games_5min': games_5min,  # Games where player played > 5 minutes
                'total_min': total_min,
                'avg_min': player['avg_min'],
                'mpg': mpg,  # Minutes per game (total_min / games_5min)
                'uper': uper,
                'aper': aper,
                'per': per,  # Normalized PER (or aPER if normalization not available)
                'is_starter': is_starter
            })
        
        if not player_pers:
            logger.warning(f"[PER] {team}: No players with valid PER after filtering")
            return None
        
        # Phase 2.1: Log final player count
        logger.debug(f"[PER] {team}: Computing PER for {len(player_pers)} players")
        if use_normalization:
            logger.debug(f"[PER] {team}: Using normalized PER (lg_aPER={lg_aper:.4f})")
        else:
            logger.debug(f"[PER] {team}: Using aPER (normalization not available)")
        
        # Use all players (no sorting/cutoff - assume player_filters provides correct players)
        # Calculate perAvg as simple average of all players' PER
        per_avg = np.mean([p['per'] for p in player_pers]) if player_pers else 0
        
        # Calculate perWeighted using minutes per game (MPG) as weight
        # MPG = total_min / games_5min (games where player played > 5 minutes)
        # If games_5min is 0, weight is 0 (MPG already calculated and stored in player dict)
        weighted_sum = 0.0
        total_mpg = 0.0
        for p in player_pers:
            mpg = p.get('mpg', 0)
            if mpg > 0:  # Only include players with games_5min > 0 (i.e., played > 5 min in at least one game)
                weighted_sum += p['per'] * mpg
                total_mpg += mpg
        per_weighted = weighted_sum / total_mpg if total_mpg > 0 else 0
        
        # Phase 4.1: For startersPerAvg calculation, use nba_rosters.starter as authority for prediction
        # CRITICAL: For prediction mode, starter status MUST come from nba_rosters.starter (not historical heuristic)
        # This ensures startersPerAvg uses the current game's starter lineup from nba_rosters collection
        if player_filters:
            # Prediction mode: nba_rosters.starter is the authority for starter status
            # Query nba_rosters collection to get current starter status for this game
            # Note: player_pers already excludes injured players (filtered earlier)
            player_ids = [str(p['player_id']) for p in player_pers]
            starter_ids = set()
            
            roster_doc = self.db.nba_rosters.find_one(
                {'season': season, 'team': team}
            )
            
            if roster_doc:
                roster = roster_doc.get('roster', [])
                for roster_entry in roster:
                    roster_player_id = str(roster_entry.get('player_id', ''))
                    if roster_player_id in player_ids and roster_entry.get('starter', False):
                        starter_ids.add(roster_player_id)
            else:
                # Fallback to players_nba if nba_rosters doesn't exist
                starter_docs = list(self.db.players_nba.find(
                    {'player_id': {'$in': player_ids}, 'team': team, 'starter': True},
                    {'player_id': 1}
                ))
                starter_ids = {str(doc['player_id']) for doc in starter_docs}
            
            starters = [p for p in player_pers if str(p['player_id']) in starter_ids][:5]
            logger.debug(f"[PER] {team}: Using {len(starters)} starters from nba_rosters (prediction mode)")
        else:
            # Training mode: Use historical heuristic (is_starter from aggregated stats)
            starters = [p for p in player_pers if p['is_starter']][:5]
            logger.debug(f"[PER] {team}: Using historical starter heuristic ({len(starters)} starters, training mode)")
        
        starters_avg = np.mean([p['per'] for p in starters]) if starters else per_avg
        
        # For per1, per2, per3: sort by PER (descending) and take top 3
        # These features represent the top 1st, 2nd, and 3rd players by PER value
        player_pers_sorted_by_per = sorted(player_pers, key=lambda x: x.get('per', 0), reverse=True)
        slot_pers = [p['per'] for p in player_pers_sorted_by_per[:3]]
        # Only keep per1, per2, per3
        while len(slot_pers) < 3:
            slot_pers.append(0)
        
        # Calculate recency-weighted PER for top player by MPG (for player_per_1|none|weighted_MIN_REC feature)
        # Note: This uses top player by MPG, not by PER
        player_pers_sorted_by_mpg = sorted(player_pers, key=lambda x: x.get('mpg', 0), reverse=True)
        per1_recency_weighted = 0.0
        if player_pers_sorted_by_mpg and len(player_pers_sorted_by_mpg) > 0:
            top_player_by_mpg_id = player_pers_sorted_by_mpg[0]['player_id']
            recency_per = self.get_player_recency_weighted_per(
                str(top_player_by_mpg_id), team, season, before_date, recency_decay_k=15.0
            )
            per1_recency_weighted = recency_per if recency_per is not None else 0.0
        
        # Phase 2.1: Log final PER values
        logger.debug(
            f"[PER] {team}: PER_avg={per_avg:.2f}, PER_weighted={per_weighted:.2f}, "
            f"Starters_avg={starters_avg:.2f}, Player_count={len(player_pers)}"
        )
        
        # Build player lists for each feature
        # perAvg: all players used in calculation
        per_avg_players = [{'player_id': str(p['player_id']), 'player_name': p['player_name'], 'per': p['per']} for p in player_pers]
        
        # perWeighted: all players with MPG > 0 (used in weighted calculation)
        per_weighted_players = [{'player_id': str(p['player_id']), 'player_name': p['player_name'], 'per': p['per'], 'mpg': p.get('mpg', 0)} 
                                for p in player_pers if p.get('mpg', 0) > 0]
        
        # startersPerAvg: starter players
        starters_players = [{'player_id': str(p['player_id']), 'player_name': p['player_name'], 'per': p['per']} for p in starters]
        
        # per1, per2, per3: top 3 players by PER (not MPG)
        per1_player = [{'player_id': str(player_pers_sorted_by_per[0]['player_id']), 'player_name': player_pers_sorted_by_per[0]['player_name'], 'per': player_pers_sorted_by_per[0]['per'], 'mpg': player_pers_sorted_by_per[0].get('mpg', 0)}] if len(player_pers_sorted_by_per) > 0 else []
        per2_player = [{'player_id': str(player_pers_sorted_by_per[1]['player_id']), 'player_name': player_pers_sorted_by_per[1]['player_name'], 'per': player_pers_sorted_by_per[1]['per'], 'mpg': player_pers_sorted_by_per[1].get('mpg', 0)}] if len(player_pers_sorted_by_per) > 1 else []
        per3_player = [{'player_id': str(player_pers_sorted_by_per[2]['player_id']), 'player_name': player_pers_sorted_by_per[2]['player_name'], 'per': player_pers_sorted_by_per[2]['per'], 'mpg': player_pers_sorted_by_per[2].get('mpg', 0)}] if len(player_pers_sorted_by_per) > 2 else []
        
        # Calculate topN_avg features (average PER of top N players)
        top1_avg = slot_pers[0] if len(slot_pers) > 0 else 0.0
        top2_avg = np.mean(slot_pers[:2]) if len(slot_pers) >= 2 else (top1_avg if len(slot_pers) >= 1 else 0.0)
        top3_avg = np.mean(slot_pers[:3]) if len(slot_pers) >= 3 else (np.mean(slot_pers) if len(slot_pers) > 0 else 0.0)
        
        # Calculate topN_weighted_MPG features (MPG-weighted average PER of top N players)
        top1_weighted = 0.0
        top2_weighted = 0.0
        top3_weighted = 0.0
        
        if len(player_pers_sorted_by_per) > 0:
            top1_players = player_pers_sorted_by_per[:1]
            top1_weighted = np.average([p['per'] for p in top1_players], weights=[p.get('mpg', 0) for p in top1_players]) if any(p.get('mpg', 0) > 0 for p in top1_players) else top1_avg
        
        if len(player_pers_sorted_by_per) >= 2:
            top2_players = player_pers_sorted_by_per[:2]
            top2_weighted = np.average([p['per'] for p in top2_players], weights=[p.get('mpg', 0) for p in top2_players]) if any(p.get('mpg', 0) > 0 for p in top2_players) else top2_avg
        
        if len(player_pers_sorted_by_per) >= 3:
            top3_players = player_pers_sorted_by_per[:3]
            top3_weighted = np.average([p['per'] for p in top3_players], weights=[p.get('mpg', 0) for p in top3_players]) if any(p.get('mpg', 0) > 0 for p in top3_players) else top3_avg
        
        return {
            'team': team,
            'season': season,
            'before_date': before_date,
            'per_avg': float(per_avg),
            'per_weighted': float(per_weighted),
            'starters_avg': float(starters_avg),
            'per1': slot_pers[0] if len(slot_pers) > 0 else 0,
            'per2': slot_pers[1] if len(slot_pers) > 1 else 0,
            'per3': slot_pers[2] if len(slot_pers) > 2 else 0,
            'per1_recency_weighted': float(per1_recency_weighted),
            'top1_avg': float(top1_avg),
            'top2_avg': float(top2_avg),
            'top3_avg': float(top3_avg),
            'top1_weighted_MPG': float(top1_weighted),
            'top2_weighted_MPG': float(top2_weighted),
            'top3_weighted_MPG': float(top3_weighted),
            'player_count': len(player_pers),
            'players': player_pers[:top_n],
            # Player lists for each feature
            'per_avg_players': per_avg_players,
            'per_weighted_players': per_weighted_players,
            'starters_players': starters_players,
            'per1_player': per1_player,
            'per2_player': per2_player,
            'per3_player': per3_player
        }
    
    def get_game_per_features(
        self,
        home_team: str,
        away_team: str,
        season: str,
        game_date: str,
        use_cache: bool = True,
        player_filters: Optional[Dict] = None,
        injured_players: Optional[Dict] = None
    ) -> Optional[dict]:
        """
        Get PER-based features for a game prediction.
        
        Args:
            home_team: Home team name
            away_team: Away team name
            season: Season string
            game_date: Date of the game (YYYY-MM-DD)
            use_cache: If True, check MongoDB cache first
            player_filters: Optional dict with team names as keys:
                {team: {'playing': [player_ids], 'starters': [player_ids]}}
            injured_players: Optional dict with team names as keys:
                {team: [player_ids]} - List of injured player IDs for each team
                Training: Should pass stats_nba.{home/away}Team.injured_players
                Prediction: Should pass injured players from nba_rosters.injured flag
            
        Returns:
            Dict with differential PER features for the matchup
        """
        # Don't use cache if player filters or injured players are provided (different configuration)
        if player_filters or injured_players:
            use_cache = False
        
        # Check in-memory cache first (only if no filters)
        cache_key = f"{season}|{home_team}|{away_team}|{game_date}"
        if use_cache and cache_key in self._per_features_cache:
            return self._per_features_cache[cache_key]
        
        # Get player filters and injured players for each team
        home_filters = player_filters.get(home_team, {}) if player_filters else None
        away_filters = player_filters.get(away_team, {}) if player_filters else None
        home_injured = injured_players.get(home_team, []) if injured_players else None
        away_injured = injured_players.get(away_team, []) if injured_players else None
        
        # Compute features
        home_per = self.compute_team_per_features(
            home_team, season, game_date, 
            player_filters=home_filters,
            injured_players=home_injured
        )
        away_per = self.compute_team_per_features(
            away_team, season, game_date,
            player_filters=away_filters,
            injured_players=away_injured
        )
        
        if not home_per or not away_per:
            return None
        
        # Return features in new pipe-delimited format
        features = {
            'player_team_per|season|avg|home': home_per['per_avg'],
            'player_team_per|season|avg|away': away_per['per_avg'],
            'player_team_per|season|avg|diff': home_per['per_avg'] - away_per['per_avg'],
            
            'player_team_per|season|weighted_MPG|home': home_per['per_weighted'],
            'player_team_per|season|weighted_MPG|away': away_per['per_weighted'],
            'player_team_per|season|weighted_MPG|diff': home_per['per_weighted'] - away_per['per_weighted'],
            
            'player_starters_per|season|avg|home': home_per['starters_avg'],
            'player_starters_per|season|avg|away': away_per['starters_avg'],
            'player_starters_per|season|avg|diff': home_per['starters_avg'] - away_per['starters_avg'],
            
            # New format: player_per|season|topN_avg (average PER of top N players)
            'player_per|season|top1_avg|home': home_per.get('top1_avg', 0),
            'player_per|season|top2_avg|home': home_per.get('top2_avg', 0),
            'player_per|season|top3_avg|home': home_per.get('top3_avg', 0),
            
            'player_per|season|top1_avg|away': away_per.get('top1_avg', 0),
            'player_per|season|top2_avg|away': away_per.get('top2_avg', 0),
            'player_per|season|top3_avg|away': away_per.get('top3_avg', 0),
            
            'player_per|season|top1_avg|diff': home_per.get('top1_avg', 0) - away_per.get('top1_avg', 0),
            'player_per|season|top2_avg|diff': home_per.get('top2_avg', 0) - away_per.get('top2_avg', 0),
            'player_per|season|top3_avg|diff': home_per.get('top3_avg', 0) - away_per.get('top3_avg', 0),
            
            # MPG-weighted versions
            'player_per|season|top1_weighted_MPG|home': home_per.get('top1_weighted_MPG', 0),
            'player_per|season|top2_weighted_MPG|home': home_per.get('top2_weighted_MPG', 0),
            'player_per|season|top3_weighted_MPG|home': home_per.get('top3_weighted_MPG', 0),
            
            'player_per|season|top1_weighted_MPG|away': away_per.get('top1_weighted_MPG', 0),
            'player_per|season|top2_weighted_MPG|away': away_per.get('top2_weighted_MPG', 0),
            'player_per|season|top3_weighted_MPG|away': away_per.get('top3_weighted_MPG', 0),
            
            'player_per|season|top1_weighted_MPG|diff': home_per.get('top1_weighted_MPG', 0) - away_per.get('top1_weighted_MPG', 0),
            'player_per|season|top2_weighted_MPG|diff': home_per.get('top2_weighted_MPG', 0) - away_per.get('top2_weighted_MPG', 0),
            'player_per|season|top3_weighted_MPG|diff': home_per.get('top3_weighted_MPG', 0) - away_per.get('top3_weighted_MPG', 0),
            
            # Player lists for each feature (for display in feature modal)
            '_player_lists': {
                'player_team_per|season|avg|home': home_per.get('per_avg_players', []),
                'player_team_per|season|avg|away': away_per.get('per_avg_players', []),
                'player_team_per|season|weighted_MPG|home': home_per.get('per_weighted_players', []),
                'player_team_per|season|weighted_MPG|away': away_per.get('per_weighted_players', []),
                'player_starters_per|season|avg|home': home_per.get('starters_players', []),
                'player_starters_per|season|avg|away': away_per.get('starters_players', []),
                'player_per_1|season|top1_avg|home': home_per.get('per1_player', []),
                'player_per_1|season|top1_avg|away': away_per.get('per1_player', []),
                'player_per_2|season|top1_avg|home': home_per.get('per2_player', []),
                'player_per_2|season|top1_avg|away': away_per.get('per2_player', []),
                'player_per_3|season|top1_avg|home': home_per.get('per3_player', []),
                'player_per_3|season|top1_avg|away': away_per.get('per3_player', [])
            },
            
            # New features for master training
            'player_per_1|none|weighted_MIN_REC|home': home_per.get('per1_recency_weighted', 0),
            'player_per_1|none|weighted_MIN_REC|away': away_per.get('per1_recency_weighted', 0),
            'player_per_1|none|weighted_MIN_REC|diff': home_per.get('per1_recency_weighted', 0) - away_per.get('per1_recency_weighted', 0),
            
            'player_per_1|season|raw|home': home_per['per1'],  # Using existing aggregated PER
            'player_per_1|season|raw|away': away_per['per1'],
            'player_per_1|season|raw|diff': home_per['per1'] - away_per['per1'],
            
            'player_per_2|season|raw|home': home_per['per2'],  # Using existing aggregated PER
            'player_per_2|season|raw|away': away_per['per2'],
            'player_per_2|season|raw|diff': home_per['per2'] - away_per['per2'],
            
            'player_per_3|season|raw|home': home_per['per3'],  # Using existing aggregated PER
            'player_per_3|season|raw|away': away_per['per3'],
            'player_per_3|season|raw|diff': home_per['per3'] - away_per['per3'],
            
            # Internal metadata (not used as features)
            'homePlayerCount': home_per['player_count'],
            'awayPlayerCount': away_per['player_count']
        }
        
        # Store in in-memory cache
        self._per_features_cache[cache_key] = features
        
        return features
    
    def save_per_features_to_db(self, season: str = None):
        """
        Save all computed PER features from memory to MongoDB.
        
        Args:
            season: If provided, only save features for this season
        """
        # Group features by season
        season_features = defaultdict(dict)
        
        for cache_key, features in self._per_features_cache.items():
            parts = cache_key.split('|')
            if len(parts) >= 4:
                key_season = parts[0]
                game_key = '|'.join(parts[1:])
                
                if season is None or key_season == season:
                    season_features[key_season][game_key] = features
        
        # Save each season
        for szn, game_features in season_features.items():
            self._save_per_cache(szn, game_features)
            print(f"  Saved {len(game_features)} PER features for {szn}")
    
    def clear_cache(self, season: str = None):
        """Clear cached PER features from MongoDB."""
        if season:
            self.db[CACHED_PER_COLLECTION].delete_one({'season': season})
        else:
            self.db[CACHED_PER_COLLECTION].delete_many({})
        
        # Clear in-memory cache
        if season:
            self._per_features_cache = {
                k: v for k, v in self._per_features_cache.items()
                if not k.startswith(f"{season}|")
            }
        else:
            self._per_features_cache = {}
    
    # =========================================================================
    # LEGACY DB QUERY METHODS (for backward compatibility)
    # =========================================================================
    
    def get_player_game_stats(self, player_id: str, game_id: str) -> Optional[dict]:
        """Get player stats for a specific game."""
        return self.db.stats_nba_players.find_one({
            'player_id': player_id,
            'game_id': game_id
        })
    
    def get_team_game_stats(self, game_id: str, is_home: bool) -> Optional[dict]:
        """Get team stats for a specific game."""
        game = self.db.stats_nba.find_one({'game_id': game_id})
        if not game:
            return None
        return game['homeTeam'] if is_home else game['awayTeam']
    
    def get_team_players_before_date(
        self,
        team: str,
        season: str,
        before_date: str,
        min_games: int = 3
    ) -> List[dict]:
        """Get all players who have played for a team before a given date."""
        return self._get_team_players_before_date_cached(team, season, before_date, min_games)
    
    def get_player_recency_weighted_per(
        self,
        player_id: str,
        team: str,
        season: str,
        before_date: str,
        recency_decay_k: float = 15.0
    ) -> Optional[float]:
        """
        Get a player's recency-weighted PER using game-level PER calculations.
        
        For each game the player played:
        - Compute PER using that game's box score and team context
        - Weight by: MIN_g * exp(-days_since_game / k)
        - Aggregate: Σ (PER_g * w_g) / Σ w_g
        
        Args:
            player_id: Player ID (as string)
            team: Team name
            season: Season string
            before_date: Date string (YYYY-MM-DD) - stats up to but not including this date
            recency_decay_k: Decay constant for recency weighting (default 15.0)
        
        Returns:
            Recency-weighted PER (float) or None if player not found or insufficient data
        """
        from datetime import datetime
        
        logger = logging.getLogger(__name__)
        
        # Get all games for this player before the date
        if self._preloaded and self._player_stats_cache:
            # Use preloaded cache
            key = (team, season)
            if key not in self._player_stats_cache:
                return None
            
            player_games = [
                pg for pg in self._player_stats_cache[key]
                if (pg.get('player_id') == player_id or str(pg.get('player_id')) == str(player_id)) and
                   pg.get('date') and pg['date'] < before_date and
                   pg.get('stats', {}).get('min', 0) > 0
            ]
        else:
            # Fallback to DB query
            player_games = list(self.db.stats_nba_players.find({
                'player_id': player_id,
                'team': team,
                'season': season,
                'date': {'$lt': before_date},
                'stats.min': {'$gt': 0}
            }))
        
        if not player_games:
            return None
        
        # Sort by date
        player_games.sort(key=lambda x: x.get('date', ''))
        
        # Get league constants (same for all games in season)
        league_constants = get_league_constants(season, self.db)
        if not league_constants:
            return None
        
        lg_pace = league_constants.get('lg_pace', 95)
        
        # Get league average aPER for normalization
        lg_aper = self.compute_league_average_aper(season, before_date)
        use_normalization = lg_aper > 0
        
        # Parse game date for recency calculation
        try:
            game_date_obj = datetime.strptime(before_date, '%Y-%m-%d').date()
        except:
            return None
        
        # Calculate PER for each game and apply recency weighting
        weighted_per_sum = 0.0
        total_weight = 0.0
        
        for pg in player_games:
            game_date_str = pg.get('date')
            if not game_date_str:
                continue
            
            try:
                pg_date_obj = datetime.strptime(str(game_date_str), '%Y-%m-%d').date() if isinstance(game_date_str, str) else game_date_str
                if isinstance(pg_date_obj, str):
                    pg_date_obj = datetime.strptime(pg_date_obj, '%Y-%m-%d').date()
            except:
                continue
            
            # Calculate days since game
            days_since = (game_date_obj - pg_date_obj).days
            if days_since < 0:
                continue  # Skip future games (shouldn't happen, but safety check)
            
            # Get player stats for this game
            stats = pg.get('stats', {})
            min_played = stats.get('min', 0)
            if min_played == 0:
                continue
            
            # Get team stats for this specific game
            game_id = pg.get('game_id')
            if not game_id:
                continue
            
            game_doc = self.db.stats_nba.find_one({'game_id': game_id})
            if not game_doc:
                continue
            
            # Determine if player was on home or away team
            is_home = pg.get('home', False)
            team_data = game_doc.get('homeTeam' if is_home else 'awayTeam', {})
            
            # Get team stats for this game
            team_stats = {
                'assists': team_data.get('assists', 1),
                'FG_made': team_data.get('FG_made', 1)
            }
            
            # Get team pace for this game's team
            team_pace = get_team_pace(season, team, self.db)
            if team_pace == 0:
                team_pace = lg_pace
            
            # Calculate PER for this game
            player_game_stats = {
                'min': min_played,
                'pts': stats.get('pts', 0),
                'fg_made': stats.get('fg_made', 0),
                'fg_att': stats.get('fg_att', 0),
                'three_made': stats.get('three_made', 0),
                'ft_made': stats.get('ft_made', 0),
                'ft_att': stats.get('ft_att', 0),
                'reb': stats.get('reb', 0),
                'oreb': stats.get('oreb', 0),
                'ast': stats.get('ast', 0),
                'stl': stats.get('stl', 0),
                'blk': stats.get('blk', 0),
                'to': stats.get('to', 0),
                'pf': stats.get('pf', 0)
            }
            
            uper = self.compute_uper(player_game_stats, team_stats, league_constants)
            aper = self.compute_aper(uper, team_pace, lg_pace)
            
            # Normalize to PER
            if use_normalization:
                per = self.compute_per(aper, lg_aper)
            else:
                per = aper
            
            # Calculate weight: MIN * exp(-days_since / k)
            recency_weight = np.exp(-days_since / recency_decay_k)
            weight = min_played * recency_weight
            
            # Add to weighted sum
            weighted_per_sum += per * weight
            total_weight += weight
        
        # Return weighted average
        if total_weight == 0:
            return None
        
        return weighted_per_sum / total_weight
    
    def get_player_recency_weighted_per(
        self,
        player_id: str,
        team: str,
        season: str,
        before_date: str,
        recency_decay_k: float = 15.0
    ) -> Optional[float]:
        """
        Get a player's recency-weighted PER using game-level PER calculations.
        
        For each game the player played:
        - Compute PER using that game's box score and team context
        - Weight by: MIN_g * exp(-days_since_game / k)
        - Aggregate: Σ (PER_g * w_g) / Σ w_g
        
        Args:
            player_id: Player ID (as string)
            team: Team name
            season: Season string
            before_date: Date string (YYYY-MM-DD) - stats up to but not including this date
            recency_decay_k: Decay constant for recency weighting (default 15.0)
        
        Returns:
            Recency-weighted PER (float) or None if player not found or insufficient data
        """
        from datetime import datetime
        
        logger = logging.getLogger(__name__)
        
        # Get all games for this player before the date
        if self._preloaded and self._player_stats_cache:
            # Use preloaded cache
            key = (team, season)
            if key not in self._player_stats_cache:
                return None
            
            player_games = [
                pg for pg in self._player_stats_cache[key]
                if (pg.get('player_id') == player_id or str(pg.get('player_id')) == str(player_id)) and
                   pg.get('date') and pg['date'] < before_date and
                   pg.get('stats', {}).get('min', 0) > 0
            ]
        else:
            # Fallback to DB query
            player_games = list(self.db.stats_nba_players.find({
                'player_id': player_id,
                'team': team,
                'season': season,
                'date': {'$lt': before_date},
                'stats.min': {'$gt': 0}
            }))
        
        if not player_games:
            return None
        
        # Sort by date
        player_games.sort(key=lambda x: x.get('date', ''))
        
        # Get league constants (same for all games in season)
        league_constants = get_league_constants(season, self.db)
        if not league_constants:
            return None
        
        lg_pace = league_constants.get('lg_pace', 95)
        
        # Get league average aPER for normalization
        lg_aper = self.compute_league_average_aper(season, before_date)
        use_normalization = lg_aper > 0
        
        # Parse game date for recency calculation
        try:
            game_date_obj = datetime.strptime(before_date, '%Y-%m-%d').date()
        except:
            return None
        
        # Calculate PER for each game and apply recency weighting
        weighted_per_sum = 0.0
        total_weight = 0.0
        
        for pg in player_games:
            game_date_str = pg.get('date')
            if not game_date_str:
                continue
            
            try:
                pg_date_obj = datetime.strptime(str(game_date_str), '%Y-%m-%d').date() if isinstance(game_date_str, str) else game_date_str
                if isinstance(pg_date_obj, str):
                    pg_date_obj = datetime.strptime(pg_date_obj, '%Y-%m-%d').date()
            except:
                continue
            
            # Calculate days since game
            days_since = (game_date_obj - pg_date_obj).days
            if days_since < 0:
                continue  # Skip future games (shouldn't happen, but safety check)
            
            # Get player stats for this game
            stats = pg.get('stats', {})
            min_played = stats.get('min', 0)
            if min_played == 0:
                continue
            
            # Get team stats for this specific game
            game_id = pg.get('game_id')
            if not game_id:
                continue
            
            game_doc = self.db.stats_nba.find_one({'game_id': game_id})
            if not game_doc:
                continue
            
            # Determine if player was on home or away team
            is_home = pg.get('home', False)
            team_data = game_doc.get('homeTeam' if is_home else 'awayTeam', {})
            
            # Get team stats for this game
            team_stats = {
                'assists': team_data.get('assists', 1),
                'FG_made': team_data.get('FG_made', 1)
            }
            
            # Get team pace for this game's team
            team_pace = get_team_pace(season, team, self.db)
            if team_pace == 0:
                team_pace = lg_pace
            
            # Calculate PER for this game
            player_game_stats = {
                'min': min_played,
                'pts': stats.get('pts', 0),
                'fg_made': stats.get('fg_made', 0),
                'fg_att': stats.get('fg_att', 0),
                'three_made': stats.get('three_made', 0),
                'ft_made': stats.get('ft_made', 0),
                'ft_att': stats.get('ft_att', 0),
                'reb': stats.get('reb', 0),
                'oreb': stats.get('oreb', 0),
                'ast': stats.get('ast', 0),
                'stl': stats.get('stl', 0),
                'blk': stats.get('blk', 0),
                'to': stats.get('to', 0),
                'pf': stats.get('pf', 0)
            }
            
            uper = self.compute_uper(player_game_stats, team_stats, league_constants)
            aper = self.compute_aper(uper, team_pace, lg_pace)
            
            # Normalize to PER
            if use_normalization:
                per = self.compute_per(aper, lg_aper)
            else:
                per = aper
            
            # Calculate weight: MIN * exp(-days_since / k)
            recency_weight = np.exp(-days_since / recency_decay_k)
            weight = min_played * recency_weight
            
            # Add to weighted sum
            weighted_per_sum += per * weight
            total_weight += weight
        
        # Return weighted average
        if total_weight == 0:
            return None
        
        return weighted_per_sum / total_weight
    
    def get_player_per_before_date(
        self,
        player_id: str,
        team: str,
        season: str,
        before_date: str
    ) -> Optional[float]:
        """
        Get a single player's PER (season-to-date) before a given date.
        Uses cache to avoid recalculating PER for the same player/team/season/date.
        
        Args:
            player_id: Player ID (as string)
            team: Team name
            season: Season string
            before_date: Date string (YYYY-MM-DD) - stats up to but not including this date
        
        Returns:
            Player's PER (float) or None if player not found or insufficient data
        """
        # Check cache first - this is critical for performance when computing PER for many injured players
        cache_key = (str(player_id), team, season, before_date)
        if cache_key in self._player_per_cache:
            cached_per = self._player_per_cache[cache_key]
            # Return None if cached value indicates no data (we use None for this)
            return cached_per if cached_per is not None else None
        
        # Get all players for the team before the date
        players = self._get_team_players_before_date_cached(team, season, before_date, min_games=1)
        
        # Find the specific player
        player_data = None
        for p in players:
            if str(p['_id']) == str(player_id):
                player_data = p
                break
        
        if not player_data or player_data['total_min'] == 0:
            # Cache None to indicate no data found
            self._player_per_cache[cache_key] = None
            return None
        
        # Get league constants and team stats
        league_constants = get_league_constants(season, self.db)
        team_stats = self._get_team_stats_before_date_cached(team, season, before_date)
        
        # Get team pace
        team_pace = get_team_pace(season, team, self.db)
        lg_pace = get_team_pace(season, None, self.db)  # League average pace
        if team_pace == 0:
            team_pace = lg_pace
        if lg_pace == 0:
            lg_pace = 100.0  # Fallback
        
        # Aggregate stats for PER calculation
        agg_stats = {
            'min': player_data['total_min'],
            'pts': player_data['total_pts'],
            'fg_made': player_data['total_fg_made'],
            'fg_att': player_data['total_fg_att'],
            'three_made': player_data['total_three_made'],
            'ft_made': player_data['total_ft_made'],
            'ft_att': player_data['total_ft_att'],
            'reb': player_data['total_reb'],
            'oreb': player_data['total_oreb'],
            'ast': player_data['total_ast'],
            'stl': player_data['total_stl'],
            'blk': player_data['total_blk'],
            'to': player_data['total_to'],
            'pf': player_data['total_pf']
        }
        
        # Compute PER
        uper = self.compute_uper(agg_stats, team_stats, league_constants)
        aper = self.compute_aper(uper, team_pace, lg_pace)
        
        # Get league average aPER for normalization
        lg_aper = self.compute_league_average_aper(season, before_date)
        if lg_aper > 0:
            per = self.compute_per(aper, lg_aper)
        else:
            per = aper  # Use aPER if normalization not available
        
        # Cache the computed PER value
        self._player_per_cache[cache_key] = per
        
        return per
    
    def _get_approximate_team_stats(
        self,
        team: str,
        season: str,
        before_date: str
    ) -> dict:
        """Get approximate team season totals for PER calculation."""
        return self._get_team_stats_before_date_cached(team, season, before_date)


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='PER Calculator CLI')
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Cache command
    cache_parser = subparsers.add_parser('cache', help='Manage PER feature cache')
    cache_parser.add_argument('action', choices=['show', 'clear', 'rebuild'],
                              help='Action to perform')
    cache_parser.add_argument('--season', '-s', type=str, help='Limit to specific season')
    
    # Team PER command
    team_parser = subparsers.add_parser('team', help='Get team PER features')
    team_parser.add_argument('team', type=str, help='Team name')
    team_parser.add_argument('--season', '-s', type=str, required=True, help='Season')
    team_parser.add_argument('--before', '-b', type=str, required=True, help='Before date')
    
    # Game PER command
    game_parser = subparsers.add_parser('game', help='Get game PER features')
    game_parser.add_argument('home', type=str, help='Home team')
    game_parser.add_argument('away', type=str, help='Away team')
    game_parser.add_argument('--season', '-s', type=str, required=True, help='Season')
    game_parser.add_argument('--date', '-d', type=str, required=True, help='Game date')
    
    args = parser.parse_args()
    
    if args.command == 'cache':
        calc = PERCalculator(preload=False)
        
        if args.action == 'show':
            cached = list(calc.db[CACHED_PER_COLLECTION].find({}))
            print(f"\nCached PER Features:")
            for doc in cached:
                print(f"  {doc['season']}: {doc.get('game_count', 0)} games, updated {doc.get('updated_at', 'N/A')}")
            if not cached:
                print("  (no cached data)")
        
        elif args.action == 'clear':
            calc.clear_cache(args.season)
            print(f"Cleared PER cache{' for ' + args.season if args.season else ''}")
        
        elif args.action == 'rebuild':
            print("Rebuilding PER cache requires running training. Use train.py train")
    
    elif args.command == 'team':
        print("Loading data...")
        calc = PERCalculator(preload=True)
        result = calc.compute_team_per_features(args.team, args.season, args.before)
        if result:
            print(f"\n{args.team} Team PER Features (before {args.before}):")
            print(f"  Team PER Average: {result['per_avg']:.2f}")
            print(f"  Team PER Weighted: {result['per_weighted']:.2f}")
            print(f"  Starters Average: {result['starters_avg']:.2f}")
            print(f"\n  Top 8 Players:")
            for i, p in enumerate(result['players'][:8], 1):
                starter = '*' if p['is_starter'] else ' '
                print(f"    {i}. {starter}{p['player_name']}: {p['aper']:.2f} PER ({p['games']} games, {p['avg_min']:.1f} mpg)")
        else:
            print("No data found")
    
    elif args.command == 'game':
        print("Loading data...")
        calc = PERCalculator(preload=True)
        result = calc.get_game_per_features(args.home, args.away, args.season, args.date)
        if result:
            print(f"\nGame PER Features: {args.away} @ {args.home}")
            print(f"  Home Team PER Avg: {result.get('player_team_per|season|avg|home', 0):.2f}")
            print(f"  Away Team PER Avg: {result.get('player_team_per|season|avg|away', 0):.2f}")
            print(f"  PER Differential: {result.get('player_team_per|season|avg|diff', 0):.2f}")
            print(f"\n  Weighted Differential: {result.get('player_team_per|season|weighted_MPG|diff', 0):.2f}")
            print(f"  Starters Differential: {result.get('player_starters_per|season|avg|diff', 0):.2f}")
        else:
            print("No data found")
    
    else:
        parser.print_help()

