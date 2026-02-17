# Layering Explained: Feature Organization, Not Model Stacking

## ❌ What Layering is NOT

**Layering is NOT:**
- Stacking models where one model's outputs become inputs to the next
- Creating hierarchical models where layer N uses layer N-1's predictions
- Neural network-style layers with weights and activations

## ✅ What Layering IS

**Layering IS:**
- **Feature organization** - grouping related features into conceptual "layers"
- **Feature selection testing** - testing which combinations of feature groups work best
- **Ablation study framework** - systematically testing feature subsets

## 🎯 The Concept

Think of "layers" as **feature categories**:

- **Layer 1**: Core strength features (wins, points, ratings)
- **Layer 2**: Contextual features (rest, schedule, pace)
- **Layer 3**: Meta features (Elo, era normalization)
- **Layer 4**: Detailed features (player talent, absolute magnitudes)

When you test `layer_1,layer_2`, you're testing a **single model** with features from **both Layer 1 AND Layer 2 combined**.

## 📊 Example

### Test: `layer_1` only
- **Model**: Single XGBoost model
- **Features**: Only Layer 1 features (~46 features)
- **Result**: 68.96% accuracy

### Test: `layer_1,layer_2`
- **Model**: Single XGBoost model
- **Features**: Layer 1 + Layer 2 features combined (~66 features)
- **Result**: 69.36% accuracy

**Key Point**: It's the SAME model type, just with different feature sets!

## 🔍 Why Use Layers?

1. **Organize features conceptually** - easier to understand what you're testing
2. **Systematic testing** - test combinations systematically
3. **Feature importance** - see which feature categories matter most
4. **Reduce overfitting** - find minimal feature sets that work well

## 🧪 How It Works

```
Test: layer_1,layer_2

Step 1: Collect features from Layer 1
  → outcome_strength (12 features)
  → shooting_efficiency (16 features)
  → offensive_engine (7 features)
  → defensive_engine (11 features)
  Total: 46 features

Step 2: Collect features from Layer 2
  → pace_volatility (6 features)
  → schedule_fatigue (11 features)
  → sample_size (3 features)
  Total: 20 features

Step 3: Combine all features
  → 46 + 20 = 66 total features

Step 4: Train ONE model with all 66 features
  → XGBoost model
  → Trained on combined feature set
  → Evaluated with cross-validation

Step 5: Compare results
  → layer_1 only: 68.96%
  → layer_1,layer_2: 69.36%
  → Conclusion: Layer 2 adds value!
```

## 🎯 Real-World Analogy

Think of it like building a house:

- **Layer 1** = Foundation (core structure)
- **Layer 2** = Walls (context)
- **Layer 3** = Roof (meta features)
- **Layer 4** = Interior details (player-level)

You can test:
- Foundation only (layer_1)
- Foundation + Walls (layer_1,layer_2)
- Foundation + Walls + Roof (layer_1,layer_2,layer_3)
- Everything (all_layers)

But you're still building **ONE house** (ONE model) - you're just choosing which parts to include!

## 📈 What You Learn

From layer testing, you discover:

1. **Which feature categories help** - Does Layer 2 improve accuracy?
2. **Which combinations work best** - Is layer_1,layer_2 better than layer_1,layer_3?
3. **Minimal feature sets** - Can you get good performance with fewer features?
4. **Feature interactions** - Do features from different layers work well together?

## 🔄 Comparison to Model Stacking

### Model Stacking (What you might be thinking of):
```
Layer 1 Model → Predictions → Layer 2 Model → Final Predictions
```

### Feature Layering (What this codebase does):
```
Layer 1 Features + Layer 2 Features → Single Model → Predictions
```

## 💡 Key Takeaway

**Layering = Feature Organization + Feature Selection Testing**

It's about **which features to include**, not about **how to structure the model**.

