# PER Feature Calculation Logic: Training vs Prediction

## Overview

The PER (Player Efficiency Rating) features are calculated differently during **training** vs **prediction**, which may explain why excluding them improves model accuracy. This document explains the logic for both phases and identifies potential inconsistencies.

---

## Key Differences: Training vs Prediction

### During Training (`create_training_data`)

1. **No Player Filters**: PER is calculated WITHOUT any player filters:
   ```python
   # Line 604 in NBAModel.py
   per_features = self._get_per_features(home_team, away_team, season, game_date)
   # player_filters=None (not passed)
   ```

2. **Historical Starter Determination**: 
   - Starters are determined historically: `starter_games > games / 2`
   - This uses aggregated data from `stats_nba_players` collection
   - A player is considered a starter if they started in more than 50% of their games **before** the game date

3. **No Injury Filtering**: 
   - All players who have played before the game date are included
   - Injuries are NOT filtered out during training

4. **Player Selection**:
   - Gets all players who played for the team before the game date
   - Filters to top 8 players by **total minutes played** (not PER)
   - Calculates PER for those top 8 players
   - Then sorts by PER to assign slots (per1, per2, ..., per5)

5. **Team Stats Aggregation**:
   - Aggregates team stats from ALL games before the game date
   - Includes incomplete games (games without scores) in the aggregation
   - Uses these for PER calculation constants

---

### During Prediction (`predict_with_player_config`)

1. **Player Filters May Be Applied**:
   ```python
   # Lines 1674-1688 in NBAModel.py
   player_filters = {
       home_team: {'playing': home_playing, 'starters': ...},
       away_team: {'playing': away_playing, 'starters': ...}
   }
   per_features = self._get_per_features(..., player_filters=player_filters)
   ```

2. **Injury Filtering**:
   - Players with `injury_status == 'Out'` are EXCLUDED (lines 556-574 in per_calculator.py)
   - This filtering happens BEFORE calculating PER
   - Only checks `players_nba` collection for current injury status

3. **Starter Determination**:
   - **If player_filters provided**: Uses explicit starter list from filters
   - **Otherwise**: Falls back to historical determination (`starter_games > games / 2`)
   - This can be DIFFERENT from training if filters are applied

4. **Player Selection**:
   - First filters out injured players
   - Then applies player filters (if any) to exclude non-playing players
   - Filters to top 8 by total minutes
   - Calculates PER, then sorts by PER for slots

5. **Team Stats Aggregation**:
   - Same as training: aggregates from games before the game date
   - Should be consistent, but may differ if games were added/updated

---

## Potential Issues Causing Accuracy Degradation

### Issue 1: Injury Filtering Inconsistency

**Problem**: During training, ALL players are included (even those who might have been injured). During prediction, injured players (`injury_status == 'Out'`) are excluded. This creates a mismatch:

- **Training**: PER calculated with injured players' historical stats included
- **Prediction**: PER calculated without injured players

**Impact**: If a star player gets injured, their PER is suddenly excluded during prediction, but was included during training. This creates a feature distribution shift.

**Example**:
- Team A's PER during training: 18.5 (includes injured star player's historical PER)
- Team A's PER during prediction: 16.2 (excludes injured star player)
- Model trained on 18.5, sees 16.2 → prediction error

---

### Issue 2: Starter Determination Inconsistency

**Problem**: Starter determination can differ between training and prediction:

- **Training**: Always uses historical (`starter_games > games / 2`)
- **Prediction**: May use explicit starter list from `player_filters`, or historical

**Impact**: The "starters PER average" feature may use different players:
- Training might consider Player X a starter based on historical data
- Prediction might exclude Player X if not in the explicit starter list

---

### Issue 3: Player Filtering Applied Inconsistently

**Problem**: During prediction, `player_filters` can exclude players who are not playing:
```python
if playing_list:
    playing_set = set(playing_list)
    players = [p for p in players if p['_id'] in playing_set]
```

