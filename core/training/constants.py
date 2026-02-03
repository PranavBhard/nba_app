"""
Training Constants

Centralized constants for model training configuration.
"""

import os

# Output file paths (consolidated to parent ../model_outputs)
try:
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _PARENT_ROOT = os.path.dirname(_PROJECT_ROOT)
    OUTPUTS_DIR = os.path.join(_PARENT_ROOT, 'model_outputs')
except Exception:
    OUTPUTS_DIR = './model_outputs'

# Model cache file paths
MODEL_CACHE_FILE = os.path.join(OUTPUTS_DIR, 'cache_model_config.json')
MODEL_CACHE_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'cache_model_config_no_per.json')

# Training info file paths
TRAINING_INFO_FILE = os.path.join(OUTPUTS_DIR, 'context_training_info.txt')
TRAINING_INFO_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'context_training_info_no_per.txt')

# Predictions file paths
PREDICTIONS_FILE = os.path.join(OUTPUTS_DIR, 'context_model_predictions.txt')
PREDICTIONS_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'context_model_predictions_no_per.txt')

# Default model types for evaluation
DEFAULT_MODEL_TYPES = ['LogisticRegression', 'GradientBoosting', 'SVM']

# Default C-values to test for regularization
DEFAULT_C_VALUES = [0.001, 0.01, 0.1, 1.0, 10.0]

# Models that support the C (regularization) parameter
C_SUPPORTED_MODELS = ['LogisticRegression', 'SVM']
