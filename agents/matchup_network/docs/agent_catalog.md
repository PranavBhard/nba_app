# Matchup Network Agent Catalog

This is the authoritative description of **what each agent does** and **what inputs/tools** it can use.
The Planner uses this to decide which agents to run.

## Agents

### `model_inspector`
- **Purpose**: Explain *why* the model predicted what it predicted (technical, model-native).
- **Inputs**:
  - `shared_context.game_id`
  - `shared_context.ensemble_model.p_home` (baseline anchor only)
  - Any other prediction artifacts must be fetched via tools (SSoT is the model predictions collection)
- **Tools** (allowed):
  - `get_base_model_direction_table(game_id)` ⭐ **USE FIRST** — pre-computed directions
  - `get_selected_configs()`
  - `get_ensemble_meta_model_params(game_id)`
  - `get_prediction_doc(game_id)`
  - `get_prediction_feature_values(game_id, keys=None)`
  - `get_prediction_base_outputs(game_id)`
- **Writes**:
  - a technical explanation of model drivers and anomalies
  - an `AuditChecklistJSON` block (for the Stats Agent to execute)
  - a `ModelClaimsJSON` block (auditable claims for contradiction detection)

### `stats_agent`
- **Purpose**: Audit Model Inspector claims using database-backed tools.
- **Inputs**:
  - `shared_context.game` (teams/date/team_ids)
  - `AuditChecklistJSON` from Model Inspector output
- **Tools** (allowed):
  - `get_team_stats(team_id, window, split=None)` ⭐ **USE FOR TEAM RECORDS** — pre-computed aggregates
  - `compare_team_stats(team_a, team_b, window)` — side-by-side team comparison
  - `get_rotation_stats(team_id, window)` ⭐ **USE FOR TALENT AUDITS** — PER aggregates
  - `get_lineups(team_id)` — roster/injury info
  - `get_team_games(team_id, window, split=None)` — individual game results (for trends)
  - `get_player_stats(player_id, window, split=None)`
  - `get_advanced_player_stats(player_id, window, split=None)`
  - `run_code(code)` (for ad-hoc aggregation)
- **Writes**:
  - audit results for each checklist item (supports/contradicts/inconclusive)
  - an `AuditResultsJSON` block

### `research_media_agent`
- **Purpose**: Fetch and summarize up-to-date media/news context for teams/players and the specific matchup.
- **Inputs**:
  - `shared_context.game` (team names/team_ids/date)
  - stats agent output for guidance (optional dependency)
- **Tools**:
  - `get_game_news(game_id, force_refresh=False)`
  - `get_team_news(team_id, force_refresh=False)`
  - `get_player_news(player_id, force_refresh=False)`
- **Writes**: concise news summary; cite sources from tool results.

### `experimenter`
- **Purpose**: Run "what if" / "with vs without player" predictions by changing roster state and rerunning the standard prediction pipeline.
- **Inputs**:
  - `shared_context.game_id`
  - `shared_context.game` (teams/date/team_ids)
- **Tools** (allowed):
  - `get_lineups(team_id)` (to discover player IDs + current bucket)
  - `set_player_lineup_bucket(player_id, bucket)` (mutates `nba_rosters`; persists platform-wide)
  - `predict()` (calls core `PredictionService` and upserts to the normal model predictions collection)
- **Writes**:
  - clear statement of what roster changes were applied
  - updated prediction summary + deltas vs baseline when applicable
  - scenario snapshot ids (for Model Inspector to analyze “what shifted”)

### `final_synthesizer`
- **Purpose**: Combine agent outputs into a single user-facing response.
- **Inputs**:
  - `shared_context` + `conversation` + `turn_plan.final_synthesis_instructions`
  - all workflow outputs this turn
- **Tools**: none
- **Writes**: final answer to user.

