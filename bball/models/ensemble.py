"""
Ensemble Predictor with Shared Feature Generation.

This module provides an optimized ensemble prediction flow that:
1. Generates features ONCE using SharedFeatureGenerator
2. Uses cached sklearn models from ArtifactLoader
3. Distributes feature subsets to each base model
4. Combines predictions with the meta-model

This is significantly faster than the original approach which created
separate BballModel instances for each base model.
"""

import os
import re
import json
import pickle
import numpy as np
from typing import Dict, List, Optional, Tuple
from bson import ObjectId

from bball.models.artifact_loader import ArtifactLoader
from bball.features.generator import SharedFeatureGenerator, collect_unique_features


class EnsemblePredictor:
    """
    Fast ensemble prediction using shared feature generation and cached models.

    This class replaces the slow _predict_ensemble_with_player_config method
    in BballModel with an optimized version that:
    - Generates features once for all base models
    - Uses in-memory cached sklearn models
    - Minimizes redundant computation

    Usage:
        predictor = EnsemblePredictor(db, ensemble_config)
        result = predictor.predict(
            home_team="BOS",
            away_team="LAL",
            season="2024-2025",
            game_date="2025-01-15",
            player_filters=player_filters
        )
    """

    def __init__(self, db, ensemble_config: Dict, league=None):
        """
        Initialize the ensemble predictor.

        Args:
            db: MongoDB database connection
            ensemble_config: Ensemble configuration with:
                - ensemble_run_id: ID for loading meta-model artifacts
                - ensemble_models: List of base model config IDs
                - ensemble_meta_features: List of meta-feature names
                - meta_model_path: Path to meta-model pickle (optional)
                - ensemble_config_path: Path to ensemble config JSON (optional)
            league: Optional LeagueConfig for league-aware collection routing
        """
        self.db = db
        self.ensemble_config = ensemble_config
        self.league = league

        # Extract configuration
        self.ensemble_run_id = ensemble_config.get('ensemble_run_id')
        self.base_model_ids = ensemble_config.get('ensemble_models', [])
        self.meta_feature_names = ensemble_config.get('ensemble_meta_features', [])

        if not self.ensemble_run_id:
            raise ValueError("Ensemble config missing ensemble_run_id")
        if not self.base_model_ids or len(self.base_model_ids) < 2:
            raise ValueError("Ensemble config must have at least 2 base models")

        # Load base model configs and collect their features
        self.base_model_configs: List[Dict] = []
        self.base_model_features: List[List[str]] = []
        self._load_base_model_configs()

        # Collect all unique features needed (base model features + extra meta-features)
        self.all_features = collect_unique_features(
            self.base_model_features + ([self.meta_feature_names] if self.meta_feature_names else [])
        )

        # Initialize shared feature generator
        self.feature_generator = SharedFeatureGenerator(db, preload_venues=True, league=league)

        # Load meta-model, scaler, and config
        self.meta_model = None
        self.meta_scaler = None
        self.meta_config = None
        self._load_meta_model()

        # Cache for tracking player lists (for UI display)
        self._per_player_lists: Dict = {}
        self._injury_player_lists: Dict = {}

        # Prediction context (set via set_prediction_context)
        self._prediction_context = None

    def set_prediction_context(self, context) -> None:
        """
        Inject preloaded prediction context to avoid per-feature DB calls.

        Propagates the context to the internal SharedFeatureGenerator.

        Args:
            context: PredictionContext instance with preloaded data
        """
        print(f"[EnsemblePredictor] set_prediction_context called, context is {'not None' if context else 'None'}")
        self._prediction_context = context
        if self.feature_generator:
            self.feature_generator.set_prediction_context(context)
        else:
            print("[EnsemblePredictor] WARNING: feature_generator is None!")

    def _load_base_model_configs(self):
        """Load base model configurations from MongoDB."""
        # Use league-aware collection name
        if self.league:
            config_collection = self.league.collections.get('model_config_classifier', 'nba_model_config')
        else:
            config_collection = 'nba_model_config'

        for base_id in self.base_model_ids:
            base_id_str = str(base_id)
            try:
                config = self.db[config_collection].find_one({'_id': ObjectId(base_id_str)})
                if not config:
                    raise ValueError(f"Base model config not found: {base_id_str}")

                self.base_model_configs.append(config)

                # Get feature names from config or load from artifacts
                feature_names = config.get('feature_names')
                if not feature_names:
                    features_path = config.get('features_path')
                    if features_path and os.path.exists(features_path):
                        with open(features_path, 'r') as f:
                            feature_names = json.load(f)
                    else:
                        # Try to load via ArtifactLoader (will also cache the model)
                        _, _, feature_names = ArtifactLoader.create_model(config, use_artifacts=True)

                self.base_model_features.append(feature_names or [])

            except Exception as e:
                raise ValueError(f"Failed to load base model {base_id_str}: {e}")

    def _load_meta_model(self):
        """Load meta-model, scaler, and configuration from artifacts."""
        # Resolve artifact paths
        meta_model_path = self.ensemble_config.get('meta_model_path')
        meta_scaler_path = self.ensemble_config.get('meta_scaler_path')
        ensemble_cfg_path = self.ensemble_config.get('ensemble_config_path')

        if not meta_model_path or not ensemble_cfg_path:
            # Derive from run_id
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ensembles_dir = os.path.join(project_root, 'cli', 'models', 'ensembles')
            meta_model_path = meta_model_path or os.path.join(ensembles_dir, f'{self.ensemble_run_id}_meta_model.pkl')
            meta_scaler_path = meta_scaler_path or os.path.join(ensembles_dir, f'{self.ensemble_run_id}_meta_scaler.pkl')
            ensemble_cfg_path = ensemble_cfg_path or os.path.join(ensembles_dir, f'{self.ensemble_run_id}_ensemble_config.json')

        if not os.path.exists(meta_model_path):
            raise ValueError(f"Meta-model not found: {meta_model_path}")
        if not os.path.exists(ensemble_cfg_path):
            raise ValueError(f"Ensemble config not found: {ensemble_cfg_path}")

        with open(meta_model_path, 'rb') as f:
            self.meta_model = pickle.load(f)

        # Load scaler (may not exist for older ensembles trained without scaling)
        if meta_scaler_path and os.path.exists(meta_scaler_path):
            with open(meta_scaler_path, 'rb') as f:
                self.meta_scaler = pickle.load(f)

        with open(ensemble_cfg_path, 'r') as f:
            self.meta_config = json.load(f)

    def predict(
        self,
        home_team: str,
        away_team: str,
        season: str,
        game_date: str,
        player_filters: Dict,
        additional_features: Optional[Dict] = None,
        venue_guid: str = None
    ) -> Dict:
        """
        Make an ensemble prediction for a game.

        Args:
            home_team: Home team name
            away_team: Away team name
            season: Season string (e.g., '2024-2025')
            game_date: Game date string (YYYY-MM-DD)
            player_filters: Dict with team names as keys:
                {team: {'playing': [player_ids], 'starters': [player_ids]}}
            additional_features: Optional dict of pre-computed features (e.g., pred_margin)
            venue_guid: Optional venue GUID for travel feature calculations

        Returns:
            Dict with prediction results matching the standard API contract
        """
        # Validate player_filters
        if not player_filters:
            raise ValueError("player_filters is required for ensemble prediction")
        if home_team not in player_filters or 'playing' not in player_filters[home_team]:
            raise ValueError(f"player_filters must include '{home_team}' with 'playing' list")
        if away_team not in player_filters or 'playing' not in player_filters[away_team]:
            raise ValueError(f"player_filters must include '{away_team}' with 'playing' list")

        # STEP 1: Generate features ONCE for all base models
        all_feature_dict = self.feature_generator.generate_features(
            feature_names=self.all_features,
            home_team=home_team,
            away_team=away_team,
            season=season,
            game_date=game_date,
            player_filters=player_filters,
            additional_features=additional_features,
            venue_guid=venue_guid
        )

        # Store player lists for UI
        self._per_player_lists = self.feature_generator._per_player_lists.copy()
        self._injury_player_lists = self.feature_generator._injury_player_lists.copy()

        # STEP 2: Get predictions from each base model
        base_home_probs: Dict[str, float] = {}
        base_model_breakdowns: List[Dict] = []

        used_model_names = set()  # Track used names to avoid collisions
        for i, (config, feature_names) in enumerate(zip(self.base_model_configs, self.base_model_features)):
            base_id_str = str(self.base_model_ids[i])

            # Use config 'name' field if available (matches stacking_tool.py training convention)
            model_name = config.get('name')
            print(f"[EnsemblePredictor] Base model {i}: config_id={base_id_str}, name='{model_name}'")
            if model_name:
                # Sanitize name for use as column name (replace spaces/special chars with underscore)
                base_id_short = re.sub(r'[^a-zA-Z0-9_]', '_', model_name)
            else:
                # Fallback to first 8 chars of ObjectId
                base_id_short = base_id_str[:8]
            print(f"[EnsemblePredictor]   -> base_id_short='{base_id_short}', key will be 'p_{base_id_short}'")

            # Handle name collisions by appending a number
            original_name = base_id_short
            counter = 1
            while base_id_short in used_model_names:
                base_id_short = f"{original_name}_{counter}"
                counter += 1
            used_model_names.add(base_id_short)

            # Get cached sklearn model
            model, scaler, _ = ArtifactLoader.create_model(config, use_artifacts=True)

            # Extract features for this model (in correct order)
            # Filter additional_features to only include features this model uses
            model_additional = None
            if additional_features:
                model_additional = {k: v for k, v in additional_features.items() if k in feature_names}

            # Build feature vector in correct order
            feature_values = []
            for fname in feature_names:
                if model_additional and fname in model_additional:
                    feature_values.append(model_additional[fname])
                else:
                    feature_values.append(all_feature_dict.get(fname, 0.0))

            # Scale and predict
            X = np.array(feature_values).reshape(1, -1)
            if scaler:
                X = scaler.transform(X)

            proba = model.predict_proba(X)[0]
            # proba[0] = P(away wins), proba[1] = P(home wins)
            home_win_prob = float(proba[1])
            home_win_prob = max(0.01, min(home_win_prob, 0.99))

            print(f"[EnsemblePredictor] Base model '{base_id_short}': raw proba={proba}, home_win_prob={home_win_prob}")
            base_home_probs[f"p_{base_id_short}"] = home_win_prob

            # Store breakdown for UI
            base_model_breakdowns.append({
                'config_id': base_id_str,
                'config_id_short': base_id_short,
                'name': config.get('name') or f'Base Model {base_id_short}',
                'model_type': config.get('model_type') or 'Unknown',
                'home_win_prob_pct': round(home_win_prob * 100, 1),
                'features_dict': {fname: all_feature_dict.get(fname, 0.0) for fname in feature_names}
            })

        # STEP 3: Build meta-features and predict with meta-model
        meta_feature_cols = self.meta_config.get('meta_feature_cols', [])
        stacking_mode = self.meta_config.get('stacking_mode', 'naive')
        use_disagree = bool(self.meta_config.get('use_disagree', False))
        use_conf = bool(self.meta_config.get('use_conf', False))

        # Reconstruct meta feature columns if missing (naive stacking)
        # Use same naming convention as stacking_tool.py training
        if not meta_feature_cols:
            reconstructed_cols = []
            seen_names = set()
            for bid, cfg in zip(self.base_model_ids, self.base_model_configs):
                model_name = cfg.get('name')
                if model_name:
                    col_name = re.sub(r'[^a-zA-Z0-9_]', '_', model_name)
                else:
                    col_name = str(bid)[:8]
                # Handle collisions
                original = col_name
                counter = 1
                while col_name in seen_names:
                    col_name = f"{original}_{counter}"
                    counter += 1
                seen_names.add(col_name)
                reconstructed_cols.append(f"p_{col_name}")
            meta_feature_cols = reconstructed_cols

        meta_values: Dict[str, float] = {}
        meta_values.update(base_home_probs)

        print(f"[EnsemblePredictor] meta_feature_cols from config: {meta_feature_cols}")
        print(f"[EnsemblePredictor] base_home_probs keys: {list(base_home_probs.keys())}")
        print(f"[EnsemblePredictor] base_home_probs values: {list(base_home_probs.values())}")

        # Debug: Check for key mismatches between base_home_probs and meta_feature_cols
        base_prob_keys = set(base_home_probs.keys())
        expected_p_cols = {c for c in meta_feature_cols if c.startswith('p_')}
        if base_prob_keys != expected_p_cols:
            print(f"[EnsemblePredictor] WARNING: Key mismatch!")
            print(f"  base_home_probs keys: {sorted(base_prob_keys)}")
            print(f"  meta_feature_cols p_ keys: {sorted(expected_p_cols)}")
            missing_from_values = expected_p_cols - base_prob_keys
            extra_in_values = base_prob_keys - expected_p_cols
            if missing_from_values:
                print(f"  Missing from base_home_probs (will be 0): {missing_from_values}")
            if extra_in_values:
                print(f"  Extra in base_home_probs (unused): {extra_in_values}")

        # Derived meta-features for informed stacking
        if stacking_mode == 'informed':
            pred_cols = sorted([c for c in meta_values.keys() if c.startswith('p_')])

            if use_disagree:
                for i in range(len(pred_cols)):
                    for j in range(i + 1, len(pred_cols)):
                        id_i = pred_cols[i].replace('p_', '')
                        id_j = pred_cols[j].replace('p_', '')
                        meta_values[f'disagree_{id_i}_{id_j}'] = abs(meta_values[pred_cols[i]] - meta_values[pred_cols[j]])

            if use_conf:
                for col in pred_cols:
                    mid = col.replace('p_', '')
                    meta_values[f'conf_{mid}'] = abs(meta_values[col] - 0.5)

            # Add extra meta-features from the game features if needed
            extra_cols = [
                c for c in meta_feature_cols
                if not (c.startswith('p_') or c.startswith('disagree_') or c.startswith('conf_'))
            ]
            for col in extra_cols:
                if col in all_feature_dict:
                    meta_values[col] = all_feature_dict[col]

        # Build meta-feature vector in correct order
        meta_X = np.array([meta_values.get(col, 0.0) for col in meta_feature_cols]).reshape(1, -1)

        # Apply scaler if available (matches training pipeline)
        if self.meta_scaler is not None:
            meta_X = self.meta_scaler.transform(meta_X)

        # Meta-model prediction
        meta_proba = self.meta_model.predict_proba(meta_X)[0]
        ensemble_home_prob = float(meta_proba[1])
        ensemble_home_prob = max(0.01, min(ensemble_home_prob, 0.99))

        # STEP 4: Build result
        pred = 1 if ensemble_home_prob >= 0.5 else 0
        if pred == 1:
            winner = home_team
            winner_prob = ensemble_home_prob
        else:
            winner = away_team
            winner_prob = 1 - ensemble_home_prob

        # Convert probability to American odds
        if winner_prob >= 0.5:
            odds = int(-100 * winner_prob / (1 - winner_prob))
        else:
            odds = int(100 * (1 - winner_prob) / winner_prob)

        # Debug: Show what p_* values are in meta_values
        p_values_in_meta = {k: v for k, v in meta_values.items() if k.startswith('p_')}
        print(f"[EnsemblePredictor] Final meta_values p_* entries: {p_values_in_meta}")

        # Build features_dict with ensemble breakdown nested inside (API expects this format)
        features_dict_with_breakdown = {
            **{k: float(v) if isinstance(v, (int, float)) else v for k, v in meta_values.items()},
            '_meta_feature_cols': meta_feature_cols,
            '_ensemble_run_id': self.ensemble_config.get('ensemble_run_id'),
            '_base_model_ids': [str(x) for x in self.base_model_ids],
            '_ensemble_breakdown': {
                'stacking_mode': stacking_mode,
                'use_disagree': use_disagree,
                'use_conf': use_conf,
                'base_models': base_model_breakdowns,
                'meta_feature_cols': meta_feature_cols,
                'meta_feature_values': {col: float(meta_values.get(col, 0.0)) for col in meta_feature_cols}
            }
        }

        return {
            'predicted_winner': winner,
            'home_win_prob': round(100 * ensemble_home_prob, 1),
            'home_pts': None,  # Points prediction handled separately
            'away_pts': None,
            'odds': odds,
            'home_games_played': None,
            'away_games_played': None,
            'features_dict': features_dict_with_breakdown,
            'base_model_breakdowns': base_model_breakdowns,  # Keep for backwards compatibility
            'meta_features': meta_values
        }

    def get_player_lists(self) -> Dict:
        """Get player lists from the most recent prediction (for UI display)."""
        result = {}
        if self._per_player_lists:
            result.update(self._per_player_lists)
        if self._injury_player_lists:
            result.update(self._injury_player_lists)
        return result


def create_ensemble_predictor(db, ensemble_config: Dict, league=None) -> Optional[EnsemblePredictor]:
    """
    Factory function to create an EnsemblePredictor.

    Args:
        db: MongoDB database connection
        ensemble_config: Ensemble configuration from model config collection
        league: Optional LeagueConfig for league-aware collection routing

    Returns:
        EnsemblePredictor instance, or None if creation fails
    """
    try:
        return EnsemblePredictor(db, ensemble_config, league=league)
    except Exception as e:
        print(f"Failed to create EnsemblePredictor: {e}")
        import traceback
        traceback.print_exc()
        return None
