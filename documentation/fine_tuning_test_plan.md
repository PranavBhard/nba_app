# Fine-Tuning Test Plan & Model Explanation

## Understanding the Models: LogisticRegression vs GradientBoosting

### GradientBoosting (Currently Used)
**What it is:**
- **Ensemble tree-based model** that builds many decision trees sequentially
- Each new tree tries to correct the mistakes of previous trees
- **Non-linear**: Can capture complex interactions between features
- **Feature interactions**: Automatically finds relationships like "if winsMonths_1Diff is high AND schedule_fatigue is low, then..."
- **No explicit regularization** in current setup (uses 100 trees, no max_depth limit mentioned)

**Strengths:**
- Handles non-linear relationships well
- Captures feature interactions automatically
- Good for complex patterns
- Feature importance scores are meaningful

**Weaknesses:**
- Can overfit easily (especially with many features)
- Less interpretable (black box)
- Slower to train
- May memorize noise in data

**Current Usage:**
- Used for all layer tests
- Default: 100 trees, random_state=42
- No regularization parameters tuned

---

### LogisticRegression
**What it is:**
- **Linear model** that finds a weighted combination of features
- Uses a sigmoid function to output probabilities
- **Linear decision boundary**: Can only learn linear relationships
- **Regularization built-in**: L1 (sparse) or L2 (smooth) via C parameter
  - C = 0.01 → Strong regularization (simpler model, less overfitting)
  - C = 1.0 → Default regularization
  - C = 10.0 → Weak regularization (more complex, risk of overfitting)

**Strengths:**
- Fast to train
- Highly interpretable (coefficients show feature importance)
- Built-in regularization prevents overfitting
- Good baseline model
- Works well when relationships are roughly linear

**Weaknesses:**
- Can't capture complex non-linear patterns
- Can't automatically find feature interactions
- May underfit if relationships are complex

**Current Usage:**
- Available but NOT tested in layer configurations
- Only tested in main training mode with different C-values

---

### Are We Using a Combo?
**No, we're NOT using a combo currently.** We're only using GradientBoosting for layer tests.

**Why this matters:**
- GradientBoosting might be overfitting with 66+ features
- LogisticRegression with regularization might perform better
- We should test BOTH models on the same layer configs to compare

---

## What We Want to Know: Key Questions

### 1. Feature Set Granularity
**Question:** Which specific feature sets help, not just which layers?
- Layer 2 has 3 sets: `pace_volatility`, `schedule_fatigue`, `sample_size`
- We know Layer 2 helps, but which of these 3 sets is doing the work?
- **Insight needed:** Can we reduce from 20 Layer 2 features to just the useful ones?

### 2. Model Comparison
**Question:** Is GradientBoosting the right model, or would LogisticRegression be better?
- GradientBoosting might be overfitting
- LogisticRegression with regularization might generalize better
- **Insight needed:** Which model performs better on layer_1_2 with proper regularization?

### 3. Feature Redundancy
**Question:** Are many Layer 1 features redundant given the dominance of `winsMonths_1Diff`?
- One feature has 82% importance
- Other 45 features might be noise
- **Insight needed:** Can we reduce Layer 1 features while maintaining performance?

### 4. Layer Approach Value
**Question:** Is the layered approach still useful, or should we test individual sets?
- Layers helped us find layer_1_2 is best
- But now we need granularity: which sets within layers matter?
- **Insight needed:** Should we abandon layers and test feature sets directly?

### 5. Regularization Impact
**Question:** Would regularization help GradientBoosting or should we switch models?
- More features = worse performance suggests overfitting
- **Insight needed:** Can regularization fix this, or is it a model choice issue?

---

## Should We Continue with Layered Approach?

### Current Status
✅ **Layers helped us discover:** layer_1_2 is optimal (69.36%)
✅ **Layers showed clear pattern:** More layers = worse performance
✅ **Layers provided structure:** Organized 100+ features into logical groups

### Limitations Now
❌ **Too coarse-grained:** We know Layer 2 helps, but not which of its 3 sets
❌ **Can't test individual sets:** Current system only tests full layers
❌ **Missing granularity:** Need to test `layer_1 + schedule_fatigue` only, etc.

