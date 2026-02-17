# PER Feature Logic Verification

This document explains how the three PER differential features are calculated and how player aggregation works during training vs prediction.

## 1. perAvgDiff

### How to Calculate PER

PER calculation follows Hollinger's formula in three steps:

1. **uPER (unadjusted PER)** - Raw per-minute efficiency:
   - Calculated from aggregated player stats (points, rebounds, assists, steals, blocks, turnovers, etc.)
   - Formula: `uper = (positive_contributions - negative_contributions) / minutes`
   - Positive contributions: 3-pointers, assists, field goals, free throws, rebounds, steals, blocks
   - Negative contributions: turnovers, missed shots, missed free throws, personal fouls
   - Uses team assist ratio and league constants (VOP, DRB_pct, factor)

2. **aPER (pace-adjusted PER)** - Adjusted for team pace:
   - Formula: `aper = uper * (lg_pace / team_pace)`
   - Normalizes for pace differences between teams

3. **PER (normalized)** - Normalized to league average = 15.0:
   - Formula: `PER = aPER * (15 / lg_aPER)`
   - `lg_aPER` is the league average aPER (minutes-weighted) for the season
   - Normalizes so that league average PER is always 15.0
   - If `lg_aPER` is not available, falls back to using aPER directly

**Code location**: `cli/per_calculator.py`
- `compute_uper()` - lines 198-283
- `compute_aper()` - lines 285-289
- `compute_per()` - lines 291-307 (normalizes aPER to PER)
- `compute_league_average_aper()` - lines 309-458 (computes lg_aPER for normalization)
- Uses aggregated stats from all games before the target game date

### How Training Aggregates Players

**Location**: `cli/NBAModel.py` - `create_training_data()` method (lines ~625-675)

1. **Player Selection**:
   - **Queries `stats_nba_players` collection by `game_id` and `team`** to get distinct player_ids who actually played in this specific game
   - Filters to players with `stats.min > 0` (only players who played)
   - Gets starter information from the `starter` field in `stats_nba_players`
   - Builds `player_filters` with:
     - `playing`: List of player_ids who played in the game
     - `starters`: List of player_ids who were starters in the game
   - If `game_id` is missing, PER calculation will use default behavior (fallback)

2. **Player Aggregation**:
   - **Uses only the players who actually played in the game** (from step 1)
   - Aggregates stats across all games **before the target game date** for these specific players:
     - Sums: total_min, total_pts, total_fg_made, total_fg_att, total_three_made, total_ft_made, total_ft_att, total_reb, total_oreb, total_ast, total_stl, total_blk, total_to, total_pf
     - Counts: games played, starter_games (games where player was starter)

3. **PER Calculation**:
   - Computes uPER and aPER (then normalized PER) for each player using aggregated stats
   - Sorts players by total_minutes (descending)
   - Takes top 8 players by minutes

4. **Feature Calculation**:
   - `per_avg = mean([PER for top 8 players])` (normalized PER, league avg = 15.0)
   - Calculated separately for home and away teams
   - `perAvgDiff = homeTeamPerAvg - awayTeamPerAvg`
   - Individual PER slots: `homePer1`, `homePer2`, `homePer3`, `awayPer1`, `awayPer2`, `awayPer3`, `per1Diff`, `per2Diff`, `per3Diff` (only per1-per3, not per4-per8)

**Key points**:
- Training uses **only players who actually played in the specific game** (queried from `stats_nba_players` by `game_id`)
- Training does **NOT** use `players_nba` collection for injured/starter status decisions
- Starter identification uses historical heuristic from `stats_nba_players` (starter_games > games / 2)
- No injured player filtering from `players_nba` (training uses actual game data only)
- Note: `players_nba` can still be used for other purposes (e.g., filtering players with 0 min) if needed

### How Prediction Aggregates Players

**Location**: `cli/NBAModel.py` - `predict()` method (lines ~1808-1899)

1. **Player Selection** (in priority order):
   - **First**: Queries `stats_nba` collection for the game and extracts `homeTeam.players` and `awayTeam.players` (each is a list of player_ids)
   - **If that doesn't exist**: Falls back to querying `stats_nba_players` collection by `game_id` and `team` (same as training)
   - **If `game_id` is missing**: Falls back to getting all players who played for the team before the game date
   - **Excludes injured players**: Filters out any players with `injured: true` from `players_nba` collection
   - Builds `player_filters` with:
     - `playing`: List of player_ids from the game data (excluding injured players)
     - `starters`: Not used - starter status comes from `players_nba.starter` (see below)

2. **Player Aggregation**:
   - **Uses only the players from the game** (from step 1)
   - Aggregates stats across all games **before the target game date** for these specific players:
     - Same aggregation process as training

3. **PER Calculation**:
   - Same process as training
   - Computes PER for top 8 players by minutes

4. **Feature Calculation**:
   - Same calculation: `perAvgDiff = homeTeamPerAvg - awayTeamPerAvg`

