Below is a **clean, explicit implementation guide**
It contains:

✅ Feature-set definitions
✅ Data modeling strategy per model type
✅ Architectural guidance
✅ Implementation requirements and warnings
✅ Exact instructions for building modular feature pipelines

You can drop this into your repo as:
**`docs/feature_set_architecture.md`**

---

# **NBA Model — Multi-Architecture Feature Set Specification**

### *(Implementation Guide for Cursor)*

This document describes **how to structure feature sets differently for each model type**, instead of relying exclusively on differential (“home – away”) features. Differential modeling is **ideal for Logistic Regression**, but suboptimal for other model families.

You will implement **independent feature pipelines** for:

1. Logistic Regression
2. Gradient Boosting / XGBoost / CatBoost
3. Neural Networks (Team Encoder + Matchup Layer)
4. Optional: Player-level Modeling (deepest model)

Each pipeline uses **different feature sets** and **different data modeling assumptions**.

---

# **1. Architectural Rule**

### **The diff-based feature design is ONLY for LogisticRegression.**

For all other model types, **we must re-model how features are structured**, because:

* Tree models learn nonlinear interactions natively
* Neural models need structured per-team input blocks
* Player-level architectures require embedding aggregation

DO NOT reuse the same features for all model types.
Implement separate builders for each.

---

# **2. Feature Set Definitions (Raw Ingredient Pools)**

These are the fundamental groups. The pipelines below will combine them differently.

### **A. Team-Level Stats (per game or aggregated)**

* points, assists, rebounds, turnovers
* offensive/defensive rating
* eFG%, TS%, 3PA rate, 3P%
* pace
* volatility measures
* home/away splits

### **B. Schedule & Fatigue**

* days rest
* back-to-back flags
* games in last N days
* cross-country travel flags (optional)

### **C. Era-Normalized Stats**

* ppg relative to league
* offense rating relative to league
* defense rating relative to league

### **D. Elo Ratings**

* home_elo / away_elo
* eloDiff (optional depending on pipeline)

### **E. Player-Level Aggregates**

* PER-based team aggregates
* Top-5 PER values
* Starter PER averages
* Minutes-weighted talent indicators
* Advanced player efficiency aggregates

---

# **3. MODEL TYPE #1 — Logistic Regression Pipeline**

### **Why:** LR assumes linear, additive, symmetric relationships.

### **Feature Strategy:** **Pure differential modeling** (+ optional absolutes).

---

## **Feature Set: LogisticRegressionFeatureSet**

### **A. Differential Features (CORE)**

```
statDiff = home_stat - away_stat
```

For:

* points
* wins
* off_rtg
* def_rtg
* eFG%, TS%
* pace
* volatility
* turnovers / assists ratio
* schedule fatigue (restDiff, b2bDiff)

### **B. Absolute Features**

Include ONLY the stats where absolute magnitude matters:

* home_off_rtg
* away_off_rtg
* home_def_rtg
* away_def_rtg
* absolute shooting efficiency

### **C. PER Aggregates**

Use differential values:

* perAvgDiff
* perWeightedDiff
* startersPerDiff

Also top-5 PER values:

```
homePer1 - awayPer1
...
homePer5 - awayPer5
```

### **Data Model**

A single flattened vector:

```
[
  statDiff1, statDiff2, ...,
  home_abs1, away_abs1,
  perAvgDiff, perWeightedDiff, ...
  eloDiff,
  restDiff
]
```

### **Cursor Implementation**

* Create `build_logreg_features(game)`
* Only this builder uses diffs
* Keep everything numeric, standardized, dense
* No interaction terms (model can’t use them) unless explicitly created

---

# **4. MODEL TYPE #2 — Tree Models (XGBoost, LightGBM, CatBoost)**

### **Why:** Tree models handle nonlinearities and interactions.

### **Feature Strategy:** **RAW per-team features**, plus optional diffs + explicit interactions.

NO aggressive collapsing of data.
We want *structure*.

---

## **Feature Set: TreeModelFeatureSet**

### **A. Per-team Blocks (PRIMARY)**

Use **two copies** of the same feature structure—one for home, one for away.

```
home_off_rtg
home_def_rtg
home_pace
home_effective_fg
home_true_shooting
home_volatility
home_games_played
...

away_off_rtg
away_def_rtg
away_pace
...
```

### **B. Differential Features (SECONDARY)**

Useful as shortcuts for decision trees:

```
off_rtgDiff
def_rtgDiff
paceDiff
efgDiff
restDiff
```

### **C. Crossed Interaction Features (VERY IMPORTANT)**

