# Experimenter Mini Tool Catalog

This is a **compact** catalog for the Experimenter agent only.

## Shared IDs
- **`game_id`**: provided in shared context (`shared_context.game_id`)
- **`team_id`**: from `shared_context.game.home.team_id` / `shared_context.game.away.team_id`
- **`player_id`**: from `get_lineups(team_id)` output (`starters[]/bench[]/injured[][].id`)

## Tools (allowed)

### `get_lineups(team_id)`
- **Use**: discover player IDs and current bucket (starters/bench/injured) as stored in `nba_rosters`.
- **Args**:
  - `team_id` (string)
- **Example**: `get_lineups(team_id="21")`

### `set_player_lineup_bucket(player_id, bucket)`
- **Use**: move a player between `injured` / `bench` / `starter` in the rosters collection.
- **Args**:
  - `player_id` (string)
  - `bucket` (string): `"injured"`, `"bench"`, or `"starter"`
- **Example**: `set_player_lineup_bucket(player_id="203507", bucket="injured")`
- **Returns**: `{ ok, team, season, before, after, note }`
- **Note**: This change **persists platform-wide** and affects subsequent predictions.

### `predict()`
- **Use**: run the standard core `PredictionService` for this `game_id` and persist to model predictions (SSoT).
- **Args**: none
- **Example**: `predict()`
- **Returns**: `{ ok, p_home, home_win_prob, away_win_prob, home_points_pred, away_points_pred, ... }`

