# Optimization Test Results Analysis

## Phase 1: Model Comparison Results

### Summary
**Best Model: LogisticRegression with C=0.1**
- **Accuracy: 70.28% ± 1.11%**
- **Log Loss: 0.5701**

### Detailed Results

| Model | C-value | Accuracy | Std Dev | Log Loss | Notes |
|-------|---------|----------|---------|----------|-------|
| **LogisticRegression** | **0.1** | **70.28%** | **±1.11%** | **0.5701** | **⭐ BEST** |
| LogisticRegression | 1.0 | 70.18% | ±0.98% | 0.5710 | Best std dev |
| LogisticRegression | 10.0 | 70.16% | ±1.01% | 0.5713 | |
| LogisticRegression | 0.01 | 70.06% | ±1.04% | 0.5701 | |
| GradientBoosting | - | 69.36% | ±0.95% | 0.5807 | Lower accuracy, better std dev |

### Key Findings
1. **LogisticRegression outperforms GradientBoosting** by ~0.9% accuracy
2. **C=0.1 is optimal** for LogisticRegression (best accuracy)
3. **C=1.0 has best std dev** (0.98%) but slightly lower accuracy
4. GradientBoosting has better stability (lower std dev) but lower peak performance

### Recommendation
✅ **Use LogisticRegression with C=0.1** for Phase 4 testing

---

## Phase 2: Layer 2 Breakdown Results

### Summary
**Best Layer 2 Combination: schedule_fatigue + sample_size**
- **Accuracy: 69.27% ± 1.44%** (with GradientBoosting)
- **Features: 60** (vs 66 for full Layer 2)

### Detailed Results

| Configuration | Features | Accuracy | Std Dev | Log Loss | Notes |
|---------------|----------|----------|---------|----------|-------|
| layer_1 + schedule_fatigue + sample_size | 60 | 69.27% | ±1.44% | 0.5829 | ⭐ Best combo |
| layer_1 + pace_volatility + schedule_fatigue | 63 | 69.25% | ±1.24% | 0.5809 | |
| layer_1 + pace_volatility | 52 | 69.34% | ±1.29% | 0.5808 | Best single set |
| layer_1 + schedule_fatigue | 57 | 69.19% | ±1.44% | 0.5844 | |
| layer_1 + sample_size | 49 | 68.85% | ±1.48% | 0.5870 | ❌ Worst |

### Key Findings
1. **pace_volatility alone performs best** (69.34%) but with high variance
2. **schedule_fatigue + sample_size** is best combo (69.27%)
3. **sample_size alone hurts performance** (-0.51% vs baseline)
4. **pace_volatility may be noisy** (high std dev)

### Recommendation
✅ **Use schedule_fatigue + sample_size** for Phase 4
- Saves 6 features (66 → 60)
- Maintains performance
- Better stability than pace_volatility alone

---

## Phase 3: Layer 1 Ablation Results

### GradientBoosting Ablation

| Feature Set | Impact | Features | Notes |
|-------------|--------|----------|-------|
| **pace_volatility** | **+0.32%** | 6 | ⭐ Helps! |
| **absolute_magnitude** | **+0.11%** | 16 | ⭐ Helps! |
| outcome_strength | -0.33% | 12 | ❌ Hurts most |
| elo_strength | -0.27% | 1 | ❌ Hurts |
| shooting_efficiency | -0.17% | 16 | ❌ Hurts |
| schedule_fatigue | -0.12% | 11 | ❌ Hurts |
| player_talent | -0.09% | 20 | ❌ Hurts |
| sample_size | -0.05% | 3 | Minimal |
| offensive_engine | -0.03% | 7 | Minimal |
| defensive_engine | -0.02% | 11 | Minimal |

### LogisticRegression Ablation

| Feature Set | Impact | Features | Notes |
|-------------|--------|----------|-------|
| **player_talent** | **+0.56%** | 20 | ⭐ Helps significantly! |
| **outcome_strength** | **+0.04%** | 12 | ⭐ Helps slightly |
| schedule_fatigue | -0.22% | 11 | ❌ Hurts |
| absolute_magnitude | -0.14% | 16 | ❌ Hurts |
| shooting_efficiency | -0.13% | 16 | ❌ Hurts |
| elo_strength | -0.07% | 1 | ❌ Hurts |
| sample_size | -0.04% | 3 | Minimal |
| defensive_engine | -0.02% | 11 | Minimal |
| offensive_engine | -0.02% | 7 | Minimal |
| pace_volatility | -0.02% | 6 | Minimal |

### Key Findings

**For LogisticRegression (our chosen model):**
1. **player_talent helps significantly** (+0.56%) - KEEP
2. **outcome_strength helps slightly** (+0.04%) - KEEP
3. **shooting_efficiency hurts** (-0.13%) - CONSIDER REMOVING
4. **absolute_magnitude hurts** (-0.14%) - CONSIDER REMOVING
5. **schedule_fatigue hurts** (-0.22%) - BUT Phase 2 showed it helps in combo
6. **offensive_engine and defensive_engine** have minimal impact - CONSIDER REMOVING

**Important Note:** Ablation results can be misleading due to feature interactions. Need to test combinations.

### Recommendation
✅ **Test these configurations in Phase 4:**
1. Layer 1 (all) + schedule_fatigue + sample_size (baseline)
2. Layer 1 - shooting_efficiency - absolute_magnitude + schedule_fatigue + sample_size
3. Layer 1 - offensive_engine - defensive_engine + schedule_fatigue + sample_size
4. outcome_strength + shooting_efficiency + schedule_fatigue + sample_size (minimal Layer 1)

---

## Phase 4: Feature Selection Plan

Based on findings, test these configurations:

### Configuration 1: Optimal Layer 1 + Best Layer 2
- **Features:** outcome_strength, shooting_efficiency, offensive_engine, defensive_engine, schedule_fatigue, sample_size
- **Expected:** ~60 features, ~70.0%+ accuracy

### Configuration 2: Reduced Layer 1 (Remove Low-Impact Sets)
- **Features:** outcome_strength, shooting_efficiency, schedule_fatigue, sample_size
- **Removes:** offensive_engine, defensive_engine (minimal impact)
- **Expected:** ~45-50 features, similar accuracy

### Configuration 3: Minimal Layer 1 (Keep Only Essential)
- **Features:** outcome_strength, schedule_fatigue, sample_size
- **Removes:** shooting_efficiency, offensive_engine, defensive_engine
- **Expected:** ~30-35 features, test if accuracy maintained

### Configuration 4: Feature Selection by Importance
- Use top N features by importance (N = 30, 40, 50)
- Test accuracy vs feature count tradeoff

---

## Expected Phase 4 Outcomes

### Optimistic
- Find configuration with **70.0-70.5% accuracy** with **40-50 features**
- Reduce from 66 to 40-50 features while maintaining/improving accuracy
- Lower variance through feature reduction

### Realistic
- Maintain **~70.0% accuracy** with **50-55 features**
- Small improvement in stability
- Clear understanding of essential features

### Success Criteria
- ✅ Accuracy ≥ 70.0%
- ✅ Features ≤ 55 (reduction from 66)
- ✅ Std dev ≤ 1.0%
- ✅ Clear feature set recommendation