**Key differences from training**:
- Prediction first tries to get players from `stats_nba.homeTeam.players` / `awayTeam.players`, then falls back to `stats_nba_players` query, then falls back to all players before date
- **For prediction**: Excludes players with `injured: true` from `players_nba` collection
- **For prediction**: Uses `players_nba.starter` boolean as **authority** for starter status (not historical heuristic)
- Training always uses `stats_nba_players` query by `game_id` and does NOT use `players_nba` collection

---

## 2. perWeightedDiff

### How to Calculate PER

**Same as perAvgDiff** - uses the same PER calculation (uPER → aPER → PER normalized).

### How Training Aggregates Players

**Same player selection and aggregation as perAvgDiff** - uses players who actually played in the game (from `stats_nba_players` query by `game_id`).

**Feature Calculation**:
- `per_weighted = sum(PER * total_min for top 8 players) / sum(total_min for top 8 players)`
- This is a **minutes-weighted average** of PER
- Players who play more minutes have more influence on the weighted average
- `perWeightedDiff = homeTeamPerWeighted - awayTeamPerWeighted`

**Code location**: `cli/per_calculator.py` line 933

### How Prediction Aggregates Players

**Same player selection as perAvgDiff** - uses players from `stats_nba.players` (priority 1), `stats_nba_players` by `game_id` (priority 2), or all players before date (priority 3).

**Feature Calculation**:
- Same as training - uses the same minutes-weighted calculation

**Key point**: Both training and prediction use the same minutes-weighted calculation, giving more weight to players who play more minutes.

---

## 3. startersPerDiff

### How to Calculate PER

**Same as perAvgDiff** - uses the same PER calculation (uPER → aPER → PER normalized).

### How Training Aggregates Players

**Same player selection and aggregation as perAvgDiff** - uses players who actually played in the game (from `stats_nba_players` query by `game_id`).

**Starter Identification**:
- Uses historical heuristic from `stats_nba_players`: `is_starter = (starter_games > games / 2)`
  - If a player started in more than half their games, they're considered a starter
- **Does NOT** query `players_nba` collection (training mode only uses `stats_nba_players`)

**Feature Calculation**:
- Filters to players identified as starters (up to 5)
- `starters_avg = mean([PER for starter players])`
- If no starters found, falls back to `per_avg`
- `startersPerDiff = homeStartersPerAvg - awayStartersPerAvg`

**Code location**: `cli/per_calculator.py` lines 935-944

### How Prediction Aggregates Players

**Same player selection as perAvgDiff** - uses players from `stats_nba.players` (priority 1), `stats_nba_players` by `game_id` (priority 2), or all players before date (priority 3).

**Starter Identification**:
- **Uses `players_nba.starter` boolean as authority** (not historical heuristic)
- Queries `players_nba` collection for each player to get `starter` field
- If player not found in `players_nba`, falls back to historical heuristic

**Feature Calculation**:
- Same as training

**Key differences from training**:
- **Excludes injured players**: Players with `injured: true` in `players_nba` are excluded from PER calculations
- **Uses `players_nba.starter` as authority**: Starter status comes from `players_nba.starter` boolean, not from `stats_nba_players` or historical heuristic
- If player not found in `players_nba`, falls back to historical heuristic

**Note**: The web interface (`web/app.py`) allows users to mark players as starters/injured, which updates `players_nba` collection. These updates are used during prediction but not during training.

---

## Summary of Key Differences

| Aspect | Training | Prediction |
|--------|----------|------------|
| **Player Selection** | Queries `stats_nba_players` by `game_id` and `team` | 1) `stats_nba.homeTeam.players` / `awayTeam.players`<br>2) `stats_nba_players` by `game_id` (fallback)<br>3) All players before date (fallback) |
| **Injured Player Filtering** | None (uses actual game data only) | Excludes players with `injured: true` from `players_nba` |
| **Uses players_nba for injured/starter** | **NO** - only uses `stats_nba_players` | **YES** - for injured status and starter status |
| **Starter Identification** | Historical heuristic: `starter_games > games / 2` | **`players_nba.starter` boolean is authority** |
| **Aggregation Method** | Stats aggregated before game date for selected players | Same as training |
| **PER Calculation** | Same (uPER → aPER → PER normalized) | Same (uPER → aPER → PER normalized) |
| **PER Features** | per1, per2, per3 only (home, away, diff) | per1, per2, per3 only (home, away, diff) |

## Code Flow

1. **PER Calculation**: `PERCalculator.compute_team_per_features()`
   - Aggregates player stats before game date
   - Computes PER for each player
   - Calculates team aggregates (avg, weighted, starters)

2. **Feature Creation**: `PERCalculator.get_game_per_features()`
   - Calls `compute_team_per_features()` for home and away
   - Calculates differentials: `perAvgDiff`, `perWeightedDiff`, `startersPerDiff`

3. **Usage**:
   - **Training**: `NBAModel.create_training_data()` → Queries `stats_nba_players` by `game_id` → Builds `player_filters` → `_get_per_features()`
   - **Prediction**: `NBAModel.predict()` → Gets players from `stats_nba.players` or `stats_nba_players` → Builds `player_filters` → `_get_per_features()`

