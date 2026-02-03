"""
Core Training Module

This module provides the foundational training infrastructure for the NBA prediction system.
All model training, evaluation, and related utilities live here.

Consumer layers (web/, cli/, agents/) should import from this module rather than
implementing training logic themselves.
"""

from nba_app.core.training.constants import (
    DEFAULT_MODEL_TYPES,
    DEFAULT_C_VALUES,
    C_SUPPORTED_MODELS,
    MODEL_CACHE_FILE,
    MODEL_CACHE_FILE_NO_PER,
    OUTPUTS_DIR,
)

from nba_app.core.training.model_factory import (
    create_model_with_c,
    XGBOOST_AVAILABLE,
    LIGHTGBM_AVAILABLE,
    CATBOOST_AVAILABLE,
)

from nba_app.core.training.model_evaluation import (
    evaluate_model_combo,
    evaluate_model_combo_with_calibration,
    compute_feature_importance,
)

from nba_app.core.training.cache_utils import (
    load_model_cache,
    save_model_cache,
    get_best_config,
    get_latest_training_csv,
    read_csv_safe,
)

__all__ = [
    # Constants
    'DEFAULT_MODEL_TYPES',
    'DEFAULT_C_VALUES',
    'C_SUPPORTED_MODELS',
    'MODEL_CACHE_FILE',
    'MODEL_CACHE_FILE_NO_PER',
    'OUTPUTS_DIR',
    # Model factory
    'create_model_with_c',
    'XGBOOST_AVAILABLE',
    'LIGHTGBM_AVAILABLE',
    'CATBOOST_AVAILABLE',
    # Model evaluation
    'evaluate_model_combo',
    'evaluate_model_combo_with_calibration',
    'compute_feature_importance',
    # Cache utilities
    'load_model_cache',
    'save_model_cache',
    'get_best_config',
    'get_latest_training_csv',
    'read_csv_safe',
]
