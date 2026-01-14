# Feature Naming Formula and Calculation Guide

## Feature Name Format

```
{stat_name}|{time_period}|{calc_weight}|{home/away/diff}[|side]
```

### Components

1. **`stat_name`**: The statistic being measured (e.g., `points`, `efg`, `off_rtg`, `points_net`)
2. **`time_period`**: The time window for the calculation
   - `season`: Full season up to the game date
   - `months_N`: Last N months (e.g., `months_1`, `months_3`)
   - `games_N`: Last N games (e.g., `games_10`, `games_20`)
   - `days_N`: Last N days (e.g., `days_2`, `days_5`)
   - `none`: No time period (for special features like `elo`, `rest`)
3. **`calc_weight`**: How the statistic is calculated
   - `avg`: Per-game average approach
   - `raw`: Aggregate-first approach
   - Special calc_weights: `weighted_MPG`, `weighted_MIN`, `top1_avg`, `top3_sum`, etc. (for PER, injury features)
4. **`home/away/diff`**: The perspective
   - `diff`: Home team stat - Away team stat (differential)
   - `home`: Home team's absolute value
   - `away`: Away team's absolute value
   - `none`: Special features that don't have home/away/diff (e.g., `per_available`)
5. **`side`** (optional): Side-split calculation
   - When present, only count games where the team played at that side (home or away)
   - Only applies to certain stats: `points`, `wins`, `efg`, `ts`, `off_rtg`, `def_rtg`

## Current Feature Generation Process (Step-by-Step)

**Step 1: Feature Names List**
- We have a list of feature names we want: `['points|season|avg|diff', 'points|season|raw|home', 'efg|season|raw|diff|side', ...]`

**Step 2: Extract What We Need**
- Parse each feature name to extract: stat_name, time_period, calc_weight, home/away/diff, side
- Build a list of stat tokens (e.g., `['pointsSznAvg', 'pointsSznAvg_side', 'effective_fg_percSznAvg_side']`)
- Group by calc_weight to see what we need: `{'raw': [...], 'avg': [...]}`

**Step 3: Call getStatAvgDiffs**
- For each calc_weight (e.g., 'raw', 'avg'), call `getStatAvgDiffs()` once
- `getStatAvgDiffs` takes the stat tokens list and returns a **flat array of numbers**
- The array order matches `self.classifier_features` order
- For each stat, it returns: `[diff]` OR `[diff, home_abs, away_abs]` if include_absolute and key stat

**Step 4: Map Numbers Back to Feature Names**
- We have arrays like: `[points_diff, points_home, points_away, points_side_diff, wins_diff, ...]`
- We try to map these back to feature names like `'points|season|avg|diff'`
- **This is where it breaks!** The mapping is complex because:
  - We need to track which index corresponds to which stat
  - We need to account for absolute values (home/away) that may or may not be present
  - We need to handle side-split stats separately
  - The order must match exactly, or we get wrong values or zeros

**Step 5: Build features_dict**
- We create a dictionary: `{'points|season|avg|diff': 5.2, 'points|season|raw|home': 105.0, ...}`
- This gets mapped to the feature_headers order when writing to CSV

**The Problem**: Steps 3-4 are fragile. We're converting feature names → stat tokens → flat array → back to feature names. If the order is wrong, we get zeros or incorrect values.

## Proposed New Architecture

Instead of the indirect mapping, we should have a **master feature generation function** that:

1. **Takes a feature name directly** (e.g., `'points|season|avg|diff'`)
2. **Calculates that specific feature** based on its name components
3. **Returns the value**

This eliminates the mapping problem entirely. We iterate through feature names and calculate each one directly.

### New Function Signature

```python
def calculate_feature(
    feature_name: str,
    home_team: str,
    away_team: str,
    season: str,
    year: int,
    month: int,
    day: int,
    stat_handler: StatHandlerV2,
    per_calculator: PERCalculator = None
) -> float:
    """
    Calculate a single feature value based on its name.
    
    Args:
        feature_name: Feature name in new format (e.g., 'points|season|avg|diff')
        home_team: Home team name
        away_team: Away team name
        season: NBA season string
        year, month, day: Game date
        stat_handler: StatHandlerV2 instance
        per_calculator: Optional PERCalculator instance
        
    Returns:
        Feature value (float)
    """
```

### Benefits

1. **Direct calculation**: No mapping, no index tracking, no order dependencies
2. **Clear and testable**: Each feature is calculated independently
3. **Easy to debug**: If a feature is zero, we can trace exactly why
4. **Flexible**: Easy to add new features or modify calculations
5. **No include_absolute needed**: The feature name itself specifies if we want home/away/diff

## Calculation Rules

### Basic Stats (Single Statistic)

Basic stats are simple counts or totals (solo/aggregated stats):
- `points`, `wins`, `reb_total`, `blocks`, `turnovers`, `three_made`

#### `calc="avg"` (Per-Game Average)
**Formula**: Sum of stat over time period / Number of games in time period

