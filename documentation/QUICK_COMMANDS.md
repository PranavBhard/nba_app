# Quick Test Commands - Copy & Paste

## ⭐ PHASE 1: Model Comparison (RUN FIRST - 30 min)

```bash
# Baseline: GradientBoosting on best config
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type GradientBoosting

# Test LogisticRegression with different regularization
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.01
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.1
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 1.0
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 10.0

# Compare on layer_1_only
python train.py train --test-layers --layer-config layer_1 --model-type LogisticRegression --c-value 0.1
```

---

## ⭐ PHASE 2: Layer 2 Breakdown (45 min)

**Note:** Requires feature-set testing capability (see implementation in test plan)

```bash
# Test each Layer 2 set individually
python train.py train --test-layers --layer-config "layer_1,pace_volatility" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,sample_size" --model-type GradientBoosting

# Test with LogisticRegression too
python train.py train --test-layers --layer-config "layer_1,pace_volatility" --model-type LogisticRegression --c-value 0.1
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue" --model-type LogisticRegression --c-value 0.1
python train.py train --test-layers --layer-config "layer_1,sample_size" --model-type LogisticRegression --c-value 0.1

# Test combinations
python train.py train --test-layers --layer-config "layer_1,pace_volatility,schedule_fatigue" --model-type GradientBoosting
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" --model-type GradientBoosting
```

---

## ⭐ PHASE 3: Layer 1 Ablation (1 hour)

```bash
# Full ablation study
python train.py train --ablate --model-type GradientBoosting
python train.py train --ablate --model-type LogisticRegression --c-value 0.1
```

---

## ⭐ PHASE 4: Optimal Config Testing (1 hour)

**Replace <MODEL> and <C_VALUE> with best from Phase 1**

```bash
# Test minimal configs based on Phase 2-3 results
python train.py train --test-layers --layer-config "layer_1,<best_layer2_set>" --model-type <MODEL> --c-value <C_VALUE>
python train.py train --test-layers --layer-config "<reduced_layer1_sets>,<best_layer2_set>" --model-type <MODEL> --c-value <C_VALUE>
```

---

## Quick Single Tests

```bash
# Just test current best with LogisticRegression
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.1

# Test all common configs with LogisticRegression
python train.py train --test-layers --model-type LogisticRegression --c-value 0.1
```

