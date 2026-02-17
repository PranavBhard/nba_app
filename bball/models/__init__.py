"""
ML Models Module.

This module contains machine learning model implementations:
- BballModel: Main classifier model for game predictions (league-aware)
- PointsRegressionTrainer: Points prediction model
- ArtifactLoader: Factory for creating sklearn models
- EnsemblePredictor: Ensemble model handling
"""

# Main basketball classifier model (league-aware)
from bball.models.bball_model import BballModel

# Backward compatibility alias
NBAModel = BballModel

# Points regression trainer
from bball.models.points_regression import PointsRegressionTrainer

# Artifact loader (model loading from disk)
from bball.models.artifact_loader import ArtifactLoader

# Backward compatibility alias
ModelFactory = ArtifactLoader

# Ensemble predictor
from bball.models.ensemble import EnsemblePredictor, create_ensemble_predictor

__all__ = [
    # Main model
    'BballModel',
    'NBAModel',  # Backward compatibility alias
    # Points regression
    'PointsRegressionTrainer',
    # Artifact loader
    'ArtifactLoader',
    'ModelFactory',  # Backward compatibility alias
    # Ensemble
    'EnsemblePredictor',
    'create_ensemble_predictor',
]
