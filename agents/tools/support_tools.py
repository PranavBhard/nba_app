"""
Support Tools - list_runs, compare_runs, explain_run, feature_audit, predict
"""

import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from scipy import stats

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.agents.tools.run_tracker import RunTracker
from nba_app.cli.Mongo import Mongo
from nba_app.cli.NBAModel import NBAModel
from nba_app.cli.master_training_data import MASTER_TRAINING_PATH
from nba_app.agents.utils.json_compression import encode_tool_output


class SupportTools:
    """Support tools for experiment analysis"""
    
    def __init__(self, db=None):
        """
        Initialize SupportTools.
        
        Args:
            db: MongoDB database instance (optional)
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        self.run_tracker = RunTracker(db=self.db)
    
    def list_runs(
        self,
        session_id: Optional[str] = None,
        model_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        List experiment runs with optional filters.
        
        Args:
            session_id: Filter by session ID
            model_type: Filter by model type
            limit: Maximum number of runs to return
            
        Returns:
            List of run summaries
        """
        runs = self.run_tracker.list_runs(
            session_id=session_id,
            model_type=model_type,
            limit=limit
        )
        
        # Format as summaries
        summaries = []
        for run in runs:
            summaries.append({
                'run_id': run['run_id'],
                'created_at': run['created_at'],
                'model_type': run['model_type'],
                'metrics': run.get('metrics', {}),
                'status': run.get('status', 'unknown'),
                'baseline': run.get('baseline', False),
                'description': run.get('config', {}).get('description')
            })
        
        return encode_tool_output(summaries)
    
    def compare_runs(self, run_ids: List[str]) -> Dict:
        """
        Compare multiple runs and generate leaderboard.
        
        Args:
            run_ids: List of run IDs to compare
            
        Returns:
            Dict with leaderboard and pairwise comparisons
        """
        runs = []
        for run_id in run_ids:
            run = self.run_tracker.get_run(run_id)
            if run:
                runs.append(run)
        
        if len(runs) < 2:
            raise ValueError("Need at least 2 runs to compare")
        
        # Extract metrics
        metrics_list = []
        for run in runs:
            metrics = run.get('metrics', {})
            metrics_list.append({
                'run_id': run['run_id'],
                'model_type': run['model_type'],
                'accuracy': metrics.get('accuracy_mean', 0),
                'log_loss': metrics.get('log_loss_mean', float('inf')),
                'brier': metrics.get('brier_mean', float('inf')),
                'auc': metrics.get('auc', 0)
            })
        
        # Sort by accuracy (descending)
        leaderboard = sorted(metrics_list, key=lambda x: x['accuracy'], reverse=True)
        
        # Pairwise comparisons
        comparisons = []
        for i in range(len(leaderboard)):
            for j in range(i + 1, len(leaderboard)):
                run1 = leaderboard[i]
                run2 = leaderboard[j]
                
                # Calculate deltas
                delta_acc = run1['accuracy'] - run2['accuracy']
                delta_ll = run1['log_loss'] - run2['log_loss']
                delta_brier = run1['brier'] - run2['brier']
                
                comparisons.append({
                    'run1_id': run1['run_id'],
                    'run2_id': run2['run_id'],
                    'delta_accuracy': delta_acc,
                    'delta_log_loss': delta_ll,
                    'delta_brier': delta_brier,
                    'better': run1['run_id'] if delta_acc > 0 else run2['run_id']
                })
        
        return {
            'leaderboard': leaderboard,
            'pairwise_comparisons': comparisons,
            'n_runs': len(runs)
        }
    
    def explain_run(self, run_id: str, session_id: Optional[str] = None) -> Dict:
        """
        Get detailed explanation of a run.
        
        Args:
            run_id: Run identifier
            session_id: Optional session ID to check if run belongs to this session
            
        Returns:
            Dict with coefficients/importances, F-scores, error analysis, calibration info
        """
        run = self.run_tracker.get_run(run_id)
        if not run:
            # Provide helpful error message with suggestions
            import re
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            is_uuid_format = bool(re.match(uuid_pattern, run_id.lower()))
            
            if is_uuid_format:
                # Run doesn't exist - provide helpful error message
                error_msg = (
                    f"Run {run_id} not found. "
                    f"This run_id doesn't exist in the database. "
                    f"It may have been deleted, or the run_id is incorrect. "
                    f"Use `list_runs()` to see available runs and their run_ids."
                )
            else:
                # Not a UUID format - likely a name or description
                error_msg = (
                    f"Run '{run_id}' not found. "
                    f"Run IDs are UUIDs (e.g., '550e8400-e29b-41d4-a716-446655440000'). "
                    f"'{run_id}' appears to be a name or description, not a run_id. "
                    f"Use `list_runs()` to see available runs and their run_ids."
                )
            
            # Add recent runs for current session if available
            if session_id:
                recent_runs = self.run_tracker.list_runs(session_id=session_id, limit=5)
                if recent_runs:
                    recent_run_ids = [r.get('run_id') for r in recent_runs if r.get('run_id')]
                    error_msg += f" Recent run_ids for this session: {recent_run_ids[:3]}"
            
            raise ValueError(error_msg)
        
        diagnostics = run.get('diagnostics', {})
        metrics = run.get('metrics', {})
        config = run.get('config') or {}  # Ensure config is always a dict, not None
        artifacts = run.get('artifacts', {})
        
        # Get feature importances (model-based: coefficients or feature_importances_)
        feature_importances = diagnostics.get('feature_importances', {})
        
        # Convert to sorted list (all features, not just top 20)
        all_features = list(feature_importances.items())
        all_features.sort(key=lambda x: x[1], reverse=True)  # Sort by importance descending
        
        # Top features for quick reference
        top_features = all_features[:20]
        
        # Calculate F-scores (statistical univariate importance) if dataset is available
        # This matches what the model-config UI uses
        f_scores = {}
        try:
            dataset_path = artifacts.get('dataset_path')
            if dataset_path and os.path.exists(dataset_path):
                import pandas as pd
                import numpy as np
                from sklearn.feature_selection import SelectKBest, f_classif
                from sklearn.preprocessing import StandardScaler
                
                # Load dataset
                df = pd.read_csv(dataset_path)
                
                # Identify columns (same logic as experiment_runner)
                meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
                if 'game_id' in df.columns:
                    meta_cols.append('game_id')
                
                target_cols = ['HomeWon']
                if 'home_points' in df.columns:
                    target_cols.append('home_points')
                if 'away_points' in df.columns:
                    target_cols.append('away_points')
                
                excluded_cols = meta_cols + target_cols
                pred_cols = ['pred_home_points', 'pred_away_points', 'pred_margin', 'pred_point_total']
                excluded_cols.extend([c for c in pred_cols if c in df.columns])
                
                feature_cols = [c for c in df.columns if c not in excluded_cols]
                
                if len(feature_cols) > 0 and 'HomeWon' in df.columns:
                    # Extract features and target
                    X = df[feature_cols].values
                    y = df['HomeWon'].values
                    
                    # Standardize (same as training)
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # Calculate F-scores using SelectKBest (same as UI)
                    fs = SelectKBest(score_func=f_classif, k=len(feature_cols))
                    fs.fit(X_scaled, y)
                    
                    # Create dict of feature -> F-score
                    f_scores = dict(zip(feature_cols, fs.scores_.tolist()))
                    
                    # Sort by F-score descending
                    f_scores_sorted = sorted(f_scores.items(), key=lambda x: x[1], reverse=True)
                    f_scores = dict(f_scores_sorted)
        except Exception as e:
            # If F-score calculation fails, continue without it
            # This can happen if dataset is missing, corrupted, or for points regression runs
            pass
        
        # Error analysis (if we have fold-level metrics)
        error_analysis = {}
        if 'accuracy_folds' in metrics:
            acc_folds = metrics['accuracy_folds']
            error_analysis = {
                'fold_accuracies': acc_folds,
                'std_across_folds': metrics.get('accuracy_std', 0),
                'min_fold': min(acc_folds) if acc_folds else 0,
                'max_fold': max(acc_folds) if acc_folds else 0
            }
        
        # Points regression specific analysis (margin and total metrics)
        points_analysis = {}
        if 'margin_mae' in metrics or 'total_mae' in metrics:
            points_analysis = {
                'margin_metrics': {
                    'mae': metrics.get('margin_mae'),
                    'rmse': metrics.get('margin_rmse'),
                    'r2': metrics.get('margin_r2')
                } if 'margin_mae' in metrics else None,
                'total_metrics': {
                    'mae': metrics.get('total_mae'),
                    'rmse': metrics.get('total_rmse'),
                    'r2': metrics.get('total_r2')
                } if 'total_mae' in metrics else None
            }
        
        # Safely extract config summary (handle both classification and regression)
        model_config = config.get('model') or config.get('points_model') or {}
        model_type = model_config.get('type') if isinstance(model_config, dict) else None
        
        # Extract hyperparameters for points regression models
        model_hyperparameters = {}
        if isinstance(model_config, dict):
            if 'alpha' in model_config:
                model_hyperparameters['alpha'] = model_config['alpha']
            if 'l1_ratio' in model_config:
                model_hyperparameters['l1_ratio'] = model_config['l1_ratio']
            if 'n_estimators' in model_config:
                model_hyperparameters['n_estimators'] = model_config['n_estimators']
            if 'max_depth' in model_config:
                model_hyperparameters['max_depth'] = model_config['max_depth']
            if 'learning_rate' in model_config:
                model_hyperparameters['learning_rate'] = model_config['learning_rate']
            if 'target' in model_config:
                model_hyperparameters['target'] = model_config['target']
        
        # Extract selected alpha and alphas tested from diagnostics/artifacts (for Ridge models)
        selected_alpha = diagnostics.get('selected_alpha') or artifacts.get('selected_alpha')
        alphas_tested = diagnostics.get('alphas_tested') or artifacts.get('alphas_tested')
        
        # If multiple alphas were tested, add this to model hyperparameters
        if selected_alpha is not None:
            model_hyperparameters['selected_alpha'] = selected_alpha
        if alphas_tested is not None and len(alphas_tested) > 1:
            model_hyperparameters['alphas_tested'] = alphas_tested
        
        features_config = config.get('features') or {}
        feature_blocks = features_config.get('blocks', []) if isinstance(features_config, dict) else []
        
        splits_config = config.get('splits') or {}
        split_type = splits_config.get('type') if isinstance(splits_config, dict) else None
        
        # Extract time-based calibration info and sample sizes
        time_calibration_info = {}
        if split_type == 'year_based_calibration' or 'train_set_size' in metrics:
            time_calibration_info = {
                'begin_year': splits_config.get('begin_year'),
                'calibration_years': splits_config.get('calibration_years', []),
                'evaluation_year': splits_config.get('evaluation_year'),
                'train_set_size': metrics.get('train_set_size'),
                'calibrate_set_size': metrics.get('calibrate_set_size'),
                'evaluate_set_size': metrics.get('evaluate_set_size'),
                'train_years': metrics.get('train_years', []),
                'calibrate_years': metrics.get('calibrate_years', []),
                'evaluate_years': metrics.get('evaluate_years', [])
            }
        
        # Extract feature names from config, artifacts, or feature_importances
        feature_names = []
        if 'features' in config:
            features_config = config['features']
            if 'features' in features_config and isinstance(features_config['features'], list):
                feature_names = features_config['features']
            elif 'blocks' in features_config:
                # Feature blocks - we can't get individual names from blocks alone
                feature_names = []
        
        # Fallback: use feature_importances keys if feature_names is empty
        if not feature_names and feature_importances:
            feature_names = list(feature_importances.keys())
        
        result = {
            'run_id': run_id,
            'model_type': run.get('model_type'),
            'metrics': metrics,
            'feature_importances': dict(feature_importances),  # Model-based: coefficients or feature_importances_
            'feature_importances_sorted': all_features,  # All features sorted by model importance
            'f_scores': f_scores,  # Statistical univariate F-scores (ANOVA F-test)
            'f_scores_sorted': sorted(f_scores.items(), key=lambda x: x[1], reverse=True) if f_scores else [],  # Sorted F-scores
            'top_features': top_features,  # Top 20 for quick reference (model-based)
            'total_features': len(feature_importances),
            'error_analysis': error_analysis,
            'config_summary': {
                'model': model_type,
                'feature_blocks': feature_blocks,
                'split_type': split_type,
                'model_hyperparameters': model_hyperparameters  # Includes selected_alpha, alphas_tested, etc.
            },
            'time_calibration_info': time_calibration_info,  # NEW: Time-based calibration details
            'feature_names': feature_names,  # NEW: List of feature names used
            'selected_alpha': selected_alpha,  # Selected alpha for Ridge models (if multiple were tested)
            'alphas_tested': alphas_tested  # List of alphas tested for Ridge models (if multiple)
        }
        
        # Add points regression specific analysis if available
        if points_analysis:
            result['points_analysis'] = points_analysis
        
        return encode_tool_output(result)
    
    def feature_audit(self, dataset_id: str) -> Dict:
        """
        Audit a dataset for data quality issues.
        
        Args:
            dataset_id: Dataset identifier (from build_dataset)
            
        Returns:
            Dict with missingness, variance, correlations, leakage signals
        """
        # Find dataset CSV
        from nba_app.agents.tools.dataset_builder import DatasetBuilder
        dataset_builder = DatasetBuilder(db=self.db)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
        cache_dir = os.path.join(parent_dir, 'model_output', 'dataset_cache')
        cache_file = os.path.join(cache_dir, f'dataset_{dataset_id}.csv')
        
        if not os.path.exists(cache_file):
            raise ValueError(f"Dataset {dataset_id} not found")
        
        # Load dataset
        df = pd.read_csv(cache_file)
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols]
        
        # Missingness
        missingness = {}
        for col in feature_cols:
            missing_count = X[col].isna().sum()
            missing_pct = (missing_count / len(X)) * 100
            missingness[col] = {
                'count': int(missing_count),
                'percentage': float(missing_pct)
            }
        
        # Variance
        variances = {}
        for col in feature_cols:
            var = X[col].var()
            variances[col] = float(var) if not np.isnan(var) else 0.0
        
        # Low variance features
        low_variance = [col for col, var in variances.items() if var < 1e-6]
        
        # Correlation clusters (highly correlated features)
        corr_matrix = X.corr().abs()
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if corr_val > 0.95:  # Very high correlation
                    high_corr_pairs.append({
                        'feature1': corr_matrix.columns[i],
                        'feature2': corr_matrix.columns[j],
                        'correlation': float(corr_val)
                    })
        
        # Stability over time (if we have time columns)
        stability = {}
        if 'Year' in df.columns:
            # Group by year and check feature means
            yearly_means = df.groupby('Year')[feature_cols].mean()
            for col in feature_cols[:10]:  # Check first 10 features
                year_means = yearly_means[col].values
                if len(year_means) > 1:
                    cv = np.std(year_means) / (np.mean(year_means) + 1e-10)  # Coefficient of variation
                    stability[col] = float(cv)
        
        return encode_tool_output({
            'dataset_id': dataset_id,
            'n_rows': len(df),
            'n_features': len(feature_cols),
            'missingness': missingness,
            'variances': variances,
            'low_variance_features': low_variance,
            'high_correlation_pairs': high_corr_pairs[:20],  # Top 20
            'stability_over_time': stability
        })
    
    def predict(self, model_id: str, prediction_spec: Dict) -> Dict:
        """
        Make predictions using a trained model.
        
        Args:
            model_id: Model identifier (run_id)
            prediction_spec: Dict with:
                - game_id: Optional game ID
                - date: Optional date (YYYY-MM-DD)
                - cutoff_date: Date to use for feature calculation
                
        Returns:
            Dict with predictions
        """
        # Get run to find model artifacts
        run = self.run_tracker.get_run(model_id)
        if not run:
            raise ValueError(f"Model {model_id} not found")
        
        # For now, return a placeholder
        # Full implementation would load the model and call NBAModel.predict()
        return encode_tool_output({
            'model_id': model_id,
            'status': 'not_implemented',
            'message': 'Prediction tool requires model artifact loading (to be implemented)'
        })
    
    def get_available_features(self) -> List[str]:
        """
        Get list of currently available features from pre-computed feature set.
        
        Returns:
            List of available feature names (excluding metadata columns)
        """
        if not os.path.exists(MASTER_TRAINING_PATH):
            return encode_tool_output({
                'available_features': [],
                'message': 'Master training CSV not found. No pre-computed features available.',
                'total_count': 0
            })
        
        try:
            # Read just the header to get feature names
            master_df = pd.read_csv(MASTER_TRAINING_PATH, nrows=0)
            
            # Metadata columns to exclude
            meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
            
            # Get feature columns
            feature_cols = [c for c in master_df.columns if c not in meta_cols]
            
            return encode_tool_output({
                'available_features': sorted(feature_cols),
                'total_count': len(feature_cols),
                'message': f'Found {len(feature_cols)} available features in pre-computed feature set.'
            })
        except Exception as e:
            return encode_tool_output({
                'available_features': [],
                'total_count': 0,
                'message': f'Error reading master training CSV: {e}',
                'error': str(e)
            })
    
    def _map_master_features_to_blocks(self, master_features: set) -> Dict[str, List[str]]:
        """
        Map all features from master CSV to feature blocks.
        Uses the same logic as web/app.py's load_features_from_master_csv().
        
        Args:
            master_features: Set of feature names from master CSV
            
        Returns:
            Dict mapping block name to list of features
        """
        from collections import defaultdict
        
        features_by_block = defaultdict(list)
        
        for feature in master_features:
            feature_lower = feature.lower()
            
            # Parse feature name to determine block
            if '|' in feature:
                parts = feature.split('|')
                stat_name = parts[0].lower()
                
                # Determine feature block based on stat name and patterns
                # Check in order of specificity (more specific first)
                if 'inj' in stat_name or 'inj' in feature_lower:
                    features_by_block['injuries'].append(feature)
                elif 'player_per' in stat_name or 'team_per' in stat_name or 'starters_per' in stat_name or \
                     'per1' in stat_name or 'per2' in stat_name or 'per3' in stat_name or 'per_available' in feature_lower:
                    features_by_block['player_talent'].append(feature)
                elif 'elo' in stat_name:
                    features_by_block['elo_strength'].append(feature)
                elif 'rel' in feature_lower:
                    features_by_block['era_normalization'].append(feature)
                elif 'off_rtg' in stat_name or 'assists_ratio' in stat_name:
                    features_by_block['offensive_engine'].append(feature)
                elif 'def_rtg' in stat_name or 'blocks' in stat_name or 'reb_total' in stat_name or 'reb_' in stat_name or 'turnovers' in stat_name:
                    features_by_block['defensive_engine'].append(feature)
                elif 'efg' in stat_name or 'ts' in stat_name or 'three' in stat_name:
                    features_by_block['shooting_efficiency'].append(feature)
                elif 'points' in stat_name or 'wins' in stat_name:
                    features_by_block['outcome_strength'].append(feature)
                elif 'pace' in stat_name or 'std' in feature_lower:
                    features_by_block['pace_volatility'].append(feature)
                elif 'b2b' in stat_name or 'travel' in stat_name or 'rest' in feature_lower:
                    features_by_block['schedule_fatigue'].append(feature)
                elif 'games_played' in stat_name:
                    if 'days' in feature_lower or 'diff' in feature_lower:
                        features_by_block['schedule_fatigue'].append(feature)
                    else:
                        features_by_block['sample_size'].append(feature)
                else:
                    # Default: put in absolute_magnitude
                    features_by_block['absolute_magnitude'].append(feature)
            else:
                # Old format features - try to categorize
                if 'Per' in feature or ('per' in feature_lower and 'percent' not in feature_lower):
                    features_by_block['player_talent'].append(feature)
                elif 'Inj' in feature or 'inj' in feature_lower:
                    features_by_block['injuries'].append(feature)
                elif 'Pace' in feature or 'pace' in feature_lower:
                    features_by_block['pace_volatility'].append(feature)
                elif 'B2B' in feature or 'Travel' in feature or 'GamesLast' in feature or 'rest' in feature_lower:
                    features_by_block['schedule_fatigue'].append(feature)
                elif 'Rel' in feature or 'rel' in feature_lower:
                    features_by_block['era_normalization'].append(feature)
                elif 'Elo' in feature or 'elo' in feature_lower:
                    features_by_block['elo_strength'].append(feature)
                elif 'GamesPlayed' in feature:
                    features_by_block['sample_size'].append(feature)
                else:
                    features_by_block['absolute_magnitude'].append(feature)
        
        # Convert to regular dict and sort features within each block
        return {block: sorted(features) for block, features in features_by_block.items()}
    
    def get_features_by_block(self, feature_blocks: List[str]) -> Dict:
        """
        Get list of features for specified feature blocks, including ALL features from master CSV.
        Features are mapped to blocks based on their names, and all master CSV features are included
        (not just those in FEATURE_SETS). This ensures the agent sees all available features.
        
        Args:
            feature_blocks: List of feature block names (e.g., ['offensive_engine', 'defensive_engine'])
                           If None or empty, returns all blocks with features.
            
        Returns:
            Dict with:
                - features_by_block: Dict mapping block name to list of available features from master CSV
                - total_features: Total number of unique available features across requested blocks
                - unique_features: Sorted list of all unique available features
                - valid_blocks: List of valid block names that have features (only returned if > 0 features)
                - invalid_blocks: List of invalid block names that were not found
                - all_valid_blocks: List of all valid feature block names (if invalid_blocks present)
        """
        # Get available features from master CSV
        master_features = set()
        if os.path.exists(MASTER_TRAINING_PATH):
            try:
                master_df = pd.read_csv(MASTER_TRAINING_PATH, nrows=0)
                meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
                master_features = set([c for c in master_df.columns if c not in meta_cols])
            except Exception as e:
                # If we can't read master CSV, return error
                return encode_tool_output({
                    'error': f'Failed to read master training CSV: {e}',
                    'features_by_block': {},
                    'total_features': 0,
                    'unique_features': [],
                    'valid_blocks': [],
                    'invalid_blocks': feature_blocks if feature_blocks else [],
                    'all_valid_blocks': []  # Can't determine without master CSV
                })
        else:
            # Master CSV doesn't exist
            return encode_tool_output({
                'error': 'Master training CSV not found. No features available.',
                'features_by_block': {},
                'total_features': 0,
                'unique_features': [],
                'valid_blocks': [],
                'invalid_blocks': feature_blocks if feature_blocks else [],
                'all_valid_blocks': []  # Can't determine without master CSV
            })
        
        # Map ALL master CSV features to blocks
        all_master_features_by_block = self._map_master_features_to_blocks(master_features)
        
        # If no specific blocks requested, return all blocks that have features
        if not feature_blocks:
            # Only return blocks that have features (don't return empty blocks)
            features_by_block = {block: features for block, features in all_master_features_by_block.items() if len(features) > 0}
            all_features = set()
            for features in features_by_block.values():
                all_features.update(features)
            
            return encode_tool_output({
                'features_by_block': features_by_block,
                'total_features': len(all_features),
                'unique_features': sorted(list(all_features)),
                'valid_blocks': sorted(list(features_by_block.keys())),
                'invalid_blocks': [],
                'all_valid_blocks': sorted(list(features_by_block.keys())),
                'message': f'Found {len(all_features)} features across {len(features_by_block)} blocks in master CSV.'
            })
        
        # Filter to requested blocks
        features_by_block = {}
        valid_blocks = []
        invalid_blocks = []
        all_features = set()
        
        for block_name in feature_blocks:
            if block_name in all_master_features_by_block:
                block_features = all_master_features_by_block[block_name]
                # Only include blocks that have features (don't return empty blocks)
                if len(block_features) > 0:
                    features_by_block[block_name] = block_features
                    valid_blocks.append(block_name)
                    all_features.update(block_features)
                # If block exists but has no features, don't include it (per requirement #2)
            else:
                invalid_blocks.append(block_name)
        
        return encode_tool_output({
            'features_by_block': features_by_block,
            'total_features': len(all_features),
            'unique_features': sorted(list(all_features)),
            'valid_blocks': valid_blocks,
            'invalid_blocks': invalid_blocks,
            'all_valid_blocks': sorted(list(all_master_features_by_block.keys())) if invalid_blocks else sorted(list(all_master_features_by_block.keys())),
            'message': f'Found {len(all_features)} available features across {len(valid_blocks)} requested blocks in master CSV.'
        })
    
    def explain_feature_calculation(self, feature_name: str) -> Dict:
        """
        Explain how a specific feature is calculated.
        
        Args:
            feature_name: Feature name in new format (e.g., 'wins_blend|none|blend:season:0.80/games_12:0.20|diff')
            
        Returns:
            Dict with:
                - feature_name: The feature name
                - calculation_type: Type of calculation (blend, regular, net, enhanced, etc.)
                - formula: Human-readable formula description
                - components: List of component details (for blend features)
                - time_periods: List of time periods used
                - weights: Dict of weights (for blend features)
                - calc_weight: Calculation method (avg, raw, etc.)
                - perspective: home, away, or diff
        """
        from nba_app.cli.feature_name_parser import parse_feature_name
        
        # Parse the feature name
        components = parse_feature_name(feature_name)
        if not components:
            return encode_tool_output({
                'feature_name': feature_name,
                'error': 'Could not parse feature name. Ensure it follows the format: stat_name|time_period|calc_weight|home/away/diff'
            })
        
        stat_name = components.stat_name
        time_period = components.time_period
        calc_weight = components.calc_weight
        perspective = components.home_away_diff
        
        result = {
            'feature_name': feature_name,
            'stat_name': stat_name,
            'time_period': time_period,
            'calc_weight': calc_weight,
            'perspective': perspective,
            'is_side': components.is_side
        }
        
        # Handle blend features
        if stat_name.endswith('_blend'):
            base_stat_name = stat_name[:-6]
            result['calculation_type'] = 'blend'
            
            # Parse blend components
            blend_components = {}
            if time_period.startswith('blend:'):
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
            else:
                # Invalid blend format
                result['error'] = f"Invalid blend format '{time_period}'. Expected 'blend:period:weight/period:weight'"
            
            result['weights'] = blend_components
            result['time_periods'] = list(blend_components.keys())
            
            # Build formula description
            formula_parts = []
            for tp, weight in sorted(blend_components.items(), key=lambda x: x[1], reverse=True):
                formula_parts.append(f"{weight:.2f} * {base_stat_name}|{tp}|{calc_weight}|{perspective}")
            
            result['formula'] = " + ".join(formula_parts)
            result['components'] = [
                {
                    'time_period': tp,
                    'weight': weight,
                    'component_feature': f"{base_stat_name}|{tp}|{calc_weight}|{perspective}"
                }
                for tp, weight in blend_components.items()
            ]
            
        # Handle net features
        elif stat_name.endswith('_net'):
            result['calculation_type'] = 'net'
            base_stat = stat_name[:-4]
            result['formula'] = f"{base_stat}_home - {base_stat}_away (using {time_period} time period, {calc_weight} calculation)"
            
        # Handle regular features
        else:
            result['calculation_type'] = 'regular'
            result['formula'] = f"{stat_name} calculated over {time_period} time period using {calc_weight} method for {perspective} perspective"
        
        return encode_tool_output(result)
    
    def get_last_run_features(self, session_id: Optional[str] = None) -> Dict:
        """
        Get features used in the most recent run for a session.
        
        Args:
            session_id: Optional session ID to filter runs. If None, gets most recent run across all sessions.
            
        Returns:
            Dict with:
                - run_id: Run identifier
                - feature_blocks: List of feature blocks used
                - features: List of actual feature names (if available)
                - config: Full experiment configuration
        """
        runs = self.run_tracker.list_runs(session_id=session_id, limit=1)
        
        if not runs:
            return encode_tool_output({
                'run_id': None,
                'message': 'No runs found for this session.',
                'feature_blocks': [],
                'features': []
            })
        
        run = runs[0]
        config = run.get('config', {})
        feature_config = config.get('features', {})
        feature_blocks = feature_config.get('blocks', [])
        
        # Get actual features from blocks using master CSV (not FEATURE_SETS)
        features = []
        if feature_blocks:
            # Read master CSV to get available features
            master_features = set()
            if os.path.exists(MASTER_TRAINING_PATH):
                try:
                    master_df = pd.read_csv(MASTER_TRAINING_PATH, nrows=0)
                    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
                    master_features = set([c for c in master_df.columns if c not in meta_cols])
                except Exception:
                    master_features = set()
            
            # Map master CSV features to blocks
            all_master_features_by_block = self._map_master_features_to_blocks(master_features)
            
            # Get features for requested blocks
            for block_name in feature_blocks:
                if block_name in all_master_features_by_block:
                    features.extend(all_master_features_by_block[block_name])
        
        return encode_tool_output({
            'run_id': run['run_id'],
            'feature_blocks': feature_blocks,
            'features': features,
            'feature_count': len(features),
            'config': config,
            'model_type': run.get('model_type'),
            'metrics': run.get('metrics', {})
        })

