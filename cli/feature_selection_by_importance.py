#!/usr/bin/env python3
"""
Feature Selection by Importance

Tests model performance with top N features selected by importance.
Useful for Phase 4.2 of optimization testing.
"""

import sys
import os
from datetime import datetime

# Add project root to path
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss

from nba_app.cli.NBAModel import NBAModel, get_default_classifier_features
from nba_app.cli.train import create_model_with_c, evaluate_model_combo


def get_feature_importance(model, feature_names: list, model_type: str) -> dict:
    """Get feature importance from trained model."""
    importance = {}
    
    if model_type == 'GradientBoosting':
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            for name, imp in zip(feature_names, importances):
                importance[name] = float(imp)
    elif model_type == 'LogisticRegression':
        # Use absolute coefficient values
        if hasattr(model, 'coef_'):
            coefs = np.abs(model.coef_[0])
            for name, coef in zip(feature_names, coefs):
                importance[name] = float(coef)
    elif model_type in ['RandomForest', 'XGBoost', 'LightGBM', 'CatBoost']:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            for name, imp in zip(feature_names, importances):
                importance[name] = float(imp)
    
    return importance


def feature_selection_by_importance(
    csv_path: str,
    model_type: str = 'LogisticRegression',
    c_value: float = 0.1,
    top_n_values: list = None,
    output_dir: str = './model_output'
):
    """
    Test model performance with top N features by importance.
    
    Args:
        csv_path: Path to training CSV
        model_type: Model type to use
        c_value: C-value for LogisticRegression
        top_n_values: List of N values to test (e.g., [20, 30, 40, 50])
        output_dir: Output directory for results
    """
    if top_n_values is None:
        top_n_values = [20, 30, 40, 50, 60]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join(output_dir, f'feature_selection_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 80)
    print("FEATURE SELECTION BY IMPORTANCE")
    print("=" * 80)
    print(f"\nModel: {model_type}")
    if c_value is not None:
        print(f"C-value: {c_value}")
    print(f"Testing top N features: {top_n_values}")
    print(f"Output directory: {results_dir}\n")
    
    # Load data
    print("Loading data...")
    df = pd.read_csv(csv_path)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    target_col = 'HomeWon'
    feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
    
    X = df[feature_cols].values
    y = df[target_col].values
    
    print(f"  Total features: {len(feature_cols)}")
    print(f"  Samples: {len(X)}\n")
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train full model to get feature importances
    print("Training full model to compute feature importances...")
    full_model = create_model_with_c(model_type, c_value)
    full_model.fit(X_scaled, y)
    
    # Get feature importances
    importances = get_feature_importance(full_model, feature_cols, model_type)
    
    # Sort features by importance
    sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTop 10 Most Important Features:")
    print("-" * 80)
    for i, (feat, imp) in enumerate(sorted_features[:10], 1):
        print(f"  {i:2d}. {feat:<50} {imp:.6f}")
    print()
    
    # Test with top N features
    results = []
    
    print("Testing configurations with top N features...")
    print("-" * 80)
    print(f"{'Top N':<8} {'Features':<10} {'Accuracy':<15} {'Log Loss':<12} {'Brier':<12}")
    print("-" * 80)
    
    for top_n in top_n_values:
        if top_n > len(feature_cols):
            continue
        
        # Select top N features
        top_features = [feat for feat, _ in sorted_features[:top_n]]
        feature_indices = [i for i, f in enumerate(feature_cols) if f in top_features]
        X_selected = X_scaled[:, feature_indices]
        
        # Evaluate
        result = evaluate_model_combo(X_selected, y, model_type, c_value, n_splits=5)
        result['top_n'] = top_n
        result['selected_features'] = top_features
        result['feature_count'] = top_n
        results.append(result)
        
        print(f"{top_n:<8} {top_n:<10} {result['accuracy_mean']:.2f}% ± {result['accuracy_std']:.2f}%  "
              f"{result['log_loss_mean']:.4f}      {result['brier_mean']:.4f}")
    
    print("-" * 80)
    
    # Find best
    best_result = max(results, key=lambda x: x['accuracy_mean'])
    print(f"\n🏆 Best Configuration:")
    print(f"   Top N: {best_result['top_n']}")
    print(f"   Accuracy: {best_result['accuracy_mean']:.2f}% ± {best_result['accuracy_std']:.2f}%")
    print(f"   Log Loss: {best_result['log_loss_mean']:.4f}")
    print(f"   Brier: {best_result['brier_mean']:.4f}")
    
    # Save results
    import json
    json_path = os.path.join(results_dir, 'feature_selection_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save feature list for best config
    best_features_path = os.path.join(results_dir, f'top_{best_result["top_n"]}_features.txt')
    with open(best_features_path, 'w') as f:
        f.write(f"Top {best_result['top_n']} Features by Importance\n")
        f.write("=" * 80 + "\n\n")
        for i, (feat, imp) in enumerate(sorted_features[:best_result['top_n']], 1):
            f.write(f"{i:3d}. {feat:<50} {imp:.6f}\n")
    
    print(f"\n💾 Results saved to: {results_dir}")
    print(f"📄 Best feature list: {best_features_path}")
    
    return results, results_dir


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Feature selection by importance')
    parser.add_argument('--csv', type=str, required=True, help='Path to training CSV')
    parser.add_argument('--model-type', type=str, default='LogisticRegression', help='Model type')
    parser.add_argument('--c-value', type=float, default=0.1, help='C-value for LogisticRegression')
    parser.add_argument('--top-n', type=str, help='Comma-separated top N values (e.g., 20,30,40,50)')
    parser.add_argument('--output-dir', type=str, default='./model_output', help='Output directory')
    
    args = parser.parse_args()
    
    top_n_values = None
    if args.top_n:
        top_n_values = [int(n.strip()) for n in args.top_n.split(',')]
    
    feature_selection_by_importance(
        csv_path=args.csv,
        model_type=args.model_type,
        c_value=args.c_value,
        top_n_values=top_n_values,
        output_dir=args.output_dir
    )

