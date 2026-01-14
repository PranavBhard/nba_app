#!/usr/bin/env python3
"""
NBA Prediction Model CLI

TRAIN COMMAND:
    python train.py train [OPTIONS]
    
    Options:
        --model-type TYPE              Single model type (e.g., LogisticRegression, GradientBoosting, SVM, XGBoost, LightGBM, CatBoost, RandomForest, NaiveBayes, MLPClassifier)
        --model-types TYPES            Comma-separated model types (e.g., LogisticRegression,GradientBoosting,SVM)
        --c-value VALUE                Single C-value to use (e.g., 0.01)
        --c-values VALUES              Comma-separated C-values to test (e.g., 0.1,0.01,1.0)
        --no-per                       Exclude PER (Player Efficiency Rating) features from training
        --model-specific-features      Use model-specific feature sets:
                                       - LogisticRegression: differentials only
                                       - Tree models (XGBoost, LightGBM, CatBoost, GradientBoosting, RandomForest): per-team + interactions
                                       - Neural Networks (MLPClassifier): structured per-team blocks
        --ablate                       Run ablation study: test model performance with each feature set removed
        --test-layers                  Test layer configurations: compare performance across different layer combinations
        --layer-config CONFIG         Specific layer config to test (e.g., "layer_1_2" or "layer_1,layer_2")
                                       If not specified with --test-layers, tests all common configs

PREDICT COMMAND:
    python train.py predict [OPTIONS]
    
    Options:
        --date DATE, -d DATE           Date for predictions in YYYY-MM-DD format (default: today)
        --model-type TYPE              Single model type (e.g., LogisticRegression)
        --model-types TYPES            Comma-separated model types (e.g., LogisticRegression,GradientBoosting,SVM)
        --c-value VALUE                Single C-value to use (e.g., 0.01)
        --c-values VALUES              Comma-separated C-values to test (e.g., 0.1,0.01,1.0)
        --no-per                       Use model trained without PER features
        --exclude-players IDS           Comma-separated list of player IDs to exclude from PER calculations (e.g., "4277961,4238338")

EXAMPLES:
    # Basic training
    python train.py train
    
    # Train without PER features
    python train.py train --no-per
    
    # Train specific models with specific C-values
    python train.py train --model-types LogisticRegression,SVM --c-values 0.01,0.1,1.0
    
    # Train with model-specific features
    python train.py train --model-type XGBoost --model-specific-features
    
    # Run ablation study
    python train.py train --ablate --model-type GradientBoosting
    
    # Test layer configurations
    python train.py train --test-layers --model-type GradientBoosting
    
    # Test specific layer configuration
    python train.py train --test-layers --layer-config layer_1,layer_2 --model-type GradientBoosting
    
    # Predict for today
    python train.py predict
    
    # Predict for specific date
    python train.py predict --date 2025-03-13
    
    # Predict with specific model and C-value
    python train.py predict --model-type SVM --c-value 0.1
"""

import sys
import os

# Add parent directory to path so we can import nba_app
# Script is in nba_app/cli/, so we need to go up two levels to find the nba_app package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import argparse
import os
import glob
import json
from datetime import datetime
from copy import deepcopy

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# Try to import advanced tree models (optional)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except (ImportError, Exception) as e:
    # Catch ImportError and also XGBoostError (when OpenMP library is missing)
    XGBOOST_AVAILABLE = False
    if 'XGBoostError' in str(type(e).__name__) or 'libomp' in str(e).lower():
        import warnings
        warnings.warn(f"XGBoost is not available: {e}. Install OpenMP with 'brew install libomp' if needed.")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except (ImportError, Exception):
    LIGHTGBM_AVAILABLE = False

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except (ImportError, Exception):
    CATBOOST_AVAILABLE = False
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss

from nba_app.cli.NBAModel import NBAModel, get_default_classifier_features, get_default_points_features
from nba_app.cli.feature_sets import (
    FEATURE_SETS,
    FEATURE_LAYERS,
    get_features_excluding_sets,
    get_set_name_for_feature,
    get_feature_set_info,
    FEATURE_SET_DESCRIPTIONS,
    get_features_by_layers,
    get_features_by_sets,
    get_layer_info,
    get_common_layer_configs,
    LAYER_DESCRIPTIONS
)


# Output file paths (consolidated to parent ../model_outputs)
try:
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _PARENT_ROOT = os.path.dirname(_PROJECT_ROOT)
    OUTPUTS_DIR = os.path.join(_PARENT_ROOT, 'model_outputs')
except Exception:
    OUTPUTS_DIR = './model_outputs'

MODEL_CACHE_FILE = os.path.join(OUTPUTS_DIR, 'cache_model_config.json')
MODEL_CACHE_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'cache_model_config_no_per.json')
TRAINING_INFO_FILE = os.path.join(OUTPUTS_DIR, 'context_training_info.txt')
TRAINING_INFO_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'context_training_info_no_per.txt')
PREDICTIONS_FILE = os.path.join(OUTPUTS_DIR, 'context_model_predictions.txt')
PREDICTIONS_FILE_NO_PER = os.path.join(OUTPUTS_DIR, 'context_model_predictions_no_per.txt')

# Default model types and C-values
DEFAULT_MODEL_TYPES = ['LogisticRegression', 'GradientBoosting', 'SVM']
DEFAULT_C_VALUES = [0.001, 0.01, 0.1, 1.0, 10.0]

# Models that support C parameter
C_SUPPORTED_MODELS = ['LogisticRegression', 'SVM']


def get_latest_training_csv(output_dir: str = OUTPUTS_DIR, no_per: bool = False) -> str:
    """
    Find the most recent classifier training CSV file.
    
    Args:
        output_dir: Directory to search for CSV files
        no_per: If True, look for files with 'no_per' in the name
                If False, look for files without 'no_per' in the name
    """
    pattern = os.path.join(output_dir, 'classifier_training_*.csv')
    csv_files = glob.glob(pattern)
    
    # Filter out standardized versions
    csv_files = [f for f in csv_files if '_standardized' not in f]
    
    # Filter based on no_per flag
    if no_per:
        csv_files = [f for f in csv_files if 'no_per' in f]
    else:
        csv_files = [f for f in csv_files if 'no_per' not in f]
    
    if not csv_files:
        return None
    
    # Sort by modification time, most recent first
    csv_files.sort(key=os.path.getmtime, reverse=True)
    return csv_files[0]


def create_model_with_c(model_type: str, c_value: float = None):
    """
    Create a classifier model with optional C-value.
    
    Args:
        model_type: Name of the model type
        c_value: C-value for regularization (only applies to LogisticRegression, SVM)
        
    Returns:
        sklearn classifier instance
    """
    if model_type == 'LogisticRegression':
        c = c_value if c_value is not None else 0.1  # Default to 0.1 for better regularization
        return LogisticRegression(C=c, max_iter=10000, random_state=42)
    elif model_type == 'SVM':
        c = c_value if c_value is not None else 0.1  # Default to 0.1 for better regularization
        return SVC(C=c, probability=True, random_state=42)
    elif model_type == 'GradientBoosting':
        return GradientBoostingClassifier(n_estimators=100, random_state=42)
    elif model_type == 'RandomForest':
        return RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'XGBoost':
        if not XGBOOST_AVAILABLE:
            raise ImportError("XGBoost not installed. Install with: pip install xgboost")
        return xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
    elif model_type == 'LightGBM':
        if not LIGHTGBM_AVAILABLE:
            raise ImportError("LightGBM not installed. Install with: pip install lightgbm")
        return lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    elif model_type == 'CatBoost':
        if not CATBOOST_AVAILABLE:
            raise ImportError("CatBoost not installed. Install with: pip install catboost")
        return cb.CatBoostClassifier(iterations=100, random_state=42, verbose=False)
    elif model_type == 'NaiveBayes':
        return GaussianNB()
    elif model_type == 'NeuralNetwork':
        return MLPClassifier(max_iter=10000, random_state=42)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def evaluate_model_combo(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str,
    c_value: float = None,
    n_splits: int = 5
) -> dict:
    """
    Evaluate a model/C-value combination using time-series cross-validation.
    
    Returns:
        Dict with accuracy, std, log_loss, brier, etc., including per-fold metrics
    """
    model = create_model_with_c(model_type, c_value)
    
    # Time-series split for CV
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    accuracies = []
    log_losses = []
    briers = []
    
    for train_idx, val_idx in tscv.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        model_copy = create_model_with_c(model_type, c_value)
        model_copy.fit(X_train, y_train)
        
        # Predictions
        y_pred = model_copy.predict(X_val)
        y_proba = model_copy.predict_proba(X_val)
        
        # Metrics
        acc = accuracy_score(y_val, y_pred) * 100
        ll = log_loss(y_val, y_proba)
        brier = brier_score_loss(y_val, y_proba[:, 1])
        
        accuracies.append(acc)
        log_losses.append(ll)
        briers.append(brier)
    
    # Always include fold-level metrics
    result = {
        'model_type': model_type,
        'c_value': c_value,
        'accuracy_mean': float(np.mean(accuracies)),
        'accuracy_std': float(np.std(accuracies)),
        'accuracy_folds': accuracies,
        'log_loss_mean': float(np.mean(log_losses)),
        'log_loss_std': float(np.std(log_losses)),
        'log_loss_folds': log_losses,
        'brier_mean': float(np.mean(briers)),
        'brier_std': float(np.std(briers)),
        'brier_folds': briers,
        'n_folds': n_splits
    }
    
    return result


