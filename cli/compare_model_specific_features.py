#!/usr/bin/env python3
"""
Compare all model types with their specific feature sets.

This script runs each model type with its optimized feature set and generates
a comprehensive comparison report.
"""

import sys
import os
from datetime import datetime
import json

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
from nba_app.cli.train import create_model_with_c, evaluate_model_combo, C_SUPPORTED_MODELS, DEFAULT_C_VALUES


# Model types to test with their specific feature sets
MODEL_TYPES_TO_TEST = [
    'LogisticRegression',
    'GradientBoosting',
    'MLPClassifier',  # Neural network
]

# Try to add tree models if available
try:
    import xgboost
    MODEL_TYPES_TO_TEST.append('XGBoost')
except (ImportError, Exception):
    print("Note: XGBoost not available, skipping")

try:
    import lightgbm
    MODEL_TYPES_TO_TEST.append('LightGBM')
except (ImportError, Exception):
    print("Note: LightGBM not available, skipping")

try:
    import catboost
    MODEL_TYPES_TO_TEST.append('CatBoost')
except (ImportError, Exception):
    print("Note: CatBoost not available, skipping")


def run_model_specific_comparison(
    output_dir: str = './model_output',
    no_per: bool = False,
    c_values: list = None
):
    """
    Run all model types with their specific feature sets and compare results.
    
    Args:
        output_dir: Directory for output files
        no_per: If True, exclude PER features
        c_values: List of C-values to test for LogisticRegression (defaults to [0.1, 1.0, 10.0])
    """
    if c_values is None:
        c_values = [0.1, 1.0, 10.0]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join(output_dir, f'model_specific_comparison_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 80)
    print("MODEL-SPECIFIC FEATURE SET COMPARISON")
    print("=" * 80)
    print(f"\nTesting {len(MODEL_TYPES_TO_TEST)} model types:")
    for mt in MODEL_TYPES_TO_TEST:
        print(f"  - {mt}")
    print(f"\nOutput directory: {results_dir}")
    if no_per:
        print("(Running without PER features)")
    print()
    
    # Initialize base model
    model = NBAModel(
        classifier_features=get_default_classifier_features(),
        points_features=None,
        include_elo=True,
        use_exponential_weighting=True,
        # Enhanced features always included (team-level only)
        include_era_normalization=False,
        include_per_features=not no_per,
        output_dir=output_dir
    )
    
    all_results = []
    
    # Test each model type
    for i, model_type in enumerate(MODEL_TYPES_TO_TEST):
        print("\n" + "=" * 80)
        print(f"[{i+1}/{len(MODEL_TYPES_TO_TEST)}] Testing {model_type}")
        print("=" * 80)
        
        # Create model-specific training data
        print(f"\nCreating {model_type}-specific features...")
        csv_filename = f'classifier_training_{model_type.lower()}_{timestamp}.csv'
        if no_per:
            csv_filename = csv_filename.replace('.csv', '_no_per.csv')
        
        csv_path = os.path.join(results_dir, csv_filename)
        
        try:
            count, clf_csv, _ = model.create_training_data_model_specific(
                model_type=model_type,
                classifier_csv=csv_path,
                min_games_filter=0
            )
            print(f"Created training data: {clf_csv} ({count} games)")
        except Exception as e:
            print(f"ERROR creating training data for {model_type}: {e}")
            continue
        
        # Load data
        print(f"\nLoading and evaluating {model_type}...")
        df = pd.read_csv(clf_csv)
        meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
        target_col = 'HomeWon'
        feature_cols = [c for c in df.columns if c not in meta_cols + [target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        print(f"  Features: {len(feature_cols)}")
        print(f"  Samples: {len(X)}")
        
        # Standardize (needed for LogisticRegression and MLPClassifier)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Evaluate model
        if model_type in C_SUPPORTED_MODELS:
            # Test multiple C-values
            best_result = None
            best_acc = -1
            
            for c_val in c_values:
                print(f"  Testing C={c_val}...", end=' ')
                result = evaluate_model_combo(X_scaled, y, model_type, c_val, n_splits=5)
                result['csv_path'] = clf_csv
                result['feature_count'] = len(feature_cols)
                result['sample_count'] = len(X)
                all_results.append(result)
                
                print(f"Acc: {result['accuracy_mean']:.2f}% | LL: {result['log_loss_mean']:.4f}")
                
                if result['accuracy_mean'] > best_acc:
                    best_acc = result['accuracy_mean']
                    best_result = result
        else:
            # Single evaluation
            print(f"  Evaluating...", end=' ')
            result = evaluate_model_combo(X_scaled, y, model_type, None, n_splits=5)
            result['csv_path'] = clf_csv
            result['feature_count'] = len(feature_cols)
            result['sample_count'] = len(X)
            all_results.append(result)
            best_result = result
            
            print(f"Acc: {result['accuracy_mean']:.2f}% | LL: {result['log_loss_mean']:.4f}")
        
        # Store best result for this model type
        if best_result:
            best_result['is_best_for_model'] = True
    
    # Generate comparison report
    print("\n" + "=" * 80)
    print("COMPARISON REPORT")
    print("=" * 80)
    
    # Sort by accuracy
    all_results.sort(key=lambda x: x['accuracy_mean'], reverse=True)
    
    # Create summary table
    print("\n" + "-" * 80)
    print(f"{'Model':<20} {'C':<8} {'Accuracy':<12} {'Log Loss':<12} {'Brier':<12} {'Features':<10}")
    print("-" * 80)
    
    for r in all_results:
        model_str = r['model_type']
        c_str = str(r.get('c_value', 'N/A'))
        acc_str = f"{r['accuracy_mean']:.2f}% ± {r['accuracy_std']:.2f}%"
        ll_str = f"{r['log_loss_mean']:.4f}"
        brier_str = f"{r['brier_mean']:.4f}"
        feat_str = str(r['feature_count'])
        
        marker = " ⭐" if r.get('is_best_for_model') else ""
        print(f"{model_str:<20} {c_str:<8} {acc_str:<12} {ll_str:<12} {brier_str:<12} {feat_str:<10}{marker}")
    
    print("-" * 80)
    
    # Find overall best
    overall_best = all_results[0]
    print(f"\n🏆 Overall Best Model:")
    print(f"   Model: {overall_best['model_type']}")
    if overall_best.get('c_value') is not None:
        print(f"   C-value: {overall_best['c_value']}")
    print(f"   Accuracy: {overall_best['accuracy_mean']:.2f}% ± {overall_best['accuracy_std']:.2f}%")
    print(f"   Log Loss: {overall_best['log_loss_mean']:.4f}")
    print(f"   Brier Score: {overall_best['brier_mean']:.4f}")
    print(f"   Features: {overall_best['feature_count']}")
    
    # Best per model type
    print(f"\n📊 Best Configuration per Model Type:")
    model_best = {}
    for r in all_results:
        mt = r['model_type']
        if mt not in model_best or r['accuracy_mean'] > model_best[mt]['accuracy_mean']:
            model_best[mt] = r
    
    for mt, best_r in sorted(model_best.items()):
        print(f"\n   {mt}:")
        if best_r.get('c_value') is not None:
            print(f"      C-value: {best_r['c_value']}")
        print(f"      Accuracy: {best_r['accuracy_mean']:.2f}% ± {best_r['accuracy_std']:.2f}%")
        print(f"      Log Loss: {best_r['log_loss_mean']:.4f}")
        print(f"      Features: {best_r['feature_count']}")
    
    # Save detailed results to JSON
    json_path = os.path.join(results_dir, 'comparison_results.json')
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n💾 Detailed results saved to: {json_path}")
    
    # Save summary report
    report_path = os.path.join(results_dir, 'comparison_report.txt')
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("MODEL-SPECIFIC FEATURE SET COMPARISON REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Models tested: {', '.join(MODEL_TYPES_TO_TEST)}\n")
        f.write(f"Total configurations: {len(all_results)}\n")
        f.write(f"\n" + "-" * 80 + "\n")
        f.write(f"{'Model':<20} {'C':<8} {'Accuracy':<12} {'Log Loss':<12} {'Brier':<12} {'Features':<10}\n")
        f.write("-" * 80 + "\n")
        
        for r in all_results:
            model_str = r['model_type']
            c_str = str(r.get('c_value', 'N/A'))
            acc_str = f"{r['accuracy_mean']:.2f}% ± {r['accuracy_std']:.2f}%"
            ll_str = f"{r['log_loss_mean']:.4f}"
            brier_str = f"{r['brier_mean']:.4f}"
            feat_str = str(r['feature_count'])
            
            marker = " ⭐" if r.get('is_best_for_model') else ""
            f.write(f"{model_str:<20} {c_str:<8} {acc_str:<12} {ll_str:<12} {brier_str:<12} {feat_str:<10}{marker}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"\n🏆 Overall Best Model:\n")
        f.write(f"   Model: {overall_best['model_type']}\n")
        if overall_best.get('c_value') is not None:
            f.write(f"   C-value: {overall_best['c_value']}\n")
        f.write(f"   Accuracy: {overall_best['accuracy_mean']:.2f}% ± {overall_best['accuracy_std']:.2f}%\n")
        f.write(f"   Log Loss: {overall_best['log_loss_mean']:.4f}\n")
        f.write(f"   Brier Score: {overall_best['brier_mean']:.4f}\n")
        f.write(f"   Features: {overall_best['feature_count']}\n")
        
        f.write(f"\n📊 Best Configuration per Model Type:\n")
        for mt, best_r in sorted(model_best.items()):
            f.write(f"\n   {mt}:\n")
            if best_r.get('c_value') is not None:
                f.write(f"      C-value: {best_r['c_value']}\n")
            f.write(f"      Accuracy: {best_r['accuracy_mean']:.2f}% ± {best_r['accuracy_std']:.2f}%\n")
            f.write(f"      Log Loss: {best_r['log_loss_mean']:.4f}\n")
            f.write(f"      Features: {best_r['feature_count']}\n")
    
    print(f"📄 Summary report saved to: {report_path}")
    print(f"\n✅ Comparison complete! Results in: {results_dir}")
    
    return all_results, results_dir


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare all model types with their specific feature sets')
    parser.add_argument('--no-per', action='store_true', help='Exclude PER features')
    parser.add_argument('--c-values', type=str, help='Comma-separated C-values (e.g., 0.1,1.0,10.0)')
    parser.add_argument('--output-dir', type=str, default='./model_output', help='Output directory')
    
    args = parser.parse_args()
    
    c_values = None
    if args.c_values:
        c_values = [float(c.strip()) for c in args.c_values.split(',')]
    
    run_model_specific_comparison(
        output_dir=args.output_dir,
        no_per=args.no_per,
        c_values=c_values
    )

