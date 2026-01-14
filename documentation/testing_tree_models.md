# Testing Tree Models Guide

This guide explains how to test different tree-based models (GradientBoosting, XGBoost, LightGBM, CatBoost, RandomForest) with the NBA prediction model.

## 🌳 Available Tree Models

### Built-in (sklearn)
- ✅ **GradientBoosting** - Always available
- ✅ **RandomForest** - Always available

### Advanced (require installation)
- ⚠️ **XGBoost** - Requires `pip install xgboost`
- ⚠️ **LightGBM** - Requires `pip install lightgbm`
- ⚠️ **CatBoost** - Requires `pip install catboost`

---

## 📦 Installation

### Install All Tree Models
```bash
pip install xgboost lightgbm catboost
```

### Install Individual Models
```bash
# XGBoost only
pip install xgboost

# LightGBM only
pip install lightgbm

# CatBoost only
pip install catboost
```

---

## 🚀 Quick Start: Test Individual Tree Models

### Test GradientBoosting (Built-in)
```bash
# With standard features
python train.py train --model-type GradientBoosting

# With model-specific features (per-team + interactions)
python train.py train --model-type GradientBoosting --model-specific-features
```

### Test RandomForest (Built-in)
```bash
# With standard features
python train.py train --model-type RandomForest

# With model-specific features (per-team + interactions)
python train.py train --model-type RandomForest --model-specific-features
```

### Test XGBoost (Requires Installation)
```bash
# First install: pip install xgboost

# With standard features
python train.py train --model-type XGBoost

# With model-specific features (per-team + interactions)
python train.py train --model-type XGBoost --model-specific-features
```

### Test LightGBM (Requires Installation)
```bash
# First install: pip install lightgbm

# With standard features
python train.py train --model-type LightGBM

# With model-specific features (per-team + interactions)
python train.py train --model-type LightGBM --model-specific-features
```

### Test CatBoost (Requires Installation)
```bash
# First install: pip install catboost

# With standard features
python train.py train --model-type CatBoost

# With model-specific features (per-team + interactions)
python train.py train --model-type CatBoost --model-specific-features
```

---

## 🔬 Compare All Tree Models

### Option 1: Test Multiple Models at Once
```bash
# Test all built-in tree models
python train.py train --model-types GradientBoosting,RandomForest

# Test with model-specific features (one at a time)
python train.py train --model-type GradientBoosting --model-specific-features
python train.py train --model-type RandomForest --model-specific-features
python train.py train --model-type XGBoost --model-specific-features
python train.py train --model-type LightGBM --model-specific-features
python train.py train --model-type CatBoost --model-specific-features
```

### Option 2: Use Comparison Script
```bash
# Compare all available models with their specific feature sets
python cli/compare_model_specific_features.py

# Without PER features
python cli/compare_model_specific_features.py --no-per
```

This script will:
- Automatically detect which tree models are installed
- Test each with its optimized feature set
- Generate a comparison report

---

## 📊 Layer Testing with Tree Models

### Test Layer Configurations
```bash
# Test with GradientBoosting (default)
python train.py train --test-layers --layer-config layer_1,schedule_fatigue,sample_size --model-type GradientBoosting

# Test with XGBoost
python train.py train --test-layers --layer-config layer_1,schedule_fatigue,sample_size --model-type XGBoost

# Test with LightGBM
python train.py train --test-layers --layer-config layer_1,schedule_fatigue,sample_size --model-type LightGBM
```

**Note:** Layer testing currently uses standard feature sets, not model-specific features.

---

## 🎯 Model-Specific Features for Tree Models

Tree models use the **TreeModelFeatureBuilder** which provides:

### Features Included:
1. **Per-team blocks** (PRIMARY):
   - `home_off_rtg`, `home_def_rtg`, `home_pace`, etc.
   - `away_off_rtg`, `away_def_rtg`, `away_pace`, etc.

2. **Differential features** (SECONDARY):
   - `off_rtgDiff`, `def_rtgDiff`, `paceDiff`, etc.

3. **Interaction features**:
   - `home_off_rtg_x_away_def_rtg`
   - `home_efg_x_away_efg_def`
   - `home_pace_x_away_pace`
   - And more...

4. **PER aggregates** (per-team, not diff):
   - `home_team_per_avg`, `away_team_per_avg`
   - `home_starters_per_avg`, `away_starters_per_avg`
   - Top 5 PER players per team

5. **Elo** (per-team + diff):
   - `home_elo`, `away_elo`, `eloDiff`

### Why This Structure?
- **Tree models excel at finding interactions** - giving them per-team features allows the model to learn complex relationships
- **Differentials are still useful** - but trees can also learn from raw per-team values
- **Explicit interactions** help the model understand matchups (e.g., strong offense vs. strong defense)

---

## 📈 Expected Performance

Based on the feature architecture:

| Model | Expected Accuracy | Notes |
|-------|------------------|-------|
| GradientBoosting | ~69-70% | Baseline tree model |
| RandomForest | ~68-69% | More variance, less overfitting |
| XGBoost | ~70-71% | Often best performance |
| LightGBM | ~70-71% | Fast, good performance |
| CatBoost | ~70-71% | Handles categoricals well |

**Note:** Actual performance depends on:
- Feature set used (standard vs. model-specific)
- Hyperparameters
- Data quality

---

## 🔍 Troubleshooting

### "Unknown model type: XGBoost"
**Solution:** Install XGBoost: `pip install xgboost`

### "XGBoost not installed"
**Solution:** The model is not installed. Install with: `pip install xgboost`

### Model-specific features not working
**Check:**
1. Are you using `--model-specific-features` flag?
2. Are you testing only ONE model type at a time?
3. Check the output CSV - it should have different feature names for tree models

### Performance is worse than expected
**Try:**
1. Use model-specific features: `--model-specific-features`
2. Test with different hyperparameters (may need to modify code)
3. Check if features are being created correctly

---

## 💡 Best Practices

1. **Start with GradientBoosting** - It's built-in and works well
2. **Test model-specific features** - Tree models perform better with per-team features
3. **Compare multiple models** - Use the comparison script to see which works best
4. **Check feature importance** - Tree models provide feature importance scores
5. **Consider hyperparameter tuning** - Tree models have many hyperparameters to tune

---

## 📝 Example: Full Comparison Test

```bash
# 1. Install all tree models
pip install xgboost lightgbm catboost

# 2. Test each with model-specific features
python train.py train --model-type GradientBoosting --model-specific-features
python train.py train --model-type RandomForest --model-specific-features
python train.py train --model-type XGBoost --model-specific-features
python train.py train --model-type LightGBM --model-specific-features
python train.py train --model-type CatBoost --model-specific-features

# 3. Or use the comparison script
python cli/compare_model_specific_features.py
```

---

## 🎯 Next Steps

After testing tree models:
1. Compare results to LogisticRegression (70.33% with 42 features)
2. Check if model-specific features improve performance
3. Consider hyperparameter tuning for the best model
4. Test on new data to validate performance