**Example**: `points|season|avg|diff`
1. Get all games for home team in season up to game date
2. Sum all points scored by home team
3. Divide by number of games → `home_ppg`
4. Repeat for away team → `away_ppg`
5. Return `home_ppg - away_ppg`

#### `calc="raw"` (Total Amount)
**Formula**: Sum of stat over time period (NOT divided by games)

**Example**: `points|season|raw|diff`
1. Get all games for home team in season up to game date
2. Sum all points scored by home team → `home_total_points`
3. Repeat for away team → `away_total_points`
4. Return `home_total_points - away_total_points`

### Rate Stats (Multiple Statistics Required)

Rate stats that require multiple inputs and special calculation logic:
- `effective_fg_perc` (efg): `(FGM + 0.5 * 3PM) / FGA`
- `true_shooting_perc` (ts): `PTS / (2 * (FGA + 0.44 * FTA))`
- `three_perc`: `three_made / three_att`
- `off_rtg`: Points per 100 possessions (requires aggregation)
- `def_rtg`: Points allowed per 100 possessions (requires aggregation)
- `assists_ratio`: `100 * (assists / (((total_min / 5) * FG_made) - FG_made))`
  - Note: `total_min` = 48 min per game unless "OT" is true in stats_nba document, then 53 min
- `to_metric` (turnover metric): `100 * TO / (FG_att + 0.44*FT_att + TO)`
- `ast_to_ratio` (assist to turnover ratio): `assists/TO`

**Important**: For all rate stats:
- `calc="raw"`: Aggregate all component stats across all games in time period, then calculate rate stat once from totals
- `calc="avg"`: Calculate rate stat for each game individually, then average those per-game values

#### `calc="avg"` (Per-Game Then Average)
**Formula**: Calculate rate stat for each game individually, then average those per-game values

**Example**: `efg|season|avg|diff`
1. Get all games for home team in season up to game date
2. For each game, calculate `efg = (FGM + 0.5 * 3PM) / FGA` for that game
3. Average all per-game efg values → `home_avg_efg`
4. Repeat for away team → `away_avg_efg`
5. Return `home_avg_efg - away_avg_efg`

#### `calc="raw"` (Aggregate Then Calculate)
**Formula**: Sum all component stats across all games, then calculate rate stat once from totals

**Example**: `efg|season|raw|diff`
1. Get all games for home team in season up to game date
2. Sum all FGM across all games → `total_fgm`
3. Sum all 3PM across all games → `total_3pm`
4. Sum all FGA across all games → `total_fga`
5. Calculate once: `efg = (total_fgm + 0.5 * total_3pm) / total_fga` → `home_efg`
6. Repeat for away team → `away_efg`
7. Return `home_efg - away_efg`

**Note**: For rate stats, `raw` is generally more indicative/important than `avg` because it represents the true rate across the entire time period.

## Special Feature Types

### Side-Split Features (`|side` suffix)

When `|side` is present, only count games where the team played at that specific side:

**Example**: `points|season|avg|diff|side`
1. For home team: Only count games where home team was the HOME team
2. For away team: Only count games where away team was the AWAY team
3. Calculate averages separately
4. Return difference

**Stats that support side-split**: `points`, `wins`, `efg`, `ts`, `off_rtg`, `def_rtg`

### Absolute Features (`|home` or `|away`)

Absolute features return the team's value directly (not a differential):

**Example**: `points|season|avg|home`
1. Get all games for home team in season up to game date
2. Calculate home team's points per game
3. Return that value (not a diff)

**Note**: With the new naming convention, `include_absolute` is no longer needed. The feature name itself specifies if we want home/away/diff.

### Net Features (`_net` suffix in stat_name)

Net features represent: `(team_stat - team_allowed_stat)`

The calculation is the difference between the team's stat value and what the team's opponents have had against them in that stat.

**Example**: `points_net|season|raw|home`
1. Get team's total points this season
2. Get team's opponents' total points this season (what the team has allowed)
3. Return `team_points - opponents_points_allowed`

**Example**: `points_net|season|avg|home`
1. For each game:
   - Get team's points for that game
   - Get opponent's points for that game (what team allowed)
   - Calculate difference: `game_points - game_opponent_points`
2. Average all per-game differences

**Example**: `efg_net|season|raw|home`
1. Calculate team's effective FG% across all games this season (aggregate first, then calculate)
2. Calculate team's opponents' effective FG% across all games this season (what team has allowed)
3. Return `team_efg - opponents_efg_allowed`

**Stats with `_net` variants**: `efg`, `ts`, `three_pct`, `off_rtg`, `assists_ratio`, `points`

## Time Periods

### `season`
All games in the current season up to (but not including) the game date.

### `months_N`
All games in the last N **calendar months** before the game date.

**Example**: If game is on Jan 15 and N=1, includes all games from Dec 15 to Jan 15.

### `games_N`
The last N games played by the team before the game date, chronologically (most recent N games).

### `days_N`
All games played in the last N **calendar days** before the game date.