def evaluate_model_combo_with_calibration(
    df: pd.DataFrame,
    X_scaled: np.ndarray,
    y: np.ndarray,
    model_type: str,
    c_value: float = None,
    calibration_method: str = 'isotonic',
    calibration_years: list = None,
    evaluation_year: int = None,
    logger = None
) -> dict:
    """
    Evaluate a model with time-based calibration using year-based temporal splits.
    
    Time-based calibration splits data chronologically by year:
    - Train: All data before first calibration_year (e.g., < 2022)
    - Calibrate: Data from calibration_years (e.g., 2022, 2023) - combined
    - Evaluate: Data from evaluation_year (e.g., 2024)
    
    This is different from the non-calibrated version which uses TimeSeriesSplit CV.
    The key difference is that calibration learns to adjust probabilities on recent
    but not latest data, then evaluates on the most recent data.
    
    Args:
        df: DataFrame with Year, Month, Day columns for sorting
        X_scaled: Scaled feature matrix (must match df rows)
        y: Target vector (must match df rows)
        model_type: Model type (e.g., 'LogisticRegression')
        c_value: C-value for regularization (optional)
        calibration_method: 'isotonic' or 'sigmoid'
        calibration_years: List of years to use for calibration (e.g., [2022, 2023])
        evaluation_year: Year to use for evaluation (e.g., 2024)
        logger: Logger instance for logging
        
    Returns:
        Dict with accuracy, std, log_loss, brier, etc.
    """
    from sklearn.calibration import IsotonicRegression
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, log_loss, brier_score_loss
    
    # Handle backward compatibility: if single calibration_year passed, convert to list
    if calibration_years is None:
        raise ValueError("calibration_years must be specified for time-based calibration")
    
    # Ensure calibration_years is a list
    if not isinstance(calibration_years, list):
        calibration_years = [calibration_years]
    
    if logger:
        logger.info(f"Using time-based calibration (method: {calibration_method})")
        logger.info(f"Calibration years: {calibration_years}, Evaluation year: {evaluation_year}")
    
    # Create date column for sorting and derive SeasonStartYear (e.g., 2010-2011 -> 2010)
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy[['Year', 'Month', 'Day']])
    df_copy['SeasonStartYear'] = np.where(df_copy['Month'] >= 10, df_copy['Year'], df_copy['Year'] - 1)
    
    if evaluation_year is None:
        raise ValueError("evaluation_year must be specified for time-based calibration")
    
    # Interpret provided years as season start years
    cal_seasons = [int(y) for y in calibration_years]
    eval_season = int(evaluation_year)
    # Get the earliest calibration season to determine training cutoff
    earliest_cal_year = min(cal_seasons)
    
    # Split by year boundaries:
    # Train: All data before earliest calibration_year (Year < earliest_cal_year)
    # Calibrate: Data from all calibration_years (Year in calibration_years) - combined
    # Evaluate: Data from evaluation_year (Year == evaluation_year)
    
    # Training set: all data before earliest calibration season
    train_mask = df_copy['SeasonStartYear'] < earliest_cal_year
    X_train = X_scaled[train_mask]
    y_train = y[train_mask]
    
    # Calibration set: data from all calibration seasons (combined)
    cal_mask = df_copy['SeasonStartYear'].isin(cal_seasons)
    X_cal = X_scaled[cal_mask]
    y_cal = y[cal_mask]
    
    # Evaluation set: data from evaluation season
    eval_mask = df_copy['SeasonStartYear'] == eval_season
    X_eval = X_scaled[eval_mask]
    y_eval = y[eval_mask]
    
    if logger:
        logger.info(f"Train set: {len(X_train)} games (SeasonStartYear < {earliest_cal_year})")
        logger.info(f"Calibration set: {len(X_cal)} games (Seasons in {cal_seasons})")
        logger.info(f"Evaluation set: {len(X_eval)} games (SeasonStartYear == {eval_season})")
        
        if len(X_train) == 0:
            logger.warning(f"Training set is empty! Check begin_year and calibration_years. Earliest cal year: {earliest_cal_year}")
        if len(X_cal) == 0:
            logger.warning(f"Calibration set is empty! Check calibration_years: {calibration_years}")
        if len(X_eval) == 0:
            logger.warning(f"Evaluation set is empty! Check evaluation_year: {evaluation_year}")
    
    # Train model on training set
    model = create_model_with_c(model_type, c_value)
    model.fit(X_train, y_train)
    
    # Get raw predictions on calibration set
    y_proba_raw_cal = model.predict_proba(X_cal)
    
    # Fit calibrator on calibration set
    if calibration_method == 'isotonic':
        calibrator = IsotonicRegression(out_of_bounds='clip')
        calibrator.fit(y_proba_raw_cal[:, 1], y_cal)
        if logger:
            logger.info("Fitted isotonic calibrator on calibration set")
    elif calibration_method == 'sigmoid':
        # Use sigmoid (Platt scaling) - create wrapper to avoid cv='prefit' compatibility issues
        sigmoid_calibrator = LogisticRegression()
        sigmoid_calibrator.fit(y_proba_raw_cal[:, 1].reshape(-1, 1), y_cal)
        
        class SigmoidCalibratedModel:
            def __init__(self, base_model, calibrator):
                self.base_model = base_model
                self.calibrator = calibrator
            
            def predict(self, X):
                return self.base_model.predict(X)
            
            def predict_proba(self, X):
                raw_proba = self.base_model.predict_proba(X)
                calibrated_1 = self.calibrator.predict_proba(raw_proba[:, 1].reshape(-1, 1))[:, 1]
                # Ensure probabilities sum to 1
                calibrated_1 = np.clip(calibrated_1, 0.0, 1.0)
                return np.column_stack([1 - calibrated_1, calibrated_1])
        
        calibrator = SigmoidCalibratedModel(model, sigmoid_calibrator)
        if logger:
            logger.info("Fitted sigmoid calibrator on calibration set")
    else:
        if logger:
            logger.warning(f"Unknown calibration method: {calibration_method}, using raw probabilities")
        calibrator = None
    
    # Get raw predictions on evaluation set
    y_proba_raw_eval = model.predict_proba(X_eval)
    
    # Apply calibration to evaluation set
    if calibrator is not None:
        if calibration_method == 'isotonic':
            y_proba_calibrated = np.column_stack([
                1 - calibrator.predict(y_proba_raw_eval[:, 1]),
                calibrator.predict(y_proba_raw_eval[:, 1])
            ])
        else:  # sigmoid
            y_proba_calibrated = calibrator.predict_proba(X_eval)
    else:
        y_proba_calibrated = y_proba_raw_eval
    
    # Calculate predictions and metrics on evaluation set
    y_pred_calibrated = (y_proba_calibrated[:, 1] >= 0.5).astype(int)
    
    acc = accuracy_score(y_eval, y_pred_calibrated) * 100
    ll = log_loss(y_eval, y_proba_calibrated)
    brier = brier_score_loss(y_eval, y_proba_calibrated[:, 1])
    
    if logger:
        logger.info(f"Calibrated results on season starting {eval_season} - Accuracy: {acc:.2f}%, Log Loss: {ll:.4f}, Brier: {brier:.4f}")
    
    # Return in same format as evaluate_model_combo (single evaluation, so std=0)
    return {
        'model_type': model_type,
        'c_value': c_value,
        'accuracy_mean': float(acc),
        'accuracy_std': 0.0,  # Single evaluation, no std
        'accuracy_folds': [acc],
        'log_loss_mean': float(ll),
        'log_loss_std': 0.0,
        'log_loss_folds': [ll],
        'brier_mean': float(brier),
        'brier_std': 0.0,
        'brier_folds': [brier],
        'n_folds': 1,  # For compatibility, but this is a single split, not cross-validation
        'split_type': 'time_based_calibration',  # Indicates this is time-based split, not CV folds
        'calibration_years': calibration_years,
        'evaluation_year': evaluation_year
    }


def load_model_cache(no_per: bool = False) -> dict:
    """Load cached model configurations."""
    cache_file = MODEL_CACHE_FILE_NO_PER if no_per else MODEL_CACHE_FILE
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {'configs': [], 'best': None, 'timestamp': None}


def save_model_cache(cache: dict, no_per: bool = False):
    """Save model configurations to cache."""
    cache_file = MODEL_CACHE_FILE_NO_PER if no_per else MODEL_CACHE_FILE
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)


