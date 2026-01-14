# PER Feature Calculation: Training vs Prediction

This document analyzes the logic for calculating PER (Player Efficiency Rating) features during training versus prediction, and identifies potential discrepancies.

## 1. Per Player Training Feature Generation Logic/Calcs

### Location
- `cli/NBAModel.py`: `create_training_data()` (lines 612-649)
- `cli/NBAModel.py`: `create_training_data_model_specific()` (lines 816-849)

### Process

1. **For each historical game in training data:**
   - Extract `game_id` from the game document
   - Query `stats_nba_players` collection to get players who **actually played** in that specific game:
     ```python
     home_players_in_game = list(self.db.stats_nba_players.find(
         {'game_id': game_id, 'team': home_team, 'stats.min': {'$gt': 0}},
         {'player_id': 1, 'starter': 1}
     ))
     ```
   - Build `player_filters` dictionary:
     ```python
     player_filters = {
         home_team: {
             'playing': [player_ids who played in this specific game],
             'starters': [player_ids who were starters in this specific game]
         },
         away_team: {
             'playing': [player_ids who played in this specific game],
             'starters': [player_ids who were starters in this specific game]
         }
     }
     ```

2. **PER Calculation (`per_calculator.compute_team_per_features`):**
   - Gets all players who have played for the team **before the game date** using `_get_team_players_before_date_cached()`
   - This returns aggregated season stats for each player (total points, rebounds, assists, etc. from all games before the game date)
   - Filters out injured players by checking `players_nba` metadata where `injured == True`
   - **Applies `player_filters['playing']`** to restrict to only players who are in the `playing` list (i.e., players who actually played in that specific game)
   - Computes PER using **season-long aggregated stats** (from all games before the game date) for the filtered players
   - Returns PER features: `per_avg`, `per_weighted`, `starters_avg`, `per1`-`per8`

### Key Points
- **Player Selection**: Only includes players who actually played in that specific historical game (`stats.min > 0` for that `game_id`)
- **PER Calculation**: Uses season-long aggregated stats (all games before the game date) for those specific players
- **Injury Filtering**: Excludes players where `injured == True` in `players_nba` metadata
- **Starter Identification**: Uses `starter` field from `stats_nba_players` for that specific game

---

## 2. Per Player Prediction Feature Generation Logic/Calcs

### Location
- `cli/NBAModel.py`: `_build_features_dict()` (lines 2002-2005)
- `cli/NBAModel.py`: `predict_with_player_config()` (lines 2043-2147)
- `web/app.py`: `/api/predict` endpoint (lines 1297-1329)

### Process

1. **Player Filters Construction:**
   - If `player_filters` is provided from the frontend (via `/api/predict`):
     - Frontend sends `player_config` with `{team: {player_id: {is_playing, is_starter, is_injured}}}`
     - Backend builds `player_filters`:
       ```python
       player_filters = {
           home_team: {
               'playing': [player_ids where is_playing=True and is_injured=False],
               'starters': [player_ids where is_starter=True]
           },
           away_team: {
               'playing': [player_ids where is_playing=True and is_injured=False],
               'starters': [player_ids where is_starter=True]
           }
       }
       ```
   - If `player_filters` is **NOT provided** (empty dict `{}`):
     - In `predict()` method (line 1770), it gets all players who have played for the team before the game date:
       ```python
       home_players = self.per_calculator.get_team_players_before_date(...)
       home_playing = [p['_id'] for p in home_players if p['_id'] not in excluded_player_ids]
       ```
     - This includes **all players** who have played for the team (not just those playing in a specific game)

2. **PER Calculation (`per_calculator.compute_team_per_features`):**
   - Gets all players who have played for the team **before the game date** using `_get_team_players_before_date_cached()`
   - This returns aggregated season stats for each player (total points, rebounds, assists, etc. from all games before the game date)
   - Filters out injured players by checking `players_nba` metadata where `injured == True`
   - **If `player_filters['playing']` is provided**: Restricts to only players in that list
   - **If `player_filters['playing']` is NOT provided or is empty**: Uses **all players** who have played for the team (not just those playing in the upcoming game)
   - Computes PER using **season-long aggregated stats** (from all games before the game date) for the filtered players
   - Returns PER features: `per_avg`, `per_weighted`, `starters_avg`, `per1`-`per8`

### Key Points
- **Player Selection (when `player_filters` provided)**: Uses players specified in `player_filters['playing']` (from frontend UI)
- **Player Selection (when `player_filters` NOT provided)**: Uses **all players** who have played for the team before the game date (not restricted to a specific game)
- **PER Calculation**: Uses season-long aggregated stats (all games before the game date) for the filtered players
- **Injury Filtering**: Excludes players where `injured == True` in `players_nba` metadata
- **Starter Identification**: Uses `player_filters['starters']` if provided, otherwise uses historical starter status (`starter_games > games / 2`)