**Example**: If game is on Jan 15 and N=10, includes all games from Jan 5-15.

## Enhanced Features

Enhanced features should be converted to the new naming convention:
- `games_played|none|raw|diff` (games played so far)
- `pace|none|avg|diff` (possessions per game)
- `travel|days_N|avg|diff` (travel distance over last N days)
- `b2b|none|raw|diff` (back-to-back indicator: 1 if b2b, 0 otherwise)

These follow the same calc_weight rules as other stats.

## PER Features

PER features use special calc_weights:
- `player_team_per|season|avg|diff`: Average PER of all players on team (season-to-date aggregated)
- `player_team_per|season|weighted_MPG|diff`: PER weighted by minutes per game (season-to-date aggregated)
- `player_starters_per|season|avg|diff`: Average PER of starters (season-to-date aggregated)
- `player_per_1|season|top1_avg|diff`: Season PER of the highest PER player on team (season-to-date aggregated)
- `player_per_2|season|top1_avg|diff`: Season PER of 2nd highest player (season-to-date aggregated)
- `player_per_3|season|top1_avg|diff`: Season PER of 3rd highest player (season-to-date aggregated)
- `player_per_1|none|weighted_MIN_REC|diff`: Recency-weighted PER of top player (game-level PER with recency decay)
- `player_per_2|season|raw|diff`: Season PER of 2nd highest player (same as top1_avg, using "raw" calc_weight)

**Calc_weights**:
- `avg`: Simple average
- `weighted_MPG`: Weighted by minutes per game (MPG = total_min / games_5min)
- `weighted_MIN_REC`: Recency-weighted by minutes and recency decay
  - Formula: `w_g = MIN_g * exp(-days_since_game / k)` where k=15 days
  - `player_PER = Σ (PER_g * w_g) / Σ w_g`
  - PER is calculated at game level using that game's team context
- `raw`: Season-to-date aggregated PER (same as aggregated calculation)
- `top1_avg`: Season PER of highest PER player (by MPG)

**Recency-Weighted PER Calculation**:
- For each game a player played:
  - Compute PER using that game's box score and team stats (not season-aggregated)
  - Use that game's team context (team FG, assists, pace)
- Then aggregate across games:
  - Weight by minutes played in game (`MIN_g`)
  - Weight by recency decay (`exp(-days_since_game / k)` where k=15)
  - Normalize by total weight: `player_PER = Σ (PER_g * w_g) / Σ w_g`
- This captures recent form vs. long-term talent (season-aggregated PER)

## Injury Features

Injury features measure the impact of injured players on team performance:

**Per-team features**:
- `homeInjPerValue` / `awayInjPerValue`: Weighted average PER of injured players (weighted by MPG and recency)
- `homeInjTop1Per` / `awayInjTop1Per`: Highest PER among injured players
- `homeInjTop3PerSum` / `awayInjTop3PerSum`: Sum of top 3 injured players' PERs
- `homeInjMinLost` / `awayInjMinLost`: Sum of MPG lost from injured rotation players (MPG >= 10)
- `homeInjurySeverity` / `awayInjurySeverity`: `injMinLost / teamRotationMPG` (proportion of rotation minutes lost)
- `homeInjRotation` / `awayInjRotation`: Count of injured rotation players (MPG >= 10)

**Differential features**:
- `injPerValueDiff`: `homeInjPerValue - awayInjPerValue`
- `injTop1PerDiff`: `homeInjTop1Per - awayInjTop1Per`
- `injTop3PerSumDiff`: `homeInjTop3PerSum - awayInjTop3PerSum`
- `injMinLostDiff`: `homeInjMinLost - awayInjMinLost`
- `injurySeverityDiff`: `homeInjurySeverity - awayInjurySeverity`
- `injRotationDiff`: `homeInjRotation - awayInjRotation`

**Blend feature** (for master training):
- `inj_impact|blend|raw|diff`: Weighted combination of injury metrics
  - Formula: `0.45 * injurySeverityDiff + 0.35 * injTop1PerDiff + 0.20 * injRotationDiff`
  - Combines severity, top player impact, and rotation depth impact into a single metric

**Calc_weights**:
- `raw`: Direct value (for differentials and blend)
- `blend`: Weighted combination of multiple injury metrics

## Key Stats (Support Absolute Values)

"Key stats" that commonly have absolute home/away features:
- `points`
- `off_rtg`
- `def_rtg`
- `effective_fg_perc` (efg)
- `true_shooting_perc` (ts)
- `wins`

**Note**: With the new naming convention, any stat can have `|home` or `|away` features - it's not limited to "key stats". The `include_absolute` flag is no longer needed.

## Old Format Features to Remove

The following old-format features should be **completely removed from the codebase**:
- `homePpgRel`, `awayPpgRel`, `ppgRelDiff`
- `homeOffRtgRel`, `awayOffRtgRel`, `offRtgRelDiff`
- Any/all old-format features (anything not using the `|` delimiter)