def read_csv_safe(csv_path: str) -> pd.DataFrame:
    """
    Read CSV file with error handling for trailing empty columns.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        DataFrame with trailing empty columns removed
    """
    # Use Python engine from the start to handle column mismatches gracefully
    # Read the CSV and manually fix any column count mismatches
    import csv
    
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        # Remove trailing empty columns from header
        while header and (not header[-1] or header[-1].strip() == ''):
            header.pop()
        expected_cols = len(header)
        
        for row_num, row in enumerate(reader, start=2):
            # Trim row to expected length (remove trailing empty columns)
            if len(row) > expected_cols:
                # Remove trailing empty columns
                row = row[:expected_cols]
            elif len(row) < expected_cols:
                # Pad with empty strings if row is too short
                row.extend([''] * (expected_cols - len(row)))
            
            # Only add rows that match expected column count
            if len(row) == expected_cols:
                rows.append(row)
            else:
                # Log warning for rows that still don't match (shouldn't happen after trimming)
                print(f"Warning: Row {row_num} has {len(row)} columns, expected {expected_cols}. Skipping.")
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=header)
    
    # Convert numeric columns
    for col in df.columns:
        if col not in ['Home', 'Away']:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
    
    # Remove any trailing empty columns (Unnamed columns)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(axis=1, how='all')
    
    return df


def get_best_config(cache: dict) -> dict:
    """Get the best model configuration from cache based on accuracy."""
    if not cache.get('configs'):
        return None
    
    # Sort by accuracy, then by lower log_loss as tiebreaker
    sorted_configs = sorted(
        cache['configs'],
        key=lambda x: (-x['accuracy_mean'], x['log_loss_mean'])
    )
    return sorted_configs[0]


