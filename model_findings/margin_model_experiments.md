# Margin (Points Regression) Model Experiments

**Date:** January 2026
**Objective:** Create an optimized "margin-only" points regression model to use as `pred_margin` in the ensemble meta-model.

---

## Background

The ensemble meta-model uses `pred_margin` (predicted point differential) as one of its meta-features alongside the base classifier probabilities. The goal was to find the best points regression model configuration that minimizes margin prediction error (MAE/RMSE) on the 2024 evaluation year.

### Time Configuration
- **Training data:** 2010-2021
- **Calibration years:** 2022, 2023
- **Evaluation year:** 2024

---

## Experiments Conducted

### 1. Ridge Alpha Sweep

Tested Ridge regression with different alpha (regularization) values.

| Alpha | Margin MAE | Margin RMSE | R² |
|-------|------------|-------------|-----|
| 0.1 | 11.4436 | 14.7473 | 0.2143 |
| **1.0** | **11.4358** | **14.7322** | **0.2159** |
| 3.0 | 11.4431 | 14.7408 | 0.2150 |
| 10.0 | 11.4688 | 14.7802 | 0.2107 |
| 30.0 | 11.5140 | 14.8410 | 0.2042 |
| 100.0 | 11.5963 | 14.9531 | 0.1921 |

**Finding:** Ridge alpha=1.0 is optimal. Very similar to alpha=2.0 (nearly identical performance).

---

### 2. Comprehensive Model Type Comparison

Ran 24 experiments across different model types and feature configurations.

| Rank | Model Type | Features | Alpha/Params | MAE | RMSE | R² |
|------|------------|----------|--------------|-----|------|-----|
| 1 | Ridge | Full (191) | alpha=1.0 | 11.4358 | 14.7322 | 0.2159 |
| 2 | Ridge | Full (191) | alpha=2.0 | 11.4364 | 14.7356 | 0.2155 |
| 3 | Ridge | Full (191) | alpha=5.0 | 11.4455 | 14.7539 | 0.2135 |
| 4 | Ridge | Full (191) | alpha=10.0 | 11.4688 | 14.7802 | 0.2107 |
| 5-8 | Ridge | Various | Various | ~11.5-11.6 | ~14.8-15.0 | ~0.19-0.21 |
| 9+ | ElasticNet | Various | Various | ~11.5-11.7 | ~14.9-15.1 | ~0.17-0.20 |
| 15+ | RandomForest | Various | Various | ~11.8-12.1 | ~15.2-15.5 | ~0.13-0.16 |
| 20+ | XGBoost | Various | Various | ~11.7-12.0 | ~15.1-15.4 | ~0.14-0.17 |

**Key Findings:**
1. **Ridge dominates** - All top 8 models were Ridge regression
2. **Full features (191) perform best** - More features = better margin prediction
3. **ElasticNet, RandomForest, XGBoost underperformed** compared to simple Ridge
4. **Tree-based models don't help** for this linear prediction task

---

### 3. Margin Model vs Ensemble Performance

**Critical Discovery:** Better margin MAE does NOT equal better ensemble classifier performance.

| Points Model | Margin MAE | Ensemble Accuracy | Ensemble Log Loss |
|--------------|------------|-------------------|-------------------|
| Ridge (alpha=1) | 11.4358 | 70.89% | 0.5571 |
| ElasticNet | 11.5124 | 70.99% | 0.5583 |
| Original | 11.4891 | 70.95% | 0.5570 |

**Insight:** The relationship between margin prediction accuracy and classifier performance is not monotonic. A model with slightly worse MAE can produce better ensemble results due to how the probability estimates interact with base classifiers.

---

## Best Model Configuration

```python
{
    'name': 'Ridge Margin Model (alpha=1)',
    'point_model_id': 'points_model_b92db252-c528-4f45-8608-bcca1a9c0971',
    'selected_margin': True,
    'model_type': 'Ridge',
    'alpha': 1.0,
    'target': 'home_away',
    'begin_year': 2010,
    'calibration_years': [2022, 2023],
    'evaluation_year': 2024,
    'metrics': {
        'margin_mae': 11.4358,
        'margin_rmse': 14.7322,
        'margin_r2': 0.2159
    }
}
```

**Saved to:** `model_config_points_nba` collection with `selected_margin=True`

---

## Key Takeaways

1. **Use Ridge regression for margin prediction** - Simple linear models outperform complex tree-based methods for this task.

2. **Alpha=1.0 is the sweet spot** - Strong enough regularization to prevent overfitting, weak enough to capture signal.

3. **Use all available features** - Unlike classifiers where feature selection helps, margin prediction benefits from more features.

4. **Don't optimize margin MAE in isolation** - Always validate against downstream ensemble performance. The best margin model may not produce the best ensemble.

5. **Margin R² ceiling is ~0.22** - NBA games have high inherent variance. Don't expect dramatic improvements in margin prediction accuracy.

---

## Future Work

1. **Test margin model impact on ensemble calibration** - Does a better-calibrated margin model improve ensemble probability calibration?

2. **Explore interaction features** - Could engineered features (e.g., margin * rest_days) improve predictions?

3. **Time-varying models** - Does a model trained on more recent data (2018+) outperform one trained on all historical data?

4. **Ensemble of margin models** - Would blending multiple margin models (Ridge + ElasticNet) help?

---

## Code References

- Experiment runner: `agents/tools/experiment_runner.py`
- Points regression trainer: `core/models/points_regression.py`
- Model configs collection: `model_config_points_nba`
