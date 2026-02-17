# PER Normalization Implementation

## Overview

PER normalization has been implemented to ensure that league average PER is always 15.0, as per Hollinger's original formula. This makes PER values comparable across different seasons and eras.

## What Features Does It Produce?

**The same feature names as before**, but with **normalized values**:

### Existing Features (Now Normalized)

1. **perAvgDiff** - `homeTeamPerAvg - awayTeamPerAvg`
   - `homeTeamPerAvg`: Average PER of top 8 players (normalized, league avg = 15.0)
   - `awayTeamPerAvg`: Average PER of top 8 players (normalized, league avg = 15.0)

2. **perWeightedDiff** - `homeTeamPerWeighted - awayTeamPerWeighted`
   - `homeTeamPerWeighted`: Minutes-weighted average PER of top 8 players (normalized)
   - `awayTeamPerWeighted`: Minutes-weighted average PER of top 8 players (normalized)

3. **startersPerDiff** - `homeStartersPerAvg - awayStartersPerAvg`
   - `homeStartersPerAvg`: Average PER of starting lineup (normalized)
   - `awayStartersPerAvg`: Average PER of starting lineup (normalized)

4. **Individual PER Slots** (per1Diff, per2Diff, etc.)
   - `homePer1` through `homePer8`: Individual PER values for top 8 players (normalized)
   - `awayPer1` through `awayPer8`: Individual PER values for top 8 players (normalized)

## Key Differences

### Before Normalization (aPER)
- League average varied by season (could be 12.0, 14.5, 16.2, etc.)
- Hard to compare across seasons
- Values not standardized

### After Normalization (PER)
- League average is always 15.0
- Values are comparable across seasons
- Follows Hollinger's original PER specification
- A PER of 20.0 means the player is 33% above league average
- A PER of 10.0 means the player is 33% below league average

## Implementation Details

### Normalization Formula
```
PER = aPER * (15.0 / lg_aPER)
```

Where:
- `aPER`: Pace-adjusted PER for the player
- `lg_aPER`: League average aPER (minutes-weighted) for the season
- `15.0`: Target league average

### League Average aPER Calculation

The `lg_aPER` is computed by:
1. Getting all player stats for the season (before the game date)
2. Calculating aPER for each player
3. Computing minutes-weighted average: `sum(aPER * minutes) / sum(minutes)`

### Fallback Behavior

If `lg_aPER` cannot be computed or is 0:
- Falls back to using aPER directly (no normalization)
- Logs a warning
- Features still work, but values are not normalized

### Caching

- `lg_aPER` is computed on-demand the first time it's needed
- Attempts to cache in `cached_league_stats` collection for future use
- If cached, uses cached value (much faster)

## Feature Values

All PER features now produce values where:
- **League average = 15.0**
- **Above average players > 15.0**
- **Below average players < 15.0**
- **Star players typically 20.0+**
- **Elite players typically 25.0+**

## Example

Before normalization (aPER):
- League average: 13.5
- Player A: 18.0 aPER (33% above average)
- Player B: 9.0 aPER (33% below average)

After normalization (PER):
- League average: 15.0
- Player A: 20.0 PER (33% above average)
- Player B: 10.0 PER (33% below average)

The relative differences are preserved, but values are now standardized.

## Benefits

1. **Era Comparison**: Can compare players across different NBA eras
2. **Consistency**: League average always 15.0 makes interpretation easier
3. **Standardization**: Follows Hollinger's original PER specification
4. **Model Training**: Normalized values may help model training (more consistent scale)

## Code Locations

- **Normalization**: `cli/per_calculator.py::compute_per()` (lines 291-307)
- **League Average**: `cli/per_calculator.py::compute_league_average_aper()` (lines 309-458)
- **Feature Calculation**: `cli/per_calculator.py::compute_team_per_features()` (uses normalized PER)

