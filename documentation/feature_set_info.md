# NBA Model Feature Set Documentation

This document describes how raw database data is transformed into training features for the NBA prediction model. The transformation pipeline is implemented in `cli/NBAModel.py` and `cli/StatHandlerV2.py`.

## Data Transformation Pipeline

### Overview
The training data creation process (`NBAModel.create_training_data()`) transforms raw MongoDB game documents into feature vectors through the following steps:

1. **Query Database**: Fetches games from `stats_nba` collection using a default query (excludes preseason/all-star, filters seasons)
2. **Compute Elo Ratings**: If enabled, calculates Elo ratings chronologically for all teams
3. **For Each Game**:
   - Extract game metadata (date, teams, season)
   - Compute base stat differentials using `StatHandlerV2.getStatAvgDiffs()`
   - Add Elo differential (if enabled)
   - Add rest differential (days since last game)
   - Add enhanced features (pace, volatility, schedule context)
   - Add era-normalized features (if enabled)
   - Add PER-based features (if enabled)
4. **Output**: Write feature vectors to CSV with metadata columns (Year, Month, Day, Home, Away) and target (HomeWon)

### Feature Computation Details

**Base Features**: Computed via `StatHandlerV2.getStatAvgDiffs()` which:
- Parses stat tokens (e.g., `pointsSznAvg`, `winsMonths_1`, `pointsGames_10_side`)
- Retrieves relevant game windows (season-to-date, last N months/days/games)
- Aggregates box score stats (points, rebounds, assists, etc.)
- Computes advanced stats (offensive/defensive ratings, eFG%, pace, etc.)
- Applies exponential weighting (if enabled) to give more weight to recent games
- Computes differentials: `(home_stat - home_opponent_stat) - (away_stat - away_opponent_stat)`

**Enhanced Features**: Computed via `StatHandlerV2.get_enhanced_features()` which:
- Uses last 10 games for pace and volatility calculations
- Computes schedule context from game history
- Calculates offense/defense splits from aggregated stats

**PER Features**: Computed via `PERCalculator.get_game_per_features()` which:
- Loads player stats from `stats_nba_players` collection
- Calculates Player Efficiency Rating (PER) for each player using Hollinger's formula
- Aggregates to team-level metrics (averages, weighted by minutes, starters-only)

---

## 1. Feature Groups

### Base Features
**Source**: `get_default_classifier_features()` in `NBAModel.py`

**Features**:
- `pointsSznAvgDiff`, `pointsSznAvg_sideDiff`, `pointsMonths_1Diff`, `pointsMonths_1_sideDiff`, `pointsGames_10Diff`, `pointsGames_10_sideDiff`
- `winsSznAvgDiff`, `winsSznAvg_sideDiff`, `winsMonths_1Diff`, `winsMonths_1_sideDiff`, `winsGames_10Diff`, `winsGames_10_sideDiff`
- `effective_fg_percSznAvgDiff`, `effective_fg_percSznAvg_sideDiff`, `effective_fg_percMonths_1Diff`, `effective_fg_percGames_10Diff`
- `true_shooting_percSznAvgDiff`, `true_shooting_percSznAvg_sideDiff`, `true_shooting_percMonths_1Diff`, `true_shooting_percGames_10Diff`
- `off_rtgSznAvgDiff`, `off_rtgSznAvg_sideDiff`
- `def_rtgSznAvgDiff`, `def_rtgSznAvg_sideDiff`
- `assists_ratioSznAvgDiff`, `assists_ratioSznAvg_sideDiff`
- `TO_metricSznAvgDiff`
- `three_madeSznAvgDiff`, `three_madeSznAvg_sideDiff`
- `total_rebSznAvgDiff`, `total_rebSznAvg_sideDiff`
- `blocksSznAvgDiff`, `blocksSznAvg_sideDiff`
- `TOSznAvgDiff`
- `b2bDays_10Diff`

