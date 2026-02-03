# Stats Agent Mini Tool Catalog

This is a **compact** catalog for the Stats Agent only.

## Critical Concept: Team Games vs Head-to-Head

**This distinction matters. Getting it wrong produces invalid audits.**

| Concept | Meaning | Tool |
|---------|---------|------|
| **Team Games** | Games a team played against ANY opponent | `get_team_games`, `get_team_stats` |
| **Head-to-Head (H2H)** | Games where two SPECIFIC teams played EACH OTHER | `get_head_to_head_games`, `get_head_to_head_stats` |

**Example:**
- "MIL's last 5 games" → `get_team_games(team_id="19", window="games5")` → MIL vs BOS, MIL vs LAL, MIL vs PHI, etc.
- "MIL vs CHI head-to-head" → `get_head_to_head_stats(team_a_id="19", team_b_id="14", window="seasons2")` → Only games where MIL played CHI

**When auditing Model Inspector claims:**
- "Team A has better recent form" → Use `get_team_stats` (general team performance)
- "Team A dominates the H2H matchup" → Use `get_head_to_head_stats` (specific matchup history)
- "Team A is 3-1 against Team B this season" → Use `get_head_to_head_stats` (H2H record)

## Shared IDs
- **`game_id`**: provided in shared context (`shared_context.game_id`)
- **`team_id`**: from `shared_context.game.home.team_id` / `shared_context.game.away.team_id`
- **`player_id`**: from `get_lineups(team_id)` output (`starters[]/bench[]/injured[][].id`)
- **`window`**:
  - `"season"`: season-to-date (scoped to matchup season + pre-game date)
  - `"gamesN"`: last N games (e.g. `"games12"`)
  - `"daysN"`: last N days (e.g. `"days5"`) as a bounded date range before the matchup date (when matchup context exists)
- **`split`**: `"home"`, `"away"`, or `null`

## Tools (allowed)

### `get_lineups(team_id)`
- **Use**: discover player IDs (starters/bench/injured).
- **Args**:
  - `team_id` (string)
- **Example**: `get_lineups(team_id="19")`
- **Returns**: `{ starters: [{id,name,pos}], bench: [...], injured: [...] }`

### `get_team_stats(team, window, split=None)` ⭐ USE FOR TEAM RECORDS/AVERAGES
- **Use**: get pre-computed team aggregates (wins, losses, averages). **Use this instead of counting games manually.**
- **Args**:
  - `team` (string): Team abbreviation (e.g., "LAL", "MIL")
  - `window` (string): "season", "games_5", "games_10", "games_12", "games_20"
  - `split` (optional string): "home", "away", or null for all
- **Example**: `get_team_stats(team="MIL", window="season")`
- **Returns**:
  ```json
  {
    "team": "MIL",
    "window": "season",
    "split": "all",
    "games_played": 45,
    "wins": 28,
    "losses": 17,
    "win_pct": 0.622,
    "avg_points": 112.4,
    "avg_points_allowed": 108.2,
    "avg_margin": 4.2,
    "streak": "W3",
    "home_games": 23,
    "away_games": 22
  }
  ```
- **IMPORTANT**: Always use this tool for team records and averages. Do NOT try to count wins/losses from `get_team_games` - it's error-prone.

### `compare_team_stats(team_a, team_b, window)`
- **Use**: compare two teams' stats side by side with deltas.
- **Args**:
  - `team_a` (string): First team abbreviation
  - `team_b` (string): Second team abbreviation
  - `window` (string): "season", "games_10", etc.
- **Example**: `compare_team_stats(team_a="MIL", team_b="BOS", window="season")`
- **Returns**: Both teams' stats plus deltas (team_a - team_b)

### `get_rotation_stats(team_id, window)` ⭐ USE FOR PLAYER TALENT AUDITS
- **Use**: get pre-computed rotation/talent aggregates. **Use this instead of calling get_advanced_player_stats for each player.**
- **Args**:
  - `team_id` (string)
  - `window` (string): "season", "games_10", etc.
