"""
Master Training Data Module (DEPRECATED)

This module is deprecated. Use nba_app.core.services.training_data instead.

All functionality has been migrated to the core layer:
    from nba_app.core.services.training_data import (
        TrainingDataService,
        MASTER_TRAINING_PATH,
        get_all_possible_features,
        get_master_training_path,
        extract_features_from_master,
        check_master_needs_regeneration,
        register_existing_master_csv,
    )
"""

import warnings

# Emit deprecation warning on import
warnings.warn(
    "nba_app.cli_old.master_training_data is deprecated. "
    "Use nba_app.core.services.training_data instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from core for backward compatibility
from nba_app.core.services.training_data import (
    # Constants
    MASTER_TRAINING_PATH,
    MASTER_COLLECTION,
    # Service class
    TrainingDataService,
    # Convenience functions
    get_master_training_path,
    get_master_collection_name,
    get_all_possible_features,
    get_available_seasons,
    extract_features_from_master,
    extract_features_from_master_for_points,
    check_master_needs_regeneration,
    register_existing_master_csv,
)

__all__ = [
    'MASTER_TRAINING_PATH',
    'MASTER_COLLECTION',
    'TrainingDataService',
    'get_master_training_path',
    'get_master_collection_name',
    'get_all_possible_features',
    'get_available_seasons',
    'extract_features_from_master',
    'extract_features_from_master_for_points',
    'check_master_needs_regeneration',
    'register_existing_master_csv',
]
