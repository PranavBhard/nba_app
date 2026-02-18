"""
BballModel.py - Unified basketball prediction model with enhanced feature engineering

League-aware: Supports multiple basketball leagues (NBA, CBB, etc.) via league config.

Features:
- Classifier mode: predicts home win probability
- Points regression mode: predicts team scores
- Enhanced features: absolute + differential, exponential weighting, rest differential, Elo ratings
- Time-aware train/test splits
- Phase 2 improvements: games_played_so_far, pace, volatility, schedule context, era normalization
- Phase 4 improvements: time-based CV, hyperparameter tuning, probability calibration
"""

import os
import csv
import math
import logging
import tempfile
import threading
from datetime import date, datetime, timedelta
from collections import defaultdict
from pprint import pprint
from typing import Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, GradientBoostingRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss, brier_score_loss
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.calibration import CalibratedClassifierCV

from bball.mongo import Mongo
from bball.features.compute import BasketballFeatureComputer
from bball.utils.collection import import_collection
from bball.data import GamesRepository, PlayerStatsRepository, RostersRepository, PointsConfigRepository
from bball.league_config import LeagueConfig, load_league_config
from bball.services.espn_sync import pull_matchups
# Note: get_matchups_with_venue imported lazily in predict_today() to avoid circular import
from bball.stats.league_cache import (
    get_season_stats_with_fallback,
    get_league_constants,
    get_team_pace,
    ensure_season_cached
)
from bball.stats.per_calculator import PERCalculator
from bball.features.parser import parse_feature_name
from bball.features.registry import FeatureRegistry