def write_training_info(
    output_path: str,
    timestamp: str,
    csv_path: str,
    game_count: int,
    results: list
):
    """Write training info report to context file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("NBA MODEL TRAINING INFO\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Training Data: {csv_path}\n")
        f.write(f"Total Games: {game_count}\n\n")
        
        f.write("MODEL CONFIGURATIONS TESTED\n")
        f.write("-" * 70 + "\n\n")
        
        # Sort by accuracy descending
        sorted_results = sorted(results, key=lambda x: -x['accuracy_mean'])
        
        for i, r in enumerate(sorted_results, 1):
            c_str = f"C={r['c_value']}" if r['c_value'] is not None else "N/A"
            f.write(f"{i}. {r['model_type']} ({c_str})\n")
            f.write(f"   Accuracy: {r['accuracy_mean']:.2f}% ± {r['accuracy_std']:.2f}%\n")
            f.write(f"   Log Loss: {r['log_loss_mean']:.4f} ± {r['log_loss_std']:.4f}\n")
            f.write(f"   Brier:    {r['brier_mean']:.4f} ± {r['brier_std']:.4f}\n")
            f.write(f"   Folds:    {r['accuracy_folds']}\n\n")
        
        f.write("-" * 70 + "\n")
        f.write(f"BEST MODEL: {sorted_results[0]['model_type']}")
        if sorted_results[0]['c_value'] is not None:
            f.write(f" (C={sorted_results[0]['c_value']})")
        f.write(f" with {sorted_results[0]['accuracy_mean']:.2f}% accuracy\n")
        f.write("-" * 70 + "\n")


def format_prediction_line(pred: dict) -> str:
    """
    Format a prediction in the format: "BOS @ MIN* - 61.4% (-159)"
    Asterisk (*) indicates the predicted winner.
    """
    home = pred['home']
    away = pred['away']
    winner = pred['predicted_winner']
    home_prob = pred['home_win_prob']
    
    # Add asterisk to winner
    if winner == home:
        home_str = f"{home}*"
        away_str = away
        prob = home_prob
    else:
        home_str = home
        away_str = f"{away}*"
        prob = 100 - home_prob
    
    # Calculate odds from probability
    prob_decimal = prob / 100
    if prob_decimal >= 0.5:
        odds = int(-100 * prob_decimal / (1 - prob_decimal))
    else:
        odds = int(100 * (1 - prob_decimal) / prob_decimal)
    
    # Format odds string
    odds_str = f"+{odds}" if odds > 0 else str(odds)
    
    return f"{away_str} @ {home_str} - {prob:.1f}% ({odds_str})"


def train_mode(args):
    """
    Train mode: creates training data, tests models, generates report.
    """
    print("=" * 60)
    print("NBA Model Training Pipeline")
    print("=" * 60)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    no_per = getattr(args, 'no_per', False)
    use_model_specific = getattr(args, 'model_specific_features', False)
    
    if no_per:
        print("\n*** Running without PER features (--no-per) ***")
    
    if use_model_specific:
        print("\n*** Using model-specific feature sets ***")
    
    # Parse model types and C-values from args
    if args.model_types:
        model_types = [m.strip() for m in args.model_types.split(',')]
    elif args.model_type:
        model_types = [args.model_type]
    else:
        model_types = DEFAULT_MODEL_TYPES
    
    if args.c_values:
        c_values = [float(c.strip()) for c in args.c_values.split(',')]
    elif args.c_value:
        c_values = [float(args.c_value)]
    else:
        c_values = DEFAULT_C_VALUES
    
    print(f"\nModel types to test: {model_types}")
    print(f"C-values to test: {c_values}")

    # Initialize model
    model = NBAModel(
        classifier_features=get_default_classifier_features(),
        points_features=get_default_points_features(),
        include_elo=True,
        use_exponential_weighting=True,
        include_era_normalization=False,
        include_per_features=not no_per
    )
    
    # Step 1: Create training data
    print("\n[1/3] Creating training data...")
    
    # Use model-specific features if requested
    if use_model_specific and len(model_types) == 1:
        # Create data for the specific model type
        model_type = model_types[0]
        print(f"Creating model-specific features for {model_type}...")
        if no_per:
            clf_csv_path = os.path.join(model.output_dir, f'classifier_training_{model_type.lower()}_no_per_{timestamp}.csv')
        else:
            clf_csv_path = os.path.join(model.output_dir, f'classifier_training_{model_type.lower()}_{timestamp}.csv')
        count, clf_csv, _ = model.create_training_data_model_specific(
            model_type=model_type,
            classifier_csv=clf_csv_path
        )
        pts_csv = None
    else:
        # Use standard features
        if no_per:
            clf_csv_path = os.path.join(model.output_dir, f'classifier_training_no_per_{timestamp}.csv')
            pts_csv_path = os.path.join(model.output_dir, f'points_training_no_per_{timestamp}.csv')
            count, clf_csv, pts_csv = model.create_training_data(
                classifier_csv=clf_csv_path,
                points_csv=pts_csv_path
            )
        else:
            count, clf_csv, pts_csv = model.create_training_data()
    print(f"Created training data: {clf_csv}")
    
    # Load data for evaluation
    print("\n[2/3] Loading training data...")
    df = read_csv_safe(clf_csv)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    target_col = 'HomeWon'
    feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
    
    X = df[feature_cols].values
    y = df[target_col].values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Rate features using ANOVA F-scores (before model evaluation)
    # This gives us the rated features list in order for all configs
    print("\n[2.5/3] Rating features (ANOVA F-scores)...")
    feature_ratings = model.rate_features(csv_path=clf_csv, top_k=None)
    # Extract just the feature names in order (sorted by F-score, highest to lowest)
    rated_features_list = [feature_name for feature_name, _ in feature_ratings]
    
    # Step 3: Evaluate all model/C-value combinations
    print("\n[3/3] Evaluating model configurations...")
    results = []
    
    total_combos = 0
    for model_type in model_types:
        if model_type in C_SUPPORTED_MODELS:
            total_combos += len(c_values)
        else:
            total_combos += 1
    
    combo_num = 0
    for model_type in model_types:
        if model_type in C_SUPPORTED_MODELS:
            # Test each C-value for this model
            for c_val in c_values:
                combo_num += 1
                print(f"  [{combo_num}/{total_combos}] {model_type} (C={c_val})...", end=' ')
                result = evaluate_model_combo(X_scaled, y, model_type, c_val)
                # Add rated features list (in order) to each result
                result['rated_features'] = rated_features_list
                results.append(result)
                print(f"Accuracy: {result['accuracy_mean']:.2f}%")
        else:
            # No C-value for this model
            combo_num += 1
            print(f"  [{combo_num}/{total_combos}] {model_type}...", end=' ')
            result = evaluate_model_combo(X_scaled, y, model_type, None)
            # Add rated features list (in order) to each result
            result['rated_features'] = rated_features_list
            results.append(result)
            print(f"Accuracy: {result['accuracy_mean']:.2f}%")
    
    # Save to cache
    print("\nSaving model configurations to cache...")
    best_config = get_best_config({'configs': results})
    # Also add rated_features to best config if it doesn't have it
    if best_config and 'rated_features' not in best_config:
        best_config['rated_features'] = rated_features_list
    
    cache = {
        'timestamp': timestamp,
        'training_csv': clf_csv,
        'game_count': count,
        'configs': results,
        'best': best_config,
        'no_per': no_per
    }
    save_model_cache(cache, no_per=no_per)
    cache_file = MODEL_CACHE_FILE_NO_PER if no_per else MODEL_CACHE_FILE
    print(f"Saved to: {cache_file}")
    
    # Write training info report
    print("Writing training info report...")
    info_file = TRAINING_INFO_FILE_NO_PER if no_per else TRAINING_INFO_FILE
    write_training_info(info_file, timestamp, clf_csv, count, results)
    print(f"Saved to: {info_file}")
    
    # Print summary
    best = cache['best']
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    print(f"\nDataset: {count} games")
    print(f"Configurations tested: {len(results)}")
    print(f"\nBest Configuration:")
    print(f"  Model: {best['model_type']}")
    if best['c_value'] is not None:
        print(f"  C-value: {best['c_value']}")
    print(f"  Accuracy: {best['accuracy_mean']:.2f}% ± {best['accuracy_std']:.2f}%")
    print(f"  Log Loss: {best['log_loss_mean']:.4f}")
    
    # Print feature ratings summary
    print("\n" + "=" * 60)
    print("FEATURE RATINGS (ANOVA F-scores)")
    print("=" * 60)
    print(f"\nTotal features rated: {len(feature_ratings)}")
    print("\nFull Feature Rankings (sorted by importance):")
    print("-" * 60)
    print(f"{'Rank':<6} {'Feature Name':<40} {'F-Score':<12}")
    print("-" * 60)
    for rank, (feature_name, score) in enumerate(feature_ratings, 1):
        print(f"{rank:<6} {feature_name:<40} {score:>12.4f}")
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


def predict_mode(args):
    """
    Predict mode: load existing training data and make predictions.
    """
    # Determine prediction date
    if args.date:
        pred_date = args.date
    else:
        pred_date = datetime.now().strftime('%Y-%m-%d')
    
    no_per = getattr(args, 'no_per', False)
    
    print("=" * 60)
    print(f"NBA Predictions for {pred_date}")
    if no_per:
        print("(Running without PER features)")
    print("=" * 60)
    
    # Try to load from MongoDB selected config first
    csv_path = None
    selected_config = None
    try:
        from nba_app.cli.Mongo import Mongo
        db = Mongo().db
        selected_config = db.model_config_nba.find_one({'selected': True})
        if selected_config:
            csv_path = selected_config.get('training_csv')
            if csv_path and os.path.exists(csv_path):
                print(f"Using selected MongoDB config: {selected_config.get('config_hash', 'unknown')}")
                print(f"  Model: {selected_config.get('model_type', 'unknown')}")
                if selected_config.get('best_c_value') is not None:
                    print(f"  C-value: {selected_config.get('best_c_value')}")
                print(f"  Training CSV: {csv_path}")
            else:
                print(f"Warning: Selected config found but training CSV not found: {csv_path}")
                csv_path = None
                selected_config = None
    except Exception as e:
        print(f"Warning: Could not load from MongoDB config: {e}")
        selected_config = None
    
    # Fallback to latest training CSV if no MongoDB config
    if not csv_path:
        csv_path = get_latest_training_csv(no_per=no_per)
        if not csv_path:
            mode_str = "no_per" if no_per else "with PER"
            print(f"Error: No training data found ({mode_str}). Run 'python train.py train{' --no-per' if no_per else ''}' first.")
            return
        print(f"Using latest training CSV: {csv_path}")
    
    # Load cache
    cache = load_model_cache(no_per=no_per)
    
    # Determine which model/C-value combos to use
    # If we have a selected MongoDB config, prefer its settings
    if selected_config:
        # Use model type and C-value from selected config if not overridden by args
        if args.model_types:
            model_types = [m.strip() for m in args.model_types.split(',')]
        elif args.model_type:
            model_types = [args.model_type]
        else:
            # Use from selected config
            model_types = [selected_config.get('model_type', 'GradientBoosting')]
        
        if args.c_values:
            c_values = [float(c.strip()) for c in args.c_values.split(',')]
        elif args.c_value:
            c_values = [float(args.c_value)]
        else:
            # Use from selected config
            best_c = selected_config.get('best_c_value')
            c_values = [best_c] if best_c is not None else [None]
    else:
        # No selected config - use args or cache
        if args.model_types:
            model_types = [m.strip() for m in args.model_types.split(',')]
        elif args.model_type:
            model_types = [args.model_type]
        else:
            model_types = None  # Use cache
        
        if args.c_values:
            c_values = [float(c.strip()) for c in args.c_values.split(',')]
        elif args.c_value:
            c_values = [float(args.c_value)]
        else:
            c_values = None  # Use cache
    
    # Build list of configs to run
    configs_to_run = []
    
    if model_types is None and c_values is None:
        # Use best from cache
        if cache.get('best'):
            configs_to_run.append(cache['best'])
            print(f"\nUsing best cached config: {cache['best']['model_type']}", end='')
            if cache['best']['c_value'] is not None:
                print(f" (C={cache['best']['c_value']})")
            else:
                print()
        else:
            # Default fallback
            configs_to_run.append({'model_type': 'GradientBoosting', 'c_value': None})
            print("\nNo cache found, using GradientBoosting default")
    else:
        # Build combos from specified args
        if model_types is None:
            model_types = ['LogisticRegression']
        if c_values is None:
            c_values = [1.0]
        
        for mt in model_types:
            if mt in C_SUPPORTED_MODELS:
                for cv in c_values:
                    # Try to find in cache
                    cached = next(
                        (c for c in cache.get('configs', []) 
                         if c['model_type'] == mt and c['c_value'] == cv),
                        None
                    )
                    if cached:
                        configs_to_run.append(cached)
                    else:
                        configs_to_run.append({'model_type': mt, 'c_value': cv})
            else:
                cached = next(
                    (c for c in cache.get('configs', []) 
                     if c['model_type'] == mt and c['c_value'] is None),
                    None
                )
                if cached:
                    configs_to_run.append(cached)
                else:
                    configs_to_run.append({'model_type': mt, 'c_value': None})
    
    # Initialize model with lazy loading for faster prediction startup
    # (Only loads data on-demand rather than preloading everything)
    # If we have a selected config, use its feature flags
    if selected_config:
        # Import the load function from web app (or duplicate the logic)
        # For now, we'll set flags based on config
        include_per = selected_config.get('include_per_features', not no_per)
        # Enhanced features always included (team-level only)
        include_era_norm = selected_config.get('include_era_normalization', False)
        include_injuries = selected_config.get('include_injuries', False)
        include_elo = selected_config.get('include_elo', True)
        include_absolute = selected_config.get('include_absolute', True)
        
        # Get classifier_features from config if available
        classifier_features = selected_config.get('classifier_features')
        if not classifier_features:
            # Will need to extract from feature names - use default for now
            from nba_app.cli.NBAModel import get_default_classifier_features
            classifier_features = get_default_classifier_features()
    else:
        # Use defaults
        include_per = not no_per
        # Enhanced features always included (team-level only)
        include_era_norm = False
        include_injuries = False
        include_elo = True
        include_absolute = True
        from nba_app.cli.NBAModel import get_default_classifier_features
        classifier_features = get_default_classifier_features()
    
    nba_model = NBAModel(
        classifier_features=classifier_features,
        points_features=get_default_points_features(),
        include_elo=include_elo,
        use_exponential_weighting=True,
        # Enhanced features always included (team-level only)
        include_era_normalization=include_era_norm,
        include_per_features=include_per,
        include_injuries=include_injuries,
        preload_data=False  # Skip expensive preloading for prediction - only load what's needed per query
    )
    nba_model.classifier_csv = csv_path
    
    # If we have a selected config, also update feature_names and extract classifier_features from CSV
    if selected_config:
        # Load the CSV to get actual feature names
        df_temp = read_csv_safe(csv_path)
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        all_feature_cols = [c for c in df_temp.columns if c not in meta_cols + [target_col]]
        
        # Filter to config features if specified (for feature_names only)
        config_features = selected_config.get('features', [])
        if config_features:
            feature_cols = [f for f in all_feature_cols if f in config_features]
        else:
            feature_cols = all_feature_cols
        
        nba_model.feature_names = feature_cols
    
    # Run predictions for each config
    all_prediction_outputs = []
    
    for config in configs_to_run:
        model_type = config['model_type']
        c_value = config.get('c_value')
        
        print(f"\n{'=' * 50}")
        print(f"MODEL: {model_type}", end='')
        if c_value is not None:
            print(f" (C={c_value})")
        else:
            print()
        print('=' * 50)
        
        # Print cached stats if available
        if config.get('accuracy_mean'):
            print(f"Cached Training Stats:")
            print(f"  Accuracy: {config['accuracy_mean']:.2f}% ± {config.get('accuracy_std', 0):.2f}%")
            print(f"  Log Loss: {config.get('log_loss_mean', 0):.4f}")
            print(f"  Brier:    {config.get('brier_mean', 0):.4f}")
            print()
        
        # Create and train model with specific C-value
        # Load data
        df = read_csv_safe(csv_path)
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        # If we have a selected config, filter to only features in the config
        if selected_config:
            config_features = selected_config.get('features', [])
            if config_features:
                # Only use features that are in both the CSV and the config
                feature_cols = [f for f in feature_cols if f in config_features]
                print(f"Filtered to {len(feature_cols)} features from config (out of {len(df.columns) - len(meta_cols) - 1} total)")
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Create model
        classifier = create_model_with_c(model_type, c_value)
        classifier.fit(X_scaled, y)
        
        # Set model on NBAModel
        nba_model.classifier_model = classifier
        nba_model.scaler = scaler
        nba_model.feature_names = feature_cols

        # Parse excluded players if provided
        excluded_player_ids = None
        if hasattr(args, 'exclude_players') and args.exclude_players:
            excluded_player_ids = set(p.strip() for p in args.exclude_players.split(','))
            print(f"\nExcluding {len(excluded_player_ids)} players from PER calculations: {', '.join(sorted(excluded_player_ids)[:5])}{'...' if len(excluded_player_ids) > 5 else ''}")
        
        # Make predictions
        predictions = nba_model.predict(pred_date, output_file=False, excluded_player_ids=excluded_player_ids)
        
        # Format output
        config_output = {
            'model_type': model_type,
            'c_value': c_value,
            'stats': {
                'accuracy': config.get('accuracy_mean'),
                'accuracy_std': config.get('accuracy_std'),
                'log_loss': config.get('log_loss_mean'),
                'brier': config.get('brier_mean')
            },
            'predictions': predictions
        }
        all_prediction_outputs.append(config_output)
        
        # Print predictions
        print("Predictions:")
        for pred in predictions:
            line = format_prediction_line(pred)
            print(f"  {line}")
    
    # Write predictions to file
    predictions_file = PREDICTIONS_FILE_NO_PER if no_per else PREDICTIONS_FILE
    print(f"\nWriting predictions to {predictions_file}...")
    write_predictions_file(predictions_file, pred_date, all_prediction_outputs)
    print("Done!")


def compute_feature_importance(model, feature_names: list, model_type: str) -> dict:
    """
    Compute feature importance for a trained model.
    
    Args:
        model: Trained sklearn model
        feature_names: List of feature names
        model_type: Type of model
        
    Returns:
        Dict mapping feature names to importance scores
    """
    importance = {}
    
    if model_type == 'GradientBoosting':
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            for name, imp in zip(feature_names, importances):
                importance[name] = float(imp)
    elif model_type == 'RandomForest':
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            for name, imp in zip(feature_names, importances):
                importance[name] = float(imp)
    elif model_type == 'LogisticRegression':
        # Use absolute coefficient values as importance proxy
        if hasattr(model, 'coef_'):
            coefs = np.abs(model.coef_[0])
            for name, coef in zip(feature_names, coefs):
                importance[name] = float(coef)
    
    return importance


def compute_correlation_by_sets(df: pd.DataFrame, feature_cols: list) -> dict:
    """
    Compute correlation matrix grouped by feature sets.
    
    Args:
        df: DataFrame with features
        feature_cols: List of feature column names
        
    Returns:
        Dict with set-to-set correlation matrices
    """
    # Get feature set assignments
    feature_to_set = {}
    for feature in feature_cols:
        set_name = get_set_name_for_feature(feature)
        if set_name:
            feature_to_set[feature] = set_name
        else:
            feature_to_set[feature] = 'unknown'
    
    # Group features by set
    set_features = {}
    for feature, set_name in feature_to_set.items():
        if set_name not in set_features:
            set_features[set_name] = []
        set_features[set_name].append(feature)
    
    # Compute correlation matrix
    corr_matrix = df[feature_cols].corr()
    
    # Compute set-to-set correlations (average pairwise correlation)
    set_names = sorted(set_features.keys())
    set_correlations = {}
    
    for set1 in set_names:
        set_correlations[set1] = {}
        for set2 in set_names:
            if set1 == set2:
                # Within-set correlation (average of upper triangle)
                feats1 = set_features[set1]
                if len(feats1) > 1:
                    sub_corr = corr_matrix.loc[feats1, feats1]
                    # Get upper triangle (excluding diagonal)
                    mask = np.triu(np.ones_like(sub_corr, dtype=bool), k=1)
                    avg_corr = sub_corr.where(mask).stack().mean()
                    set_correlations[set1][set2] = float(avg_corr) if not np.isnan(avg_corr) else 0.0
                else:
                    set_correlations[set1][set2] = 1.0
            else:
                # Between-set correlation (average pairwise)
                feats1 = set_features[set1]
                feats2 = set_features[set2]
                if feats1 and feats2:
                    sub_corr = corr_matrix.loc[feats1, feats2]
                    avg_corr = sub_corr.stack().mean()
                    set_correlations[set1][set2] = float(avg_corr) if not np.isnan(avg_corr) else 0.0
                else:
                    set_correlations[set1][set2] = 0.0
    
    return {
        'set_correlations': set_correlations,
        'feature_to_set': feature_to_set,
        'set_features': set_features
    }


def ablation_mode(args):
    """
    Ablation mode: test model performance with each feature set removed.
    """
    print("=" * 60)
    print("NBA Model Ablation Study")
    print("=" * 60)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    no_per = getattr(args, 'no_per', False)
    
    # Determine model type and C-value
    if args.model_type:
        model_type = args.model_type
    else:
        model_type = 'GradientBoosting'  # Default for ablation
    
    if args.c_value:
        c_value = float(args.c_value)
    else:
        c_value = None
    
    print(f"\nModel: {model_type}")
    if c_value is not None:
        print(f"C-value: {c_value}")
    
    # Initialize model and create training data if needed
    model = NBAModel(
        classifier_features=get_default_classifier_features(),
        points_features=get_default_points_features(),
        include_elo=True,
        use_exponential_weighting=True,
        include_era_normalization=False,
        include_per_features=not no_per
    )
    
    # Check if we need to create training data
    csv_path = get_latest_training_csv(no_per=no_per)
    if not csv_path:
        print("\n[1/4] Creating training data...")
        if no_per:
            clf_csv_path = os.path.join(model.output_dir, f'classifier_training_no_per_{timestamp}.csv')
            count, csv_path, _ = model.create_training_data(classifier_csv=clf_csv_path)
        else:
            count, csv_path, _ = model.create_training_data()
        print(f"Created: {csv_path}")
    else:
        print(f"\n[1/4] Using existing training data: {csv_path}")
    
    # Load data
    print("\n[2/4] Loading and analyzing data...")
    df = pd.read_csv(csv_path)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    target_col = 'HomeWon'
    feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
    
    X = df[feature_cols].values
    y = df[target_col].values
    
    # Compute correlation analysis
    print("  Computing correlation analysis by feature sets...")
    corr_analysis = compute_correlation_by_sets(df, feature_cols)
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train baseline model (all features)
    print("\n[3/4] Training baseline model (all features)...")
    baseline_model = create_model_with_c(model_type, c_value)
    tscv = TimeSeriesSplit(n_splits=5)
    
    baseline_results = evaluate_model_combo(X_scaled, y, model_type, c_value, n_splits=5)
    baseline_model.fit(X_scaled, y)  # Fit on full data for importance
    
    baseline_importance = compute_feature_importance(baseline_model, feature_cols, model_type)
    
    print(f"  Baseline Accuracy: {baseline_results['accuracy_mean']:.2f}% ± {baseline_results['accuracy_std']:.2f}%")
    print(f"  Baseline Log Loss: {baseline_results['log_loss_mean']:.4f} ± {baseline_results['log_loss_std']:.4f}")
    
    # Run ablation: drop each set one at a time
    print("\n[4/4] Running ablation studies (dropping one set at a time)...")
    ablation_results = []
    
    set_info = get_feature_set_info()
    all_set_names = list(FEATURE_SETS.keys())
    
    for set_name in all_set_names:
        # Skip if this set has no features in the data
        # Filter set features by model type for consistency
        set_features = get_features_by_sets([set_name], model_type=model_type)
        available_set_features = [f for f in set_features if f in feature_cols]
        
        if not available_set_features:
            print(f"  Skipping {set_name} (no features in dataset)")
            continue
        
        print(f"  Testing without {set_name} ({len(available_set_features)} features)...", end=' ')
        
        # Get features excluding this set (filtered by model type)
        excluded_features = get_features_excluding_sets([set_name], model_type=model_type)
        excluded_features = [f for f in excluded_features if f in feature_cols]
        
        if len(excluded_features) == 0:
            print("SKIP (would remove all features)")
            continue
        
        # Get indices of features to keep
        feature_indices = [i for i, f in enumerate(feature_cols) if f in excluded_features]
        X_ablated = X_scaled[:, feature_indices]
        
        # Evaluate
        ablated_results = evaluate_model_combo(X_ablated, y, model_type, c_value, n_splits=5)
        
        # Train on full data for importance comparison
        ablated_model = create_model_with_c(model_type, c_value)
        ablated_model.fit(X_ablated, y)
        ablated_importance = compute_feature_importance(ablated_model, excluded_features, model_type)
        
        # Compute importance changes for remaining features
        importance_changes = {}
        for feat in excluded_features:
            baseline_imp = baseline_importance.get(feat, 0)
            ablated_imp = ablated_importance.get(feat, 0)
            importance_changes[feat] = {
                'baseline': baseline_imp,
                'ablated': ablated_imp,
                'change': ablated_imp - baseline_imp,
                'change_pct': ((ablated_imp - baseline_imp) / baseline_imp * 100) if baseline_imp > 0 else 0
            }
        
        # Compute performance delta
        acc_delta = ablated_results['accuracy_mean'] - baseline_results['accuracy_mean']
        ll_delta = ablated_results['log_loss_mean'] - baseline_results['log_loss_mean']
        
        result = {
            'set_name': set_name,
            'set_description': FEATURE_SET_DESCRIPTIONS.get(set_name, ''),
            'features_dropped': len(available_set_features),
            'features_remaining': len(excluded_features),
            'baseline_accuracy': baseline_results['accuracy_mean'],
            'ablated_accuracy': ablated_results['accuracy_mean'],
            'accuracy_delta': acc_delta,
            'baseline_log_loss': baseline_results['log_loss_mean'],
            'ablated_log_loss': ablated_results['log_loss_mean'],
            'log_loss_delta': ll_delta,
            'baseline_brier': baseline_results['brier_mean'],
            'ablated_brier': ablated_results['brier_mean'],
            'brier_delta': ablated_results['brier_mean'] - baseline_results['brier_mean'],
            'per_fold_accuracy': ablated_results['accuracy_folds'],
            'per_fold_log_loss': ablated_results.get('log_loss_folds', []),
            'per_fold_brier': ablated_results.get('brier_folds', []),
            'importance_changes': importance_changes,
        }
        
        ablation_results.append(result)
        
        print(f"Acc: {ablated_results['accuracy_mean']:.2f}% (Δ{acc_delta:+.2f}%)")
    
    # Sort by accuracy delta (most negative = biggest drop)
    ablation_results.sort(key=lambda x: x['accuracy_delta'])
    
    # Write detailed ablation report
    output_file = os.path.join(model.output_dir, f'ablation_study_{timestamp}.txt')
    print(f"\nWriting detailed ablation report to: {output_file}")
    write_ablation_report(
        output_file,
        timestamp,
        csv_path,
        model_type,
        c_value,
        baseline_results,
        baseline_importance,
        ablation_results,
        corr_analysis,
        set_info
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("ABLATION SUMMARY")
    print("=" * 60)
    print(f"\nBaseline (all features):")
    print(f"  Accuracy: {baseline_results['accuracy_mean']:.2f}% ± {baseline_results['accuracy_std']:.2f}%")
    print(f"  Log Loss: {baseline_results['log_loss_mean']:.4f}")
    print(f"\nFeature Set Impact (sorted by accuracy drop):")
    print("-" * 60)
    for result in ablation_results:
        delta_str = f"{result['accuracy_delta']:+.2f}%"
        print(f"  {result['set_name']:25s} | {delta_str:>8s} | {result['features_dropped']:2d} features")
    
    print("\n" + "=" * 60)
    print("Ablation study complete!")
    print("=" * 60)


def layer_test_mode(args):
    """
    Layer testing mode: compare model performance across different layer configurations.
    """
    print("=" * 60)
    print("NBA Model Layer Configuration Testing")
    print("=" * 60)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    no_per = getattr(args, 'no_per', False)
    use_model_specific = getattr(args, 'model_specific_features', False)
    
    # Determine model type and C-value
    if args.model_type:
        model_type = args.model_type
    else:
        model_type = 'GradientBoosting'  # Default for layer testing
    
    if args.c_value:
        c_value = float(args.c_value)
    else:
        c_value = None
    
    print(f"\nModel: {model_type}")
    if c_value is not None:
        print(f"C-value: {c_value}")
    
    # Warn if using model-specific features with layer testing
    if use_model_specific:
        print("\n⚠️  WARNING: Layer testing with --model-specific-features may not work correctly!")
        print("   Model-specific features use different naming conventions (e.g., 'home_ppg' vs 'pointsSznAvgDiff')")
        print("   that don't match the feature sets defined in feature_sets.py.")
        print("   Consider using standard features (without --model-specific-features) for layer testing.")
        print()
    
    # Print available layer and feature set names
    print("Available Layer Names:")
    for layer_name in FEATURE_LAYERS.keys():
        sets_in_layer = ', '.join(FEATURE_LAYERS[layer_name])
        print(f"  - {layer_name}: {sets_in_layer}")
    
    print("\nAvailable Feature Set Names:")
    for set_name in FEATURE_SETS.keys():
        print(f"  - {set_name}")
    
    print("\nCommon Layer Configurations:")
    common_configs = get_common_layer_configs()
    for config_name, layers in common_configs.items():
        print(f"  - {config_name}: {', '.join(layers)}")
    print()
    
    # Determine which layer configs to test
    if args.layer_config:
        # Parse custom layer config - can be layers, feature sets, or mix
        parts = [p.strip() for p in args.layer_config.split(',')]
        
        # Check if all parts are layer names (start with 'layer_')
        if all(p.startswith('layer_') for p in parts):
            # All are layers - use existing logic
            layer_names = parts
            configs_to_test = {args.layer_config: layer_names}
            print(f"\nTesting custom layer config: {args.layer_config}")
        else:
            # Mix of layers and feature sets, or just feature sets
            # Need to resolve to feature lists
            feature_sets_to_use = []
            layer_names_for_display = []
            
            for part in parts:
                if part.startswith('layer_'):
                    # It's a layer - get its feature sets
                    if part in FEATURE_LAYERS:
                        feature_sets_to_use.extend(FEATURE_LAYERS[part])
                        layer_names_for_display.append(part)
                elif part in FEATURE_SETS:
                    # It's a feature set name
                    feature_sets_to_use.append(part)
                    layer_names_for_display.append(part)
                else:
                    print(f"Warning: '{part}' is not a recognized layer or feature set, skipping")
            
            # Get features for these sets (filtered by model type for consistency)
            config_features = get_features_by_sets(feature_sets_to_use, model_type=model_type)
            
            # Create a config entry
            configs_to_test = {args.layer_config: feature_sets_to_use}
            print(f"\nTesting custom config: {args.layer_config}")
            print(f"  Feature sets: {', '.join(feature_sets_to_use)}")
    else:
        # Test all common configs
        common_configs = get_common_layer_configs()
        configs_to_test = common_configs
        print(f"\nTesting {len(common_configs)} common layer configurations:")
        for config_name in common_configs.keys():
            print(f"  - {config_name}")
    
    # Initialize model and get training data
    model = NBAModel(
        classifier_features=get_default_classifier_features(),
        points_features=get_default_points_features(),
        include_elo=True,
        use_exponential_weighting=True,
        include_era_normalization=False,
        include_per_features=not no_per
    )
    
    # Check if we need to create training data
    csv_path = get_latest_training_csv(no_per=no_per)
    if not csv_path:
        print("\n[1/3] Creating training data...")
        if no_per:
            clf_csv_path = os.path.join(model.output_dir, f'classifier_training_no_per_{timestamp}.csv')
            count, csv_path, _ = model.create_training_data(classifier_csv=clf_csv_path)
        else:
            count, csv_path, _ = model.create_training_data()
        print(f"Created: {csv_path}")
    else:
        print(f"\n[1/3] Using existing training data: {csv_path}")
    
    # Load data
    print("\n[2/3] Loading data...")
    df = read_csv_safe(csv_path)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    target_col = 'HomeWon'
    all_feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
    
    # Check if this looks like model-specific features (different naming convention)
    has_model_specific_features = any('_' in f and (f.startswith('home_') or f.startswith('away_')) for f in all_feature_cols[:10])
    if has_model_specific_features:
        print("\n⚠️  WARNING: Detected old snake_case feature naming (e.g., 'home_ppg', 'away_off_rtg')")
        print("   This CSV was generated with the old naming convention.")
        print("   Layer testing expects standardized camelCase names (e.g., 'homePointsSznAvg', 'homeOffRtg').")
        print("\n   SOLUTION: Regenerate your training data with the updated code:")
        print("   python train.py train --model-type XGBoost --model-specific-features")
        print(f"\n   Sample features in CSV: {', '.join(all_feature_cols[:5])}...")
        print(f"   Total features in CSV: {len(all_feature_cols)}")
    
    X_all = df[all_feature_cols].values
    y = df[target_col].values
    
    # Standardize all features once
    scaler = StandardScaler()
    X_all_scaled = scaler.fit_transform(X_all)
    
    # Get layer info for reporting
    layer_info = get_layer_info()
    
    # Test each layer configuration
    print("\n[3/3] Testing layer configurations...")
    results = []
    
    for config_name, config_items in configs_to_test.items():
        # config_items can be either layer names or feature set names
        print(f"\n  Testing: {config_name} ({', '.join(config_items)})...", end=' ')
        
        # Determine if config_items are layers or feature sets
        # Filter features by model type to ensure consistency (diffs for LR, per-team for Tree/NN)
        if all(item.startswith('layer_') for item in config_items):
            # All are layers - use get_features_by_layers
            config_features = get_features_by_layers(config_items, model_type=model_type)
            layer_names = config_items
        else:
            # Mix or just feature sets - use get_features_by_sets
            config_features = get_features_by_sets(config_items, model_type=model_type)
            # For display, try to map back to layers if possible
            layer_names = config_items
        
        # Filter to features that exist in the dataset
        available_features = [f for f in config_features if f in all_feature_cols]
        
        if len(available_features) == 0:
            print("SKIP (no features available)")
            continue
        
        # Get feature indices
        feature_indices = [i for i, f in enumerate(all_feature_cols) if f in available_features]
        X_config = X_all_scaled[:, feature_indices]
        
        # Evaluate
        config_results = evaluate_model_combo(X_config, y, model_type, c_value, n_splits=5)
        
        # Train on full data for feature importance
        config_model = create_model_with_c(model_type, c_value)
        config_model.fit(X_config, y)
        config_importance = compute_feature_importance(config_model, available_features, model_type)
        
        # Get layer/set breakdown
        layer_breakdown = {}
        for item in layer_names:
            if item.startswith('layer_'):
                # It's a layer
                layer_sets = get_features_by_layers([item], model_type=model_type)
                layer_features = [f for f in layer_sets if f in available_features]
                layer_breakdown[item] = {
                    'feature_count': len(layer_features),
                    'description': LAYER_DESCRIPTIONS.get(item, '')
                }
            elif item in FEATURE_SETS:
                # It's a feature set
                set_features = get_features_by_sets([item], model_type=model_type)
                available_set_features = [f for f in set_features if f in available_features]
                layer_breakdown[item] = {
                    'feature_count': len(available_set_features),
                    'description': FEATURE_SET_DESCRIPTIONS.get(item, '')
                }
        
        result = {
            'config_name': config_name,
            'layer_names': layer_names,
            'layer_breakdown': layer_breakdown,
            'feature_count': len(available_features),
            'accuracy_mean': config_results['accuracy_mean'],
            'accuracy_std': config_results['accuracy_std'],
            'accuracy_folds': config_results['accuracy_folds'],
            'log_loss_mean': config_results['log_loss_mean'],
            'log_loss_std': config_results['log_loss_std'],
            'log_loss_folds': config_results['log_loss_folds'],
            'brier_mean': config_results['brier_mean'],
            'brier_std': config_results['brier_std'],
            'brier_folds': config_results['brier_folds'],
            'feature_importance': config_importance,
        }
        
        results.append(result)
        print(f"Acc: {config_results['accuracy_mean']:.2f}% ± {config_results['accuracy_std']:.2f}%")
    
    # Sort by accuracy
    results.sort(key=lambda x: x['accuracy_mean'], reverse=True)
    
    # Write detailed layer test report
    output_file = os.path.join(model.output_dir, f'layer_test_{timestamp}.txt')
    print(f"\nWriting layer test report to: {output_file}")
    write_layer_test_report(
        output_file,
        timestamp,
        csv_path,
        model_type,
        c_value,
        results,
        layer_info
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("LAYER CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"\n{'Config':<20} {'Layers':<30} {'Features':<10} {'Accuracy':<15} {'Log Loss':<12}")
    print("-" * 90)
    for result in results:
        layers_str = ', '.join(result['layer_names'])
        print(f"{result['config_name']:<20} {layers_str:<30} {result['feature_count']:<10} "
              f"{result['accuracy_mean']:>6.2f}% ± {result['accuracy_std']:<5.2f}  "
              f"{result['log_loss_mean']:>8.4f}")
    
    print("\n" + "=" * 60)
    print("Layer testing complete!")
    print("=" * 60)


def write_layer_test_report(
    output_path: str,
    timestamp: str,
    csv_path: str,
    model_type: str,
    c_value: float,
    results: list,
    layer_info: dict
):
    """Write detailed layer configuration test report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NBA MODEL LAYER CONFIGURATION TEST REPORT\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Training Data: {csv_path}\n")
        f.write(f"Model: {model_type}\n")
        if c_value is not None:
            f.write(f"C-value: {c_value}\n")
        f.write("\n")
        
        # Layer information
        f.write("LAYER INFORMATION\n")
        f.write("-" * 80 + "\n")
        for layer_name, info in layer_info.items():
            f.write(f"{layer_name}:\n")
            f.write(f"  Sets: {', '.join(info['sets'])}\n")
            f.write(f"  Features: {info['feature_count']}\n")
            f.write(f"  Description: {info['description']}\n")
            f.write("\n")
        
        # Results
        f.write("LAYER CONFIGURATION RESULTS (Sorted by Accuracy)\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result['config_name']}\n")
            f.write(f"   Layers: {', '.join(result['layer_names'])}\n")
            f.write(f"   Total Features: {result['feature_count']}\n")
            f.write("\n")
            
            f.write("   Layer Breakdown:\n")
            for layer_name, breakdown in result['layer_breakdown'].items():
                f.write(f"     {layer_name}: {breakdown['feature_count']} features - {breakdown['description']}\n")
            f.write("\n")
            
            f.write("   Performance Metrics:\n")
            f.write(f"     Accuracy: {result['accuracy_mean']:.2f}% ± {result['accuracy_std']:.2f}%\n")
            f.write(f"     Log Loss: {result['log_loss_mean']:.4f} ± {result['log_loss_std']:.4f}\n")
            f.write(f"     Brier:    {result['brier_mean']:.4f} ± {result['brier_std']:.4f}\n")
            f.write("\n")
            
            f.write("   Per-Fold Metrics:\n")
            f.write(f"     Accuracy Folds: {result['accuracy_folds']}\n")
            f.write(f"     Log Loss Folds: {result['log_loss_folds']}\n")
            f.write(f"     Brier Folds:    {result['brier_folds']}\n")
            f.write("\n")
            
            # Top 10 most important features
            f.write("   Top 10 Most Important Features:\n")
            importance = result['feature_importance']
            sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
            for feat_name, imp_score in sorted_importance:
                f.write(f"     {feat_name:30s} | {imp_score:8.4f}\n")
            
            f.write("\n" + "-" * 80 + "\n\n")
        
        # Comparison table
        f.write("COMPARISON TABLE\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Config':<20} {'Accuracy':<15} {'Log Loss':<12} {'Brier':<12} {'Features':<10}\n")
        f.write("-" * 80 + "\n")
        for result in results:
            f.write(f"{result['config_name']:<20} "
                   f"{result['accuracy_mean']:>6.2f}% ± {result['accuracy_std']:<5.2f}  "
                   f"{result['log_loss_mean']:>8.4f}  "
                   f"{result['brier_mean']:>8.4f}  "
                   f"{result['feature_count']:>10d}\n")