Let trees learn matchup effects:

```
home_off_rtg * away_def_rtg
home_efg * away_efg_def
home_pace * away_pace
home_tov * away_def_forced_tov
home_reb * away_def_reb_allowed
```

### **D. PER Aggregates (Per-team, not diff)**

Keep full structure:

```
homeTeamPerAvg
homeTeamPerWeighted
homeStartersPerAvg
homePer1, ..., homePer5

awayTeamPerAvg
...
```

### **Data Model**

A structured vector of:

1. **home_block**
2. **away_block**
3. **differentials**
4. **interactions**

### **Cursor Implementation**

Create:

```python
build_tree_features(game)
```

Where:

* home features = dict
* away features = dict
* diff = computed automatically
* interactions = generated automatically

**No normalization needed** (tree models ignore scale).

---

# **5. MODEL TYPE #3 — Neural Network (Team Encoder Architecture)**

### **Why:** Neural networks excel when the input has *structure*.

### **Feature Strategy:** **Encode each team separately**, then compute matchup interactions.

This is the modern Elo-like NN architecture.

---

## **Feature Set: NeuralNetworkFeatureSet**

### **A. Per-Team Input Blocks**

Each team gets the *full* feature set:

```
TeamEncoderInput = [
  off_rtg, def_rtg, pace, efg, ts,
  wins, points, volatility,
  schedule fatigue metrics,
  Elo,
  PER aggregates,
  era-normalized stats,
  home/away context,
]
```

### **B. The Model Architecture**

```
home_vec  = TeamEncoder(home_features)
away_vec  = TeamEncoder(away_features)

diff_vec  = home_vec - away_vec
matchup   = concat(home_vec, away_vec, diff_vec)

output    = MatchupHead(matchup)
```

### TeamEncoder:

* 1–3 dense layers
* BatchNorm optional
* Outputs 16–64 dimensional vector

### MatchupHead:

* 1–3 dense layers
* FINAL SIGMOID → home win probability

### **Data Model**

Input is:

```
{
   "home": {full team stat block},
   "away": {full team stat block}
}
```

Not flattened diffs.

### **Cursor Implementation**

Create:

```
build_neural_inputs(game)
```

Two dicts: `home_features`, `away_features`.

No diffs needed—NN computes its own abstract comparison.

---

# **6. MODEL TYPE #4 — Player-Level Modeling (Optional)**

### *(This is the best model if implemented correctly)*

### **Strategy:**

Generate team vectors from **player embeddings**, then feed them into the neural matchup architecture.

---

## **Feature Set: PlayerLevelFeatureSet**

### **A. Per-Player Input**

For each player:

* mins, pts, reb, ast, stl, blk, tov
* shooting splits
* possession stats
* RAPM-like estimates (if you compute them)
* PER components
* On/off indicators (optional)

### **B. PlayerEncoder**

Neural layer that maps player stat vector → embedding.

### **C. Team Aggregation**

Use:

* weighted sum (minutes)
* mean pooling
* top-k pooling (optional)

Outputs a **team latent vector**.

### **D. Matchup Model**

Same as neural architecture above.

### **Cursor Implementation**

Create:

```
build_player_level_inputs(game)
```

You load all players for each team in the game.

This model is deeper and requires batching.

---

# **7. Implementation Summary (for Cursor)**

Implement four independent feature pipelines:

---

## **1. `build_logreg_features(game)`**

* Uses ONLY differential features
* Adds small set of absolute features
* Feature vector is flat
* Use StandardScaler

---

## **2. `build_tree_features(game)`**

* Per-team blocks
* Diff features
* Interaction features
* No scaling
* Wide feature set

---

## **3. `build_neural_inputs(game)`**

* Two structured dicts: home + away
* No diffs
* No interactions
* NN handles architecture

---

## **4. `build_player_level_inputs(game)`**

* Player-level input arrays
* Aggregation into team embeddings
* Neural matchup model

---

# **8. Why Separate Pipelines Matter**

| Model Type              | Why It Needs Its Own Feature Structure                                      |
| ----------------------- | --------------------------------------------------------------------------- |
| **Logistic Regression** | Must enforce linear, symmetric structure → diffs are mathematically optimal |
| **Tree Models**         | Learn nonlinear interactions → need raw per-team structure + interactions   |
| **Neural Networks**     | Require structured blocks → team encoder + matchup head                     |
| **Player-Level Models** | Directly model roster → structured player→team→matchup encoding             |

Using the **same feature engineering** for all model types is a performance bottleneck.
These pipelines unlock the strengths of each model family.

---