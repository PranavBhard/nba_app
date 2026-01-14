# Layer Configuration Optimization Analysis

## Executive Summary

**Best Configuration**: `layer_1_2` with **69.36% accuracy** (±0.95%)
- 66 features total (46 from Layer 1, 20 from Layer 2)
- Lowest variance and best overall performance

## Key Findings

### 1. Layer Performance Ranking
| Config | Accuracy | Log Loss | Brier | Features | Std Dev |
|--------|----------|----------|-------|----------|---------|
| **layer_1_2** | **69.36%** | **0.5807** | **0.1984** | **66** | **±0.95%** |
| layer_1_2_3 | 69.18% | 0.5806 | 0.1984 | 67 | ±1.26% |
| layer_1_2_4 | 68.99% | 0.5836 | 0.1997 | 102 | ±1.55% |
| layer_1_only | 68.96% | 0.5850 | 0.2002 | 46 | ±1.41% |
| all_layers | 68.80% | 0.5870 | 0.2010 | 103 | ±1.59% |
| core_only | 68.65% | 0.5900 | 0.2022 | 47 | ±1.92% |

### 2. Critical Observations

#### ✅ What's Working
- **Layer 2 adds value**: +0.40% improvement over layer_1_only (68.96% → 69.36%)
- **Minimal feature set**: 66 features provides best accuracy/complexity tradeoff
- **Low variance**: ±0.95% standard deviation shows consistent performance

#### ❌ What's NOT Working
- **Layer 3 hurts**: Adding meta priors reduces accuracy by -0.18% and increases variance
- **Layer 4 hurts**: Adding player talent reduces accuracy by -0.37% and increases variance significantly
- **Diminishing returns**: More features = worse performance (clear overfitting signal)
- **Feature imbalance**: Single feature (`winsMonths_1Diff`) dominates with 0.82 importance

### 3. Feature Importance Analysis

In the best config (layer_1_2), feature importance shows:
```
winsMonths_1Diff          | 0.8218  (82% of importance!)
winsSznAvgDiff            | 0.0207
pointsMonths_1Diff        | 0.0117
winsSznAvg_sideDiff       | 0.0088
awayGamesPlayed           | 0.0066  (from Layer 2)
homeGamesLast5Days        | 0.0059  (from Layer 2)
```

**Problem**: One feature accounts for 82% of model importance. This suggests:
- Over-reliance on recent wins
- Other features may be redundant or noisy
- Potential for feature engineering or regularization

## Optimization Recommendations

### Priority 1: Test Individual Layer 2 Sets ⭐⭐⭐

**Hypothesis**: Only some Layer 2 sets contribute value. Test each individually:

```bash
# Test Layer 1 + just pace features
python train.py train --test-layers --layer-config layer_1+pace

# Test Layer 1 + just schedule/fatigue features  
python train.py train --test-layers --layer-config layer_1+schedule

# Test Layer 1 + just sample size features
python train.py train --test-layers --layer-config layer_1+sample
```

**Expected Outcome**: May find that only `schedule_fatigue` from Layer 2 helps, allowing you to reduce from 20 to ~11 features while maintaining performance.

### Priority 2: Feature Selection in Layer 1 ⭐⭐⭐

**Hypothesis**: Many Layer 1 features are redundant given the dominance of `winsMonths_1Diff`.

**Actions**:
1. Run ablation study on Layer 1 sets:
   ```bash
   python train.py train --ablate --model-type GradientBoosting
   ```
2. Test removing low-importance features (bottom 50% by importance)
3. Test configurations with only top N features from Layer 1

### Priority 3: Regularization for Layer 1+2 ⭐⭐

**Hypothesis**: Current GradientBoosting may be overfitting. Test with:
- More regularization (lower learning rate, more subsampling)
- Different model types (LogisticRegression with L1/L2 regularization)
- Feature importance-based feature selection

```bash
# Test LogisticRegression with regularization
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-type LogisticRegression --c-value 0.01

# Test GradientBoosting with more regularization (requires code changes)
```