def write_ablation_report(
    output_path: str,
    timestamp: str,
    csv_path: str,
    model_type: str,
    c_value: float,
    baseline_results: dict,
    baseline_importance: dict,
    ablation_results: list,
    corr_analysis: dict,
    set_info: dict
):
    """Write detailed ablation study report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NBA MODEL ABLATION STUDY REPORT\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Training Data: {csv_path}\n")
        f.write(f"Model: {model_type}\n")
        if c_value is not None:
            f.write(f"C-value: {c_value}\n")
        f.write("\n")
        
        # Baseline performance
        f.write("BASELINE PERFORMANCE (All Features)\n")
        f.write("-" * 80 + "\n")
        f.write(f"Accuracy: {baseline_results['accuracy_mean']:.2f}% ± {baseline_results['accuracy_std']:.2f}%\n")
        f.write(f"Log Loss: {baseline_results['log_loss_mean']:.4f} ± {baseline_results['log_loss_std']:.4f}\n")
        f.write(f"Brier Score: {baseline_results['brier_mean']:.4f} ± {baseline_results['brier_std']:.4f}\n")
        f.write(f"CV Folds: {baseline_results['n_folds']}\n")
        f.write(f"Per-fold Accuracy: {baseline_results['accuracy_folds']}\n")
        f.write("\n")
        
        # Feature set info
        f.write("FEATURE SET INFORMATION\n")
        f.write("-" * 80 + "\n")
        for set_name, count in sorted(set_info.items()):
            desc = FEATURE_SET_DESCRIPTIONS.get(set_name, '')
            f.write(f"  {set_name:25s} | {count:3d} features | {desc}\n")
        f.write("\n")
        
        # Correlation analysis
        f.write("FEATURE SET CORRELATIONS\n")
        f.write("-" * 80 + "\n")
        set_corrs = corr_analysis['set_correlations']
        set_names = sorted(set_corrs.keys())
        
        # Header
        f.write(" " * 25)
        for set_name in set_names:
            f.write(f" {set_name[:8]:>8s}")
        f.write("\n")
        
        # Rows
        for set1 in set_names:
            f.write(f"{set1[:24]:24s}")
            for set2 in set_names:
                corr = set_corrs[set1][set2]
                f.write(f" {corr:8.3f}")
            f.write("\n")
        f.write("\n")
        
        # Ablation results
        f.write("ABLATION RESULTS (Sorted by Accuracy Impact)\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(ablation_results, 1):
            f.write(f"{i}. {result['set_name']}\n")
            f.write(f"   Description: {result['set_description']}\n")
            f.write(f"   Features Dropped: {result['features_dropped']}\n")
            f.write(f"   Features Remaining: {result['features_remaining']}\n")
            f.write("\n")
            
            f.write("   Performance Metrics:\n")
            f.write(f"     Accuracy: {result['ablated_accuracy']:.2f}% (Δ{result['accuracy_delta']:+.2f}%)\n")
            f.write(f"     Log Loss: {result['ablated_log_loss']:.4f} (Δ{result['log_loss_delta']:+.4f})\n")
            f.write(f"     Brier:    {result['ablated_brier']:.4f} (Δ{result['brier_delta']:+.4f})\n")
            f.write("\n")
            
            f.write("   Per-Fold Metrics:\n")
            f.write(f"     Accuracy Folds: {result['per_fold_accuracy']}\n")
            if result.get('per_fold_log_loss'):
                f.write(f"     Log Loss Folds: {result['per_fold_log_loss']}\n")
            if result.get('per_fold_brier'):
                f.write(f"     Brier Folds:    {result['per_fold_brier']}\n")
            f.write("\n")
            
            # Top importance changes
            f.write("   Top 10 Feature Importance Changes:\n")
            importance_changes = result['importance_changes']
            sorted_changes = sorted(
                importance_changes.items(),
                key=lambda x: abs(x[1]['change']),
                reverse=True
            )[:10]
            
            for feat_name, change_info in sorted_changes:
                f.write(f"     {feat_name:30s} | Baseline: {change_info['baseline']:8.4f} | "
                       f"Ablated: {change_info['ablated']:8.4f} | "
                       f"Change: {change_info['change']:+.4f} ({change_info['change_pct']:+.1f}%)\n")
            
            f.write("\n" + "-" * 80 + "\n\n")
        
        # Summary table
        f.write("SUMMARY TABLE\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Set Name':<25} {'Acc Δ':>8} {'LL Δ':>10} {'Brier Δ':>10} {'Features':>9}\n")
        f.write("-" * 80 + "\n")
        for result in ablation_results:
            f.write(f"{result['set_name']:<25} "
                   f"{result['accuracy_delta']:>+8.2f}% "
                   f"{result['log_loss_delta']:>+10.4f} "
                   f"{result['brier_delta']:>+10.4f} "
                   f"{result['features_dropped']:>9d}\n")


def write_predictions_file(output_path: str, pred_date: str, outputs: list):
    """Write predictions to context file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write(f"NBA PREDICTIONS - {pred_date}\n")
        f.write("=" * 60 + "\n\n")
        
        for output in outputs:
            model_type = output['model_type']
            c_value = output['c_value']
            stats = output['stats']
            predictions = output['predictions']
            
            f.write("-" * 60 + "\n")
            f.write(f"MODEL: {model_type}")
            if c_value is not None:
                f.write(f" (C={c_value})")
            f.write("\n")
            
            if stats.get('accuracy'):
                f.write(f"Training Stats: {stats['accuracy']:.2f}% accuracy")
                if stats.get('accuracy_std'):
                    f.write(f" ± {stats['accuracy_std']:.2f}%")
                if stats.get('log_loss'):
                    f.write(f", log_loss={stats['log_loss']:.4f}")
                f.write("\n")
            
            f.write("-" * 60 + "\n")
            
            for pred in predictions:
                line = format_prediction_line(pred)
                f.write(f"{line}\n")
            
            f.write("\n")


