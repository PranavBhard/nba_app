# Optimization Test Results Summary

## 🏆 Key Findings

### Best Model: LogisticRegression (C=0.1)
- **Accuracy: 70.28% ± 1.11%**
- **Log Loss: 0.5701**
- Outperforms GradientBoosting by ~0.9%

### Best Layer 2 Combination: schedule_fatigue + sample_size
- **Accuracy: 69.27%** (with GradientBoosting)
- **Features: 60** (saves 6 features vs full Layer 2)

### Layer 1 Ablation Insights (LogisticRegression)
- ✅ **player_talent helps** (+0.56%)
- ✅ **outcome_strength helps** (+0.04%)
- ❌ **shooting_efficiency hurts** (-0.13%)
- ❌ **absolute_magnitude hurts** (-0.14%)
- ⚠️ **offensive_engine/defensive_engine** minimal impact

---

## 📊 Phase 1 Results (Model Comparison)

| Model | C-value | Accuracy | Std Dev | Winner |
|-------|---------|----------|---------|--------|
| **LogisticRegression** | **0.1** | **70.28%** | **±1.11%** | **⭐** |
| LogisticRegression | 1.0 | 70.18% | ±0.98% | Best std dev |
| LogisticRegression | 10.0 | 70.16% | ±1.01% | |
| LogisticRegression | 0.01 | 70.06% | ±1.04% | |
| GradientBoosting | - | 69.36% | ±0.95% | Lower accuracy |

**Decision: Use LogisticRegression with C=0.1**

---

## 📊 Phase 2 Results (Layer 2 Breakdown)

| Configuration | Features | Accuracy | Notes |
|---------------|----------|----------|-------|
| layer_1 + schedule_fatigue + sample_size | 60 | 69.27% | ⭐ Best combo |
| layer_1 + pace_volatility + schedule_fatigue | 63 | 69.25% | |
| layer_1 + pace_volatility | 52 | 69.34% | Best single, high variance |
| layer_1 + schedule_fatigue | 57 | 69.19% | |
| layer_1 + sample_size | 49 | 68.85% | ❌ Worst |

**Decision: Use schedule_fatigue + sample_size**

---

## 📊 Phase 3 Results (Layer 1 Ablation)

### LogisticRegression Ablation (Most Relevant)

| Feature Set | Impact | Decision |
|-------------|--------|----------|
| player_talent | **+0.56%** | ✅ **KEEP** |
| outcome_strength | **+0.04%** | ✅ **KEEP** |
| schedule_fatigue | -0.22% | ⚠️ Test in combo |
| absolute_magnitude | -0.14% | ❌ **REMOVE** |
| shooting_efficiency | -0.13% | ❌ **REMOVE** |
| offensive_engine | -0.02% | ⚠️ Test removal |
| defensive_engine | -0.02% | ⚠️ Test removal |

**Note:** Ablation can be misleading due to interactions. Test combinations.

---

## 🎯 Phase 4 Recommendations

### Configuration Priority Order

1. **Config 1 (Baseline):** layer_1 + schedule_fatigue + sample_size
   - Expected: ~60 features, ~70.0%+ accuracy

2. **Config 2 (Reduced Engine):** outcome_strength + shooting_efficiency + schedule_fatigue + sample_size
   - Removes: offensive_engine, defensive_engine
   - Expected: ~45-50 features

3. **Config 3 (With Talent):** layer_1 + schedule_fatigue + sample_size + player_talent
   - Adds: player_talent (helps +0.56%)
   - Expected: ~80 features, potentially higher accuracy

4. **Config 4 (Minimal):** outcome_strength + schedule_fatigue + sample_size
   - Removes: shooting_efficiency, offensive_engine, defensive_engine
   - Expected: ~30-35 features

5. **Config 5 (No Absolute):** layer_1 - absolute_magnitude + schedule_fatigue + sample_size
   - Removes: absolute_magnitude (hurts -0.14%)
   - Expected: ~50 features

---

## 🚀 Quick Start: Run Phase 4

```bash
# Run all Phase 4 tests
./cli/run_phase4_feature_selection.sh

# Or run individual tests:
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1
```

---

## 📈 Success Criteria

- ✅ Accuracy ≥ 70.0%
- ✅ Features ≤ 55 (reduction from 66)
- ✅ Std dev ≤ 1.0%
- ✅ Clear feature set recommendation

---

## 📝 Next Steps After Phase 4

1. Review Phase 4 results
2. Select optimal configuration
3. Update production code
4. Document final feature set
5. Test on new data

