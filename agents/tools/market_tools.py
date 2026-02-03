"""
Market tools for matchup agents.

Provides a single entrypoint:
  get_game_markets(game_id) -> {
      'prediction_markets': {...},
      'vegas_odds': {...}
  }

Kalshi market data is fetched via core `core/market/kalshi.py` (public API).
Vegas odds are sourced from the game document (`pregame_lines` / `vegas`).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from nba_app.core.mongo import Mongo
from nba_app.core.market.kalshi import get_game_market_data
from nba_app.core.services.espn_odds import get_live_pregame_lines


def _get_coll(league, key: str, fallback: str) -> str:
    if league is not None and getattr(league, "collections", None):
        return league.collections.get(key) or fallback
    return fallback


def get_game_markets(game_id: str, *, db=None, league=None, league_id: str = "nba") -> Dict[str, Any]:
    if db is None:
        db = Mongo().db
    league_id = (league_id or "nba").lower()

    games_coll = _get_coll(league, "games", "stats_nba")
    game = db[games_coll].find_one({"game_id": game_id}) or {}

    # Vegas odds from ESPN API (fresh). Fallback to DB snapshot if fetch fails.
    vegas_odds = get_live_pregame_lines(game_id, league=league) or (game.get("pregame_lines") or game.get("vegas") or {})
    vegas_odds_source = "espn_api" if (isinstance(vegas_odds, dict) and ("over_under" in vegas_odds or "spread" in vegas_odds or "home_ml" in vegas_odds or "away_ml" in vegas_odds)) else "db_snapshot"

    # Kalshi prediction markets (best-effort)
    prediction_markets: Optional[Dict[str, Any]] = None
    try:
        date_str = str(game.get("date") or "")[:10]
        game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        away = (game.get("awayTeam") or {}).get("name") or ""
        home = (game.get("homeTeam") or {}).get("name") or ""
        md = get_game_market_data(game_date=game_date, away_team=away, home_team=home, league_id=league_id)
        prediction_markets = md.to_dict() if md is not None else None
    except Exception as e:
        prediction_markets = {"error": str(e)}

    return {
        "prediction_markets": prediction_markets,
        "vegas_odds": vegas_odds,
        "vegas_odds_source": vegas_odds_source,
    }