def generate_master_points_mode(args):
    """Generate master points training data CSV."""
    from nba_app.cli.master_training_data_points import (
        generate_master_training_points_data,
        register_existing_master_points_csv,
        MASTER_TRAINING_POINTS_PATH
    )
    from nba_app.cli.Mongo import Mongo
    
    db = Mongo().db
    
    if args.register_only:
        # Just register existing file
        print("Registering existing master points training CSV...")
        metadata = register_existing_master_points_csv(db)
        print(f"Successfully registered master points training data")
    else:
        # Generate new master file
        print("=" * 60)
        print("GENERATING MASTER POINTS TRAINING DATA")
        print("=" * 60)
        print(f"\nOutput will be saved to: {MASTER_TRAINING_POINTS_PATH}\n")
        
        def progress_callback(current, total, progress_pct):
            # Show progress every 50 games, at start, and at end
            if current == 1 or current % 50 == 0 or current == total:
                bar_length = 40
                filled = int(bar_length * current / total) if total > 0 else 0
                bar = '=' * filled + '-' * (bar_length - filled)
                print(f"  [{bar}] {current}/{total} ({progress_pct:.1f}%)", end='\r')
                if current == total:
                    print()  # New line when complete
        
        csv_path, features, game_count = generate_master_training_points_data(
            progress_callback=progress_callback,
            limit=args.limit
        )
        
        print(f"\nSuccessfully generated master points training data:")
        print(f"  File: {csv_path}")
        print(f"  Games: {game_count}")
        print(f"  Features: {len(features)}")
        
        # Register in MongoDB
        from nba_app.cli.master_training_data_points import create_or_update_master_points_metadata
        from datetime import datetime
        
        # Find latest date in CSV
        import pandas as pd
        df = pd.read_csv(csv_path)
        if len(df) > 0:
            df_sorted = df.sort_values(['Year', 'Month', 'Day'], ascending=False)
            latest_row = df_sorted.iloc[0]
            last_date = f"{int(latest_row['Year'])}-{int(latest_row['Month']):02d}-{int(latest_row['Day']):02d}"
        else:
            last_date = datetime.now().strftime('%Y-%m-%d')
        
        create_or_update_master_points_metadata(
            db,
            csv_path,
            features,
            len(features),
            last_date,
            {}
        )
        print(f"  Registered in MongoDB")


