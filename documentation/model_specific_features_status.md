# Model-Specific Feature Sets Status

## ✅ Implemented Feature Builders

### 1. LogisticRegressionFeatureBuilder
**Model Types:** `LogisticRegression`
- **Strategy:** Pure differential modeling + optional absolutes
- **Features:** All differentials (stat diffs, enhanced diffs, Elo diff, rest diff)
- **Status:** ✅ Fully implemented

### 2. TreeModelFeatureBuilder
**Model Types:** 
- `GradientBoosting`
- `XGBoost`
- `LightGBM`
- `CatBoost`
- `RandomForest`

**Strategy:** RAW per-team features + differentials + explicit interactions
- **Features:**
  - Per-team blocks (home_off_rtg, away_def_rtg, etc.)
  - Differential features (off_rtgDiff, def_rtgDiff, etc.)
  - Crossed interaction features (home_off_rtg_x_away_def_rtg, etc.)
  - PER aggregates (per-team, not diff)
- **Status:** ✅ Fully implemented

### 3. NeuralNetworkFeatureBuilder
**Model Types:**
- `NeuralNetwork`
- `MLPClassifier`

**Strategy:** Structured per-team blocks
- **Features:** Dictionary with 'home' and 'away' keys, each containing per-team features
- **Status:** ✅ Fully implemented

---

## ⚠️ Models Without Explicit Feature Builders

### 4. SVM (Support Vector Machine)
**Model Type:** `SVM`
- **Current Behavior:** Defaults to `LogisticRegressionFeatureBuilder` (line 470-473 in `model_specific_features.py`)
- **Rationale:** SVM is a linear model like LogisticRegression, so differential features are appropriate
- **Status:** ⚠️ Works but not explicitly handled
- **Recommendation:** Add explicit SVM support (same as LogisticRegression)

### 5. NaiveBayes
**Model Type:** `NaiveBayes`
- **Current Behavior:** Defaults to `LogisticRegressionFeatureBuilder`
- **Rationale:** NaiveBayes can work with differential features, but might benefit from different structure
- **Status:** ⚠️ Works but not explicitly handled
- **Recommendation:** Test if differential features work well, or create separate builder

---

## 📋 Integration Status

### ✅ Fully Integrated
- **train_mode:** Model-specific features work with `--model-specific-features` flag
- **predict_mode:** Can use model-specific feature CSVs for prediction

### ❌ NOT Integrated
- **layer_test_mode:** Layer testing uses standard feature sets (not model-specific)
- **ablation_mode:** Ablation studies use standard feature sets (not model-specific)
- **Optimization test scripts:** Phase 1-4 tests use standard feature sets (not model-specific)

---

## 🔧 How to Use Model-Specific Features

### Training with Model-Specific Features
```bash
# Train LogisticRegression with differential features
python train.py train --model-type LogisticRegression --model-specific-features

# Train GradientBoosting with per-team + interaction features
python train.py train --model-type GradientBoosting --model-specific-features

# Train NeuralNetwork with structured features
python train.py train --model-type NeuralNetwork --model-specific-features
```

### Current Limitations
1. **Only works with single model type** (not multiple model types at once)
2. **Not integrated with layer testing** (uses standard feature sets)
3. **Not integrated with ablation studies** (uses standard feature sets)
4. **Not integrated with optimization tests** (Phase 1-4 use standard features)

---

## 🎯 Recommendations

### 1. Add Explicit SVM Support
```python
# In get_feature_builder():
elif model_type == 'SVM':
    return LogisticRegressionFeatureBuilder(...)  # Same as LR
```

### 2. Integrate with Layer Testing
- Add `--model-specific-features` flag to `layer_test_mode`
- Use model-specific builders when flag is set

### 3. Integrate with Ablation Studies
- Add `--model-specific-features` flag to `ablation_mode`
- Use model-specific builders when flag is set

### 4. Integrate with Optimization Tests
- Update `run_optimization_tests.sh` to support model-specific features
- Test if model-specific features improve performance in Phase 1-4

### 5. Test NaiveBayes
- Determine if differential features work well
- Or create separate feature builder if needed

---

## 📊 Feature Set Comparison

| Model Type | Feature Builder | Strategy | Features |
|------------|----------------|----------|----------|
| LogisticRegression | ✅ LogisticRegressionFeatureBuilder | Differentials | ~60-80 diffs |
| SVM | ⚠️ LogisticRegressionFeatureBuilder (default) | Differentials | ~60-80 diffs |
| GradientBoosting | ✅ TreeModelFeatureBuilder | Per-team + interactions | ~100-150 features |
| XGBoost | ✅ TreeModelFeatureBuilder | Per-team + interactions | ~100-150 features |
| LightGBM | ✅ TreeModelFeatureBuilder | Per-team + interactions | ~100-150 features |
| CatBoost | ✅ TreeModelFeatureBuilder | Per-team + interactions | ~100-150 features |
| RandomForest | ✅ TreeModelFeatureBuilder | Per-team + interactions | ~100-150 features |
| NeuralNetwork | ✅ NeuralNetworkFeatureBuilder | Structured blocks | Dictionary format |
| MLPClassifier | ✅ NeuralNetworkFeatureBuilder | Structured blocks | Dictionary format |
| NaiveBayes | ⚠️ LogisticRegressionFeatureBuilder (default) | Differentials | ~60-80 diffs |

---

## 🚀 Next Steps

1. **Add explicit SVM support** (5 minutes)
2. **Test NaiveBayes with differential features** (10 minutes)
3. **Integrate model-specific features with layer testing** (30 minutes)
4. **Integrate model-specific features with ablation studies** (30 minutes)
5. **Update optimization test scripts** (1 hour)
6. **Run Phase 1-4 with model-specific features** (2-3 hours)

