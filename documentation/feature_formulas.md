# Feature Formulas Documentation

This document describes the mathematical formulas for each feature included in the master training file (`MASTER_TRAINING.csv`).

## Feature Naming Convention

All features follow the format:
```
{stat_name}|{time_period}|{calc_weight}|{home/away/diff}[|side]
```

### Component Breakdown

1. **`stat_name`**: The base statistic name (e.g., `points`, `efg`, `wins`, `points_net`, `wins_blend`)
2. **`time_period`**: The time window for calculation (e.g., `season`, `games_12`, `months_1`, `blend:season:0.80/games_12:0.20`)
3. **`calc_weight`**: The calculation method (e.g., `avg`, `raw`, `weighted_MPG`, `none`)
4. **`home/away/diff`**: The perspective (home team value, away team value, or difference)
5. **`|side`** (optional): Side-split flag - only includes games where team played at that side

### Examples

- `points|season|avg|diff`: Average points per game difference (home - away) across the season
- `efg|games_12|raw|home`: Effective field goal percentage for home team over last 12 games (aggregated calculation)
- `wins_blend|none|blend:season:0.80/games_12:0.20|diff`: Blended wins feature with 80% season weight, 20% games_12 weight
- `points|season|avg|diff|side`: Points difference using only home games for home team, away games for away team

---

## Blend Feature Notation

Blend features use a special notation in the `time_period` field to encode the exact weights used:

### Format
```
blend:{time_period1}:{weight1}/{time_period2}:{weight2}/...
```

### Rules
- Weights must sum to 1.0 (within floating point tolerance)
- Multiple time periods can be combined (e.g., season + games_20 + games_12)
- Weights are specified as decimals (e.g., `0.80`, `0.20`)

### Examples

1. **Two-component blend**:
   ```
   wins_blend|none|blend:season:0.80/games_12:0.20|diff
   ```
   Formula: `0.80 * wins|season|avg|diff + 0.20 * wins|games_12|avg|diff`

2. **Three-component blend**:
   ```
   points_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|diff
   ```
   Formula: `0.80 * points_net|season|avg|diff + 0.10 * points_net|games_20|avg|diff + 0.10 * points_net|games_12|avg|diff`

### Current Blend Features in Master Training

The master training includes **48 blend features** total (4 base features × 4 weight combinations × 3 perspectives):

#### Base Features:
1. **`wins_blend`** (uses `avg` calculation)
2. **`points_net_blend`** (uses `avg` calculation)
3. **`off_rtg_net_blend`** (uses `raw` calculation)
4. **`efg_net_blend`** (uses `raw` calculation)

#### Weight Combinations (each with `diff`, `home`, `away` versions):

1. **`blend:season:0.80/games_20:0.10/games_12:0.10`**
   - 80% season, 10% games_20, 10% games_12

2. **`blend:season:0.70/games_20:0.20/games_12:0.10`**
   - 70% season, 20% games_20, 10% games_12

3. **`blend:season:0.60/games_20:0.20/games_12:0.20`**
   - 60% season, 20% games_20, 20% games_12

4. **`blend:season:0.80/games_12:0.20`**
   - 80% season, 20% games_12

#### Example Feature Names:
- `wins_blend|none|blend:season:0.80/games_12:0.20|diff`
- `wins_blend|none|blend:season:0.80/games_12:0.20|home`
- `wins_blend|none|blend:season:0.80/games_12:0.20|away`
- `points_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff`
- ... and so on for all 48 combinations

---

## 1. Base Statistics

### Points (`points`)

**Formula**: Total points scored by the team

**Calculation Methods**:
- `avg`: Average points per game across time period
  - `points|season|avg|diff = (Σ home_points / home_games) - (Σ away_points / away_games)`