def main():
    parser = argparse.ArgumentParser(
        description='NBA Prediction Model CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python train.py train                                        # Train with default models and C-values
  python train.py train --no-per                               # Train without PER features
  python train.py train --model-types LogisticRegression,SVM   # Train specific models
  python train.py train --c-values 0.01,0.1,1.0                # Train with specific C-values
  python train.py train --model-type LogisticRegression --c-value 0.1
  
  python train.py predict                                      # Predict using best cached model
  python train.py predict --no-per                             # Predict using no-PER model
  python train.py predict --date 2025-03-13                    # Predict for specific date
  python train.py predict --model-type SVM --c-value 0.1       # Predict with specific config
  python train.py predict --model-types LogisticRegression,SVM --c-values 0.1,1.0  # Multiple configs
  python train.py predict --exclude-players 4277961,4238338    # Exclude specific players from PER calculations
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Create training data, test models, generate report')
    train_parser.add_argument(
        '--c-value',
        type=float,
        help='Single C-value to use (e.g., 0.01)'
    )
    train_parser.add_argument(
        '--c-values',
        type=str,
        help='Comma-separated C-values to test (e.g., 0.1,0.01,1.0)'
    )
    train_parser.add_argument(
        '--model-type',
        type=str,
        help='Single model type (e.g., LogisticRegression)'
    )
    train_parser.add_argument(
        '--model-types',
        type=str,
        help='Comma-separated model types (e.g., LogisticRegression,GradientBoosting,SVM)'
    )
    train_parser.add_argument(
        '--no-per',
        action='store_true',
        help='Exclude PER (Player Efficiency Rating) features from training'
    )
    train_parser.add_argument(
        '--ablate',
        action='store_true',
        help='Run ablation study: test model performance with each feature set removed'
    )
    train_parser.add_argument(
        '--test-layers',
        action='store_true',
        help='Test layer configurations: compare performance across different layer combinations'
    )
    train_parser.add_argument(
        '--layer-config',
        type=str,
        help='Specific layer config to test (e.g., "layer_1_2" or "layer_1,layer_2"). If not specified with --test-layers, tests all common configs.'
    )
    train_parser.add_argument(
        '--model-specific-features',
        action='store_true',
        help='Use model-specific feature sets (LogisticRegression=differentials, TreeModels=per-team+interactions, NeuralNetworks=structured blocks)'
    )
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Make predictions for a specific date')
    predict_parser.add_argument(
        '--date', '-d',
        type=str,
        help='Date for predictions in YYYY-MM-DD format (default: today)'
    )
    predict_parser.add_argument(
        '--c-value',
        type=float,
        help='Single C-value to use (e.g., 0.01)'
    )
    predict_parser.add_argument(
        '--c-values',
        type=str,
        help='Comma-separated C-values to test (e.g., 0.1,0.01,1.0)'
    )
    predict_parser.add_argument(
        '--model-type',
        type=str,
        help='Single model type (e.g., LogisticRegression)'
    )
    predict_parser.add_argument(
        '--model-types',
        type=str,
        help='Comma-separated model types (e.g., LogisticRegression,GradientBoosting,SVM)'
    )
    predict_parser.add_argument(
        '--no-per',
        action='store_true',
        help='Use model trained without PER features'
    )
    predict_parser.add_argument(
        '--exclude-players',
        type=str,
        help='Comma-separated list of player IDs to exclude from PER calculations (e.g., "4277961,4238338")'
    )
    
    # Generate master points training data command
    master_points_parser = subparsers.add_parser('generate-master-points', help='Generate master points training CSV with all features')
    master_points_parser.add_argument(
        '--register-only',
        action='store_true',
        help='Only register an existing master points CSV file in MongoDB (don\'t generate)'
    )
    master_points_parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit the number of rows to write (for testing/debugging). If not specified, writes all rows.'
    )
    master_points_parser.add_argument(
        '--include-injuries',
        action='store_true',
        help='Include injury impact features in the master training data'
    )
    master_points_parser.add_argument(
        '--recency-decay-k',
        type=float,
        default=15.0,
        help='Recency decay constant for injury features (default: 15.0)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'train':
        if getattr(args, 'ablate', False):
            ablation_mode(args)
        elif getattr(args, 'test_layers', False):
            layer_test_mode(args)
        else:
            train_mode(args)
    elif args.command == 'predict':
        predict_mode(args)
    elif args.command == 'generate-master-points':
        generate_master_points_mode(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

