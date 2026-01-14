"""
Unified Model Configuration Management.
Centralizes all model configuration operations using MongoDB as single source of truth.
"""

import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from bson import ObjectId


class ModelConfigManager:
    """Centralized model configuration management using MongoDB."""
    
    def __init__(self, db):
        self.db = db
    
    def get_config(self, config_id: str = None, config_hash: str = None, selected: bool = False) -> Optional[Dict]:
        """
        Get model configuration by ID, hash, or selected flag.
        
        Args:
            config_id: MongoDB _id as string
            config_hash: Config hash for unique identification
            selected: Get the currently selected config
            
        Returns:
            Configuration dict or None if not found
        """
        try:
            if config_id:
                return self.db.model_config_nba.find_one({'_id': ObjectId(config_id)})
            elif config_hash:
                return self.db.model_config_nba.find_one({'config_hash': config_hash})
            elif selected:
                return self.db.model_config_nba.find_one({'selected': True})
            else:
                raise ValueError("Must specify config_id, config_hash, or selected=True")
        except Exception as e:
            print(f"Error getting config: {e}")
            return None
    
    def save_config(self, config: Dict) -> str:
        """
        Save or update model configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            MongoDB document _id as string
        """
        try:
            # Generate config hash if not provided
            if 'config_hash' not in config:
                config['config_hash'] = self._generate_config_hash(config)
            
            # Add timestamps
            config['updated_at'] = datetime.utcnow()
            if 'created_at' not in config:
                config['created_at'] = datetime.utcnow()
            
            # Upsert using config_hash as unique identifier
            result = self.db.model_config_nba.update_one(
                {'config_hash': config['config_hash']},
                {'$set': config},
                upsert=True
            )
            
            # Get document ID
            if result.upserted_id:
                config_id = str(result.upserted_id)
            else:
                doc = self.db.model_config_nba.find_one({'config_hash': config['config_hash']})
                config_id = str(doc['_id'])
            
            print(f"✅ Saved config {config_id[:8]} with hash {config['config_hash'][:8]}")
            return config_id
            
        except Exception as e:
            print(f"Error saving config: {e}")
            raise
    
    def set_selected_config(self, config_id: str) -> bool:
        """
        Set a configuration as selected (unselect all others).
        
        Args:
            config_id: MongoDB _id as string
            
        Returns:
            True if successful
        """
        try:
            # Unselect all configs first
            self.db.model_config_nba.update_many(
                {},
                {'$set': {'selected': False}}
            )
            
            # Select the specified config
            result = self.db.model_config_nba.update_one(
                {'_id': ObjectId(config_id)},
                {'$set': {
                    'selected': True,
                    'updated_at': datetime.utcnow()
                }}
            )
            
            success = result.modified_count > 0
            if success:
                print(f"✅ Selected config {config_id[:8]}")
            else:
                print(f"❌ Config {config_id[:8]} not found")
            
            return success
            
        except Exception as e:
            print(f"Error selecting config: {e}")
            return False
    
    def get_selected_config(self) -> Optional[Dict]:
        """Get the currently selected configuration."""
        return self.get_config(selected=True)

    @staticmethod
    def validate_config_for_prediction(config: Dict, check_file_exists: bool = True) -> tuple:
        """
        Validate that a model config is trained and ready for predictions.

        This is the single source of truth for validation logic used by:
        - Web app prediction endpoints
        - Agent prediction tools
        - Any other prediction interface

        Args:
            config: Model configuration dictionary
            check_file_exists: Whether to verify training_csv file exists on disk

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
            If valid, error_message is None.
        """
        if not config:
            return False, "No model config provided."

        config_name = config.get('name', 'Unnamed')
        is_ensemble = bool(config.get('ensemble', False))

        if is_ensemble:
            # Ensemble models are considered trained when they have an ensemble_run_id
            ensemble_run_id = config.get('ensemble_run_id')
            if not ensemble_run_id:
                return False, (
                    f'The selected ensemble model config "{config_name}" has not been trained yet. '
                    f'Please train the ensemble meta-model first.'
                )
        else:
            # Regular models are considered trained when they have a training_csv path
            training_csv = config.get('training_csv')
            if not training_csv:
                return False, (
                    f'The selected model config "{config_name}" has not been trained yet. '
                    f'Please train the model first.'
                )
            if check_file_exists and not os.path.exists(training_csv):
                return False, (
                    f'The selected model config "{config_name}" training data file not found at: {training_csv}. '
                    f'The file may have been deleted or moved. Please retrain the model.'
                )

        return True, None
    
    def list_configs(self, model_type: str = None, ensemble: bool = None) -> List[Dict]:
        """
        List configurations with optional filtering.
        
        Args:
            model_type: Filter by model type
            ensemble: Filter by ensemble flag
            
        Returns:
            List of configuration dictionaries
        """
        try:
            query = {}
            if model_type:
                query['model_type'] = model_type
            if ensemble is not None:
                query['ensemble'] = ensemble
            
            configs = list(self.db.model_config_nba.find(query))
            
            # Convert ObjectIds to strings for JSON serialization
            for config in configs:
                if '_id' in config:
                    config['_id'] = str(config['_id'])
            
            return configs
            
        except Exception as e:
            print(f"Error listing configs: {e}")
            return []
    
    def delete_config(self, config_id: str) -> bool:
        """
        Delete a configuration.
        
        Args:
            config_id: MongoDB _id as string
            
        Returns:
            True if successful
        """
        try:
            result = self.db.model_config_nba.delete_one({'_id': ObjectId(config_id)})
            success = result.deleted_count > 0
            
            if success:
                print(f"✅ Deleted config {config_id[:8]}")
            else:
                print(f"❌ Config {config_id[:8]} not found")
            
            return success
            
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False
    
    def _generate_config_hash(self, config: Dict) -> str:
        """
        Generate unique hash for configuration identification.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            MD5 hash string
        """
        # Use key fields for hash generation
        hash_fields = {
            'model_type': config.get('model_type'),
            'feature_set_hash': config.get('feature_set_hash'),
            'best_c_value': config.get('best_c_value'),
            'use_time_calibration': config.get('use_time_calibration'),
            'calibration_method': config.get('calibration_method'),
            'calibration_years': config.get('calibration_years'),
            'begin_year': config.get('begin_year'),
            'evaluation_year': config.get('evaluation_year'),
            'include_injuries': config.get('include_injuries'),
            'recency_decay_k': config.get('recency_decay_k'),
            'use_master': config.get('use_master'),
            'min_games_played': config.get('min_games_played')
        }
        
        # Create deterministic string representation
        hash_str = '|'.join(f"{k}:{v}" for k, v in sorted(hash_fields.items()) if v is not None)
        
        # Generate MD5 hash
        return hashlib.md5(hash_str.encode()).hexdigest()
    
    @staticmethod
    def create_from_request(request_data: Dict) -> Dict:
        """
        Create configuration dictionary from web request data.
        
        Args:
            request_data: JSON data from web request
            
        Returns:
            Configuration dictionary
        """
        # Extract and validate fields from request
        config = {
            'model_type': request_data.get('model_type'),
            'features': request_data.get('features', []),
            'use_time_calibration': request_data.get('use_time_calibration', False),
            'calibration_method': request_data.get('calibration_method'),
            'begin_year': request_data.get('begin_year'),
            'calibration_years': request_data.get('calibration_years', []),
            'evaluation_year': request_data.get('evaluation_year'),
            'include_injuries': request_data.get('include_injuries', False),
            'recency_decay_k': request_data.get('recency_decay_k'),
            'use_master': request_data.get('use_master', True),
            'min_games_played': request_data.get('min_games_played', 15),
            'ensemble': request_data.get('ensemble', False),
            'ensemble_models': request_data.get('ensemble_models', []),
            'ensemble_type': request_data.get('ensemble_type'),
            'ensemble_meta_features': request_data.get('ensemble_meta_features', []),
            'ensemble_use_disagree': request_data.get('ensemble_use_disagree', False),
            'ensemble_use_conf': request_data.get('ensemble_use_conf', False)
        }
        
        # Remove None values
        return {k: v for k, v in config.items() if v is not None}