### Priority 4: Remove Layer 3 and Layer 4 Entirely ⭐⭐

**Action**: Based on results showing they hurt performance:
1. Update default feature configuration to exclude Layer 3 and Layer 4
2. Document why they were removed
3. Focus optimization efforts on Layer 1 + selective Layer 2

### Priority 5: Address Feature Imbalance ⭐

**Problem**: `winsMonths_1Diff` has 0.82 importance - everything else is <0.02

**Potential Solutions**:
1. **Feature transformation**: Normalize or transform `winsMonths_1Diff` to reduce dominance
2. **Ensemble approach**: Create separate models for different feature groups
3. **Regularization**: Use L1 regularization to force feature sparsity and balance importance
4. **Feature engineering**: Create interaction features that combine `winsMonths_1Diff` with other features

## Recommended Testing Sequence

### Phase 1: Layer 2 Breakdown (30 min)
```bash
# Test which Layer 2 sets actually help
python train.py train --test-layers --layer-config layer_1,pace_volatility
python train.py train --test-layers --layer-config layer_1,schedule_fatigue  
python train.py train --test-layers --layer-config layer_1,sample_size
```

### Phase 2: Layer 1 Optimization (1-2 hours)
```bash
# Run ablation to see which Layer 1 sets matter most
python train.py train --ablate --model-type GradientBoosting

# Test configurations removing weakest Layer 1 sets
python train.py train --test-layers --layer-config layer_1_minimal
```

### Phase 3: Model & Regularization (1 hour)
```bash
# Test different models with layer_1_2
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-type LogisticRegression --c-values 0.001,0.01,0.1,1.0
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-type SVM --c-values 0.1,1.0,10.0
```

### Phase 4: Feature Selection (2-3 hours)
- Implement feature selection based on importance thresholds
- Test configurations with top 30, 40, 50 features from layer_1_2
- Compare performance vs. feature count

## Expected Outcomes

### Optimistic Scenario
- Identify that only `schedule_fatigue` from Layer 2 helps → reduce to ~57 features
- Find that 2-3 Layer 1 sets can be removed → reduce to ~35-40 features
- Achieve **69.5-70.0% accuracy** with **fewer features** and **lower variance**

### Realistic Scenario
- Confirm `layer_1_2` is optimal
- Reduce features by 10-15 through selection → maintain 69.3-69.4% accuracy
- Improve variance from ±0.95% to ±0.70-0.80%

### Conservative Scenario
- Confirm current `layer_1_2` config is best
- Focus on model hyperparameter tuning
- Achieve 69.5% accuracy with better regularization

## Implementation Notes

### Creating Custom Layer Configs

You'll need to modify `feature_sets.py` to support testing individual sets. Currently, you can only test full layers. Consider adding:

```python
def get_custom_layer_config(set_names: list) -> list:
    """Get features for custom set combination."""
    return get_features_by_sets(set_names)
```

Then test with:
```bash
python train.py train --test-layers --layer-config "outcome_strength,shooting_efficiency,schedule_fatigue"
```

## Questions to Answer

1. **Which Layer 2 sets matter?** Is it pace, schedule, or sample_size that provides the +0.4% boost?
2. **Can Layer 1 be reduced?** Which of the 4 Layer 1 sets are essential?
3. **Why does Layer 4 hurt?** 36 features but degrades performance - investigate correlation/redundancy
4. **Why does Layer 3 hurt?** Elo and era normalization seem valuable in theory but hurt in practice
5. **Can we balance feature importance?** Is the 82% dominance of `winsMonths_1Diff` a problem?

## Next Steps

1. ✅ Document current findings (this file)
2. ⬜ Implement custom set-level testing capability
3. ⬜ Run Layer 2 breakdown tests
4. ⬜ Run Layer 1 ablation study  
5. ⬜ Test regularization approaches
6. ⬜ Implement feature selection pipeline
7. ⬜ Update production config to use optimal settings

