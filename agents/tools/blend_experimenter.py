"""
Blend Feature Experimenter Tool - Experiment with different blend feature weights
"""

import sys
import os
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.core.mongo import Mongo
from nba_app.core.models.bball_model import BballModel
from nba_app.core.data import GamesRepository
from nba_app.core.training.model_factory import create_model_with_c
from nba_app.core.training.cache_utils import read_csv_safe


class BlendExperimenter:
    """Experiments with different blend feature weight configurations"""
    
    def __init__(self, db=None):
        """
        Initialize BlendExperimenter.
        
        Args:
            db: MongoDB database instance (optional)
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db

        # Initialize repository
        self._games_repo = GamesRepository(self.db)

        # Cache directory for blend variant CSVs
        self.cache_dir = os.path.join(parent_dir, 'model_output', 'blend_experiments')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def experiment_blend_weights(
        self,
        blend_feature_name: str,
        weight_configs: List[Dict],
        time_period: Optional[Dict] = None,
        base_features: Optional[List[str]] = None,
        model_type: str = "LogisticRegression",
        min_games_played: int = 15
    ) -> Dict:
        """
        Experiment with different blend feature weight configurations.
        
        Args:
            blend_feature_name: Base name (e.g., "wins", "points_net", "off_rtg_net", "efg_net") or full name with "_blend" suffix (e.g., "wins_blend")
            weight_configs: List of blend component configurations. Each config is a dict with 'blend_components' key.
                Each component in 'blend_components' has 'time_period' (e.g., 'season', 'games_10', 'games_12', 'games_20')
                and 'weight' (float). Weights must sum to 1.0.
                Example: [{'blend_components': [{'time_period': 'season', 'weight': 0.6},
                                                 {'time_period': 'games_20', 'weight': 0.3},
                                                 {'time_period': 'games_10', 'weight': 0.1}]}]
            time_period: Dict with begin_year/end_year or begin_date/end_date (defaults to last 2 full seasons)
            base_features: List of other features to include from master CSV (optional, defaults to empty)
            model_type: Model type for lightweight experiment (default: "LogisticRegression")
            min_games_played: Minimum games filter (default: 15)
            
        Returns:
            Dict with:
                - comparison_table: List of dicts with weight config, importance score, and metrics
                - variant_csv_paths: Dict mapping weight config strings to CSV paths
                - summary: Best weight configuration
        """
        # Normalize blend feature name (accept both 'wins' and 'wins_blend')
        if blend_feature_name.endswith('_blend'):
            base_feature_name = blend_feature_name[:-6]  # Remove '_blend' suffix
        else:
            base_feature_name = blend_feature_name
        
        # Validate blend feature name
        valid_blends = ['wins', 'points_net', 'off_rtg_net', 'efg_net']
        if base_feature_name not in valid_blends:
            raise ValueError(
                f"Invalid blend_feature_name: {blend_feature_name}. "
                f"Must be one of {valid_blends} (or with '_blend' suffix: {[b + '_blend' for b in valid_blends]})"
            )
        
        # Use the base feature name for the rest of the function
        blend_feature_name = base_feature_name
        
        # Validate and normalize weight configs
        validated_weight_configs = []
        for wc in weight_configs:
            if 'blend_components' in wc:
                # Multiple time periods with weights
                components = wc['blend_components']
                if not isinstance(components, list) or len(components) == 0:
                    raise ValueError(f"blend_components must be a non-empty list: {wc}")
                
                validated_components = []
                total_weight = 0.0
                for comp in components:
                    if not isinstance(comp, dict) or 'time_period' not in comp or 'weight' not in comp:
                        raise ValueError(f"Each component must have 'time_period' and 'weight' keys: {comp}")
                    
                    time_period_str = comp['time_period']
                    weight = comp['weight']
                    
                    # Validate time_period format
                    if time_period_str not in ['season', 'none'] and not (
                        time_period_str.startswith('games_') and 
                        time_period_str[6:].isdigit()
                    ):
                        raise ValueError(
                            f"Invalid time_period: {time_period_str}. Must be 'season', 'none', or 'games_N' (e.g., 'games_10', 'games_12', 'games_20')"
                        )
                    
                    if not (0 <= weight <= 1):
                        raise ValueError(f"Weight must be between 0 and 1: {weight}")
                    
                    validated_components.append({
                        'time_period': time_period_str,
                        'weight': float(weight)
                    })
                    total_weight += float(weight)
                
                if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
                    raise ValueError(f"Component weights must sum to 1.0, got {total_weight}: {wc}")
                
                validated_weight_configs.append(validated_components)
            else:
                raise ValueError(
                    f"Weight config must have 'blend_components' with list of {{'time_period': str, 'weight': float}}: {wc}"
                )
        
        # Determine date range (default: last 2 full seasons = 2022-2023 and 2023-2024)
        if time_period is None:
            time_period = {'begin_year': 2022, 'end_year': 2024}
        
        # Get base feature info (stat_name, calc_weight, is_net)
        stat_name, calc_weight, is_net = self._get_base_feature_info(blend_feature_name)
        
        # Build MongoDB query
        query = self._build_query(time_period)
        
        # Initialize BballModel to access StatHandlerV2
        # Use minimal features list since we're generating our own blend features
        # Need to preload data for StatHandlerV2 to calculate features properly
        classifier_features = []  # Empty - we'll calculate features manually
        model = BballModel(
            classifier_features=classifier_features,
            include_elo=False,
            include_per_features=False,
            include_injuries=False,
            preload_data=True  # Need preloaded data for feature calculation
        )
        
        # Fetch games
        games = self._games_repo.find(query, sort=[('year', 1), ('month', 1), ('day', 1)])
        if len(games) == 0:
            raise ValueError(f"No games found for time period: {time_period}")
        
        print(f"Found {len(games)} games for blend experiment")
        
        # Collect all unique time periods from all weight configs
        all_time_periods = set()
        for components in validated_weight_configs:
            for comp in components:
                all_time_periods.add(comp['time_period'])
        
        print(f"Calculating base features for time periods: {sorted(all_time_periods)}")
        
        # Calculate base features for all time periods for all games
        base_feature_data = []
        processed_count = 0
        skipped_count = 0
        
        for game in games:
            home_team = game.get('homeTeam', {}).get('name', '')
            away_team = game.get('awayTeam', {}).get('name', '')
            season = game.get('season', '')
            year = game.get('year', 0)
            month = game.get('month', 0)
            day = game.get('day', 0)
            home_won = 1 if game.get('homeTeam', {}).get('points', 0) > game.get('awayTeam', {}).get('points', 0) else 0
            
            if not home_team or not away_team:
                skipped_count += 1
                continue
            
            try:
                # Calculate feature value for each time period
                game_features = {
                    'Year': year,
                    'Month': month,
                    'Day': day,
                    'Home': home_team,
                    'Away': away_team,
                    'HomeWon': home_won
                }
                
                has_nan = False
                for tp in all_time_periods:
                    if is_net:
                        value = model.stat_handler._calculate_net_feature(
                            stat_name, tp, calc_weight, 'diff', False,
                            home_team, away_team, season, year, month, day
                        )
                    else:
                        value = model.stat_handler._calculate_regular_feature(
                            stat_name, tp, calc_weight, 'diff', False,
                            home_team, away_team, season, year, month, day
                        )
                    
                    # Store with a consistent column name
                    col_name = f"{tp}_component"
                    game_features[col_name] = value
                    
                    import math
                    if math.isnan(value):
                        has_nan = True
                
                if has_nan:
                    skipped_count += 1
                    if processed_count < 5:  # Only log first few to avoid spam
                        print(f"Warning: NaN values for game {year}-{month}-{day} {home_team} vs {away_team}")
                    continue
                
                base_feature_data.append(game_features)
                processed_count += 1
            except Exception as e:
                skipped_count += 1
                if processed_count + skipped_count <= 10:  # Only log first few errors to avoid spam
                    import traceback
                    print(f"Warning: Failed to calculate features for game {year}-{month}-{day} {home_team} vs {away_team}: {e}")
                    print(f"Traceback: {traceback.format_exc()}")
                continue
        
        if len(base_feature_data) == 0:
            raise ValueError(
                f"No games processed successfully (processed: {processed_count}, skipped: {skipped_count}, total: {len(games)}). "
                f"Check that games have valid team names, dates, and sufficient historical data for feature calculation."
            )
        
        base_df = pd.DataFrame(base_feature_data)
        print(f"Calculated base features for {len(base_df)} games (skipped {skipped_count} games)")
        
        # Verify required columns exist
        required_cols = [f"{tp}_component" for tp in all_time_periods]
        missing_cols = [col for col in required_cols if col not in base_df.columns]
        if missing_cols:
            raise ValueError(
                f"Missing required columns in base_df: {missing_cols}. "
                f"DataFrame columns: {list(base_df.columns)}. "
                f"DataFrame shape: {base_df.shape}"
            )
        
        # Generate blend variants and run experiments
        results = []
        variant_csv_paths = {}
        
        for components in validated_weight_configs:
            # Create a descriptive weight string for this configuration
            weight_parts = []
            weight_dict = {}
            for comp in components:
                tp = comp['time_period']
                w = comp['weight']
                weight_parts.append(f"{tp}_{w:.2f}")
                weight_dict[tp] = w
            
            weight_str = "_".join(weight_parts)
            blend_feature_name_variant = f"{blend_feature_name}_blend_{weight_str}"
            
            print(f"\nTesting blend components: {[(c['time_period'], c['weight']) for c in components]}")
            
            # Calculate blend feature by summing weighted components
            blend_values = pd.Series(0.0, index=base_df.index)
            for comp in components:
                tp = comp['time_period']
                w = comp['weight']
                col_name = f"{tp}_component"
                if col_name not in base_df.columns:
                    raise ValueError(f"Missing component column {col_name} in base_df. Available columns: {list(base_df.columns)}")
                blend_values += w * base_df[col_name]
            
            # Create DataFrame for this variant
            variant_df = base_df[['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']].copy()
            variant_df[blend_feature_name_variant] = blend_values
            
            # Add base features if specified
            if base_features:
                # Load from master CSV if needed (simplified - just include the blend for now)
                # For full implementation, would merge with master CSV
                pass
            
            # Save CSV
            csv_filename = f"blend_{blend_feature_name}_{weight_str}.csv"
            csv_path = os.path.join(self.cache_dir, csv_filename)
            variant_df.to_csv(csv_path, index=False)
            variant_csv_paths[weight_str] = csv_path
            
            # Run lightweight experiment
            importance_score, metrics = self._run_lightweight_experiment(
                csv_path, blend_feature_name_variant, model_type
            )
            
            # Build result dict with all component weights
            result_dict = {
                'weight_config': weight_str,
                'importance_score': importance_score,
                'accuracy': metrics.get('accuracy', 0),
                'log_loss': metrics.get('log_loss', float('inf')),
                'brier_score': metrics.get('brier_score', float('inf'))
            }
            # Add individual component weights for readability
            for comp in components:
                result_dict[f"{comp['time_period']}_weight"] = comp['weight']
            
            results.append(result_dict)
        
        # Sort by importance score (descending)
        results.sort(key=lambda x: x['importance_score'], reverse=True)
        
        # Find best configuration
        best_config = results[0] if results else None
        
        return {
            'comparison_table': results,
            'variant_csv_paths': variant_csv_paths,
            'summary': {
                'best_config': best_config,
                'blend_feature_name': blend_feature_name,
                'total_variants': len(results)
            }
        }
    
    def _get_base_feature_info(self, blend_feature_name: str) -> Tuple[str, str, bool]:
        """
        Get base feature information for a blend feature.
        
        Returns:
            Tuple of (stat_name, calc_weight, is_net)
        """
        # Map blend feature names to base feature info
        # Based on StatHandlerV2._calculate_blend_feature blend_configs
        blend_info = {
            'wins': ('wins', 'avg', False),
            'points_net': ('points', 'avg', True),
            'off_rtg_net': ('off_rtg', 'raw', True),
            'efg_net': ('efg', 'raw', True),
        }
        
        if blend_feature_name not in blend_info:
            raise ValueError(f"Unknown blend_feature_name: {blend_feature_name}")
        
        return blend_info[blend_feature_name]
    
    def _build_query(self, time_period: Dict) -> Dict:
        """Build MongoDB query from time_period dict"""
        query = {
            'homeTeam.points': {'$gt': 0},
            'awayTeam.points': {'$gt': 0},
            'game_type': {'$nin': ['preseason', 'allstar']}
        }
        
        if 'begin_year' in time_period:
            query['year'] = {'$gte': time_period['begin_year']}
        if 'end_year' in time_period:
            if 'year' in query:
                query['year']['$lte'] = time_period['end_year']
            else:
                query['year'] = {'$lte': time_period['end_year']}
        
        if 'begin_date' in time_period or 'end_date' in time_period:
            date_query = {}
            if 'begin_date' in time_period:
                date_query['$gte'] = time_period['begin_date']
            if 'end_date' in time_period:
                date_query['$lte'] = time_period['end_date']
            if date_query:
                query['date'] = date_query
        
        return query
    
    def _run_lightweight_experiment(
        self,
        csv_path: str,
        feature_name: str,
        model_type: str
    ) -> Tuple[float, Dict]:
        """
        Run lightweight experiment to get feature importance.
        
        Returns:
            Tuple of (importance_score, metrics_dict)
        """
        # Load data
        df = read_csv_safe(csv_path)
        
        if df.empty:
            return 0.0, {}
        
        # Prepare features and target
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        if len(feature_cols) == 0:
            return 0.0, {}
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        # Simple train/test split (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = create_model_with_c(model_type, c_value=0.1 if model_type == 'LogisticRegression' else None)
        model.fit(X_train_scaled, y_train)
        
        # Get feature importance/coefficient
        importance_score = 0.0
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            importances = model.feature_importances_
            if feature_name in feature_cols:
                feature_idx = feature_cols.index(feature_name)
                importance_score = float(importances[feature_idx])
        elif hasattr(model, 'coef_'):
            # Linear models - use absolute coefficient
            coef = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
            if feature_name in feature_cols:
                feature_idx = feature_cols.index(feature_name)
                importance_score = float(abs(coef[feature_idx]))
        
        # Calculate metrics on test set
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        y_pred = (y_pred_proba > 0.5).astype(int)
        
        accuracy = float(accuracy_score(y_test, y_pred))
        log_loss_val = float(log_loss(y_test, y_pred_proba))
        brier_score = float(brier_score_loss(y_test, y_pred_proba))
        
        metrics = {
            'accuracy': accuracy,
            'log_loss': log_loss_val,
            'brier_score': brier_score
        }
        
        return importance_score, metrics

