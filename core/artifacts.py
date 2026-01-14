"""
Centralized Artifact Management for consistent model storage and retrieval.
Handles all artifact operations with standardized paths and validation.
"""

import os
import pickle
import json
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bson import ObjectId


class ArtifactManager:
    """Centralized artifact management with cleanup and validation."""
    
    def __init__(self, base_path: str = 'cli/models'):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def save_artifacts(self, model: object, scaler: object, feature_names: List[str],
                     run_id: str, config_id: str = None, 
                     metadata: Dict = None) -> Dict:
        """
        Save model artifacts with standardized structure.
        
        Args:
            model: Trained sklearn model
            scaler: Fitted scaler
            feature_names: List of feature names
            run_id: Unique identifier
            config_id: MongoDB config ID
            metadata: Additional metadata to store
            
        Returns:
            Result dictionary with paths and success status
        """
        try:
            # Generate file paths
            model_path = os.path.join(self.base_path, f'{run_id}_model.pkl')
            scaler_path = os.path.join(self.base_path, f'{run_id}_scaler.pkl')
            features_path = os.path.join(self.base_path, f'{run_id}_features.json')
            metadata_path = os.path.join(self.base_path, f'{run_id}_metadata.json')
            
            # Save model artifact
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Save scaler artifact
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
            
            # Save feature names
            with open(features_path, 'w') as f:
                json.dump(feature_names, f, indent=2)
            
            # Save metadata
            artifact_metadata = {
                'run_id': run_id,
                'config_id': config_id,
                'model_type': type(model).__name__,
                'n_features': len(feature_names),
                'feature_names': feature_names,
                'saved_at': datetime.utcnow().isoformat(),
                'file_paths': {
                    'model': model_path,
                    'scaler': scaler_path,
                    'features': features_path,
                    'metadata': metadata_path
                }
            }
            
            if metadata:
                artifact_metadata.update(metadata)
            
            with open(metadata_path, 'w') as f:
                json.dump(artifact_metadata, f, indent=2)
            
            result = {
                'success': True,
                'run_id': run_id,
                'paths': {
                    'model': model_path,
                    'scaler': scaler_path,
                    'features': features_path,
                    'metadata': metadata_path
                },
                'metadata': artifact_metadata
            }
            
            print(f"✅ Saved artifacts for {run_id[:8]}")
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'run_id': run_id
            }
    
    def load_artifacts(self, run_id: str) -> Dict:
        """
        Load model artifacts by run_id.
        
        Args:
            run_id: Unique identifier
            
        Returns:
            Dictionary with loaded artifacts
        """
        try:
            model_path = os.path.join(self.base_path, f'{run_id}_model.pkl')
            scaler_path = os.path.join(self.base_path, f'{run_id}_scaler.pkl')
            features_path = os.path.join(self.base_path, f'{run_id}_features.json')
            metadata_path = os.path.join(self.base_path, f'{run_id}_metadata.json')
            
            # Check if all files exist
            if not all([os.path.exists(p) for p in [model_path, scaler_path, features_path, metadata_path]]):
                return {
                    'success': False,
                    'error': f'Incomplete artifact set for {run_id[:8]}',
                    'missing_files': [p for p in [model_path, scaler_path, features_path, metadata_path] if not os.path.exists(p)]
                }
            
            # Load artifacts
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            
            with open(features_path, 'r') as f:
                feature_names = json.load(f)
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            result = {
                'success': True,
                'run_id': run_id,
                'model': model,
                'scaler': scaler,
                'feature_names': feature_names,
                'metadata': metadata,
                'paths': {
                    'model': model_path,
                    'scaler': scaler_path,
                    'features': features_path,
                    'metadata': metadata_path
                }
            }
            
            print(f"✅ Loaded artifacts for {run_id[:8]}")
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to load artifacts for {run_id[:8]}: {str(e)}',
                'run_id': run_id
            }
    
    def load_from_config(self, config: Dict) -> Dict:
        """
        Load artifacts using configuration paths.
        
        Args:
            config: Configuration dictionary with artifact paths
            
        Returns:
            Dictionary with loaded artifacts
        """
        try:
            run_id = config.get('run_id')
            if not run_id:
                return {
                    'success': False,
                    'error': 'No run_id in configuration'
                }
            
            return self.load_artifacts(run_id)
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to load artifacts from config: {str(e)}'
            }
    
    def list_artifacts(self, model_type: str = None, days_old: int = None) -> List[Dict]:
        """
        List available artifacts with optional filtering.
        
        Args:
            model_type: Filter by model type
            days_old: Only include artifacts newer than this many days
            
        Returns:
            List of artifact information dictionaries
        """
        try:
            artifacts = []
            
            if not os.path.exists(self.base_path):
                return artifacts
            
            # Get all metadata files
            metadata_files = [f for f in os.listdir(self.base_path) if f.endswith('_metadata.json')]
            
            for metadata_file in metadata_files:
                metadata_path = os.path.join(self.base_path, metadata_file)
                
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    # Apply filters
                    if days_old:
                        saved_at = datetime.fromisoformat(metadata['saved_at'])
                        if (datetime.utcnow() - saved_at).days > days_old:
                            continue
                    
                    if model_type and metadata.get('model_type') != model_type:
                        continue
                    
                    # Check if artifact files still exist
                    if all([os.path.exists(p) for p in metadata['file_paths'].values()]):
                        artifacts.append(metadata)
                        
                except Exception as e:
                    print(f"⚠️  Error reading metadata {metadata_file}: {e}")
                    continue
            
            # Sort by saved_at (newest first)
            artifacts.sort(key=lambda x: x['saved_at'], reverse=True)
            return artifacts
            
        except Exception as e:
            print(f"Error listing artifacts: {e}")
            return []
    
    def cleanup_artifacts(self, days_old: int = 30, dry_run: bool = False) -> Dict:
        """
        Clean up old artifacts.
        
        Args:
            days_old: Remove artifacts older than this many days
            dry_run: If True, only report what would be deleted
            
        Returns:
            Cleanup result dictionary
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            artifacts = self.list_artifacts(days_old=days_old)
            
            to_delete = []
            for artifact in artifacts:
                if datetime.fromisoformat(artifact['saved_at']) < cutoff_date:
                    to_delete.extend(artifact['file_paths'].values())
            
            if dry_run:
                return {
                    'success': True,
                    'dry_run': True,
                    'would_delete': len(to_delete),
                    'artifacts_to_delete': [a['run_id'] for a in artifacts if datetime.fromisoformat(a['saved_at']) < cutoff_date]
                }
            
            # Actually delete files
            deleted_count = 0
            for file_path in set(to_delete):
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                except Exception as e:
                    print(f"⚠️  Could not delete {file_path}: {e}")
            
            return {
                'success': True,
                'dry_run': False,
                'deleted_count': deleted_count,
                'cutoff_date': cutoff_date.isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Cleanup failed: {str(e)}'
            }
    
    def get_artifact_info(self, run_id: str) -> Dict:
        """
        Get information about specific artifact.
        
        Args:
            run_id: Artifact identifier
            
        Returns:
            Artifact information dictionary
        """
        try:
            metadata_path = os.path.join(self.base_path, f'{run_id}_metadata.json')
            
            if not os.path.exists(metadata_path):
                return {
                    'success': False,
                    'error': f'No metadata found for {run_id[:8]}'
                }
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Add file existence info
            file_info = {}
            for name, path in metadata['file_paths'].items():
                file_info[name] = {
                    'path': path,
                    'exists': os.path.exists(path),
                    'size': os.path.getsize(path) if os.path.exists(path) else 0,
                    'modified': datetime.fromtimestamp(os.path.getmtime(path)).isoformat() if os.path.exists(path) else None
                }
            
            metadata['file_info'] = file_info
            metadata['success'] = True
            
            return metadata
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get artifact info: {str(e)}'
            }
    
    def validate_artifact_set(self, run_id: str) -> Dict:
        """
        Validate that all artifact files exist and are readable.
        
        Args:
            run_id: Artifact identifier
            
        Returns:
            Validation result dictionary
        """
        try:
            model_path = os.path.join(self.base_path, f'{run_id}_model.pkl')
            scaler_path = os.path.join(self.base_path, f'{run_id}_scaler.pkl')
            features_path = os.path.join(self.base_path, f'{run_id}_features.json')
            metadata_path = os.path.join(self.base_path, f'{run_id}_metadata.json')
            
            validation = {
                'success': True,
                'run_id': run_id,
                'files_exist': True,
                'files_readable': True,
                'missing_files': [],
                'unreadable_files': []
            }
            
            # Check file existence
            files_to_check = {
                'model': model_path,
                'scaler': scaler_path,
                'features': features_path,
                'metadata': metadata_path
            }
            
            for name, path in files_to_check.items():
                if not os.path.exists(path):
                    validation['files_exist'] = False
                    validation['missing_files'].append(name)
                else:
                    # Check readability
                    try:
                        if name in ['model', 'scaler']:
                            with open(path, 'rb') as f:
                                pickle.load(f)
                        else:
                            with open(path, 'r') as f:
                                json.load(f)
                    except Exception as e:
                        validation['files_readable'] = False
                        validation['unreadable_files'].append(name)
            
            validation['success'] = validation['files_exist'] and validation['files_readable']
            
            return validation
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Validation failed: {str(e)}',
                'run_id': run_id
            }
