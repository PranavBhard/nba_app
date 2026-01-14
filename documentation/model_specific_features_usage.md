# Model-Specific Features Usage Guide

This guide explains how to use the new model-specific feature builders that create optimized feature sets for different model types.

## Overview

Each model type now has its own specialized feature pipeline:
- **LogisticRegression**: Differential-based features (current approach)
- **Tree Models** (GradientBoosting, XGBoost, etc.): Per-team blocks + interactions
- **Neural Networks**: Structured per-team blocks

## Usage

### Basic Usage

```bash
# Train with model-specific features for LogisticRegression
python train.py train --model-specific-features --model-type LogisticRegression

# Train with model-specific features for GradientBoosting
python train.py train --model-specific-features --model-type GradientBoosting

# Train with model-specific features for Neural Network
python train.py train --model-specific-features --model-type MLPClassifier
```

### With Layer Testing

```bash
# Test layers with LogisticRegression-specific features
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-specific-features --model-type LogisticRegression --c-value 0.1

# Test layers with GradientBoosting-specific features
python train.py train --test-layers --layer-config layer_1,layer_2 \
  --model-specific-features --model-type GradientBoosting
```

## Feature Set Differences

### LogisticRegression Features
- **Structure**: Flat vector of differentials
- **Format**: `statDiff`, `eloDiff`, `restDiff`, etc.
- **Example**: `pointsSznAvgDiff`, `winsMonths_1Diff`, `offRtgDiff`
- **Why**: Linear models work best with symmetric, differential features

### Tree Model Features (GradientBoosting, etc.)
- **Structure**: Per-team blocks + differentials + interactions
- **Format**: 
  - Per-team: `home_off_rtg`, `away_off_rtg`, `home_pace`, `away_pace`
  - Differentials: `off_rtgDiff`, `paceDiff`
  - Interactions: `home_off_rtg_x_away_def_rtg`, `home_pace_x_away_pace`
- **Why**: Trees can learn interactions, so we provide explicit interaction features

### Neural Network Features
- **Structure**: Structured per-team blocks (flattened to CSV)
- **Format**: `home_off_rtg`, `home_def_rtg`, `away_off_rtg`, `away_def_rtg`, etc.
- **Why**: NNs benefit from structured input where they can learn team encodings

## Implementation Details

The feature builders are in `cli/model_specific_features.py`:
- `LogisticRegressionFeatureBuilder`: Builds differential features
- `TreeModelFeatureBuilder`: Builds per-team + interaction features
- `NeuralNetworkFeatureBuilder`: Builds structured per-team features

The `NBAModel.create_training_data_model_specific()` method uses these builders to create model-specific training CSVs.

## Comparison Testing

To compare model-specific vs. standard features:

```bash
# Standard features (differential-based for all models)
python train.py train --model-type GradientBoosting

# Model-specific features (per-team + interactions for GradientBoosting)
python train.py train --model-specific-features --model-type GradientBoosting
```

## Notes

- Model-specific features are only used when `--model-specific-features` flag is set
- When not set, all models use the standard differential-based features
- Neural network features are flattened to CSV format (in production, you might use a different storage format)
- Feature counts will differ between model types due to different structures

