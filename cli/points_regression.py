#!/usr/bin/env python3
"""
Points Regression Model for NBA Score Prediction

Predicts home_points and away_points with derived point_total_pred and point_diff_pred.
Uses Ridge Regression as primary model with support for ElasticNet, RandomForest, and XGBoost.
"""

import os
import json
import pickle
import math
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

# Optional imports for XGBoost
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except (ImportError, Exception) as e:
    # Catch ImportError and also XGBoostError (when OpenMP library is missing)
    XGBOOST_AVAILABLE = False
    if 'XGBoostError' in str(type(e).__name__) or 'libomp' in str(e).lower():
        import warnings
        warnings.warn(f"XGBoost is not available: {e}. Install OpenMP with 'brew install libomp' if needed.")

# Optional imports for SHAP
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

from nba_app.cli.Mongo import Mongo
from nba_app.cli.StatHandlerV2 import StatHandlerV2
from nba_app.cli.per_calculator import PERCalculator
from nba_app.cli.collection_to_dict import import_collection
from nba_app.cli.feature_name_parser import parse_feature_name

logger = logging.getLogger(__name__)


def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate MAPE (Mean Absolute Percentage Error)."""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


class PointsRegressionTrainer:
    """
    Trainer for NBA points regression model.
    
    Supports:
    - Ridge Regression (primary)
    - ElasticNet
    - RandomForest
    - XGBoost
    """
    
    # Default alphas for Ridge Regression
    # Reduced from 6 to 3 for faster experimentation (can be overridden)
    DEFAULT_RIDGE_ALPHAS = [1.0, 10.0, 100.0]
    
    # Default query for training data
    DEFAULT_QUERY = {
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']},
        'season': {
            '$gte': '2007-2008',
            '$nin': ['2011-2012', '2019-2020', '2020-2021']  # lockout + COVID seasons
        }
    }
    
    # Default recency decay constant for injury features
    DEFAULT_RECENCY_DECAY_K = 15.0
    
    def __init__(
        self,
        db=None,
        output_dir: str = './models/point_regression',
        reports_dir: str = './reports'
    ):
        """
        Initialize PointsRegressionTrainer.
        
        Args:
            db: MongoDB database connection
            output_dir: Directory to save model artifacts
            reports_dir: Directory to save diagnostic reports
        """
        self.db = db if db is not None else Mongo().db
        self.output_dir = output_dir
        self.reports_dir = reports_dir
        self.artifacts_dir = os.path.join(output_dir, 'artifacts')
        self.recency_decay_k = self.DEFAULT_RECENCY_DECAY_K
        
        # Create directories
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Caches for optimization (built during create_training_data)
        self._venue_location_cache = {}  # dict[venue_guid] -> (lat, lon)
        self._top_ppg_cache = {}  # dict[(team, season, date_str)] -> float
        
        # Initialize components
        self.stat_handler = None
        self.per_calculator = None
        self.scaler = None
        self.model = None
        self.feature_names = []
        self.target_type = 'home_away'  # 'home_away' or 'margin'
        
    def _create_model(self, model_type: str, **kwargs):
        """
        Create a regression model instance.
        
        Args:
            model_type: 'Ridge', 'ElasticNet', 'RandomForest', or 'XGBoost'
            **kwargs: Model-specific hyperparameters
            
        Returns:
            Model instance
        """
        if model_type == 'Ridge':
            alpha = kwargs.get('alpha', 1.0)
            return Ridge(alpha=alpha, random_state=42)
        elif model_type == 'ElasticNet':
            alpha = kwargs.get('alpha', 1.0)
            l1_ratio = kwargs.get('l1_ratio', 0.5)
            return ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42, max_iter=10000)
        elif model_type == 'RandomForest':
            n_estimators = kwargs.get('n_estimators', 100)
            max_depth = kwargs.get('max_depth', None)
            return RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'XGBoost':
            if not XGBOOST_AVAILABLE:
                raise ImportError("XGBoost is not installed. Install with: pip install xgboost")
            n_estimators = kwargs.get('n_estimators', 100)
            max_depth = kwargs.get('max_depth', 6)
            learning_rate = kwargs.get('learning_rate', 0.1)
            return xgb.XGBRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                n_jobs=-1
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def _get_base_features(self, game: dict, before_date: str) -> Dict:
        """
        Extract base team efficiency and pace features.
        
        Returns dict with keys like:
        - home_offRtg_szn_avg, away_offRtg_szn_avg
        - home_defRtg_szn_avg, away_defRtg_szn_avg
        - home_pace_szn_avg, away_pace_szn_avg
        - home_efg_szn_avg, away_efg_szn_avg
        - home_TOV_pct_szn_avg, away_TOV_pct_szn_avg
        - home_ORB_pct_szn_avg, away_ORB_pct_szn_avg
        - home_offRtg_last10, away_offRtg_last10
        - home_pace_last10, away_pace_last10
        - home_points_last5_avg, away_points_last5_avg
        - home_3PA_rate, away_3PA_rate (for interaction features)
        - home_3P_pct_allowed, away_3P_pct_allowed (opponent 3P% defense)
        """
        if self.stat_handler is None:
            # Initialize stat handler with required stat tokens
            stat_tokens = [
                'offRtgSznAvg', 'defRtgSznAvg', 'paceSznAvg',
                'effective_fg_percSznAvg', 'TO_metricSznAvg', 'total_rebSznAvg',
                'offRtgGames_10', 'paceGames_10', 'pointsGames_5',
                'three_madeSznAvg', 'three_attSznAvg', 'FG_attSznAvg'
            ]
            self.stat_handler = StatHandlerV2(
                statistics=stat_tokens,
                include_absolute=True,
                use_exponential_weighting=True,
                db=self.db
            )
        
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2024-2025')
        year = game.get('year', 2024)
        month = game.get('month', 1)
        day = game.get('day', 1)
        
        # Get stat averages using getStatAvgDiffs
        # Note: getStatAvgDiffs returns a dict, but we need to parse it properly
        # For now, we'll get games and compute stats manually
        home_games = self.stat_handler.get_team_games_before_date(home_team, year, month, day, season)
        away_games = self.stat_handler.get_team_games_before_date(away_team, year, month, day, season)
        
        features = {}
        
        # Helper function to compute team stats from games
        def compute_team_stats(games, team_name, is_home=True):
            if not games:
                return {}
            
            complete_games = [g for g in games if g.get('homeTeam', {}).get('points', 0) > 0]
            if not complete_games:
                return {}
            
            # Aggregate stats
            agg = {
                'points': 0, 'FG_made': 0, 'FG_att': 0, 'three_made': 0, 'three_att': 0,
                'FT_made': 0, 'FT_att': 0, 'off_reb': 0, 'total_reb': 0, 'TO': 0,
                'assists': 0, 'possessions': 0
            }
            against_agg = {
                'points': 0, 'FG_made': 0, 'FG_att': 0, 'three_made': 0, 'three_att': 0
            }
            
            for g in complete_games:
                if g['homeTeam']['name'] == team_name:
                    side = 'homeTeam'
                    opp = 'awayTeam'
                else:
                    side = 'awayTeam'
                    opp = 'homeTeam'
                
                team_data = g.get(side, {})
                opp_data = g.get(opp, {})
                
                agg['points'] += team_data.get('points', 0)
                agg['FG_made'] += team_data.get('FG_made', 0)
                agg['FG_att'] += team_data.get('FG_att', 0)
                agg['three_made'] += team_data.get('three_made', 0)
                agg['three_att'] += team_data.get('three_att', 0)
                agg['FT_made'] += team_data.get('FT_made', 0)
                agg['FT_att'] += team_data.get('FT_att', 0)
                agg['off_reb'] += team_data.get('off_reb', 0)
                agg['total_reb'] += team_data.get('total_reb', 0)
                agg['TO'] += team_data.get('TO', 0)
                agg['assists'] += team_data.get('assists', 0)
                
                # Possessions for this game
                fg_att = team_data.get('FG_att', 0)
                off_reb = team_data.get('off_reb', 0)
                to = team_data.get('TO', 0)
                ft_att = team_data.get('FT_att', 0)
                poss = fg_att - off_reb + to + 0.4 * ft_att
                agg['possessions'] += poss
                
                # Opponent stats (for defensive metrics)
                against_agg['points'] += opp_data.get('points', 0)
                against_agg['FG_made'] += opp_data.get('FG_made', 0)
                against_agg['FG_att'] += opp_data.get('FG_att', 0)
                against_agg['three_made'] += opp_data.get('three_made', 0)
                against_agg['three_att'] += opp_data.get('three_att', 0)
            
            n_games = len(complete_games)
            if n_games == 0:
                return {}
            
            # Compute rates and percentages
            stats = {}
            stats['offRtg'] = 100 * (agg['points'] / agg['possessions']) if agg['possessions'] > 0 else 0
            stats['defRtg'] = 100 * (against_agg['points'] / agg['possessions']) if agg['possessions'] > 0 else 0
            stats['pace'] = agg['possessions'] / n_games if n_games > 0 else 0
            stats['efg'] = (agg['FG_made'] + 0.5 * agg['three_made']) / agg['FG_att'] if agg['FG_att'] > 0 else 0
            stats['TOV_pct'] = agg['TO'] / agg['possessions'] if agg['possessions'] > 0 else 0
            stats['ORB_pct'] = agg['off_reb'] / (agg['off_reb'] + (agg['total_reb'] - agg['off_reb'])) if agg['total_reb'] > 0 else 0
            stats['3PA_rate'] = agg['three_att'] / agg['FG_att'] if agg['FG_att'] > 0 else 0
            stats['3P_pct_allowed'] = against_agg['three_made'] / against_agg['three_att'] if against_agg['three_att'] > 0 else 0
            stats['points_avg'] = agg['points'] / n_games
            
            return stats
        
        # Compute stats for both teams
        home_stats = compute_team_stats(home_games, home_team)
        away_stats = compute_team_stats(away_games, away_team)
        
        # Season averages
        features['home_offRtg_szn_avg'] = home_stats.get('offRtg', 0)
        features['away_offRtg_szn_avg'] = away_stats.get('offRtg', 0)
        features['home_defRtg_szn_avg'] = home_stats.get('defRtg', 0)
        features['away_defRtg_szn_avg'] = away_stats.get('defRtg', 0)
        features['home_pace_szn_avg'] = home_stats.get('pace', 0)
        features['away_pace_szn_avg'] = away_stats.get('pace', 0)
        features['home_efg_szn_avg'] = home_stats.get('efg', 0)
        features['away_efg_szn_avg'] = away_stats.get('efg', 0)
        features['home_TOV_pct_szn_avg'] = home_stats.get('TOV_pct', 0)
        features['away_TOV_pct_szn_avg'] = away_stats.get('TOV_pct', 0)
        features['home_ORB_pct_szn_avg'] = home_stats.get('ORB_pct', 0)
        features['away_ORB_pct_szn_avg'] = away_stats.get('ORB_pct', 0)
        features['home_3PA_rate'] = home_stats.get('3PA_rate', 0)
        features['away_3PA_rate'] = away_stats.get('3PA_rate', 0)
        features['home_3P_pct_allowed'] = home_stats.get('3P_pct_allowed', 0)
        features['away_3P_pct_allowed'] = away_stats.get('3P_pct_allowed', 0)
        
        # Last 10 games (simplified - use last 10 from season games)
        home_last10 = home_games[-10:] if len(home_games) >= 10 else home_games
        away_last10 = away_games[-10:] if len(away_games) >= 10 else away_games
        
        home_stats_10 = compute_team_stats(home_last10, home_team)
        away_stats_10 = compute_team_stats(away_last10, away_team)
        
        features['home_offRtg_last10'] = home_stats_10.get('offRtg', 0)
        features['away_offRtg_last10'] = away_stats_10.get('offRtg', 0)
        features['home_pace_last10'] = home_stats_10.get('pace', 0)
        features['away_pace_last10'] = away_stats_10.get('pace', 0)
        
        # Last 5 games points average
        home_last5 = home_games[-5:] if len(home_games) >= 5 else home_games
        away_last5 = away_games[-5:] if len(away_games) >= 5 else away_games
        
        home_points_5 = [g['homeTeam']['points'] if g['homeTeam']['name'] == home_team else g['awayTeam']['points'] 
                        for g in home_last5 if g.get('homeTeam', {}).get('points', 0) > 0]
        away_points_5 = [g['homeTeam']['points'] if g['homeTeam']['name'] == away_team else g['awayTeam']['points'] 
                        for g in away_last5 if g.get('homeTeam', {}).get('points', 0) > 0]
        
        features['home_points_last5_avg'] = np.mean(home_points_5) if home_points_5 else 0
        features['away_points_last5_avg'] = np.mean(away_points_5) if away_points_5 else 0
        
        return features
    
    def _get_player_availability_features(self, game: dict, before_date: str) -> Dict:
        """
        Get player availability features.
        
        Returns:
        - perWeighted_available (home, away)
        - startersPer_available (home, away)
        - top1PPG_available (home, away)
        - top1PPG_diff
        - perAvg_available (home, away)
        """
        if self.per_calculator is None:
            self.per_calculator = PERCalculator(db=self.db, preload=True)
        
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2024-2025')
        
        features = {}
        
        try:
            # Extract injured players from game document (training mode)
            home_injured = game.get('homeTeam', {}).get('injured_players', [])
            away_injured = game.get('awayTeam', {}).get('injured_players', [])
            home_injured_list = [str(pid) for pid in home_injured] if home_injured else None
            away_injured_list = [str(pid) for pid in away_injured] if away_injured else None
            
            # Get PER features for both teams
            home_per_features = self.per_calculator.compute_team_per_features(
                home_team, season, before_date, top_n=8,
                injured_players=home_injured_list
            )
            away_per_features = self.per_calculator.compute_team_per_features(
                away_team, season, before_date, top_n=8,
                injured_players=away_injured_list
            )
            
            if home_per_features:
                features['home_perWeighted_available'] = home_per_features.get('per_weighted', 0)
                features['home_startersPer_available'] = home_per_features.get('starters_avg', 0)  # Fixed key name
                features['home_perAvg_available'] = home_per_features.get('per_avg', 0)
                
                # Get top PPG player by querying stats_nba_players for this team before the game date
                top_ppg_home = self._get_top_ppg_for_team(home_team, season, before_date)
                features['home_top1PPG_available'] = top_ppg_home
            else:
                features['home_perWeighted_available'] = 0
                features['home_startersPer_available'] = 0
                features['home_perAvg_available'] = 0
                features['home_top1PPG_available'] = 0
            
            if away_per_features:
                features['away_perWeighted_available'] = away_per_features.get('per_weighted', 0)
                features['away_startersPer_available'] = away_per_features.get('starters_avg', 0)  # Fixed key name
                features['away_perAvg_available'] = away_per_features.get('per_avg', 0)
                
                # Get top PPG player by querying stats_nba_players for this team before the game date
                top_ppg_away = self._get_top_ppg_for_team(away_team, season, before_date)
                features['away_top1PPG_available'] = top_ppg_away
            else:
                features['away_perWeighted_available'] = 0
                features['away_startersPer_available'] = 0
                features['away_perAvg_available'] = 0
                features['away_top1PPG_available'] = 0
            
            # Calculate top1PPG_diff
            features['top1PPG_diff'] = features.get('home_top1PPG_available', 0) - features.get('away_top1PPG_available', 0)
            
        except Exception as e:
            logger.warning(f"Error computing PER features: {e}")
            # Set defaults
            for key in ['home_perWeighted_available', 'away_perWeighted_available',
                       'home_startersPer_available', 'away_startersPer_available',
                       'home_top1PPG_available', 'away_top1PPG_available',
                       'home_perAvg_available', 'away_perAvg_available', 'top1PPG_diff']:
                features[key] = 0
        
        return features
    
    def _get_contextual_features(self, game: dict, before_date: str) -> Dict:
        """
        Get contextual features: restDays, travelDistance (optional), b2b, homeCourt.
        """
        features = {}
        
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2024-2025')
        year = game.get('year', 2024)
        month = game.get('month', 1)
        day = game.get('day', 1)
        
        if self.stat_handler is None:
            self.stat_handler = StatHandlerV2(
                statistics=[],
                include_absolute=True,
                use_exponential_weighting=True,
                db=self.db
            )
        
        # Home court advantage (1 for home team)
        features['homeCourt'] = 1
        
        # Get rest days from game history
        target_date = date(year, month, day)
        
        # Get last game for each team
        home_games = self.stat_handler.get_team_games_before_date(home_team, year, month, day, season)
        away_games = self.stat_handler.get_team_games_before_date(away_team, year, month, day, season)
        
        # Find most recent game date for each team
        def get_last_game_date(games, team_name):
            for g in reversed(games):
                if g.get('homeTeam', {}).get('points', 0) > 0:  # Only complete games
                    game_date_str = g.get('date')
                    if game_date_str:
                        try:
                            return datetime.strptime(game_date_str, '%Y-%m-%d').date()
                        except:
                            pass
            return None
        
        home_last_date = get_last_game_date(home_games, home_team)
        away_last_date = get_last_game_date(away_games, away_team)
        
        if home_last_date:
            features['home_restDays'] = (target_date - home_last_date).days
        else:
            features['home_restDays'] = 7  # Default if no prior game
        
        if away_last_date:
            features['away_restDays'] = (target_date - away_last_date).days
        else:
            features['away_restDays'] = 7  # Default if no prior game
        
        # Back-to-back: game yesterday
        yesterday = target_date - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        home_b2b = any(g.get('date') == yesterday_str and g.get('homeTeam', {}).get('points', 0) > 0 
                      for g in home_games)
        away_b2b = any(g.get('date') == yesterday_str and g.get('homeTeam', {}).get('points', 0) > 0 
                      for g in away_games)
        
        features['home_b2b'] = 1 if home_b2b else 0
        features['away_b2b'] = 1 if away_b2b else 0
        
        # Travel distance: calculate distance from team's last game venue to this game's venue
        features['travelDistance'] = self._calculate_travel_distance(away_team, game, before_date)
        
        return features
    
    def _get_interaction_features(self, base_features: Dict) -> Dict:
        """
        Create interaction features.
        
        - threePointMatchup = team_3PA_rate * opp_3P%Allowed
        - projectedPace = (pace + opp_pace) / 2
        """
        features = {}
        
        # threePointMatchup: team's 3PA rate * opponent's 3P% allowed
        home_3pa_rate = base_features.get('home_3PA_rate', 0)
        away_3p_pct_allowed = base_features.get('away_3P_pct_allowed', 0)
        features['home_threePointMatchup'] = home_3pa_rate * away_3p_pct_allowed
        
        away_3pa_rate = base_features.get('away_3PA_rate', 0)
        home_3p_pct_allowed = base_features.get('home_3P_pct_allowed', 0)
        features['away_threePointMatchup'] = away_3pa_rate * home_3p_pct_allowed
        
        # Projected pace: average of both teams' pace
        home_pace = base_features.get('home_pace_szn_avg', 0)
        away_pace = base_features.get('away_pace_szn_avg', 0)
        features['projectedPace'] = (home_pace + away_pace) / 2 if (home_pace > 0 and away_pace > 0) else 0
        
        return features
    
    def _build_top_ppg_cache(self, games: list):
        """
        Precompute top PPG for all team/season/date combinations needed for the games.
        This avoids per-game DB queries.
        """
        # Collect all unique (team, season, date) combinations from games
        team_season_dates = set()
        for game in games:
            home_team = game.get('homeTeam', {}).get('name')
            away_team = game.get('awayTeam', {}).get('name')
            season = game.get('season', '2024-2025')
            year = game.get('year', 2024)
            month = game.get('month', 1)
            day = game.get('day', 1)
            before_date = f"{year}-{month:02d}-{day:02d}"
            
            if home_team:
                team_season_dates.add((home_team, season, before_date))
            if away_team:
                team_season_dates.add((away_team, season, before_date))
        
        # Get all unique teams and seasons
        teams_seasons = {}
        for team, season, date_str in team_season_dates:
            if (team, season) not in teams_seasons:
                teams_seasons[(team, season)] = []
            teams_seasons[(team, season)].append(date_str)
        
        # For each team/season, get all player stats and compute PPG per date
        print(f"    Computing top PPG for {len(teams_seasons)} team/season combinations...")
        for (team, season), dates in teams_seasons.items():
            # Get all player stats for this team/season
            player_stats = list(self.db.stats_nba_players.find(
                {
                    'team': team,
                    'season': season,
                    'stats.min': {'$gt': 0}
                },
                {'player_id': 1, 'date': 1, 'stats.pts': 1}
            ))
            
            if not player_stats:
                continue
            
            # Sort dates for this team/season
            dates_sorted = sorted(set(dates))
            
            # For each date, compute top PPG from players who played before that date
            for before_date in dates_sorted:
                # Filter to players who played before this date
                players_before_date = {}
                for ps in player_stats:
                    ps_date = ps.get('date', '')
                    if ps_date and ps_date < before_date:
                        player_id = ps.get('player_id')
                        pts = ps.get('stats', {}).get('pts', 0)
                        
                        if player_id not in players_before_date:
                            players_before_date[player_id] = {'total_points': 0, 'games': 0}
                        players_before_date[player_id]['total_points'] += pts
                        players_before_date[player_id]['games'] += 1
                
                # Calculate PPG for each player and find max
                max_ppg = 0.0
                for player_id, stats in players_before_date.items():
                    if stats['games'] > 0:
                        ppg = stats['total_points'] / stats['games']
                        if ppg > max_ppg:
                            max_ppg = ppg
                
                # Cache the result
                self._top_ppg_cache[(team, season, before_date)] = max_ppg
    
    def _get_top_ppg_for_team(self, team: str, season: str, before_date: str) -> float:
        """
        Get the highest PPG for a team before a given date.
        Uses precomputed cache if available, otherwise falls back to DB query.
        
        Args:
            team: Team name
            season: Season string
            before_date: Date string in YYYY-MM-DD format (exclusive)
        
        Returns:
            Highest PPG value for any player on the team before the given date, or 0.0 if no data
        """
        # Check cache first
        cache_key = (team, season, before_date)
        if cache_key in self._top_ppg_cache:
            return self._top_ppg_cache[cache_key]
        
        # Fallback to DB query if not in cache (shouldn't happen if cache was built properly)
        try:
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
                        'total_points': {'$sum': '$stats.pts'},
                        'games_played': {'$sum': 1}
                    }
                },
                {
                    '$match': {
                        'games_played': {'$gt': 0}
                    }
                },
                {
                    '$project': {
                        'ppg': {'$divide': ['$total_points', '$games_played']},
                        'games_played': 1
                    }
                },
                {
                    '$sort': {'ppg': -1}
                },
                {
                    '$limit': 1
                }
            ]
            
            result = list(self.db.stats_nba_players.aggregate(pipeline))
            
            if result and len(result) > 0:
                top_ppg = result[0].get('ppg', 0)
                ppg_value = float(top_ppg) if top_ppg else 0.0
                # Cache for future use
                self._top_ppg_cache[cache_key] = ppg_value
                return ppg_value
            else:
                logger.debug(f"No PPG data found for {team} before {before_date}")
                self._top_ppg_cache[cache_key] = 0.0
                return 0.0
                
        except Exception as e:
            logger.warning(f"Error calculating top PPG for {team}: {e}")
            self._top_ppg_cache[cache_key] = 0.0
            return 0.0
    
    def _build_venue_location_cache(self):
        """Precompute venue locations to avoid per-game DB queries."""
        print("    Loading venue locations...")
        venues = list(self.db.nba_venues.find(
            {'location': {'$exists': True}},
            {'venue_guid': 1, 'location.lat': 1, 'location.lon': 1}
        ))
        
        for venue in venues:
            venue_guid = venue.get('venue_guid')
            location = venue.get('location', {})
            lat = location.get('lat')
            lon = location.get('lon')
            if venue_guid and lat is not None and lon is not None:
                self._venue_location_cache[venue_guid] = (lat, lon)
    
    def _calculate_travel_distance(self, away_team: str, game: dict, before_date: str) -> float:
        """
        Calculate travel distance for the away team from their last game venue to this game's venue.
        Uses precomputed cache for venue locations.
        
        Args:
            away_team: Away team name
            game: Current game dictionary
            before_date: Date string in YYYY-MM-DD format
        
        Returns:
            Distance in miles (or 0.0 if unable to calculate)
        """
        try:
            # Get current game's venue
            current_venue_guid = game.get('venue_guid')
            if not current_venue_guid:
                logger.debug(f"Travel distance: Current game missing venue_guid for {away_team} on {before_date}")
                return 0.0
            
            # Get venue location from cache
            current_location = self._venue_location_cache.get(current_venue_guid)
            if not current_location:
                # Fallback to DB query if not in cache
                current_venue = self.db.nba_venues.find_one({'venue_guid': current_venue_guid})
                if not current_venue:
                    logger.debug(f"Travel distance: Venue {current_venue_guid} not found in nba_venues collection")
                    return 0.0
                if 'location' not in current_venue:
                    logger.debug(f"Travel distance: Venue {current_venue_guid} missing location data")
                    return 0.0
                current_lat = current_venue['location'].get('lat')
                current_lon = current_venue['location'].get('lon')
                if current_lat is None or current_lon is None:
                    logger.debug(f"Travel distance: Venue {current_venue_guid} has None lat/lon")
                    return 0.0
                current_location = (current_lat, current_lon)
                self._venue_location_cache[current_venue_guid] = current_location
            
            current_lat, current_lon = current_location
            
            # Find away team's last game before this date
            year = game.get('year', 2024)
            month = game.get('month', 1)
            day = game.get('day', 1)
            season = game.get('season', '2024-2025')
            
            # Get team's games before this date (now includes venue_guid from import_collection)
            if self.stat_handler is None:
                self.stat_handler = StatHandlerV2(
                    statistics=[],
                    include_absolute=True,
                    use_exponential_weighting=True,
                    db=self.db
                )
            
            away_games = self.stat_handler.get_team_games_before_date(away_team, year, month, day, season)
            
            # Find most recent game with a venue_guid (where the game was completed)
            last_venue_guid = None
            for g in reversed(away_games):
                # Check if game was completed (has points for both teams)
                home_points = g.get('homeTeam', {}).get('points', 0)
                away_points = g.get('awayTeam', {}).get('points', 0)
                venue_guid = g.get('venue_guid')
                if venue_guid and home_points > 0 and away_points > 0:
                    last_venue_guid = venue_guid
                    break
            
            if not last_venue_guid:
                # No previous game with venue, return 0
                logger.debug(f"Travel distance: No previous game with venue_guid found for {away_team} (checked {len(away_games)} games)")
                return 0.0
            
            # Get last game's venue location from cache
            last_location = self._venue_location_cache.get(last_venue_guid)
            if not last_location:
                # Fallback to DB query if not in cache
                last_venue = self.db.nba_venues.find_one({'venue_guid': last_venue_guid})
                if not last_venue or 'location' not in last_venue:
                    return 0.0
                last_lat = last_venue['location'].get('lat')
                last_lon = last_venue['location'].get('lon')
                if last_lat is None or last_lon is None:
                    return 0.0
                last_location = (last_lat, last_lon)
                self._venue_location_cache[last_venue_guid] = last_location
            
            last_lat, last_lon = last_location
            
            # Calculate distance using Haversine formula
            distance = self._haversine_distance(last_lat, last_lon, current_lat, current_lon)
            return distance
            
        except Exception as e:
            logger.warning(f"Error calculating travel distance: {e}")
            return 0.0
    
    def _get_injury_features(self, game: dict, before_date: str) -> Dict:
        """
        Get injury impact features for the game.
        
        Args:
            game: Game dictionary
            before_date: Date string in YYYY-MM-DD format
        
        Returns:
            Dict with injury feature values
        """
        if not self.stat_handler:
            return {}
        
        try:
            home_team = game['homeTeam']['name']
            away_team = game['awayTeam']['name']
            season = game.get('season', '2024-2025')
            year = game.get('year', 2024)
            month = game.get('month', 1)
            day = game.get('day', 1)
            
            # Get injury features from StatHandlerV2
            injury_features = self.stat_handler.get_injury_features(
                HOME=home_team,
                AWAY=away_team,
                season=season,
                year=year,
                month=month,
                day=day,
                game_doc=game,
                per_calculator=self.per_calculator,
                recency_decay_k=self.recency_decay_k
            )
            
            return injury_features
        except Exception as e:
            logger.warning(f"Error calculating injury features: {e}")
            return {}
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth using Haversine formula.
        
        Args:
            lat1, lon1: Latitude and longitude of first point (in degrees)
            lat2, lon2: Latitude and longitude of second point (in degrees)
        
        Returns:
            Distance in miles
        """
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Earth radius in miles
        R = 3958.8
        
        return R * c
    
    def _build_feature_vector(self, game: dict, before_date: str, selected_features: List[str] = None) -> Tuple[np.ndarray, List[str]]:
        """
        Build flattened feature vector for a game.
        
        Supports both old format (home_offRtg_szn_avg) and new format (off_rtg|season|avg|home).
        If selected_features are in new format (contain '|'), uses StatHandlerV2.calculate_feature().
        Otherwise, uses legacy methods (_get_base_features, etc.).
        
        Args:
            game: Game dictionary
            before_date: Date string
            selected_features: Optional list of feature names to include. If None, includes all features.
        
        Returns:
            Tuple of (feature_vector, feature_names)
        """
        # Always use new format - old format is no longer supported
        if selected_features and len(selected_features) > 0:
            # Check if features use new format (contain '|')
            use_new_format = any('|' in f for f in selected_features)
            if not use_new_format:
                raise ValueError("Old format features are no longer supported. All features must use the new pipe-delimited format.")
        
        # NEW FORMAT: Use StatHandlerV2.calculate_feature() directly (like NBAModel)
        return self._build_feature_vector_new_format(game, before_date, selected_features)
    
    def _build_feature_vector_new_format(self, game: dict, before_date: str, selected_features: List[str] = None) -> Tuple[np.ndarray, List[str]]:
        """
        Build feature vector using new format (off_rtg|season|avg|home).
        Uses StatHandlerV2.calculate_feature() similar to NBAModel.
        """
        # Initialize StatHandlerV2 if needed
        if self.stat_handler is None:
            # StatHandlerV2 doesn't need specific stat tokens for new format - it parses feature names
            self.stat_handler = StatHandlerV2(
                statistics=[],  # Empty - calculate_feature will parse feature names
                include_absolute=True,
                use_exponential_weighting=True,
                db=self.db
            )
        
        # Initialize PER calculator if needed (for PER features)
        if self.per_calculator is None:
            # Only initialize if PER features are needed
            if selected_features and any(f.startswith('player_') or 'per' in f.lower() for f in selected_features):
                self.per_calculator = PERCalculator(db=self.db, preload=False)  # Don't preload for single prediction
        
        home_team = game.get('homeTeam', {}).get('name')
        away_team = game.get('awayTeam', {}).get('name')
        season = game.get('season', '2024-2025')
        year = game.get('year', 2024)
        month = game.get('month', 1)
        day = game.get('day', 1)
        
        if not home_team or not away_team:
            raise ValueError(f"Game missing home_team or away_team: {game}")
        
        # Build features dict by calculating each feature directly
        all_features = {}
        
        if selected_features is None:
            # If no selection, we can't build features (need to know which ones)
            raise ValueError("selected_features must be provided when using new format")
        
        # Calculate each selected feature
        for feature_name in selected_features:
            try:
                # Handle pred_* features - these are not available at prediction time (circular dependency)
                if feature_name.startswith('pred_'):
                    all_features[feature_name] = 0.0
                    logger.debug(f"Point prediction feature {feature_name} not available during points prediction, setting to 0.0")
                    continue
                
                # Parse feature name to check format
                components = parse_feature_name(feature_name)
                
                # Handle injury features - use get_injury_features for better performance
                if components and components.stat_name.startswith('inj_'):
                    try:
                        game_doc = game if isinstance(game, dict) else None
                        injury_features = self.stat_handler.get_injury_features(
                            home_team, away_team, season, year, month, day,
                            game_doc=game_doc,
                            per_calculator=self.per_calculator,
                            recency_decay_k=self.recency_decay_k
                        )
                        if injury_features and feature_name in injury_features:
                            all_features[feature_name] = injury_features[feature_name]
                        else:
                            all_features[feature_name] = 0.0
                    except Exception as e:
                        logger.warning(f"Error calculating injury feature {feature_name}: {e}")
                        all_features[feature_name] = 0.0
                    continue
                
                # Handle PER features - points model typically doesn't use these, but handle gracefully
                if components and (components.stat_name.startswith('player_') or components.stat_name == 'per_available'):
                    # PER features require player filters - not available at prediction time for points model
                    # Set to 0 (points model shouldn't use PER features, but handle gracefully)
                    all_features[feature_name] = 0.0
                    logger.debug(f"PER feature {feature_name} not supported in points prediction without player filters, setting to 0.0")
                    continue
                
                # All other features (regular stats, enhanced features, special features like elo/rest)
                # Use calculate_feature which handles all cases automatically
                try:
                    value = self.stat_handler.calculate_feature(
                        feature_name, home_team, away_team, season, year, month, day, self.per_calculator
                    )
                    all_features[feature_name] = value if value is not None and not (isinstance(value, float) and (np.isnan(value) or np.isinf(value))) else 0.0
                except Exception as e:
                    logger.warning(f"Error calculating feature {feature_name}: {e}")
                    all_features[feature_name] = 0.0
                    
            except Exception as e:
                logger.warning(f"Error processing feature {feature_name}: {e}")
                all_features[feature_name] = 0.0
        
        # Build feature vector in the order specified by selected_features (preserve order)
        feature_vector = np.array([all_features.get(name, 0.0) for name in selected_features])
        feature_names = selected_features.copy()
        
        return feature_vector, feature_names
    
    def create_training_data(self, query: dict = None, selected_features: List[str] = None, progress_callback: callable = None, limit: int = None) -> pd.DataFrame:
        """
        Create training data DataFrame from MongoDB games.
        
        Args:
            query: MongoDB query filter
            selected_features: Optional list of feature names to include
            progress_callback: Optional callback function(current, total, progress_pct) for progress updates
            limit: Optional limit on number of games to process (for testing/debugging). If None, processes all games.
        
        Returns:
            DataFrame with features and targets (home_points, away_points)
        """
        query = query or self.DEFAULT_QUERY
        
        # Fetch games
        print("  Fetching games from database...")
        all_games = list(self.db.stats_nba.find(query).sort([('year', 1), ('month', 1), ('day', 1)]))
        total_games_available = len(all_games)
        
        # Apply limit if specified
        if limit is not None and limit > 0:
            games = all_games[:limit]
            print(f"  Found {total_games_available} games, limiting to {len(games)} games")
        else:
            games = all_games
            print(f"  Found {total_games_available} games")
        logger.info(f"Processing {len(games)} games for training (limit={limit})")
        
        # Precompute caches to avoid per-game DB queries
        print("  Building caches (venue locations, top PPG)...")
        self._build_venue_location_cache()
        self._build_top_ppg_cache(games)
        print(f"    Cached {len(self._venue_location_cache)} venues")
        print(f"    Cached {len(self._top_ppg_cache)} team/season/date combinations")
        
        # Preload injury cache if injury features are needed (check if any selected feature starts with 'inj_')
        needs_injury_features = False
        if selected_features:
            needs_injury_features = any(f.startswith('inj_') for f in selected_features)
        else:
            # If no selection, include all features including injuries
            needs_injury_features = True
        
        if needs_injury_features and self.stat_handler:
            print("  Preloading injury feature cache...")
            self.stat_handler.preload_injury_cache(games)
            print("    Injury cache preloaded")
        
        X_list = []
        y_home = []
        y_away = []
        metadata = []
        
        total_games_to_process = len(games)
        print("  Processing games and building features...")
        for i, game in enumerate(games):
            try:
                year = game.get('year', 0)
                month = game.get('month', 0)
                day = game.get('day', 0)
                before_date = f"{year}-{month:02d}-{day:02d}"
                
                # Build feature vector
                feature_vector, feature_names = self._build_feature_vector(game, before_date, selected_features)
                
                # Store feature names (should be same for all games)
                if not self.feature_names:
                    self.feature_names = feature_names
                
                # Get targets
                home_points = game.get('homeTeam', {}).get('points', 0)
                away_points = game.get('awayTeam', {}).get('points', 0)
                
                if home_points > 0 and away_points > 0:
                    X_list.append(feature_vector)
                    y_home.append(home_points)
                    y_away.append(away_points)
                    metadata.append({
                        'year': year,
                        'month': month,
                        'day': day,
                        'home': game['homeTeam']['name'],
                        'away': game['awayTeam']['name']
                    })
                
                # Progress callback (use limited total for progress calculation)
                if progress_callback and ((i + 1) % 50 == 0 or i == 0 or i == total_games_to_process - 1):
                    progress_pct = ((i + 1) / total_games_to_process * 100) if total_games_to_process > 0 else 0
                    progress_callback(i + 1, total_games_to_process, progress_pct)
            except Exception as e:
                logger.warning(f"Error processing game: {e}")
                continue
        
        # Create DataFrame
        print("  Creating DataFrame...")
        X = np.array(X_list)
        df = pd.DataFrame(X, columns=self.feature_names)
        df['home_points'] = y_home
        df['away_points'] = y_away
        
        # Add metadata
        for i, meta in enumerate(metadata):
            df.loc[i, 'Year'] = meta['year']
            df.loc[i, 'Month'] = meta['month']
            df.loc[i, 'Day'] = meta['day']
            df.loc[i, 'Home'] = meta['home']
            df.loc[i, 'Away'] = meta['away']
        
        print(f"  Successfully created training data: {len(df)} games, {len(self.feature_names)} features")
        logger.info(f"Created training data: {len(df)} games, {len(self.feature_names)} features")
        return df
    
    def load_training_data_from_csv(self, csv_path: str, selected_features: List[str] = None) -> pd.DataFrame:
        """
        Load training data from a CSV file (e.g., extracted from master training data).
        
        Args:
            csv_path: Path to CSV file
            selected_features: Optional list of feature names to use (if None, uses all features in CSV)
            
        Returns:
            DataFrame with features and targets
        """
        # Read CSV with error handling
        try:
            df = pd.read_csv(csv_path, on_bad_lines='skip', engine='python')
        except TypeError:
            # Older pandas versions
            try:
                df = pd.read_csv(csv_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
            except:
                # Fallback: use csv module
                import csv
                rows = []
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    for row in reader:
                        if len(row) == len(header):
                            rows.append(row)
                df = pd.DataFrame(rows, columns=header)
                # Convert numeric columns
                for col in df.columns:
                    if col not in ['Home', 'Away']:
                        try:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                        except:
                            pass
        
        # Meta columns that should always be included
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'home_points', 'away_points']
        
        # Filter to selected features if provided
        if selected_features:
            # Check which requested features exist in CSV
            available_features = [f for f in selected_features if f in df.columns]
            missing_features = [f for f in selected_features if f not in df.columns]
            
            if missing_features:
                logger.warning(f"Requested features not found in CSV: {missing_features}")
            
            # Extract columns: meta + available features
            columns_to_keep = meta_cols + available_features
            df = df[columns_to_keep]
            self.feature_names = available_features
        else:
            # Use all features in CSV (excluding meta columns)
            self.feature_names = [col for col in df.columns if col not in meta_cols]
        
        logger.info(f"Loaded training data from CSV: {len(df)} games, {len(self.feature_names)} features")
        return df
    
    def train(
        self,
        model_type: str = 'Ridge',
        alphas: List[float] = None,
        selected_features: List[str] = None,
        training_csv: str = None,
        target: str = 'home_away',
        use_time_calibration: bool = False,
        calibration_years: List[int] = None,
        evaluation_year: int = None,
        begin_year: int = None,
        **model_kwargs
    ) -> Dict:
        """
        Train the points regression model.
        
        Args:
            model_type: 'Ridge', 'ElasticNet', 'RandomForest', or 'XGBoost'
            alphas: List of alpha values for Ridge/ElasticNet (only used if model_type is Ridge)
            selected_features: List of feature names to use (only used if training_csv is None)
            training_csv: Optional path to CSV file to load training data from (e.g., extracted from master)
            target: 'home_away' (default) trains separate models for home/away points, 'margin' trains single model on margin (home - away)
            use_time_calibration: If True, use year-based temporal splits (train/calibrate/evaluate) instead of TimeSeriesSplit CV
            calibration_years: List of season start years for calibration set (e.g., [2023] means 2023-2024 season)
            evaluation_year: Season start year for evaluation set (e.g., 2024 means 2024-2025 season)
            begin_year: Minimum season start year to include (e.g., 2012 means >= 2012-2013 season)
            **model_kwargs: Additional model-specific hyperparameters
            
        Returns:
            Dictionary with training results and metrics
        """
        # Load training data from CSV if provided, otherwise create from MongoDB
        if training_csv and os.path.exists(training_csv):
            df = self.load_training_data_from_csv(training_csv, selected_features=selected_features)
        else:
            df = self.create_training_data(selected_features=selected_features)
        
        # Filter by begin_year if provided (safety measure in case CSV wasn't filtered during extraction)
        if begin_year is not None:
            # Calculate SeasonStartYear: Oct-Dec belong to that calendar year's season,
            # Jan-Jun belong to the previous calendar year's season
            df = df.copy()
            df['SeasonStartYear'] = np.where(df['Month'] >= 10, df['Year'], df['Year'] - 1)
            initial_count = len(df)
            df = df[df['SeasonStartYear'] >= int(begin_year)]
            filtered_count = len(df)
            if filtered_count < initial_count:
                logger.info(f"Filtered dataset by begin_year={begin_year}: {initial_count} -> {filtered_count} rows")
            # Drop SeasonStartYear column after filtering (it's a helper column)
            df = df.drop('SeasonStartYear', axis=1)
        
        # Separate features and targets
        feature_cols = [col for col in df.columns if col not in 
                       ['home_points', 'away_points', 'Year', 'Month', 'Day', 'Home', 'Away']]
        X = df[feature_cols].values
        y_home = df['home_points'].values
        y_away = df['away_points'].values
        
        # Sort by date for consistent ordering
        date_cols = ['Year', 'Month', 'Day']
        df_sorted = df.sort_values(date_cols)
        sort_idx = df_sorted.index
        df = df_sorted.reset_index(drop=True)
        X = X[sort_idx]
        y_home = y_home[sort_idx]
        y_away = y_away[sort_idx]
        
        # Standardize features (fit on full dataset for consistency)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Determine split strategy
        use_time_based_split = use_time_calibration and calibration_years is not None and evaluation_year is not None
        
        print(f"[PointsRegressionTrainer.train] Split strategy determination:")
        print(f"  use_time_calibration parameter: {use_time_calibration} (type: {type(use_time_calibration)})")
        print(f"  calibration_years: {calibration_years} (type: {type(calibration_years)})")
        print(f"  evaluation_year: {evaluation_year} (type: {type(evaluation_year)})")
        print(f"  use_time_based_split: {use_time_based_split}")
        
        if not use_time_based_split:
            print(f"[PointsRegressionTrainer.train] WARNING: Time-based split is DISABLED. Reason: use_time_calibration={use_time_calibration}, calibration_years={calibration_years}, evaluation_year={evaluation_year}")
            print(f"[PointsRegressionTrainer.train] WARNING: This will use TimeSeriesSplit CV and evaluate on full dataset, which can give negative R²")
        
        # Prepare time-based splits if using calibration
        if use_time_based_split:
            # Calculate SeasonStartYear for each row (Oct-Dec belong to that year's season, Jan-Jun belong to previous year)
            df['SeasonStartYear'] = np.where(df['Month'] >= 10, df['Year'], df['Year'] - 1)
            
            # Convert calibration_years to list if single value
            if not isinstance(calibration_years, list):
                cal_seasons = [int(calibration_years)]
            else:
                cal_seasons = [int(y) for y in calibration_years]
            eval_season = int(evaluation_year)
            earliest_cal_year = min(cal_seasons)
            
            # Split by season boundaries:
            # Train: All data before earliest calibration_year (SeasonStartYear < earliest_cal_year, e.g., < 2022 means before 2022-2023 season)
            # Calibrate: Data from all calibration_years (SeasonStartYear in calibration_years, e.g., [2023] means 2023-2024 season)
            # Evaluate: Data from evaluation_year (SeasonStartYear == evaluation_year, e.g., 2024 means 2024-2025 season)
            train_mask = df['SeasonStartYear'] < earliest_cal_year
            cal_mask = df['SeasonStartYear'].isin(cal_seasons)
            eval_mask = df['SeasonStartYear'] == eval_season
            
            train_idx = np.where(train_mask)[0]
            cal_idx = np.where(cal_mask)[0]
            eval_idx = np.where(eval_mask)[0]
            
            print(f"[PointsRegressionTrainer.train] Time-based calibration splits:")
            print(f"  Train set: {len(train_idx)} games (SeasonStartYear < {earliest_cal_year}, seasons before {earliest_cal_year}-{earliest_cal_year+1})")
            print(f"  Calibration set: {len(cal_idx)} games (SeasonStartYear in {cal_seasons}, seasons {[f'{y}-{y+1}' for y in cal_seasons]})")
            print(f"  Evaluation set: {len(eval_idx)} games (SeasonStartYear == {eval_season}, season {eval_season}-{eval_season+1})")
            print(f"  Total dataset: {len(df)} games")
            
            if len(train_idx) == 0:
                logger.warning(f"Training set is empty! Check begin_year and calibration_years. Earliest cal year: {earliest_cal_year}")
            if len(cal_idx) == 0:
                logger.warning(f"Calibration set is empty! Check calibration_years: {calibration_years}")
            if len(eval_idx) == 0:
                logger.warning(f"Evaluation set is empty! Check evaluation_year: {evaluation_year}")
        else:
            # Use TimeSeriesSplit CV (default behavior)
            tscv = TimeSeriesSplit(n_splits=3)
            train_idx = None
            cal_idx = None
            eval_idx = None
        
        results = []
        selected_alpha = None  # Will be set for Ridge models
        alphas_tested = None  # Will be set for Ridge models
        
        # Handle margin-only target
        if target == 'margin':
            # Calculate margin target (home - away)
            y_margin = y_home - y_away
            self.target_type = 'margin'
            
            # Train single model on margin
            if model_type == 'Ridge':
                alphas = alphas or self.DEFAULT_RIDGE_ALPHAS
                
                if use_time_based_split:
                    # Time-based calibration: train on train set, evaluate on calibration set, report evaluation set metrics
                    X_train_split = X_scaled[train_idx]
                    y_train_m_split = y_margin[train_idx]
                    X_cal_split = X_scaled[cal_idx] if len(cal_idx) > 0 else None
                    y_cal_m_split = y_margin[cal_idx] if len(cal_idx) > 0 else None
                    X_eval_split = X_scaled[eval_idx] if len(eval_idx) > 0 else None
                    y_eval_m_split = y_margin[eval_idx] if len(eval_idx) > 0 else None
                    
                    # Train models for each alpha value on training set
                    for alpha in alphas:
                        logger.info(f"Training Ridge (margin-only) with alpha={alpha} using time-based calibration")
                        
                        margin_model = Ridge(alpha=alpha, random_state=42)
                        margin_model.fit(X_train_split, y_train_m_split)
                        
                        # Evaluate on calibration set (for hyperparameter selection)
                        if X_cal_split is not None and len(X_cal_split) > 0:
                            y_pred_cal = margin_model.predict(X_cal_split)
                            cal_mae = mean_absolute_error(y_cal_m_split, y_pred_cal)
                            cal_rmse = np.sqrt(mean_squared_error(y_cal_m_split, y_pred_cal))
                            cal_r2 = r2_score(y_cal_m_split, y_pred_cal)
                        else:
                            cal_mae = cal_rmse = cal_r2 = np.nan
                        
                        result = {
                            'alpha': alpha,
                            'margin_mae': cal_mae,  # Calibration set MAE for hyperparameter selection
                            'margin_rmse': cal_rmse,
                            'margin_r2': cal_r2,
                            'margin_model': margin_model
                        }
                        results.append(result)
                    
                    # Select best alpha (lowest margin MAE on calibration set)
                    best_result = min(results, key=lambda x: x['margin_mae'] if not np.isnan(x['margin_mae']) else float('inf'))
                    selected_alpha = best_result.get('alpha')
                    alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None] if results else None
                    self.model = best_result['margin_model']
                    
                    # Evaluate on evaluation set
                    if X_eval_split is not None and len(X_eval_split) > 0:
                        y_pred_eval = self.model.predict(X_eval_split)
                        eval_mae = mean_absolute_error(y_eval_m_split, y_pred_eval)
                        eval_rmse = np.sqrt(mean_squared_error(y_eval_m_split, y_pred_eval))
                        eval_r2 = r2_score(y_eval_m_split, y_pred_eval)
                    else:
                        eval_mae = eval_rmse = eval_r2 = np.nan
                    
                    # Retrain on full training data (train + calibration) with best alpha for final model
                    logger.info(f"Retraining margin-only model on training+calibration data with best alpha={selected_alpha}")
                    X_train_full = X_scaled[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else X_train_split
                    y_train_m_full = y_margin[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_m_split
                    self.model = Ridge(alpha=selected_alpha, random_state=42)
                    self.model.fit(X_train_full, y_train_m_full)
                    
                    # Update final_metrics with evaluation set metrics
                    final_metrics = {
                        'margin_mae': eval_mae,
                        'margin_rmse': eval_rmse,
                        'margin_r2': eval_r2
                    }
                else:
                    # Use TimeSeriesSplit CV (original behavior)
                    # Train models for each alpha value
                    for alpha in alphas:
                        logger.info(f"Training Ridge (margin-only) with alpha={alpha}")
                        
                        margin_model = Ridge(alpha=alpha, random_state=42)
                        margin_cv_scores = {'mae': [], 'rmse': [], 'r2': []}
                        
                        for train_idx_cv, val_idx_cv in tscv.split(X_scaled):
                            X_train, X_val = X_scaled[train_idx_cv], X_scaled[val_idx_cv]
                            y_train_m, y_val_m = y_margin[train_idx_cv], y_margin[val_idx_cv]
                            
                            margin_model.fit(X_train, y_train_m)
                            y_pred_m = margin_model.predict(X_val)
                            
                            margin_cv_scores['mae'].append(mean_absolute_error(y_val_m, y_pred_m))
                            margin_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_m, y_pred_m)))
                            margin_cv_scores['r2'].append(r2_score(y_val_m, y_pred_m))
                        
                        result = {
                            'alpha': alpha,
                            'margin_mae': np.mean(margin_cv_scores['mae']),
                            'margin_rmse': np.mean(margin_cv_scores['rmse']),
                            'margin_r2': np.mean(margin_cv_scores['r2']),
                            'margin_model': margin_model
                        }
                        results.append(result)
                    
                    # Select best alpha (lowest margin MAE)
                    best_result = min(results, key=lambda x: x['margin_mae'])
                    selected_alpha = best_result.get('alpha')
                    alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None] if results else None
                    self.model = best_result['margin_model']
                    
                    # Retrain on full data with best alpha
                    logger.info(f"Retraining margin-only model on full data with best alpha={selected_alpha}")
                    self.model = Ridge(alpha=selected_alpha, random_state=42)
                    self.model.fit(X_scaled, y_margin)
                    
                    # Final evaluation on full data (margin-only)
                    y_pred_margin = self.model.predict(X_scaled)
                    
                    final_metrics = {
                        'margin_mae': mean_absolute_error(y_margin, y_pred_margin),
                        'margin_rmse': np.sqrt(mean_squared_error(y_margin, y_pred_margin)),
                        'margin_r2': r2_score(y_margin, y_pred_margin)
                    }
            else:
                # For other model types (ElasticNet, RandomForest, XGBoost)
                if use_time_based_split:
                    # Time-based calibration: train on train set, evaluate on calibration set, report evaluation set metrics
                    X_train_split = X_scaled[train_idx]
                    y_train_m_split = y_margin[train_idx]
                    X_cal_split = X_scaled[cal_idx] if len(cal_idx) > 0 else None
                    y_cal_m_split = y_margin[cal_idx] if len(cal_idx) > 0 else None
                    X_eval_split = X_scaled[eval_idx] if len(eval_idx) > 0 else None
                    y_eval_m_split = y_margin[eval_idx] if len(eval_idx) > 0 else None
                    
                    logger.info(f"Training {model_type} model (margin-only) using time-based calibration")
                    margin_model = self._create_model(model_type, **model_kwargs)
                    margin_model.fit(X_train_split, y_train_m_split)
                    
                    # Evaluate on calibration set
                    if X_cal_split is not None and len(X_cal_split) > 0:
                        y_pred_cal = margin_model.predict(X_cal_split)
                        cal_mae = mean_absolute_error(y_cal_m_split, y_pred_cal)
                        cal_rmse = np.sqrt(mean_squared_error(y_cal_m_split, y_pred_cal))
                        cal_r2 = r2_score(y_cal_m_split, y_pred_cal)
                    else:
                        cal_mae = cal_rmse = cal_r2 = np.nan
                    
                    # Evaluate on evaluation set
                    if X_eval_split is not None and len(X_eval_split) > 0:
                        y_pred_eval = margin_model.predict(X_eval_split)
                        eval_mae = mean_absolute_error(y_eval_m_split, y_pred_eval)
                        eval_rmse = np.sqrt(mean_squared_error(y_eval_m_split, y_pred_eval))
                        eval_r2 = r2_score(y_eval_m_split, y_pred_eval)
                    else:
                        eval_mae = eval_rmse = eval_r2 = np.nan
                    
                    # Retrain on full training data (train + calibration) for final model
                    X_train_full = X_scaled[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else X_train_split
                    y_train_m_full = y_margin[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_m_split
                    self.model = self._create_model(model_type, **model_kwargs)
                    self.model.fit(X_train_full, y_train_m_full)
                    
                    final_metrics = {
                        'margin_mae': eval_mae,
                        'margin_rmse': eval_rmse,
                        'margin_r2': eval_r2
                    }
                    
                    best_result = {
                        'margin_mae': cal_mae,
                        'margin_rmse': cal_rmse,
                        'margin_r2': cal_r2
                    }
                    results = [best_result]
                else:
                    # Use TimeSeriesSplit CV (original behavior)
                    logger.info(f"Training {model_type} model (margin-only)")
                    margin_model = self._create_model(model_type, **model_kwargs)
                    margin_model.fit(X_scaled, y_margin)
                    self.model = margin_model
                    
                    # Evaluate with CV
                    margin_cv_scores = {'mae': [], 'rmse': [], 'r2': []}
                    
                    for train_idx_cv, val_idx_cv in tscv.split(X_scaled):
                        X_train, X_val = X_scaled[train_idx_cv], X_scaled[val_idx_cv]
                        y_train_m, y_val_m = y_margin[train_idx_cv], y_margin[val_idx_cv]
                        
                        # Train temporary model
                        temp_model = self._create_model(model_type, **model_kwargs)
                        temp_model.fit(X_train, y_train_m)
                        
                        # Predict
                        y_pred_m = temp_model.predict(X_val)
                        
                        # Evaluate
                        margin_cv_scores['mae'].append(mean_absolute_error(y_val_m, y_pred_m))
                        margin_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_m, y_pred_m)))
                        margin_cv_scores['r2'].append(r2_score(y_val_m, y_pred_m))
                    
                    best_result = {
                        'margin_mae': np.mean(margin_cv_scores['mae']),
                        'margin_rmse': np.mean(margin_cv_scores['rmse']),
                        'margin_r2': np.mean(margin_cv_scores['r2'])
                    }
                    results = [best_result]
                    
                    # Final evaluation on full data (margin-only)
                    y_pred_margin = self.model.predict(X_scaled)
                    
                    final_metrics = {
                        'margin_mae': mean_absolute_error(y_margin, y_pred_margin),
                        'margin_rmse': np.sqrt(mean_squared_error(y_margin, y_pred_margin)),
                        'margin_r2': r2_score(y_margin, y_pred_margin)
                    }
            
            # Extract alphas tested and selected alpha (already set above for Ridge models with multiple alphas)
            # Only set if not already set above (for single alpha case or non-Ridge models)
            if model_type != 'Ridge':
                selected_alpha = None
                alphas_tested = None
            elif not results:
                selected_alpha = None
                alphas_tested = None
            elif selected_alpha is None and len(results) == 1 and results[0].get('alpha') is not None:
                # Single alpha was tested or specified - use it as selected (only if not already set)
                selected_alpha = results[0].get('alpha')
                alphas_tested = [selected_alpha] if alphas_tested is None else alphas_tested
            elif len(results) == 1 and results[0].get('alpha') is None:
                # Non-Ridge model (no alpha in result)
                selected_alpha = None
                alphas_tested = None
            elif alphas_tested is None and results:
                # Fallback: extract alphas from results if not already set
                alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None]
                if len(alphas_tested) == 1 and selected_alpha is None:
                    selected_alpha = alphas_tested[0]
            
            return {
                'model_type': model_type,
                'target': 'margin',
                'cv_results': results,
                'final_metrics': final_metrics,
                'feature_names': self.feature_names,
                'n_samples': len(df),
                'n_features': len(self.feature_names),
                'use_time_calibration': use_time_based_split,
                'calibration_years': calibration_years if use_time_based_split else None,
                'evaluation_year': evaluation_year if use_time_based_split else None,
                'selected_alpha': selected_alpha if model_type == 'Ridge' else None,
                'alphas_tested': alphas_tested if model_type == 'Ridge' else None
            }
        
        # Original home_away target (existing behavior)
        self.target_type = 'home_away'
        
        if model_type == 'Ridge':
            alphas = alphas or self.DEFAULT_RIDGE_ALPHAS
            
            if use_time_based_split:
                # Time-based calibration: train on train set, evaluate on calibration set, report evaluation set metrics
                X_train_split = X_scaled[train_idx]
                y_train_h_split = y_home[train_idx]
                y_train_a_split = y_away[train_idx]
                X_cal_split = X_scaled[cal_idx] if len(cal_idx) > 0 else None
                y_cal_h_split = y_home[cal_idx] if len(cal_idx) > 0 else None
                y_cal_a_split = y_away[cal_idx] if len(cal_idx) > 0 else None
                X_eval_split = X_scaled[eval_idx] if len(eval_idx) > 0 else None
                y_eval_h_split = y_home[eval_idx] if len(eval_idx) > 0 else None
                y_eval_a_split = y_away[eval_idx] if len(eval_idx) > 0 else None
                
                # Train models for each alpha value on training set
                for alpha in alphas:
                    logger.info(f"Training Ridge with alpha={alpha} using time-based calibration")
                    
                    # Train home points model
                    home_model = Ridge(alpha=alpha, random_state=42)
                    home_model.fit(X_train_split, y_train_h_split)
                    
                    # Evaluate on calibration set
                    if X_cal_split is not None and len(X_cal_split) > 0:
                        y_pred_h_cal = home_model.predict(X_cal_split)
                        home_cal_mae = mean_absolute_error(y_cal_h_split, y_pred_h_cal)
                        home_cal_rmse = np.sqrt(mean_squared_error(y_cal_h_split, y_pred_h_cal))
                        home_cal_r2 = r2_score(y_cal_h_split, y_pred_h_cal)
                        home_cal_mape = mean_absolute_percentage_error(y_cal_h_split, y_pred_h_cal)
                    else:
                        home_cal_mae = home_cal_rmse = home_cal_r2 = home_cal_mape = np.nan
                    
                    # Train away points model
                    away_model = Ridge(alpha=alpha, random_state=42)
                    away_model.fit(X_train_split, y_train_a_split)
                    
                    # Evaluate on calibration set
                    if X_cal_split is not None and len(X_cal_split) > 0:
                        y_pred_a_cal = away_model.predict(X_cal_split)
                        away_cal_mae = mean_absolute_error(y_cal_a_split, y_pred_a_cal)
                        away_cal_rmse = np.sqrt(mean_squared_error(y_cal_a_split, y_pred_a_cal))
                        away_cal_r2 = r2_score(y_cal_a_split, y_pred_a_cal)
                        away_cal_mape = mean_absolute_percentage_error(y_cal_a_split, y_pred_a_cal)
                    else:
                        away_cal_mae = away_cal_rmse = away_cal_r2 = away_cal_mape = np.nan
                    
                    # Average CV scores for hyperparameter selection
                    result = {
                        'alpha': alpha,
                        'home_mae': home_cal_mae,
                        'home_rmse': home_cal_rmse,
                        'home_r2': home_cal_r2,
                        'home_mape': home_cal_mape,
                        'away_mae': away_cal_mae,
                        'away_rmse': away_cal_rmse,
                        'away_r2': away_cal_r2,
                        'away_mape': away_cal_mape,
                        'home_model': home_model,
                        'away_model': away_model
                    }
                    results.append(result)
                
                # Select best alpha (lowest combined MAE on calibration set)
                best_result = min(results, key=lambda x: (x['home_mae'] + x['away_mae']) / 2 if not (np.isnan(x['home_mae']) or np.isnan(x['away_mae'])) else float('inf'))
                selected_alpha = best_result.get('alpha')
                alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None] if results else None
                
                # Evaluate best model on evaluation set (BEFORE retraining - this is just for diagnostics)
                # NOTE: These metrics are overwritten later after retraining, so they're not used in final_metrics
                if X_eval_split is not None and len(X_eval_split) > 0:
                    print(f"[PointsRegressionTrainer.train] DIAGNOSTIC: Evaluating model (trained on train_idx only, {len(X_train_split)} samples) on evaluation set BEFORE retraining")
                    y_pred_h_eval_pre = best_result['home_model'].predict(X_eval_split)
                    y_pred_a_eval_pre = best_result['away_model'].predict(X_eval_split)
                    
                    eval_home_mae_pre = mean_absolute_error(y_eval_h_split, y_pred_h_eval_pre)
                    eval_home_r2_pre = r2_score(y_eval_h_split, y_pred_h_eval_pre)
                    eval_away_mae_pre = mean_absolute_error(y_eval_a_split, y_pred_a_eval_pre)
                    eval_away_r2_pre = r2_score(y_eval_a_split, y_pred_a_eval_pre)
                    print(f"[PointsRegressionTrainer.train] DIAGNOSTIC metrics (pre-retrain): Home MAE={eval_home_mae_pre:.2f}, R²={eval_home_r2_pre:.4f}, Away MAE={eval_away_mae_pre:.2f}, R²={eval_away_r2_pre:.4f}")
                    
                    # Initialize variables (will be overwritten after retraining)
                    eval_home_mae = eval_home_rmse = eval_home_r2 = eval_home_mape = np.nan
                    eval_away_mae = eval_away_rmse = eval_away_r2 = eval_away_mape = np.nan
                    eval_diff_mae = eval_diff_rmse = eval_diff_r2 = np.nan
                    eval_total_mae = eval_total_rmse = eval_total_r2 = np.nan
                else:
                    eval_home_mae = eval_home_rmse = eval_home_r2 = eval_home_mape = np.nan
                    eval_away_mae = eval_away_rmse = eval_away_r2 = eval_away_mape = np.nan
                    eval_diff_mae = eval_diff_rmse = eval_diff_r2 = np.nan
                    eval_total_mae = eval_total_rmse = eval_total_r2 = np.nan
                
                # Retrain on full training data (train + calibration) with best alpha for final model
                logger.info(f"Retraining on training+calibration data with best alpha={selected_alpha}")
                X_train_full = X_scaled[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else X_train_split
                y_train_h_full = y_home[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_h_split
                y_train_a_full = y_away[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_a_split
                
                self.model = {
                    'home': Ridge(alpha=selected_alpha, random_state=42),
                    'away': Ridge(alpha=selected_alpha, random_state=42)
                }
                self.model['home'].fit(X_train_full, y_train_h_full)
                self.model['away'].fit(X_train_full, y_train_a_full)
                
                # Re-evaluate the retrained model on evaluation set for final metrics
                if X_eval_split is not None and len(X_eval_split) > 0:
                    print(f"[PointsRegressionTrainer.train] Evaluating retrained model on evaluation set: {len(X_eval_split)} samples")
                    y_pred_h_eval = self.model['home'].predict(X_eval_split)
                    y_pred_a_eval = self.model['away'].predict(X_eval_split)
                    
                    eval_home_mae = mean_absolute_error(y_eval_h_split, y_pred_h_eval)
                    eval_home_rmse = np.sqrt(mean_squared_error(y_eval_h_split, y_pred_h_eval))
                    eval_home_r2 = r2_score(y_eval_h_split, y_pred_h_eval)
                    eval_home_mape = mean_absolute_percentage_error(y_eval_h_split, y_pred_h_eval)
                    
                    eval_away_mae = mean_absolute_error(y_eval_a_split, y_pred_a_eval)
                    eval_away_rmse = np.sqrt(mean_squared_error(y_eval_a_split, y_pred_a_eval))
                    eval_away_r2 = r2_score(y_eval_a_split, y_pred_a_eval)
                    eval_away_mape = mean_absolute_percentage_error(y_eval_a_split, y_pred_a_eval)
                    
                    # Margin and total metrics
                    eval_diff_true = y_eval_h_split - y_eval_a_split
                    eval_diff_pred = y_pred_h_eval - y_pred_a_eval
                    eval_total_true = y_eval_h_split + y_eval_a_split
                    eval_total_pred = y_pred_h_eval + y_pred_a_eval
                    
                    eval_diff_mae = mean_absolute_error(eval_diff_true, eval_diff_pred)
                    eval_diff_rmse = np.sqrt(mean_squared_error(eval_diff_true, eval_diff_pred))
                    eval_diff_r2 = r2_score(eval_diff_true, eval_diff_pred)
                    eval_total_mae = mean_absolute_error(eval_total_true, eval_total_pred)
                    eval_total_rmse = np.sqrt(mean_squared_error(eval_total_true, eval_total_pred))
                    eval_total_r2 = r2_score(eval_total_true, eval_total_pred)
                    
                    print(f"[PointsRegressionTrainer.train] Final metrics from EVALUATION SET ({len(X_eval_split)} samples):")
                    print(f"  Home: MAE={eval_home_mae:.2f}, RMSE={eval_home_rmse:.2f}, R²={eval_home_r2:.4f}, MAPE={eval_home_mape:.2f}%")
                    print(f"  Away: MAE={eval_away_mae:.2f}, RMSE={eval_away_rmse:.2f}, R²={eval_away_r2:.4f}, MAPE={eval_away_mape:.2f}%")
                    print(f"  Diff: MAE={eval_diff_mae:.2f}, RMSE={eval_diff_rmse:.2f}, R²={eval_diff_r2:.4f}")
                    print(f"  Total: MAE={eval_total_mae:.2f}, RMSE={eval_total_rmse:.2f}, R²={eval_total_r2:.4f}")
                else:
                    print(f"[PointsRegressionTrainer.train] WARNING: Evaluation set is empty or None! Cannot compute final metrics.")
                    eval_home_mae = eval_home_rmse = eval_home_r2 = eval_home_mape = np.nan
                    eval_away_mae = eval_away_rmse = eval_away_r2 = eval_away_mape = np.nan
                    eval_diff_mae = eval_diff_rmse = eval_diff_r2 = np.nan
                    eval_total_mae = eval_total_rmse = eval_total_r2 = np.nan
                
                # Final metrics from evaluation set (using retrained model)
                final_metrics = {
                    'home_mae': eval_home_mae,
                    'home_rmse': eval_home_rmse,
                    'home_r2': eval_home_r2,
                    'home_mape': eval_home_mape,
                    'away_mae': eval_away_mae,
                    'away_rmse': eval_away_rmse,
                    'away_r2': eval_away_r2,
                    'away_mape': eval_away_mape,
                    'diff_mae': eval_diff_mae,
                    'diff_rmse': eval_diff_rmse,
                    'diff_r2': eval_diff_r2,
                    'total_mae': eval_total_mae,
                    'total_rmse': eval_total_rmse,
                    'total_r2': eval_total_r2
                }
            else:
                # Use TimeSeriesSplit CV (original behavior)
                # Train separate models for home and away points
                for alpha in alphas:
                    logger.info(f"Training Ridge with alpha={alpha}")
                    
                    # Train home points model
                    home_model = Ridge(alpha=alpha, random_state=42)
                    home_cv_scores = {'mae': [], 'rmse': [], 'r2': [], 'mape': []}
                    
                    for train_idx_cv, val_idx_cv in tscv.split(X_scaled):
                        X_train, X_val = X_scaled[train_idx_cv], X_scaled[val_idx_cv]
                        y_train_h, y_val_h = y_home[train_idx_cv], y_home[val_idx_cv]
                        
                        home_model.fit(X_train, y_train_h)
                        y_pred_h = home_model.predict(X_val)
                        
                        home_cv_scores['mae'].append(mean_absolute_error(y_val_h, y_pred_h))
                        home_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_h, y_pred_h)))
                        home_cv_scores['r2'].append(r2_score(y_val_h, y_pred_h))
                        home_cv_scores['mape'].append(mean_absolute_percentage_error(y_val_h, y_pred_h))
                    
                    # Train away points model
                    away_model = Ridge(alpha=alpha, random_state=42)
                    away_cv_scores = {'mae': [], 'rmse': [], 'r2': [], 'mape': []}
                    
                    for train_idx_cv, val_idx_cv in tscv.split(X_scaled):
                        X_train, X_val = X_scaled[train_idx_cv], X_scaled[val_idx_cv]
                        y_train_a, y_val_a = y_away[train_idx_cv], y_away[val_idx_cv]
                        
                        away_model.fit(X_train, y_train_a)
                        y_pred_a = away_model.predict(X_val)
                        
                        away_cv_scores['mae'].append(mean_absolute_error(y_val_a, y_pred_a))
                        away_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_a, y_pred_a)))
                        away_cv_scores['r2'].append(r2_score(y_val_a, y_pred_a))
                        away_cv_scores['mape'].append(mean_absolute_percentage_error(y_val_a, y_pred_a))
                    
                    # Average CV scores
                    result = {
                        'alpha': alpha,
                        'home_mae': np.mean(home_cv_scores['mae']),
                        'home_rmse': np.mean(home_cv_scores['rmse']),
                        'home_r2': np.mean(home_cv_scores['r2']),
                        'home_mape': np.mean(home_cv_scores['mape']),
                        'away_mae': np.mean(away_cv_scores['mae']),
                        'away_rmse': np.mean(away_cv_scores['rmse']),
                        'away_r2': np.mean(away_cv_scores['r2']),
                        'away_mape': np.mean(away_cv_scores['mape']),
                        'home_model': home_model,
                        'away_model': away_model
                    }
                    results.append(result)
                
                # Select best alpha (lowest combined MAE)
                best_result = min(results, key=lambda x: (x['home_mae'] + x['away_mae']) / 2)
                selected_alpha = best_result.get('alpha')
                alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None] if results else None
                self.model = {
                    'home': best_result['home_model'],
                    'away': best_result['away_model']
                }
                
                # Retrain on full data with best alpha
                logger.info(f"Retraining on full data with best alpha={selected_alpha}")
                print(f"[PointsRegressionTrainer.train] WARNING: Time-based calibration DISABLED - retraining on FULL DATASET ({len(X_scaled)} samples)")
                self.model['home'] = Ridge(alpha=selected_alpha, random_state=42)
                self.model['away'] = Ridge(alpha=selected_alpha, random_state=42)
                self.model['home'].fit(X_scaled, y_home)
                self.model['away'].fit(X_scaled, y_away)
                
                # Final evaluation on full data
                print(f"[PointsRegressionTrainer.train] WARNING: Evaluating on FULL DATASET ({len(X_scaled)} samples, includes training data)")
                print(f"[PointsRegressionTrainer.train] This can give negative R² because model is evaluated on data it was trained on!")
                y_pred_home = self.model['home'].predict(X_scaled)
                y_pred_away = self.model['away'].predict(X_scaled)
                
                final_metrics = {
                    'home_mae': mean_absolute_error(y_home, y_pred_home),
                    'home_rmse': np.sqrt(mean_squared_error(y_home, y_pred_home)),
                    'home_r2': r2_score(y_home, y_pred_home),
                    'home_mape': mean_absolute_percentage_error(y_home, y_pred_home),
                    'away_mae': mean_absolute_error(y_away, y_pred_away),
                    'away_rmse': np.sqrt(mean_squared_error(y_away, y_pred_away)),
                    'away_r2': r2_score(y_away, y_pred_away),
                    'away_mape': mean_absolute_percentage_error(y_away, y_pred_away)
                }
                print(f"[PointsRegressionTrainer.train] Final metrics from FULL DATASET ({len(X_scaled)} samples):")
                print(f"  Home: MAE={final_metrics['home_mae']:.2f}, RMSE={final_metrics['home_rmse']:.2f}, R²={final_metrics['home_r2']:.4f}, MAPE={final_metrics['home_mape']:.2f}%")
                print(f"  Away: MAE={final_metrics['away_mae']:.2f}, RMSE={final_metrics['away_rmse']:.2f}, R²={final_metrics['away_r2']:.4f}, MAPE={final_metrics['away_mape']:.2f}%")
                
                # Combined metrics
                y_total_true = y_home + y_away
                y_total_pred = y_pred_home + y_pred_away
                y_diff_true = y_home - y_away
                y_diff_pred = y_pred_home - y_pred_away
                
                final_metrics['total_mae'] = mean_absolute_error(y_total_true, y_total_pred)
                final_metrics['total_rmse'] = np.sqrt(mean_squared_error(y_total_true, y_total_pred))
                final_metrics['total_r2'] = r2_score(y_total_true, y_total_pred)
                final_metrics['diff_mae'] = mean_absolute_error(y_diff_true, y_diff_pred)
                final_metrics['diff_rmse'] = np.sqrt(mean_squared_error(y_diff_true, y_diff_pred))
                final_metrics['diff_r2'] = r2_score(y_diff_true, y_diff_pred)
            
        else:
            # For other model types (ElasticNet, RandomForest, XGBoost)
            if use_time_based_split:
                # Time-based calibration: train on train set, evaluate on calibration set, report evaluation set metrics
                X_train_split = X_scaled[train_idx]
                y_train_h_split = y_home[train_idx]
                y_train_a_split = y_away[train_idx]
                X_cal_split = X_scaled[cal_idx] if len(cal_idx) > 0 else None
                y_cal_h_split = y_home[cal_idx] if len(cal_idx) > 0 else None
                y_cal_a_split = y_away[cal_idx] if len(cal_idx) > 0 else None
                X_eval_split = X_scaled[eval_idx] if len(eval_idx) > 0 else None
                y_eval_h_split = y_home[eval_idx] if len(eval_idx) > 0 else None
                y_eval_a_split = y_away[eval_idx] if len(eval_idx) > 0 else None
                
                logger.info(f"Training {model_type} model using time-based calibration")
                home_model = self._create_model(model_type, **model_kwargs)
                away_model = self._create_model(model_type, **model_kwargs)
                
                home_model.fit(X_train_split, y_train_h_split)
                away_model.fit(X_train_split, y_train_a_split)
                
                # Evaluate on calibration set
                if X_cal_split is not None and len(X_cal_split) > 0:
                    y_pred_h_cal = home_model.predict(X_cal_split)
                    y_pred_a_cal = away_model.predict(X_cal_split)
                    
                    home_cal_mae = mean_absolute_error(y_cal_h_split, y_pred_h_cal)
                    home_cal_rmse = np.sqrt(mean_squared_error(y_cal_h_split, y_pred_h_cal))
                    home_cal_r2 = r2_score(y_cal_h_split, y_pred_h_cal)
                    home_cal_mape = mean_absolute_percentage_error(y_cal_h_split, y_pred_h_cal)
                    
                    away_cal_mae = mean_absolute_error(y_cal_a_split, y_pred_a_cal)
                    away_cal_rmse = np.sqrt(mean_squared_error(y_cal_a_split, y_pred_a_cal))
                    away_cal_r2 = r2_score(y_cal_a_split, y_pred_a_cal)
                    away_cal_mape = mean_absolute_percentage_error(y_cal_a_split, y_pred_a_cal)
                else:
                    home_cal_mae = home_cal_rmse = home_cal_r2 = home_cal_mape = np.nan
                    away_cal_mae = away_cal_rmse = away_cal_r2 = away_cal_mape = np.nan
                
                # Evaluate on evaluation set
                if X_eval_split is not None and len(X_eval_split) > 0:
                    y_pred_h_eval = home_model.predict(X_eval_split)
                    y_pred_a_eval = away_model.predict(X_eval_split)
                    
                    eval_home_mae = mean_absolute_error(y_eval_h_split, y_pred_h_eval)
                    eval_home_rmse = np.sqrt(mean_squared_error(y_eval_h_split, y_pred_h_eval))
                    eval_home_r2 = r2_score(y_eval_h_split, y_pred_h_eval)
                    eval_home_mape = mean_absolute_percentage_error(y_eval_h_split, y_pred_h_eval)
                    
                    eval_away_mae = mean_absolute_error(y_eval_a_split, y_pred_a_eval)
                    eval_away_rmse = np.sqrt(mean_squared_error(y_eval_a_split, y_pred_a_eval))
                    eval_away_r2 = r2_score(y_eval_a_split, y_pred_a_eval)
                    eval_away_mape = mean_absolute_percentage_error(y_eval_a_split, y_pred_a_eval)
                    
                    # Margin and total metrics
                    eval_diff_true = y_eval_h_split - y_eval_a_split
                    eval_diff_pred = y_pred_h_eval - y_pred_a_eval
                    eval_total_true = y_eval_h_split + y_eval_a_split
                    eval_total_pred = y_pred_h_eval + y_pred_a_eval
                    
                    eval_diff_mae = mean_absolute_error(eval_diff_true, eval_diff_pred)
                    eval_diff_rmse = np.sqrt(mean_squared_error(eval_diff_true, eval_diff_pred))
                    eval_diff_r2 = r2_score(eval_diff_true, eval_diff_pred)
                    eval_total_mae = mean_absolute_error(eval_total_true, eval_total_pred)
                    eval_total_rmse = np.sqrt(mean_squared_error(eval_total_true, eval_total_pred))
                    eval_total_r2 = r2_score(eval_total_true, eval_total_pred)
                else:
                    eval_home_mae = eval_home_rmse = eval_home_r2 = eval_home_mape = np.nan
                    eval_away_mae = eval_away_rmse = eval_away_r2 = eval_away_mape = np.nan
                    eval_diff_mae = eval_diff_rmse = eval_diff_r2 = np.nan
                    eval_total_mae = eval_total_rmse = eval_total_r2 = np.nan
                
                # Retrain on full training data (train + calibration) for final model
                X_train_full = X_scaled[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else X_train_split
                y_train_h_full = y_home[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_h_split
                y_train_a_full = y_away[np.concatenate([train_idx, cal_idx])] if len(cal_idx) > 0 else y_train_a_split
                
                self.model = {
                    'home': self._create_model(model_type, **model_kwargs),
                    'away': self._create_model(model_type, **model_kwargs)
                }
                self.model['home'].fit(X_train_full, y_train_h_full)
                self.model['away'].fit(X_train_full, y_train_a_full)
                
                final_metrics = {
                    'home_mae': eval_home_mae,
                    'home_rmse': eval_home_rmse,
                    'home_r2': eval_home_r2,
                    'home_mape': eval_home_mape,
                    'away_mae': eval_away_mae,
                    'away_rmse': eval_away_rmse,
                    'away_r2': eval_away_r2,
                    'away_mape': eval_away_mape,
                    'diff_mae': eval_diff_mae,
                    'diff_rmse': eval_diff_rmse,
                    'diff_r2': eval_diff_r2,
                    'total_mae': eval_total_mae,
                    'total_rmse': eval_total_rmse,
                    'total_r2': eval_total_r2
                }
                
                best_result = {
                    'home_mae': home_cal_mae,
                    'home_rmse': home_cal_rmse,
                    'home_r2': home_cal_r2,
                    'home_mape': home_cal_mape,
                    'away_mae': away_cal_mae,
                    'away_rmse': away_cal_rmse,
                    'away_r2': away_cal_r2,
                    'away_mape': away_cal_mape
                }
                results = [best_result]
            else:
                # Use TimeSeriesSplit CV (original behavior)
                logger.info(f"Training {model_type} model")
                home_model = self._create_model(model_type, **model_kwargs)
                away_model = self._create_model(model_type, **model_kwargs)
                
                home_model.fit(X_scaled, y_home)
                away_model.fit(X_scaled, y_away)
                
                self.model = {
                    'home': home_model,
                    'away': away_model
                }
                
                # Evaluate with CV
                home_cv_scores = {'mae': [], 'rmse': [], 'r2': [], 'mape': []}
                away_cv_scores = {'mae': [], 'rmse': [], 'r2': [], 'mape': []}
                
                for train_idx_cv, val_idx_cv in tscv.split(X_scaled):
                    X_train, X_val = X_scaled[train_idx_cv], X_scaled[val_idx_cv]
                    y_train_h, y_val_h = y_home[train_idx_cv], y_home[val_idx_cv]
                    y_train_a, y_val_a = y_away[train_idx_cv], y_away[val_idx_cv]
                    
                    # Train temporary models
                    temp_home = self._create_model(model_type, **model_kwargs)
                    temp_away = self._create_model(model_type, **model_kwargs)
                    temp_home.fit(X_train, y_train_h)
                    temp_away.fit(X_train, y_train_a)
                    
                    # Predict
                    y_pred_h = temp_home.predict(X_val)
                    y_pred_a = temp_away.predict(X_val)
                    
                    # Evaluate
                    home_cv_scores['mae'].append(mean_absolute_error(y_val_h, y_pred_h))
                    home_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_h, y_pred_h)))
                    home_cv_scores['r2'].append(r2_score(y_val_h, y_pred_h))
                    home_cv_scores['mape'].append(mean_absolute_percentage_error(y_val_h, y_pred_h))
                    
                    away_cv_scores['mae'].append(mean_absolute_error(y_val_a, y_pred_a))
                    away_cv_scores['rmse'].append(np.sqrt(mean_squared_error(y_val_a, y_pred_a)))
                    away_cv_scores['r2'].append(r2_score(y_val_a, y_pred_a))
                    away_cv_scores['mape'].append(mean_absolute_percentage_error(y_val_a, y_pred_a))
                
                best_result = {
                    'home_mae': np.mean(home_cv_scores['mae']),
                    'home_rmse': np.mean(home_cv_scores['rmse']),
                    'home_r2': np.mean(home_cv_scores['r2']),
                    'home_mape': np.mean(home_cv_scores['mape']),
                    'away_mae': np.mean(away_cv_scores['mae']),
                    'away_rmse': np.mean(away_cv_scores['rmse']),
                    'away_r2': np.mean(away_cv_scores['r2']),
                    'away_mape': np.mean(away_cv_scores['mape'])
                }
                results = [best_result]
                
                # Final evaluation on full data
                y_pred_home = self.model['home'].predict(X_scaled)
                y_pred_away = self.model['away'].predict(X_scaled)
                
                final_metrics = {
                    'home_mae': mean_absolute_error(y_home, y_pred_home),
                    'home_rmse': np.sqrt(mean_squared_error(y_home, y_pred_home)),
                    'home_r2': r2_score(y_home, y_pred_home),
                    'home_mape': mean_absolute_percentage_error(y_home, y_pred_home),
                    'away_mae': mean_absolute_error(y_away, y_pred_away),
                    'away_rmse': np.sqrt(mean_squared_error(y_away, y_pred_away)),
                    'away_r2': r2_score(y_away, y_pred_away),
                    'away_mape': mean_absolute_percentage_error(y_away, y_pred_away)
                }
                
                # Combined metrics
                y_total_true = y_home + y_away
                y_total_pred = y_pred_home + y_pred_away
                y_diff_true = y_home - y_away
                y_diff_pred = y_pred_home - y_pred_away
                
                final_metrics['total_mae'] = mean_absolute_error(y_total_true, y_total_pred)
                final_metrics['total_rmse'] = np.sqrt(mean_squared_error(y_total_true, y_total_pred))
                final_metrics['total_r2'] = r2_score(y_total_true, y_total_pred)
                final_metrics['diff_mae'] = mean_absolute_error(y_diff_true, y_diff_pred)
                final_metrics['diff_rmse'] = np.sqrt(mean_squared_error(y_diff_true, y_diff_pred))
                final_metrics['diff_r2'] = r2_score(y_diff_true, y_diff_pred)
        
        # Extract alphas tested and selected alpha for Ridge models (already set above for multiple alphas)
        # Extract alphas tested and selected alpha for Ridge models (already set above for multiple alphas)
        # Only set if not already set above (for single alpha case or non-Ridge models)
        if model_type != 'Ridge':
            selected_alpha = None
            alphas_tested = None
        elif not results:
            selected_alpha = None
            alphas_tested = None
        elif selected_alpha is None and len(results) == 1 and results[0].get('alpha') is not None:
            # Single alpha was tested or specified - use it as selected (only if not already set)
            selected_alpha = results[0].get('alpha')
            alphas_tested = [selected_alpha] if alphas_tested is None else alphas_tested
        elif len(results) == 1 and results[0].get('alpha') is None:
            # Non-Ridge model (no alpha in result)
            selected_alpha = None
            alphas_tested = None
        elif alphas_tested is None and results:
            # Fallback: extract alphas from results if not already set
            alphas_tested = [r.get('alpha') for r in results if r.get('alpha') is not None]
            if len(alphas_tested) == 1 and selected_alpha is None:
                selected_alpha = alphas_tested[0]
        
        return {
            'model_type': model_type,
            'target': 'home_away',
            'cv_results': results,
            'final_metrics': final_metrics,
            'feature_names': self.feature_names,
            'n_samples': len(df),
            'n_features': len(self.feature_names),
            'use_time_calibration': use_time_based_split,
            'calibration_years': calibration_years if use_time_based_split else None,
            'evaluation_year': evaluation_year if use_time_based_split else None,
            'selected_alpha': selected_alpha if model_type == 'Ridge' else None,
            'alphas_tested': alphas_tested if model_type == 'Ridge' else None
        }
    
    def save_model(self, model_name: str = None):
        """Save model and scaler to artifacts directory."""
        if model_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_name = f"points_regression_{timestamp}"
        
        model_path = os.path.join(self.artifacts_dir, f"{model_name}.pkl")
        scaler_path = os.path.join(self.artifacts_dir, f"{model_name}_scaler.pkl")
        feature_names_path = os.path.join(self.artifacts_dir, f"{model_name}_features.json")
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save scaler
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save feature names
        with open(feature_names_path, 'w') as f:
            json.dump(self.feature_names, f)
        
        logger.info(f"Model saved to {model_path}")
        return model_path
    
    def load_model(self, model_name: str):
        """Load model and scaler from artifacts directory."""
        model_path = os.path.join(self.artifacts_dir, f"{model_name}.pkl")
        scaler_path = os.path.join(self.artifacts_dir, f"{model_name}_scaler.pkl")
        feature_names_path = os.path.join(self.artifacts_dir, f"{model_name}_features.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
        if not os.path.exists(feature_names_path):
            raise FileNotFoundError(f"Feature names file not found: {feature_names_path}")
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(feature_names_path, 'r') as f:
            self.feature_names = json.load(f)
        
        # Validate loaded model - handle both home_away (dict) and margin (single model) structures
        if isinstance(self.model, dict):
            # Home/away model structure
            if 'home' not in self.model or 'away' not in self.model:
                raise ValueError(f"Invalid model structure. Expected dict with 'home' and 'away' keys, or single model for margin target.")
            self.target_type = 'home_away'
        else:
            # Single model structure (margin-only)
            self.target_type = 'margin'
        
        if self.scaler is None:
            raise ValueError("Scaler is None after loading.")
        
        if not self.feature_names or len(self.feature_names) == 0:
            raise ValueError("Feature names list is empty after loading.")
        
        # Check scaler dimensions match feature count
        if hasattr(self.scaler, 'n_features_in_'):
            if self.scaler.n_features_in_ != len(self.feature_names):
                raise ValueError(f"Scaler expects {self.scaler.n_features_in_} features but model has {len(self.feature_names)} feature names.")
        
        logger.info(f"Model loaded from {model_path}")
        if self.target_type == 'margin':
            logger.info(f"  Model type: {type(self.model)} (margin-only)")
        else:
            logger.info(f"  Model type: {type(self.model['home'])} (home/away)")
        logger.info(f"  Features: {len(self.feature_names)}")
        logger.info(f"  Scaler features in: {getattr(self.scaler, 'n_features_in_', 'unknown')}")
    
    def predict(self, game: dict, before_date: str, use_shap: bool = False, selected_features: List[str] = None) -> Dict:
        """
        Predict points for a game.
        
        Args:
            game: Game dictionary from MongoDB
            before_date: Date string in YYYY-MM-DD format
            use_shap: If True, use SHAP for feature contributions (for non-linear models)
        
        Returns:
            Dictionary with predictions and feature contributions
        """
        # Build feature vector (use saved feature names if model is loaded)
        if self.feature_names:
            # Use the feature names from the trained model
            feature_vector, built_feature_names = self._build_feature_vector(game, before_date, selected_features=self.feature_names)
        else:
            # Build with selected features (for training)
            feature_vector, built_feature_names = self._build_feature_vector(game, before_date, selected_features=selected_features)
        
        # Ensure feature order matches training
        # Create a dict from the feature vector we built
        feature_dict = dict(zip(built_feature_names, feature_vector))
        
        # Check for missing features
        missing_features = [name for name in self.feature_names if name not in feature_dict]
        if missing_features:
            logger.warning(f"Missing features in prediction: {missing_features[:10]}{'...' if len(missing_features) > 10 else ''}. Using 0.0 as default.")
        
        # Build ordered vector, using 0.0 for missing features
        feature_vector_ordered = np.array([feature_dict.get(name, 0.0) for name in self.feature_names])
        
        # Validate feature vector
        if len(feature_vector_ordered) != len(self.feature_names):
            raise ValueError(f"Feature vector length mismatch: expected {len(self.feature_names)}, got {len(feature_vector_ordered)}")
        
        # Check for NaN or infinite values
        if np.any(np.isnan(feature_vector_ordered)) or np.any(np.isinf(feature_vector_ordered)):
            nan_indices = np.where(np.isnan(feature_vector_ordered) | np.isinf(feature_vector_ordered))[0]
            nan_features = [self.feature_names[i] for i in nan_indices]
            logger.warning(f"NaN or Inf values found in features: {nan_features}. Replacing with 0.")
            feature_vector_ordered = np.nan_to_num(feature_vector_ordered, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Scale
        if self.scaler is None:
            raise ValueError("Scaler not loaded. Model may not be properly initialized.")
        
        try:
            feature_vector_scaled = self.scaler.transform(feature_vector_ordered.reshape(1, -1))
        except Exception as e:
            logger.error(f"Error scaling features: {e}")
            logger.error(f"Feature vector shape: {feature_vector_ordered.shape}, Feature names: {self.feature_names[:5]}...")
            raise
        
        # Predict - handle both home_away (dict) and margin (single model) structures
        try:
            if self.target_type == 'margin':
                # Margin-only model: single model that predicts margin directly
                margin_pred = self.model.predict(feature_vector_scaled)[0]
                # For margin-only, we don't predict home/away separately
                home_points_pred = None
                away_points_pred = None
                point_diff_pred = margin_pred
            else:
                # Home/away models: dict with 'home' and 'away' keys
                if not isinstance(self.model, dict) or 'home' not in self.model or 'away' not in self.model:
                    raise ValueError(f"Invalid model structure for target='home_away'. Expected dict with 'home' and 'away' keys, got: {type(self.model)}")
                home_points_pred = self.model['home'].predict(feature_vector_scaled)[0]
                away_points_pred = self.model['away'].predict(feature_vector_scaled)[0]
                point_diff_pred = home_points_pred - away_points_pred
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            if self.target_type == 'margin':
                logger.error(f"Model type: {type(self.model)}, Scaled vector shape: {feature_vector_scaled.shape}")
            else:
                logger.error(f"Model type: {type(self.model.get('home')) if isinstance(self.model, dict) else 'unknown'}, Scaled vector shape: {feature_vector_scaled.shape}")
            raise
        
        # Debug: Log prediction details if values are unreasonable
        if self.target_type == 'margin':
            # Margin-only: validate margin prediction is reasonable (typical NBA margin: -50 to +50)
            if abs(point_diff_pred) > 60:
                logger.warning(f"Unusual margin prediction: {point_diff_pred}. Typical NBA margins range from -50 to +50.")
                # Clamp to reasonable range for margin
                point_diff_pred = max(-60, min(60, point_diff_pred))
        else:
            # Home/away: validate both predictions
            if abs(home_points_pred) > 200 or abs(away_points_pred) > 200:
                logger.error(f"CRITICAL: Unreasonable predictions detected!")
                logger.error(f"  Home prediction: {home_points_pred}")
                logger.error(f"  Away prediction: {away_points_pred}")
                logger.error(f"  Feature vector (first 10): {feature_vector_ordered[:10]}")
                logger.error(f"  Scaled vector (first 10): {feature_vector_scaled[0, :10]}")
                logger.error(f"  Feature vector stats: min={np.min(feature_vector_ordered):.2f}, max={np.max(feature_vector_ordered):.2f}, mean={np.mean(feature_vector_ordered):.2f}, std={np.std(feature_vector_ordered):.2f}")
                logger.error(f"  Scaled vector stats: min={np.min(feature_vector_scaled):.2f}, max={np.max(feature_vector_scaled):.2f}, mean={np.mean(feature_vector_scaled):.2f}, std={np.std(feature_vector_scaled):.2f}")
                
                # Check if model has coefficients (linear model)
                if hasattr(self.model['home'], 'coef_'):
                    logger.error(f"  Home model intercept: {self.model['home'].intercept_}")
                    logger.error(f"  Home model coef range: min={np.min(self.model['home'].coef_):.2f}, max={np.max(self.model['home'].coef_):.2f}")
                    logger.error(f"  Away model intercept: {self.model['away'].intercept_}")
                    logger.error(f"  Away model coef range: min={np.min(self.model['away'].coef_):.2f}, max={np.max(self.model['away'].coef_):.2f}")
            
            # Validate predictions are reasonable (NBA games typically score 80-150 points)
            if home_points_pred < 0 or home_points_pred > 200:
                logger.warning(f"Unusual home points prediction: {home_points_pred}. Clamping to reasonable range.")
                home_points_pred = max(0, min(200, home_points_pred))
            
            if away_points_pred < 0 or away_points_pred > 200:
                logger.warning(f"Unusual away points prediction: {away_points_pred}. Clamping to reasonable range.")
                away_points_pred = max(0, min(200, away_points_pred))
        
        # Get feature contributions
        contributions = {}
        
        if self.target_type == 'margin':
            # Margin-only model: single model feature contributions
            if hasattr(self.model, 'coef_'):
                # Linear model (Ridge, ElasticNet) - use coefficients
                margin_coef = self.model.coef_
                if len(margin_coef.shape) > 1:
                    margin_coef = margin_coef[0]
                
                for i, feature_name in enumerate(self.feature_names):
                    contributions[feature_name] = {
                        'margin': float(margin_coef[i] * feature_vector_scaled[0, i])
                    }
            elif use_shap and SHAP_AVAILABLE:
                # Non-linear model - use SHAP
                try:
                    if isinstance(self.model, (RandomForestRegressor, xgb.XGBRegressor if XGBOOST_AVAILABLE else type(None))):
                        explainer = shap.TreeExplainer(self.model)
                    else:
                        explainer = shap.KernelExplainer(self.model.predict, feature_vector_scaled[:10])
                    
                    shap_values = explainer.shap_values(feature_vector_scaled)
                    
                    for i, feature_name in enumerate(self.feature_names):
                        contributions[feature_name] = {
                            'margin': float(shap_values[0][i]) if len(shap_values.shape) > 1 else float(shap_values[i])
                        }
                except Exception as e:
                    logger.warning(f"SHAP calculation failed: {e}. Using feature importance instead.")
                    if hasattr(self.model, 'feature_importances_'):
                        margin_importance = self.model.feature_importances_
                        for i, feature_name in enumerate(self.feature_names):
                            contributions[feature_name] = {
                                'margin': float(margin_importance[i] * feature_vector_scaled[0, i])
                            }
            elif hasattr(self.model, 'feature_importances_'):
                # Tree-based model - use feature importance
                margin_importance = self.model.feature_importances_
                for i, feature_name in enumerate(self.feature_names):
                    contributions[feature_name] = {
                        'margin': float(margin_importance[i] * feature_vector_scaled[0, i])
                    }
            
            return {
                'home_points': None,
                'away_points': None,
                'point_total_pred': None,
                'point_diff_pred': float(point_diff_pred),
                'feature_contributions': contributions
            }
        else:
            # Home/away models: existing logic
            if hasattr(self.model['home'], 'coef_'):
                # Linear model (Ridge, ElasticNet) - use coefficients
                home_coef = self.model['home'].coef_
                away_coef = self.model['away'].coef_
                
                for i, feature_name in enumerate(self.feature_names):
                    contributions[feature_name] = {
                        'home': float(home_coef[i] * feature_vector_scaled[0, i]),
                        'away': float(away_coef[i] * feature_vector_scaled[0, i])
                    }
            elif use_shap and SHAP_AVAILABLE:
                # Non-linear model - use SHAP
                try:
                    # Create SHAP explainer (TreeExplainer for tree models, KernelExplainer for others)
                    if isinstance(self.model['home'], (RandomForestRegressor, xgb.XGBRegressor if XGBOOST_AVAILABLE else type(None))):
                        explainer_home = shap.TreeExplainer(self.model['home'])
                        explainer_away = shap.TreeExplainer(self.model['away'])
                    else:
                        # For other models, use KernelExplainer (slower but more general)
                        explainer_home = shap.KernelExplainer(self.model['home'].predict, feature_vector_scaled[:10])
                        explainer_away = shap.KernelExplainer(self.model['away'].predict, feature_vector_scaled[:10])
                    
                    # Calculate SHAP values
                    shap_values_home = explainer_home.shap_values(feature_vector_scaled)
                    shap_values_away = explainer_away.shap_values(feature_vector_scaled)
                    
                    # Convert to feature contributions
                    for i, feature_name in enumerate(self.feature_names):
                        contributions[feature_name] = {
                            'home': float(shap_values_home[0][i]) if len(shap_values_home.shape) > 1 else float(shap_values_home[i]),
                            'away': float(shap_values_away[0][i]) if len(shap_values_away.shape) > 1 else float(shap_values_away[i])
                        }
                except Exception as e:
                    logger.warning(f"SHAP calculation failed: {e}. Using feature importance instead.")
                    # Fallback to feature importance if available
                    if hasattr(self.model['home'], 'feature_importances_'):
                        home_importance = self.model['home'].feature_importances_
                        away_importance = self.model['away'].feature_importances_
                        for i, feature_name in enumerate(self.feature_names):
                            contributions[feature_name] = {
                                'home': float(home_importance[i] * feature_vector_scaled[0, i]),
                                'away': float(away_importance[i] * feature_vector_scaled[0, i])
                            }
            elif hasattr(self.model['home'], 'feature_importances_'):
                # Tree-based model - use feature importance as proxy
                home_importance = self.model['home'].feature_importances_
                away_importance = self.model['away'].feature_importances_
                for i, feature_name in enumerate(self.feature_names):
                    contributions[feature_name] = {
                        'home': float(home_importance[i] * feature_vector_scaled[0, i]),
                        'away': float(away_importance[i] * feature_vector_scaled[0, i])
                    }
            
            return {
                'home_points': float(home_points_pred),
                'away_points': float(away_points_pred),
                'point_total_pred': float(home_points_pred + away_points_pred),
                'point_diff_pred': float(point_diff_pred),
                'feature_contributions': contributions
            }
    
    def generate_diagnostics(self, training_results: Dict, output_path: str = None):
        """Generate diagnostic report and save to reports directory."""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.reports_dir, f"points_regression_{timestamp}.txt")
        
        with open(output_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("NBA POINTS REGRESSION MODEL DIAGNOSTICS\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Model Type: {training_results['model_type']}\n")
            f.write(f"Training Samples: {training_results['n_samples']}\n")
            f.write(f"Features: {training_results['n_features']}\n\n")
            
            f.write("FINAL METRICS (Full Dataset)\n")
            f.write("-" * 70 + "\n")
            metrics = training_results['final_metrics']
            
            f.write("Home Points:\n")
            f.write(f"  MAE:  {metrics['home_mae']:.2f}\n")
            f.write(f"  RMSE: {metrics['home_rmse']:.2f}\n")
            f.write(f"  R²:   {metrics['home_r2']:.4f}\n")
            f.write(f"  MAPE: {metrics['home_mape']:.2f}%\n\n")
            
            f.write("Away Points:\n")
            f.write(f"  MAE:  {metrics['away_mae']:.2f}\n")
            f.write(f"  RMSE: {metrics['away_rmse']:.2f}\n")
            f.write(f"  R²:   {metrics['away_r2']:.4f}\n")
            f.write(f"  MAPE: {metrics['away_mape']:.2f}%\n\n")
            
            f.write("Total Points:\n")
            f.write(f"  MAE:  {metrics['total_mae']:.2f}\n")
            f.write(f"  RMSE: {metrics['total_rmse']:.2f}\n")
            f.write(f"  R²:   {metrics['total_r2']:.4f}\n\n")
            
            f.write("Point Differential:\n")
            f.write(f"  MAE:  {metrics['diff_mae']:.2f}\n")
            f.write(f"  RMSE: {metrics['diff_rmse']:.2f}\n")
            f.write(f"  R²:   {metrics['diff_r2']:.4f}\n\n")
            
            if training_results['model_type'] == 'Ridge' and 'cv_results' in training_results:
                f.write("CROSS-VALIDATION RESULTS (TimeSeriesSplit, 5 folds)\n")
                f.write("-" * 70 + "\n")
                for result in training_results['cv_results']:
                    f.write(f"Alpha: {result['alpha']}\n")
                    f.write(f"  Home MAE: {result['home_mae']:.2f}, Away MAE: {result['away_mae']:.2f}\n")
                    f.write(f"  Combined MAE: {(result['home_mae'] + result['away_mae']) / 2:.2f}\n\n")
        
        logger.info(f"Diagnostics saved to {output_path}")
        return output_path