class BballModel:
    """
    Unified basketball prediction model with enhanced feature engineering.

    League-aware: Supports NBA, CBB, and other basketball leagues via league config.

    Usage:
        from bball.league_config import load_league_config

        # For NBA (default)
        model = BballModel(classifier_features, points_features)

        # For CBB or other leagues
        league = load_league_config('cbb')
        model = BballModel(classifier_features, points_features, league=league)

        model.create_training_data(query)
        model.test_training_data()
        model.rate_features()
        model.predict('2025-01-15')  # or model.predict() for today
    """
    
    # Default MongoDB query for training data
    # Includes all available data - season filtering done at training time if needed
    DEFAULT_QUERY = {
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']},
        'season': {'$exists': True}  # Just require season field exists
    }
    
    # Available ML models for classification
    CLASSIFIERS = {
        'LogisticRegression': LogisticRegression(max_iter=10000, random_state=42),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'NaiveBayes': GaussianNB(),
        'NeuralNetwork': MLPClassifier(max_iter=10000, random_state=42)
    }
    
    # GBM hyperparameter grid for tuning
    GBM_PARAM_GRID = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 4, 5],
        'subsample': [0.8, 1.0],
        'min_samples_leaf': [1, 2, 5]
    }
    
    # Smaller grid for quick tuning
    GBM_PARAM_GRID_SMALL = {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1],
        'max_depth': [3, 5],
        'subsample': [0.8, 1.0]
    }
    
    def __init__(
        self,
        classifier_features: list,
        points_features: list = None,
        include_elo: bool = True,
        use_exponential_weighting: bool = True,
        exponential_lambda: float = 0.1,
        include_era_normalization: bool = False,
        include_per_features: bool = True,
        include_injuries: bool = False,
        recency_decay_k: float = 15.0,
        output_dir: str = './model_output',
        preload_data: bool = True,
        master_training_mode: bool = False,
        league: LeagueConfig = None,
        max_workers: int = None
    ):
        """
        Initialize BballModel.

        Args:
            classifier_features: List of feature names  (e.g., ['points|season|avg|diff', 'wins|season|avg|diff'])
            points_features: List of feature tokens for points regression (optional)
            include_elo: If True, compute and include Elo ratings as features
            use_exponential_weighting: If True, apply exponential decay to historical averages
            exponential_lambda: Decay rate for exponential weighting (higher = more recent bias)
            include_era_normalization: If True, include era-normalized features
            Note: Enhanced features (pace, volatility, schedule, games_played) are always included (team-level only)
            include_per_features: If True, include Player Efficiency Rating (PER) based team features
            output_dir: Directory for output files (CSVs, predictions)
            preload_data: If True, preload all game data and player stats (fast for training, slow init).
                         If False, skip preloading and query on-demand (fast init, slower per-query for prediction).
            league: LeagueConfig for the target league. If None, defaults to NBA.
        """
        # Initialize league config (default to NBA if not provided)
        if league is None:
            league = load_league_config("nba")
        self.league = league
        # Validate classifier features against FeatureRegistry (SSoT)
        if classifier_features:
            validation_result = FeatureRegistry.validate_feature_list(classifier_features)
            if not validation_result["valid"]:
                invalid_list = "\n  ".join(validation_result["errors"][:10])  # Show first 10
                raise ValueError(
                    f"Invalid classifier features detected (SSoT violation):\n  {invalid_list}\n"
                    f"Total invalid: {len(validation_result['invalid_features'])}. "
                    "All features must be valid according to FeatureRegistry."
                )

        self.classifier_features = classifier_features
        self.points_features = points_features or []
        self.include_elo = include_elo
        self.use_exponential_weighting = use_exponential_weighting
        self.exponential_lambda = exponential_lambda
        self.include_era_normalization = include_era_normalization
        self.include_per_features = include_per_features
        self.include_injuries = include_injuries
        self.recency_decay_k = recency_decay_k
        self.master_training_mode = master_training_mode
        self.max_workers = max_workers  # None = use CPU count (default)
        # Determine default consolidated output directory one level above project root
        try:
            _project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            _parent_root = os.path.dirname(_project_root)
            _default_output = os.path.join(_parent_root, 'model_outputs')
        except Exception:
            _default_output = './model_outputs'

        # If caller left default './model_output' or None, use consolidated default
        if output_dir in (None, './model_output'):
            self.output_dir = _default_output
        else:
            self.output_dir = output_dir
        
        # Initialize MongoDB connection
        print("Connecting to MongoDB...")
        self.mongo = Mongo()
        self.db = self.mongo.db
        print("Connected to MongoDB.")

        # Initialize repositories with league config
        self._games_repo = GamesRepository(self.db, league=self.league)
        self._players_repo = PlayerStatsRepository(self.db, league=self.league)
        self._rosters_repo = RostersRepository(self.db, league=self.league)
        self._points_config_repo = PointsConfigRepository(self.db, league=self.league)

        # Get collection name from league config
        games_collection = self.league.collections.get("games", "stats_nba")

        # Load game data once (shared between stat handlers) - only if preloading
        all_games = None
        if preload_data:
            print(f"Loading game data from {games_collection} (this may take a moment)...")
            all_games = import_collection(games_collection)
            self.all_games = all_games
            print(f"Loaded game data.")
        else:
            self.all_games = None
            print("Skipping game data preloading (will query on-demand)")
        
        # Compute league averages for era normalization if enabled
        self.league_averages = {}
        if include_era_normalization:
            if all_games:
                print("Computing league averages for era normalization...")
                self.league_averages = self._compute_league_averages(all_games)
            else:
                print("Warning: Era normalization requires preloaded data, but preload_data=False")
        
        # Initialize BasketballFeatureComputer for regular features
        print("Initializing feature computers...")
        _alpha = exponential_lambda if use_exponential_weighting else 0.0
        self._computer = BasketballFeatureComputer(db=self.db, league=self.league, recency_alpha=_alpha)
        if all_games:
            games_home, games_away = all_games
            self._computer.set_preloaded_data(games_home, games_away)
        # Preload venue cache for travel feature calculations (lightweight, always do it)
        try:
            self._computer.preload_venue_cache()
        except Exception:
            pass

        if points_features:
            self._points_computer = BasketballFeatureComputer(db=self.db, league=self.league, recency_alpha=_alpha)
            if all_games:
                games_home, games_away = all_games
                self._points_computer.set_preloaded_data(games_home, games_away)
        else:
            self._points_computer = None
        
        # Initialize PER calculator if enabled
        self.per_calculator = None
        if include_per_features:
            if preload_data:
                print("Initializing PER calculator (preloading player stats)...")
                self.per_calculator = PERCalculator(self.db, preload=True, league=self.league)
            else:
                print("Initializing PER calculator (no preloading - will query on-demand)...")
                self.per_calculator = PERCalculator(self.db, preload=False, league=self.league)
        else:
            print("PER features disabled - skipping PER calculator initialization.")
        
        print("Initialization complete.")
        
        # Elo ratings cache
        self.elo_ratings = {}
        self.elo_history = {}
        
        # Training data paths
        self.classifier_csv = "./model_output/classifier_training_20251127_024650.csv"
        self.points_csv = None
        
        # Trained models
        self.classifier_model = None
        self.calibrated_model = None
        self.points_model = None
        self.scaler = None
        self.feature_names = []
        self.best_params = None
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    # =========================================================================
    # PREDICTION CONTEXT INJECTION
    # =========================================================================

    def set_prediction_context(self, context) -> None:
        """
        Inject preloaded prediction context to avoid per-feature DB calls.

        This method injects preloaded game data, player stats, and venue cache
        into the feature computer and per_calculator, enabling in-memory feature
        calculations instead of per-feature database queries.

        Args:
            context: PredictionContext instance with preloaded data:
                - games_home: Dict[season][date][team] -> game_doc
                - games_away: Dict[season][date][team] -> game_doc
                - player_stats: Dict[(team, season)] -> [player_records]
                - venue_cache: Dict[venue_guid] -> (lat, lon)
        """
        if context is None:
            return

        # Inject into _computer (for regular stat features)
        if hasattr(self, '_computer') and self._computer:
            self._computer.set_preloaded_data(
                context.games_home, context.games_away,
                venue_cache=context.venue_cache,
            )

        # Inject into _points_computer if it exists
        if hasattr(self, '_points_computer') and self._points_computer:
            self._points_computer.set_preloaded_data(
                context.games_home, context.games_away,
                venue_cache=context.venue_cache,
            )

        # Inject into per_calculator (for PER/injury features)
        if hasattr(self, 'per_calculator') and self.per_calculator:
            # Convert defaultdict to regular dict for compatibility
            player_stats = dict(context.player_stats)
            self.per_calculator._player_stats_cache = player_stats
            self.per_calculator._preloaded = True
            # Inject cross-team cache for traded player support in prediction
            if hasattr(context, 'player_stats_by_player') and context.player_stats_by_player:
                self.per_calculator._player_stats_by_player = dict(context.player_stats_by_player)

        # Inject into ensemble predictor if it exists (for ensemble models)
        if hasattr(self, '_ensemble_predictor') and self._ensemble_predictor:
            self._ensemble_predictor.set_prediction_context(context)

        # Store reference to context for debugging/stats
        self._prediction_context = context

    # =========================================================================
    # LEAGUE AVERAGES FOR ERA NORMALIZATION
    # =========================================================================
    
    def _compute_league_averages(self, all_games: list) -> dict:
        """
        Compute league-wide averages per season for era normalization.
        
        Uses cached league stats from MongoDB if available, falls back to computation.
        
        Returns:
            Dict of {season: {stat: avg_value}}
        """
        home_games = all_games[0]
        averages = {}
        
        # First, try to use cached stats from MongoDB
        for season in home_games.keys():
            cached = get_season_stats_with_fallback(season, self.db)
            if cached:
                lg = cached['league_constants']
                averages[season] = {
                    'ppg': cached['league_totals']['PTS'] / cached['league_totals']['team_games'],
                    'off_rtg': 100 * cached['league_constants']['VOP'],  # Approximate
                    'pace': cached['lg_pace'],
                    'efg': (cached['league_totals']['FG'] + 0.5 * cached['league_totals'].get('three_made', 0)) / 
                           cached['league_totals']['FGA'] if cached['league_totals']['FGA'] > 0 else 0,
                    # Store full PER constants for later use
                    'factor': lg['factor'],
                    'VOP': lg['VOP'],
                    'DRB_pct': lg['DRB_pct']
                }
                continue
            
            # Fallback to computing from loaded games if not cached
            season_stats = {
                'ppg': [], 'off_rtg': [], 'pace': [], 'efg': []
            }
            
            dates = home_games.get(season, {})
            for date_str, games in dates.items():
                for team, game in games.items():
                    if game.get('game_type') == 'preseason':
                        continue
                    
                    for side in ['homeTeam', 'awayTeam']:
                        team_data = game[side]
                        pts = team_data.get('points', 0)
                        fg_att = team_data.get('FG_att', 1)
                        fg_made = team_data.get('FG_made', 0)
                        three_made = team_data.get('three_made', 0)
                        ft_att = team_data.get('FT_att', 0)
                        off_reb = team_data.get('off_reb', 0)
                        to = team_data.get('TO', 0)
                        
                        if fg_att > 0:
                            possessions = fg_att - off_reb + to + (0.4 * ft_att)
                            if possessions > 0:
                                season_stats['ppg'].append(pts)
                                season_stats['off_rtg'].append(100 * pts / possessions)
                                season_stats['pace'].append(possessions)
                                season_stats['efg'].append((fg_made + 0.5 * three_made) / fg_att)
            
            if season_stats['ppg']:
                averages[season] = {
                    'ppg': np.mean(season_stats['ppg']),
                    'off_rtg': np.mean(season_stats['off_rtg']),
                    'pace': np.mean(season_stats['pace']),
                    'efg': np.mean(season_stats['efg'])
                }
        
        return averages
    
    def get_cached_league_constants(self, season: str) -> dict:
        """
        Get league constants for PER calculation from MongoDB cache.
        
        Args:
            season: Season string (e.g., '2024-2025')
            
        Returns:
            Dict with factor, VOP, DRB_pct, lg_pace, and foul term components
        """
        return get_league_constants(season, self.db)
    
    def get_cached_team_pace(self, season: str, team: str) -> float:
        """
        Get team's average pace from MongoDB cache.
        
        Args:
            season: Season string
            team: Team name
            
        Returns:
            Average possessions per game for team
        """
        return get_team_pace(season, team, self.db)
    
    def ensure_league_stats_cached(self, seasons: list = None):
        """
        Ensure league stats are cached for the given seasons.
        
        Args:
            seasons: List of season strings. If None, uses all seasons from DEFAULT_QUERY.
        """
        if seasons is None:
            # Get seasons from loaded games
            seasons = list(self.all_games[0].keys())
        
        print(f"Ensuring league stats cached for {len(seasons)} seasons...")
        for season in seasons:
            ensure_season_cached(season, self.db)
    
    # =========================================================================
    # PER-BASED FEATURES
    # =========================================================================
    
    def _get_per_features(self, home_team: str, away_team: str, season: str, game_date: str, 
                         player_filters: Optional[Dict] = None, injured_players: Optional[Dict] = None) -> dict:
        """
        Get PER-based features for a game.
        
        Uses PERCalculator to compute team-level PER aggregates based on
        player stats up to (but not including) the game date.
        
        Args:
            home_team: Home team name
            away_team: Away team name
            season: Season string (e.g., '2024-2025')
            game_date: Game date string (YYYY-MM-DD)
            player_filters: Optional dict with team names as keys:
                {team: {'playing': [player_ids], 'starters': [player_ids]}}
            injured_players: Optional dict with team names as keys:
                {team: [player_ids]} - List of injured player IDs for each team
                Training: Should pass stats_nba.{home/away}Team.injured_players
                Prediction: Should pass injured players from nba_rosters.injured flag
            
        Returns:
            Dict with PER features or None if data unavailable
        """
        if not self.per_calculator:
            return None
        
        try:
            per_features = self.per_calculator.get_game_per_features(
                home_team, away_team, season, game_date, 
                player_filters=player_filters,
                injured_players=injured_players
            )
            return per_features
        except Exception as e:
            # PER data may not be available for all games (e.g., missing player stats)
            return None
    
    # =========================================================================
    # ELO RATING SYSTEM
    # =========================================================================
    
    def _compute_elo_ratings(self, games: list, starting_elo: float = 1500, K: float = 20, home_advantage: float = 100):
        """
        Compute Elo ratings for all teams based on game history.
        
        Args:
            games: List of game documents sorted chronologically
            starting_elo: Initial Elo for new teams
            K: Elo K-factor (sensitivity to results)
            home_advantage: Elo points added for home team
        """
        elo = defaultdict(lambda: starting_elo)
        self.elo_history = {}
        
        # Filter out games without 'season' field
        games_with_season = [g for g in games if 'season' in g and g.get('season')]
        if len(games_with_season) < len(games):
            print(f"Warning: {len(games) - len(games_with_season)} games missing 'season' field in Elo calculation, excluding them")
        
        for game in sorted(games_with_season, key=lambda g: g.get('date', '')):
            # Additional safety checks
            if 'homeTeam' not in game or 'awayTeam' not in game or 'date' not in game:
                continue
            if 'homeWon' not in game:
                # Skip games without result
                continue
                
            home = game['homeTeam']['name']
            away = game['awayTeam']['name']
            game_date = game['date']
            season = game['season']
            
            # Store pre-game Elo
            key = (home, game_date, season)
            self.elo_history[key] = elo[home]
            key = (away, game_date, season)
            self.elo_history[key] = elo[away]
            
            # Calculate expected win probability for home team
            home_elo_adj = elo[home] + home_advantage
            expected_home = 1 / (1 + 10 ** ((elo[away] - home_elo_adj) / 400))
            
            # Update based on result
            actual_home = 1 if game['homeWon'] else 0
            elo_change = K * (actual_home - expected_home)
            
            elo[home] += elo_change
            elo[away] -= elo_change
        
        self.elo_ratings = dict(elo)
    
    def _get_elo_for_game(self, team: str, game_date: str, season: str) -> float:
        """Get pre-game Elo rating for a team."""
        key = (team, game_date, season)
        return self.elo_history.get(key, 1500)
    
    def _get_current_elo(self, team: str) -> float:
        """Get current Elo rating for a team."""
        return self.elo_ratings.get(team, 1500)
    
    # =========================================================================
    # REST/FATIGUE CALCULATIONS
    # =========================================================================
    
    def _get_days_rest(self, team: str, year: int, month: int, day: int, games: list) -> int:
        """
        Calculate days since team's last game.
        
        Returns:
            Number of days since last game (capped at 7 if no recent game found)
        """
        target_date = date(year, month, day)
        
        for game in sorted(games, key=lambda g: g['date'], reverse=True):
            game_date = datetime.strptime(game['date'], '%Y-%m-%d').date()
            if game_date < target_date:
                team_in_game = (
                    game['homeTeam']['name'] == team or 
                    game['awayTeam']['name'] == team
                )
                if team_in_game:
                    return (target_date - game_date).days
        
        return 7  # Default if no prior games found
    
    # =========================================================================
    # TRAINING DATA CREATION
    # =========================================================================
    
    def _process_game_chunk(
        self,
        games_chunk: list,
        chunk_idx: int,
        feature_headers: list,
        min_games_filter: int,
        include_points: bool,
        progress_callback: callable = None,
        total_games: int = None,
    ) -> tuple:
        """
        Process a chunk of games and write to a temporary CSV file.
        This method is designed to be called in parallel by multiple threads.
        
        Args:
            games_chunk: List of game documents to process
            chunk_idx: Index of this chunk (for temp file naming)
            feature_headers: List of feature header names
            min_games_filter: Minimum games filter
            include_points: Whether to generate points regression data
            progress_callback: Optional callback function to report progress (processed, skipped, total)
            total_games: Total number of games being processed (for progress calculation)
            
        Returns:
            Tuple of (temp_csv_path, games_processed_count, skipped_count)
        """
        # Create temp file for this chunk
        temp_fd, temp_path = tempfile.mkstemp(suffix='.csv', prefix=f'training_chunk_{chunk_idx}_', dir=self.output_dir)
        os.close(temp_fd)  # Close file descriptor, we'll open it properly for writing
        
        classifier_rows = []
        points_rows = []
        games_processed = 0
        skipped_count = 0
        last_progress_report = 0  # Track games processed since last progress report
        
        # Adjust reporting frequency based on chunk size
        # For small chunks, report every game; for larger chunks, report every 10 games
        report_interval = 1 if len(games_chunk) <= 100 else 10
        
        # Import time for timing info
        import time
        chunk_start_time = time.time()
        
        # Log chunk start for visibility
        if total_games and total_games <= 100:
            print(f"  [Chunk {chunk_idx}] Starting to process {len(games_chunk)} games...")
        
        for game_idx, game in enumerate(games_chunk):
            game_start_time = time.time()
            
            # Skip games without season field
            if 'season' not in game or not game.get('season'):
                skipped_count += 1
                continue
            
            home_team = game['homeTeam']['name']
            away_team = game['awayTeam']['name']
            year = game['year']
            month = game['month']
            day = game['day']
            season = game['season']
            game_date = game['date']
            venue_guid = game.get('venue_guid')  # For travel feature calculation

            # Build features
            # Use _build_features_dict
            # Note: _build_features_dict already includes Elo, rest, enhanced, era, PER, injury features
            game_id = game.get('game_id')
            player_filters = None
            if game_id and hasattr(self, '_per_player_cache') and game_id in self._per_player_cache:
                home_players_in_game = self._per_player_cache[game_id].get(home_team, [])
                away_players_in_game = self._per_player_cache[game_id].get(away_team, [])
                if home_players_in_game or away_players_in_game:
                    home_playing = [p['player_id'] for p in home_players_in_game]
                    away_playing = [p['player_id'] for p in away_players_in_game]
                    home_starters = [p['player_id'] for p in home_players_in_game if p.get('starter', False)]
                    away_starters = [p['player_id'] for p in away_players_in_game if p.get('starter', False)]
                    player_filters = {
                        home_team: {'playing': home_playing, 'starters': home_starters},
                        away_team: {'playing': away_playing, 'starters': away_starters}
                    }
            
            step_start = time.time()
            features_dict = self._build_features_dict(
                home_team, away_team, season, year, month, day,
                player_filters=player_filters, target_venue_guid=venue_guid,
                game_doc=game  # Pass game doc to avoid DB query for injured players
            )
            step_time = time.time() - step_start
            
            if features_dict is None:
                skipped_count += 1
                # Log why the game was skipped
                import logging
                logging.warning(f"Skipping game {away_team} @ {home_team} ({year}-{month:02d}-{day:02d}): _build_features_dict returned None")
                if progress_callback and total_games:
                    progress_callback(0, 1, total_games)
                continue
            
            # Get games_played feature names (needed for filtering)
            home_gp_feature = 'games_played|season|avg|home'
            away_gp_feature = 'games_played|season|avg|away'
            
            # Apply min_games_filter (enhanced features always enabled)
            if min_games_filter > 0:
                if home_gp_feature in features_dict and away_gp_feature in features_dict:
                    home_gp = features_dict[home_gp_feature]
                    away_gp = features_dict[away_gp_feature]
                    # Handle None, NaN, or invalid values
                    try:
                        home_gp = float(home_gp) if home_gp is not None else 0.0
                        away_gp = float(away_gp) if away_gp is not None else 0.0
                        if np.isnan(home_gp) or np.isinf(home_gp):
                            home_gp = 0.0
                        if np.isnan(away_gp) or np.isinf(away_gp):
                            away_gp = 0.0
                    except (ValueError, TypeError):
                        home_gp = 0.0
                        away_gp = 0.0
                    
                    min_gp = min(home_gp, away_gp)
                    if min_gp < min_games_filter:
                        skipped_count += 1
                        # Log first 3 skipped games to diagnose filtering issue
                        if skipped_count <= 3:
                            logging.warning(
                                f"Filtered: {away_team} @ {home_team} ({year}-{month:02d}-{day:02d}, {season}): "
                                f"games_played={min_gp:.0f} < {min_games_filter} (home={home_gp:.0f}, away={away_gp:.0f})"
                            )
                        continue
                else:
                    # games_played features missing
                    missing = [f for f in [home_gp_feature, away_gp_feature] if f not in features_dict]
                    if skipped_count == 0:
                        import logging
                        logging.warning(
                            f"games_played features missing from features_dict: {missing}. "
                            f"This may cause all games to be filtered out."
                        )
                    skipped_count += 1
                    continue
            
            # Map features_dict to feature_headers order
            features = [features_dict.get(fname, 0.0) for fname in feature_headers]
            
            # Check if features list matches header length
            if len(features) != len(feature_headers):
                missing = set(feature_headers) - set(features_dict.keys())
                import logging
                logging.warning(
                    f"Game {away_team} @ {home_team}: features length ({len(features)}) != headers length ({len(feature_headers)}). "
                    f"Missing {len(missing)} features: {list(missing)[:10]}..."
                )
                continue
            
            # Sanitize feature values 
            sanitized_features = []
            for f in features:
                if isinstance(f, (float, np.floating)):
                    if np.isnan(f) or np.isinf(f):
                        sanitized_features.append('0')
                    else:
                        sanitized_features.append(str(f))
                elif isinstance(f, (int, np.integer)):
                    sanitized_features.append(str(f))
                else:
                    val_str = str(f).replace(',', '').replace('\n', '').replace('\r', '')
                    sanitized_features.append(val_str)
            
            # Build classifier row
            # Skip games without result
            if 'homeWon' not in game:
                skipped_count += 1
                continue
            won = 1 if game['homeWon'] else 0
            
            # Extract game_id, home_points, away_points
            game_id = game.get('game_id', '') or ''
            home_points = game.get('homeTeam', {}).get('points', 0) or 0
            away_points = game.get('awayTeam', {}).get('points', 0) or 0
            
            # Row format: [Year, Month, Day, Home, Away, game_id, ...features..., HomeWon, home_points, away_points]
            row = [str(year), str(month), str(day), home_team, away_team, str(game_id)] + sanitized_features + [str(won), str(home_points), str(away_points)]
            
            # Verify row length matches expected
            expected_row_len = 6 + len(feature_headers) + 3  # meta (6: Year, Month, Day, Home, Away, game_id) + features + targets (HomeWon, home_points, away_points)
            if len(row) != expected_row_len:
                import logging
                logging.warning(f"Game {away_team} @ {home_team}: row length ({len(row)}) != expected ({expected_row_len}). Headers: {len(feature_headers)}, features: {len(sanitized_features)}")
                continue
            
            classifier_rows.append(row)
            games_processed += 1
            
            game_elapsed = time.time() - game_start_time
            
            # Report progress incrementally based on report_interval
            # Report EVERY game for small batches to see what's happening
            games_since_last_report = games_processed - last_progress_report
            should_report = (games_since_last_report >= report_interval or 
                           game_idx == len(games_chunk) - 1 or
                           (total_games and total_games <= 100))  # Always report for small batches
            
            # Only report if we have games to report and haven't already reported them
            if progress_callback and total_games and should_report and games_since_last_report > 0:
                progress_callback(games_since_last_report, 0, total_games)
                last_progress_report = games_processed  # Update BEFORE next iteration to prevent double-counting
                # Also print directly for visibility (helps debug)
                if total_games <= 100 or game_elapsed > 5:  # Print slow games or all games for small batches
                    elapsed_str = f"{game_elapsed:.1f}s" if game_elapsed > 1 else "<1s"
                    print(f"  [Chunk {chunk_idx}] Processed game {game_idx + 1}/{len(games_chunk)}: {away_team} @ {home_team} ({year}-{month:02d}-{day:02d}) in {elapsed_str}")
        
        # Report any remaining progress for this chunk (only if there's actually remaining)
        remaining = games_processed - last_progress_report
        if progress_callback and total_games and remaining > 0:
            progress_callback(remaining, 0, total_games)
            last_progress_report = games_processed  # Update to prevent double-reporting
        
        # Sort classifier rows chronologically (year, month, day)
        classifier_rows.sort(key=lambda row: (
            int(row[0]) if row[0].isdigit() else 0,  # Year
            int(row[1]) if row[1].isdigit() else 0,  # Month
            int(row[2]) if row[2].isdigit() else 0   # Day
        ))
        
        # Write chunk to temp CSV
        with open(temp_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(classifier_rows)
        
        return temp_path, None, games_processed, skipped_count
    
    def create_training_data(
        self,
        query: dict = None,
        classifier_csv: str = None,
        points_csv: str = None,
        standardize: bool = False,
        total_only: bool = False,
        min_games_filter: int = 15,
        progress_callback: callable = None,
    ) -> tuple:
        """
        Create training data CSVs from MongoDB game data.
        
        Args:
            query: MongoDB query filter (uses DEFAULT_QUERY if None)
            classifier_csv: Output path for classifier training data
            points_csv: Output path for points regression data
            standardize: If True, standardize features after creation
            total_only: If True, just return game count without creating CSV
            min_games_filter: If > 0, skip games where min(homeGamesPlayed, awayGamesPlayed) < this value
            progress_callback: Optional callback function(current, total, progress_pct) called every ~7.5% progress
            
        Returns:
            Tuple of (game_count, classifier_csv_path, points_csv_path)
        """
        query = query or self.DEFAULT_QUERY
        
        # Fetch games from MongoDB
        print("Fetching games from database...")
        print(f"  Query: {query}")
        print(f"  Collection: {self.league.collections.get('games', 'stats_nba')}")
        games = self._games_repo.find(query)
        game_count = len(games)
        print(f"Found {game_count} games from {self.league.collections.get('games', 'stats_nba')} collection")
        if game_count > 0:
            print(f"  Sample game keys: {list(games[0].keys())[:10]}")
            print(f"  Sample game has 'season': {'season' in games[0]}")
            print(f"  Sample game has 'homeWon': {'homeWon' in games[0]}")
        
        # Filter out games without 'season' field
        games_with_season = [g for g in games if 'season' in g and g.get('season')]
        if len(games_with_season) < len(games):
            print(f"Warning: {len(games) - len(games_with_season)} games missing 'season' field, excluding them")
        games = games_with_season
        game_count = len(games)
        print(f"Processing {game_count} games with season data")
        
        # Sort games chronologically (year, month, day) to ensure training data is in order
        print("Sorting games chronologically...")
        games.sort(key=lambda g: (
            g.get('year', 0),
            g.get('month', 0),
            g.get('day', 0),
            g.get('homeTeam', {}).get('name', ''),
            g.get('awayTeam', {}).get('name', '')
        ))
        
        if total_only:
            return game_count, None, None
        
        # Ensure league stats are cached for all seasons in the data
        seasons_in_data = set(g['season'] for g in games if 'season' in g)
        self.ensure_league_stats_cached(list(seasons_in_data))

        import time as _time
        print(f"\n{'='*70}")
        print(f"  PRELOADING DATA CACHES")
        print(f"{'='*70}")

        # Preload venue cache to avoid per-game DB queries
        print("  [1/4] Venue locations...", end=" ", flush=True)
        t0 = _time.time()
        self._computer.preload_venue_cache()
        if self._points_computer:
            self._points_computer.preload_venue_cache()
        print(f"✓ {len(self._computer._venue_cache):,} venues ({_time.time()-t0:.1f}s)")

        # Preload injury cache if injury features are enabled
        if self.include_injuries:
            print("  [2/4] Injury feature cache...", end=" ", flush=True)
            t0 = _time.time()
            if not hasattr(self, '_injury_calculator'):
                from bball.features.injury import InjuryFeatureCalculator
                self._injury_calculator = InjuryFeatureCalculator(
                    db=self.db, league=self.league, batch_training_mode=True,
                )
                if self.all_games:
                    gh, ga = self.all_games
                    self._injury_calculator.set_preloaded_data(gh, ga)
            self._injury_calculator.preload_injury_cache(games)
            num_teams = len(getattr(self._injury_calculator, '_injury_preloaded_players', {}))
            print(f"✓ {num_teams:,} team-seasons ({_time.time()-t0:.1f}s)")
        else:
            print("  [2/4] Injury features... SKIPPED (disabled)")

        print(f"  [*] Batch training mode: ENABLED")

        # Preload PER player cache to avoid per-game DB queries
        if self.include_per_features and self.per_calculator:
            print("  [3/4] PER player cache...", end=" ", flush=True)
            t0 = _time.time()
            game_ids = [g.get('game_id') for g in games if g.get('game_id')]
            if game_ids:
                # Preload all players for all games in one query
                all_players = self._players_repo.find(
                    {'game_id': {'$in': game_ids}, 'stats.min': {'$gt': 0}},
                    projection={'game_id': 1, 'team': 1, 'player_id': 1, 'starter': 1}
                )
                # Build cache: game_id -> {team: [players]}
                self._per_player_cache = {}
                player_count = 0
                for player in all_players:
                    game_id = player.get('game_id')
                    team = player.get('team')
                    if game_id not in self._per_player_cache:
                        self._per_player_cache[game_id] = {}
                    if team not in self._per_player_cache[game_id]:
                        self._per_player_cache[game_id][team] = []
                    self._per_player_cache[game_id][team].append({
                        'player_id': player.get('player_id'),
                        'starter': player.get('starter', False)
                    })
                    player_count += 1
                print(f"✓ {player_count:,} players across {len(self._per_player_cache):,} games ({_time.time()-t0:.1f}s)")
            else:
                self._per_player_cache = {}
                print("✓ No games (0s)")
        else:
            self._per_player_cache = {}
            print("  [3/4] PER features... SKIPPED (disabled)")

        # Compute Elo ratings if enabled (skip if already computed, e.g., when using --limit)
        if self.include_elo:
            if not hasattr(self, 'elo_history') or not self.elo_history:
                print("  [4/4] Elo ratings...", end=" ", flush=True)
                t0 = _time.time()
                self._compute_elo_ratings(games)
                print(f"✓ {len(self.elo_history):,} game-team ratings ({_time.time()-t0:.1f}s)")
            else:
                print(f"  [4/4] Elo ratings... ✓ Using pre-computed ({len(self.elo_history):,} ratings)")
        else:
            print("  [4/4] Elo features... SKIPPED (disabled)")

        print(f"{'='*70}\n")

        # Build feature headers
        feature_headers = self._build_feature_headers()
        
        # Set feature_names so _build_features_dict 
        self.feature_names = feature_headers
        
        # Set output paths
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.classifier_csv = classifier_csv or os.path.join(
            self.output_dir, f'classifier_training_{timestamp}.csv'
        )
        
        
        # Split games into chunks of 500 for parallel processing
        chunk_size = 500
        game_chunks = [games[i:i + chunk_size] for i in range(0, len(games), chunk_size)]
        num_chunks = len(game_chunks)

        # Determine actual worker count
        import os as _os
        actual_workers = self.max_workers if self.max_workers else _os.cpu_count()

        # Print cache status summary before processing
        print(f"\n{'='*70}")
        print(f"  CACHE STATUS (should all be TRUE for fast processing)")
        print(f"{'='*70}")
        print(f"  _computer preloaded:                 {self._computer.games_home is not None}")
        if hasattr(self, '_injury_calculator'):
            print(f"  _injury_calculator cache_loaded:     {getattr(self._injury_calculator, '_injury_cache_loaded', False)}")
        if self.per_calculator:
            print(f"  per_calculator._preloaded:           {getattr(self.per_calculator, '_preloaded', False)}")
            per_cache_size = len(getattr(self.per_calculator, '_player_stats_cache', {}) or {})
            print(f"  per_calculator._player_stats_cache:  {per_cache_size:,} team-seasons")
        print(f"{'='*70}")

        print(f"\n{'='*70}")
        print(f"  PARALLEL PROCESSING")
        print(f"{'='*70}")
        print(f"  Total games:    {game_count:,}")
        print(f"  Chunks:         {num_chunks} (size ~{chunk_size})")
        print(f"  Workers:        {actual_workers}")
        print(f"  Chunk/Worker:   ~{num_chunks // actual_workers if actual_workers else num_chunks} chunks per worker")
        print(f"{'='*70}")
        
        # Thread-safe progress tracker
        import time as _time
        progress_lock = threading.Lock()
        progress_state = {
            'processed': 0,
            'skipped': 0,
            'last_logged': 0,
            'start_time': _time.time()
        }
        
        # Progress logging interval (log every N games processed)
        # For small batches, log more frequently; for large batches, log ~50 times
        if game_count <= 100:
            progress_interval = 1  # Log every game for small batches
        elif game_count <= 500:
            progress_interval = max(1, game_count // 20)  # Log ~20 times for medium batches
        else:
            progress_interval = max(1, game_count // 50)  # Log ~50 times for large batches
        
        def log_progress_if_needed(processed, skipped, total):
            """Thread-safe progress logging."""
            import time as _time
            with progress_lock:
                progress_state['processed'] += processed
                progress_state['skipped'] += skipped
                current = progress_state['processed']

                # Cap current at total to avoid >100% (handles any double-counting issues)
                current = min(current, total)

                # Log if we've processed enough games since last log OR if it's a small batch (always log)
                should_log = (current - progress_state['last_logged'] >= progress_interval or
                            current == total or
                            (total <= 100 and processed > 0))  # Always log for small batches

                if should_log:
                    progress_state['last_logged'] = current
                    progress_pct = (current / total) * 100 if total > 0 else 0

                    # Calculate rate and ETA
                    elapsed = _time.time() - progress_state.get('start_time', _time.time())
                    rate = current / elapsed if elapsed > 0 else 0
                    eta_str = ""
                    if rate > 0 and current < total:
                        eta_secs = int((total - current) / rate)
                        eta_mins, eta_secs = divmod(eta_secs, 60)
                        eta_hrs, eta_mins = divmod(eta_mins, 60)
                        if eta_hrs > 0:
                            eta_str = f" | ETA: {eta_hrs}h {eta_mins:02d}m"
                        else:
                            eta_str = f" | ETA: {eta_mins}m {eta_secs:02d}s"

                    if progress_callback:
                        progress_callback(current, total, progress_pct)
                    else:
                        # More descriptive progress format
                        bar_width = 30
                        filled = int(bar_width * progress_pct / 100)
                        bar = "█" * filled + "░" * (bar_width - filled)
                        print(f"  [{bar}] {progress_pct:5.1f}% | {current:,}/{total:,} games | {rate:.1f} games/sec{eta_str}")
        
        # Process chunks in parallel
        temp_csv_files = []
        temp_points_files = []
        total_processed = 0
        total_skipped = 0
        
        # Use ThreadPoolExecutor to process chunks in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:  # None = use default (CPU count)
            # Submit all chunks
            future_to_chunk = {
                executor.submit(
                    self._process_game_chunk,
                    chunk,
                    chunk_idx,
                    feature_headers,
                    min_games_filter,
                    False,  # include_points - deprecated, always False
                    log_progress_if_needed,
                    game_count,
                ): chunk_idx
                for chunk_idx, chunk in enumerate(game_chunks)
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_chunk):
                chunk_idx = future_to_chunk[future]
                temp_csv, _, games_processed, skipped = future.result()
                temp_csv_files.append((chunk_idx, temp_csv))
                total_processed += games_processed
                total_skipped += skipped
                completed += 1
                
                # Don't call progress_callback here - log_progress_if_needed already handles progress reporting
                # The progress is already being tracked and reported incrementally from within _process_game_chunk
                # Calling it again here would cause double-counting
                print(f"  ✓ Chunk {chunk_idx + 1}/{num_chunks} complete ({games_processed:,} games)")
        
        # Sort temp files by chunk index to maintain chronological order
        temp_csv_files.sort(key=lambda x: x[0])
        temp_points_files.sort(key=lambda x: x[0])
        
        # Combine all temp CSV files into final output
        print(f"\nCombining {len(temp_csv_files)} chunks into final CSV...")
        
        # Write classifier CSV header
        # Format: [Year, Month, Day, Home, Away, game_id, ...features..., HomeWon, home_points, away_points]
        classifier_header = ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id'] + feature_headers + ['HomeWon', 'home_points', 'away_points']
        
        # Collect all rows from all chunks first, then sort chronologically before writing
        all_rows = []
        for chunk_idx, temp_csv in temp_csv_files:
            with open(temp_csv, 'r', newline='') as infile:
                reader = csv.reader(infile)
                # Temp files don't have headers - they're just data rows, so don't skip anything
                row_count = 0
                for row in reader:
                    row_count += 1
                    # Only add rows that have the expected number of columns
                    # Expected: 6 metadata (Year, Month, Day, Home, Away, game_id) + features + 3 targets (HomeWon, home_points, away_points)
                    expected_cols = len(classifier_header)
                    if len(row) == expected_cols:
                        all_rows.append(row)
                    else:
                        import logging
                        logging.warning(f"Skipping malformed row in chunk {chunk_idx}: expected {expected_cols} columns, got {len(row)}")
                if row_count == 0:
                    print(f"  [WARNING] Chunk {chunk_idx} temp file is empty!")
                elif len(all_rows) == 0:
                    print(f"  [WARNING] Chunk {chunk_idx} had {row_count} rows but none matched expected column count ({len(classifier_header)})")
            # Clean up temp file
            os.remove(temp_csv)
        
        # Sort all rows chronologically (year, month, day, home, away)
        all_rows.sort(key=lambda row: (
            int(row[0]) if len(row) > 0 and row[0].isdigit() else 0,  # Year
            int(row[1]) if len(row) > 1 and row[1].isdigit() else 0,  # Month
            int(row[2]) if len(row) > 2 and row[2].isdigit() else 0,  # Day
            row[3] if len(row) > 3 else '',  # Home team
            row[4] if len(row) > 4 else ''   # Away team
        ))
        
        # Write sorted rows to final CSV
        with open(self.classifier_csv, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(classifier_header)  # Write header (always write header, even if no rows)
            if all_rows:
                writer.writerows(all_rows)
            else:
                print(f"  [WARNING] No valid rows to write to classifier CSV. Header written with {len(classifier_header)} columns: {classifier_header[:5]}...{classifier_header[-1]}")
        
        # Calculate total elapsed time
        total_elapsed = _time.time() - progress_state['start_time']
        elapsed_mins, elapsed_secs = divmod(int(total_elapsed), 60)
        elapsed_hrs, elapsed_mins = divmod(elapsed_mins, 60)
        if elapsed_hrs > 0:
            elapsed_str = f"{elapsed_hrs}h {elapsed_mins:02d}m {elapsed_secs:02d}s"
        else:
            elapsed_str = f"{elapsed_mins}m {elapsed_secs:02d}s"

        avg_rate = total_processed / total_elapsed if total_elapsed > 0 else 0

        print(f"\n{'='*70}")
        print(f"  GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"  Output:         {self.classifier_csv}")
        print(f"  Features:       {len(feature_headers):,}")
        print(f"  Rows written:   {len(all_rows):,}")
        print(f"  Games processed:{total_processed:,}")
        print(f"  Games skipped:  {total_skipped:,}")
        print(f"  Total time:     {elapsed_str}")
        print(f"  Avg rate:       {avg_rate:.1f} games/sec")
        print(f"{'='*70}")
        
        if len(all_rows) == 0:
            print(f"  [ERROR] No rows written to CSV! All {game_count} games were filtered out.")
            print(f"  Most likely cause: min_games_filter={min_games_filter} is too restrictive.")
            print(f"  Check logs above for 'Filtered:' messages showing games_played values.")
            print(f"  Try reducing min_games_played to 5-10 or 0 to include early-season games.")
        
        # Standardize if requested
        if standardize:
            self.classifier_csv = self._standardize_csv(self.classifier_csv)
        
        # Save computed PER features to MongoDB cache
        if self.include_per_features and self.per_calculator:
            print("Saving PER features to cache...")
            self.per_calculator.save_per_features_to_db()
        
        # Return actual number of rows written, not games fetched
        rows_written = len(all_rows)
        return rows_written, self.classifier_csv, None

    def _build_feature_headers(self) -> list:
        """
        Build list of feature column headers.
        
        Generates headers directly from feature names .
        No stat tokens needed - headers are feature names themselves.
        """
        headers = []
        seen = set()  # Track seen headers to prevent duplicates
        
        def add_header(header):
            """Add header if not already seen."""
            if header not in seen:
                seen.add(header)
                headers.append(header)
        
        
        if True:
            # NEW ARCHITECTURE: classifier_features now contains feature names directly 
            # If feature_names is already set, use it directly
            if hasattr(self, 'feature_names') and self.feature_names:
                # Feature names already set - use them directly
                for header in self.feature_names:
                    add_header(header)
            else:
                # Use classifier_features directly (they are now feature names, not stat tokens)
                if self.classifier_features:
                    for header in self.classifier_features:
                        add_header(header)
            
            # Add Elo and rest features
            # Note: Elo uses historical data (all seasons up to game date, cumulative/all-time)
            # Rest is days since last game (point-in-time calculation, no time period needed)
            if self.include_elo:
                add_header('elo|none|raw|diff')
            
            add_header('rest|none|raw|diff')
            
            # Add enhanced features (always included - all team-level)
            enhanced_features = [
                    'games_played|season|avg|home',
                    'games_played|season|avg|away',
                    'games_played|season|avg|diff',
                    'pace|season|avg|home',
                    'pace|season|avg|away',
                    'pace|season|avg|diff',
                    'pace|games_10|avg|home',
                    'pace|games_10|avg|away',
                    'pace|games_10|avg|diff',
                    'points|season|std|home',
                    'points|season|std|away',
                    'points|season|std|diff',
                    'games_played|days_3|avg|home',
                    'games_played|days_3|avg|away',
                    'games_played|days_3|avg|diff',
                    'games_played|days_5|avg|home',
                    'games_played|days_5|avg|away',
                    'games_played|days_5|avg|diff',
                    'days_rest|none|raw|home',
                    'days_rest|none|raw|away',
                    'days_rest|none|raw|diff',
                    'b2b|none|raw|home',
                    'b2b|none|raw|away',
                    'b2b|none|raw|diff',
                    'travel|days_12|avg|home',
                    'travel|days_12|avg|away',
                    'travel|days_12|avg|diff',
                    'travel|days_5|avg|home',
                    'travel|days_5|avg|away',
                    'travel|days_5|avg|diff',

                    # Matchup-scalar possessions/interaction features
                    'pace_interaction_season|none|harmonic_mean|none',
                    'pace_interaction_games_10|none|harmonic_mean|none',
                    'est_possessions_season|none|derived|home',
                    'est_possessions_season|none|derived|away',
                    'est_possessions_games_10|none|derived|home',
                    'est_possessions_games_10|none|derived|away',

                    # Shot-mix attempt rates
                    'three_rate|season|avg|home',
                    'three_rate|season|avg|away',
                    'three_rate|season|avg|diff',
                    'three_rate|games_10|avg|home',
                    'three_rate|games_10|avg|away',
                    'three_rate|games_10|avg|diff',
                    'ft_rate|season|avg|home',
                    'ft_rate|season|avg|away',
                    'ft_rate|season|avg|diff',
                    'ft_rate|games_10|avg|home',
                    'ft_rate|games_10|avg|away',
                    'ft_rate|games_10|avg|diff',

                    # Points decomposition (derived)
                    'exp_points_off_season|none|derived|home',
                    'exp_points_off_season|none|derived|away',
                    'exp_points_off_season|none|derived|diff',
                    'exp_points_off_games_10|none|derived|home',
                    'exp_points_off_games_10|none|derived|away',
                    'exp_points_off_games_10|none|derived|diff',
                    'exp_points_def_season|none|derived|home',
                    'exp_points_def_season|none|derived|away',
                    'exp_points_def_season|none|derived|diff',
                    'exp_points_def_games_10|none|derived|home',
                    'exp_points_def_games_10|none|derived|away',
                    'exp_points_def_games_10|none|derived|diff',
                    'exp_points_matchup_season|none|derived|home',
                    'exp_points_matchup_season|none|derived|away',
                    'exp_points_matchup_games_10|none|derived|home',
                    'exp_points_matchup_games_10|none|derived|away',
                ]
            for header in enhanced_features:
                add_header(header)
            
            # Add PER features 
            # PER features use season time period (player stats up to game date in season)
            if self.include_per_features:
                if self.master_training_mode:
                    # Master training mode: only include the specified player-level features
                    # Include home, away, and diff versions for consistency
                    per_features = [
                        'player_team_per|season|weighted_MPG|diff',
                        'player_team_per|season|weighted_MPG|home',
                        'player_team_per|season|weighted_MPG|away',
                        'player_starters_per|season|avg|diff',
                        'player_starters_per|season|avg|home',
                        'player_starters_per|season|avg|away',
                        'player_per_1|none|weighted_MIN_REC|diff',
                        'player_per_1|none|weighted_MIN_REC|home',
                        'player_per_1|none|weighted_MIN_REC|away',
                        'player_per_1|season|raw|diff',
                        'player_per_1|season|raw|home',
                        'player_per_1|season|raw|away',
                        'player_per_2|season|raw|diff',
                        'player_per_2|season|raw|home',
                        'player_per_2|season|raw|away',
                        'player_per_3|season|raw|diff',
                        'player_per_3|season|raw|home',
                        'player_per_3|season|raw|away',
                        # Format: player_per|season|topN_avg (average PER of top N players)
                        'player_per|season|top1_avg|diff',
                        'player_per|season|top1_avg|home',
                        'player_per|season|top1_avg|away',
                        'player_per|season|top2_avg|diff',
                        'player_per|season|top2_avg|home',
                        'player_per|season|top2_avg|away',
                        'player_per|season|top3_avg|diff',
                        'player_per|season|top3_avg|home',
                        'player_per|season|top3_avg|away',
                        # MPG-weighted versions
                        'player_per|season|top1_weighted_MPG|diff',
                        'player_per|season|top1_weighted_MPG|home',
                        'player_per|season|top1_weighted_MPG|away',
                        'player_per|season|top2_weighted_MPG|diff',
                        'player_per|season|top2_weighted_MPG|home',
                        'player_per|season|top2_weighted_MPG|away',
                        'player_per|season|top3_weighted_MPG|diff',
                        'player_per|season|top3_weighted_MPG|home',
                        'player_per|season|top3_weighted_MPG|away',
                    ]
                else:
                    # Regular training: include all PER features
                    per_features = [
                        'player_team_per|season|avg|home',
                        'player_team_per|season|avg|away',
                        'player_team_per|season|avg|diff',
                        'player_team_per|season|weighted_MPG|home',
                        'player_team_per|season|weighted_MPG|away',
                        'player_team_per|season|weighted_MPG|diff',
                        'player_starters_per|season|avg|home',
                        'player_starters_per|season|avg|away',
                        'player_starters_per|season|avg|diff',
                        # Format: player_per|season|topN_avg (average PER of top N players)
                        'player_per|season|top1_avg|home',
                        'player_per|season|top1_avg|away',
                        'player_per|season|top1_avg|diff',
                        'player_per|season|top2_avg|home',
                        'player_per|season|top2_avg|away',
                        'player_per|season|top2_avg|diff',
                        'player_per|season|top3_avg|home',
                        'player_per|season|top3_avg|away',
                        'player_per|season|top3_avg|diff',
                        # MPG-weighted versions
                        'player_per|season|top1_weighted_MPG|home',
                        'player_per|season|top1_weighted_MPG|away',
                        'player_per|season|top1_weighted_MPG|diff',
                        'player_per|season|top2_weighted_MPG|home',
                        'player_per|season|top2_weighted_MPG|away',
                        'player_per|season|top2_weighted_MPG|diff',
                        'player_per|season|top3_weighted_MPG|home',
                        'player_per|season|top3_weighted_MPG|away',
                        'player_per|season|top3_weighted_MPG|diff',
                        # New PER features for master training
                        'player_per_1|none|weighted_MIN_REC|home',
                        'player_per_1|none|weighted_MIN_REC|away',
                        'player_per_1|none|weighted_MIN_REC|diff',
                        'player_per_2|season|raw|home',
                        'player_per_2|season|raw|away',
                        'player_per_2|season|raw|diff',
                        'per_available|season|none|none',
                    ]
                for header in per_features:
                    add_header(header)
            
            # Add injury features if enabled
            if self.include_injuries:
                if self.master_training_mode:
                    # Master training mode: include injury component features + blend
                    injury_features = [
                        # Core components
                        'inj_severity|none|raw|diff',
                        'inj_severity|none|raw|home',
                        'inj_severity|none|raw|away',
                        'inj_per|none|top1_avg|diff',
                        'inj_per|none|top1_avg|home',
                        'inj_per|none|top1_avg|away',
                        'inj_rotation_per|none|raw|diff',
                        'inj_rotation_per|none|raw|home',
                        'inj_rotation_per|none|raw|away',
                        # Additional components
                        'inj_per|none|weighted_MIN|diff',
                        'inj_per|none|weighted_MIN|home',
                        'inj_per|none|weighted_MIN|away',
                        'inj_per|none|top3_sum|diff',
                        'inj_per|none|top3_sum|home',
                        'inj_per|none|top3_sum|away',
                        'inj_min_lost|none|raw|diff',
                        'inj_min_lost|none|raw|home',
                        'inj_min_lost|none|raw|away',
                        # Injury blend (new notation)
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff',
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home',
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away',
                    ]
                else:
                    # Regular training: include all injury features ()
                    
                    injury_features = [
                        
                        # These should be added back  if needed for regular training
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff',
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home',
                        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away',
                    ]
                for header in injury_features:
                    add_header(header)
            
            return headers

        # PER features (if enabled)
        if self.include_per_features:
            headers.extend([
                # Team PER averages (simple and weighted) - 
                'player_team_per|season|avg|home', 'player_team_per|season|avg|away', 'player_team_per|season|avg|diff',
                'player_team_per|season|weighted_MPG|home', 'player_team_per|season|weighted_MPG|away', 'player_team_per|season|weighted_MPG|diff',
                # Starters PER
                'player_starters_per|season|avg|home', 'player_starters_per|season|avg|away', 'player_starters_per|season|avg|diff',
                # Top player PER slots (1-3)
                'player_per_1|season|top1_avg|home', 'player_per_2|season|top1_avg|home', 'player_per_3|season|top1_avg|home',
                'player_per_1|season|top1_avg|away', 'player_per_2|season|top1_avg|away', 'player_per_3|season|top1_avg|away',
                'player_per_1|season|top1_avg|diff', 'player_per_2|season|top1_avg|diff', 'player_per_3|season|top1_avg|diff',
                # New PER features for master training
                'player_per_1|none|weighted_MIN_REC|home', 'player_per_1|none|weighted_MIN_REC|away', 'player_per_1|none|weighted_MIN_REC|diff',
                'player_per_2|season|raw|home', 'player_per_2|season|raw|away', 'player_per_2|season|raw|diff',
                # PER availability flag
                'per_available|season|none|none',
            ])
        
        # Injury features ()
        if self.include_injuries:
            headers.extend([
                'inj_per|none|weighted_MIN|home', 'inj_per|none|weighted_MIN|away', 'inj_per|none|weighted_MIN|diff',
                'inj_per|none|top1_avg|home', 'inj_per|none|top1_avg|away', 'inj_per|none|top1_avg|diff',
                'inj_per|none|top3_sum|home', 'inj_per|none|top3_sum|away', 'inj_per|none|top3_sum|diff',
                'inj_min_lost|none|raw|home', 'inj_min_lost|none|raw|away', 'inj_min_lost|none|raw|diff',
                'inj_severity|none|raw|home', 'inj_severity|none|raw|away', 'inj_severity|none|raw|diff',
                'inj_rotation_per|none|raw|home', 'inj_rotation_per|none|raw|away', 'inj_rotation_per|none|raw|diff',
                # Injury blend feature
                'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home',
                'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away',
                'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff',
                'inj_impact|blend|raw|diff',  # Legacy alias
            ])
        
        return headers
    
    def _read_csv_safe(self, csv_path: str) -> pd.DataFrame:
        """
        Read CSV file with error handling for trailing empty columns.
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            DataFrame with trailing empty columns removed
        """
        # Use Python engine from the start to handle column mismatches gracefully
        # Read the CSV and manually fix any column count mismatches
        import csv
        
        rows = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            # Remove trailing empty columns from header
            while header and (not header[-1] or header[-1].strip() == ''):
                header.pop()
            expected_cols = len(header)
            
            for row_num, row in enumerate(reader, start=2):
                # Trim row to expected length (remove trailing empty columns)
                if len(row) > expected_cols:
                    # Remove trailing empty columns
                    row = row[:expected_cols]
                elif len(row) < expected_cols:
                    # Pad with empty strings if row is too short
                    row.extend([''] * (expected_cols - len(row)))
                
                # Only add rows that match expected column count
                if len(row) == expected_cols:
                    rows.append(row)
                else:
                    # Log warning for rows that still don't match (shouldn't happen after trimming)
                    import logging
                    logging.warning(f"Row {row_num} has {len(row)} columns, expected {expected_cols}. Skipping.")
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=header)
        
        # Convert numeric columns
        for col in df.columns:
            if col not in ['Home', 'Away', 'Team']:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    pass
        
        # Remove any trailing empty columns (Unnamed columns)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.dropna(axis=1, how='all')
        
        return df

    def _standardize_csv(self, csv_path: str) -> str:
        """Standardize feature columns in a CSV file."""
        df = self._read_csv_safe(csv_path)
        
        # Identify metadata and target columns
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'Team', 'isHome']
        target_cols = ['HomeWon', 'Points']
        
        meta_cols = [c for c in meta_cols if c in df.columns]
        target_col = [c for c in target_cols if c in df.columns][0]
        
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        # Standardize features
        scaler = StandardScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
        
        # Save standardized version
        std_path = csv_path.replace('.csv', '_standardized.csv')
        df.to_csv(std_path, index=False)
        
        print(f"Standardized data written to: {std_path}")
        return std_path
    
    def _print_progress(self, current: int, total: int, bar_length: int = 20):
        """Print progress bar."""
        progress = current / total
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f'\r|{bar}| {current}/{total} ({100*progress:.1f}%)', end='', flush=True)
    
    # =========================================================================
    # MODEL TRAINING & TESTING
    # =========================================================================
    
    def test_training_data(
        self,
        csv_path: str = None,
        test_size: float = 0.1,
        time_split: bool = True,
        n_runs: int = 5,
        season_split: bool = False
    ) -> dict:
        """
        Test model accuracy on training data.
        
        Args:
            csv_path: Path to classifier CSV (uses self.classifier_csv if None)
            test_size: Fraction of data for testing
            time_split: If True, use chronological split instead of random
            n_runs: Number of test runs to average (ignored if time_split=True)
            season_split: If True, split by season for more realistic validation
            
        Returns:
            Dict of model_name -> average accuracy percentage
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available. Run create_training_data first.")
        
        # Load data
        df = self._read_csv_safe(csv_path)
        
        # Separate features and target
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        self.feature_names = feature_cols
        
        results = defaultdict(list)
        
        if time_split:
            # Chronological split - train on earlier games, test on later
            split_idx = int(len(X) * (1 - test_size))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            print(f"\nTime-based split: {split_idx} train, {len(X) - split_idx} test")
            
            for name, model in self.CLASSIFIERS.items():
                # Create fresh model instance
                model_instance = type(model)(**model.get_params())
                model_instance.fit(X_train, y_train)
                preds = model_instance.predict(X_test)
                acc = 100 * accuracy_score(y_test, preds)
                
                # Also compute log loss and Brier score
                if hasattr(model_instance, 'predict_proba'):
                    proba = model_instance.predict_proba(X_test)[:, 1]
                    ll = log_loss(y_test, proba)
                    brier = brier_score_loss(y_test, proba)
                    print(f"  {name}: {acc:.2f}% | Log Loss: {ll:.4f} | Brier: {brier:.4f}")
                else:
                    print(f"  {name}: {acc:.2f}%")
                
                results[name].append(acc)
        else:
            # Random splits with multiple runs
            for run in range(n_runs):
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=run
                )
                
                for name, model in self.CLASSIFIERS.items():
                    # Create fresh model instance
                    model_instance = type(model)(**model.get_params())
                    model_instance.fit(X_train, y_train)
                    preds = model_instance.predict(X_test)
                    acc = 100 * accuracy_score(y_test, preds)
                    results[name].append(acc)
            
            print(f"\nAverage accuracy over {n_runs} runs:")
            for name, accs in results.items():
                avg = sum(accs) / len(accs)
                print(f"  {name}: {avg:.2f}%")
        
        # Return averaged results
        return {name: sum(accs) / len(accs) for name, accs in results.items()}
    
    def time_series_cv(
        self,
        csv_path: str = None,
        n_splits: int = 5,
        model_type: str = 'GradientBoosting'
    ) -> dict:
        """
        Perform time-series cross-validation (Phase 4.1).
        
        Args:
            csv_path: Path to classifier CSV
            n_splits: Number of CV splits
            model_type: Classifier to evaluate
            
        Returns:
            Dict with per-fold and average metrics
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available. Run create_training_data first.")
        
        df = pd.read_csv(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        
        results = {'accuracy': [], 'log_loss': [], 'brier': []}
        
        print(f"\nTime-Series Cross-Validation ({n_splits} folds):")
        print("-" * 50)
        
        for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Train model
            model = type(self.CLASSIFIERS[model_type])(**self.CLASSIFIERS[model_type].get_params())
            model.fit(X_train, y_train)
            
            # Evaluate
            preds = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1]
            
            acc = 100 * accuracy_score(y_test, preds)
            ll = log_loss(y_test, proba)
            brier = brier_score_loss(y_test, proba)
            
            results['accuracy'].append(acc)
            results['log_loss'].append(ll)
            results['brier'].append(brier)
            
            print(f"  Fold {fold+1}: Acc={acc:.2f}% | LL={ll:.4f} | Brier={brier:.4f}")
        
        # Compute averages
        avg_acc = np.mean(results['accuracy'])
        avg_ll = np.mean(results['log_loss'])
        avg_brier = np.mean(results['brier'])
        
        print("-" * 50)
        print(f"  Average: Acc={avg_acc:.2f}% | LL={avg_ll:.4f} | Brier={avg_brier:.4f}")
        
        return {
            'folds': results,
            'avg_accuracy': avg_acc,
            'avg_log_loss': avg_ll,
            'avg_brier': avg_brier
        }
    
    def tune_hyperparameters(
        self,
        csv_path: str = None,
        param_grid: dict = None,
        cv: int = 3,
        scoring: str = 'neg_log_loss',
        quick: bool = True
    ) -> dict:
        """
        Tune GradientBoosting hyperparameters (Phase 4.2).
        
        Args:
            csv_path: Path to classifier CSV
            param_grid: Parameter grid (uses default if None)
            cv: Number of CV folds
            scoring: Scoring metric ('accuracy', 'neg_log_loss', etc.)
            quick: If True, use smaller parameter grid
            
        Returns:
            Dict with best params and score
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available. Run create_training_data first.")
        
        df = pd.read_csv(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        # Use smaller grid if quick mode
        if param_grid is None:
            param_grid = self.GBM_PARAM_GRID_SMALL if quick else self.GBM_PARAM_GRID
        
        print(f"\nHyperparameter Tuning (GridSearchCV with {cv} folds)...")
        print(f"Parameter grid: {param_grid}")
        
        base_model = GradientBoostingClassifier(random_state=42)
        
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X, y)
        
        self.best_params = grid_search.best_params_
        
        print(f"\nBest parameters: {self.best_params}")
        print(f"Best score ({scoring}): {grid_search.best_score_:.4f}")
        
        return {
            'best_params': self.best_params,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }
    
    def rate_features(self, csv_path: str = None, top_k: int = None) -> list:
        """
        Rate feature importance using ANOVA F-scores.
        
        Args:
            csv_path: Path to classifier CSV
            top_k: Number of top features to return (all if None)
            
        Returns:
            List of (feature_name, score) tuples sorted by importance
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available. Run create_training_data first.")
        
        # Load data
        df = self._read_csv_safe(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        # Split for feature selection
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        
        # Compute F-scores
        k = top_k or len(feature_cols)
        fs = SelectKBest(score_func=f_classif, k=min(k, len(feature_cols)))
        fs.fit(X_train, y_train)
        
        # Build ranked list
        feature_scores = list(zip(feature_cols, fs.scores_))
        feature_scores.sort(key=lambda x: x[1], reverse=True)
        
        print("\nFeature Importance (F-score):")
        print("-" * 50)
        for name, score in feature_scores[:top_k] if top_k else feature_scores:
            print(f"  {name}: {score:.4f}")
        
        return feature_scores
    
    def get_gbm_feature_importance(self, csv_path: str = None, top_k: int = 20) -> list:
        """
        Get feature importance from trained GradientBoosting model (Phase 5).
        
        Args:
            csv_path: Path to classifier CSV
            top_k: Number of top features to show
            
        Returns:
            List of (feature_name, importance) tuples
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available.")
        
        df = pd.read_csv(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        # Train GBM
        if self.best_params:
            model = GradientBoostingClassifier(**self.best_params, random_state=42)
        else:
            model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        
        model.fit(X, y)
        
        # Get importance
        importances = list(zip(feature_cols, model.feature_importances_))
        importances.sort(key=lambda x: x[1], reverse=True)
        
        print("\nGBM Feature Importance (Gain):")
        print("-" * 50)
        for name, imp in importances[:top_k]:
            print(f"  {name}: {imp:.4f}")
        
        return importances
    
    def train(
        self,
        csv_path: str = None,
        model_type: str = 'LogisticRegression',
        standardize: bool = True,
        calibrate: bool = False,
        use_tuned_params: bool = False
    ):
        """
        Train the classifier model for predictions.
        
        Args:
            csv_path: Path to classifier CSV
            model_type: Name of classifier to use (from CLASSIFIERS)
            standardize: If True, fit a StandardScaler
            calibrate: If True, apply probability calibration (Phase 4.3)
            use_tuned_params: If True and model_type is GradientBoosting, use tuned params
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available. Run create_training_data first.")
        
        # Load data
        df = self._read_csv_safe(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        self.feature_names = feature_cols
        
        # Optionally standardize
        if standardize:
            self.scaler = StandardScaler()
            X = self.scaler.fit_transform(X)
        
        # Select model
        if model_type not in self.CLASSIFIERS:
            raise ValueError(f"Unknown model type: {model_type}. Choose from {list(self.CLASSIFIERS.keys())}")
        
        # Use tuned params for GBM if available
        if model_type == 'GradientBoosting' and use_tuned_params and self.best_params:
            self.classifier_model = GradientBoostingClassifier(**self.best_params, random_state=42)
            print(f"Using tuned parameters: {self.best_params}")
        else:
            self.classifier_model = type(self.CLASSIFIERS[model_type])(
                **self.CLASSIFIERS[model_type].get_params()
            )
        
        # Train classifier
        self.classifier_model.fit(X, y)
        
        print(f"Trained {model_type} on {len(X)} samples with {len(feature_cols)} features")
        
        # Calibrate if requested (Phase 4.3)
        if calibrate:
            print("Calibrating probabilities...")
            # Use time-based split for calibration
            split_idx = int(len(X) * 0.8)
            X_train, X_cal = X[:split_idx], X[split_idx:]
            y_train, y_cal = y[:split_idx], y[split_idx:]
            
            # Retrain on training portion
            self.classifier_model.fit(X_train, y_train)
            
            # Calibrate on held-out portion - use IsotonicRegression directly to avoid cv='prefit' compatibility issues
            from sklearn.calibration import IsotonicRegression
            y_proba_raw_cal = self.classifier_model.predict_proba(X_cal)
            isotonic_calibrator = IsotonicRegression(out_of_bounds='clip')
            isotonic_calibrator.fit(y_proba_raw_cal[:, 1], y_cal)
            
            # Create wrapper class for isotonic calibration that mimics CalibratedClassifierCV interface
            class IsotonicCalibratedModel:
                def __init__(self, base_model, calibrator):
                    self.base_model = base_model
                    self.calibrator = calibrator
                
                def predict(self, X):
                    return self.base_model.predict(X)
                
                def predict_proba(self, X):
                    raw_proba = self.base_model.predict_proba(X)
                    calibrated_1 = self.calibrator.predict(raw_proba[:, 1])
                    # Ensure probabilities sum to 1
                    calibrated_1 = np.clip(calibrated_1, 0.0, 1.0)
                    return np.column_stack([1 - calibrated_1, calibrated_1])
            
            self.calibrated_model = IsotonicCalibratedModel(self.classifier_model, isotonic_calibrator)
            print("Probability calibration complete.")
        
    
    def load_cached_model(self, no_per: bool = False):
        """
        Load and train model from cache file.
        
        Args:
            no_per: If True, load cache without PER features
        """
        import json
        import os
        from bball.training.cache_utils import load_model_cache
        from bball.training.model_factory import create_model_with_c
        
        # Load cache
        cache = load_model_cache(no_per=no_per)
        
        if not cache.get('best'):
            raise ValueError("No cached model found. Please train a model first.")
        
        best_config = cache['best']
        model_type = best_config['model_type']
        c_value = best_config.get('c_value')
        training_csv = cache.get('training_csv')
        
        if not training_csv or not os.path.exists(training_csv):
            raise ValueError(f"Training CSV not found: {training_csv}")
        
        # Set classifier CSV path
        self.classifier_csv = training_csv
        
        # Load data
        df = pd.read_csv(training_csv)
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        self.feature_names = feature_cols
        
        # Standardize
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Create and train model with best config
        self.classifier_model = create_model_with_c(model_type, c_value)
        self.classifier_model.fit(X_scaled, y)
        
        print(f"Loaded and trained {model_type}" + (f" (C={c_value})" if c_value else "") + 
              f" from cache on {len(X)} samples with {len(feature_cols)} features")
    
    
    # =========================================================================
    # PREDICTIONS
    # =========================================================================
    
    def predict(
        self,
        date_str: str = None,
        matchups: list = None,
        season: str = None,
        output_file: bool = True,
        use_calibrated: bool = False,
        excluded_player_ids: Optional[set] = None
    ) -> list:
        """
        Make predictions for games on a given date.
        
        Args:
            date_str: Date in 'YYYY-MM-DD' format (defaults to today)
            matchups: Optional list of [home, away] pairs to predict
            season: NBA season string (e.g., '2024-2025'). Auto-detected if None.
            output_file: If True, write predictions to file
            use_calibrated: If True and calibrated model exists, use it
            excluded_player_ids: Optional set of player IDs to exclude from PER calculations
            
        Returns:
            List of prediction dictionaries
        """
        # Handle ensemble predictions
        if hasattr(self, 'is_ensemble') and self.is_ensemble:
            return self._predict_ensemble(date_str, matchups, season, output_file, excluded_player_ids)
        
        if not self.classifier_model:
            raise ValueError("Model not trained. Run train() first.")
        
        # Use calibrated model if available and requested
        model = self.calibrated_model if (use_calibrated and self.calibrated_model) else self.classifier_model
        
        # Parse date
        if date_str:
            pred_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            pred_date = datetime.now()
        
        year = pred_date.year
        month = pred_date.month
        day = pred_date.day
        
        # Auto-detect season
        if not season:
            season = self._get_season(year, month)
        
        # Ensure league stats are cached for this season
        ensure_season_cached(season, self.db)
        
        # Get matchups from ESPN if not provided
        if not matchups:
            # Lazy import to avoid circular dependency (cli.espn_api -> core -> nba_model -> cli.espn_api)
            from bball.services.espn_sync import get_matchups_with_venue
            print(f"Pulling matchups with venue info for {year}-{month:02d}-{day:02d}...")
            matchups = get_matchups_with_venue(year, month, day)

        if not matchups:
            print("No matchups found for this date.")
            return []

        print(f"Making predictions for {len(matchups)} games...")

        predictions = []

        for game in matchups:
            # Handle both old format (list) and new format (dict with venue_guid)
            if isinstance(game, dict):
                home_team = game.get('home_team', '').upper()
                away_team = game.get('away_team', '').upper()
                venue_guid = game.get('venue_guid')
            else:
                # Legacy format: [home, away]
                if len(game) < 2:
                    continue
                home_team = game[0].upper()
                away_team = game[1].upper()
                venue_guid = None

            if not home_team or not away_team:
                continue

            # Build features dict to match training CSV schema
            features_dict = self._build_features_dict(
                home_team, away_team, season, year, month, day,
                player_filters=None, target_venue_guid=venue_guid
            )
            if features_dict is None:
                print(f"  Skipping {away_team} @ {home_team} (insufficient data)")
                continue
            
            # Check for missing features that are expected
            if hasattr(self, 'feature_names') and self.feature_names:
                missing_features = [fname for fname in self.feature_names if fname not in features_dict]
                if missing_features:
                    print(f"  WARNING: Missing {len(missing_features)} expected features for {away_team} @ {home_team}")
                    print(f"    Missing: {missing_features[:10]}{'...' if len(missing_features) > 10 else ''}")
            
            # Align feature vector to training CSV column order
            features = [features_dict.get(fname, 0.0) for fname in self.feature_names]
            
            # Check for all-zero features which would indicate a problem
            non_zero_count = sum(1 for f in features if abs(f) > 1e-10)
            if non_zero_count == 0:
                print(f"  ERROR: All features are zero for {away_team} @ {home_team} - skipping prediction")
                continue
            
            # Check for features with extreme values that might indicate an issue
            extreme_values = [i for i, f in enumerate(features) if abs(f) > 1000]
            if extreme_values and len(extreme_values) > len(features) * 0.1:
                print(f"  WARNING: {len(extreme_values)} features have extreme values (>1000) for {away_team} @ {home_team}")
                print(f"    Feature names: {[self.feature_names[i] for i in extreme_values[:5]]}")
                print(f"    Values: {[features[i] for i in extreme_values[:5]]}")
            
            # Scale features if scaler exists
            X = np.array(features).reshape(1, -1)
            if self.scaler:
                X = self.scaler.transform(X)
            
            # Make prediction
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]
            
            # proba[0] = P(away wins), proba[1] = P(home wins)
            home_win_prob = proba[1]
            home_win_prob = max(0.01, min(home_win_prob, 0.99))  # Cap between 1% and 99%
            
            # Predict points if model available
            home_pts, away_pts = None, None
            if self.points_model and self._points_computer:
                pts_data = self._points_computer.getStatAvgDiffs(
                    home_team, away_team, season,
                    year=year, month=month, day=day,
                    point_regression=True
                )
                if pts_data != 'SOME BS':
                    home_pts = int(round(self.points_model.predict([pts_data[0]])[0]))
                    away_pts = int(round(self.points_model.predict([pts_data[1]])[0]))
            
            # Calculate American odds for the predicted winner
            if pred == 1:  # Home team predicted to win
                winner = home_team
                winner_prob = home_win_prob
            else:  # Away team predicted to win
                winner = away_team
                winner_prob = 1 - home_win_prob
            
            # Convert probability to American odds
            if winner_prob >= 0.5:
                odds = int(-100 * winner_prob / (1 - winner_prob))
            else:
                odds = int(100 * (1 - winner_prob) / winner_prob)
            
            # Include reliability info using features_dict if available
            games_played_info = ""
            home_gp_feature = 'games_played|season|avg|home'
            away_gp_feature = 'games_played|season|avg|away'
            if home_gp_feature in features_dict and away_gp_feature in features_dict:
                home_gp = features_dict[home_gp_feature]
                away_gp = features_dict[away_gp_feature]
                if home_gp is not None and away_gp is not None:
                    games_played_info = f" [GP: {int(home_gp)}/{int(away_gp)}]"
            
            prediction = {
                'home': home_team,
                'away': away_team,
                'predicted_winner': winner,
                'home_win_prob': round(100 * home_win_prob, 1),
                'home_pts': home_pts,
                'away_pts': away_pts,
                'odds': odds,
                'home_games_played': home_gp if home_gp is not None else None,
                'away_games_played': away_gp if away_gp is not None else None,
            }
            predictions.append(prediction)
            
            # Format output
            winner_marker = '*' if winner == home_team else ''
            away_marker = '*' if winner == away_team else ''
            
            print(f"  {away_team}{away_marker} @ {home_team}{winner_marker} - {prediction['home_win_prob']}% ({odds}){games_played_info}")
        
        # Write to file
        if output_file and predictions:
            folder = os.path.join(self.output_dir, f"{year}-{month}-{day}")
            os.makedirs(folder, exist_ok=True)
            
            filepath = os.path.join(folder, 'predictions.txt')
            with open(filepath, 'w') as f:
                for p in predictions:
                    if p['home_pts'] and p['away_pts']:
                        line = f"{p['away']}({p['away_pts']}) @ {p['home']}({p['home_pts']})"
                    else:
                        line = f"{p['away']} @ {p['home']}"
                    
                    winner = '*' if p['predicted_winner'] == p['home'] else ''
                    away_winner = '*' if p['predicted_winner'] == p['away'] else ''
                    
                    f.write(f"{p['away']}{away_winner} @ {p['home']}{winner} - {p['home_win_prob']}% ({p['odds']})\n")
            
            print(f"\nPredictions saved to: {filepath}")
        
        return predictions
    
    def _predict_ensemble(
        self,
        date_str: str = None,
        matchups: list = None,
        season: str = None,
        output_file: bool = True,
        excluded_player_ids: Optional[set] = None
    ) -> list:
        """
        Make predictions using ensemble model.
        
        Args:
            date_str: Date in 'YYYY-MM-DD' format (defaults to today)
            matchups: Optional list of [home, away] pairs to predict
            season: NBA season string (e.g., '2024-2025'). Auto-detected if None.
            output_file: If True, write predictions to file
            excluded_player_ids: Optional set of player IDs to exclude from PER calculations
            
        Returns:
            List of prediction dictionaries
        """
        if not hasattr(self, 'ensemble_result') or not self.ensemble_result:
            raise ValueError("Ensemble model not properly trained")
        
        # Parse date
        if date_str:
            pred_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            pred_date = datetime.now()
        
        year = pred_date.year
        month = pred_date.month
        day = pred_date.day
        
        # Auto-detect season
        if not season:
            season = self._get_season(year, month)
        
        # Get matchups from ESPN if not provided
        if not matchups:
            print(f"Pulling matchups for {year}-{month:02d}-{day:02d}...")
            matchups = pull_matchups(year, month, day)
        
        if not matchups:
            print("No matchups found for this date")
            return []
        
        predictions = []
        print(f"Making ensemble predictions for {len(matchups)} games...")
        
        # Get ensemble meta-model and base models from stored result
        ensemble_run_id = self.ensemble_run_id
        ensemble_meta_features = self.ensemble_meta_features
        
        # Load stacking trainer to get meta-model
        from bball.training.run_tracker import RunTracker
        from bball.training.stacking_trainer import StackingTrainer
        
        run_tracker = RunTracker(db=self.db)
        stacking_trainer = StackingTrainer(db=self.db)
        
        # Get the trained stacking result
        stacking_run = run_tracker.get_run(ensemble_run_id)
        if not stacking_run:
            raise ValueError(f"Ensemble run {ensemble_run_id} not found")
        
        # Load base models and meta-model
        base_models_info = stacking_trainer._load_base_models(self.ensemble_base_models)
        meta_model = stacking_trainer._train_meta_model(
            stacking_df=pd.DataFrame(),  # We'll load this from calibration data
            meta_c_value=0.1
        )
        
        # Load the actual trained meta-model from the run
        # For now, we'll need to reconstruct the meta-model from the run data
        # This is a simplified version - in production, we'd load the saved model
        
        for matchup in matchups:
            home_team, away_team = matchup
            
            # Get game data for features
            game_doc = self._games_repo.find_one({
                'homeTeam.name': home_team,
                'awayTeam.name': away_team,
                'date': f"{year}-{month:02d}-{day:02d}"
            })
            
            if not game_doc:
                print(f"Warning: No game data found for {away_team} @ {home_team}")
                continue
            
            # Build features dict for ensemble prediction
            # We need predictions from all base models + meta features
            base_predictions = []
            
            # Get predictions from each base model
            for model_info in base_models_info:
                try:
                    # This is simplified - in production, we'd use the actual loaded models
                    # For now, we'll use the stacking tool's prediction logic
                    base_model = model_info['model']
                    scaler = model_info['scaler']
                    feature_names = model_info['feature_names']
                    
                    # Build features for this base model
                    features_dict = self._build_features_dict(
                        home_team, away_team, season, year, month, day, excluded_player_ids
                    )
                    
                    if not features_dict:
                        continue
                    
                    # Extract features in the right order
                    X = np.zeros((1, len(feature_names)))
                    for i, feat_name in enumerate(feature_names):
                        if feat_name in features_dict:
                            X[0, i] = features_dict[feat_name]
                        else:
                            X[0, i] = 0.0  # Default for missing features
                    
                    # Scale features
                    if scaler:
                        X = scaler.transform(X)
                    
                    # Get prediction
                    y_proba = base_model.predict_proba(X)
                    base_predictions.append(y_proba[0, 1])  # Probability of home win
                    
                except Exception as e:
                    print(f"Warning: Failed to get prediction from base model: {e}")
                    base_predictions.append(0.5)  # Default to 50% if failed
            
            # Get meta features (like pred_margin)
            meta_features_values = []
            for meta_feat in ensemble_meta_features:
                if meta_feat == 'pred_margin':
                    # Get pred_margin from selected points model
                    try:
                        selected_points_config = self._points_config_repo.get_selected_config()
                        if selected_points_config:
                            from bball.models.points_regression import PointsRegressionTrainer
                            points_trainer = PointsRegressionTrainer(db=self.db)
                            model_path = selected_points_config.get('model_path')
                            if model_path and os.path.exists(model_path):
                                model_name = os.path.basename(model_path).replace('.pkl', '')
                                points_trainer.load_model(model_name)
                                
                                # Create game dict for points prediction
                                game_dict = {
                                    'game_id': game_doc.get('game_id', ''),
                                    'date': f"{year}-{month:02d}-{day:02d}",
                                    'year': year,
                                    'month': month,
                                    'day': day,
                                    'season': season,
                                    'homeTeam': {'name': home_team},
                                    'awayTeam': {'name': away_team}
                                }
                                
                                points_pred = points_trainer.predict(game_dict, f"{year}-{month:02d}-{day:02d}")
                                
                                # Extract predicted margin
                                if 'point_diff_pred' in points_pred:
                                    pred_margin = points_pred['point_diff_pred']
                                elif 'home_points' in points_pred and 'away_points' in points_pred:
                                    pred_margin = points_pred['home_points'] - points_pred['away_points']
                                else:
                                    pred_margin = 0.0
                                
                                meta_features_values.append(pred_margin)
                            else:
                                meta_features_values.append(0.0)
                        else:
                            meta_features_values.append(0.0)
                    except Exception as e:
                        print(f"Warning: Failed to get pred_margin: {e}")
                        meta_features_values.append(0.0)
                else:
                    # For other meta features, try to get from features_dict
                    features_dict = self._build_features_dict(
                        home_team, away_team, season, year, month, day, excluded_player_ids
                    )
                    meta_features_values.append(features_dict.get(meta_feat, 0.0))
            
            # Combine base predictions and meta features for meta-model
            ensemble_features = base_predictions + meta_features_values
            X_ensemble = np.array([ensemble_features])
            
            # Get meta-model prediction
            try:
                # Use the trained meta-model from ensemble result
                # This is simplified - would normally load the saved model
                home_win_prob = meta_model.predict_proba(X_ensemble)[0, 1]
                winner = home_team if home_win_prob >= 0.5 else away_team
            except Exception as e:
                print(f"Warning: Failed to get ensemble prediction: {e}")
                home_win_prob = 0.5
                winner = home_team  # Default
            
            # Calculate odds
            if home_win_prob >= 0.5:
                odds = int(-100 * home_win_prob / (1 - home_win_prob))
            else:
                odds = int(100 * (1 - home_win_prob) / home_win_prob)
            
            prediction = {
                'home': home_team,
                'away': away_team,
                'predicted_winner': winner,
                'home_win_prob': round(100 * home_win_prob, 1),
                'odds': odds,
                'ensemble_base_predictions': base_predictions,  # For debugging
                'ensemble_meta_features': dict(zip(ensemble_meta_features, meta_features_values))  # For debugging
            }
            
            predictions.append(prediction)
            
            # Format output
            winner_marker = '*' if winner == home_team else ''
            away_marker = '*' if winner == away_team else ''
            
            base_preds_str = ', '.join([f"{p:.1%}" for p in base_predictions])
            meta_feats_str = ', '.join([f"{k}:{v:.1f}" for k, v in zip(ensemble_meta_features, meta_features_values)])
            
            print(f"  {away_team}{away_marker} @ {home_team}{winner_marker} - {prediction['home_win_prob']}% ({odds}) [Base: {base_preds_str}] [Meta: {meta_feats_str}]")
        
        # Write to file
        if output_file and predictions:
            folder = os.path.join(self.output_dir, f"{year}-{month}-{day}")
            os.makedirs(folder, exist_ok=True)
            
            filepath = os.path.join(folder, 'predictions.txt')
            with open(filepath, 'w') as f:
                for p in predictions:
                    line = f"{p['away']} @ {p['home']}"
                    winner = '*' if p['predicted_winner'] == p['home'] else ''
                    away_winner = '*' if p['predicted_winner'] == p['away'] else ''
                    f.write(f"{p['away']}{away_winner} @ {p['home']}{winner} - {p['home_win_prob']}% ({p['odds']})\n")
            
            print(f"\nPredictions saved to: {filepath}")
        
        return predictions
    
    def _build_features_dict(self, home_team: str, away_team: str, season: str,
                             year: int, month: int, day: int,
                             player_filters: Dict = None,
                             target_venue_guid: str = None,
                             game_doc: Dict = None) -> dict:
        """
        Build features as a dictionary, matching the structure used in training CSV.
        Returns a dict with feature names as keys.

        NEW ARCHITECTURE: Calculates features directly from their names using calculate_feature().
        No stat tokens, no mapping, no index tracking - just direct calculation.

        Args:
            home_team, away_team: Team names
            season: NBA season string
            year, month, day: Game date
            player_filters: Optional player filters for PER features
            target_venue_guid: Venue GUID of the target game (for travel features)
            game_doc: Optional pre-loaded game document (avoids DB query for injured players)
        """
        features_dict = {}

        # Known special features that are NOT pipe-delimited but are valid
        VALID_SPECIAL_FEATURES = {
            'pred_margin',  # From points prediction model
            'SeasonStartYear', 'Year', 'Month', 'Day',  # Temporal metadata
        }

        # Validate that features use pipe-delimited format (or are known special features)
        if hasattr(self, 'feature_names') and self.feature_names:
            non_pipe_features = [f for f in self.feature_names if '|' not in f]
            unknown_non_pipe = [f for f in non_pipe_features if f not in VALID_SPECIAL_FEATURES]
            if unknown_non_pipe and not any('|' in fname for fname in self.feature_names):
                import logging
                logging.error(f"_build_features_dict: Invalid features detected: {unknown_non_pipe[:5]}")
                raise ValueError(f"Invalid feature names: {unknown_non_pipe[:3]}. Features must use pipe-delimited format (e.g., 'points|season|avg|diff').")

        # Calculate each feature directly from its name
        if not hasattr(self, 'feature_names') or not self.feature_names:
            import logging
            logging.warning(f"_build_features_dict: feature_names is empty for {away_team} @ {home_team}")
            return None
        
        # DEBUG: Log feature calculation for first call
        if not hasattr(self, '_debug_features_logged'):
            import logging
            logging.info(f"[DEBUG] _build_features_dict: Calculating {len(self.feature_names)} features for {away_team} @ {home_team}")
            logging.info(f"[DEBUG] First 10 feature_names: {self.feature_names[:10]}")
            self._debug_features_logged = True
        
        # Categorize features
        regular_features = []
        game_date_str = f"{year}-{month:02d}-{day:02d}"
        for feature_name in self.feature_names:
            if '|' not in feature_name:
                # Special non-pipe features (metadata, computed values)
                if feature_name == 'SeasonStartYear':
                    features_dict[feature_name] = int(year) if int(month) >= 10 else int(year) - 1
                elif feature_name == 'Year':
                    features_dict[feature_name] = int(year)
                elif feature_name == 'Month':
                    features_dict[feature_name] = int(month)
                elif feature_name == 'Day':
                    features_dict[feature_name] = int(day)
                elif feature_name == 'pred_margin':
                    features_dict[feature_name] = 0.0
                else:
                    features_dict[feature_name] = 0.0
            elif feature_name.startswith('player_') or feature_name.startswith('per_available'):
                pass  # PER features - handled separately below
            elif feature_name.startswith('inj_'):
                pass  # Injury features - handled separately below
            else:
                regular_features.append(feature_name)

        # Batch compute regular features via BasketballFeatureComputer
        if regular_features:
            regular_results = self._computer.compute_matchup_features(
                regular_features, home_team, away_team, season,
                game_date_str, venue_guid=target_venue_guid,
            )
            features_dict.update(regular_results)
        
        # Add PER features - calculate if ANY PER features are in feature_names (regardless of include_per_features flag)
        # The flag should only control training, not prediction-time calculation
        has_per_features = any(fname.startswith('player_') or fname.startswith('per_available') for fname in self.feature_names)
        if has_per_features and self.per_calculator:
            game_date_str = f"{year}-{month:02d}-{day:02d}"
            
            # Extract injured players based on context (training vs prediction)
            injured_players_dict = None
            # Use passed game_doc if available (training mode - avoids DB query)
            # Only query DB if game_doc not passed (prediction mode)
            if game_doc is None:
                try:
                    game_doc = self._games_repo.find_one({
                        'homeTeam.name': home_team,
                        'awayTeam.name': away_team,
                        'season': season,
                        'date': game_date_str
                    })
                except:
                    pass

            if game_doc:
                # Training mode: Use stats_nba.{home/away}Team.injured_players
                home_injured = game_doc.get('homeTeam', {}).get('injured_players', [])
                away_injured = game_doc.get('awayTeam', {}).get('injured_players', [])
                if home_injured or away_injured:
                    injured_players_dict = {
                        home_team: [str(pid) for pid in home_injured] if home_injured else [],
                        away_team: [str(pid) for pid in away_injured] if away_injured else []
                    }
            elif player_filters:
                # Prediction mode: Use injured list from player_filters (already sourced from rosters)
                injured_players_dict = {
                    team: player_filters.get(team, {}).get('injured', [])
                    for team in [home_team, away_team]
                }
            
            per_features = self._get_per_features(
                home_team, away_team, season, game_date_str, 
                player_filters=player_filters,
                injured_players=injured_players_dict
            )
            if per_features:
                # PER features are now returned  directly from PERCalculator
                # Copy all PER features that are in feature_names
                for feature_name in self.feature_names:
                    if feature_name.startswith('player_') or feature_name.startswith('per_available'):
                        if feature_name in per_features:
                            features_dict[feature_name] = per_features[feature_name]
                        else:
                            # Feature expected but not in per_features - set to 0
                            if feature_name not in features_dict:
                                features_dict[feature_name] = 0.0
                
                # Extract player lists from PER features (for display in feature modal)
                # Store in a special key that will be saved separately
                if '_player_lists' in per_features:
                    if not hasattr(self, '_per_player_lists'):
                        self._per_player_lists = {}
                    self._per_player_lists.update(per_features['_player_lists'])
                
                # Handle per_available flag
                per_available_feature = 'per_available|season|none|none'
                if per_available_feature in self.feature_names:
                    features_dict[per_available_feature] = 1 if per_features else 0
            else:
                # PER features expected but calculation failed - set all to 0
                for feature_name in self.feature_names:
                    if feature_name.startswith('player_') or feature_name.startswith('per_available'):
                        if feature_name not in features_dict:
                            features_dict[feature_name] = 0.0
        
        # Enhanced features are now calculated via calculate_feature() above
        # No need for separate handling
        
        # Add injury features - calculate if ANY injury features are in feature_names (regardless of include_injuries flag)
        # The flag should only control training, not prediction-time calculation
        has_injury_features = any(fname.startswith('inj_') for fname in self.feature_names)
        if has_injury_features:
            # Use passed game_doc if available (training mode), otherwise query DB (prediction mode)
            injury_game_doc = game_doc
            if injury_game_doc is None:
                game_date_str = f"{year}-{month:02d}-{day:02d}"
                try:
                    injury_game_doc = self._games_repo.find_one({
                        'homeTeam.name': home_team,
                        'awayTeam.name': away_team,
                        'season': season,
                        'date': game_date_str
                    })
                except:
                    pass

            if not hasattr(self, '_injury_calculator'):
                from bball.features.injury import InjuryFeatureCalculator
                self._injury_calculator = InjuryFeatureCalculator(db=self.db, league=self.league)
                if self._computer.games_home is not None:
                    self._injury_calculator.set_preloaded_data(
                        self._computer.games_home, self._computer.games_away,
                    )
            injury_features = self._injury_calculator.get_injury_features(
                home_team, away_team, season, year, month, day,
                game_doc=injury_game_doc,
                per_calculator=self.per_calculator,
                recency_decay_k=getattr(self, 'recency_decay_k', 15.0),
            )
            if injury_features:
                # Copy all injury features that are in feature_names
                for feature_name in self.feature_names:
                    if feature_name.startswith('inj_'):
                        if feature_name in injury_features:
                            features_dict[feature_name] = injury_features[feature_name]
                        else:
                            # Feature expected but not in injury_features - set to 0
                            if feature_name not in features_dict:
                                features_dict[feature_name] = 0.0
                
                # Extract player lists from injury features (for display in feature modal)
                # Store in a special key that will be saved separately
                if '_player_lists' in injury_features:
                    if not hasattr(self, '_injury_player_lists'):
                        self._injury_player_lists = {}
                    self._injury_player_lists.update(injury_features['_player_lists'])
            else:
                # Injury features expected but calculation failed - set all to 0
                for feature_name in self.feature_names:
                    if feature_name.startswith('inj_'):
                        if feature_name not in features_dict:
                            features_dict[feature_name] = 0.0
        
        # Note: pred_* features and some other features may be added later via additional_features parameter
        # So missing features warning is logged here, but they may be filled in by the caller
        
        return features_dict

    def predict_with_player_config(
        self,
        home_team: str,
        away_team: str,
        season: str,
        game_date: str,
        player_filters: Dict,
        use_calibrated: bool = False,
        additional_features: Dict = None,
        venue_guid: str = None
    ) -> dict:
        """
        Make a prediction for a single game with player availability configuration.

        Args:
            home_team: Home team name
            away_team: Away team name
            season: Season string (e.g., '2024-2025')
            game_date: Game date string (YYYY-MM-DD)
            player_filters: REQUIRED dict with team names as keys:
                {team: {'playing': [player_ids], 'starters': [player_ids]}}
                Both teams must have 'playing' lists. 'starters' is optional.
            use_calibrated: If True and calibrated model exists, use it
            additional_features: Optional dict of additional features to merge into features_dict
                (e.g., {'pred_margin': 5.2} from point prediction models). These features must
                be in the model's feature_names list for them to be included in the prediction.
            venue_guid: Optional venue GUID for travel feature calculations
            
        Returns:
            Dict with prediction results
            
        Raises:
            ValueError: If player_filters is missing or incomplete
        """
        # Ensemble support (web game_detail workflow).
        # Ensemble models do not populate self.classifier_model; they use a stacked meta-model over base models.
        if hasattr(self, 'is_ensemble') and self.is_ensemble:
            return self._predict_ensemble_with_player_config(
                home_team=home_team,
                away_team=away_team,
                season=season,
                game_date=game_date,
                player_filters=player_filters,
                additional_features=additional_features,
                venue_guid=venue_guid
            )

        if not self.classifier_model:
            raise ValueError("Model not trained. Run train() first.")
        
        if not self.feature_names:
            raise ValueError("Feature names not loaded. Model may not have been loaded from cache correctly.")
        
        # Phase 1.2: Require player_filters for realistic predictions
        if not player_filters:
            raise ValueError(
                "player_filters is required for prediction with PER features. "
                "Provide explicit player availability to match training behavior."
            )
        
        # Validate that both teams have 'playing' lists
        if home_team not in player_filters or 'playing' not in player_filters[home_team]:
            raise ValueError(f"player_filters must include '{home_team}' with 'playing' list")
        if away_team not in player_filters or 'playing' not in player_filters[away_team]:
            raise ValueError(f"player_filters must include '{away_team}' with 'playing' list")
        
        # Use calibrated model if available and requested
        model = self.calibrated_model if (use_calibrated and self.calibrated_model) else self.classifier_model
        
        # Parse date
        pred_date = datetime.strptime(game_date, '%Y-%m-%d')
        year = pred_date.year
        month = pred_date.month
        day = pred_date.day
        
        # Build features as dict
        features_dict = self._build_features_dict(
            home_team, away_team, season, year, month, day, player_filters,
            target_venue_guid=venue_guid
        )
        
        if features_dict is None:
            raise ValueError(f"Insufficient data for {away_team} @ {home_team}")
        
        # Merge additional features if provided (e.g., pred_margin from point prediction model)
        # This should be done BEFORE checking for missing features to avoid false warnings
        if additional_features:
            features_dict.update(additional_features)
        
        # Ensure all features in feature_names are present (set missing to 0.0)
        # This handles cases where features couldn't be calculated
        for feature_name in self.feature_names:
            if feature_name not in features_dict:
                features_dict[feature_name] = 0.0
        
        # Order features according to training CSV feature order
        features = [features_dict.get(fname, 0.0) for fname in self.feature_names]
        
        # Scale features if scaler exists
        X = np.array(features).reshape(1, -1)
        if self.scaler:
            X = self.scaler.transform(X)
        
        # Make prediction
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        
        # proba[0] = P(away wins), proba[1] = P(home wins)
        home_win_prob = proba[1]
        home_win_prob = max(0.01, min(home_win_prob, 0.99))  # Cap between 1% and 99%
        
        # Predict points if model available
        home_pts, away_pts = None, None
        if self.points_model and self._points_computer:
            pts_data = self._points_computer.getStatAvgDiffs(
                home_team, away_team, season,
                year=year, month=month, day=day,
                point_regression=True
            )
            if pts_data != 'SOME BS':
                home_pts = int(round(self.points_model.predict([pts_data[0]])[0]))
                away_pts = int(round(self.points_model.predict([pts_data[1]])[0]))
        
        # Calculate American odds for the predicted winner
        if pred == 1:  # Home team predicted to win
            winner = home_team
            winner_prob = home_win_prob
        else:  # Away team predicted to win
            winner = away_team
            winner_prob = 1 - home_win_prob
        
        # Convert probability to American odds
        if winner_prob >= 0.5:
            odds = int(-100 * winner_prob / (1 - winner_prob))
        else:
            odds = int(100 * (1 - winner_prob) / winner_prob)
        
        # Get games played from features_dict 
        home_gp = None
        away_gp = None
        if hasattr(self, 'feature_names') and self.feature_names:
            home_gp_feature = 'games_played|season|avg|home'
            away_gp_feature = 'games_played|season|avg|away'
            if home_gp_feature in features_dict:
                home_gp = int(features_dict[home_gp_feature])
            if away_gp_feature in features_dict:
                away_gp = int(features_dict[away_gp_feature])
        
        return {
            'predicted_winner': winner,
            'home_win_prob': round(100 * home_win_prob, 1),
            'home_pts': home_pts,
            'away_pts': away_pts,
            'odds': odds,
            'home_games_played': home_gp,
            'away_games_played': away_gp,
            'features_dict': features_dict  # Include features dict for display/storage
        }

    def _predict_ensemble_with_player_config(
        self,
        home_team: str,
        away_team: str,
        season: str,
        game_date: str,
        player_filters: Dict,
        additional_features: Optional[Dict] = None,
        venue_guid: str = None
    ) -> dict:
        """
        Predict a single game using a trained stacking ensemble while respecting player availability.

        Uses the optimized EnsemblePredictor which:
        - Generates features ONCE for all base models (shared feature generator)
        - Uses in-memory cached sklearn models (ArtifactLoader cache)
        - Minimizes redundant DB queries and computation

        Returns a prediction dict matching the API contract.
        """
        from bball.models.ensemble import EnsemblePredictor

        # Use cached EnsemblePredictor if available, otherwise create one
        if not hasattr(self, '_ensemble_predictor') or self._ensemble_predictor is None:
            ensemble_config = getattr(self, 'ensemble_config', None) or {}
            self._ensemble_predictor = EnsemblePredictor(self.db, ensemble_config, league=self.league)
            # Inject prediction context if available (for preloaded data)
            if hasattr(self, '_prediction_context') and self._prediction_context:
                self._ensemble_predictor.set_prediction_context(self._prediction_context)

        # Make prediction using optimized path
        result = self._ensemble_predictor.predict(
            home_team=home_team,
            away_team=away_team,
            season=season,
            game_date=game_date,
            player_filters=player_filters,
            additional_features=additional_features,
            venue_guid=venue_guid
        )

        # Copy player lists for UI display
        player_lists = self._ensemble_predictor.get_player_lists()
        if player_lists:
            if not hasattr(self, '_per_player_lists'):
                self._per_player_lists = {}
            if not hasattr(self, '_injury_player_lists'):
                self._injury_player_lists = {}
            for k, v in player_lists.items():
                if k.startswith('inj_'):
                    self._injury_player_lists[k] = v
                else:
                    self._per_player_lists[k] = v

        return result

    def _get_season(self, year: int, month: int) -> str:
        """Determine NBA season string from date."""
        if month >= 10:  # Oct-Dec = first year of season
            return f"{year}-{year + 1}"
        else:  # Jan-Jun = second year of season
            return f"{year - 1}-{year}"
    
    # =========================================================================
    # MONITORING & BACKTESTING (Phase 5)
    # =========================================================================
    
    def backtest_by_season(self, csv_path: str = None, model_type: str = 'GradientBoosting') -> dict:
        """
        Backtest model performance by season (Phase 5).
        
        Args:
            csv_path: Path to classifier CSV
            model_type: Classifier to use
            
        Returns:
            Dict with per-season metrics
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available.")
        
        df = pd.read_csv(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        # Create season column
        df['Season'] = df.apply(
            lambda r: f"{r['Year']}-{r['Year']+1}" if r['Month'] >= 10 else f"{r['Year']-1}-{r['Year']}", 
            axis=1
        )
        
        seasons = sorted(df['Season'].unique())
        results = {}
        
        print("\nBacktest by Season:")
        print("-" * 60)
        
        for i, test_season in enumerate(seasons[1:], 1):  # Skip first season (need training data)
            train_seasons = seasons[:i]
            
            train_mask = df['Season'].isin(train_seasons)
            test_mask = df['Season'] == test_season
            
            X_train = df.loc[train_mask, feature_cols].values
            y_train = df.loc[train_mask, target_col].values
            X_test = df.loc[test_mask, feature_cols].values
            y_test = df.loc[test_mask, target_col].values
            
            if len(X_test) == 0:
                continue
            
            # Train and evaluate
            model = type(self.CLASSIFIERS[model_type])(**self.CLASSIFIERS[model_type].get_params())
            model.fit(X_train, y_train)
            
            preds = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1]
            
            acc = 100 * accuracy_score(y_test, preds)
            ll = log_loss(y_test, proba)
            brier = brier_score_loss(y_test, proba)
            
            results[test_season] = {
                'accuracy': acc,
                'log_loss': ll,
                'brier': brier,
                'n_games': len(y_test)
            }
            
            print(f"  {test_season}: Acc={acc:.2f}% | LL={ll:.4f} | Brier={brier:.4f} | n={len(y_test)}")
        
        # Compute overall average
        avg_acc = np.mean([r['accuracy'] for r in results.values()])
        avg_ll = np.mean([r['log_loss'] for r in results.values()])
        avg_brier = np.mean([r['brier'] for r in results.values()])
        
        print("-" * 60)
        print(f"  Average: Acc={avg_acc:.2f}% | LL={avg_ll:.4f} | Brier={avg_brier:.4f}")
        
        return results
    
    def early_vs_late_season_analysis(self, csv_path: str = None, 
                                       games_threshold: int = 20,
                                       model_type: str = 'GradientBoosting') -> dict:
        """
        Compare model performance on early-season vs mid/late-season games (Phase 5).
        
        Args:
            csv_path: Path to classifier CSV
            games_threshold: Number of games to define "early season"
            model_type: Classifier to use
            
        Returns:
            Dict with early vs late season metrics
        """
        csv_path = csv_path or self.classifier_csv
        if not csv_path:
            raise ValueError("No training data available.")
        
        df = pd.read_csv(csv_path)
        
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        # Need games_played feature 
        games_played_home_col = 'games_played|season|avg|home'
        games_played_away_col = 'games_played|season|avg|away'
        if games_played_home_col not in df.columns or games_played_away_col not in df.columns:
            print("Warning: games_played features not in dataset. Enhanced features should always be included.")
            return {}
        
        # Split by games played
        early_mask = (df[games_played_home_col] < games_threshold) | (df[games_played_away_col] < games_threshold)
        late_mask = ~early_mask
        
        # Time-based split for train/test
        split_idx = int(len(df) * 0.8)
        
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        
        X_train = train_df[feature_cols].values
        y_train = train_df[target_col].values
        
        # Train model
        model = type(self.CLASSIFIERS[model_type])(**self.CLASSIFIERS[model_type].get_params())
        model.fit(X_train, y_train)
        
        results = {}
        
        print(f"\nEarly vs Late Season Analysis (threshold: {games_threshold} games):")
        print("-" * 60)
        
        for name, mask in [('Early', early_mask), ('Late', late_mask)]:
            test_subset = test_df[mask.iloc[split_idx:].values]
            
            if len(test_subset) == 0:
                continue
            
            X_test = test_subset[feature_cols].values
            y_test = test_subset[target_col].values
            
            preds = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1]
            
            acc = 100 * accuracy_score(y_test, preds)
            ll = log_loss(y_test, proba)
            brier = brier_score_loss(y_test, proba)
            
            results[name] = {
                'accuracy': acc,
                'log_loss': ll,
                'brier': brier,
                'n_games': len(y_test)
            }
            
            print(f"  {name} Season: Acc={acc:.2f}% | LL={ll:.4f} | Brier={brier:.4f} | n={len(y_test)}")
        
        return results


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    print("BballModel example usage:")
    print("  features = ['points|season|avg|diff', 'off_rtg|games_10|avg|diff']")
    print("  model = BballModel(classifier_features=features, points_features=features)")
    print("  # For CBB: model = BballModel(features, league=load_league_config('cbb'))")

