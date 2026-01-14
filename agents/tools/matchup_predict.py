"""
Matchup Predict Tool - Generate predictions for NBA matchups
"""

import sys
import os
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from nba_app.cli.Mongo import Mongo
from nba_app.cli.NBAModel import NBAModel
from nba_app.cli.points_regression import PointsRegressionTrainer
from nba_app.cli.player_utils import build_player_lists_for_prediction
from nba_app.core.config_manager import ModelConfigManager


# get_season_from_date is imported from web.app if available, otherwise defined above


# get_nba_model and get_points_model_trainer are imported from web.app if available


def predict(
    home: str,
    away: str,
    game_id: Optional[str] = None,
    game_date: Optional[str] = None,
    home_injuries: List[str] = None,
    away_injuries: List[str] = None,
    home_starters: List[str] = None,
    away_starters: List[str] = None,
    db=None
) -> Dict:
    """
    Generate prediction for a matchup.
    
    Args:
        home: Home team abbreviation (e.g., 'LAL')
        away: Away team abbreviation (e.g., 'BOS')
        game_id: Optional game ID
        game_date: Optional game date (YYYY-MM-DD). If not provided, uses today's date.
        home_injuries: Optional list of home team injured player IDs (strings)
        away_injuries: Optional list of away team injured player IDs (strings)
        home_starters: Optional list of home team starter player IDs (strings)
        away_starters: Optional list of away team starter player IDs (strings)
        db: Optional MongoDB database instance
        
    Returns:
        Dict with prediction results including:
        - predicted_winner: 'home' or 'away'
        - home_win_prob: Probability of home win (0-100)
        - away_win_prob: Probability of away win (0-100)
        - home_odds: American odds for home team
        - away_odds: American odds for away team
        - home_points_pred: Predicted home points (if available)
        - away_points_pred: Predicted away points (if available)
        - features_dict: Feature values used in prediction
    """
    if db is None:
        db = Mongo().db
    
    # Get game info if game_id provided
    game_doc = None
    if game_id:
        game_doc = db.stats_nba.find_one({'game_id': game_id})
    
    # Determine game date
    if game_date:
        try:
            game_date_obj = datetime.strptime(game_date, '%Y-%m-%d').date()
            game_date_str = game_date
        except ValueError:
            return {'error': f'Invalid date format: {game_date}. Use YYYY-MM-DD format.'}
    elif game_doc and game_doc.get('date'):
        game_date_str = game_doc['date']
        game_date_obj = datetime.strptime(game_date_str, '%Y-%m-%d').date()
    else:
        game_date_obj = datetime.now().date()
        game_date_str = game_date_obj.strftime('%Y-%m-%d')
    
    season = get_season_func(datetime(game_date_obj.year, game_date_obj.month, game_date_obj.day))
    
    # Get selected configs
    selected_classifier_config = db.model_config_nba.find_one({'selected': True})
    selected_points_config = db.model_config_points_nba.find_one({'selected': True})
    
    # Validate that the selected config is trained and ready for predictions
    # Uses shared validation logic from core/config_manager.py
    is_valid, error_msg = ModelConfigManager.validate_config_for_prediction(selected_classifier_config)
    if not is_valid:
        return {'error': error_msg}
    
    # Get model (use web.app functions if available)
    if _has_app_imports:
        model = get_nba_model()
        if not model or not model.classifier_model:
            return {'error': 'Failed to load model. Please ensure a model is selected and trained.'}
    else:
        return {'error': 'Model loading functions not available. Please ensure the web app is running.'}
    
    # Build player_filters from nba_rosters (source of truth)
    # Priority: Use stats_nba.{home/away}Team.players if game has been clicked into
    # Otherwise: Use nba_rosters roster
    # Injury/starter status always comes from nba_rosters (unless custom injuries/starters provided)
    
    if home_injuries is None:
        home_injuries = []
    if away_injuries is None:
        away_injuries = []

    # Build player_filters using shared utility
    # Supports custom injuries/starters for agent flexibility
    player_filters = build_player_lists_for_prediction(
        home_team=home,
        away_team=away,
        season=season,
        game_id=game_id,
        game_doc=game_doc,
        home_injuries=home_injuries,
        away_injuries=away_injuries,
        home_starters=home_starters,
        away_starters=away_starters,
        db=db
    )
    
    # Check if calibrated model should be used
    use_calibrated = selected_classifier_config.get('use_time_calibration', False)
    
    # Get points prediction if available
    points_prediction = None
    additional_features = None
    
    if selected_points_config and _has_app_imports:
        points_trainer = get_points_model_trainer(selected_points_config)
        if points_trainer:
            try:
                if not game_doc:
                    game_doc = {
                        'game_id': game_id or '',
                        'date': game_date_str,
                        'year': game_date_obj.year,
                        'month': game_date_obj.month,
                        'day': game_date_obj.day,
                        'season': season,
                        'homeTeam': {'name': home},
                        'awayTeam': {'name': away}
                    }
                
                points_prediction = points_trainer.predict(game_doc, game_date_str)
                
                # Check if model needs pred_margin
                if hasattr(model, 'feature_names') and model.feature_names and 'pred_margin' in model.feature_names:
                    pred_margin = None
                    if 'point_diff_pred' in points_prediction and points_prediction['point_diff_pred'] is not None:
                        pred_margin = points_prediction['point_diff_pred']
                    elif 'home_points' in points_prediction and 'away_points' in points_prediction:
                        pred_home = points_prediction.get('home_points', 0) or 0
                        pred_away = points_prediction.get('away_points', 0) or 0
                        pred_margin = pred_home - pred_away
                    
                    if pred_margin is not None:
                        additional_features = {'pred_margin': pred_margin}
            except Exception as e:
                print(f"Warning: Error making points prediction: {e}")
    
    # Make prediction
    try:
        prediction = model.predict_with_player_config(
            home, away, season, game_date_str, player_filters,
            use_calibrated=use_calibrated,
            additional_features=additional_features
        )
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}
    
    # Calculate odds
    home_win_prob = prediction.get('home_win_prob', 0)
    away_win_prob = 100 - home_win_prob
    
    def calculate_odds(prob_percent):
        prob = prob_percent / 100.0
        if prob >= 0.5:
            return int(-100 * prob / (1 - prob))
        else:
            return int(100 * (1 - prob) / prob)
    
    home_odds = calculate_odds(home_win_prob)
    away_odds = calculate_odds(away_win_prob)
    
    result = {
        'predicted_winner': prediction.get('predicted_winner', 'home' if home_win_prob > 50 else 'away'),
        'home_win_prob': home_win_prob,
        'away_win_prob': away_win_prob,
        'home_odds': home_odds,
        'away_odds': away_odds,
        'features_dict': prediction.get('features_dict', {})
    }
    
    # Add points predictions if available
    if points_prediction:
        if 'home_points' in points_prediction and points_prediction['home_points'] is not None:
            result['home_points_pred'] = round(points_prediction['home_points'])
        if 'away_points' in points_prediction and points_prediction['away_points'] is not None:
            result['away_points_pred'] = round(points_prediction['away_points'])
        if 'point_diff_pred' in points_prediction and points_prediction['point_diff_pred'] is not None:
            result['point_diff_pred'] = round(points_prediction['point_diff_pred'])
    
    return result


# Try to import model loading functions from web.app
# This works when tools are called from the same process as the Flask app
try:
    # Try direct import - will work when running in Flask process
    import sys
    import importlib
    try:
        # Try to import web.app module
        web_app = importlib.import_module('web.app')
        get_nba_model = web_app.get_nba_model
        load_model_from_mongo_config = web_app.load_model_from_mongo_config
        get_points_model_trainer = web_app.get_points_model_trainer
        get_season_func = web_app.get_season_from_date
        _has_app_imports = True
    except (ImportError, AttributeError):
        _has_app_imports = False
        # Fallback: define get_season_func here
        def get_season_func(d: datetime) -> str:
            if d.month > 8:
                return f"{d.year}-{d.year + 1}"
            else:
                return f"{d.year - 1}-{d.year}"
except Exception:
    _has_app_imports = False
    def get_season_func(d: datetime) -> str:
        if d.month > 8:
            return f"{d.year}-{d.year + 1}"
        else:
            return f"{d.year - 1}-{d.year}"
