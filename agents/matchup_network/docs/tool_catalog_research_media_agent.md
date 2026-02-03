# Research / Media Agent Mini Tool Catalog

This is a **compact** catalog for the Research/Media agent only.

## Shared IDs
- **`game_id`**: provided in shared context (`shared_context.game_id`)
- **`team_id`**: from `shared_context.game.home.team_id` / `shared_context.game.away.team_id`
- **`player_id`**: from `get_lineups(team_id)` output (if Stats Agent provides it), or from shared context in the future
- **`force_refresh`**: set true when the UI toggle “Re-run web searches” is enabled

## Tools (allowed)

### `web_search(query, force_refresh=False, num_results=5)`
- **Use**: general-purpose web search when the specialized news tools are too strict or you need broader context.
- **Args**:
  - `query` (string)
  - `force_refresh` (bool)
  - `num_results` (int, default 5)
- **Example**: `web_search(query="Orlando Magic Franz Wagner injury update", force_refresh=true, num_results=5)`

### `get_game_news(game_id, force_refresh=False)`
- **Use**: matchup-scoped news sweep (preview/injuries/rotation notes).
- **Args**:
  - `game_id` (string)
  - `force_refresh` (bool)
- **Example**: `get_game_news(game_id="401810542", force_refresh=true)`

### `get_team_news(team_id, force_refresh=False)`
- **Use**: team-scoped latest news.
- **Args**:
  - `team_id` (string)
  - `force_refresh` (bool)
- **Example**: `get_team_news(team_id="19", force_refresh=true)`

### `get_player_news(player_id, force_refresh=False)`
- **Use**: player-scoped latest news (availability/minutes/role).
- **Args**:
  - `player_id` (string)
  - `force_refresh` (bool)
- **Example**: `get_player_news(player_id="203507", force_refresh=true)`

