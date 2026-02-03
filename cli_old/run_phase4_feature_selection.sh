#!/bin/bash
# Phase 4: Feature Selection Based on Optimization Results
# Run after reviewing Phases 1-3 results

set -e  # Exit on error

echo "=========================================="
echo "Phase 4: Feature Selection"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results directory
RESULTS_DIR="./model_output/phase4_feature_selection_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo "Results will be saved to: $RESULTS_DIR"
echo ""
echo "Based on optimization analysis:"
echo "  - Best Model: LogisticRegression (C=0.1)"
echo "  - Best Layer 2: schedule_fatigue + sample_size"
echo "  - Layer 1 findings: player_talent helps, some sets minimal impact"
echo ""

# ============================================================================
# PHASE 4.1: Test Optimal Configurations
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 4.1: Optimal Configurations${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Testing Configuration 1: Full Layer 1 + schedule_fatigue + sample_size (baseline)..."
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config1_baseline.txt" 2>&1
echo -e "${GREEN}✓ Configuration 1 complete${NC}"

echo "Testing Configuration 2: Layer 1 - offensive_engine - defensive_engine + schedule_fatigue + sample_size..."
python train.py train --test-layers --layer-config "outcome_strength,shooting_efficiency,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config2_reduced_engine.txt" 2>&1
echo -e "${GREEN}✓ Configuration 2 complete${NC}"

echo "Testing Configuration 3: Minimal Layer 1 (outcome_strength only) + schedule_fatigue + sample_size..."
python train.py train --test-layers --layer-config "outcome_strength,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config3_minimal.txt" 2>&1
echo -e "${GREEN}✓ Configuration 3 complete${NC}"

echo "Testing Configuration 4: Layer 1 - shooting_efficiency + schedule_fatigue + sample_size..."
python train.py train --test-layers --layer-config "outcome_strength,offensive_engine,defensive_engine,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config4_no_shooting.txt" 2>&1
echo -e "${GREEN}✓ Configuration 4 complete${NC}"

echo ""

# ============================================================================
# PHASE 4.2: Feature Selection by Importance
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 4.2: Feature Selection by Importance${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Find the training CSV (use most recent)
TRAINING_CSV=$(ls -t ./model_output/classifier_training_*.csv 2>/dev/null | head -1)

if [ -z "$TRAINING_CSV" ]; then
    echo -e "${YELLOW}Warning: No training CSV found. Skipping Phase 4.2${NC}"
else
    echo "Using training data: $TRAINING_CSV"
    echo "Testing top 20, 30, 40, 50, 60 features by importance..."
    python "$(dirname "$0")/feature_selection_by_importance.py" \
        --csv "$TRAINING_CSV" \
        --model-type LogisticRegression \
        --c-value 0.1 \
        --top-n "20,30,40,50,60" \
        --output-dir "$RESULTS_DIR" > "$RESULTS_DIR/phase4_feature_selection_importance.txt" 2>&1
    echo -e "${GREEN}✓ Feature selection by importance complete${NC}"
fi

echo ""

# ============================================================================
# PHASE 4.3: Test with player_talent (LR ablation showed it helps)
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 4.3: Test player_talent Inclusion${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Testing: Layer 1 + schedule_fatigue + sample_size + player_talent..."
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size,player_talent" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config5_with_talent.txt" 2>&1
echo -e "${GREEN}✓ Configuration 5 (with player_talent) complete${NC}"

echo ""

# ============================================================================
# PHASE 4.4: Test without absolute_magnitude (LR ablation showed it hurts)
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 4.4: Test without absolute_magnitude${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Testing: Layer 1 + schedule_fatigue + sample_size - absolute_magnitude..."
# Note: This requires specifying exact feature sets to exclude absolute_magnitude
# For now, test with explicit sets
python train.py train --test-layers --layer-config "outcome_strength,shooting_efficiency,offensive_engine,defensive_engine,schedule_fatigue,sample_size" \
  --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase4_config6_no_absolute.txt" 2>&1
echo -e "${GREEN}✓ Configuration 6 (no absolute_magnitude) complete${NC}"

echo ""

# ============================================================================
# Summary
# ============================================================================
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Phase 4 tests complete!${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "Next steps:"
echo "1. Review all Phase 4 configuration results"
echo "2. Compare accuracy, log loss, and feature counts"
echo "3. Select optimal configuration"
echo "4. Update production code with best configuration"
echo ""