**Summary**:
- Core team performance metrics computed as differentials (home advantage - away advantage) across multiple time windows (season, last month, last 10 games)
- Includes both overall and side-specific (home/away) statistics to capture venue effects
- Uses exponential weighting (if enabled) to emphasize recent performance over historical averages

### Absolute Features
**Source**: Computed alongside base features when `include_absolute=True`

**Features** (for key stats only):
- `pointsSznAvg_home_abs`, `pointsSznAvg_away_abs`
- `pointsSznAvg_side_home_abs`, `pointsSznAvg_side_away_abs`
- `winsSznAvg_home_abs`, `winsSznAvg_away_abs`
- `winsSznAvg_side_home_abs`, `winsSznAvg_side_away_abs`
- `off_rtgSznAvg_home_abs`, `off_rtgSznAvg_away_abs`
- `def_rtgSznAvg_home_abs`, `def_rtgSznAvg_away_abs`
- `effective_fg_percSznAvg_home_abs`, `effective_fg_percSznAvg_away_abs`
- `true_shooting_percSznAvg_home_abs`, `true_shooting_percSznAvg_away_abs`

**Summary**:
- Absolute values for key statistics (points, wins, ratings, shooting efficiency) included alongside differentials
- Provides model with magnitude context, not just relative differences between teams
- Helps capture non-linear relationships where absolute performance levels matter

### Elo Features
**Source**: `NBAModel._compute_elo_ratings()` and `_get_elo_for_game()`

**Features**:
- `eloDiff` (home_elo - away_elo, with +100 home advantage)

**Summary**:
- Elo rating system tracks team strength over time, updating after each game result
- Uses K-factor of 20 and starting Elo of 1500, with 100-point home court advantage
- Captures team strength trends and momentum that may not be reflected in recent stat averages

### Rest Features
**Source**: `NBAModel._get_days_rest()`

**Features**:
- `restDiff` (home_days_rest - away_days_rest)

**Summary**:
- Measures fatigue/rest advantage by calculating days since each team's last game
- Positive values indicate home team is more rested, negative values indicate away team is more rested
- Defaults to 7 days if no prior game found (beginning of season)

### Enhanced Features
**Source**: `StatHandlerV2.get_enhanced_features()`

**Features**:
- `homeGamesPlayed`, `awayGamesPlayed`, `gamesPlayedDiff`
- `homePace`, `awayPace`, `paceDiff`
- `homePointsStd`, `awayPointsStd`, `pointsStdDiff`
- `homeGamesLast3Days`, `awayGamesLast3Days`, `gamesLast3DaysDiff`
- `homeGamesLast5Days`, `awayGamesLast5Days`, `gamesLast5DaysDiff`
- `homeB2B`, `awayB2B`, `b2bDiff`
- `homeOffRtg`, `awayOffRtg`, `offRtgDiff`
- `homeDefRtg`, `awayDefRtg`, `defRtgDiff`
- `homeEfgOff`, `awayEfgOff`, `efgOffDiff`
- `homeEfgDef`, `awayEfgDef`, `efgDefDiff`

**Summary**:
- **Games Played**: Reliability signal indicating how much data is available for each team (early season vs. mid/late season)
- **Pace**: Possessions per game calculated from last 10 games, captures tempo differences
- **Volatility**: Standard deviation of points scored over last 10 games, measures consistency
- **Schedule Context**: Games played in last 3/5 days and back-to-back indicators capture fatigue and schedule density
- **Offense/Defense Splits**: Absolute offensive/defensive ratings and eFG% for both teams, providing magnitude context alongside differentials

### Era Normalization Features
**Source**: `StatHandlerV2.get_era_normalized_features()` (optional, `include_era_normalization=True`)

**Features**:
- `homePpgRel`, `awayPpgRel`, `ppgRelDiff` (points per game relative to league average)
- `homeOffRtgRel`, `awayOffRtgRel`, `offRtgRelDiff` (offensive rating relative to league average)

