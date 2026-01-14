"""
Point Prediction Cache Utility

Manages caching and loading of point predictions for use as classifier features.
Predictions are stored in MongoDB and can be merged into datasets on-demand.
"""

import sys
import os
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.cli.Mongo import Mongo


COLLECTION_NAME = 'point_predictions_cache'


class PointPredictionCache:
    """Manages point prediction caching and retrieval."""
    
    def __init__(self, db=None):
        """
        Initialize PointPredictionCache.
        
        Args:
            db: MongoDB database instance (optional)
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        self.collection = self.db[COLLECTION_NAME]
        
        # Create indexes for fast lookups
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Ensure indexes exist for fast lookups."""
        try:
            # Compound index on (game_id, model_id) for fast lookups
            self.collection.create_index([('game_id', 1), ('model_id', 1)], unique=True)
            # Index on model_id for bulk operations
            self.collection.create_index([('model_id', 1)])
        except Exception:
            # Indexes may already exist
            pass
    
    def cache_predictions(
        self,
        model_id: str,
        predictions: List[Dict],
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Cache point predictions for a model.
        
        Args:
            model_id: Unique identifier for the point prediction model
            predictions: List of prediction dicts, each with:
                - game_id: str (ESPN game_id)
                - pred_home_points: float
                - pred_away_points: float
                - year: int (optional, for fallback matching)
                - month: int (optional, for fallback matching)
                - day: int (optional, for fallback matching)
                - home_team: str (optional, for fallback matching)
                - away_team: str (optional, for fallback matching)
            metadata: Optional metadata about the model (e.g., training config)
            
        Returns:
            Number of predictions cached
        """
        from pymongo import UpdateOne
        
        # Use bulk operations for much faster writes
        now = datetime.utcnow()
        operations = []
        
        for pred in predictions:
            game_id = pred.get('game_id', '')
            
            # Build document - handle both home/away and margin-only predictions
            # For margin-only models, pred_home_points and pred_away_points may be None
            pred_home = pred.get('pred_home_points')
            pred_away = pred.get('pred_away_points')
            pred_margin = pred.get('pred_margin')
            
            # Convert None to 0.0 for database storage (or keep as None if pred_margin exists)
            if pred_home is None and pred_away is None and pred_margin is not None:
                # Margin-only model
                doc = {
                    'game_id': game_id,
                    'model_id': model_id,
                    'pred_home_points': None,
                    'pred_away_points': None,
                    'pred_margin': float(pred_margin),
                    'created_at': now,
                    'metadata': {
                        'year': pred.get('year'),
                        'month': pred.get('month'),
                        'day': pred.get('day'),
                        'home_team': pred.get('home_team', ''),
                        'away_team': pred.get('away_team', ''),
                        'target_type': 'margin'  # Mark as margin-only model
                    }
                }
            else:
                # Home/away model (default behavior)
                doc = {
                    'game_id': game_id,
                    'model_id': model_id,
                    'pred_home_points': float(pred_home) if pred_home is not None else 0.0,
                    'pred_away_points': float(pred_away) if pred_away is not None else 0.0,
                    'created_at': now,
                    'metadata': {
                        'year': pred.get('year'),
                        'month': pred.get('month'),
                        'day': pred.get('day'),
                        'home_team': pred.get('home_team', ''),
                        'away_team': pred.get('away_team', ''),
                        'target_type': 'home_away'  # Mark as home/away model
                    }
                }
                # Derive pred_margin from home/away for consistency
                if pred_home is not None and pred_away is not None:
                    doc['pred_margin'] = float(pred_home) - float(pred_away)
            
            if metadata:
                doc['model_metadata'] = metadata
            
            # Build bulk operation (upsert)
            operations.append(
                UpdateOne(
                    {'game_id': game_id, 'model_id': model_id},
                    {'$set': doc},
                    upsert=True
                )
            )
        
        # Execute bulk write in batches of 1000 for efficiency
        batch_size = 1000
        cached_count = 0
        for i in range(0, len(operations), batch_size):
            batch = operations[i:i + batch_size]
            result = self.collection.bulk_write(batch, ordered=False)
            cached_count += result.upserted_count + result.modified_count
        
        return cached_count
    
    def load_predictions(
        self,
        model_id: str,
        game_ids: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Load cached point predictions.
        
        Args:
            model_id: Model identifier
            game_ids: Optional list of game_ids to filter (if None, returns all for model)
            
        Returns:
            DataFrame with columns: game_id, pred_home_points, pred_away_points, metadata
        """
        query = {'model_id': model_id}
        if game_ids:
            query['game_id'] = {'$in': game_ids}
        
        predictions = list(self.collection.find(query))
        
        if not predictions:
            return pd.DataFrame()
        
        # Convert to DataFrame - handle both home/away and margin-only models
        data = []
        for pred in predictions:
            data.append({
                'game_id': pred.get('game_id', ''),
                'pred_home_points': pred.get('pred_home_points'),  # May be None for margin-only
                'pred_away_points': pred.get('pred_away_points'),  # May be None for margin-only
                'pred_margin': pred.get('pred_margin'),  # Exists for both types
                'year': pred.get('metadata', {}).get('year'),
                'month': pred.get('metadata', {}).get('month'),
                'day': pred.get('metadata', {}).get('day'),
                'home_team': pred.get('metadata', {}).get('home_team', ''),
                'away_team': pred.get('metadata', {}).get('away_team', ''),
                'target_type': pred.get('metadata', {}).get('target_type', 'home_away')  # Default to home_away for backward compatibility
            })
        
        return pd.DataFrame(data)
    
    def merge_predictions_into_dataframe(
        self,
        df: pd.DataFrame,
        model_id: str
    ) -> pd.DataFrame:
        """
        Merge point predictions into a dataframe.
        
        Args:
            df: DataFrame with master training data (must have game_id or Year/Month/Day/Home/Away)
            model_id: Model identifier for predictions to merge
            
        Returns:
            DataFrame with added columns: pred_home_points, pred_away_points, pred_margin, pred_point_total
        """
        # Check if predictions exist
        pred_count = self.collection.count_documents({'model_id': model_id})
        if pred_count == 0:
            raise ValueError(f"No predictions found for model_id: {model_id}")
        
        # Load predictions
        pred_df = self.load_predictions(model_id)
        
        if pred_df.empty:
            raise ValueError(f"No predictions loaded for model_id: {model_id}")
        
        # Determine merge key
        has_game_id = 'game_id' in df.columns
        
        # Select columns to merge based on what's available in pred_df
        merge_cols = ['game_id', 'pred_margin']  # Always include pred_margin
        if 'pred_home_points' in pred_df.columns:
            merge_cols.append('pred_home_points')
        if 'pred_away_points' in pred_df.columns:
            merge_cols.append('pred_away_points')
        
        if has_game_id:
            # Merge by game_id
            df = df.merge(
                pred_df[merge_cols],
                on='game_id',
                how='left'
            )
        else:
            # Fallback: merge by date + teams
            if not all(col in df.columns for col in ['Year', 'Month', 'Day', 'Home', 'Away']):
                raise ValueError("DataFrame must have game_id or (Year, Month, Day, Home, Away) columns")
            
            # Include metadata columns for merging
            merge_cols_with_meta = merge_cols + ['year', 'month', 'day', 'home_team', 'away_team']
            merge_cols_with_meta = [col for col in merge_cols_with_meta if col in pred_df.columns]
            
            # Merge on date + teams
            df = df.merge(
                pred_df[merge_cols_with_meta],
                left_on=['Year', 'Month', 'Day', 'Home', 'Away'],
                right_on=['year', 'month', 'day', 'home_team', 'away_team'],
                how='left'
            )
            # Drop temporary merge columns
            df = df.drop(columns=['year', 'month', 'day', 'home_team', 'away_team'], errors='ignore')
        
        # Handle margin-only vs home/away models
        # Ensure all expected columns exist
        if 'pred_home_points' not in df.columns:
            df['pred_home_points'] = None
        if 'pred_away_points' not in df.columns:
            df['pred_away_points'] = None
        if 'pred_margin' not in df.columns:
            df['pred_margin'] = None
        
        # For home/away models: fill NaN with 0, calculate pred_margin if missing
        # For margin-only models: pred_home_points and pred_away_points remain None/NaN, pred_margin is filled
        has_home_away = df['pred_home_points'].notna().any() or df['pred_away_points'].notna().any()
        
        if has_home_away:
            # Home/away model: fill NaN with 0 for home/away
            df['pred_home_points'] = df['pred_home_points'].fillna(0.0)
            df['pred_away_points'] = df['pred_away_points'].fillna(0.0)
            
            # Calculate pred_margin if not already present
            mask_margin_na = df['pred_margin'].isna()
            if mask_margin_na.any():
                df.loc[mask_margin_na, 'pred_margin'] = (
                    df.loc[mask_margin_na, 'pred_home_points'] - 
                    df.loc[mask_margin_na, 'pred_away_points']
                )
            
            # Calculate pred_point_total for home/away models
            df['pred_point_total'] = df['pred_home_points'] + df['pred_away_points']
        else:
            # Margin-only model: pred_home_points and pred_away_points remain None/NaN
            # pred_margin should be filled (if predictions were cached correctly)
            # For margin-only, we can't calculate pred_point_total without knowing actual points
            df['pred_point_total'] = None
        
        return df
    
    def get_model_ids(self) -> List[str]:
        """Get list of all model_ids with cached predictions."""
        return self.collection.distinct('model_id')
    
    def delete_predictions(self, model_id: str) -> int:
        """
        Delete all predictions for a model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Number of predictions deleted
        """
        result = self.collection.delete_many({'model_id': model_id})
        return result.deleted_count
    
    def get_stats(self, model_id: Optional[str] = None) -> Dict:
        """
        Get cache statistics.
        
        Args:
            model_id: Optional model_id to filter (if None, returns stats for all models)
            
        Returns:
            Dict with statistics
        """
        query = {'model_id': model_id} if model_id else {}
        
        total = self.collection.count_documents(query)
        models = self.collection.distinct('model_id', query) if not model_id else [model_id]
        
        return {
            'total_predictions': total,
            'model_ids': models,
            'model_count': len(models)
        }
