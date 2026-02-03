This is what should live in your **authoritative feature definition registry**.

---

# A) Missing `calc_weight` definitions (FULL, CANONICAL)

These define **how values are aggregated**, independent of window or side.

---

## `std`

**Name:** standard deviation

**Definition:**
Sample standard deviation of per-game stat values over the selected game set.

**Formula:**

* If `n >= 2`:

```text
std = sqrt( (1 / (n - 1)) * Σ (x_i - mean)^2 )
```

* If `n < 2`:

```text
std = 0.0
```

---

## `top1_avg`, `top2_avg`, `top3_avg`

**Selection rule (canonical):**

* Rank players by **minutes per game (MPG)** over the same window.
* Select top N players.

**Definition:**

```text
topN_avg = (1 / N') * Σ s_i
```

where:

* `s_i` = stat value for player *i*
* `N' = min(N, number of available players)`

**Edge case:**

* If no eligible players → `0.0`

---

## `top1_weighted_MPG`, `top2_weighted_MPG`, `top3_weighted_MPG`

**Selection rule:**

* Rank players by MPG over the window.
* Select top N players.

**Definition:**

```text
topN_weighted_MPG = Σ (s_i * mpg_i) / Σ mpg_i
```

**Edge case:**

* If `Σ mpg_i == 0` → `0.0`

---

## `top3_sum`

**Selection rule:**

* Rank players by MPG.
* Select top 3.

**Definition:**

```text
top3_sum = Σ s_i
```

**Edge case:**

* If fewer than 3 players exist → sum what is available.

---

## `weighted_MIN`

**Purpose:** Injury impact weighted by minutes lost.

**Definition:**

```text
weighted_MIN = Σ (v_i * min_lost_i) / Σ min_lost_i
```

Where:

* `v_i` = player value metric (PER / player_per)
* `min_lost_i` = expected minutes missed for player *i*

**Edge case:**

* If `Σ min_lost_i == 0` → `0.0`

---

## `weighted_MIN_REC`

**Purpose:** Injury impact with recency decay.

**Recency weight function:**

```text
w_rec(d) = exp(-d / τ)
```

Canonical:

* `τ = 14` days

**Definition:**

```text
weighted_MIN_REC =
Σ (v_i * min_lost_i * w_rec(d_i)) / Σ (min_lost_i * w_rec(d_i))
```

Where:

* `d_i` = days since player *i* last played

**Edge case:**

* If denominator is `0` → `0.0`

---

# B) Missing stat definitions (WHAT the stat means)

---

## `ast_to_ratio`

**Definition:**

```text
ast_to_ratio = Σ assists / max(Σ turnovers, 1)
```

---

## `rest` (deprecated) and `days_rest`

### `days_rest`

**Definition:**

```text
days_rest = min( (game_date - previous_game_date).days, 7 )
```

**Edge case:**

* If no previous game exists → `days_rest = 7`

### `rest`

**Canonical alias:**

```text
rest ≡ days_rest
```

---

## Injury-related stats

---

### `inj_min_lost`

**Definition:**

```text
inj_min_lost = Σ expected_minutes_missing(player)
```

**Expected minutes missing:**

* Prefer projected minutes
* Else fallback to season MPG (or last-10 MPG)

---

### `inj_severity`

**Canonical severity scale:**

```text
OUT           = 1.00
DOUBTFUL      = 0.75
QUESTIONABLE  = 0.50
PROBABLE      = 0.25
```

**Definition:**

```text
inj_severity = Σ (severity_i * expected_minutes_missing_i)
               / max(Σ expected_minutes_missing_i, 1)
```

---

### `inj_per`

**Player value:** PER or `player_per`

Variants:

* `top3_sum`:

```text
inj_per_top3_sum = Σ (PER of top 3 injured players)
```

* `top1_avg`:

```text
inj_per_top1_avg = max(PER of injured players)
```

* `weighted_MIN`:

```text
inj_per_weighted_MIN = Σ (PER_i * min_lost_i) / Σ min_lost_i
```

---

