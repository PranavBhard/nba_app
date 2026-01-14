"""
Unified Model Factory for consistent model creation and loading across all components.
Prioritizes saved artifacts for fast loading with graceful fallback to retraining.
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import StandardScaler


class ModelFactory:
    """Centralized model creation and loading with artifact support."""
    
    @staticmethod
    def create_model(config: Dict, use_artifacts: bool = True) -> Tuple[object, StandardScaler, List[str]]:
        """
        Create or load model from configuration.
        
        Args:
            config: Model configuration dictionary
            use_artifacts: Whether to prioritize saved artifacts
            
        Returns:
            Tuple of (model, scaler, feature_names)
        """
        model_type = config.get('model_type', 'LogisticRegression')
        
        if use_artifacts:
            # Try to load from saved artifacts (fast path)
            model, scaler, feature_names = ModelFactory._load_from_artifacts(config)
            if model is not None:
                print(f"✅ Loaded {model_type} from artifacts")
                return model, scaler, feature_names
            else:
                print(f"⚠️  Artifacts not found, will train {model_type}")
        
        # Fallback to training from data (slow path)
        return ModelFactory._train_from_data(config)
    
    @staticmethod
    def save_model_artifacts(model: object, scaler: StandardScaler, feature_names: List[str], 
                        config: Dict, run_id: str = None) -> bool:
        """
        Save trained model artifacts to standardized location.
        
        Args:
            model: Trained sklearn model
            scaler: Fitted StandardScaler
            feature_names: List of feature names
            config: Model configuration
            run_id: Optional run identifier
            
        Returns:
            True if successful
        """
        try:
            import uuid
            from datetime import datetime
            
            if run_id is None:
                run_id = str(uuid.uuid4())
            
            # Create models directory
            models_dir = 'cli/models'
            os.makedirs(models_dir, exist_ok=True)
            
            # Generate file paths
            model_path = f'{models_dir}/{run_id}_model.pkl'
            scaler_path = f'{models_dir}/{run_id}_scaler.pkl'
            features_path = f'{models_dir}/{run_id}_features.json'
            
            # Save artifacts
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
            
            with open(features_path, 'w') as f:
                json.dump(feature_names, f, indent=2)
            
            # Update config with artifact paths
            config_id = config.get('_id')
            if config_id:
                from bson import ObjectId
                
                # Import here to avoid circular imports
                from nba_app.web.app import db
                db.model_config_nba.update_one(
                    {'_id': ObjectId(config_id)},
                    {'$set': {
                        'model_artifact_path': model_path,
                        'scaler_artifact_path': scaler_path,
                        'features_path': features_path,
                        'run_id': run_id,
                        'artifacts_saved_at': datetime.utcnow()
                    }}
                )
            
            print(f"✅ Saved artifacts for {config_id[:8] if config_id else run_id[:8]}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving artifacts: {e}")
            return False
    
    @staticmethod
    def _load_from_artifacts(config: Dict) -> Tuple[Optional[object], Optional[StandardScaler], Optional[List[str]]]:
        """
        Load model from saved artifacts.
        
        Args:
            config: Model configuration
            
        Returns:
            Tuple of (model, scaler, feature_names) or (None, None, None)
        """
        try:
            model_path = config.get('model_artifact_path')
            scaler_path = config.get('scaler_artifact_path')
            features_path = config.get('features_path')
            
            if not all([model_path, scaler_path, features_path]):
                return None, None, None
            
            if not all([os.path.exists(p) for p in [model_path, scaler_path, features_path]]):
                print(f"⚠️  Missing artifacts:")
                print(f"   Model: {model_path} {'✅' if os.path.exists(model_path) else '❌'}")
                print(f"   Scaler: {scaler_path} {'✅' if os.path.exists(scaler_path) else '❌'}")
                print(f"   Features: {features_path} {'✅' if os.path.exists(features_path) else '❌'}")
                return None, None, None
            
            # Load artifacts
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            
            with open(features_path, 'r') as f:
                feature_names = json.load(f)
            
            return model, scaler, feature_names
            
        except Exception as e:
            print(f"❌ Error loading artifacts: {e}")
            return None, None, None
    
    @staticmethod
    def _train_from_data(config: Dict) -> Tuple[object, StandardScaler, List[str]]:
        """
        Train model from training data (fallback when artifacts not available).
        
        Args:
            config: Model configuration
            
        Returns:
            Tuple of (model, scaler, feature_names)
        """
        try:
            training_csv = config.get('training_csv')
            if not training_csv or not os.path.exists(training_csv):
                raise FileNotFoundError(f"Training data not found: {training_csv}")
            
            # Load and prepare data
            df = pd.read_csv(training_csv)
            meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon', 'game_id', 'home_points', 'away_points']
            feature_cols = [c for c in df.columns if c not in meta_cols]

            if 'HomeWon' not in df.columns:
                raise ValueError(f"Training CSV missing required target column 'HomeWon': {training_csv}")

            # Coerce features to numeric (object dtype will break np.isnan)
            X_df = df[feature_cols].apply(pd.to_numeric, errors='coerce')

            # Drop feature columns that are entirely non-numeric
            all_nan_cols = [c for c in X_df.columns if X_df[c].isna().all()]
            if all_nan_cols:
                X_df = X_df.drop(columns=all_nan_cols)
                feature_cols = [c for c in feature_cols if c not in all_nan_cols]

            if not feature_cols:
                raise ValueError(
                    f"No usable numeric feature columns found in training CSV: {training_csv}"
                )

            # Coerce y to numeric as well
            y_series = pd.to_numeric(df['HomeWon'], errors='coerce')

            X = X_df.to_numpy(dtype=float)
            y = y_series.to_numpy()

            # Filter rows with any NaNs in X or y
            nan_mask = np.isnan(X).any(axis=1) | np.isnan(y)
            if nan_mask.sum() > 0:
                X = X[~nan_mask]
                y = y[~nan_mask]

            if X.shape[0] == 0:
                raise ValueError(
                    f"No usable training rows after numeric coercion/NaN filtering for: {training_csv}"
                )

            # Ensure y is 1D numeric
            y = y.astype(float)

            # Standardize
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Create model based on type
            model_type = config.get('model_type', 'LogisticRegression')
            best_c_value = config.get('best_c_value', 0.1)
            
            if model_type == 'LogisticRegression':
                from sklearn.linear_model import LogisticRegression
                model = LogisticRegression(C=best_c_value, max_iter=1000, random_state=42)
            elif model_type == 'SVM':
                from sklearn.svm import SVC
                model = SVC(C=best_c_value, probability=True, random_state=42)
            elif model_type == 'GradientBoosting':
                from sklearn.ensemble import GradientBoostingClassifier
                model = GradientBoostingClassifier(random_state=42)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            # Train model
            model.fit(X_scaled, y)
            
            print(f"✅ Trained {model_type} from {len(X)} samples, {len(feature_cols)} features")
            return model, scaler, feature_cols
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            raise
    
    @staticmethod
    def create_sklearn_model(model_type: str, c_value: float = 0.1, random_state: int = 42) -> object:
        """
        Create sklearn model instance.
        
        Args:
            model_type: Type of model to create
            c_value: C-value for regularized models
            random_state: Random state for reproducibility
            
        Returns:
            sklearn model instance
        """
        if model_type == 'LogisticRegression':
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(C=c_value, max_iter=1000, random_state=random_state)
        elif model_type == 'SVM':
            from sklearn.svm import SVC
            return SVC(C=c_value, probability=True, random_state=random_state)
        elif model_type == 'GradientBoosting':
            from sklearn.ensemble import GradientBoostingClassifier
            return GradientBoostingClassifier(random_state=random_state)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    @staticmethod
    def get_model_info(model: object) -> Dict:
        """
        Get information about a trained model.
        
        Args:
            model: Trained sklearn model
            
        Returns:
            Dictionary with model information
        """
        info = {
            'model_type': type(model).__name__,
            'has_probabilities': hasattr(model, 'predict_proba'),
            'feature_count': getattr(model, 'n_features_in_', 'unknown'),
            'classes': getattr(model, 'classes_', 'unknown').tolist() if hasattr(model, 'classes_') else 'unknown'
        }
        
        # Add model-specific information
        if hasattr(model, 'C'):
            info['c_value'] = model.C
        if hasattr(model, 'n_estimators'):
            info['n_estimators'] = model.n_estimators
        if hasattr(model, 'feature_importances_'):
            info['has_feature_importance'] = True
        
        return info
