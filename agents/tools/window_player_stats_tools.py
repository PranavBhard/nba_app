"""
Windowed player stats tools for matchup agents.

Implements the Stats agent expected interfaces:
  - get_player_stats(player_id, window, split=None)
  - get_advanced_player_stats(player_id, window, split=None)

For now, `advanced` returns lightweight derived per-game averages from the raw window.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from nba_app.core.mongo import Mongo
from nba_app.core.stats.per_calculator import PERCalculator


def _get_coll(league, key: str, fallback: str) -> str:
    if league is not None and getattr(league, "collections", None):
        return league.collections.get(key) or fallback
    return fallback


WINDOW_RE = re.compile(r"^games(\d+)$", re.I)
DAYS_RE = re.compile(r"^days(\d+)$", re.I)


def _parse_window(window: str) -> Dict[str, Any]:
    if not window:
        raise ValueError('window is required (examples: "days5", "games10", "games12", "games18", "season")')
    w = window.strip()
    if w.lower() == "season":
        return {"kind": "season"}
    m = WINDOW_RE.match(w)
    if m:
        try:
            return {"kind": "games", "n": int(m.group(1))}
        except Exception as e:
            raise ValueError(f'invalid window "{window}"') from e
    d = DAYS_RE.match(w)
    if d:
        try:
            return {"kind": "days", "n": int(d.group(1))}
        except Exception as e:
            raise ValueError(f'invalid window "{window}"') from e
    raise ValueError(f'invalid window "{window}" (allowed: "season", "gamesN", or "daysN")')


def get_player_stats(
    player_id: str,
    window: str,
    split: Optional[str] = None,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> List[Dict[str, Any]]:
    if db is None:
        db = Mongo().db
    spec = _parse_window(window)

    # Hard rule: exclude preseason/allstar by default (audits should never include preseason).
    # If `game_type` is missing in older docs, Mongo `$nin` still matches and includes them.
    query: Dict[str, Any] = {
        "player_id": str(player_id),
        "stats.min": {"$gt": 0},
        "game_type": {"$nin": ["preseason", "allstar"]},
    }

    # Anchor to matchup date/season when possible (prevents multi-season/career pulls).
    if game_id and spec.get("kind") in {"season", "days"}:
        games_coll = _get_coll(league, "games", "stats_nba")
        game_doc = db[games_coll].find_one({"game_id": game_id}) or {}
        game_season = game_doc.get("season")
        game_date = str(game_doc.get("date") or "")[:10] if game_doc.get("date") else ""
        if game_season:
            query["season"] = game_season
        if game_date:
            date_clause: Dict[str, Any] = {"$lt": game_date}
            if spec.get("kind") == "days":
                try:
                    n_days = int(spec.get("n") or 0)
                except Exception:
                    n_days = 0
                if n_days > 0:
                    start = (datetime.strptime(game_date, "%Y-%m-%d") - timedelta(days=n_days)).strftime("%Y-%m-%d")
                    date_clause["$gte"] = start
            query["date"] = date_clause
    if split == "home":
        query["home"] = True
    elif split == "away":
        query["home"] = False

    player_stats_coll = _get_coll(league, "player_stats", "stats_nba_players")
    cursor = db[player_stats_coll].find(query).sort("date", -1)
    docs = list(cursor)
    if spec.get("kind") == "games":
        try:
            n = int(spec.get("n") or 0)
        except Exception:
            n = 0
        if n > 0:
            docs = docs[:n]

    out: List[Dict[str, Any]] = []
    for g in docs:
        out.append(
            {
                "player_id": str(g.get("player_id", "")),
                "player_name": g.get("player_name", ""),
                "game_id": g.get("game_id", ""),
                "date": str(g.get("date", ""))[:10],
                "season": g.get("season", ""),
                "team": g.get("team", ""),
                "opponent": g.get("opponent", ""),
                "home": g.get("home", False),
                "starter": g.get("starter", False),
                "stats": g.get("stats", {}) or {},
            }
        )
    return out


def get_advanced_player_stats(
    player_id: str,
    window: str,
    split: Optional[str] = None,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> List[Dict[str, Any]]:
    """
    Lightweight derived stats per window.

    Returns a single-element list with averaged box score fields (pts, reb, ast, min, etc.)
    plus basic rates when possible.
    """
    if db is None:
        db = Mongo().db
    games = get_player_stats(player_id, window, split=split, db=db, game_id=game_id, league=league)
    if not games:
        return []

    # Aggregate simple means
    keys = ["min", "pts", "reb", "ast", "stl", "blk", "to", "pf", "fg_made", "fg_att", "three_made", "three_att", "ft_made", "ft_att"]
    sums = {k: 0.0 for k in keys}
    n = 0
    name = games[0].get("player_name", "")
    for g in games:
        stats = g.get("stats") or {}
        n += 1
        for k in keys:
            sums[k] += float(stats.get(k, 0) or 0)
    avgs = {k: (sums[k] / n if n else 0.0) for k in keys}

    fg_pct = (avgs["fg_made"] / avgs["fg_att"]) if avgs["fg_att"] else 0.0
    three_pct = (avgs["three_made"] / avgs["three_att"]) if avgs["three_att"] else 0.0
    ft_pct = (avgs["ft_made"] / avgs["ft_att"]) if avgs["ft_att"] else 0.0

    # Add season-to-date PER when we can anchor it to the matchup season/date.
    # This is intentionally independent of the requested window; PER is used as a baseline ability metric.
    per: Optional[float] = None
    try:
        if game_id:
            games_coll = _get_coll(league, "games", "stats_nba")
            game_doc = db[games_coll].find_one({"game_id": game_id}) or {}
            matchup_season = game_doc.get("season")
            matchup_date = str(game_doc.get("date") or "")[:10] if game_doc.get("date") else ""
            # Best-effort team from the most recent game in the window
            team = games[0].get("team") or ""
            if matchup_season and matchup_date and team:
                calc = PERCalculator(db=db, preload=False, league=league)
                per = calc.get_player_per_before_date(
                    player_id=str(player_id),
                    team=str(team),
                    season=str(matchup_season),
                    before_date=str(matchup_date),
                )
    except Exception:
        per = None

    return [
        {
            "player_id": str(player_id),
            "player_name": name,
            "window": window,
            "split": split,
            "games": n,
            "avg": avgs,
            "pct": {"fg": fg_pct, "three": three_pct, "ft": ft_pct},
            # Convenience fields (explicit) for common display/analysis
            "mpg": avgs.get("min", 0.0),
            "per": per,
        }
    ]


def get_rotation_stats(
    team_id: str,
    window: str,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> Dict[str, Any]:
    """
    Get pre-computed rotation/talent aggregates for a team.

    Returns PER-based aggregates: top-1, top-3 avg, starter avg, rotation avg, MPG-weighted PER.
    This eliminates the need for stats_agent to call get_advanced_player_stats for each player.

    Args:
        team_id: Team ID
        window: Time window ("season", "games10", etc.)
        game_id: Matchup game_id for date scoping
        db: MongoDB database instance
        league: League config

    Returns:
        Dict with rotation aggregates and per-player breakdowns
    """
    if db is None:
        db = Mongo().db

    # Import lineup tool to get roster
    from nba_app.agents.tools.lineup_tools import get_lineups

    lineup_data = get_lineups(team_id, game_id=game_id, db=db, league=league)

    if "error" in lineup_data:
        return {"error": lineup_data["error"], "team_id": team_id, "window": window}

    team_label = lineup_data.get("team", str(team_id))
    starters_raw = lineup_data.get("starters", [])
    bench_raw = lineup_data.get("bench", [])
    injured_raw = lineup_data.get("injured", [])

    # Collect player stats for starters and bench (active players)
    starters_stats = []
    bench_stats = []

    for player in starters_raw:
        player_id = player.get("id") or player.get("player_id")
        if not player_id:
            continue
        adv = get_advanced_player_stats(str(player_id), window, game_id=game_id, db=db, league=league)
        if adv and len(adv) > 0:
            stat = adv[0]
            starters_stats.append({
                "name": stat.get("player_name", player.get("name", "")),
                "player_id": str(player_id),
                "per": stat.get("per"),
                "mpg": stat.get("mpg", 0.0),
                "games": stat.get("games", 0),
            })

    for player in bench_raw:
        player_id = player.get("id") or player.get("player_id")
        if not player_id:
            continue
        adv = get_advanced_player_stats(str(player_id), window, game_id=game_id, db=db, league=league)
        if adv and len(adv) > 0:
            stat = adv[0]
            bench_stats.append({
                "name": stat.get("player_name", player.get("name", "")),
                "player_id": str(player_id),
                "per": stat.get("per"),
                "mpg": stat.get("mpg", 0.0),
                "games": stat.get("games", 0),
            })

    # Combine all active players for rotation stats
    all_players = starters_stats + bench_stats

    # Filter to players with valid PER
    players_with_per = [p for p in all_players if p.get("per") is not None]

    if not players_with_per:
        return {
            "team": team_label,
            "team_id": str(team_id),
            "window": window,
            "error": "No players with PER data found",
            "starters": starters_stats,
            "bench": bench_stats,
            "injured": [{"name": p.get("name", ""), "player_id": p.get("id") or p.get("player_id")} for p in injured_raw],
        }

    # Sort by PER descending
    sorted_by_per = sorted(players_with_per, key=lambda x: x.get("per", 0) or 0, reverse=True)

    # Top-1 PER
    top1 = sorted_by_per[0] if sorted_by_per else None

    # Top-3 PER average
    top3 = sorted_by_per[:3]
    top3_per_avg = sum(p.get("per", 0) or 0 for p in top3) / len(top3) if top3 else 0.0
    top3_players = [p.get("name", "") for p in top3]

    # Starter average PER
    starters_with_per = [p for p in starters_stats if p.get("per") is not None]
    starter_avg_per = sum(p.get("per", 0) or 0 for p in starters_with_per) / len(starters_with_per) if starters_with_per else 0.0

    # Rotation average PER (all active players)
    rotation_avg_per = sum(p.get("per", 0) or 0 for p in players_with_per) / len(players_with_per) if players_with_per else 0.0

    # MPG-weighted PER
    total_mpg = sum(p.get("mpg", 0) or 0 for p in players_with_per)
    if total_mpg > 0:
        mpg_weighted_per = sum((p.get("per", 0) or 0) * (p.get("mpg", 0) or 0) for p in players_with_per) / total_mpg
    else:
        mpg_weighted_per = 0.0

    return {
        "team": team_label,
        "team_id": str(team_id),
        "window": window,
        "top1_per": {
            "player": top1.get("name", "") if top1 else None,
            "player_id": top1.get("player_id", "") if top1 else None,
            "per": round(top1.get("per", 0) or 0, 1) if top1 else None,
            "mpg": round(top1.get("mpg", 0) or 0, 1) if top1 else None,
        } if top1 else None,
        "top3_per_avg": round(top3_per_avg, 1),
        "top3_players": top3_players,
        "starter_avg_per": round(starter_avg_per, 1),
        "rotation_avg_per": round(rotation_avg_per, 1),
        "mpg_weighted_per": round(mpg_weighted_per, 1),
        "starters": starters_stats,
        "bench": bench_stats,
        "injured": [{"name": p.get("name", ""), "player_id": p.get("id") or p.get("player_id")} for p in injured_raw],
    }

