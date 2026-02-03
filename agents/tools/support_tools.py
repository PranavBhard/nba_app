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
from nba_app.core.mongo import Mongo
from nba_app.core.models.bball_model import BballModel
from nba_app.core.data import ClassifierConfigRepository, PointsConfigRepository
from nba_app.core.services.training_data import MASTER_TRAINING_PATH
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

        # Initialize repositories
        self._classifier_repo = ClassifierConfigRepository(self.db)
        self._points_repo = PointsConfigRepository(self.db)

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
        # Full implementation would load the model and call BballModel.predict()
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
        Map features from master CSV to feature blocks using FEATURE_SETS as SSoT.

        Uses feature_sets.py (which imports from FeatureRegistry) as the canonical
        source for block-to-feature mappings. Features in master_features that exist
        in FEATURE_SETS are mapped to their respective blocks.

        Args:
            master_features: Set of feature names from master CSV

        Returns:
            Dict mapping block name to list of available features
        """
        from nba_app.core.features.sets import FEATURE_SETS

        features_by_block = {}

        # Use FEATURE_SETS as the canonical source (SSoT via FeatureRegistry)
        for block_name, block_features in FEATURE_SETS.items():
            # Filter to only features that exist in master CSV
            available_features = [f for f in block_features if f in master_features]
            if available_features:
                features_by_block[block_name] = sorted(available_features)

        return features_by_block
    
    def get_features_by_block(self, feature_blocks: List[str]) -> Dict:
        """
        Get list of features for specified feature blocks using FEATURE_SETS as SSoT.

        Features are mapped to blocks using feature_sets.py (which uses FeatureRegistry as SSoT).
        Only features that exist in both FEATURE_SETS and master CSV are returned.

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
            feature_name: Feature name (e.g., 'wins_blend|none|blend:season:0.80/games_12:0.20|diff')
            
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
        from nba_app.core.features.parser import parse_feature_name

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

    def get_selected_configs(self) -> Dict:
        """
        Get the currently selected model configurations (classifier and points regression).

        These are the configs selected in the web UI that are used for predictions.

        Returns:
            Dict with:
                - classifier_config: The selected classifier/binary model config (or None if none selected)
                - points_config: The selected points regression model config (or None if none selected)
                - summary: Human-readable summary of selected configs
        """
        # Query for selected classifier config
        classifier_config = self._classifier_repo.get_selected_config()

        # Query for selected points regression config
        points_config = self._points_repo.get_selected_config()

        # Convert MongoDB documents to dicts (remove _id for JSON serialization)
        if classifier_config:
            classifier_config = dict(classifier_config)
            if '_id' in classifier_config:
                classifier_config['_id'] = str(classifier_config['_id'])

        if points_config:
            points_config = dict(points_config)
            if '_id' in points_config:
                points_config['_id'] = str(points_config['_id'])

        # Build summary
        summary_parts = []

        if classifier_config:
            model_type = classifier_config.get('model_type', 'unknown')
            name = classifier_config.get('name', 'unnamed')
            feature_count = len(classifier_config.get('features', []))
            summary_parts.append(f"Classifier: {name} ({model_type}, {feature_count} features)")
        else:
            summary_parts.append("Classifier: None selected")

        if points_config:
            model_type = points_config.get('model_type', 'unknown')
            name = points_config.get('name', 'unnamed')
            feature_count = len(points_config.get('features', []))
            summary_parts.append(f"Points Regression: {name} ({model_type}, {feature_count} features)")
        else:
            summary_parts.append("Points Regression: None selected")

        return encode_tool_output({
            'classifier_config': classifier_config,
            'points_config': points_config,
            'summary': ' | '.join(summary_parts)
        })

    def get_config_by_id(self, config_id: str, config_type: str = 'classifier') -> Dict:
        """
        Get a model configuration by its MongoDB ObjectId.

        Args:
            config_id: MongoDB ObjectId as string
            config_type: 'classifier' for model_config_nba, 'points' for model_config_points_nba

        Returns:
            Dict with the full config document or error message
        """
        from bson import ObjectId
        from bson.errors import InvalidId

        try:
            oid = ObjectId(config_id)
        except InvalidId:
            return encode_tool_output({
                'error': f"Invalid ObjectId format: {config_id}",
                'config': None
            })

        repo = self._classifier_repo if config_type == 'classifier' else self._points_repo
        config = repo.find_by_id(oid)

        if not config:
            return encode_tool_output({
                'error': f"Config not found with id: {config_id} in {config_type} collection",
                'config': None
            })

        # Convert ObjectId to string for JSON serialization
        config = dict(config)
        config['_id'] = str(config['_id'])

        return encode_tool_output({
            'config': config,
            'config_type': config_type,
            'is_trained': bool(config.get('model_artifact_path')),
            'is_selected': config.get('selected', False)
        })

    def list_trained_configs(
        self,
        config_type: str = 'classifier',
        limit: int = 20,
        include_untrained: bool = False
    ) -> Dict:
        """
        List model configurations with training status and metadata.

        Args:
            config_type: 'classifier' for model_config_nba, 'points' for model_config_points_nba, 'all' for both
            limit: Maximum number of configs to return per type
            include_untrained: Whether to include configs without trained artifacts

        Returns:
            Dict with list of configs and summary statistics
        """
        results = {'classifier_configs': [], 'points_configs': []}

        def process_configs(repo, config_key: str, limit: int):
            query = {} if include_untrained else {'model_artifact_path': {'$exists': True, '$ne': None}}
            configs = repo.find(query, sort=[('trained_at', -1)], limit=limit)

            processed = []
            for config in configs:
                processed.append({
                    '_id': str(config['_id']),
                    'config_hash': config.get('config_hash', '')[:8],  # Short hash for reference
                    'name': config.get('name', 'unnamed'),
                    'model_type': config.get('model_type', 'unknown'),
                    'feature_count': len(config.get('features', [])),
                    'features': config.get('features', [])[:10],  # First 10 features for preview
                    'selected': config.get('selected', False),
                    'trained_at': str(config.get('trained_at', '')) if config.get('trained_at') else None,
                    'has_artifacts': bool(config.get('model_artifact_path')),
                    'is_ensemble': config.get('ensemble', False),
                    'use_time_calibration': config.get('use_time_calibration', False),
                    'begin_year': config.get('begin_year'),
                    'calibration_years': config.get('calibration_years', []),
                    'evaluation_year': config.get('evaluation_year'),
                    # Dataset reproducibility fields
                    'dataset_id': config.get('dataset_id'),
                    'diff_mode': config.get('diff_mode'),
                    'feature_blocks': config.get('feature_blocks', []),
                    'include_per': config.get('include_per'),
                    'run_id': config.get('run_id'),
                    # Training metrics preview
                    'accuracy': config.get('accuracy'),
                    'log_loss': config.get('log_loss'),
                    # Points-specific fields
                    'target': config.get('target'),  # 'home_away' or 'margin'
                })
            results[config_key] = processed

        if config_type in ['classifier', 'all']:
            process_configs(self._classifier_repo, 'classifier_configs', limit)

        if config_type in ['points', 'all']:
            process_configs(self._points_repo, 'points_configs', limit)

        # Summary
        n_classifier = len(results['classifier_configs'])
        n_points = len(results['points_configs'])
        selected_classifier = next((c for c in results['classifier_configs'] if c['selected']), None)
        selected_points = next((c for c in results['points_configs'] if c['selected']), None)

        return encode_tool_output({
            **results,
            'summary': {
                'classifier_count': n_classifier,
                'points_count': n_points,
                'selected_classifier_id': selected_classifier['_id'] if selected_classifier else None,
                'selected_points_id': selected_points['_id'] if selected_points else None,
            }
        })

    def run_prediction_with_config(
        self,
        config_id: str,
        home: str,
        away: str,
        config_type: str = 'classifier',
        game_date: Optional[str] = None,
        points_config_id: Optional[str] = None
    ) -> Dict:
        """
        Run a prediction using a specific model config (not just the selected one).

        Args:
            config_id: MongoDB ObjectId of the classifier config to use
            home: Home team abbreviation (e.g., 'LAL')
            away: Away team abbreviation (e.g., 'BOS')
            config_type: 'classifier' (default) - points models are loaded via points_config_id
            game_date: Optional game date (YYYY-MM-DD). Defaults to today.
            points_config_id: Optional MongoDB ObjectId of points config to use for pred_margin

        Returns:
            Dict with prediction results including probabilities, odds, and feature values
        """
        from bson import ObjectId
        from bson.errors import InvalidId
        from datetime import datetime

        # Import prediction infrastructure
        from nba_app.agents.tools.matchup_predict import (
            load_model_from_config,
            load_points_model,
            get_season_from_date
        )
        from nba_app.core.utils.players import build_player_lists_for_prediction
        from nba_app.core.services.config_manager import ModelConfigManager

        # Load classifier config
        try:
            oid = ObjectId(config_id)
        except InvalidId:
            return encode_tool_output({'error': f"Invalid config_id format: {config_id}"})

        config = self._classifier_repo.find_by_id(oid)
        if not config:
            return encode_tool_output({'error': f"Classifier config not found: {config_id}"})

        # Validate config is ready for prediction
        is_valid, error_msg = ModelConfigManager.validate_config_for_prediction(config)
        if not is_valid:
            return encode_tool_output({'error': error_msg})

        # Parse game date
        if game_date:
            try:
                game_date_obj = datetime.strptime(game_date, '%Y-%m-%d').date()
            except ValueError:
                return encode_tool_output({'error': f'Invalid date format: {game_date}. Use YYYY-MM-DD.'})
        else:
            game_date_obj = datetime.now().date()
        game_date_str = game_date_obj.strftime('%Y-%m-%d')
        season = get_season_from_date(datetime(game_date_obj.year, game_date_obj.month, game_date_obj.day))

        # Load model
        model = load_model_from_config(config, self.db)
        if not model:
            return encode_tool_output({'error': 'Failed to load model from config artifacts.'})

        # Build player filters
        player_filters = build_player_lists_for_prediction(
            home_team=home,
            away_team=away,
            season=season,
            game_id=None,
            game_doc=None,
            home_injuries=[],
            away_injuries=[],
            home_starters=None,
            away_starters=None,
            db=self.db
        )

        # Load points model if specified
        additional_features = None
        points_prediction = None

        if points_config_id:
            try:
                points_oid = ObjectId(points_config_id)
                points_config = self._points_repo.find_by_id(points_oid)
                if points_config:
                    points_trainer = load_points_model(points_config, self.db)
                    if points_trainer:
                        game_doc = {
                            'game_id': '',
                            'date': game_date_str,
                            'year': game_date_obj.year,
                            'month': game_date_obj.month,
                            'day': game_date_obj.day,
                            'season': season,
                            'homeTeam': {'name': home},
                            'awayTeam': {'name': away}
                        }
                        points_prediction = points_trainer.predict(game_doc, game_date_str)

                        # Check if classifier needs pred_margin
                        if hasattr(model, 'feature_names') and model.feature_names and 'pred_margin' in model.feature_names:
                            pred_margin = None
                            if 'point_diff_pred' in points_prediction and points_prediction['point_diff_pred'] is not None:
                                pred_margin = points_prediction['point_diff_pred']
                            elif 'home_points' in points_prediction and 'away_points' in points_prediction:
                                pred_home = points_prediction.get('home_points', 0) or 0
                                pred_away = points_prediction.get('away_points', 0) or 0
                                pred_margin = pred_home - pred_away

                            if pred_margin is not None:
                                additional_features = {'pred_margin': pred_margin}
            except Exception as e:
                # Continue without points prediction
                pass

        # Make prediction
        try:
            use_calibrated = config.get('use_time_calibration', False)
            prediction = model.predict_with_player_config(
                home, away, season, game_date_str, player_filters,
                use_calibrated=use_calibrated,
                additional_features=additional_features
            )
        except Exception as e:
            return encode_tool_output({'error': f'Prediction failed: {str(e)}'})

        # Calculate odds
        home_win_prob = prediction.get('home_win_prob', 0)
        away_win_prob = 100 - home_win_prob

        def calculate_odds(prob_percent):
            prob = prob_percent / 100.0
            if prob >= 0.5:
                return int(-100 * prob / (1 - prob))
            else:
                return int(100 * (1 - prob) / prob)

        result = {
            'config_id': config_id,
            'config_name': config.get('name', 'unnamed'),
            'model_type': config.get('model_type'),
            'home': home,
            'away': away,
            'game_date': game_date_str,
            'predicted_winner': prediction.get('predicted_winner', 'home' if home_win_prob > 50 else 'away'),
            'home_win_prob': home_win_prob,
            'away_win_prob': away_win_prob,
            'home_odds': calculate_odds(home_win_prob),
            'away_odds': calculate_odds(away_win_prob),
            'features_used': len(prediction.get('features_dict', {})),
        }

        # Add points predictions if available
        if points_prediction:
            if 'home_points' in points_prediction and points_prediction['home_points'] is not None:
                result['home_points_pred'] = round(points_prediction['home_points'])
            if 'away_points' in points_prediction and points_prediction['away_points'] is not None:
                result['away_points_pred'] = round(points_prediction['away_points'])

        return encode_tool_output(result)

    def config_to_experiment_spec(self, config_id: str, config_type: str = 'classifier') -> Dict:
        """
        Convert a MongoDB model config to an ExperimentConfig-compatible dict.

        This allows the agent to reproduce or modify existing production configs
        by converting them into the experiment schema format.

        IMPORTANT: This method preserves dataset reproducibility fields (diff_mode,
        include_per, feature_blocks, point_model_id) from the config when available.
        When fields are missing, defaults are used and warnings are provided.

        Args:
            config_id: MongoDB ObjectId of the config
            config_type: 'classifier' or 'points'

        Returns:
            Dict that can be passed to run_experiment() with modifications
        """
        from bson import ObjectId
        from bson.errors import InvalidId

        try:
            oid = ObjectId(config_id)
        except InvalidId:
            return encode_tool_output({'error': f"Invalid config_id format: {config_id}"})

        repo = self._classifier_repo if config_type == 'classifier' else self._points_repo
        config = repo.find_by_id(oid)

        if not config:
            return encode_tool_output({'error': f"Config not found: {config_id}"})

        # Track defaulted fields for warnings
        warnings = []

        # Extract dataset reproducibility fields with defaults
        diff_mode = config.get('diff_mode')
        if diff_mode is None:
            diff_mode = 'home_minus_away'
            warnings.append("diff_mode not stored in config - defaulting to 'home_minus_away'")

        include_per = config.get('include_per')
        if include_per is None:
            include_per = config.get('include_per_features', True)
            if 'include_per_features' not in config:
                warnings.append("include_per not stored in config - defaulting to True")

        feature_blocks = config.get('feature_blocks', [])
        point_model_id = config.get('point_model_id')

        # Build experiment config based on type
        if config_type == 'classifier':
            experiment_spec = {
                'task': 'binary_home_win',
                'model': {
                    'type': config.get('model_type', 'LogisticRegression'),
                    'c_value': config.get('best_c_value', 0.1),
                },
                'features': {
                    'blocks': feature_blocks,
                    'features': config.get('features', []) if not feature_blocks else None,
                    'diff_mode': diff_mode,
                    'include_per': include_per,
                    'point_model_id': point_model_id,
                },
                'splits': {
                    'type': 'year_based_calibration' if config.get('use_time_calibration') else 'time_split',
                    'begin_year': config.get('begin_year', 2012),
                    'calibration_years': config.get('calibration_years', [2023]),
                    'evaluation_year': config.get('evaluation_year', 2024),
                    'min_games_played': config.get('min_games_played', 15),
                },
                'preprocessing': {
                    'scaler': 'standard',
                    'impute': 'median',
                },
                'use_time_calibration': config.get('use_time_calibration', True),
                'calibration_method': config.get('calibration_method', 'sigmoid'),
                'description': f"Reproduced from config {config.get('name', config_id[:8])}",
            }
        else:  # points
            experiment_spec = {
                'task': 'points_regression',
                'points_model': {
                    'type': config.get('model_type', 'Ridge'),
                    'target': config.get('target', 'home_away'),
                    'alpha': config.get('best_alpha', 1.0),
                    'l1_ratio': config.get('l1_ratio'),
                },
                'features': {
                    'blocks': feature_blocks,
                    'features': config.get('features', []) if not feature_blocks else None,
                    'diff_mode': diff_mode,
                    'include_per': include_per,
                },
                'splits': {
                    'type': 'year_based_calibration',
                    'begin_year': config.get('begin_year', 2012),
                    'calibration_years': config.get('calibration_years', [2023]),
                    'evaluation_year': config.get('evaluation_year', 2024),
                    'min_games_played': config.get('min_games_played', 15),
                },
                'preprocessing': {
                    'scaler': 'standard',
                    'impute': 'median',
                },
                'description': f"Reproduced from points config {config.get('name', config_id[:8])}",
            }

        result = {
            'experiment_spec': experiment_spec,
            'source_config_id': config_id,
            'source_config_name': config.get('name'),
            'source_dataset_id': config.get('dataset_id'),
            'source_run_id': config.get('run_id'),
            'reproducibility_status': 'full' if not warnings else 'partial',
        }

        if warnings:
            result['warnings'] = warnings
            result['note'] = (
                'Some dataset fields were not stored in the original config. '
                'Defaults were used - the reproduced experiment may produce a different dataset. '
                'Fields with defaults: ' + ', '.join([w.split(' ')[0] for w in warnings])
            )
        else:
            result['note'] = (
                'Full reproducibility: all dataset fields preserved. '
                'This spec can be modified and passed to run_experiment().'
            )

        return encode_tool_output(result)

    def create_model_config(
        self,
        config_type: str,
        model_type: str,
        features: List[str] = None,
        feature_blocks: List[str] = None,
        # Classifier params
        c_value: float = 0.1,
        use_time_calibration: bool = True,
        calibration_method: str = 'sigmoid',
        # Points params
        target: str = 'home_away',
        alpha: float = 1.0,
        l1_ratio: float = None,
        # Shared params
        begin_year: int = 2012,
        calibration_years: List[int] = None,
        evaluation_year: int = 2024,
        min_games_played: int = 15,
        diff_mode: str = 'home_minus_away',
        include_per: bool = True,
        name: str = None,
        selected: bool = False
    ) -> Dict:
        """
        Create a new model configuration in MongoDB.

        This uses the core ModelConfigManager infrastructure (same as web UI).
        Configs are upserted by hash - same params = same config (no duplicates).

        Args:
            config_type: 'classifier' or 'points'
            model_type: Model type (LogisticRegression, Ridge, etc.)
            features: List of individual feature names (mutually exclusive with feature_blocks)
            feature_blocks: List of feature block names (mutually exclusive with features)
            c_value: Regularization for classifier models
            use_time_calibration: Use time-based calibration (classifier only)
            calibration_method: 'sigmoid' or 'isotonic' (classifier only)
            target: 'home_away' or 'margin' (points only)
            alpha: Regularization for points models
            l1_ratio: L1 ratio for ElasticNet (points only)
            begin_year: Training data start year
            calibration_years: Years for calibration set
            evaluation_year: Year for evaluation
            min_games_played: Minimum games filter
            diff_mode: Feature differencing mode
            include_per: Include PER features
            name: Optional custom config name
            selected: Whether to mark as selected

        Returns:
            Dict with config_id, config details, and whether it was newly created or existing
        """
        from nba_app.core.services.config_manager import ModelConfigManager

        config_manager = ModelConfigManager(self.db)

        # Resolve features from blocks if needed
        actual_features = features
        if feature_blocks and not features:
            # Get features from blocks using master CSV mapping
            block_result = self.get_features_by_block(feature_blocks)
            if isinstance(block_result, str):
                import json
                block_result = json.loads(block_result)
            actual_features = block_result.get('unique_features', [])

        if not actual_features:
            return encode_tool_output({
                'error': 'Must provide either features or feature_blocks',
                'config_id': None
            })

        if calibration_years is None:
            calibration_years = [2023]

        try:
            if config_type == 'classifier':
                config_id, config = config_manager.create_classifier_config(
                    model_type=model_type,
                    features=actual_features,
                    c_value=c_value,
                    use_time_calibration=use_time_calibration,
                    calibration_method=calibration_method,
                    begin_year=begin_year,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    min_games_played=min_games_played,
                    diff_mode=diff_mode,
                    feature_blocks=feature_blocks,
                    include_per=include_per,
                    name=name,
                    selected=selected
                )
            else:  # points
                config_id, config = config_manager.create_points_config(
                    model_type=model_type,
                    features=actual_features,
                    target=target,
                    alpha=alpha,
                    l1_ratio=l1_ratio,
                    begin_year=begin_year,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    min_games_played=min_games_played,
                    diff_mode=diff_mode,
                    feature_blocks=feature_blocks,
                    include_per=include_per,
                    name=name,
                    selected=selected
                )

            return encode_tool_output({
                'config_id': config_id,
                'config_hash': config.get('config_hash'),
                'config_type': config_type,
                'name': config.get('name'),
                'model_type': model_type,
                'feature_count': len(actual_features),
                'is_trained': bool(config.get('model_artifact_path')),
                'selected': config.get('selected', False),
                'message': f"Config created/found with hash {config.get('config_hash', '')[:8]}"
            })

        except Exception as e:
            return encode_tool_output({
                'error': f"Failed to create config: {str(e)}",
                'config_id': None
            })

    def run_experiment_from_config(
        self,
        config_id: str,
        config_type: str = 'classifier',
        modifications: Dict = None,
        link_to_config: bool = True
    ) -> Dict:
        """
        Run an experiment using an existing config as the base.

        This converts the config to an experiment spec, applies any modifications,
        and runs the experiment. Optionally links results back to the config.

        Args:
            config_id: MongoDB ObjectId of the config to use as base
            config_type: 'classifier' or 'points'
            modifications: Optional dict of modifications to apply to the spec.
                          Keys can include: 'model', 'features', 'splits', etc.
            link_to_config: Whether to link run results back to the config

        Returns:
            Dict with run results including run_id, metrics, and artifacts
        """
        import json

        # Get experiment spec from config
        spec_result = self.config_to_experiment_spec(config_id, config_type)
        if isinstance(spec_result, str):
            spec_result = json.loads(spec_result)

        if 'error' in spec_result:
            return encode_tool_output(spec_result)

        experiment_spec = spec_result.get('experiment_spec')
        if not experiment_spec:
            return encode_tool_output({'error': 'Failed to convert config to experiment spec'})

        # Apply modifications if provided
        if modifications:
            for key, value in modifications.items():
                if key in experiment_spec:
                    if isinstance(value, dict) and isinstance(experiment_spec[key], dict):
                        experiment_spec[key].update(value)
                    else:
                        experiment_spec[key] = value
                else:
                    experiment_spec[key] = value

        # Run experiment using experiment_runner
        from nba_app.agents.tools.experiment_runner import ExperimentRunner

        experiment_runner = ExperimentRunner(db=self.db)
        # Use a default session_id for config-based runs
        session_id = f"config_run_{config_id[:8]}"

        try:
            result = experiment_runner.run_experiment(experiment_spec, session_id)

            # Link results back to config if requested
            if link_to_config and result.get('run_id'):
                from nba_app.core.services.config_manager import ModelConfigManager
                config_manager = ModelConfigManager(self.db)

                config_manager.link_run_to_config(
                    config_id=config_id,
                    run_id=result['run_id'],
                    config_type=config_type,
                    metrics=result.get('metrics'),
                    artifacts=result.get('artifacts'),
                    dataset_id=result.get('dataset_id'),
                    training_csv=result.get('artifacts', {}).get('dataset_path')
                )
                result['linked_to_config'] = config_id

            return encode_tool_output(result)

        except Exception as e:
            return encode_tool_output({
                'error': f"Experiment failed: {str(e)}",
                'config_id': config_id
            })

