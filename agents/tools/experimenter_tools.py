"""
Tools for the `experimenter` matchup-network agent.

These tools are intentionally restricted to this agent because they mutate
platform-wide prediction inputs (nba_rosters) and then trigger a standard
core prediction run that persists to the model_predictions collection.

Key idea:
- No "override params" to prediction. We persist roster state in `nba_rosters`,
  then call the same PredictionService path used everywhere else.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from nba_app.core.mongo import Mongo
from nba_app.core.data import RostersRepository, GamesRepository
from nba_app.core.services.prediction import PredictionService


def _get_coll(league, key: str, fallback: str) -> str:
    if league is not None and getattr(league, "collections", None):
        return league.collections.get(key) or fallback
    return fallback


def set_player_lineup_bucket(
    player_id: str,
    bucket: str,
    *,
    game_id: str,
    db=None,
    league=None,
) -> Dict[str, Any]:
    """
    Move a player between lineup buckets by mutating `nba_rosters`.

    Args:
      player_id: ESPN player id (string)
      bucket: one of {"starter", "bench", "injured"}
      game_id: matchup game id (string) used to infer season + which teams apply

    Returns:
      Small JSON-safe summary including team/season and before/after flags.
    """
    if db is None:
        db = Mongo().db
    bucket_norm = (bucket or "").strip().lower()
    if bucket_norm not in {"starter", "bench", "injured"}:
        return {"error": f'invalid bucket "{bucket}" (allowed: "starter", "bench", "injured")'}

    games_coll = _get_coll(league, "games", "stats_nba")
    game_doc = db[games_coll].find_one({"game_id": game_id}) or {}
    season = game_doc.get("season")
    home = (game_doc.get("homeTeam") or {}).get("name")
    away = (game_doc.get("awayTeam") or {}).get("name")
    if not season or not home or not away:
        return {"error": "could_not_infer_season_or_teams", "game_id": game_id, "season": season, "home": home, "away": away}

    rosters_repo = RostersRepository(db, league=league)

    # Determine which team roster contains the player (home or away).
    target_team: Optional[str] = None
    before: Optional[Dict[str, Any]] = None
    for team in [home, away]:
        r = rosters_repo.find_roster(team, season) or {}
        for entry in (r.get("roster") or []):
            if str(entry.get("player_id")) == str(player_id):
                target_team = team
                before = {
                    "injured": bool(entry.get("injured", False)),
                    "starter": bool(entry.get("starter", False)),
                }
                break
        if target_team:
            break

    if not target_team:
        return {"error": "player_not_found_on_home_or_away_roster", "player_id": str(player_id), "home_team": home, "away_team": away, "season": season}

    # Map bucket -> (injured, starter)
    injured = bucket_norm == "injured"
    starter = bucket_norm == "starter"
    # bench => both False

    ok = rosters_repo.update_player_lineup_flags(
        target_team,
        season,
        str(player_id),
        injured=injured,
        starter=starter,
    )

    after = {"injured": injured, "starter": starter}
    return {
        "ok": bool(ok),
        "game_id": str(game_id),
        "season": str(season),
        "team": str(target_team),
        "player_id": str(player_id),
        "before": before,
        "after": after,
        "note": "This change persists in nba_rosters and will affect subsequent predictions until changed again.",
    }


def predict_game_and_persist(*, game_id: str, db=None, league=None) -> Dict[str, Any]:
    """
    Run the standard core prediction pipeline for this game_id and persist it.

    IMPORTANT:
    - This uses PredictionService, which reads nba_rosters starter/injured flags.
    - It upserts into the model_predictions collection (SSoT).
    """
    if db is None:
        db = Mongo().db
    games_repo = GamesRepository(db, league=league)
    game_doc = games_repo.find_by_game_id(game_id) or {}
    home = (game_doc.get("homeTeam") or {}).get("name") or ""
    away = (game_doc.get("awayTeam") or {}).get("name") or ""
    game_date = str(game_doc.get("date") or "")[:10]
    if not home or not away or not game_date:
        return {"error": "missing_game_metadata", "game_id": str(game_id), "home_team": home, "away_team": away, "game_date": game_date}

    service = PredictionService(db=db, league=league)
    result = service.predict_game(
        home_team=home,
        away_team=away,
        game_date=game_date,
        game_id=game_id,
        player_config={},  # no overrides; roster state is the source of truth
        include_points=True,
    )
    if getattr(result, "error", None):
        return {"error": "prediction_failed", "message": result.error, "game_id": str(game_id)}

    # Persist via core SSoT (latest prediction per game_id)
    try:
        game_date_obj = datetime.strptime(game_date, "%Y-%m-%d").date()
        saved = service.save_prediction(result=result, game_id=game_id, game_date=game_date_obj, home_team=home, away_team=away)
    except Exception as e:
        return {
            "error": "prediction_save_failed",
            "message": str(e),
            "game_id": str(game_id),
            "prediction_preview": {
                "home_win_prob": getattr(result, "home_win_prob", None),
                "away_win_prob": getattr(result, "away_win_prob", None),
                "home_points_pred": getattr(result, "home_points_pred", None),
                "away_points_pred": getattr(result, "away_points_pred", None),
            },
        }

    # Snapshot: persist an immutable scenario record so later analysis can compare
    # even though the main predictions collection is upserted by game_id.
    snapshot_id = str(uuid4())
    try:
        # Capture roster state (starter/injured flags) for both teams
        rosters_repo = RostersRepository(db, league=league)
        season = (game_doc.get("season") or "").strip()
        home_roster = rosters_repo.find_roster(home, season) or {}
        away_roster = rosters_repo.find_roster(away, season) or {}

        def _min_roster(doc: Dict[str, Any]) -> Dict[str, Any]:
            out = {"team": doc.get("team"), "season": doc.get("season"), "updated_at": str(doc.get("updated_at") or "")}
            roster = []
            for p in (doc.get("roster") or []):
                roster.append(
                    {
                        "player_id": str(p.get("player_id", "")),
                        "starter": bool(p.get("starter", False)),
                        "injured": bool(p.get("injured", False)),
                    }
                )
            out["roster"] = roster
            return out

        # Capture the just-saved prediction doc (full) so it can be compared later.
        pred_doc = service.get_prediction_for_game(game_id) or {}
        pred_doc.pop("_id", None)

        scenarios_coll = "nba_prediction_scenarios"
        if league is not None and getattr(league, "collections", None):
            scenarios_coll = league.collections.get("prediction_scenarios", scenarios_coll)

        db[scenarios_coll].insert_one(
            {
                "snapshot_id": snapshot_id,
                "game_id": str(game_id),
                "created_at": datetime.utcnow().isoformat() + "+00:00",
                "season": season,
                "home_team": home,
                "away_team": away,
                "roster_state": {
                    "home": _min_roster(home_roster),
                    "away": _min_roster(away_roster),
                },
                "prediction_doc": pred_doc,
            }
        )
    except Exception as e:
        # Don't fail the tool; just report snapshot failure.
        snapshot_id = ""
        snapshot_error = str(e)
    else:
        snapshot_error = ""

    # Return a small summary (avoid huge features_dict blobs)
    p_home = None
    try:
        if getattr(result, "home_win_prob", None) is not None:
            p_home = float(result.home_win_prob) / 100.0
    except Exception:
        p_home = None

    return {
        "ok": True,
        "game_id": str(game_id),
        "home_team": home,
        "away_team": away,
        "game_date": game_date,
        "p_home": p_home,
        "home_win_prob": getattr(result, "home_win_prob", None),
        "away_win_prob": getattr(result, "away_win_prob", None),
        "home_points_pred": getattr(result, "home_points_pred", None),
        "away_points_pred": getattr(result, "away_points_pred", None),
        "point_diff_pred": getattr(result, "point_diff_pred", None),
        "saved_to_model_predictions": True,
        "predicted_at": (saved or {}).get("predicted_at"),
        "snapshot_id": snapshot_id,
        **({"snapshot_error": snapshot_error} if snapshot_error else {}),
    }

