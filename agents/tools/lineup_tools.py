"""
Lineup tools for matchup agents.

Goal: return starters/bench/injured in the shape used by stats + research agents:
{
  "starters": [{id, name, pos}, ...],
  "bench": [{id, name, pos}, ...],
  "injured": [{id, name, pos}, ...]
}

This is intended to be sourced from the same roster/inactives source used by
prediction (rosters collection + players lookup).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from nba_app.core.mongo import Mongo
from nba_app.core.utils import get_season_from_date


def _get_coll(league, key: str, fallback: str) -> str:
    if league is not None and getattr(league, "collections", None):
        return league.collections.get(key) or fallback
    return fallback


def _team_abbrev_from_team_id(db, league, team_id: str) -> Optional[str]:
    teams_coll = _get_coll(league, "teams", "teams_nba")
    doc = db[teams_coll].find_one({"team_id": team_id}) or db[teams_coll].find_one({"id": team_id}) or {}
    abbr = doc.get("abbreviation") or doc.get("abbr")
    return str(abbr) if abbr else None


def get_lineups(team_id: str, *, game_id: Optional[str] = None, db=None, league=None) -> Dict[str, List[Dict[str, Any]]]:
    if db is None:
        db = Mongo().db

    # Determine season from the game if possible
    season = None
    if game_id:
        games_coll = _get_coll(league, "games", "stats_nba")
        g = db[games_coll].find_one({"game_id": game_id}) or {}
        if g.get("season"):
            season = g.get("season")
        elif g.get("date"):
            try:
                season = get_season_from_date(str(g["date"])[:10])
            except Exception:
                season = None

    team_abbrev = _team_abbrev_from_team_id(db, league, str(team_id)) or str(team_id)

    rosters_coll = _get_coll(league, "rosters", "nba_rosters")
    roster_doc = None
    if season:
        roster_doc = db[rosters_coll].find_one({"season": season, "team": team_abbrev})
    if roster_doc is None:
        roster_doc = db[rosters_coll].find_one({"team": team_abbrev})

    roster_list = (roster_doc or {}).get("roster") or []

    players_coll = _get_coll(league, "players", "players_nba")
    player_ids = [str(p.get("player_id", "")) for p in roster_list if p.get("player_id") is not None]
    players = list(db[players_coll].find({"player_id": {"$in": player_ids}}, {"player_id": 1, "player_name": 1, "position": 1}))
    name_map = {str(p.get("player_id")): p.get("player_name") for p in players}
    pos_map = {str(p.get("player_id")): p.get("position") for p in players}

    starters: List[Dict[str, Any]] = []
    bench: List[Dict[str, Any]] = []
    injured: List[Dict[str, Any]] = []

    for entry in roster_list:
        pid = str(entry.get("player_id", ""))
        obj = {"id": pid, "name": name_map.get(pid, ""), "pos": pos_map.get(pid, "")}
        if entry.get("injured"):
            injured.append(obj)
        elif entry.get("starter"):
            starters.append(obj)
        else:
            bench.append(obj)

    return {"starters": starters, "bench": bench, "injured": injured}

