I’ve grouped features by *conceptual family* so intent is clear, but **each feature is independently defined**.

---

# 📘 Head-to-Head (H2H) Feature Specification

**Purpose:**
Capture matchup-specific historical performance *with reliability, recency, and context awareness*, designed to stack cleanly into a multi-GB → LR ensemble.

---

## 1️⃣ Core Reliability-Weighted H2H Margin

### `margin_h2h|season|avg|home`

Home team’s **average point margin** in prior head-to-head games vs the away team **within the current season**, regardless of venue.

**Calculation:**

```
mean(home_score - away_score)
```

Over all H2H games played earlier this season.

---

### `margin_h2h|season|avg|away`

Away team’s **average point margin** in prior head-to-head games vs the home team within the current season.

---

### `margin_h2h|season|avg|diff`

```
margin_h2h|season|avg|home
-
margin_h2h|season|avg|away
```

---

## 2️⃣ Shrinkage / Reliability-Aware H2H Margin

### `margin_h2h|season|eb|home`

Empirical-Bayes-shrunken average margin for the home team in prior H2H games this season.

**Calculation:**

```
(n / (n + k)) * margin_h2h_avg
```

Where:

* `n` = number of H2H games this season
* `k` = shrinkage constant (global, e.g. 5–10)

---

### `margin_h2h|season|eb|away`

Same as above, computed from the away team’s perspective.

---

### `margin_h2h|season|eb|diff`

```
margin_h2h|season|eb|home
-
margin_h2h|season|eb|away
```

---

### `margin_h2h|season|logw|home`

Reliability-weighted margin using logarithmic weighting.

**Calculation:**

```
margin_h2h_avg * log1p(h2h_games_count)
```

---

### `margin_h2h|season|logw|away`

---

### `margin_h2h|season|logw|diff`

---

## 3️⃣ Shrinkage-Adjusted H2H Win Percentage

### `h2h_win_pct|season|raw|home`

Home team’s raw win percentage in prior H2H games this season.

---

### `h2h_win_pct|season|raw|away`

---

### `h2h_win_pct|season|raw|diff`

---

### `h2h_win_pct|season|beta|home`

Beta-prior-smoothed win probability for the home team.

**Calculation:**

```
(wins + α) / (games + α + β)
```

Where α and β are global smoothing constants.

---

### `h2h_win_pct|season|beta|away`

---

### `h2h_win_pct|season|beta|diff`

---

## 4️⃣ Recent / Recency-Weighted H2H Margin

### `margin_h2h|last_n|avg|home`

Home team’s average margin over the **last N H2H meetings**, regardless of season.

---

### `margin_h2h|last_n|avg|away`

---

### `margin_h2h|last_n|avg|diff`

---

### `margin_h2h|exp_decay|lambda_X|home`

Exponentially-decayed H2H margin favoring recent meetings.

**Calculation:**

```
Σ (margin_i * exp(-λ * age_i)) / Σ exp(-λ * age_i)
```

Where `age_i` is games ago.

---

### `margin_h2h|exp_decay|lambda_X|away`

---

### `margin_h2h|exp_decay|lambda_X|diff`

---

## 5️⃣ Venue-Conditioned H2H Margin

### `margin_h2h|season|avg|home|side`

Home team’s average margin **only in prior H2H games where the home team was at home**.

---

### `margin_h2h|season|avg|away|side`

Away team’s average margin **only in prior H2H games where the away team was away**.

---

### `margin_h2h|season|avg|diff|side`

```
home|side − away|side
```

---

### `margin_h2h|exp_decay|lambda_X|home|side`

Exponentially-decayed margin restricted to games where the home team was home.

---

### `margin_h2h|exp_decay|lambda_X|away|side`

---

### `margin_h2h|exp_decay|lambda_X|diff|side`

---

## 6️⃣ Context-Matched H2H Margin

### `margin_h2h|season|avg|home|same_rest`

Average margin for the home team in prior H2H games **where rest-day differential matched the current game**.

---

### `margin_h2h|season|avg|away|same_rest`

---

### `margin_h2h|season|avg|diff|same_rest`

---

### `margin_h2h|season|avg|home|same_conf`

Average margin in prior H2H games **played under same conference alignment**.

---

### `margin_h2h|season|avg|away|same_conf`

---

### `margin_h2h|season|avg|diff|same_conf`

---

## 7️⃣ H2H Sample Size / Reliability Indicators

### `h2h_games_count|season|raw|none`

Number of prior H2H games between these teams this season.

---

### `h2h_games_count|last_n|raw|none`

Number of prior H2H games considered in `last_n` window.

---

### `h2h_games_count|exp_decay|lambda_X|none`

Effective sample size under exponential decay weighting.

---

## 8️⃣ Diff Rule (Global)

For all features with `{home/away}` variants:

```
<stat>|<period>|<calc>|diff
=
<stat>|<period>|<calc>|home
-
<stat>|<period>|<calc>|away
```

This rule applies identically to `|side` and context-restricted variants.

---