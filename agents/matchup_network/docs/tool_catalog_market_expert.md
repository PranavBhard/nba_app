# Market Expert Mini Tool Catalog

This is a **compact** catalog for the Market Expert only.

## Shared IDs
- **`game_id`**: provided in shared context (`shared_context.game_id`)

## Tools (allowed)

### `get_game_markets(game_id)`
- **Use**: fetch prediction market prices + vegas odds (live from ESPN with fallback).
- **Args**:
  - `game_id` (string)
- **Example**: `get_game_markets(game_id="401810542")`
- **Returns**: `{ prediction_markets: {...}, vegas_odds: {...} }`

