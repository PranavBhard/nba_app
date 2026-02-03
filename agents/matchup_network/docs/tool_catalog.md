# Matchup Network Tool Catalog (SSoT)

This catalog defines the **tool surface** available to the matchup network.
System messages include this catalog so agents know what exists, but each agent must follow its own **allowed tools** list.

## Shared IDs / where to find arguments

- **`game_id`**: the game’s unique ID (string). Provided by the UI + shared context.
- **`team_id`**: numeric-ish string ID for a team.
  - **Where to find**: `shared_context.game.home.team_id` and `shared_context.game.away.team_id`
- **`player_id`**: numeric-ish string ID for a player.
  - **Where to find**: from `get_lineups(team_id)` results (`starters[]/bench[]/injured[]` items have `id`)
- **`window`**: which time window of games/stats you want.
  - **Allowed examples**: `"days5"`, `"games10"`, `"games12"`, `"games18"`, `"season"`
- **`split`**: optional filter for home/away splits.
  - **Allowed**: `"home"`, `"away"`, or `null`
- **`force_refresh`**: bypass cache and fetch fresh web results.
  - **Where it comes from**: the UI toggle “Re-run web searches” will set this for you.

## Market

### `get_game_markets(game_id)`
- **Args**
  - `game_id` (string): the game to fetch markets/odds for
- **Example**
  - `get_game_markets(game_id="401704123")`
- **Returns**: `{ prediction_markets: {...}, vegas_odds: {...} }`
- **Notes**: Kalshi is fetched live; vegas odds are fetched live from ESPN (with DB fallback if ESPN odds are unavailable).

## Model / Prediction

### `get_selected_configs()`
- **Args**: none
- **Returns**: `{ classifier: {...} | null, points: {...} | null }`
- **Notes**: Returns the currently selected model configs (classifier + points) from the DB.

### `get_prediction_doc(game_id)`
- **Args**
  - `game_id` (string)
- **Returns**: `whole_doc.output.features_dict._ensemble_breakdown.base_models` (JSON-safe; `{}` if missing)
- **Notes**: This is the per-game ensemble breakdown of base models (not the whole prediction doc).

### `get_prediction_feature_values(game_id, keys=None)`
- **Args**
  - `game_id` (string)
  - `keys` (optional list of strings): if provided, returns only those feature keys
- **Examples**
  - `get_prediction_feature_values(game_id="401704123")`
  - `get_prediction_feature_values(game_id="401704123", keys=["home_elo", "away_elo"])`
- **Returns**: `features_dict` (either full dict or a filtered subset by `keys`)

### `get_prediction_base_outputs(game_id)`
- **Args**
  - `game_id` (string)
- **Returns**: `whole_doc.output.features_dict._ensemble_breakdown.meta_feature_values` (JSON-safe; `{}` if missing)

### `get_ensemble_meta_model_params(game_id)`
- **Args**
  - `game_id` (string)
- **Returns**: `{ ensemble_run_id, meta_model_type, meta_feature_cols, intercept, coefficients }` (JSON-safe)
- **Use**: enables “what moved the needle” analysis by computing per-meta-feature logit contributions.

## News / Web

### `web_search(query, force_refresh=False, num_results=5)`
- **Args**
  - `query` (string): what you want to search for
  - `force_refresh` (bool, default `False`): bypass cache (use for breaking news)
  - `num_results` (int, default `5`): number of results to return
- **Returns**: `[{source, content, metadata}, ...]` (top 5)
- **Notes**: Uses SERP API + core webpage parsing.

### `get_game_news(game_id, force_refresh=False)`
- **Args**
  - `game_id` (string)
  - `force_refresh` (bool, default `False`)
- **Use**: game-scoped preview/injury/news sweep for the matchup
- **Returns**: `[{source, content, metadata}, ...]`
- **Notes**:
  - Uses SERP API **News vertical** (direct articles preferred; hub pages filtered when possible)
  - `content` is extracted article text (fallback: search snippet)

### `get_team_news(team_id, force_refresh=False)`
- **Args**
  - `team_id` (string): from `shared_context.game.home.team_id` / `shared_context.game.away.team_id`
  - `force_refresh` (bool, default `False`)
- **Use**: team-scoped latest news (injuries/quotes/rotation changes)
- **Returns**: `[{source, content, metadata}, ...]`
- **Notes**:
  - Uses SERP API **News vertical** (direct articles preferred; hub pages filtered when possible)
  - `content` is extracted article text (fallback: search snippet)

### `get_player_news(player_id, force_refresh=False)`
- **Args**
  - `player_id` (string): from `get_lineups(team_id)` output
  - `force_refresh` (bool, default `False`)
- **Use**: player-scoped latest news (availability, minutes, role)
- **Returns**: `[{source, content, metadata}, ...]`
- **Notes**:
  - Uses SERP API **News vertical** (direct articles preferred; hub pages filtered when possible)
  - `content` is extracted article text (fallback: search snippet)

## Stats / Data

### `get_lineups(team_id)`
- **Args**
  - `team_id` (string): from shared context (`game.home.team_id` / `game.away.team_id`)
- **Example**
  - `get_lineups(team_id="19")`
- **Returns**:
  - `{ starters: [{id,name,pos}], bench: [{id,name,pos}], injured: [{id,name,pos}] }`
- **Notes**
  - Use this first to discover `player_id` values for player stats/news tools.

### `get_team_games(team_id, window, split=None)`
- **Args**
  - `team_id` (string)
  - `window` (string): `"season"`, `"gamesN"` (e.g. `"games12"`), or `"daysN"` (e.g. `"days5"`)
  - `split` (optional string): `"home"`, `"away"`, or `null`
- **Examples**
  - `get_team_games(team_id="19", window="games10")`
  - `get_team_games(team_id="19", window="season", split="home")`
- **Returns**: list of simplified game docs prior to the current game date.

### `get_player_stats(player_id, window, split=None)`
- **Args**
  - `player_id` (string): from `get_lineups(team_id)` output
  - `window` (string): `"season"`, `"gamesN"` (e.g. `"games12"`), or `"daysN"` (e.g. `"days5"`)
  - `split` (optional string): `"home"`, `"away"`, or `null`
- **Example**
  - `get_player_stats(player_id="203507", window="games10")`

### `get_advanced_player_stats(player_id, window, split=None)`
- **Args**
  - `player_id` (string): from `get_lineups(team_id)` output
  - `window` (string): `"season"`, `"gamesN"` (e.g. `"games12"`), or `"daysN"` (e.g. `"days5"`)
  - `split` (optional string): `"home"`, `"away"`, or `null`
- **Example**
  - `get_advanced_player_stats(player_id="203507", window="games10")`

### `run_code(code)`
- **Args**
  - `code` (string): Python code to execute in a sandboxed helper that can query DB via the tool implementation
- **Purpose**: ad-hoc aggregation/calcs (e.g. with/without-player splits, derived metrics, custom filters)

## Situational / Counterfactual prediction

### `set_player_lineup_bucket(player_id, bucket)`
- **Args**
  - `player_id` (string)
  - `bucket` (string): `"injured"`, `"bench"`, or `"starter"`
- **Use**: mutate `nba_rosters` to change who is considered injured/starter for prediction.
- **Notes**: this change **persists platform-wide** until changed again.

### `predict()`
- **Args**: none
- **Use**: run the standard core prediction pipeline for the current matchup and persist to the model predictions collection (SSoT).

