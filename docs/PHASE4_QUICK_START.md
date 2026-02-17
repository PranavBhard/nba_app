# Phase 4: Feature Selection - Quick Start Guide

## 📋 Summary of Findings

### Phase 1: Best Model
✅ **LogisticRegression with C=0.1** - 70.28% accuracy

### Phase 2: Best Layer 2
✅ **schedule_fatigue + sample_size** - 60 features, 69.27% accuracy

### Phase 3: Layer 1 Insights
- ✅ **player_talent helps** (+0.56%)
- ✅ **outcome_strength helps** (+0.04%)
- ❌ **shooting_efficiency hurts** (-0.13%)
- ❌ **absolute_magnitude hurts** (-0.14%)
- ⚠️ **offensive_engine/defensive_engine** minimal impact

---

## 🚀 Run Phase 4

### Option 1: Run All Tests (Recommended)
```bash
cd /Users/pranav/Desktop/MB2024Desktop/NBA/nba_app
./cli/run_phase4_feature_selection.sh
```

### Option 2: Run Individual Tests

#### Test Configuration 1 (Baseline)
```bash
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1
```

#### Test Configuration 2 (Reduced Engine)
```bash
python train.py train --test-layers --layer-config "outcome_strength,shooting_efficiency,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1
```

#### Test Configuration 3 (Minimal)
```bash
python train.py train --test-layers --layer-config "outcome_strength,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1
```

#### Test Configuration 4 (With Talent)
```bash
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size,player_talent" \
  --model-type LogisticRegression --c-value 0.1
```

#### Test Feature Selection by Importance
```bash
# Find your training CSV first
TRAINING_CSV=$(ls -t ./model_output/classifier_training_*.csv | head -1)

python cli/feature_selection_by_importance.py \
  --csv "$TRAINING_CSV" \
  --model-type LogisticRegression \
  --c-value 0.1 \
  --top-n "20,30,40,50,60"
```

---

## 📊 Expected Results

After running Phase 4, you should have:

1. **Configuration comparison** showing:
   - Accuracy for each config
   - Feature counts
   - Log loss and Brier scores

2. **Feature importance ranking** showing:
   - Top N features by importance
   - Performance with different N values

3. **Optimal configuration recommendation** based on:
   - Highest accuracy
   - Reasonable feature count (≤55)
   - Low variance (std dev ≤1.0%)

---

## 📁 Output Files

Results will be saved to:
```
./model_output/phase4_feature_selection_YYYYMMDD_HHMMSS/
├── phase4_config1_baseline.txt
├── phase4_config2_reduced_engine.txt
├── phase4_config3_minimal.txt
├── phase4_config4_no_shooting.txt
├── phase4_config5_with_talent.txt
├── phase4_config6_no_absolute.txt
├── phase4_feature_selection_importance.txt
└── feature_selection_YYYYMMDD_HHMMSS/
    ├── feature_selection_results.json
    └── top_N_features.txt
```

---

## 🎯 Decision Criteria

After Phase 4, choose the configuration that:
1. ✅ Has accuracy ≥ 70.0%
2. ✅ Has ≤ 55 features (reduction from 66)
3. ✅ Has std dev ≤ 1.0%
4. ✅ Balances accuracy vs. complexity

---

## 📝 Next Steps

1. Review all Phase 4 results
2. Compare configurations side-by-side
3. Select optimal configuration
4. Update production code with best config
5. Document final feature set