---

## 3. Comparison and List of Possible Discrepancies

### Discrepancy #1: Player Selection Scope
**Training:**
- Uses only players who **actually played in that specific historical game** (from `stats_nba_players` for that `game_id`)

**Prediction (when `player_filters` not provided):**
- Uses **all players** who have played for the team before the game date (not restricted to a specific game)

**Impact:**
- If a key player was injured/rested in a historical game, training excludes them from PER calculation for that game
- If a key player is injured/rested in an upcoming game but `player_filters` is not provided, prediction **includes** them in PER calculation
- This creates a mismatch: training learns from games where injured players were excluded, but prediction may include them

**Severity:** HIGH - This is likely the main issue causing predictions to not change when marking players as injured

### Discrepancy #2: Default Behavior When No Player Filters Provided
**Training:**
- Always queries `stats_nba_players` for each game to get actual players who played
- `player_filters` is always populated (even if empty lists) based on actual game data

**Prediction:**
- If `player_filters` is not provided or is empty `{}`, the `predict()` method (line 1770) builds it from `get_team_players_before_date()`, which includes **all players** who have played for the team
- This means prediction defaults to including all players, while training defaults to only players who played in that specific game

**Impact:**
- Default prediction behavior includes more players than training, leading to different PER calculations

**Severity:** HIGH - This explains why predictions don't change when players are marked as injured (if the frontend doesn't properly send `player_filters`)

### Discrepancy #3: Injury Status Check Timing
**Training:**
- Injury filtering happens in `compute_team_per_features()` by checking `players_nba` metadata at the time of PER calculation
- The `player_filters['playing']` list is built from `stats_nba_players` (who actually played), so injured players are already excluded by definition

**Prediction:**
- Injury filtering happens in two places:
  1. Frontend sends `is_injured` flag, and backend excludes those players from `player_filters['playing']`
  2. `compute_team_per_features()` also filters out players where `injured == True` in `players_nba` metadata

**Impact:**
- If the frontend doesn't properly mark players as injured, or if `players_nba` metadata is not up-to-date, injured players may still be included in prediction

**Severity:** MEDIUM - Double-checking is good, but inconsistency in data sources could cause issues

### Discrepancy #4: Starter Identification
**Training:**
- Uses `starter` field from `stats_nba_players` for that specific game
- `player_filters['starters']` contains players who were starters in that specific game

**Prediction:**
- Uses `player_filters['starters']` if provided (from frontend UI)
- If not provided, uses historical starter status (`starter_games > games / 2`)

**Impact:**
- If a player was a starter in a historical game but is not a starter in the upcoming game, training and prediction may use different starter lists
- This affects `startersPerAvg` and `startersPerDiff` features

**Severity:** MEDIUM - Starter status may change, but this is less critical than the playing/not playing distinction

### Discrepancy #5: PER Calculation Uses Season-Long Stats (Both Training and Prediction)
**Both Training and Prediction:**
- PER is calculated using **season-long aggregated stats** (all games before the game date)
- This means PER reflects a player's performance across the entire season, not just their performance in that specific game

**Impact:**
- If a player had a great season but was injured/rested in a specific game, training excludes them (correct)
- If a player had a great season but is injured/rested in an upcoming game, prediction may still include them if `player_filters` is not properly set (incorrect)
- The PER calculation itself is consistent (uses season-long stats), but the player selection is inconsistent

**Severity:** LOW - The PER calculation method is correct, but the player selection inconsistency is the real issue

---

## Summary of Root Causes

1. **Primary Issue**: Training uses only players who played in that specific game, while prediction (when `player_filters` is not provided) uses all players who have played for the team. This creates a fundamental mismatch.

2. **Secondary Issue**: The frontend may not be properly sending `player_filters` when players are marked as injured, or the backend may not be properly handling empty `player_filters`.

3. **Tertiary Issue**: Even when `player_filters` is provided, if it's not properly constructed (e.g., includes injured players), the PER calculation will still include them.

## Recommendations

1. **Ensure `player_filters` is always provided during prediction**: The frontend should always send `player_filters` based on the current player availability, even if all players are available.

2. **Default behavior should match training**: If `player_filters` is not provided, prediction should default to an empty list (no players) rather than all players, forcing the frontend to explicitly specify available players.

3. **Verify frontend sends `player_filters` correctly**: Check that when players are marked as injured in the UI, the `player_config` properly excludes them from the `playing` list.

4. **Add logging**: Log the `player_filters` being used during prediction to verify it matches the expected players (injured players excluded, only available players included).

