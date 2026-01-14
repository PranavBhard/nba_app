"""
Experiment Runner Tool - Runs complete experiments (build dataset, train, evaluate, store)
"""

import sys
import os
import json
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Optional
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss, roc_auc_score

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.cli.train import (
    create_model_with_c,
    evaluate_model_combo,
    evaluate_model_combo_with_calibration,
    read_csv_safe
)
from nba_app.cli.points_regression import PointsRegressionTrainer
from nba_app.agents.tools.dataset_builder import DatasetBuilder
from nba_app.agents.tools.run_tracker import RunTracker
from nba_app.agents.schemas.experiment_config import ExperimentConfig
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class ExperimentRunner:
    """Runs complete experiments"""
    
    def __init__(self, db=None):
        """
        Initialize ExperimentRunner.
        
        Args:
            db: MongoDB database instance (optional)
        """
        if db is None:
            from nba_app.cli.Mongo import Mongo
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        self.dataset_builder = DatasetBuilder(db=self.db)
        self.run_tracker = RunTracker(db=self.db)
        
        # Set up artifacts directory for classifier models
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
        self.classifier_models_dir = os.path.join(parent_dir, 'model_output', 'classifier_models')
        os.makedirs(self.classifier_models_dir, exist_ok=True)
    
    def run_experiment(self, config: Dict, session_id: str) -> Dict:
        """
        Run a complete experiment.
        
        Args:
            config: Experiment configuration dict (validated against ExperimentConfig)
            session_id: Chat session ID
            
        Returns:
            Dict with:
                - run_id: Unique identifier
                - metrics: Evaluation metrics
                - diagnostics: Model diagnostics
                - artifacts: Paths to saved artifacts
                - dataset_id: Dataset identifier
        """
        # Validate config
        try:
            exp_config = ExperimentConfig(**config)
        except Exception as e:
            raise ValueError(f"Invalid experiment config: {e}")
        
        # Build dataset spec from experiment config
        # Apply default begin_year=2012 if not specified (2012 = 2012-2013 season)
        begin_year = exp_config.splits.begin_year if exp_config.splits.begin_year is not None else 2012
        
        dataset_spec = {
            'feature_blocks': exp_config.features.blocks,
            'individual_features': exp_config.features.features,
            'begin_year': begin_year,
            'min_games_played': exp_config.splits.min_games_played,
            'exclude_preseason': True,
            'include_per': exp_config.features.include_per,
            'diff_mode': exp_config.features.diff_mode,
            'point_model_id': exp_config.features.point_model_id
        }
        
        # Build dataset
        dataset_result = self.dataset_builder.build_dataset(dataset_spec)
        dataset_id = dataset_result['dataset_id']
        csv_path = dataset_result['csv_path']
        dropped_features = dataset_result.get('dropped_features', [])
        
        # Route to appropriate experiment type
        if exp_config.task == 'points_regression':
            result = self._run_points_experiment(exp_config, config, dataset_id, csv_path, session_id)
        else:
            result = self._run_classification_experiment(exp_config, config, dataset_id, csv_path, session_id)
        
        # Pass through dropped_features if any were dropped
        if dropped_features:
            result['dropped_features'] = dropped_features
        
        return result
    
    def _run_classification_experiment(self, exp_config, config, dataset_id, csv_path, session_id):
        """Run binary classification experiment"""
        # Create run
        run_id = self.run_tracker.create_run(
            config=config,
            dataset_id=dataset_id,
            model_type=exp_config.model.type,
            session_id=session_id,
            baseline=False
        )
        
        # Update status
        self.run_tracker.update_run(run_id, status='running')
        
        try:
            # Load data
            df = read_csv_safe(csv_path)
            
            # Check if CSV is empty
            if df.empty:
                raise ValueError(f"CSV file {csv_path} is empty. No training data available.")
            
            meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
            if 'game_id' in df.columns:
                meta_cols.append('game_id')
            
            # Target columns: HomeWon (required), home_points and away_points (optional, for points regression)
            target_cols = ['HomeWon']
            if 'home_points' in df.columns:
                target_cols.append('home_points')
            if 'away_points' in df.columns:
                target_cols.append('away_points')
            
            # Check if target column exists
            if 'HomeWon' not in df.columns:
                available_cols = list(df.columns)
                raise ValueError(
                    f"Target column 'HomeWon' not found in CSV. "
                    f"Available columns: {available_cols}. "
                    f"CSV file: {csv_path}"
                )
            
            # Exclude metadata, target columns, and non-margin prediction columns from features
            excluded_cols = meta_cols + target_cols
            # Exclude other prediction columns (pred_margin is included as a feature by default)
            other_pred_cols = ['pred_home_points', 'pred_away_points', 'pred_point_total']
            excluded_cols.extend([c for c in other_pred_cols if c in df.columns])
            
            feature_cols = [c for c in df.columns if c not in excluded_cols]
            
            # Validate that we have features
            if len(feature_cols) == 0:
                available_cols = list(df.columns)
                raise ValueError(
                    f"No feature columns found in CSV. "
                    f"CSV has {len(df)} rows but only metadata columns: {available_cols}. "
                    f"This likely means the dataset was created without any features, or all features were filtered out. "
                    f"CSV file: {csv_path}. "
                    f"Dataset ID: {dataset_id}. "
                    f"Check the dataset_builder logs to see why features are missing."
                )
            
            X = df[feature_cols].values
            y = df['HomeWon'].values
            
            # Preprocess
            if exp_config.preprocessing.scaler == 'standard':
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
            else:
                X_scaled = X
                scaler = None
            
            # Evaluate model
            if exp_config.splits.type == 'year_based_calibration':
                # Use time-based calibration evaluation
                metrics = evaluate_model_combo_with_calibration(
                    df=df,
                    X_scaled=X_scaled,
                    y=y,
                    model_type=exp_config.model.type,
                    c_value=exp_config.model.c_value,
                    calibration_method=exp_config.calibration_method,
                    calibration_years=exp_config.splits.calibration_years,
                    evaluation_year=exp_config.splits.evaluation_year
                )
            else:
                # Use time-series cross-validation
                n_splits = exp_config.splits.n_splits if exp_config.splits.n_splits else 5
                metrics = evaluate_model_combo(
                    X=X_scaled,
                    y=y,
                    model_type=exp_config.model.type,
                    c_value=exp_config.model.c_value,
                    n_splits=n_splits
                )
            
            # Calculate additional metrics if possible and save model
            model = None
            feature_importances = {}
            try:
                # Train final model for feature importance and saving
                model = create_model_with_c(exp_config.model.type, exp_config.model.c_value)
                model.fit(X_scaled, y)
                
                # Get feature importances if available
                if hasattr(model, 'feature_importances_'):
                    importances = model.feature_importances_
                    feature_importances = dict(zip(feature_cols, importances.tolist()))
                    # Sort by importance
                    feature_importances = dict(sorted(
                        feature_importances.items(),
                        key=lambda x: x[1],
                        reverse=True
                    ))
                elif hasattr(model, 'coef_'):
                    # For linear models, use absolute coefficients
                    coef = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
                    feature_importances = dict(zip(feature_cols, np.abs(coef).tolist()))
                    feature_importances = dict(sorted(
                        feature_importances.items(),
                        key=lambda x: x[1],
                        reverse=True
                    ))
            except Exception as e:
                feature_importances = {}
            
            # Save model artifacts
            model_artifacts = {}
            if model is not None:
                try:
                    model_artifacts = self._save_classification_model(
                        run_id=run_id,
                        model=model,
                        scaler=scaler,
                        feature_names=feature_cols
                    )
                except Exception as e:
                    print(f"Warning: Failed to save model artifacts: {e}")
            
            # Prepare diagnostics
            diagnostics = {
                'feature_importances': feature_importances,
                'n_features': len(feature_cols),
                'n_samples': len(y),
                'feature_names': feature_cols[:20]  # Top 20 for preview
            }
            
            # Prepare artifacts
            artifacts = {
                'dataset_path': csv_path,
                'model_type': exp_config.model.type,
                **model_artifacts  # Include model paths
            }
            
            # Update run with results
            self.run_tracker.update_run(
                run_id=run_id,
                metrics=metrics,
                diagnostics=diagnostics,
                artifacts=artifacts,
                status='completed'
            )
            
            return {
                'run_id': run_id,
                'metrics': metrics,
                'diagnostics': diagnostics,
                'artifacts': artifacts,
                'dataset_id': dataset_id
            }
        
        except Exception as e:
            # Update run with error
            self.run_tracker.update_run(
                run_id=run_id,
                status='failed',
                diagnostics={'error': str(e)}
            )
            raise
    
    def _save_classification_model(self, run_id: str, model, scaler, feature_names: list) -> Dict[str, str]:
        """
        Save classification model, scaler, and feature names to disk.
        
        Args:
            run_id: Run identifier
            model: Trained sklearn model
            scaler: Fitted StandardScaler (or None)
            feature_names: List of feature names
            
        Returns:
            Dict with paths to saved artifacts
        """
        model_dir = os.path.join(self.classifier_models_dir, run_id)
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        feature_names_path = os.path.join(model_dir, 'feature_names.json')
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Save scaler (even if None, for consistency)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        # Save feature names
        with open(feature_names_path, 'w') as f:
            json.dump(feature_names, f)
        
        return {
            'model_path': model_path,
            'scaler_path': scaler_path,
            'feature_names_path': feature_names_path
        }
    
    def _load_classification_model(self, run_id: str):
        """
        Load classification model, scaler, and feature names from disk.
        
        Args:
            run_id: Run identifier
            
        Returns:
            Tuple of (model, scaler, feature_names)
        """
        model_dir = os.path.join(self.classifier_models_dir, run_id)
        model_path = os.path.join(model_dir, 'model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        feature_names_path = os.path.join(model_dir, 'feature_names.json')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
        if not os.path.exists(feature_names_path):
            raise FileNotFoundError(f"Feature names file not found: {feature_names_path}")
        
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # Load feature names
        with open(feature_names_path, 'r') as f:
            feature_names = json.load(f)
        
        return model, scaler, feature_names
    
    def _run_points_experiment(self, exp_config, config, dataset_id, csv_path, session_id):
        """Run points regression experiment"""
        # Create run
        run_id = self.run_tracker.create_run(
            config=config,
            dataset_id=dataset_id,
            model_type=exp_config.points_model.type,
            session_id=session_id,
            baseline=False
        )
        
        # Update status
        self.run_tracker.update_run(run_id, status='running')
        
        try:
            # Load data
            df = read_csv_safe(csv_path)
            
            # Check if CSV is empty
            if df.empty:
                raise ValueError(f"CSV file {csv_path} is empty. No training data available.")
            
            meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
            if 'game_id' in df.columns:
                meta_cols.append('game_id')
            target_cols = ['home_points', 'away_points']
            
            # Check if target columns exist
            missing_targets = [col for col in target_cols if col not in df.columns]
            if missing_targets:
                available_cols = list(df.columns)
                raise ValueError(
                    f"Target columns {missing_targets} not found in CSV. "
                    f"Available columns: {available_cols}. "
                    f"CSV file: {csv_path}"
                )
            
            # Filter out rows with missing/invalid points (0 or NaN)
            initial_count = len(df)
            df = df[(df['home_points'] > 0) & (df['away_points'] > 0)]
            df = df.dropna(subset=['home_points', 'away_points'])
            filtered_count = len(df)
            
            if filtered_count == 0:
                raise ValueError(
                    f"No valid rows with home_points > 0 and away_points > 0. "
                    f"Initial rows: {initial_count}, After filtering: {filtered_count}"
                )
            
            if filtered_count < initial_count:
                print(f"Warning: Filtered out {initial_count - filtered_count} rows with invalid points")
            
            feature_cols = [c for c in df.columns if c not in meta_cols + target_cols + ['HomeWon']]
            
            # Validate that we have features
            if len(feature_cols) == 0:
                available_cols = list(df.columns)
                raise ValueError(
                    f"No feature columns found in CSV. "
                    f"CSV has {len(df)} rows but only metadata/target columns: {available_cols}. "
                    f"CSV file: {csv_path}. "
                    f"Dataset ID: {dataset_id}."
                )
            
            # Create PointsRegressionTrainer
            trainer = PointsRegressionTrainer()
            
            # Train model
            model_type = exp_config.points_model.type
            target = getattr(exp_config.points_model, 'target', 'home_away')  # Default to 'home_away' for backward compatibility
            
            # Extract time-based calibration parameters from splits config
            use_time_calibration = False
            calibration_years = None
            evaluation_year = None
            begin_year = None
            
            if exp_config.splits.type == 'year_based_calibration':
                use_time_calibration = True
                calibration_years = exp_config.splits.calibration_years if exp_config.splits.calibration_years else [2023]
                evaluation_year = exp_config.splits.evaluation_year if exp_config.splits.evaluation_year else 2024
                begin_year = exp_config.splits.begin_year if exp_config.splits.begin_year else 2012
            
            # Extract model_kwargs from points_model config
            model_kwargs = {}
            if hasattr(exp_config.points_model, 'alpha') and exp_config.points_model.alpha:
                model_kwargs['alpha'] = exp_config.points_model.alpha
            if hasattr(exp_config.points_model, 'l1_ratio') and exp_config.points_model.l1_ratio:
                model_kwargs['l1_ratio'] = exp_config.points_model.l1_ratio
            if hasattr(exp_config.points_model, 'n_estimators') and exp_config.points_model.n_estimators:
                model_kwargs['n_estimators'] = exp_config.points_model.n_estimators
            if hasattr(exp_config.points_model, 'max_depth') and exp_config.points_model.max_depth:
                model_kwargs['max_depth'] = exp_config.points_model.max_depth
            if hasattr(exp_config.points_model, 'learning_rate') and exp_config.points_model.learning_rate:
                model_kwargs['learning_rate'] = exp_config.points_model.learning_rate
            
            # Map model types - pass target parameter and calibration parameters to trainer.train()
            if model_type == 'Ridge':
                alphas = model_kwargs.get('alpha')
                alphas = [alphas] if alphas else None
                train_result = trainer.train(
                    model_type='Ridge',
                    alphas=alphas,
                    training_csv=csv_path,
                    selected_features=feature_cols,
                    target=target,
                    use_time_calibration=use_time_calibration,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    begin_year=begin_year,
                    **model_kwargs
                )
            elif model_type == 'ElasticNet':
                alphas = model_kwargs.get('alpha')
                alphas = [alphas] if alphas else None
                l1_ratios = [model_kwargs.get('l1_ratio', 0.5)]
                train_result = trainer.train(
                    model_type='ElasticNet',
                    alphas=alphas,
                    l1_ratios=l1_ratios,
                    training_csv=csv_path,
                    selected_features=feature_cols,
                    target=target,
                    use_time_calibration=use_time_calibration,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    begin_year=begin_year,
                    **{k: v for k, v in model_kwargs.items() if k != 'alpha' and k != 'l1_ratio'}
                )
            elif model_type == 'RandomForest':
                n_estimators = model_kwargs.get('n_estimators', 100)
                max_depth = model_kwargs.get('max_depth', None)
                train_result = trainer.train(
                    model_type='RandomForest',
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    training_csv=csv_path,
                    selected_features=feature_cols,
                    target=target,
                    use_time_calibration=use_time_calibration,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    begin_year=begin_year,
                    **{k: v for k, v in model_kwargs.items() if k not in ['n_estimators', 'max_depth']}
                )
            elif model_type == 'XGBoost':
                n_estimators = model_kwargs.get('n_estimators', 100)
                max_depth = model_kwargs.get('max_depth', 6)
                learning_rate = model_kwargs.get('learning_rate', 0.1)
                train_result = trainer.train(
                    model_type='XGBoost',
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    learning_rate=learning_rate,
                    training_csv=csv_path,
                    selected_features=feature_cols,
                    target=target,
                    use_time_calibration=use_time_calibration,
                    calibration_years=calibration_years,
                    evaluation_year=evaluation_year,
                    begin_year=begin_year,
                    **{k: v for k, v in model_kwargs.items() if k not in ['n_estimators', 'max_depth', 'learning_rate']}
                )
            else:
                raise ValueError(f"Unsupported points regression model type: {model_type}")
            
            # Extract metrics from training result
            # The train() method returns metrics nested under 'final_metrics'
            final_metrics = train_result.get('final_metrics', {})
            target = train_result.get('target', 'home_away')  # Get target from train_result
            
            # Handle metrics based on target type
            if target == 'margin':
                # Margin-only models: only margin metrics
                metrics = {
                    'margin_mae': final_metrics.get('margin_mae', 0.0),
                    'margin_rmse': final_metrics.get('margin_rmse', 0.0),
                    'margin_r2': final_metrics.get('margin_r2', 0.0),
                }
            else:
                # Home/away models: all metrics
                metrics = {
                    'home_mae': final_metrics.get('home_mae', 0.0),
                    'home_rmse': final_metrics.get('home_rmse', 0.0),
                    'home_r2': final_metrics.get('home_r2', 0.0),
                    'home_mape': final_metrics.get('home_mape', 0.0),
                    'away_mae': final_metrics.get('away_mae', 0.0),
                    'away_rmse': final_metrics.get('away_rmse', 0.0),
                    'away_r2': final_metrics.get('away_r2', 0.0),
                    'away_mape': final_metrics.get('away_mape', 0.0),
                    'home_mae_mean': (final_metrics.get('home_mae', 0.0) + final_metrics.get('away_mae', 0.0)) / 2,
                    'away_mae_mean': (final_metrics.get('home_mae', 0.0) + final_metrics.get('away_mae', 0.0)) / 2,
                    # Margin metrics (home_points - away_points)
                    'margin_mae': final_metrics.get('diff_mae', 0.0),
                    'margin_rmse': final_metrics.get('diff_rmse', 0.0),
                    'margin_r2': final_metrics.get('diff_r2', 0.0),
                    # Total metrics (home_points + away_points)
                    'total_mae': final_metrics.get('total_mae', 0.0),
                    'total_rmse': final_metrics.get('total_rmse', 0.0),
                    'total_r2': final_metrics.get('total_r2', 0.0),
                }
            
            # Generate predictions for all games in dataset and cache them
            # OPTIMIZATION: Use vectorized prediction instead of row-by-row
            from nba_app.cli.point_prediction_cache import PointPredictionCache
            cache = PointPredictionCache(db=self.db)
            
            # Generate predictions for all games in dataset using the trained model
            # We need to load the CSV again and prepare features for prediction
            # The trainer already has the model and scaler loaded from training
            print(f"Generating predictions for {len(df)} games...")
            
            # Prepare features for prediction (using same scaler from training)
            X_pred = df[feature_cols].values
            X_pred_scaled = trainer.scaler.transform(X_pred)
            
            # Handle prediction generation based on target type
            df_reset = df.reset_index(drop=True)
            
            if target == 'margin':
                # Margin-only model: predict margin directly
                pred_margin_all = trainer.model.predict(X_pred_scaled)
                # Clamp to reasonable range (typical NBA margin: -50 to +50)
                pred_margin_all = np.clip(pred_margin_all, -60, 60)
                
                # Build predictions list for margin-only model (using positional indexing)
                predictions = []
                for pos_idx, row in df_reset.iterrows():
                    game_id = row.get('game_id', '') if 'game_id' in row else ''
                    predictions.append({
                        'game_id': game_id,
                        'pred_home_points': None,  # Not predicted for margin-only
                        'pred_away_points': None,  # Not predicted for margin-only
                        'pred_margin': float(pred_margin_all[pos_idx]),
                        'year': int(row['Year']),
                        'month': int(row['Month']),
                        'day': int(row['Day']),
                        'home_team': row['Home'],
                        'away_team': row['Away']
                    })
            else:
                # Home/away models: predict both separately
                pred_home_all = trainer.model['home'].predict(X_pred_scaled)
                pred_away_all = trainer.model['away'].predict(X_pred_scaled)
                
                # Clamp to reasonable range (vectorized)
                pred_home_all = np.clip(pred_home_all, 0, 200)
                pred_away_all = np.clip(pred_away_all, 0, 200)
                
                # Build predictions list (using positional indexing)
                predictions = []
                for pos_idx, row in df_reset.iterrows():
                    game_id = row.get('game_id', '') if 'game_id' in row else ''
                    predictions.append({
                        'game_id': game_id,
                        'pred_home_points': float(pred_home_all[pos_idx]),
                        'pred_away_points': float(pred_away_all[pos_idx]),
                        'year': int(row['Year']),
                        'month': int(row['Month']),
                        'day': int(row['Day']),
                        'home_team': row['Home'],
                        'away_team': row['Away']
                    })
            
            # Cache predictions (batch insert for efficiency)
            model_id = f"points_model_{run_id}"
            print(f"Caching {len(predictions)} predictions to MongoDB...")
            cached_count = cache.cache_predictions(
                model_id=model_id,
                predictions=predictions,
                metadata={
                    'run_id': run_id,
                    'model_type': model_type,
                    'config': config,
                    'dataset_id': dataset_id
                }
            )
            print(f"Cached {cached_count} point predictions with model_id: {model_id}")
            
            # Calculate feature importances (coefficients for linear models, feature_importances_ for tree models)
            feature_importances = {}
            try:
                if target == 'margin':
                    # Margin-only model: single model
                    model = trainer.model
                    if hasattr(model, 'coef_'):
                        # Linear model (Ridge, ElasticNet) - use absolute coefficients
                        coef = model.coef_
                        if len(coef.shape) > 1:
                            coef = coef[0]
                        feature_importances = dict(zip(feature_cols, np.abs(coef).tolist()))
                    elif hasattr(model, 'feature_importances_'):
                        # Tree-based model (RandomForest, XGBoost) - use feature importances
                        feature_importances = dict(zip(feature_cols, model.feature_importances_.tolist()))
                else:
                    # Home/away models: combine importances from both models
                    home_model = trainer.model['home']
                    away_model = trainer.model['away']
                    
                    if hasattr(home_model, 'coef_'):
                        # Linear model (Ridge, ElasticNet) - use absolute coefficients
                        home_coef = home_model.coef_
                        away_coef = away_model.coef_
                        # Handle 1D or 2D coefficient arrays
                        if len(home_coef.shape) > 1:
                            home_coef = home_coef[0]
                        if len(away_coef.shape) > 1:
                            away_coef = away_coef[0]
                        # Average absolute coefficients for combined importance
                        combined_importance = (np.abs(home_coef) + np.abs(away_coef)) / 2
                        feature_importances = dict(zip(feature_cols, combined_importance.tolist()))
                    elif hasattr(home_model, 'feature_importances_'):
                        # Tree-based model (RandomForest, XGBoost) - use feature importances
                        home_importance = home_model.feature_importances_
                        away_importance = away_model.feature_importances_
                        # Average feature importances for combined importance
                        combined_importance = (home_importance + away_importance) / 2
                        feature_importances = dict(zip(feature_cols, combined_importance.tolist()))
                
                # Sort by importance
                if feature_importances:
                    feature_importances = dict(sorted(
                        feature_importances.items(),
                        key=lambda x: x[1],
                        reverse=True
                    ))
            except Exception as e:
                print(f"Warning: Could not calculate feature importances: {e}")
                import traceback
                traceback.print_exc()
                feature_importances = {}
            
            # Prepare diagnostics
            # Get n_samples from training results or dataframe
            n_samples = train_result.get('n_samples', len(df))
            
            # Extract selected alpha and alphas tested for reporting
            selected_alpha = train_result.get('selected_alpha')
            alphas_tested = train_result.get('alphas_tested')
            
            diagnostics = {
                'n_features': len(feature_cols),
                'n_samples': n_samples,
                'feature_names': feature_cols[:20],  # Top 20 for preview
                'point_model_id': model_id,
                'cached_predictions': cached_count,
                'feature_importances': feature_importances,  # Add feature importances for points regression
                'selected_alpha': selected_alpha,  # Selected alpha value (if Ridge model)
                'alphas_tested': alphas_tested  # List of alphas tested (if multiple)
            }
            
            # Prepare artifacts
            artifacts = {
                'dataset_path': csv_path,
                'model_type': model_type,
                'point_model_id': model_id,
                'selected_alpha': selected_alpha,  # Include selected alpha in artifacts for easy access
                'alphas_tested': alphas_tested
            }
            
            # Update run with results
            self.run_tracker.update_run(
                run_id=run_id,
                metrics=metrics,
                diagnostics=diagnostics,
                artifacts=artifacts,
                status='completed'
            )
            
            return {
                'run_id': run_id,
                'metrics': metrics,
                'diagnostics': diagnostics,
                'artifacts': artifacts,
                'dataset_id': dataset_id,
                'point_model_id': model_id
            }
        
        except Exception as e:
            # Update run with error
            self.run_tracker.update_run(
                run_id=run_id,
                status='failed',
                diagnostics={'error': str(e)}
            )
            raise