**Summary**:
- Normalizes key metrics relative to league-wide averages for each season
- Accounts for era effects (e.g., higher scoring in modern NBA vs. 2000s)
- Helps model compare teams across different seasons by removing league-wide trends

### PER Features
**Source**: `PERCalculator.get_game_per_features()` (optional, `include_per_features=True`)

**Features**:
- `homeTeamPerAvg`, `awayTeamPerAvg`, `perAvgDiff`
- `homeTeamPerWeighted`, `awayTeamPerWeighted`, `perWeightedDiff`
- `homeStartersPerAvg`, `awayStartersPerAvg`, `startersPerDiff`
- `homePer1`, `homePer2`, `homePer3`, `homePer4`, `homePer5`
- `awayPer1`, `awayPer2`, `awayPer3`, `awayPer4`, `awayPer5`

**Summary**:
- **Team PER Averages**: Simple and minutes-weighted averages of all players' PER values
- **Starters PER**: Average PER of starting lineup only
- **Top 5 PER Slots**: Individual PER values for top 5 players (sorted by PER), captures star power
- Player Efficiency Rating (PER) measures per-minute productivity, normalized so league average = 15.0
- Provides player-level talent signal that complements team-level statistics

---

## 2. Model Specific Groups

### 2.1 Classifier Model (Win Prediction)

#### Feature Set
All features from the groups above are included in the classifier model:
- Base features (differentials)
- Absolute features (for key stats)
- Elo differential
- Rest differential
- Enhanced features (games played, pace, volatility, schedule, offense/defense splits)
- Era normalization features (if enabled)
- PER features (if enabled)

**Total Feature Count** (approximate):
- Base: ~40 differential features
- Absolute: ~16 features (for key stats)
- Elo: 1 feature
- Rest: 1 feature
- Enhanced: 27 features
- Era normalization: 6 features (if enabled)
- PER: 19 features (if enabled)
- **Total: ~110 features** (with all optional groups enabled)

#### Reason
The classifier model uses a comprehensive feature set because:

1. **Multiple Time Windows**: Features computed over different time horizons (season, last month, last 10 games) capture both long-term trends and recent form, allowing the model to weight recency appropriately

2. **Differential + Absolute**: Including both differentials (relative advantage) and absolute values (magnitude) helps the model learn non-linear relationships where both relative and absolute performance matter

3. **Side-Specific Statistics**: Home/away splits capture venue effects that are crucial in NBA (home court advantage is significant)

4. **Enhanced Context**: Schedule context (rest, back-to-backs, games in short periods) and volatility metrics capture situational factors that affect game outcomes beyond raw talent

5. **Player-Level Signal**: PER features provide individual talent metrics that complement team-level statistics, especially important for star-driven matchups

6. **Era Normalization**: When enabled, allows fair comparison across seasons with different league-wide scoring environments

7. **Elo Ratings**: Provide a dynamic strength metric that evolves with each game, capturing momentum and trends not fully reflected in stat averages

8. **Exponential Weighting**: When enabled, recent games are weighted more heavily, allowing the model to adapt to mid-season changes (trades, injuries, coaching changes)

The model architecture (LogisticRegression, GradientBoosting, SVM, etc.) can handle this high-dimensional feature space and learn complex interactions between features, making the comprehensive set optimal for win prediction.

### 2.2 Points Regression Model (Score Prediction)

#### Feature Set
**Source**: `get_default_points_features()` in `NBAModel.py`