### `inj_rotation_per`

**Definition:**

1. Define rotation players = top 8 by MPG.
2. Compute:

```text
inj_rotation_per = Σ mpg_i (injured rotation players)
                   / Σ mpg_i (all rotation players)
```

---

## Player talent stats

---

### `player_team_per`

**Definition:**

```text
player_team_per = Σ (PER_i * mpg_i) / Σ mpg_i
```

Eligible players:

* Games played ≥ minimum threshold (e.g., 5)

---

### `player_starters_per`

**Starter identification (canonical):**

* Top 5 players by start count in last 5 games
* Fallback: top 5 by MPG

**Definition:**

```text
player_starters_per = mean(PER of starter set)
```

---

### `player_per|season|topN_*`

**Ranking rule:**

* Rank players by season MPG.

**Definitions:**

* `player_per_1` = PER of top MPG player
* `player_per_2` = PER of 2nd MPG player
* `player_per_3` = PER of 3rd MPG player

---

### `player_per_1|none|weighted_MIN_REC`

**Definition:**

```text
if player_1 is injured:
    value = PER_1 * min_lost_1 * w_rec(days_since_last_played)
else:
    value = 0.0
```

---

# C) Blend stat definitions

---

## `*_blend`

**General form:**

```text
blend:window1:w1/window2:w2/...
```

**Definition:**

```text
blend_value = Σ (w_k * value(window_k))
```

**Edge case:**

* If a window has no data → omit it and renormalize weights.

---

# D) Selection & window rules (canonical)

* Ranking by **MPG**
* Windows:

  * `season`: season-to-date
  * `months_1`: last 30 days
  * `games_N`: last N games
* If fewer than N games exist → use available games
* `diff` computed as:

```text
home_value − away_value
```

---

--UPDATE--

# 1) `player_per_1|none|weighted_MIN_REC|diff` — is `diff` meaningful?

Yes, it’s meaningful, and your interpretation is correct.

## Canonical definition

Compute home and away independently, then subtract:

```text
player_per_1|none|weighted_MIN_REC|home =
  (PER_topMPG_home * min_lost_topMPG_home * w_rec(days_since_last_played_topMPG_home))
  if topMPG_home is OUT (misses game)
  else 0

player_per_1|none|weighted_MIN_REC|away = same for away

player_per_1|none|weighted_MIN_REC|diff = home_value - away_value
```

## What it captures

* Non-zero when:

  * one team’s “minutes leader” is out and the other’s isn’t, **or**
  * both are out but with different PER/min_lost/recency
* This is a strong “**star availability shock**” feature. It’s *supposed* to be sparse and asymmetric.

✅ Keep it as-is.

---

# 2) `player_per|season|top1_avg` vs `player_per_1|season|raw` — are they identical?

Under the canonical rules you and I laid out: **they should be identical** if:

* “top1” selection is by MPG
* `top1_avg` is average over the top1 set
* `player_per_1` is PER of the top MPG player

So yes: **they are redundant**.

## Canonical resolution

Pick one representation as SSoT and treat the other as an alias.

### Recommended SSoT

✅ Keep **slot-based** naming for player rank features:

* `player_per_1|season|raw|{home/away/diff}`
* `player_per_2|season|raw|...`
* `player_per_3|season|raw|...`

### Alias mapping

Define:

```text
player_per|season|top1_avg|X  := player_per_1|season|raw|X
```

And optionally:

```text
player_per|season|top2_avg|X  := mean(player_per_1, player_per_2)
player_per|season|top3_avg|X  := mean(player_per_1, player_per_2, player_per_3)
```

But **don’t** keep both as separate computed features—just alias or deprecate one.

---

# 3) `harmonic_mean` — define it explicitly

## Canonical definition

For two nonnegative scalars `a`, `b`:

If `a > 0 and b > 0`:

```text
harmonic_mean(a,b) = 2ab / (a + b)
```

Fallbacks:

* If exactly one is > 0: return the non-zero value
* If both are 0/missing: return a baseline (league or season baseline)

