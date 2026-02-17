#!/bin/bash
# NBA Model Optimization Test Suite
# Run this script to execute all optimization tests systematically

set -e  # Exit on error

echo "=========================================="
echo "NBA Model Optimization Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results directory
RESULTS_DIR="./model_output/optimization_tests_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo "Results will be saved to: $RESULTS_DIR"
echo ""

# ============================================================================
# PHASE 1: Model Comparison (CRITICAL - Run First)
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 1: Model Comparison${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Testing GradientBoosting baseline..."
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type GradientBoosting > "$RESULTS_DIR/phase1_gb_baseline.txt" 2>&1
echo -e "${GREEN}✓ GradientBoosting baseline complete${NC}"

echo "Testing LogisticRegression with C=0.01..."
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.01 > "$RESULTS_DIR/phase1_lr_c001.txt" 2>&1
echo -e "${GREEN}✓ LogisticRegression C=0.01 complete${NC}"

echo "Testing LogisticRegression with C=0.1..."
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase1_lr_c01.txt" 2>&1
echo -e "${GREEN}✓ LogisticRegression C=0.1 complete${NC}"

echo "Testing LogisticRegression with C=1.0..."
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 1.0 > "$RESULTS_DIR/phase1_lr_c10.txt" 2>&1
echo -e "${GREEN}✓ LogisticRegression C=1.0 complete${NC}"

echo "Testing LogisticRegression with C=10.0..."
python train.py train --test-layers --layer-config layer_1,layer_2 --model-type LogisticRegression --c-value 10.0 > "$RESULTS_DIR/phase1_lr_c100.txt" 2>&1
echo -e "${GREEN}✓ LogisticRegression C=10.0 complete${NC}"

echo ""

# ============================================================================
# PHASE 2: Layer 2 Breakdown
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 2: Layer 2 Breakdown${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Testing Layer 1 + pace_volatility..."
python train.py train --test-layers --layer-config "layer_1,pace_volatility" --model-type GradientBoosting > "$RESULTS_DIR/phase2_layer1_pace.txt" 2>&1
echo -e "${GREEN}✓ Layer 1 + pace_volatility complete${NC}"

echo "Testing Layer 1 + schedule_fatigue..."
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue" --model-type GradientBoosting > "$RESULTS_DIR/phase2_layer1_schedule.txt" 2>&1
echo -e "${GREEN}✓ Layer 1 + schedule_fatigue complete${NC}"

echo "Testing Layer 1 + sample_size..."
python train.py train --test-layers --layer-config "layer_1,sample_size" --model-type GradientBoosting > "$RESULTS_DIR/phase2_layer1_sample.txt" 2>&1
echo -e "${GREEN}✓ Layer 1 + sample_size complete${NC}"

echo "Testing Layer 1 + pace_volatility + schedule_fatigue..."
python train.py train --test-layers --layer-config "layer_1,pace_volatility,schedule_fatigue" --model-type GradientBoosting > "$RESULTS_DIR/phase2_layer1_pace_schedule.txt" 2>&1
echo -e "${GREEN}✓ Layer 1 + pace + schedule complete${NC}"

echo "Testing Layer 1 + schedule_fatigue + sample_size..."
python train.py train --test-layers --layer-config "layer_1,schedule_fatigue,sample_size" --model-type GradientBoosting > "$RESULTS_DIR/phase2_layer1_schedule_sample.txt" 2>&1
echo -e "${GREEN}✓ Layer 1 + schedule + sample complete${NC}"

echo ""

# ============================================================================
# PHASE 3: Layer 1 Ablation
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 3: Layer 1 Ablation Study${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Running full ablation study with GradientBoosting..."
python train.py train --ablate --model-type GradientBoosting > "$RESULTS_DIR/phase3_ablation_gb.txt" 2>&1
echo -e "${GREEN}✓ Ablation study (GradientBoosting) complete${NC}"

echo "Running full ablation study with LogisticRegression..."
python train.py train --ablate --model-type LogisticRegression --c-value 0.1 > "$RESULTS_DIR/phase3_ablation_lr.txt" 2>&1
echo -e "${GREEN}✓ Ablation study (LogisticRegression) complete${NC}"

echo ""

# ============================================================================
# Summary
# ============================================================================
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}All tests complete!${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "Next steps:"
echo "1. Review Phase 1 results to determine best model"
echo "2. Review Phase 2 results to identify which Layer 2 sets help"
echo "3. Review Phase 3 results to identify which Layer 1 sets are essential"
echo "4. Run Phase 4 (Feature Selection) based on findings"
echo ""