**Features**:
- `ppgSznAvg` (team's points per game, season average)
- `sidePpgSznAvg` (team's points per game in home/away context)
- `oppAgainstPpgSznAvg` (opponent's points allowed per game)
- `opp_against_side_ppgSznAvg` (opponent's points allowed in home/away context)
- `offRtgSznAvg` (team's offensive rating)
- `oppDefRtgSznAvg` (opponent's defensive rating)
- `paceSznAvg` (team's pace - possessions per game)
- `efgSznAvg` (team's effective field goal percentage)
- `opp_efg_defSznAvg` (opponent's defensive eFG% allowed)
- `gamesPlayedSoFar` (number of games played in season so far)

**Total Feature Count**: 9 features per team (18 total for both teams)

#### Reason
The points regression model uses a focused feature set because:

1. **Team-Specific Features**: Unlike the classifier which uses differentials, points regression predicts each team's score independently, requiring per-team features

2. **Offense vs. Defense**: Includes both team's offensive capability (`ppgSznAvg`, `offRtgSznAvg`, `efgSznAvg`) and opponent's defensive capability (`oppAgainstPpgSznAvg`, `oppDefRtgSznAvg`, `opp_efg_defSznAvg`) to capture the matchup

3. **Pace Control**: Pace feature is critical for score prediction as it determines the number of possessions, directly affecting total points

4. **Side Context**: Home/away splits matter for scoring (home teams typically score more), so side-specific features are included

5. **Season Progression**: `gamesPlayedSoFar` accounts for early-season uncertainty and late-season rest/playoff preparation effects

6. **Simpler Model Needs**: Regression models benefit from a focused feature set that directly relates to scoring (offensive stats, defensive matchups, pace) without the complexity needed for win prediction

7. **Computational Efficiency**: Fewer features make the model faster to train and easier to interpret, which is valuable for a secondary prediction task

The points model uses GradientBoostingRegressor which can capture non-linear relationships between these core features without needing the full complexity of the classifier feature set.

---

## Feature Transformation Summary

### Database → Features Pipeline

1. **Raw Game Data** (`stats_nba` collection):
   - Box scores: points, rebounds, assists, field goals, free throws, turnovers, etc.
   - Game metadata: date, teams, season, home/away, result

2. **StatHandlerV2 Processing**:
   - Aggregates stats over time windows (season, months, days, games)
   - Computes advanced stats (ratings, eFG%, pace, etc.)
   - Applies exponential weighting (optional)
   - Calculates differentials: `(home_stat - home_opponent_stat) - (away_stat - away_opponent_stat)`

3. **Enhanced Feature Computation**:
   - Pace: `(FG_att - off_reb + TO + 0.4*FT_att) / games`
   - Volatility: Standard deviation of points over last 10 games
   - Schedule context: Count games in last N days, detect back-to-backs
   - Offense/defense splits: Separate offensive and defensive ratings

4. **Elo Rating System**:
   - Initialize all teams at 1500
   - Update after each game: `new_elo = old_elo + K * (actual - expected)`
   - Expected win probability: `1 / (1 + 10^((opponent_elo - team_elo + home_advantage) / 400))`

5. **PER Calculation**:
   - Load player stats from `stats_nba_players`
   - Calculate PER using Hollinger's formula (uPER → aPER → PER)
   - Aggregate to team level (averages, weighted, starters-only, top 5)

6. **Feature Vector Assembly**:
   - Combine all feature groups in fixed order
   - Handle missing data (PER features default to 0 if unavailable)
   - Write to CSV with metadata and target label

### Key Design Decisions

- **Differential Features**: Most features are differentials (home - away) rather than absolute values, which is optimal for binary classification (home win vs. away win)
- **Multiple Time Windows**: Same stat computed over different windows (season, month, 10 games) allows model to learn optimal recency weighting
- **Exponential Weighting**: Optional decay function (`exp(-lambda * days_ago)`) gives more weight to recent games
- **Side-Specific Stats**: Home/away splits capture venue effects that are significant in NBA
- **Enhanced Features**: Contextual features (rest, schedule density, volatility) capture situational factors beyond raw talent
- **PER Integration**: Player-level metrics complement team-level stats, especially important for star-driven outcomes

