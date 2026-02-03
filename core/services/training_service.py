"""
Training Service - Thin orchestration layer for CLI training scripts.

Coordinates existing components:
- ModelConfigManager: Config creation and management
- ExperimentRunner: Training execution
- StackingTrainer: Ensemble model training
- ClassifierConfigRepository: Config data access
"""

import uuid
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from bson import ObjectId

if TYPE_CHECKING:
    from nba_app.core.league_config import LeagueConfig


# Model type aliases for CLI convenience
MODEL_TYPE_ALIASES = {
    'LR': 'LogisticRegression',
    'GB': 'GradientBoosting',
    'SVM': 'SVM',
}


class TrainingService:
    """
    Thin orchestration layer for model training operations.

    Coordinates existing core components for CLI training workflows.
    This is NOT a replacement for existing logic - it simply wires together
    existing functionality for CLI use.
    """

    def __init__(self, league: Optional["LeagueConfig"] = None, db=None):
        """
        Initialize TrainingService.

        Args:
            league: LeagueConfig instance for league-specific operations
            db: MongoDB database instance (optional, creates if not provided)
        """
        # Lazy imports to avoid circular dependencies
        from nba_app.core.mongo import Mongo
        from nba_app.core.data import ClassifierConfigRepository, ExperimentRunsRepository
        from nba_app.core.services.config_manager import ModelConfigManager
        from nba_app.agents.tools.experiment_runner import ExperimentRunner
        from nba_app.agents.tools.stacking_tool import StackingTrainer
        from nba_app.agents.tools.run_tracker import RunTracker

        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db

        self.league = league

        # Initialize components with league awareness
        self._classifier_repo = ClassifierConfigRepository(self.db, league=league)
        self._runs_repo = ExperimentRunsRepository(self.db, league=league)
        self._config_manager = ModelConfigManager(self.db, league=league)
        self._experiment_runner = ExperimentRunner(db=self.db, league=league)
        self._stacking_trainer = StackingTrainer(db=self.db, league=league)
        self._run_tracker = RunTracker(db=self.db, league=league)

    def resolve_model(self, name_or_id: str) -> Optional[Dict]:
        """
        Resolve a model by name OR MongoDB _id.

        Args:
            name_or_id: Model name (string) or MongoDB ObjectId (24-char hex)

        Returns:
            Model config dict or None if not found
        """
        # 1. Try as ObjectId (24-char hex string)
        if len(name_or_id) == 24:
            try:
                config = self._classifier_repo.find_one({'_id': ObjectId(name_or_id)})
                if config:
                    config['_id'] = str(config['_id'])
                    return config
            except Exception:
                pass  # Not a valid ObjectId, try as name

        # 2. Try as name
        config = self._classifier_repo.find_one({'name': name_or_id})
        if config:
            config['_id'] = str(config['_id'])
            return config

        return None

    def resolve_model_type(self, model_type: str) -> str:
        """
        Resolve model type alias to full name.

        Args:
            model_type: Model type or alias (e.g., 'LR', 'GB')

        Returns:
            Full model type name (e.g., 'LogisticRegression')
        """
        return MODEL_TYPE_ALIASES.get(model_type.upper(), model_type)

    def train_base_model(
        self,
        model_type: str,
        features: List[str],
        train_seasons: List[int],
        calibration_seasons: List[int],
        evaluation_season: int,
        c_value: float = 0.1,
        calibration_method: str = 'sigmoid',
        name: Optional[str] = None,
        min_games_played: int = 20,
        include_injuries: bool = False,
        use_master: bool = True,
    ) -> Dict:
        """
        Train a base classifier model.

        Args:
            model_type: Model type ('LogisticRegression', 'GradientBoosting', etc.)
            features: List of feature names
            train_seasons: List of training season years (begin_year values)
            calibration_seasons: List of calibration season years
            evaluation_season: Evaluation season year
            c_value: Regularization parameter (for LR, SVM)
            calibration_method: 'sigmoid' or 'isotonic'
            name: Optional model name
            min_games_played: Minimum games filter
            include_injuries: Include injury features
            use_master: Use master training CSV

        Returns:
            Dict with config_id, run_id, metrics, feature_importances
        """
        # Resolve model type alias
        model_type = self.resolve_model_type(model_type)

        # Determine begin_year from train_seasons
        begin_year = min(train_seasons) if train_seasons else 2012

        # Create or get config via ModelConfigManager
        config_id, config = self._config_manager.create_classifier_config(
            model_type=model_type,
            features=features,
            c_value=c_value,
            use_time_calibration=True,
            calibration_method=calibration_method,
            begin_year=begin_year,
            calibration_years=calibration_seasons,
            evaluation_year=evaluation_season,
            min_games_played=min_games_played,
            include_injuries=include_injuries,
            use_master=use_master,
            name=name,
        )

        # Build model config - only include c_value for models that support it
        model_config = {'type': model_type}
        if model_type in ('LogisticRegression', 'SVM'):
            model_config['c_value'] = c_value

        # Build experiment config for ExperimentRunner
        experiment_config = {
            'task': 'binary_home_win',
            'model': model_config,
            'features': {
                'blocks': [],
                'features': features,
                'include_per': True,
                'diff_mode': 'home_minus_away',
                'point_model_id': None,
            },
            'splits': {
                'type': 'year_based_calibration',
                'begin_year': begin_year,
                'calibration_years': calibration_seasons,
                'evaluation_year': evaluation_season,
                'min_games_played': min_games_played,
            },
            'preprocessing': {
                'scaler': 'standard',
            },
            'calibration_method': calibration_method,
        }

        # Generate a CLI session ID
        session_id = f"cli-{uuid.uuid4().hex[:8]}"

        # Run the experiment
        result = self._experiment_runner.run_experiment(experiment_config, session_id)

        # Extract F-scores and feature importances from diagnostics
        diagnostics = result.get('diagnostics', {})
        f_scores = diagnostics.get('f_scores', {})
        feature_importances = diagnostics.get('feature_importances', {})

        # Link run to config (including features, F-scores, and model importances)
        self._config_manager.link_run_to_config(
            config_id=config_id,
            run_id=result['run_id'],
            config_type='classifier',
            metrics=result.get('metrics'),
            artifacts=result.get('artifacts'),
            dataset_id=result.get('dataset_id'),
            training_csv=result.get('artifacts', {}).get('dataset_path'),
            f_scores=f_scores,
            feature_importances=feature_importances,
            features=features,
        )

        return {
            'config_id': config_id,
            'run_id': result['run_id'],
            'metrics': result.get('metrics', {}),
            'f_scores': f_scores,
            'feature_importances': feature_importances,
            'n_features': diagnostics.get('n_features', 0),
            'n_samples': diagnostics.get('n_samples', 0),
        }

    def train_ensemble(
        self,
        meta_model_type: str,
        base_model_names_or_ids: List[str],
        meta_c_value: float = 0.1,
        extra_features: Optional[List[str]] = None,
        stacking_mode: str = 'informed',
        use_disagree: bool = False,
        use_conf: bool = False,
    ) -> Dict:
        """
        Train an ensemble (stacking) model.

        IMPORTANT: Temporal parameters (begin_year, calibration_years, evaluation_year)
        are derived from the base models to ensure consistency. All base models must
        have identical temporal configurations.

        Args:
            meta_model_type: Meta-model type ('LogisticRegression', 'GradientBoosting')
            base_model_names_or_ids: List of base model names or MongoDB _ids
            meta_c_value: C-value for meta-model (if applicable)
            extra_features: Additional features to include in meta-model
            stacking_mode: 'naive' or 'informed'
            use_disagree: Include disagreement features
            use_conf: Include confidence features

        Returns:
            Dict with run_id, metrics, base_models summary
        """
        # Resolve model type alias
        meta_model_type = self.resolve_model_type(meta_model_type)

        # Resolve base models to config IDs and validate temporal consistency
        base_config_ids = []
        base_models_info = []
        ref_begin_year = None
        ref_calibration_years = None
        ref_evaluation_year = None

        for i, name_or_id in enumerate(base_model_names_or_ids):
            config = self.resolve_model(name_or_id)
            if not config:
                raise ValueError(f"Base model not found: {name_or_id}")

            base_config_ids.append(config['_id'])
            base_models_info.append({
                'name': config.get('name'),
                'id': config['_id'],
                'model_type': config.get('model_type'),
            })

            # Extract temporal parameters from config
            begin_year = config.get('begin_year')
            calibration_years = config.get('calibration_years', [])
            evaluation_year = config.get('evaluation_year')

            if i == 0:
                # First model sets the reference
                ref_begin_year = begin_year
                ref_calibration_years = calibration_years
                ref_evaluation_year = evaluation_year
            else:
                # Validate subsequent models match
                if begin_year != ref_begin_year:
                    raise ValueError(
                        f"Base model '{config.get('name')}' has begin_year={begin_year}, "
                        f"but first model has begin_year={ref_begin_year}. "
                        f"All base models must have identical temporal configurations."
                    )
                if calibration_years != ref_calibration_years:
                    raise ValueError(
                        f"Base model '{config.get('name')}' has calibration_years={calibration_years}, "
                        f"but first model has calibration_years={ref_calibration_years}. "
                        f"All base models must have identical temporal configurations."
                    )
                if evaluation_year != ref_evaluation_year:
                    raise ValueError(
                        f"Base model '{config.get('name')}' has evaluation_year={evaluation_year}, "
                        f"but first model has evaluation_year={ref_evaluation_year}. "
                        f"All base models must have identical temporal configurations."
                    )

        # Get reference config from first base model
        first_config = self.resolve_model(base_model_names_or_ids[0])

        # Build dataset spec DERIVED FROM base models (no overrides allowed)
        dataset_spec = {
            'begin_year': ref_begin_year,
            'calibration_years': ref_calibration_years,
            'evaluation_year': ref_evaluation_year,
            'min_games_played': first_config.get('min_games_played', 15),
        }

        # Generate a CLI session ID
        session_id = f"cli-ensemble-{uuid.uuid4().hex[:8]}"

        # Train stacked model
        result = self._stacking_trainer.train_stacked_model(
            dataset_spec=dataset_spec,
            session_id=session_id,
            base_config_ids=base_config_ids,
            meta_model_type=meta_model_type,
            meta_c_value=meta_c_value,
            stacking_mode=stacking_mode,
            meta_features=extra_features,
            use_disagree=use_disagree,
            use_conf=use_conf,
        )

        # Create ensemble config in model_config collection
        from datetime import datetime
        import hashlib

        # Generate config hash for deduplication
        hash_input = f"ensemble_{'_'.join(sorted(base_config_ids))}_{meta_model_type}"
        config_hash = f"ensemble_{hashlib.md5(hash_input.encode()).hexdigest()[:16]}"

        # Get max min_games_played from base models (Rule 3)
        min_games_values = []
        for name_or_id in base_model_names_or_ids:
            cfg = self.resolve_model(name_or_id)
            if cfg:
                min_games_values.append(cfg.get('min_games_played', 0) or 0)
        meta_min_games_played = max(min_games_values) if min_games_values else 20

        # Build ensemble config document
        ensemble_config = {
            'ensemble': True,
            'ensemble_type': 'stacking',
            'ensemble_models': base_config_ids,
            'ensemble_meta_features': extra_features or [],
            'ensemble_use_disagree': use_disagree,
            'ensemble_use_conf': use_conf,
            'model_type': meta_model_type,
            'best_c_value': meta_c_value if meta_model_type in ('LogisticRegression', 'SVM') else None,
            'features': [],  # Ensembles don't have traditional features
            'feature_count': 0,
            'name': f'Ensemble ({len(base_config_ids)} models) - {meta_model_type}',
            'selected': False,
            'use_master': True,
            'use_time_calibration': True,
            'calibration_method': first_config.get('calibration_method', 'sigmoid'),
            'begin_year': ref_begin_year,
            'calibration_years': ref_calibration_years,
            'evaluation_year': ref_evaluation_year,
            'min_games_played': meta_min_games_played,
            'include_injuries': False,
            'config_hash': config_hash,
            'run_id': result['run_id'],
            'ensemble_run_id': result['run_id'],
            'trained_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }

        # Add metrics from training result
        metrics = result.get('metrics', {})
        if metrics:
            ensemble_config['accuracy'] = metrics.get('accuracy_mean')
            ensemble_config['std_dev'] = metrics.get('accuracy_std')
            ensemble_config['log_loss'] = metrics.get('log_loss_mean')
            ensemble_config['brier_score'] = metrics.get('brier_mean')

        # Add artifact paths from training result
        artifacts = result.get('artifacts', {})
        if artifacts:
            ensemble_config['meta_model_path'] = artifacts.get('meta_model_path')
            ensemble_config['ensemble_config_path'] = artifacts.get('ensemble_config_path')

        # Upsert ensemble config (update if exists, insert if not)
        existing = self._classifier_repo.find_one({'config_hash': config_hash})
        if existing:
            # Update existing
            self._classifier_repo.update_one(
                {'_id': existing['_id']},
                {'$set': ensemble_config}
            )
            ensemble_id = str(existing['_id'])
        else:
            # Insert new
            insert_result = self._classifier_repo.insert_one(ensemble_config)
            ensemble_id = str(insert_result.inserted_id)

        return {
            'config_id': ensemble_id,
            'run_id': result['run_id'],
            'metrics': result.get('metrics', {}),
            'base_models': base_models_info,
            'diagnostics': result.get('diagnostics', {}),
        }

    def get_model_results(self, name_or_id: str) -> Optional[Dict]:
        """
        Get detailed model results by name or ID.

        Args:
            name_or_id: Model name or MongoDB _id

        Returns:
            Dict with config details, metrics, feature importances
        """
        config = self.resolve_model(name_or_id)
        if not config:
            return None

        is_ensemble = config.get('ensemble', False)

        result = {
            'config_id': config.get('_id'),
            'name': config.get('name'),
            'model_type': config.get('model_type'),
            'is_ensemble': is_ensemble,
            'features': config.get('features', []),
            'feature_count': config.get('feature_count', len(config.get('features', []))),
            'begin_year': config.get('begin_year'),
            'calibration_years': config.get('calibration_years', []),
            'evaluation_year': config.get('evaluation_year'),
            'c_value': config.get('best_c_value'),
            'calibration_method': config.get('calibration_method'),
        }

        # Get metrics from config (they're stored there after training)
        result['metrics'] = {
            'accuracy': config.get('accuracy'),
            'log_loss': config.get('log_loss'),
            'brier_score': config.get('brier_score'),
            'auc': config.get('auc'),
        }

        # For feature importances, look at the linked run
        run_id = config.get('run_id')
        if run_id:
            run = self._run_tracker.get_run(run_id)
            if run:
                diagnostics = run.get('diagnostics', {})
                result['feature_importances'] = diagnostics.get('feature_importances', {})
                # Update metrics from run if available
                run_metrics = run.get('metrics', {})
                if run_metrics:
                    result['metrics'] = {
                        'accuracy': run_metrics.get('accuracy_mean'),
                        'log_loss': run_metrics.get('log_loss_mean'),
                        'brier_score': run_metrics.get('brier_mean'),
                        'auc': run_metrics.get('auc_mean') or run_metrics.get('auc'),
                    }

        # For ensemble models, get base model details
        if is_ensemble:
            ensemble_models = config.get('ensemble_models', [])
            base_models = []
            for base_id in ensemble_models:
                base_config = self.resolve_model(base_id)
                if base_config:
                    base_run_id = base_config.get('run_id')
                    base_feature_importances = {}
                    if base_run_id:
                        base_run = self._run_tracker.get_run(base_run_id)
                        if base_run:
                            base_feature_importances = base_run.get('diagnostics', {}).get('feature_importances', {})

                    base_models.append({
                        'id': base_config.get('_id'),
                        'name': base_config.get('name'),
                        'model_type': base_config.get('model_type'),
                        'features': base_config.get('features', []),
                        'feature_importances': base_feature_importances,
                    })
            result['base_models'] = base_models

        return result

    def list_models(
        self,
        model_type: Optional[str] = None,
        ensemble_only: bool = False,
        trained_only: bool = False,
        limit: int = 50,
    ) -> List[Dict]:
        """
        List available models with optional filters.

        Args:
            model_type: Filter by model type
            ensemble_only: Only return ensemble models
            trained_only: Only return trained models
            limit: Maximum number of results

        Returns:
            List of model config summaries
        """
        if model_type:
            model_type = self.resolve_model_type(model_type)
            configs = self._classifier_repo.find_by_model_type(model_type)
        elif ensemble_only:
            configs = self._classifier_repo.find_ensembles()
        else:
            configs = self._classifier_repo.find_all(trained_only=trained_only, limit=limit)

        results = []
        for config in configs[:limit]:
            results.append({
                'id': str(config.get('_id')),
                'name': config.get('name'),
                'model_type': config.get('model_type'),
                'is_ensemble': config.get('ensemble', False),
                'accuracy': config.get('accuracy'),
                'trained': bool(config.get('model_artifact_path') or config.get('run_id')),
                'created_at': config.get('created_at'),
            })

        return results