- **Example**: `get_rotation_stats(team_id="19", window="season")`
- **Returns**:
  ```json
  {
    "team": "MIL",
    "window": "season",
    "top1_per": {"player": "Giannis Antetokounmpo", "player_id": "203507", "per": 28.4, "mpg": 35.2},
    "top3_per_avg": 24.1,
    "top3_players": ["Giannis Antetokounmpo", "Damian Lillard", "Khris Middleton"],
    "starter_avg_per": 19.2,
    "rotation_avg_per": 16.8,
    "mpg_weighted_per": 18.5,
    "starters": [
      {"name": "Giannis Antetokounmpo", "player_id": "203507", "per": 28.4, "mpg": 35.2},
      ...
    ],
    "bench": [
      {"name": "Bobby Portis", "player_id": "...", "per": 14.2, "mpg": 22.1},
      ...
    ]
  }
  ```
- **IMPORTANT**: Use this for talent/rotation audits. Returns all the aggregates you need in one call.

### `get_team_games(team_id, window, split=None)`
- **Use**: pull individual game results for trend analysis (NOT for counting records - use `get_team_stats` instead).
- **Args**:
  - `team_id` (string)
  - `window` (string)
  - `split` (optional string)
- **Example**: `get_team_games(team_id="19", window="games_10")`
- **Returns**: list of simplified game docs with `team_won` and points fields.
- **Note**: For W-L records, use `get_team_stats`. This tool is for inspecting individual game trends.
- **⚠️ NOT FOR HEAD-TO-HEAD**: This returns a team's games against ANY opponent. For games between two specific teams, use `get_head_to_head_games` or `get_head_to_head_stats`.

### `get_head_to_head_games(team_a_id, team_b_id, window)` ⭐ USE FOR H2H GAME LIST
- **Use**: get games where two specific teams played EACH OTHER (head-to-head matchups).
- **Args**:
  - `team_a_id` (string): First team ID
  - `team_b_id` (string): Second team ID
  - `window` (string): "season", "games5", "seasons2" (last 2 seasons), etc.
- **Example**: `get_head_to_head_games(team_a_id="19", team_b_id="14", window="seasons2")`
- **Returns**: list of H2H games with results from team_a's perspective
  ```json
  [
    {
      "date": "2024-12-15",
      "team_a": "MIL", "team_b": "CHI",
      "team_a_home": true,
      "team_a_points": 112, "team_b_points": 105,
      "team_a_won": true
    }
  ]
  ```
- **IMPORTANT**: This is the ONLY tool for head-to-head analysis. `get_team_games` does NOT filter by opponent.

### `get_head_to_head_stats(team_a_id, team_b_id, window)` ⭐ USE FOR H2H RECORDS
- **Use**: get aggregated head-to-head record and stats between two teams.
- **Args**:
  - `team_a_id` (string): First team ID
  - `team_b_id` (string): Second team ID
  - `window` (string): "season", "games5", "seasons2" (last 2 seasons), etc.
- **Example**: `get_head_to_head_stats(team_a_id="19", team_b_id="14", window="seasons2")`
- **Returns**:
  ```json
  {
    "team_a": "MIL",
    "team_b": "CHI",
    "games_played": 6,
    "team_a_wins": 4,
    "team_b_wins": 2,
    "record": "MIL 4-2 vs CHI",
    "team_a_avg_points": 115.2,
    "team_b_avg_points": 108.4,
    "avg_margin": 6.8,
    "last_meeting_date": "2024-12-15",
    "last_meeting_winner": "MIL",
    "recent_games": [...]
  }
  ```
- **IMPORTANT**: Use this for H2H record verification. Do NOT try to infer H2H from `get_team_games`.

### `get_player_stats(player_id, window, split=None)`
- **Use**: pull per-game player box-score rows.
- **Args**:
  - `player_id` (string)
  - `window` (string)
  - `split` (optional string)
- **Example**: `get_player_stats(player_id="203507", window="games12")`

### `get_advanced_player_stats(player_id, window, split=None)`
- **Use**: pull derived per-window player summary (avg box stats + pct + mpg + per when matchup context available).
- **Args**:
  - `player_id` (string)
  - `window` (string)
  - `split` (optional string)
- **Example**: `get_advanced_player_stats(player_id="203507", window="season")`

### `run_code(code)`
- **Use**: compute aggregates (MPG-weighted PER, rotation summaries, with/without-player, etc.).
- **Args**:
  - `code` (string)