### Recommendation
**Hybrid Approach:**
1. **Keep layers for high-level discovery** (already done - we know layer_1_2 is best)
2. **Add feature-set-level testing** to drill down into what works
3. **Test both models** (GradientBoosting AND LogisticRegression) on same configs
4. **Compare results** to see if model choice matters more than feature choice

---

## Test Plan: Commands to Run

### Phase 1: Model Comparison (CRITICAL - Run First) ⭐⭐⭐
**Goal:** Determine if we're using the right model

**Time:** ~30 minutes

```bash
# Test GradientBoosting on best config (baseline)
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type GradientBoosting

# Test LogisticRegression with different regularization strengths
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.01
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.1
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 1.0
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 10.0

# Test LogisticRegression on layer_1_only for comparison
python train.py train --test-layers --layer-config layer_1 --model-type LogisticRegression --c-value 0.1
```

**What to look for:**
- Does LogisticRegression match or beat GradientBoosting?
- Which C-value performs best?
- Is the variance lower with LogisticRegression?

---

### Phase 2: Layer 2 Breakdown (HIGH PRIORITY) ⭐⭐⭐
**Goal:** Identify which Layer 2 feature sets actually help

**Time:** ~45 minutes

**Note:** This requires adding feature-set-level testing capability first (see implementation below)

```bash
# Test Layer 1 + just pace features
python train.py train --test-layers --layer-config "layer_1,pace_volatility" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,pace_volatility" --model-type LogisticRegression --c-value 0.1

# Test Layer 1 + just schedule/fatigue features
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue" --model-type LogisticRegression --c-value 0.1

# Test Layer 1 + just sample size features
python train.py train --test-layers --layer-config "layer_1,sample_size" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,sample_size" --model-type LogisticRegression --c-value 0.1

# Test combinations of Layer 2 sets
python train.py train --test-layers --layer-config "layer_1,pace_volatility,schedule_fatigue" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" --model-type GradientBoosting
```

**What to look for:**
- Which single Layer 2 set provides the most value?
- Can we get same performance with fewer Layer 2 features?
- Do different models prefer different Layer 2 sets?

---

### Phase 3: Layer 1 Ablation (MEDIUM PRIORITY) ⭐⭐
**Goal:** Understand which Layer 1 feature sets are essential

**Time:** ~1 hour

```bash
# Full ablation study (tests removing each set)
python train.py train --ablate --model-type GradientBoosting
python train.py train --ablate --model-type LogisticRegression --c-value 0.1

# Test Layer 1 subsets
python train.py train --test-layers --layer-config "outcome_strength,shooting_efficiency" --model-type GradientBoosting
python train.py train --test-layers --layer-config "outcome_strength,offensive_engine,defensive_engine" --model-type GradientBoosting
python train.py train --test-layers --layer-config "shooting_efficiency,offensive_engine,defensive_engine" --model-type GradientBoosting
```

**What to look for:**
- Which Layer 1 sets can be removed without hurting performance?
- Is `outcome_strength` doing all the work (given winsMonths_1Diff dominance)?
- Can we reduce from 46 to 30-35 Layer 1 features?

---

### Phase 4: Optimal Configuration Testing (HIGH PRIORITY) ⭐⭐⭐
**Goal:** Find the best model + feature combination

**Time:** ~1 hour

```bash
# Test best model from Phase 1 on various configs
# (Replace MODEL and C_VALUE with best from Phase 1)

# Minimal config: Layer 1 + best Layer 2 set
python train.py train --test-layers --layer-config "layer_1,<best_layer2_set>" --model-type <MODEL> --c-value <C_VALUE>

# Test with reduced Layer 1 (if Phase 3 shows some sets can be removed)
python train.py train --test-layers --layer-config "<reduced_layer1_sets>,<best_layer2_set>" --model-type <MODEL> --c-value <C_VALUE>

# Compare to current best
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type <MODEL> --c-value <C_VALUE>
```

**What to look for:**
- Can we beat 69.36% accuracy?
- Can we reduce features while maintaining performance?
- What's the optimal accuracy/complexity tradeoff?

