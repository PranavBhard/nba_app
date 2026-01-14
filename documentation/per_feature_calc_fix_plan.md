# PER Feature Calculation Fix Plan

## Goal
Ensure training and prediction use the **same player selection logic** for PER feature calculation, so that:
- Training uses only players who actually played in each historical game
- Prediction uses only players who are available/playing in the upcoming game (excluding injured players)
- Both use the same ID namespace and filtering logic

---

## Issues Identified

### Issue 1: Default Player Set Mismatch (HIGH PRIORITY)
**Problem:**
- **Training**: Always queries `stats_nba_players` for each game to get only players who played (`stats.min > 0` for that `game_id`)
- **Prediction**: When `player_filters` is `None` or empty `{}`, defaults to using **all players** who have played for the team before the game date

**Impact:** Training learns from games with specific lineups, but prediction may use entire roster, causing feature mismatch.

**Fix Required:** Make prediction require explicit `player_filters` or use a sensible default (e.g., last game's lineup).

---

### Issue 2: ID Namespace Consistency (MEDIUM PRIORITY)
**Current State:**
- Training builds `player_filters['playing']` from `stats_nba_players.player_id`
- `_get_team_players_before_date_cached()` returns players with `'_id': pid` where `pid = pg['player_id']`
- `compute_team_per_features()` matches using `p['_id']` against `player_filters['playing']`
- **Status:** IDs appear to match (both use `player_id` from `stats_nba_players`), but we should verify and add logging

**Fix Required:** Add explicit logging/validation to ensure ID matching works correctly.

---

### Issue 3: Injury Filtering Logic (MEDIUM PRIORITY)
**Current State:**
- Training: Implicitly excludes injured players (only queries players who logged minutes)
- Prediction: Filters by `players_nba.injured == True` AND uses UI `is_injured` flag
- **Potential Issue:** For future games, UI may have more up-to-date info than DB

**Fix Required:** 
- For **historical games**: Use `injured=True` from `players_nba` as source of truth
- For **future games**: UI `is_injured` flag should be able to override DB (UI can mark someone out even if DB says healthy)
- Effective rule: `effective_injured = db_injured OR ui_is_injured` (UI can exclude, but can't magically include DB-injured players unless DB is updated)

---

### Issue 4: Starter Identification (LOW PRIORITY)
**Current State:**
- Training: Uses `starter` flag from `stats_nba_players` for that specific game
- Prediction: Uses `player_filters['starters']` if provided, else uses historical pattern (`starter_games > games/2`)

**Impact:** Less critical than playing/not playing, but can cause noise in `startersPerAvg` features.

**Fix Required:** Ensure starter logic is consistent when `player_filters['starters']` is provided.

---

## Implementation Plan

### Phase 1: Fix Default Player Set Behavior (HIGH PRIORITY)

#### 1.1 Update `predict()` method in `NBAModel.py`
**Location:** `cli/NBAModel.py`, lines ~1765-1780

**Current Code:**
```python
if excluded_player_ids and self.per_calculator:
    home_players = self.per_calculator.get_team_players_before_date(...)
    home_playing = [p['_id'] for p in home_players if p['_id'] not in excluded_player_ids]
    player_filters = {
        home_team: {'playing': home_playing},
        away_team: {'playing': away_playing}
    }
```

**Problem:** 
- Only builds `player_filters` if `excluded_player_ids` is provided
- When `player_filters` is `None`, PER calculation defaults to using **all players who have ever played** (not players who played in a specific game)
- This does NOT match training, which uses only players who logged minutes in that specific game

**Fix:**
- **For historical games with `game_id`**: Build `player_filters` by querying `stats_nba_players` for that specific game (same logic as training)
- **For future games without `game_id`**: Either disable PER features OR require explicit `player_filters` parameter
- Do NOT use `get_team_players_before_date()` as a default - that gets "all players ever", not "players in this game"

**New Code:**
```python
# Build player_filters to match training behavior
player_filters = None
if self.include_per_features and self.per_calculator:
    # For historical games: use actual boxscore (same as training)
    # For future games: require explicit player_filters or skip PER features
    if game_id:  # Historical game - we can query the boxscore
        # Query stats_nba_players for this specific game (same as training)
        home_players_in_game = list(self.db.stats_nba_players.find(
            {'game_id': game_id, 'team': home_team, 'stats.min': {'$gt': 0}},
            {'player_id': 1, 'starter': 1}
        ))
        away_players_in_game = list(self.db.stats_nba_players.find(
            {'game_id': game_id, 'team': away_team, 'stats.min': {'$gt': 0}},
            {'player_id': 1, 'starter': 1}
        ))
        
        if home_players_in_game or away_players_in_game:
            home_playing = [p['player_id'] for p in home_players_in_game]
            away_playing = [p['player_id'] for p in away_players_in_game]
            home_starters = [p['player_id'] for p in home_players_in_game if p.get('starter', False)]
            away_starters = [p['player_id'] for p in away_players_in_game if p.get('starter', False)]
            
            # Filter out excluded players if provided
            if excluded_player_ids:
                home_playing = [pid for pid in home_playing if pid not in excluded_player_ids]
                away_playing = [pid for pid in away_playing if pid not in excluded_player_ids]
                home_starters = [pid for pid in home_starters if pid not in excluded_player_ids]
                away_starters = [pid for pid in away_starters if pid not in excluded_player_ids]
            
            player_filters = {
                home_team: {
                    'playing': home_playing,
                    'starters': home_starters
                },
                away_team: {
                    'playing': away_playing,
                    'starters': away_starters
                }
            }
        else:
            logger.warning(f"No boxscore data found for game_id={game_id}, skipping PER features")
    else:
        # Future game - no boxscore available
        # POLICY: Compute full-roster PER with loud warning (do NOT skip PER features)
        # Reason: If model was trained with PER features, skipping them breaks feature dimensionality
        # This fallback is NOT training-equivalent but maintains feature shape consistency
        home_players = self.per_calculator.get_team_players_before_date(home_team, season, game_date_str, min_games=1)
        away_players = self.per_calculator.get_team_players_before_date(away_team, season, game_date_str, min_games=1)
        
        # Filter out excluded players if provided
        if excluded_player_ids:
            home_playing = [p['_id'] for p in home_players if p['_id'] not in excluded_player_ids]
            away_playing = [p['_id'] for p in away_players if p['_id'] not in excluded_player_ids]
        else:
            # No exclusions - use all players who have played
            home_playing = [p['_id'] for p in home_players]
            away_playing = [p['_id'] for p in away_players]
        
        player_filters = {
            home_team: {'playing': home_playing},
            away_team: {'playing': away_playing}
        }
        
        logger.warning(
            f"[PER] Future game detected (no game_id) for {home_team} vs {away_team} on {game_date_str}. "
            f"Using full-roster PER (all players who have played before this date). "
            f"This is NOT training-equivalent (training uses only players in specific game). "
            f"Expect weaker player-level effects. "
            f"For realistic predictions, use predict_with_player_config() with explicit player_filters."
        )
```

#### 1.2 Update `predict_with_player_config()` to require `player_filters`
**Location:** `cli/NBAModel.py`, lines ~2043-2147

**Current Code:**
- Accepts `player_filters: Dict` but doesn't validate it

**Fix:**
- Make `player_filters` strictly required (remove `Optional`)
- Raise a clear error if `player_filters` is `None` or empty
- Document that `player_filters` must be provided for realistic roster-sensitive predictions

**New Code:**
```python
def predict_with_player_config(
    self,
    home_team: str,
    away_team: str,
    season: str,
    game_date: str,
    player_filters: Dict,  # REQUIRED - no Optional
    use_calibrated: bool = False
) -> dict:
    """
    Make a prediction for a single game with player availability configuration.
    
    Args:
        ...
        player_filters: Dict with team names as keys (REQUIRED):
            {team: {'playing': [player_ids], 'starters': [player_ids]}}
            Must be provided to ensure consistency with training.
            For future games, this should reflect the expected lineup.
            For historical games, this should match the actual boxscore.
    """
    # Strict validation: player_filters is required
    if not player_filters:
        raise ValueError(
            "player_filters is required for prediction with PER features. "
            "Provide explicit player availability to match training behavior. "
            "For future games, specify expected lineup. For historical games, use actual boxscore."
        )
    
    # Validate that both teams have filters
    if home_team not in player_filters or away_team not in player_filters:
        missing = [t for t in [home_team, away_team] if t not in player_filters]
        raise ValueError(f"player_filters missing for team(s): {missing}")
    
    # Rest of the method...
```

#### 1.3 Update `_build_features_dict()` to handle missing `player_filters`
**Location:** `cli/NBAModel.py`, lines ~1898-2041

**Current Code:**
- Accepts `player_filters: Dict = None` and passes it directly to `_get_per_features()`

**Fix:**
- If `player_filters` is `None`:
  - **Do NOT skip PER features** (would break feature dimensionality if model was trained with PER)
  - Instead: `compute_team_per_features()` will use all players (no filter applied)
  - This is handled in `compute_team_per_features()` - it will log that no filter was provided
- The key fix is ensuring `predict()` builds `player_filters` from boxscore when `game_id` is available
- For future games without `game_id`, `predict()` will build full-roster filters with warning (see 1.1)

---

### Phase 2: Add Logging and Validation (MEDIUM PRIORITY)

#### 2.1 Add logging to `compute_team_per_features()`
**Location:** `cli/per_calculator.py`, lines ~529-694

**Add logging for:**
- Number of players before filtering
- Number of injured players filtered out
- Number of players after applying `player_filters['playing']`
- Final player IDs used in PER calculation
- Resulting PER features

**New Code:**
```python
def compute_team_per_features(...):
    # ... existing code ...
    
    # Log initial player count
    logger.debug(f"PER calculation for {team} before {before_date}: {len(players)} players found")
    
    # Filter out injured players
    # ... existing code ...
    
    if injured_players:
        logger.debug(f"Filtered out {len(injured_players)} injured players: {injured_players}")
        players = [p for p in players if p['_id'] not in injured_players]
    
    # Apply player filters
    if player_filters:
        playing_list = player_filters.get('playing', [])
        if playing_list:
            playing_set = set(playing_list)
            before_filter_count = len(players)
            players = [p for p in players if p['_id'] in playing_set]
            logger.debug(f"Applied player_filters: {before_filter_count} -> {len(players)} players")
            
            # Warn if no players matched
            if len(players) == 0 and len(playing_list) > 0:
                logger.warning(f"No players matched player_filters['playing'] for {team}. Filter IDs: {playing_list[:5]}...")
        else:
            logger.debug(f"No 'playing' filter provided for {team}, using all {len(players)} players")
    else:
        logger.debug(f"No player_filters provided for {team}, using all {len(players)} players")
    
    # Log final player set
    final_player_ids = [p['_id'] for p in players[:top_n]]
    logger.debug(f"Final player set for PER calculation ({team}): {len(final_player_ids)} players: {final_player_ids[:5]}...")
    
    # ... rest of PER calculation ...
```

#### 2.2 Add hard ID mismatch check in `compute_team_per_features()`
**Location:** `cli/per_calculator.py`, lines ~583-591

**Add explicit sanity check right before filtering:**
```python
# Apply player filters if provided
if player_filters:
    playing_list = player_filters.get('playing', [])
    
    if playing_list:
        # HARD CHECK: Validate ID matching before filtering
        filter_ids = set(playing_list)
        available_ids = {p['_id'] for p in players}
        unmatched = filter_ids - available_ids
        
        if unmatched:
            logger.warning(
                f"[PER] Some player_filters IDs not found for team {team}: "
                f"{list(unmatched)[:5]} (showing up to 5). "
                f"This may indicate an ID namespace mismatch (_id vs player_id) or stale filter data."
            )
        
        playing_set = set(playing_list)
        before_filter_count = len(players)
        players = [p for p in players if p['_id'] in playing_set]
        logger.debug(f"Applied player_filters: {before_filter_count} -> {len(players)} players")
        
        # Warn if no players matched
        if len(players) == 0 and len(playing_list) > 0:
            logger.warning(
                f"No players matched player_filters['playing'] for {team}. "
                f"Filter had {len(playing_list)} IDs but none matched available players. "
                f"Check ID namespace consistency."
            )
```

**Note:** This check is added directly in `compute_team_per_features()` rather than as a separate helper, so it runs immediately before filtering and catches issues early.

---

### Phase 3: Ensure Consistent Injury Filtering (MEDIUM PRIORITY)

#### 3.1 Verify injury filtering uses `injured=True` consistently
**Location:** `cli/per_calculator.py`, lines ~556-574

**Current Code:**
- Filters by `players_nba.injured == True`
- This is correct per user's request

**Action:**
- Verify this is the only place injury filtering happens
- Ensure training path doesn't have additional injury filtering that prediction doesn't have
- Add logging to show which players are filtered due to injury

**Note:** Training implicitly excludes injured players by only querying players who logged minutes. This is fine, but we should ensure prediction also excludes them explicitly.

---

### Phase 4: Fix Starter Identification (LOW PRIORITY)

#### 4.1 Ensure starter logic is consistent
**Location:** `cli/per_calculator.py`, lines ~635-670

**Current Code:**
- Uses `player_filters['starters']` if provided
- Falls back to historical pattern if not provided

**Fix:**
- When `player_filters['starters']` is provided, use it (this is correct)
- When not provided, log a warning that starter identification may differ from training
- Consider: Should we require `starters` in `player_filters` for consistency?

---

## Testing Plan

### Test 1: Verify Same Players = Same PER Features
1. Pick a historical game (e.g., `game_id = "401585123"`, date `"2024-12-02"`)
2. Query `stats_nba_players` to get actual players who played in that game
3. Run training path PER calculation for that game
4. Run prediction path PER calculation for the same date/teams with `player_filters` built from the same players
5. **Expected:** PER features should match (within floating-point error)

### Test 1b: Compare Default vs Explicit Filters (NEW)
1. For the same historical game from Test 1:
2. Run prediction path **with no `player_filters`** (current default behavior)
3. Run prediction path **with correct `player_filters`** built from boxscore
4. Compare PER features between the two
5. **Expected:** If they're identical or very close, that confirms the default is using "all players ever" and ignoring the actual lineup, which explains why PER features don't move the needle

### Test 2: Verify Injury Filtering Works
1. Mark a key player as injured (`injured=True` in `players_nba`)
2. Run prediction with `player_filters` that includes that player
3. **Expected:** Player should be excluded from PER calculation
4. Run prediction again with `player_filters` that excludes that player
5. **Expected:** PER features should differ

### Test 3: Verify Default Behavior
1. Run prediction for a **future game** (no `game_id`) without providing `player_filters`
2. **Expected:** Should either:
   - Skip PER features entirely (safest), OR
   - Log a clear warning that full-roster PER is being used (not training-equivalent)
3. Run prediction for a **historical game** (with `game_id`) without providing `player_filters`
4. **Expected:** Should build `player_filters` from boxscore (same as training) and PER features should match training

### Test 4: Verify ID Matching
1. Build `player_filters` with known player IDs
2. Add logging to see which players are matched
3. **Expected:** All filter IDs should match player `_id` values

### Test 5: Real-World Sanity Test - Star Player Removal (NEW)
1. Pick a future (or pretend-future) game
2. Build `player_filters` from the full expected lineup (all available players)
3. Run prediction → record `home_win_prob` and PER features (`homeTeamPerAvg`, `awayTeamPerAvg`)
4. Identify a star player from one team (high PER, high minutes)
5. Remove that star player from `player_filters['playing']` and `player_filters['starters']` for their team
6. Run prediction again → record new `home_win_prob` and PER features
7. **Expected:**
   - PER features for that team should drop (e.g., `homeTeamPerAvg` decreases if star was on home team)
   - Win probability should move by a few percentage points in the "right" direction (team without star is less likely to win)
   - If this doesn't happen, the issue is likely:
     - Low marginal value of PER features given team stats (model regularization/collinearity), OR
     - PER features are still being computed incorrectly (need to debug further)
   - But first, this test confirms the structural mismatch is fixed

---

## Implementation Order

1. **Phase 1.1** - Fix `predict()` method to always build `player_filters` (HIGH PRIORITY)
2. **Phase 1.2** - Update `predict_with_player_config()` to require `player_filters` (HIGH PRIORITY)
3. **Phase 2.1** - Add logging to `compute_team_per_features()` (MEDIUM PRIORITY)
4. **Phase 2.2** - Add ID validation helper (MEDIUM PRIORITY)
5. **Phase 3.1** - Verify injury filtering consistency (MEDIUM PRIORITY)
6. **Phase 4.1** - Fix starter identification (LOW PRIORITY)

---

## Success Criteria

1. ✅ Training and prediction use the same player selection logic when given the same `player_filters`
2. ✅ For historical games: `player_filters` built from boxscore (same as training)
3. ✅ For future games: Full-roster PER computed with loud warning (maintains feature dimensionality)
4. ✅ `predict_with_player_config()` requires explicit `player_filters` for realistic predictions
5. ✅ Logging shows which players are used in PER calculation for both training and prediction
6. ✅ Hard ID mismatch check catches any `_id` vs `player_id` issues
7. ✅ Injury filtering: UI can override DB for future games (`effective_injured = db_injured OR ui_is_injured`)
8. ✅ Test 1 passes: Same players = same PER features
9. ✅ Test 1b shows difference between default (all players) vs explicit filters (actual lineup)
10. ✅ Test 5 passes: Removing star player changes PER features and win probability in expected direction

---

## Notes

- **UI Integration:** This plan focuses on backend fixes. The UI should continue to send `player_filters` based on `is_injured` flags, and the backend will use those filters. For future games, UI is the source of truth for lineup.

- **Future Games Policy (LOCKED):**
  - **Policy:** Compute full-roster PER with loud warning (do NOT skip PER features)
  - **Rationale:** If model was trained with PER features, skipping them breaks feature dimensionality. Feature vector shape must stay constant.
  - **Implementation:** `predict()` builds `player_filters` from all players who have played (with warning). `predict_with_player_config()` requires explicit `player_filters` for realistic predictions.
  - **Alternative:** If you want to support models without PER, train separate model versions (one with PER requiring `player_filters`, one without PER for generic `predict()`).

- **Backward Compatibility:** 
  - For historical games: We can build `player_filters` from boxscore automatically (backward compatible)
  - For future games: `predict()` will use full-roster PER with warning (backward compatible but less accurate)
  - `predict_with_player_config()` now requires `player_filters` (breaking change, but necessary for correctness)

- **Performance:** Adding logging should not significantly impact performance. Consider using `logger.debug()` for verbose logging and `logger.warning()` for important issues.

- **Key Insight:** The bug is that `get_team_players_before_date()` returns "all players who have ever played" not "players who played in this game". Training uses boxscore queries, prediction should too (when `game_id` available).

- **Injury Filtering Implementation:**
  - Apply DB injury filter first (`players_nba.injured == True`)
  - Then apply UI overrides (any player in `player_filters` with `is_injured=True` should be removed from `playing`)
  - Log both counts: DB-filtered and UI-filtered
  - Effective rule: `effective_injured = db_injured OR ui_is_injured` (UI can exclude, but can't magically include DB-injured players)

- **Implementation Caveats:**
  - **Verify `game_id` availability:** During implementation, confirm that `game_id` is actually available in `predict()` contexts where you want historical behavior. Check:
    - Where `predict()` is called from (CLI, web app, etc.)
    - Whether `game_id` is passed or can be derived from the game data
    - If `game_id` is not available, the code will fall back to full-roster PER (with warning)
  - **Post-Implementation Testing:**
    - Run star-on/star-off scenarios: Pick a game, run prediction with full lineup, then remove a star player and verify PER features drop and win probability moves in expected direction
    - Re-run ablation tests: Compare model performance with `player_talent` feature set enabled vs disabled
    - Expected outcome: After this fix, `player_talent` features should show actual CV gains (or at least not hurt performance) and predictions should be sensitive to lineup changes

- **Implementation Caveats:**
  - **Verify `game_id` availability:** During implementation, confirm that `game_id` is actually available in `predict()` contexts where you want historical behavior. Check:
    - Where `predict()` is called from (CLI, web app, etc.)
    - Whether `game_id` is passed or can be derived from the game data
    - If `game_id` is not available, the code will fall back to full-roster PER (with warning)
  - **Post-Implementation Testing:**
    - Run star-on/star-off scenarios: Pick a game, run prediction with full lineup, then remove a star player and verify PER features drop and win probability moves in expected direction
    - Re-run ablation tests: Compare model performance with `player_talent` feature set enabled vs disabled
    - Expected outcome: After this fix, `player_talent` features should show actual CV gains (or at least not hurt performance) and predictions should be sensitive to lineup changes

---

