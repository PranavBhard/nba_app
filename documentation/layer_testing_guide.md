# Layer Configuration Testing Guide

This guide explains how to systematically test different layer configurations for the NBA prediction model.

## Layer Hierarchy

The feature sets are organized into 4 conceptual layers:

### Layer 1: Outcome & Ratings (Core Strength Comparison)
- **Sets**: `outcome_strength`, `shooting_efficiency`, `offensive_engine`, `defensive_engine`
- **Purpose**: Core team performance metrics - what actually happened and how efficiently
- **Feature Count**: ~60-70 features

### Layer 2: Tempo, Schedule, Sample Size (Situational Context)
- **Sets**: `pace_volatility`, `schedule_fatigue`, `sample_size`
- **Purpose**: Contextual factors that modify predictions (rest, fatigue, tempo, data reliability)
- **Feature Count**: ~20 features

### Layer 3: Meta Priors & Normalization (Global Calibration)
- **Sets**: `elo_strength`, `era_normalization`
- **Purpose**: High-level strength signals and cross-era comparability
- **Feature Count**: ~7 features

### Layer 4: Player Talent & Absolute Magnitudes (Detailed Structure)
- **Sets**: `player_talent`, `absolute_magnitude`
- **Purpose**: Player-level metrics and absolute performance context
- **Feature Count**: ~35 features

## Testing Strategy

### Step 1: Baseline - Layer 1 Only

Test the core strength signals alone:

```bash
python train.py train --test-layers --layer-config layer_1
```

**What to look for:**
- How well do outcome/ratings features perform in isolation?
- This establishes the baseline performance floor

### Step 2: Add Layer 2 (First + Second Layer)

Test core strength + situational context:

```bash
python train.py train --test-layers --layer-config layer_1,layer_2
```

**What to look for:**
- Does adding situational context (rest, schedule, pace) improve predictions?
- How much lift does Layer 2 provide over Layer 1 alone?
- This tests the hypothesis that context matters beyond raw strength

### Step 3: Compare All Common Configurations

Test all predefined layer combinations:

```bash
python train.py train --test-layers
```

This tests:
- `layer_1_only`: Core strength only
- `layer_1_2`: Core + context
- `layer_1_2_3`: Core + context + meta priors
- `layer_1_2_4`: Core + context + player talent
- `all_layers`: Everything
- `core_only`: Layer 1 + Layer 3 (skip context)
- `context_heavy`: Layer 1 + Layer 2 + Layer 4 (skip era normalization)

### Step 4: Analyze Results

The layer test report (`model_output/layer_test_TIMESTAMP.txt`) includes:

1. **Performance Comparison**: Accuracy, log loss, Brier score for each config
2. **Per-Fold Metrics**: CV fold breakdowns to assess stability
3. **Feature Importance**: Top features for each configuration
4. **Layer Breakdown**: Feature counts per layer in each config

## Key Questions to Answer

### For First Layer (Layer 1):
1. **Is Layer 1 sufficient?** What's the accuracy with just core strength metrics?
2. **Which sets in Layer 1 matter most?** Use ablation study to see impact of each set

### For Second Layer (Layer 2):
1. **Does Layer 2 add value?** Compare `layer_1` vs `layer_1_2`
2. **Which Layer 2 sets matter?** Test:
   - `layer_1` + `pace_volatility` only
   - `layer_1` + `schedule_fatigue` only
   - `layer_1` + `sample_size` only

### For Layer Combinations:
1. **Is Layer 2 more valuable than Layer 3?** Compare `layer_1_2` vs `layer_1_3`
2. **Does Layer 4 (player talent) add value beyond Layer 1?** Compare `layer_1` vs `layer_1_4`
3. **What's the optimal configuration?** Find the best accuracy/complexity tradeoff

## Recommended Testing Sequence

### Quick Test (5-10 minutes)
```bash
# Test just first and second layers
python train.py train --test-layers --layer-config layer_1
python train.py train --test-layers --layer-config layer_1,layer_2
```

### Comprehensive Test (30-60 minutes)
```bash
# Test all common configurations
python train.py train --test-layers

# Then run ablation to understand which sets within layers matter
python train.py train --ablate
```

### Deep Dive (2+ hours)
```bash
# Test all common configs
python train.py train --test-layers

# Ablation study for each layer
python train.py train --ablate

# Test custom combinations
python train.py train --test-layers --layer-config layer_1,layer_3  # Core + meta
python train.py train --test-layers --layer-config layer_1,layer_4  # Core + players
python train.py train --test-layers --layer-config layer_2,layer_3  # Context + meta
```

## Interpreting Results

### Performance Metrics
- **Accuracy**: Higher is better (target: >65% for NBA)
- **Log Loss**: Lower is better (measures probability calibration)
- **Brier Score**: Lower is better (measures probability accuracy)

### Feature Count vs Performance
- **More features ≠ better performance**
- Look for the configuration with best accuracy/complexity tradeoff
- If adding a layer only improves by 0.1% but adds 20 features, it may not be worth it

### Stability
- Check per-fold metrics: large std dev indicates instability
- Prefer configurations with consistent performance across folds

## Example Workflow

```bash
# 1. Quick sanity check: Layer 1 baseline
python train.py train --test-layers --layer-config layer_1 --model-type GradientBoosting

# 2. Test Layer 1 + Layer 2 (your main question)
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type GradientBoosting

# 3. Compare to all layers
python train.py train --test-layers --model-type GradientBoosting

# 4. If Layer 2 shows promise, do ablation to see which sets matter
python train.py train --ablate --model-type GradientBoosting

# 5. Test with different models
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.1
```

## Output Files

- `model_output/layer_test_TIMESTAMP.txt`: Detailed comparison report
- Console output: Quick summary table sorted by accuracy

## Tips

1. **Start simple**: Test Layer 1 first to establish baseline
2. **Add incrementally**: Test Layer 1+2, then add Layer 3, then Layer 4
3. **Compare models**: Test same layer configs with different model types
4. **Check stability**: Look at per-fold metrics, not just averages
5. **Consider complexity**: More features = more overfitting risk, slower training