This is the exact definition your agent should implement for `pace_interaction_*`.

---

# 4) `derived` — make formulas explicit (`est_possessions_*`, `exp_points_*`)

Below are explicit formulas with exact feature names.

## 4.1 `est_possessions_*`

These are matchup scalars derived from pace interaction. (Same value for home/away in v1.)

Inputs:

* `pace_interaction_season|none|harmonic_mean|none`
* `pace_interaction_games_10|none|harmonic_mean|none`

Definitions:

```text
est_possessions_season|none|derived|home = pace_interaction_season|none|harmonic_mean|none
est_possessions_season|none|derived|away = pace_interaction_season|none|harmonic_mean|none

est_possessions_games_10|none|derived|home = pace_interaction_games_10|none|harmonic_mean|none
est_possessions_games_10|none|derived|away = pace_interaction_games_10|none|harmonic_mean|none
```

## 4.2 `exp_points_off_*`

Assuming `off_rtg` is points per 100 possessions:

```text
exp_points_off_season|none|derived|home =
  (off_rtg|season|raw|home / 100.0) * est_possessions_season|none|derived|home

exp_points_off_season|none|derived|away =
  (off_rtg|season|raw|away / 100.0) * est_possessions_season|none|derived|away

exp_points_off_games_10|none|derived|home =
  (off_rtg|games_10|raw|home / 100.0) * est_possessions_games_10|none|derived|home

exp_points_off_games_10|none|derived|away =
  (off_rtg|games_10|raw|away / 100.0) * est_possessions_games_10|none|derived|away
```

Diff variants (if you want them):

```text
exp_points_off_season|none|derived|diff = exp_points_off_season_home - exp_points_off_season_away
exp_points_off_games_10|none|derived|diff = exp_points_off_games_10_home - exp_points_off_games_10_away
```

## 4.3 `exp_points_def_*` (expected points allowed)

Assuming `def_rtg` is points allowed per 100 possessions:

```text
exp_points_def_season|none|derived|home =
  (def_rtg|season|raw|home / 100.0) * est_possessions_season|none|derived|home

exp_points_def_season|none|derived|away =
  (def_rtg|season|raw|away / 100.0) * est_possessions_season|none|derived|away

exp_points_def_games_10|none|derived|home =
  (def_rtg|games_10|raw|home / 100.0) * est_possessions_games_10|none|derived|home

exp_points_def_games_10|none|derived|away =
  (def_rtg|games_10|raw|away / 100.0) * est_possessions_games_10|none|derived|away
```

---

# Conflict resolution decisions

## Conflict A: `weighted_MIN_REC` decay (τ=14 in doc vs k=15 in code)

### Recommendation: **align docs to code** (least risky)

Your models already learned behavior around whatever’s implemented. Changing decay changes feature distribution and can shift performance.

✅ Canonical decision:

* Set **τ = 15 days** in the SSoT doc for `weighted_MIN_REC` to match `per_calculator.py:1903`.

If you later want to retune:

* treat τ as a hyperparameter and version it (e.g., `weighted_MIN_REC_tau15`), but don’t silently change it.

---

## Conflict B: `inj_severity` formula (status-based in doc vs minutes-lost proportion in code)

### Recommendation: **keep existing code formula as canonical** (for now)

Your current implementation:

```text
inj_severity = inj_min_lost / team_rotation_mpg
```

is actually a *very reasonable* “severity” proxy:

* it normalizes minutes lost by how many minutes matter (rotation)
* it’s continuous and stable
* and it doesn’t require reliable status tags (which are often messy)

✅ Canonical decision (SSoT):
Define `inj_severity|none|raw|X` as:

```text
team_rotation_mpg = Σ mpg_i for top 8 players by season MPG   (or season-to-date MPG)
inj_severity = inj_min_lost / max(team_rotation_mpg, 1)
```

and **drop** the status-scale definition unless/until you actually have injury status data you trust.

If you later want a status-aware version, add it as a *new stat*:

* `inj_status_severity|none|raw|...`

Don’t overload `inj_severity` with two meanings.

