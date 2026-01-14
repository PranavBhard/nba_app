# Testing Layers with XGBoost

## 🚀 Quick Start

### Test Specific Layer Configuration
```bash
python train.py train --test-layers --layer-config layer_1,schedule_fatigue,sample_size --model-type XGBoost
```

### Test All Common Configurations
```bash
python train.py train --test-layers --model-type XGBoost
```

## 📋 Available Layer Configurations

### Single Layers
```bash
# Layer 1 only (core strength)
python train.py train --test-layers --layer-config layer_1 --model-type XGBoost

# Layer 2 only (context)
python train.py train --test-layers --layer-config layer_2 --model-type XGBoost
```

### Layer Combinations
```bash
# Layer 1 + Layer 2 (core + context)
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type XGBoost

# Layer 1 + Layer 3 (core + meta)
python train.py train --test-layers --layer-config layer_1,layer_3 --model-type XGBoost

# All layers
python train.py train --test-layers --layer-config layer_1,layer_2,layer_3,layer_4 --model-type XGBoost
```

### Individual Feature Sets
```bash
# Test specific feature sets
python train.py train --test-layers --layer-config outcome_strength,schedule_fatigue --model-type XGBoost

# Mix layers and feature sets
python train.py train --test-layers --layer-config layer_1,schedule_fatigue,sample_size --model-type XGBoost
```

## 🎯 Best Practices

### 1. Start with Baseline
```bash
# Test Layer 1 only (baseline)
python train.py train --test-layers --layer-config layer_1 --model-type XGBoost
```

### 2. Add Layers Incrementally
```bash
# Add Layer 2
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type XGBoost

# Compare results
```

### 3. Test Optimal Configuration (from Phase 4)
```bash
# Best config from Phase 4: outcome_strength + shooting_efficiency + schedule_fatigue + sample_size
python train.py train --test-layers --layer-config outcome_strength,shooting_efficiency,schedule_fatigue,sample_size --model-type XGBoost
```

## 📊 Understanding Results

After running layer tests, you'll get a report showing:

1. **Performance Metrics**:
   - Accuracy (mean ± std dev)
   - Log Loss
   - Brier Score

2. **Feature Counts**:
   - Total features in each configuration
   - Features per layer/set

3. **Feature Importance**:
   - Top 10 most important features for each config

4. **Comparison Table**:
   - All configurations ranked by accuracy

## 🔍 Example: Testing Phase 4 Best Config with XGBoost

```bash
# Test the best configuration from Phase 4 (70.33% with LogisticRegression)
python train.py train --test-layers \
  --layer-config outcome_strength,shooting_efficiency,schedule_fatigue,sample_size \
  --model-type XGBoost
```

**Expected Output:**
- Report showing XGBoost performance with this feature set
- Comparison to LogisticRegression results
- Feature importance for XGBoost

## ⚠️ Important Notes

### Model-Specific Features vs. Layer Testing

**Layer testing uses STANDARD feature sets** (not model-specific):
- Features are organized by layers/sets
- Same features regardless of model type
- Good for comparing models on same feature set

**Model-specific features** (`--model-specific-features`):
- Different feature structure per model type
- Tree models get per-team + interactions
- LogisticRegression gets differentials
- **NOT compatible with layer testing** (they use different feature structures)

### When to Use Each

**Use Layer Testing when:**
- Comparing different models on same feature set
- Testing which feature categories help
- Finding optimal feature combinations
- Systematic feature selection

**Use Model-Specific Features when:**
- Optimizing for specific model type
- Want per-team features for tree models
- Want differentials for linear models
- Single model type testing

## 📈 Example Workflow

### Step 1: Test XGBoost with Best Layer Config
```bash
python train.py train --test-layers \
  --layer-config outcome_strength,shooting_efficiency,schedule_fatigue,sample_size \
  --model-type XGBoost
```

### Step 2: Compare to LogisticRegression
```bash
python train.py train --test-layers \
  --layer-config outcome_strength,shooting_efficiency,schedule_fatigue,sample_size \
  --model-type LogisticRegression --c-value 0.1
```

### Step 3: Test XGBoost with Model-Specific Features
```bash
# This uses per-team + interaction features (different structure)
python train.py train --model-type XGBoost --model-specific-features
```

### Step 4: Compare Results
- Layer test: XGBoost with standard features
- Model-specific: XGBoost with optimized features
- See which performs better!

## 🎯 Quick Reference

```bash
# Test single layer
--layer-config layer_1

# Test multiple layers
--layer-config layer_1,layer_2

# Test specific feature sets
--layer-config outcome_strength,schedule_fatigue

# Test with XGBoost
--model-type XGBoost

# Test all common configs
--test-layers (no --layer-config)
```

## 💡 Pro Tips

1. **Start simple**: Test layer_1 first, then add layers
2. **Compare models**: Test same config with different models
3. **Check feature importance**: See which features XGBoost values most
4. **Compare to baseline**: Always compare to LogisticRegression (70.33%)
5. **Use Phase 4 results**: Test the best configs from Phase 4