But during training, NO such filtering occurs. This means:
- **Training**: Includes all players who have played before the game
- **Prediction**: May exclude specific players based on availability

**Impact**: If Player Y is included in training but excluded in prediction, the PER features will differ.

---

### Issue 4: Top N Selection by Minutes, Not PER

**Problem**: The code selects the top 8 players by **total minutes played**, then calculates PER:
```python
for player in players[:top_n]:  # top_n = 8, sorted by total_min
    # Calculate PER for these 8 players
```

Then PER slots are assigned by sorting the calculated PERs. This means:
- The players used for PER calculation are the minutes leaders, not the PER leaders
- A high-PER bench player might be excluded if they don't play enough minutes
- This selection happens BEFORE PER calculation, which seems backwards

**Impact**: The team PER average might not represent the actual best players (by PER), but rather the most-played players.

---

### Issue 5: Incomplete Games in Team Stats

**Problem**: Team stats are aggregated from games before the game date, but the code may include incomplete games:

Looking at `_get_team_stats_before_date_cached`, it aggregates from ALL games before the date, without checking if games are complete (have scores). However, `StatHandlerV2._is_game_complete()` filters incomplete games for other features.

**Impact**: Team totals (assists, FG_att, etc.) used for PER calculation might include incomplete games, leading to incorrect constants.

---

### Issue 6: Temporal Consistency of Team Stats

**Problem**: Team stats (`team_stats`) are aggregated across the entire season up to the game date. However, PER calculation uses these as if they represent the "team context" for that specific game. The team's style of play might have changed over the season, making early-season team stats less relevant for late-season games.

**Impact**: PER values may not accurately reflect player efficiency in the context of the team's current style of play.

---

## Code Flow Comparison

### Training Flow (simplified):
1. Load all games from database
2. For each game:
   - Get all players for home/away teams (before game date)
   - **No injury filtering**
   - **No player filters**
   - Select top 8 by minutes
   - Calculate PER for each player
   - Aggregate to team PER features
   - Add to feature vector

### Prediction Flow (simplified):
1. For a specific game:
   - Get all players for home/away teams (before game date)
   - **Filter out injured players** (`injury_status == 'Out'`)
   - **Apply player filters** (if provided) to exclude non-playing players
   - Select top 8 by minutes
   - Calculate PER for each player
   - **Determine starters** (may use explicit list vs historical)
   - Aggregate to team PER features
   - Add to feature vector

---

## Recommendations to Fix

1. **Consistent Injury Filtering**: Either:
   - Filter injuries during training (exclude players marked "Out" at game time)
   - OR: Don't filter injuries during prediction (use historical stats regardless)

2. **Consistent Starter Determination**: Always use the same method:
   - Use historical (`starter_games > games / 2`) for both training and prediction
   - OR: Store actual starters for each game and use those during training

3. **Player Filtering**: If player filters are used during prediction, they should also be simulated during training:
   - During training, check if players were actually available for each game
   - Store player availability in the training data

4. **Top N Selection**: Consider selecting by PER, not minutes:
   - Calculate PER for all players first
   - Then select top 8 by PER (not minutes)
   - This would better represent "talent level"

5. **Team Stats**: Filter incomplete games from team stats aggregation, consistent with other features

6. **Temporal Weighting**: Consider weighting team stats by recency (more recent games count more), similar to exponential weighting in other features

---

## Why Excluding PER Features Improves Accuracy

The most likely reasons:

1. **Distribution Shift**: Training and prediction use different player sets (injuries, filters), causing PER values to have different distributions
2. **Information Leakage**: PER might be indirectly capturing information about game outcomes that shouldn't be available (e.g., player performance in the actual game)
3. **Noise**: PER calculation is complex and may introduce noise that hurts rather than helps
4. **Redundancy**: Team-level stats (points, offensive rating, etc.) may already capture the same information that PER is trying to add

By excluding PER features, the model relies solely on team-level aggregated stats, which are more consistent between training and prediction.