---

--UPDATE2--

1. Here’s the **exact, unambiguous SSoT** for `exp_points_matchup_*` (home/away) in a way that is consistent with how `off_rtg` / `def_rtg` are defined (points per 100 possessions) and with your existing `est_possessions_*`.

## Core idea

For each team, build an expected PPP by combining:

* that team’s **offense** (off_rtg)
* opponent’s **defense** (def_rtg)

Then multiply by estimated possessions.

---

# 1) Define matchup PPP (points per possession)

Use the **average of offense PPP and opponent defense PPP**.

For a given window `W` (season or games_10):

```text
home_ppp_matchup_W =
  0.5 * (off_rtg_W_home / 100.0) +
  0.5 * (def_rtg_W_away / 100.0)

away_ppp_matchup_W =
  0.5 * (off_rtg_W_away / 100.0) +
  0.5 * (def_rtg_W_home / 100.0)
```

Why this is the clean default:

* symmetric
* stable
* doesn’t overfit
* consistent units (PPP)

*(If you later want, you can tune the 0.5/0.5 weights, but this is the canonical v1.)*

---

# 2) Multiply by estimated possessions

Let `poss_W` be:

* Season: `est_possessions_season|none|derived|home` (same as away)
* Games_10: `est_possessions_games_10|none|derived|home` (same as away)

Then:

## Season

```text
exp_points_matchup_season|none|derived|home =
  home_ppp_matchup_season * est_possessions_season|none|derived|home

exp_points_matchup_season|none|derived|away =
  away_ppp_matchup_season * est_possessions_season|none|derived|away
```

## Games_10

```text
exp_points_matchup_games_10|none|derived|home =
  home_ppp_matchup_games_10 * est_possessions_games_10|none|derived|home

exp_points_matchup_games_10|none|derived|away =
  away_ppp_matchup_games_10 * est_possessions_games_10|none|derived|away
```

---

# 3) Fully expanded formulas (copy/paste)

## Season

```text
exp_points_matchup_season|none|derived|home =
  (
    0.5 * (off_rtg|season|raw|home / 100.0) +
    0.5 * (def_rtg|season|raw|away / 100.0)
  )
  * est_possessions_season|none|derived|home

exp_points_matchup_season|none|derived|away =
  (
    0.5 * (off_rtg|season|raw|away / 100.0) +
    0.5 * (def_rtg|season|raw|home / 100.0)
  )
  * est_possessions_season|none|derived|away
```

## Games_10

```text
exp_points_matchup_games_10|none|derived|home =
  (
    0.5 * (off_rtg|games_10|raw|home / 100.0) +
    0.5 * (def_rtg|games_10|raw|away / 100.0)
  )
  * est_possessions_games_10|none|derived|home

exp_points_matchup_games_10|none|derived|away =
  (
    0.5 * (off_rtg|games_10|raw|away / 100.0) +
    0.5 * (def_rtg|games_10|raw|home / 100.0)
  )
  * est_possessions_games_10|none|derived|away
```

---

# 4) Edge handling (minimal and consistent)

* If any required input is missing:

  * fall back to the season version (if computing games_10), else 0.0
* `est_possessions_*` already has its own fallback rules, so you typically won’t hit missing possessions.

---

If you want a slightly more “basketball-true” variant later, the next step is a *log-space blend* (geometric mean) for PPP instead of the arithmetic mean. But the arithmetic mean above is the cleanest canonical default for v1.

2. avg means per game avg, raw means over time period (same for "single" stats like points -- different for "rate stats" like efg). i.e. efg|season|avg is average efg per game this season; efg|season|raw is efg this season (not calculating efg per game at all). For single game stats, only include avg (raw would be the same calculation for these)
3. make days_N and games_N all valid according to the registry (where N is any int). I know this means there are infinite feature possibilities, but is there a clean practice way to implmenent this in the feature registry core SSoT?
4. For all redundancies that follow this example's pattern: player_per|season|top1_avg and player_per_1|season|raw -- use player_per|season|top1_avg