- `raw`: Total points divided by number of games
  - `points|season|raw|diff = (total_home_points / home_games) - (total_away_points / away_games)`
  - Note: For `raw`, this is equivalent to `avg` for points (since it's already a sum)

**Side-Split**: When `|side` is present, only includes games where team played at that side (home or away)

---

### Effective Field Goal Percentage (`efg`)

**Formula**: 
```
efg = (FGM + 0.5 * 3PM) / FGA * 100
```

Where:
- `FGM` = Field goals made
- `3PM` = Three-pointers made
- `FGA` = Field goal attempts

**Calculation Methods**:
- `avg`: Calculate efg for each game, then average
  - `efg|season|avg|diff = mean([efg_game1, efg_game2, ...])_home - mean([efg_game1, efg_game2, ...])_away`
- `raw`: Aggregate all FGM, 3PM, FGA across time period, then calculate once
  - `efg|season|raw|diff = ((total_FGM + 0.5 * total_3PM) / total_FGA * 100)_home - ((total_FGM + 0.5 * total_3PM) / total_FGA * 100)_away`

**Note**: `raw` is generally preferred for rate statistics as it represents the true rate across the entire time period.

---

### True Shooting Percentage (`ts`)

**Formula**:
```
ts = PTS / (2 * (FGA + 0.44 * FTA)) * 100
```

Where:
- `PTS` = Total points
- `FGA` = Field goal attempts
- `FTA` = Free throw attempts

**Calculation Methods**: Same as `efg` (avg vs raw)

---

### Offensive Rating (`off_rtg`)

**Formula**:
```
off_rtg = (Points / Possessions) * 100
```

Where Possessions are calculated as:
```
Possessions = FGA - OReb + TO + 0.44 * FTA
```

**Calculation Methods**:
- `avg`: Calculate off_rtg for each game, then average
- `raw`: Aggregate all points and possessions across time period, then calculate once
  - `off_rtg|season|raw|diff = (total_points / total_possessions * 100)_home - (total_points / total_possessions * 100)_away`

---

### Defensive Rating (`def_rtg`)

**Formula**:
```
def_rtg = (Opponent Points / Opponent Possessions) * 100
```

Where Opponent Possessions are calculated the same way as above, using opponent's stats.

**Note**: Defensive rating measures points allowed per 100 possessions, so it uses the opponent's offensive stats.

---

### Assist Ratio (`assists_ratio`)

**Formula**:
```
assists_ratio = 100 * (Assists / (FGA + 0.44 * FTA + Assists + TO))
```

**Calculation Methods**: Same as other rate stats (avg vs raw)

---

### Turnover Metric (`to_metric`)

**Formula**:
```
to_metric = 100 * (TO / (FGA + 0.44 * FTA + TO))
```

**Calculation Methods**: Same as other rate stats (avg vs raw)

---

### Three-Point Percentage (`three_pct`)

**Formula**:
```
three_pct = (3PM / 3PA) * 100
```

**Calculation Methods**: Same as other rate stats (avg vs raw)

---

### Wins (`wins`)

**Formula**: Number of games won

**Calculation Methods**:
- `avg`: Win percentage (wins / total games)
  - `wins|season|avg|diff = (home_wins / home_games) - (away_wins / away_games)`
- `raw`: Total wins (same as avg for wins, since it's already a count)

---

### Rebounds, Blocks, Steals, Turnovers

These are counting statistics:

**Formulas**:
- `total_reb|season|avg|diff`: Average rebounds per game
- `blocks|season|avg|diff`: Average blocks per game
- `steals|season|avg|diff`: Average steals per game
- `TO|season|avg|diff`: Average turnovers per game

**Calculation**: Simple average across time period

---

## 2. Net Features (`_net` suffix)

Net features represent the difference between a team's stat and what they've allowed opponents to achieve.

**Formula**:
```
stat_net = team_stat - opponent_stat_allowed
```

**Example**: `points_net|season|raw|home`
1. Calculate team's total points this season
2. Calculate total points opponents scored against this team this season
3. Return `team_points - opponent_points_allowed`

**Available Net Features**:
- `points_net`
- `efg_net`
- `ts_net`
- `three_pct_net`
- `off_rtg_net`
- `assists_ratio_net`

---

## 3. Blend Features (`_blend` suffix)

Blend features are weighted combinations of multiple time periods for the same base statistic.

### General Formula

For a blend feature with components `(time_period1, weight1), (time_period2, weight2), ...`:

```
blend_feature = weight1 * base_stat|time_period1|calc_weight|perspective 
              + weight2 * base_stat|time_period2|calc_weight|perspective 
              + ...
```

### Current Blend Features

#### `wins_blend`

**Base Stat**: `wins`
**Calc Weight**: `avg`
**Available Combinations**:
1. `blend:season:0.80/games_20:0.10/games_12:0.10`
   - Formula: `0.80 * wins|season|avg|diff + 0.10 * wins|games_20|avg|diff + 0.10 * wins|games_12|avg|diff`
2. `blend:season:0.70/games_20:0.20/games_12:0.10`
   - Formula: `0.70 * wins|season|avg|diff + 0.20 * wins|games_20|avg|diff + 0.10 * wins|games_12|avg|diff`
3. `blend:season:0.60/games_20:0.20/games_12:0.20`
   - Formula: `0.60 * wins|season|avg|diff + 0.20 * wins|games_20|avg|diff + 0.20 * wins|games_12|avg|diff`
4. `blend:season:0.80/games_12:0.20`
   - Formula: `0.80 * wins|season|avg|diff + 0.20 * wins|games_12|avg|diff`

**Perspectives**: `diff`, `home`, `away` (12 total features)

---

#### `points_net_blend`

**Base Stat**: `points_net`
**Calc Weight**: `avg`
**Available Combinations**: Same 4 weight combinations as `wins_blend`
**Perspectives**: `diff`, `home`, `away` (12 total features)

**Example**: `points_net_blend|none|blend:season:0.80/games_12:0.20|diff`
- Formula: `0.80 * points_net|season|avg|diff + 0.20 * points_net|games_12|avg|diff`

---

#### `off_rtg_net_blend`

**Base Stat**: `off_rtg_net`
**Calc Weight**: `raw`
**Available Combinations**: Same 4 weight combinations as `wins_blend`
**Perspectives**: `diff`, `home`, `away` (12 total features)

**Example**: `off_rtg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff`
- Formula: `0.70 * off_rtg_net|season|raw|diff + 0.20 * off_rtg_net|games_20|raw|diff + 0.10 * off_rtg_net|games_12|raw|diff`

---

#### `efg_net_blend`

**Base Stat**: `efg_net`
**Calc Weight**: `raw`
**Available Combinations**: Same 4 weight combinations as `wins_blend`
**Perspectives**: `diff`, `home`, `away` (12 total features)

**Example**: `efg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|diff`
- Formula: `0.60 * efg_net|season|raw|diff + 0.20 * efg_net|games_20|raw|diff + 0.20 * efg_net|games_12|raw|diff`

---

## 4. Enhanced Features

### Games Played (`games_played`)

**Formula**: Number of games played by the team in the time period

**Example**: `games_played|season|avg|diff`
- Returns: `home_games_played - away_games_played`

---

### Pace (`pace`)

**Formula**: Possessions per game

```
pace = Possessions / Games
```

Where Possessions are calculated as described in Offensive Rating.

**Example**: `pace|season|avg|diff`
- Returns: `home_pace - away_pace`

---

### Travel (`travel`)

**Formula**: Total travel distance (in miles) over the time period

Uses Haversine formula to calculate distance between venues:
```
distance = 2 * R * arcsin(√(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)))
```
Where R = 3958.8 miles (Earth's radius)

**Example**: `travel|days_12|avg|diff`
- Calculates total miles traveled by each team in last 12 days
- Returns: `home_travel - away_travel`

---

### Back-to-Back (`b2b`)

**Formula**: Binary indicator (1 if back-to-back, 0 otherwise)

```
b2b = 1 if team played yesterday, else 0
```

**Example**: `b2b|none|raw|diff`
- Returns: `home_b2b - away_b2b` (typically -1, 0, or 1)

---

## 5. Player Efficiency Rating (PER) Features

PER is calculated using Hollinger's formula. See `PER_CALCULATION_LOGIC.md` for detailed explanation.

### Base PER Calculation

**Step 1: Calculate uPER (unadjusted PER)**
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

Where:
- `MP` = Minutes played
- `VOP` = Value of Possession = lgPTS / (lgFGA - lgORB + lgTO + 0.44 * lgFTA)
- `DRB%` = Defensive Rebound Percentage = (lgTRB - lgORB) / lgTRB
- `factor` = (2 / 3) - (0.5 * (lgAST / lgFG)) / (2 * (lgFG / lgFT))
- `lg*` = League average

**Step 2: Calculate aPER (pace-adjusted PER)**
```
aPER = uPER * (lgPace / tmPace)
```

**Step 3: Calculate normalized PER**
```
PER = aPER * (15 / lg_aPER)
```

Where `lg_aPER` is the league average aPER (normalized so league average = 15.0)

---

### Team PER Features

#### `player_team_per|season|weighted_MPG|diff`

**Formula**: PER weighted by minutes per game (MPG)

```
weighted_PER = Σ(PER_i * MPG_i) / Σ(MPG_i)
```

Where:
- `PER_i` = PER of player i (season-to-date aggregated)
- `MPG_i` = Minutes per game of player i (total_min / games_played)

**Calculation**:
1. Get all players on team who played before game date
2. Calculate season-to-date PER for each player
3. Calculate MPG for each player
4. Weight PER by MPG and normalize
5. Return: `home_weighted_PER - away_weighted_PER`

---

#### `player_starters_per|season|avg|diff`

**Formula**: Average PER of starters only

```
starters_avg_PER = mean([PER_starter1, PER_starter2, ..., PER_starter5])
```

**Calculation**:
1. Identify starters (top 2 guards, top 2 forwards, top 1 center by games started)
2. Calculate season-to-date PER for each starter
3. Average the starter PERs
4. Return: `home_starters_avg_PER - away_starters_avg_PER`

---

#### `player_per_1|none|weighted_MIN_REC|diff`

**Formula**: Recency-weighted PER of top player by MPG

**Game-Level PER Calculation**:
For each game a player played:
1. Compute PER using that game's box score
2. Use that game's team context (team FG%, assists, pace, etc.)
3. Do NOT use season-aggregated team stats

**Recency Weighting**:
```
w_g = MIN_g * exp(-days_since_game / k)
```

Where:
- `MIN_g` = Minutes played in game g
- `days_since_game` = Days between game g and target game date
- `k` = Recency decay constant (default: 15 days, tunable 10-25 days)

**Final Calculation**:
```
player_PER = Σ(PER_g * w_g) / Σ(w_g)
```

**Selection**:
1. Get top player by MPG (season-to-date)
2. Calculate recency-weighted PER for that player
3. Return: `home_top_player_PER - away_top_player_PER`

**Note**: `time_period = none` because this is an implicit, continuous window (not season-bounded)

---

#### `player_per_2|season|raw|diff`

**Formula**: Season-to-date PER of 2nd highest PER player

**Calculation**:
1. Get all players on team
2. Calculate season-to-date PER for each (aggregated stats, not game-level)
3. Sort by PER (descending)
4. Take 2nd highest PER
5. Return: `home_per2 - away_per2`

**Note**: Uses `raw` calc_weight to indicate season-aggregated calculation (same as `top1_avg`)

---

## 6. Injury Impact Features

### `inj_impact|blend|raw|diff`

**Formula**: Blended injury impact metric

```
inj_impact_blend = 0.45 * injurySeverity + 0.35 * injTop1Per + 0.20 * injRotation
```

Where each component is calculated as follows:

#### `injurySeverity`

**Formula**:
```
injurySeverity = injMinLost / teamRotationMPG
```

Where:
- `injMinLost` = Sum of MPG for injured rotation players (MPG >= 10)
- `teamRotationMPG` = Sum of MPG for all rotation players on team (MPG >= 10)

**Interpretation**: Proportion of rotation minutes lost to injury (0.0 = no impact, 1.0 = entire rotation injured)

---

#### `injTop1Per`

**Formula**: Highest PER among injured players

```
injTop1Per = max([PER_i for all injured players i])
```

**Calculation**:
1. Get all injured players (from `nba_rosters` where `injured = true`)
2. Calculate season-to-date PER for each
3. Return maximum PER

**Note**: If no injured players, returns 0.0

---

#### `injRotation`

**Formula**: Count of injured rotation players

```
injRotation = count([players where injured = true AND MPG >= 10])
```

**Interpretation**: Number of rotation players (MPG >= 10) who are injured

---

#### `injPerValue` (component, not in master training)

**Formula**: Weighted average PER of injured players

```
injPerValue = Σ(PER_i * MPG_weight_i * recency_weight_i) / Σ(MPG_weight_i * recency_weight_i)
```

Where:
- `MPG_weight_i = MPG_i / max_MPG_on_team` (normalized 0-1)
- `recency_weight_i = exp(-days_since_last_game / k)` (k = 15 days)

**Note**: This is a component used in injury feature calculations but not directly in master training

---

### Final Blended Feature

```
inj_impact|blend|raw|diff = (0.45 * home_injurySeverity + 0.35 * home_injTop1Per + 0.20 * home_injRotation) 
                           - (0.45 * away_injurySeverity + 0.35 * away_injTop1Per + 0.20 * away_injRotation)
```

**Interpretation**: 
- Positive values = home team has more injury impact
- Negative values = away team has more injury impact
- Higher absolute value = greater injury impact difference

**Note**: This uses the legacy `blend` format (not the new `blend:...` notation) because it blends different metrics, not time periods.

---

## 7. Elo Rating Features

### `elo|none|raw|diff`

**Formula**: Elo rating difference

```
eloDiff = home_elo - away_elo
```

**Elo Update Formula** (after game):
```
new_elo = old_elo + K * (actual_score - expected_score)
```

Where:
- `K` = Elo K-factor (typically 20 for NBA)
- `actual_score` = 1 if team won, 0 if lost
- `expected_score` = 1 / (1 + 10^((opponent_elo - team_elo) / 400))

**Initial Elo**: Typically 1500 for all teams

**Home Court Advantage**: Often adds ~100 points to home team's Elo for expected score calculation

---

## 8. Rest Features

### `rest|none|raw|diff`

**Formula**: Rest days difference

```
restDiff = home_rest_days - away_rest_days
```

Where `rest_days` = Days since team's last game

**Calculation**:
1. Find team's most recent game before target game date
2. Calculate days between: `(game_date - last_game_date).days`
3. Return: `home_rest_days - away_rest_days`

**Note**: Uses `raw` as calc_weight (not `day_count`) to indicate it's a point-in-time calculation, not an aggregated statistic.

**Interpretation**:
- Positive = home team has more rest
- Negative = away team has more rest
- Typical range: -3 to +3 days

---

## 9. Time Period Calculations

### `season`
All games in the current NBA season up to (but not including) the game date.

**Example**: For a game on Jan 15, 2024 in the 2023-2024 season:
- Includes all games from Oct 2023 to Jan 14, 2024

---

### `months_N`
All games in the last N **calendar months** before the game date.

**Example**: `points|months_1|avg|diff` for a game on Jan 15:
- Includes all games from Dec 15 to Jan 15

---

### `games_N`
The last N games played by the team before the game date, chronologically (most recent N games).

**Example**: `points|games_10|avg|diff`
- Includes the 10 most recent games before the target game

---

### `days_N`
All games played in the last N **calendar days** before the game date.

**Example**: `points|days_10|avg|diff` for a game on Jan 15:
- Includes all games from Jan 5 to Jan 15

---

### `none`
No time period restriction (for special features like `elo`, `rest`, `b2b`, or blend features where time periods are encoded in the blend notation)

---

## 10. Calculation Weight Methods

### `avg` (Per-Game Then Average)
Calculate the stat for each game individually, then average those per-game values.

**Example**: `efg|season|avg|diff`
1. For each game: calculate `efg = (FGM + 0.5 * 3PM) / FGA`
2. Average all per-game efg values
3. Return: `home_avg_efg - away_avg_efg`

**Use Case**: When you want to see average performance per game

---

### `raw` (Aggregate Then Calculate)
Sum all component stats across all games, then calculate the rate stat once from totals.

**Example**: `efg|season|raw|diff`
1. Sum all FGM, 3PM, FGA across all games
2. Calculate once: `efg = (total_FGM + 0.5 * total_3PM) / total_FGA`
3. Return: `home_efg - away_efg`

**Use Case**: When you want the true rate across the entire time period (generally preferred for rate stats)

---

### Special Calc Weights

#### `weighted_MPG`
Weight by minutes per game (used for PER features)

#### `weighted_MIN_REC`
Weight by minutes and recency decay (used for recency-weighted PER)

#### `top1_avg`
Top player by MPG, then use their PER (used for PER features)

#### `none`
No calculation weight (used for blend features, elo, rest, b2b)

---

## 11. Differential Calculation

All features in master training can use `|diff`, `|home`, or `|away` suffix:

### `|diff`
```
feature_diff = home_value - away_value
```

**Interpretation**:
- Positive = home team advantage
- Negative = away team advantage
- Zero = teams are equal

### `|home`
Returns the home team's value only

### `|away`
Returns the away team's value only

---

## 12. Side-Split Features (`|side` suffix)

When `|side` is present, only count games where the team played at that specific side (home or away).

**Example**: `points|season|avg|diff|side`
- For home team: only includes games where they were the home team
- For away team: only includes games where they were the away team
- Then calculates: `home_points_at_home - away_points_at_away`

**Use Case**: Captures venue-specific performance (home court advantage, road performance)

**Available for**: `points`, `wins`, `efg`, `ts`, `off_rtg`, `def_rtg`, `three_pct`, `assists_ratio`

---

## Summary

The master training file includes:
1. **Base statistics** (points, efg, ts, off_rtg, def_rtg, etc.) across multiple time periods
2. **Net features** (difference between team stat and opponent stat allowed)
3. **Blend features** (48 total: 4 base features × 4 weight combinations × 3 perspectives)
4. **Enhanced features** (pace, travel, b2b, games_played)
5. **PER features** (4 specific player-level features)
6. **Injury features** (1 blended injury impact feature)
7. **Elo rating** (team strength metric)
8. **Rest** (days since last game)

All features can be computed with different time periods, calculation weights, and perspectives (home/away/diff).
