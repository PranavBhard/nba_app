# Model Inspector Mini Tool Catalog

This is a **compact** catalog for the Model Inspector only.

## Shared IDs
- **`game_id`**: provided in shared context (`shared_context.game_id`)

## Tools (allowed)

### `get_base_model_direction_table(game_id)` ⭐ USE THIS FIRST
- **Use**: Get pre-computed direction table showing which team each base model favors
- **Args**:
  - `game_id` (string)
- **Example**: `get_base_model_direction_table(game_id="401810542")`
- **Returns**:
  ```json
  {
    "game_id": "401810542",
    "p_home": 0.471,
    "ensemble_favors": "AWAY",
    "direction_table": [
      {"base_model": "B1", "name": "Season Strength", "output": 0.514, "favors": "HOME", "magnitude": 0.014},
      {"base_model": "B2", "name": "Recent Form", "output": 0.594, "favors": "HOME", "magnitude": 0.094},
      {"base_model": "B4", "name": "Player Talent", "output": 0.387, "favors": "AWAY", "magnitude": 0.113},
      ...
    ],
    "summary": {"home_count": 4, "away_count": 2, "neutral_count": 0}
  }
  ```
- **IMPORTANT**: This tool computes directions for you. The `favors` field is the ground truth. Do NOT override it with your own interpretation.

### `get_prediction_base_outputs(game_id)`
- **Use**: fetch raw meta-feature values (meta-model inputs) for this game.
- **Args**:
  - `game_id` (string)
- **Example**: `get_prediction_base_outputs(game_id="401810542")`
- **Returns**: `whole_doc.output.features_dict._ensemble_breakdown.meta_feature_values`
- **Note**: Use `get_base_model_direction_table` instead for pre-computed directions.

### `get_prediction_snapshot_base_outputs(snapshot_id)`
- **Use**: fetch meta-feature values (meta-model inputs) for a specific scenario snapshot (immutable).
- **Args**:
  - `snapshot_id` (string): returned by `experimenter`'s `predict()` tool
- **Example**: `get_prediction_snapshot_base_outputs(snapshot_id="9f6e8c3b-...")`
- **Returns**: `prediction_doc.output.features_dict._ensemble_breakdown.meta_feature_values`

### `get_ensemble_meta_model_params(game_id)`
- **Use**: fetch meta-model coefficients/intercept/feature order for contribution reconstruction.
- **Args**:
  - `game_id` (string)
- **Example**: `get_ensemble_meta_model_params(game_id="401810542")`
- **Returns**: `{ ensemble_run_id, meta_model_type, meta_feature_cols, intercept, coefficients }`

### `get_prediction_doc(game_id)`
- **Use**: fetch per-base-model breakdown for this game (not the entire prediction doc).
- **Args**:
  - `game_id` (string)
- **Example**: `get_prediction_doc(game_id="401810542")`
- **Returns**: `whole_doc.output.features_dict._ensemble_breakdown.base_models`

### `get_prediction_snapshot_doc(snapshot_id)`
- **Use**: fetch per-base-model breakdown for a specific scenario snapshot (immutable).
- **Args**:
  - `snapshot_id` (string): returned by `experimenter`'s `predict()` tool
- **Example**: `get_prediction_snapshot_doc(snapshot_id="9f6e8c3b-...")`
- **Returns**: `prediction_doc.output.features_dict._ensemble_breakdown.base_models`

### `get_prediction_feature_values(game_id, keys=None)`
- **Use**: fetch specific feature values from the prediction doc (selectively; avoid pulling everything unless needed).
- **Args**:
  - `game_id` (string)
  - `keys` (optional list[str])
- **Examples**:
  - `get_prediction_feature_values(game_id="401810542", keys=["home_elo","away_elo"])`
- **Returns**: `features_dict` (full or filtered)

### `get_selected_configs()`
- **Use**: see which model configs are active.
- **Args**: none
- **Returns**: `{ classifier: {...} | null, points: {...} | null }`

