# Player-Level Feature Formulas

This document describes the calculation formulas for all player-level features (PER and injury-related) in the master training CSV.

## Table of Contents

1. [PER Features](#per-features)
   - [Base PER Calculation](#base-per-calculation)
   - [Team PER Features](#team-per-features)
   - [Starter PER Features](#starter-per-features)
   - [Individual Player PER Features](#individual-player-per-features)
2. [Injury Features](#injury-features)
   - [Injury Severity](#injury-severity)
   - [Injury PER Features](#injury-per-features)
   - [Injury Minutes Lost](#injury-minutes-lost)
   - [Injury Rotation Count](#injury-rotation-count)
   - [Injury Impact Blend](#injury-impact-blend)

---

## PER Features

### Base PER Calculation

Player Efficiency Rating (PER) is calculated using Hollinger's formula in three steps:

#### Step 1: uPER (Unadjusted PER)

Raw per-minute efficiency rating:

```
uPER = (1 / MP) * [
    3P * (1 / lgAST) * (2 / 3) * (1 - 0.5 * ((AST / FG) / lgAST))
    + (2 / 3) * AST
    + (2 - factor * (tmAST / tmFG)) * FG
    + FT * 0.5 * (1 + (1 - (tmAST / tmFG)) + (2 / 3) * (tmAST / tmFG))
    - VOP * TO
    - VOP * DRB% * (FGA - FG)
    - VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA - FT)
    + VOP * (1 - DRB%) * (TRB - ORB)
    + VOP * DRB% * ORB
    + VOP * STL
    + VOP * DRB% * BLK
    - PF * ((lgFT / lgPF) - 0.44 * (lgFTA / lgPF) * VOP)
]
```

**Variables:**
- `MP` = Minutes played
- `FG` = Field goals made
- `FGA` = Field goal attempts
- `3P` = Three-pointers made
- `FT` = Free throws made
- `FTA` = Free throw attempts
- `TRB` = Total rebounds
- `ORB` = Offensive rebounds
- `AST` = Assists
- `STL` = Steals
- `BLK` = Blocks
- `TO` = Turnovers
- `PF` = Personal fouls
- `tmAST` = Team assists
- `tmFG` = Team field goals made
- `lgAST` = League average assists
- `lgFT` = League average free throws made
- `lgPF` = League average personal fouls
- `lgFTA` = League average free throw attempts

**League Constants:**
- `VOP` = Value of Possession = `lgPTS / (lgFGA - lgORB + lgTO + 0.44 * lgFTA)`
- `DRB%` = Defensive Rebound Percentage = `(lgTRB - lgORB) / lgTRB`
- `factor` = `(2 / 3) - (0.5 * (lgAST / lgFG)) / (2 * (lgFG / lgFT))`

#### Step 2: aPER (Pace-Adjusted PER)

Adjusts for team pace differences:

```
aPER = uPER * (lgPace / tmPace)
```

Where:
- `lgPace` = League average pace (possessions per game)
- `tmPace` = Team pace (possessions per game)

#### Step 3: PER (Normalized)

Normalizes so league average = 15.0:

```
PER = aPER * (15 / lg_aPER)
```

Where `lg_aPER` is the league average aPER (minutes-weighted) for the season.

**Code Location:** `cli/per_calculator.py`
- `compute_uper()` - lines 265-350
- `compute_aper()` - lines 352-356
- `compute_per()` - lines 358-374

---

### Team PER Features

#### `player_team_per|season|weighted_MPG|{home/away/diff}`

**Description:** Team average PER weighted by minutes per game (MPG).

**Formula:**
```
weighted_PER = Σ(PER_i * MPG_i) / Σ(MPG_i)
```

Where:
- `PER_i` = Season-to-date PER of player i
- `MPG_i` = Minutes per game of player i = `total_minutes / games_played`

**Calculation Process:**
1. Get all players on team who played before game date
2. Calculate season-to-date aggregated PER for each player:
   - Aggregate all player stats (points, rebounds, assists, etc.) from games before target date
   - Calculate uPER using aggregated stats and team context
   - Calculate aPER using team pace
   - Normalize to PER using league average aPER
3. Calculate MPG for each player (total minutes / games played)
4. Weight each player's PER by their MPG
5. Sum weighted PERs and divide by sum of MPGs

**Feature Versions:**
- `player_team_per|season|weighted_MPG|home`: Home team weighted PER
- `player_team_per|season|weighted_MPG|away`: Away team weighted PER
- `player_team_per|season|weighted_MPG|diff`: `home - away`

**Example:**
- Home team: Player A (PER=20, MPG=30), Player B (PER=15, MPG=25), Player C (PER=10, MPG=20)
- Weighted PER = (20×30 + 15×25 + 10×20) / (30 + 25 + 20) = 1175 / 75 = 15.67

**Code Location:** `cli/per_calculator.py` - `compute_team_per_features()` method

---

### Starter PER Features

#### `player_starters_per|season|avg|{home/away/diff}`

**Description:** Average PER of starting players only.

**Formula:**
```
starters_avg_PER = mean([PER_starter1, PER_starter2, ..., PER_starter5])
```

**Calculation Process:**
1. Identify starters:
   - Top 2 guards by games started
   - Top 2 forwards by games started
   - Top 1 center by games started
   - A player is considered a starter if `starter_games > total_games / 2`
2. Calculate season-to-date PER for each starter (same process as team PER)
3. Average the starter PERs

**Feature Versions:**
- `player_starters_per|season|avg|home`: Home team starters average PER
- `player_starters_per|season|avg|away`: Away team starters average PER
- `player_starters_per|season|avg|diff`: `home - away`

**Example:**
- Home starters: PER values [22, 18, 16, 14, 12]
- Starters avg PER = (22 + 18 + 16 + 14 + 12) / 5 = 16.4

**Code Location:** `cli/per_calculator.py` - `compute_team_per_features()` method

---

### Individual Player PER Features

#### `player_per_1|none|weighted_MIN_REC|{home/away/diff}`

**Description:** Recency-weighted PER of the top player by MPG.

**Key Difference:** This feature uses **game-level PER** (not season-aggregated) with recency weighting.

**Game-Level PER Calculation:**
For each game a player played:
1. Compute PER using that game's box score
2. Use that game's team context (team FG%, assists, pace, etc.)
3. Do NOT use season-aggregated team stats

**Recency Weighting Formula:**
```
w_g = MIN_g * exp(-days_since_game / k)
```

Where:
- `MIN_g` = Minutes played in game g
- `days_since_game` = Days between game g and target game date
- `k` = Recency decay constant (default: 15 days, tunable 10-25 days)

**Final Calculation:**
```
player_PER = Σ(PER_g * w_g) / Σ(w_g)
```

**Process:**
1. Get top player by MPG (season-to-date)
2. For each game that player played before target date:
   - Calculate PER using that game's box score and team context
   - Calculate recency weight: `MIN_g * exp(-days_since_game / 15)`
3. Weight each game's PER by its recency weight
4. Sum weighted PERs and divide by sum of weights

**Feature Versions:**
- `player_per_1|none|weighted_MIN_REC|home`: Home team top player recency-weighted PER
- `player_per_1|none|weighted_MIN_REC|away`: Away team top player recency-weighted PER
- `player_per_1|none|weighted_MIN_REC|diff`: `home - away`

**Example:**
- Top player played 3 games:
  - Game 1 (5 days ago, 30 min): PER=22, weight = 30 × exp(-5/15) = 30 × 0.717 = 21.5
  - Game 2 (10 days ago, 28 min): PER=20, weight = 28 × exp(-10/15) = 28 × 0.513 = 14.4
  - Game 3 (20 days ago, 32 min): PER=18, weight = 32 × exp(-20/15) = 32 × 0.264 = 8.4
- Weighted PER = (22×21.5 + 20×14.4 + 18×8.4) / (21.5 + 14.4 + 8.4) = 1010.2 / 44.3 = 22.8

**Code Location:** `cli/per_calculator.py` - `get_player_recency_weighted_per()` method

---

#### `player_per_2|season|raw|{home/away/diff}`

**Description:** Season-to-date PER of the second-best player by MPG.

**Formula:**
```
player_per_2 = PER of 2nd player by MPG (season-to-date aggregated)
```

**Calculation Process:**
1. Get all players on team who played before game date
2. Sort by MPG (descending)
3. Take 2nd player
4. Calculate season-to-date aggregated PER for that player (same as team PER calculation)

**Feature Versions:**
- `player_per_2|season|raw|home`: Home team 2nd player PER
- `player_per_2|season|raw|away`: Away team 2nd player PER
- `player_per_2|season|raw|diff`: `home - away`

**Example:**
- Team players sorted by MPG: Player A (MPG=35, PER=22), Player B (MPG=30, PER=18), ...
- `player_per_2` = 18 (PER of Player B)

**Code Location:** `cli/per_calculator.py` - `compute_team_per_features()` method

---

## Injury Features

Injury features measure the impact of injured players on team performance. All injury features use `time_period='none'` because they are calculated based on the current injury status at game time, not aggregated over a time period.

### Injury Severity

#### `inj_severity|none|raw|{home/away/diff}`

**Description:** Proportion of rotation minutes lost due to injuries.

**Formula:**
```
injurySeverity = injMinLost / teamRotationMPG
```

Where:
- `injMinLost` = Sum of MPG for injured rotation players (MPG >= 10)
- `teamRotationMPG` = Sum of MPG for all rotation players on team (MPG >= 10)

**Calculation Process:**
1. Get injured player list from game document (`game.homeTeam.injured_players` or `game.awayTeam.injured_players`)
2. Get season-to-date MPG for each injured player
3. Filter to rotation players only (MPG >= 10)
4. Sum MPG of injured rotation players = `injMinLost`
5. Get total rotation MPG for team = `teamRotationMPG`
6. Calculate severity = `injMinLost / teamRotationMPG`

**Feature Versions:**
- `inj_severity|none|raw|home`: Home team injury severity (0.0 to 1.0)
- `inj_severity|none|raw|away`: Away team injury severity (0.0 to 1.0)
- `inj_severity|none|raw|diff`: `home - away`

**Example:**
- Team rotation MPG = 240 (sum of all rotation players)
- Injured rotation players: Player A (MPG=30), Player B (MPG=25)
- `injMinLost` = 55
- `injurySeverity` = 55 / 240 = 0.229 (22.9% of rotation minutes lost)

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

### Injury PER Features

#### `inj_per|none|weighted_MIN|{home/away/diff}`

**Description:** Weighted average PER of injured players (weighted by MPG and recency).

**Formula:**
```
injPerValue = Σ(PER_i * MPG_weight_i * recency_weight_i)
```

Where:
- `PER_i` = Season-to-date PER of injured player i
- `MPG_weight_i` = `MPG_i / max_MPG_on_team` (normalized 0-1)
- `recency_weight_i` = `exp(-days_since_last_game / k)` where k=15 days

**Calculation Process:**
1. Get injured player list
2. For each injured player:
   - Get season-to-date PER
   - Get MPG (normalized by max MPG on team)
   - Get days since last game
   - Calculate recency weight: `exp(-days_since / 15)`
   - Weighted PER contribution = `PER × MPG_weight × recency_weight`
3. Sum all weighted PER contributions

**Feature Versions:**
- `inj_per|none|weighted_MIN|home`: Home team weighted injured PER
- `inj_per|none|weighted_MIN|away`: Away team weighted injured PER
- `inj_per|none|weighted_MIN|diff`: `home - away`

**Example:**
- Injured players:
  - Player A: PER=20, MPG=30, days_since=5
    - MPG_weight = 30/35 = 0.857
    - Recency_weight = exp(-5/15) = 0.717
    - Contribution = 20 × 0.857 × 0.717 = 12.3
  - Player B: PER=15, MPG=25, days_since=10
    - MPG_weight = 25/35 = 0.714
    - Recency_weight = exp(-10/15) = 0.513
    - Contribution = 15 × 0.714 × 0.513 = 5.5
- `injPerValue` = 12.3 + 5.5 = 17.8

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

#### `inj_per|none|top1_avg|{home/away/diff}`

**Description:** Highest PER among injured players.

**Formula:**
```
injTop1Per = max([PER_i for all injured players i])
```

**Calculation Process:**
1. Get injured player list
2. Get season-to-date PER for each injured player
3. Return maximum PER value

**Feature Versions:**
- `inj_per|none|top1_avg|home`: Home team top injured player PER
- `inj_per|none|top1_avg|away`: Away team top injured player PER
- `inj_per|none|top1_avg|diff`: `home - away`

**Example:**
- Injured players: PER values [20, 15, 12, 8]
- `injTop1Per` = 20

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

#### `inj_per|none|top3_sum|{home/away/diff}`

**Description:** Sum of top 3 injured players' PERs.

**Formula:**
```
injTop3PerSum = sum(sorted([PER_i], reverse=True)[:3])
```

**Calculation Process:**
1. Get injured player list
2. Get season-to-date PER for each injured player
3. Sort PERs in descending order
4. Sum top 3 PERs

**Feature Versions:**
- `inj_per|none|top3_sum|home`: Home team top 3 injured PER sum
- `inj_per|none|top3_sum|away`: Away team top 3 injured PER sum
- `inj_per|none|top3_sum|diff`: `home - away`

**Example:**
- Injured players: PER values [20, 15, 12, 8, 5]
- Sorted: [20, 15, 12, 8, 5]
- Top 3: [20, 15, 12]
- `injTop3PerSum` = 20 + 15 + 12 = 47

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

### Injury Minutes Lost

#### `inj_min_lost|none|raw|{home/away/diff}`

**Description:** Total minutes per game lost from injured rotation players.

**Formula:**
```
injMinLost = Σ(MPG_i) for all injured rotation players i where MPG_i >= 10
```

**Calculation Process:**
1. Get injured player list
2. Get season-to-date MPG for each injured player
3. Filter to rotation players only (MPG >= 10)
4. Sum MPG of injured rotation players

**Feature Versions:**
- `inj_min_lost|none|raw|home`: Home team minutes lost
- `inj_min_lost|none|raw|away`: Away team minutes lost
- `inj_min_lost|none|raw|diff`: `home - away`

**Example:**
- Injured rotation players: Player A (MPG=30), Player B (MPG=25), Player C (MPG=12)
- `injMinLost` = 30 + 25 + 12 = 67 minutes per game

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

### Injury Rotation Count

#### `inj_rotation_per|none|raw|{home/away/diff}`

**Description:** Count of injured rotation players (MPG >= 10).

**Formula:**
```
injRotation = count([injured players i where MPG_i >= 10])
```

**Calculation Process:**
1. Get injured player list
2. Get season-to-date MPG for each injured player
3. Count players with MPG >= 10

**Feature Versions:**
- `inj_rotation_per|none|raw|home`: Home team injured rotation count
- `inj_rotation_per|none|raw|away`: Away team injured rotation count
- `inj_rotation_per|none|raw|diff`: `home - away`

**Example:**
- Injured players: 5 total
- Rotation players (MPG >= 10): 3
- `injRotation` = 3

**Code Location:** `cli/StatHandlerV2.py` - `_calculate_team_injury_features()` method

---

### Injury Impact Blend

#### `inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|{home/away/diff}`

**Description:** Weighted combination of injury metrics to measure overall injury impact.

**Formula:**
```
inj_impact = 0.45 × injurySeverity + 0.35 × injTop1Per + 0.20 × injRotation
```

Where:
- `injurySeverity` = `inj_severity|none|raw` (proportion of rotation minutes lost, 0.0-1.0)
- `injTop1Per` = `inj_per|none|top1_avg` (highest injured player PER, typically 0-30)
- `injRotation` = `inj_rotation_per|none|raw` (count of injured rotation players, typically 0-5)

**Blend Weights:**
- **Severity (0.45)**: Most important - measures proportion of rotation lost
- **Top1 PER (0.35)**: Important - measures quality of best injured player
- **Rotation Count (0.20)**: Less important - measures depth of injuries

**Feature Versions:**
- `inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home`: Home team injury impact
- `inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away`: Away team injury impact
- `inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff`: `home - away`

**Example:**
- Home team:
  - `injurySeverity` = 0.30 (30% of rotation lost)
  - `injTop1Per` = 22 (best injured player has PER 22)
  - `injRotation` = 2 (2 rotation players injured)
- `inj_impact` = 0.45 × 0.30 + 0.35 × 22 + 0.20 × 2 = 0.135 + 7.7 + 0.4 = 8.235

**Note:** The blend combines normalized (severity, 0-1) and raw (PER, rotation count) metrics. The PER component dominates the value, so typical ranges are 0-15 for teams with no injuries to 20+ for teams with star players injured.

**Code Location:** `cli/StatHandlerV2.py` - `get_injury_features()` method (lines 2455-2484)

---

## Feature Naming Convention

All player-level features follow the standard naming convention:

```
{stat_name}|{time_period}|{calc_weight}|{perspective}
```

**For PER Features:**
- `stat_name`: `player_team_per`, `player_starters_per`, `player_per_1`, `player_per_2`
- `time_period`: `season` (season-to-date aggregated) or `none` (recency-weighted, no time aggregation)
- `calc_weight`: `weighted_MPG`, `avg`, `weighted_MIN_REC`, `raw`, `top1_avg`
- `perspective`: `home`, `away`, `diff`

**For Injury Features:**
- `stat_name`: `inj_severity`, `inj_per`, `inj_min_lost`, `inj_rotation_per`, `inj_impact`
- `time_period`: `none` (calculated at game time, not aggregated)
- `calc_weight`: `raw`, `weighted_MIN`, `top1_avg`, `top3_sum`, `blend:...`
- `perspective`: `home`, `away`, `diff`

---

## Implementation Notes

### Data Sources

**PER Features:**
- Player stats: `stats_nba_players` collection
- Team stats: `stats_nba` collection (for team context in PER calculation)
- League stats: Cached in `league_stats_cache` collection

**Injury Features:**
- Injured players: `stats_nba` collection (`homeTeam.injured_players`, `awayTeam.injured_players`)
- Player stats: `stats_nba_players` collection (for MPG and PER calculations)

### Temporal Constraints

All features use data **before the target game date** to prevent data leakage:
- Season-to-date aggregations exclude the target game
- Recency-weighted features only use games before the target date
- Injury features use current injury status at game time (from game document)

### Performance Optimizations

- PER calculations use preloaded caches to avoid 27k+ DB queries
- Injury features use preloaded player stats for fast MPG lookups
- League constants are cached per season
- Team pace values are cached

**Code Locations:**
- PER Calculator: `cli/per_calculator.py`
- Injury Features: `cli/StatHandlerV2.py` - `get_injury_features()` and `_calculate_team_injury_features()`
- Master Training Generation: `cli/master_training_data.py`
