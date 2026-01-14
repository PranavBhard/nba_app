# Tree Models Quick Reference

## 🚀 Command Format

```bash
python train.py train --model-type <MODEL_TYPE> --model-specific-features
```

## 📋 Available Tree Models

### Built-in (No Installation Required)

```bash
# GradientBoosting
python train.py train --model-type GradientBoosting --model-specific-features

# RandomForest
python train.py train --model-type RandomForest --model-specific-features
```

### Advanced (Require Installation)

**First install:**
```bash
pip install xgboost lightgbm catboost
```

**Then test:**
```bash
# XGBoost
python train.py train --model-type XGBoost --model-specific-features

# LightGBM
python train.py train --model-type LightGBM --model-specific-features

# CatBoost
python train.py train --model-type CatBoost --model-specific-features
```

## 📊 All Tree Models at Once

```bash
# Test all built-in models
python train.py train --model-types GradientBoosting,RandomForest --model-specific-features

# Note: --model-specific-features only works with single model type
# So test them one at a time:
python train.py train --model-type GradientBoosting --model-specific-features
python train.py train --model-type RandomForest --model-specific-features
python train.py train --model-type XGBoost --model-specific-features
python train.py train --model-type LightGBM --model-specific-features
python train.py train --model-type CatBoost --model-specific-features
```

## ✅ Quick Test Checklist

- [ ] GradientBoosting (built-in)
- [ ] RandomForest (built-in)
- [ ] XGBoost (`pip install xgboost`)
- [ ] LightGBM (`pip install lightgbm`)
- [ ] CatBoost (`pip install catboost`)

## 🎯 Example: Test All Tree Models

```bash
# 1. Install advanced models
pip install xgboost lightgbm catboost

# 2. Test each one
python train.py train --model-type GradientBoosting --model-specific-features
python train.py train --model-type RandomForest --model-specific-features
python train.py train --model-type XGBoost --model-specific-features
python train.py train --model-type LightGBM --model-specific-features
python train.py train --model-type CatBoost --model-specific-features
```