---

### Phase 5: Regularization Deep Dive (IF NEEDED) ⭐
**Goal:** Fine-tune regularization if GradientBoosting is still best

**Time:** ~30 minutes

**Note:** Requires code changes to support GradientBoosting regularization

```bash
# Would need to add --learning-rate, --max-depth, --subsample parameters
# Then test:
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-type GradientBoosting --learning-rate 0.05 --max-depth 3
```

**What to look for:**
- Can regularization improve GradientBoosting performance?
- Does it reduce variance?

---

## Implementation: Adding Feature-Set-Level Testing

To run Phase 2, we need to enhance the system to accept feature set names directly. Here's what needs to be added:

**Modify `layer_test_mode` in `train.py` to:**
1. Check if `--layer-config` contains feature set names (not just layer names)
2. If feature set names, use `get_features_by_sets()` instead of `get_features_by_layers()`
3. Allow comma-separated mix of layers and sets: `"layer_1,schedule_fatigue"`

**Example enhancement needed:**
```python
# In layer_test_mode function, around line 940:
if args.layer_config:
    parts = [p.strip() for p in args.layer_config.split(',')]
    
    # Check if these are layers or feature sets
    if all(p.startswith('layer_') for p in parts):
        # All are layers - use existing logic
        layer_names = parts
        configs_to_test = {args.layer_config: layer_names}
    else:
        # Mix of layers and sets, or just sets
        # Need to handle this case
        ...
```

---

## Expected Insights from Each Phase

### Phase 1 Insights
- **If LogisticRegression matches/bests GradientBoosting:**
  - Switch to LogisticRegression (simpler, faster, more interpretable)
  - Use optimal C-value for regularization
- **If GradientBoosting still best:**
  - Continue with it, but add regularization
  - Consider ensemble of both models

### Phase 2 Insights
- **If one Layer 2 set dominates:**
  - Reduce from 20 to ~6-11 features (just that set)
  - Simpler model, same or better performance
- **If multiple sets needed:**
  - Keep optimal combination
  - Document which sets matter

### Phase 3 Insights
- **If some Layer 1 sets can be removed:**
  - Reduce from 46 to 30-40 features
  - Less overfitting, better generalization
- **If all Layer 1 sets needed:**
  - Focus optimization on regularization/model choice

### Phase 4 Insights
- **Optimal final configuration:**
  - Best model type
  - Best feature combination
  - Best hyperparameters
  - Target: 69.5-70%+ accuracy with fewer features

---

## Recommended Execution Order

1. **First:** Run Phase 1 (Model Comparison) - 30 min
   - This tells us if we're using the right model
   - Everything else depends on this

2. **Second:** Implement feature-set-level testing (15 min coding)
   - Needed for Phase 2

3. **Third:** Run Phase 2 (Layer 2 Breakdown) - 45 min
   - Quick wins: identify which Layer 2 sets matter

4. **Fourth:** Run Phase 3 (Layer 1 Ablation) - 1 hour
   - Understand Layer 1 redundancy

5. **Fifth:** Run Phase 4 (Optimal Config) - 1 hour
   - Combine insights from Phases 1-3
   - Find final optimal configuration

6. **Optional:** Run Phase 5 (Regularization) - 30 min
   - Only if GradientBoosting is still best

**Total Time:** ~3.5 hours of testing + 15 min implementation

---

## Success Criteria

After running this plan, we should know:

1. ✅ **Best model type:** GradientBoosting or LogisticRegression?
2. ✅ **Optimal feature combination:** Which sets from Layer 1 and Layer 2?
3. ✅ **Feature count:** Can we reduce from 66 to 40-50 features?
4. ✅ **Target accuracy:** Can we reach 69.5-70%+?
5. ✅ **Variance reduction:** Can we get std dev < 0.80%?

---

## Next Steps

1. **Run Phase 1 immediately** (no code changes needed)
2. **Implement feature-set testing** (small code change)
3. **Run Phases 2-4** systematically
4. **Document final optimal configuration**
5. **Update production code** to use optimal settings

