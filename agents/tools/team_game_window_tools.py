"""
Windowed team game retrieval tools for matchup agents.

Implements the Stats agent expected interface:
  get_team_games(team_id, window, split=None) -> List[Dict]
where window examples include: "games10", "games12", "season".
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from nba_app.core.mongo import Mongo


WINDOW_RE = re.compile(r"^games(\d+)$", re.I)
DAYS_RE = re.compile(r"^days(\d+)$", re.I)


def _get_coll(league, key: str, fallback: str) -> str:
    if league is not None and getattr(league, "collections", None):
        return league.collections.get(key) or fallback
    return fallback


def _team_keys_from_team_id(db, league, team_id: str) -> List[str]:
    """
    Return possible identifiers used in games documents for this team.

    Some datasets store `homeTeam.name`/`awayTeam.name` as abbreviations (e.g. "PHX"),
    others as display names (e.g. "Phoenix Suns"). We query with both to avoid
    silently missing games (which causes bad W/L records).
    """
    teams_coll = _get_coll(league, "teams", "teams_nba")
    doc = db[teams_coll].find_one({"team_id": team_id}) or db[teams_coll].find_one({"id": team_id}) or {}
    abbr = (doc.get("abbreviation") or doc.get("abbr") or "").strip()
    display = (doc.get("displayName") or doc.get("name") or "").strip()
    # De-dupe while preserving order
    out: List[str] = []
    for v in [abbr, display, str(team_id).strip()]:
        if v and v not in out:
            out.append(v)
    return out


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
    # IMPORTANT: do not treat unknown windows as unlimited (this can explode context).
    raise ValueError(f'invalid window "{window}" (allowed: "season", "gamesN", or "daysN")')


def get_team_games(
    team_id: str,
    window: str,
    split: Optional[str] = None,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> List[Dict[str, Any]]:
    if db is None:
        db = Mongo().db
    team_keys = _team_keys_from_team_id(db, league, str(team_id))
    # For output labeling, prefer the first key (usually abbrev).
    team_label = team_keys[0] if team_keys else str(team_id)

    games_coll = _get_coll(league, "games", "stats_nba")
    game_doc = db[games_coll].find_one({"game_id": game_id}) if game_id else None
    before_date = None
    game_season = None
    if game_doc and game_doc.get("date"):
        before_date = str(game_doc["date"])[:10]
    if game_doc and game_doc.get("season"):
        game_season = game_doc.get("season")

    spec = _parse_window(window)

    query: Dict[str, Any] = {
        "$or": [{"homeTeam.name": {"$in": team_keys}}, {"awayTeam.name": {"$in": team_keys}}],
        # Completed games only (NBA games won't be 0-0).
        "homeTeam.points": {"$gt": 0},
        "awayTeam.points": {"$gt": 0},
        "game_type": {"$nin": ["preseason", "allstar"]},
    }
    # Date scoping
    if before_date:
        # window is always "before the matchup date" when game_id is available
        date_clause: Dict[str, Any] = {"$lt": before_date}
        if spec.get("kind") == "days":
            n_days = int(spec.get("n") or 0)
            if n_days > 0:
                start = (datetime.strptime(before_date, "%Y-%m-%d") - timedelta(days=n_days)).strftime("%Y-%m-%d")
                date_clause["$gte"] = start
        query["date"] = date_clause

    # Season scoping (avoid multi-season pulls)
    if game_season and spec.get("kind") in {"season", "days"}:
        query["season"] = game_season

    if split == "home":
        query = {**query, "homeTeam.name": {"$in": team_keys}}
        query.pop("$or", None)
    elif split == "away":
        query = {**query, "awayTeam.name": {"$in": team_keys}}
        query.pop("$or", None)

    projection = {
        "game_id": 1,
        "date": 1,
        "season": 1,
        "homeTeam.name": 1,
        "awayTeam.name": 1,
        "homeTeam.points": 1,
        "awayTeam.points": 1,
        "homeWon": 1,
    }

    cursor = db[games_coll].find(query, projection).sort("date", -1)
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
        home = (g.get("homeTeam") or {}).get("name")
        away = (g.get("awayTeam") or {}).get("name")
        home_pts = (g.get("homeTeam") or {}).get("points")
        away_pts = (g.get("awayTeam") or {}).get("points")
        home_won = g.get("homeWon")
        is_team_home = (home in team_keys)
        team_points = home_pts if is_team_home else away_pts
        opp_points = away_pts if is_team_home else home_pts
        # If homeWon is missing, fall back to points comparison.
        team_won = None
        try:
            if isinstance(home_won, bool):
                team_won = bool(home_won) if is_team_home else (not bool(home_won))
            elif home_pts is not None and away_pts is not None:
                team_won = (team_points > opp_points) if (team_points is not None and opp_points is not None) else None
        except Exception:
            team_won = None
        out.append(
            {
                "game_id": g.get("game_id"),
                "date": str(g.get("date") or "")[:10],
                "season": g.get("season"),
                "home": home,
                "away": away,
                "home_points": home_pts,
                "away_points": away_pts,
                "homeWon": home_won,
                "team": team_label,
                # Convenience fields for unambiguous record calculations
                "is_team_home": is_team_home,
                "team_points": team_points,
                "opp_points": opp_points,
                "team_won": team_won,
            }
        )
    return out


def get_team_stats(
    team_id: str,
    window: str,
    split: Optional[str] = None,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> Dict[str, Any]:
    """
    Get pre-computed team aggregates (wins, losses, averages) over a time window.

    This is more reliable than having the LLM count wins/losses from get_team_games.

    Args:
        team_id: Team ID (e.g., "19")
        window: Time window - "season", "games_5", "games_10", "games_12", "games_20"
        split: Optional - "home", "away", or None for all
        game_id: Matchup game_id for date scoping
        db: MongoDB database instance
        league: League config for collection names

    Returns:
        Dict with aggregated statistics:
        - team, window, split, season
        - games_played, wins, losses, win_pct
        - avg_points, avg_points_allowed, avg_margin
        - streak, last_game_date
        - home_games, away_games (if split is None)
    """
    # Reuse get_team_games to get the filtered game list
    # Convert window format if needed (games_10 -> games10)
    window_normalized = window.replace("_", "")
    games = get_team_games(team_id, window_normalized, split=split, game_id=game_id, db=db, league=league)

    if not games:
        return {
            "team": str(team_id),
            "window": window,
            "split": split or "all",
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "win_pct": 0.0,
            "error": f"No games found for team {team_id} with window {window}"
        }

    # Compute aggregates
    wins = 0
    losses = 0
    home_games = 0
    away_games = 0
    total_points = 0
    total_points_allowed = 0

    # Track streak
    streak_type = None
    streak_count = 0
    streak_broken = False

    for i, game in enumerate(games):
        is_home = game.get("is_team_home", False)
        team_won = game.get("team_won")
        team_points = game.get("team_points", 0) or 0
        opp_points = game.get("opp_points", 0) or 0

        if is_home:
            home_games += 1
        else:
            away_games += 1

        if team_won is True:
            wins += 1
        elif team_won is False:
            losses += 1

        # Track streak (games are sorted most recent first)
        # Once streak is broken, stop counting
        if not streak_broken and team_won is not None:
            if i == 0:
                streak_type = "W" if team_won else "L"
                streak_count = 1
            elif (team_won and streak_type == "W") or (not team_won and streak_type == "L"):
                streak_count += 1
            else:
                streak_broken = True

        total_points += team_points
        total_points_allowed += opp_points

    games_played = len(games)
    team_label = games[0].get("team", str(team_id)) if games else str(team_id)
    season = games[0].get("season") if games else None

    result = {
        "team": team_label,
        "window": window,
        "split": split or "all",
        "season": season,
        "games_played": games_played,
        "wins": wins,
        "losses": losses,
        "win_pct": round(wins / games_played, 3) if games_played > 0 else 0.0,
        "avg_points": round(total_points / games_played, 1) if games_played > 0 else 0.0,
        "avg_points_allowed": round(total_points_allowed / games_played, 1) if games_played > 0 else 0.0,
        "avg_margin": round((total_points - total_points_allowed) / games_played, 1) if games_played > 0 else 0.0,
        "streak": f"{streak_type}{streak_count}" if streak_type else None,
        "last_game_date": games[0].get("date") if games else None,
    }

    # Add home/away breakdown if not filtered by split
    if not split:
        result["home_games"] = home_games
        result["away_games"] = away_games

    return result


def compare_team_stats(
    team_a_id: str,
    team_b_id: str,
    window: str,
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> Dict[str, Any]:
    """
    Compare two teams' stats side by side with deltas.

    Useful for matchup analysis - returns both teams' stats and the differences.

    Args:
        team_a_id: First team ID
        team_b_id: Second team ID
        window: Time window (season, games_10, etc.)
        game_id: Matchup game_id for date scoping
        db: MongoDB database instance
        league: League config

    Returns:
        Dict with team_a stats, team_b stats, and deltas (team_a - team_b)
    """
    stats_a = get_team_stats(team_a_id, window, game_id=game_id, db=db, league=league)
    stats_b = get_team_stats(team_b_id, window, game_id=game_id, db=db, league=league)

    # Compute deltas (team_a - team_b)
    deltas = {}
    numeric_keys = ["win_pct", "avg_points", "avg_points_allowed", "avg_margin"]

    for key in numeric_keys:
        val_a = stats_a.get(key)
        val_b = stats_b.get(key)
        if val_a is not None and val_b is not None:
            deltas[key] = round(val_a - val_b, 2)

    return {
        "team_a": stats_a,
        "team_b": stats_b,
        "deltas": deltas,
        "window": window,
        "season": stats_a.get("season"),
    }


def get_head_to_head_games(
    team_a_id: str,
    team_b_id: str,
    window: str = "season",
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> List[Dict[str, Any]]:
    """
    Get games where team_a and team_b played EACH OTHER (head-to-head).

    This is NOT the same as get_team_games which returns all games for one team.
    Head-to-head means only games where these two specific teams faced each other.

    Args:
        team_a_id: First team ID (e.g., "19")
        team_b_id: Second team ID (e.g., "14")
        window: Time window - "season", "games5", "games10", or "seasons2" (last 2 seasons)
        game_id: Matchup game_id for date scoping (only return games before this game)
        db: MongoDB database instance
        league: League config for collection names

    Returns:
        List of game dicts with results from team_a's perspective:
        - game_id, date, season
        - team_a, team_b (abbreviations)
        - team_a_home (bool), team_a_points, team_b_points
        - team_a_won (bool)
    """
    if db is None:
        db = Mongo().db
    team_a_keys = _team_keys_from_team_id(db, league, str(team_a_id))
    team_b_keys = _team_keys_from_team_id(db, league, str(team_b_id))
    team_a_label = team_a_keys[0] if team_a_keys else str(team_a_id)
    team_b_label = team_b_keys[0] if team_b_keys else str(team_b_id)

    games_coll = _get_coll(league, "games", "stats_nba")

    # Get matchup date/season context
    game_doc = db[games_coll].find_one({"game_id": game_id}) if game_id else None
    before_date = None
    game_season = None
    if game_doc and game_doc.get("date"):
        before_date = str(game_doc["date"])[:10]
    if game_doc and game_doc.get("season"):
        game_season = game_doc.get("season")

    # Build query: games where team_a vs team_b (either as home or away)
    query: Dict[str, Any] = {
        "$or": [
            # team_a home, team_b away
            {"homeTeam.name": {"$in": team_a_keys}, "awayTeam.name": {"$in": team_b_keys}},
            # team_b home, team_a away
            {"homeTeam.name": {"$in": team_b_keys}, "awayTeam.name": {"$in": team_a_keys}},
        ],
        # Completed games only
        "homeTeam.points": {"$gt": 0},
        "awayTeam.points": {"$gt": 0},
        "game_type": {"$nin": ["preseason", "allstar"]},
    }

    # Date scoping
    if before_date:
        query["date"] = {"$lt": before_date}

    # Parse window for season scoping
    w = window.strip().lower() if window else "season"

    # Handle multi-season window (e.g., "seasons2", "seasons3")
    seasons_match = re.match(r"^seasons(\d+)$", w)
    if seasons_match:
        n_seasons = int(seasons_match.group(1))
        if game_season:
            # Build list of seasons to include
            try:
                start_year = int(game_season.split("-")[0])
                seasons_to_include = [f"{start_year - i}-{start_year - i + 1}" for i in range(n_seasons)]
                query["season"] = {"$in": seasons_to_include}
            except (ValueError, IndexError):
                pass
    elif w == "season" and game_season:
        query["season"] = game_season

    projection = {
        "game_id": 1,
        "date": 1,
        "season": 1,
        "homeTeam.name": 1,
        "awayTeam.name": 1,
        "homeTeam.points": 1,
        "awayTeam.points": 1,
        "homeWon": 1,
    }

    cursor = db[games_coll].find(query, projection).sort("date", -1)
    docs = list(cursor)

    # Apply games limit if specified (e.g., "games5" = last 5 H2H games)
    games_match = WINDOW_RE.match(w)
    if games_match:
        try:
            n = int(games_match.group(1))
            if n > 0:
                docs = docs[:n]
        except Exception:
            pass

    out: List[Dict[str, Any]] = []
    for g in docs:
        home = (g.get("homeTeam") or {}).get("name")
        away = (g.get("awayTeam") or {}).get("name")
        home_pts = (g.get("homeTeam") or {}).get("points")
        away_pts = (g.get("awayTeam") or {}).get("points")
        home_won = g.get("homeWon")

        # Determine perspective from team_a
        team_a_is_home = (home in team_a_keys)
        team_a_pts = home_pts if team_a_is_home else away_pts
        team_b_pts = away_pts if team_a_is_home else home_pts

        # Determine winner
        team_a_won = None
        try:
            if isinstance(home_won, bool):
                team_a_won = bool(home_won) if team_a_is_home else (not bool(home_won))
            elif home_pts is not None and away_pts is not None:
                team_a_won = (team_a_pts > team_b_pts) if (team_a_pts is not None and team_b_pts is not None) else None
        except Exception:
            team_a_won = None

        out.append({
            "game_id": g.get("game_id"),
            "date": str(g.get("date") or "")[:10],
            "season": g.get("season"),
            "team_a": team_a_label,
            "team_b": team_b_label,
            "team_a_home": team_a_is_home,
            "team_a_points": team_a_pts,
            "team_b_points": team_b_pts,
            "team_a_won": team_a_won,
            # Raw game info
            "home": home,
            "away": away,
            "home_points": home_pts,
            "away_points": away_pts,
        })

    return out


def get_head_to_head_stats(
    team_a_id: str,
    team_b_id: str,
    window: str = "season",
    *,
    game_id: Optional[str] = None,
    db=None,
    league=None,
) -> Dict[str, Any]:
    """
    Get head-to-head record and stats between two teams.

    Returns aggregated stats from games where team_a and team_b played EACH OTHER.

    Args:
        team_a_id: First team ID (e.g., "19")
        team_b_id: Second team ID (e.g., "14")
        window: Time window - "season", "games5", "games10", or "seasons2" (last 2 seasons)
        game_id: Matchup game_id for date scoping
        db: MongoDB database instance
        league: League config for collection names

    Returns:
        Dict with head-to-head stats:
        - team_a, team_b (abbreviations)
        - games_played, team_a_wins, team_b_wins
        - team_a_home_wins, team_a_away_wins (when team_a was home/away)
        - team_a_avg_points, team_b_avg_points, avg_margin
        - last_meeting_date, last_meeting_winner
        - recent_games: list of last 5 games with scores
    """
    games = get_head_to_head_games(team_a_id, team_b_id, window, game_id=game_id, db=db, league=league)

    if not games:
        if db is None:
            db = Mongo().db
        team_a_keys = _team_keys_from_team_id(db, league, str(team_a_id))
        team_b_keys = _team_keys_from_team_id(db, league, str(team_b_id))
        return {
            "team_a": team_a_keys[0] if team_a_keys else str(team_a_id),
            "team_b": team_b_keys[0] if team_b_keys else str(team_b_id),
            "window": window,
            "games_played": 0,
            "team_a_wins": 0,
            "team_b_wins": 0,
            "error": f"No head-to-head games found between these teams with window {window}"
        }

    team_a_label = games[0].get("team_a", str(team_a_id))
    team_b_label = games[0].get("team_b", str(team_b_id))

    # Compute aggregates
    team_a_wins = 0
    team_b_wins = 0
    team_a_home_wins = 0
    team_a_away_wins = 0
    team_a_total_pts = 0
    team_b_total_pts = 0

    for g in games:
        team_a_won = g.get("team_a_won")
        team_a_home = g.get("team_a_home", False)
        team_a_pts = g.get("team_a_points") or 0
        team_b_pts = g.get("team_b_points") or 0

        if team_a_won is True:
            team_a_wins += 1
            if team_a_home:
                team_a_home_wins += 1
            else:
                team_a_away_wins += 1
        elif team_a_won is False:
            team_b_wins += 1

        team_a_total_pts += team_a_pts
        team_b_total_pts += team_b_pts

    games_played = len(games)

    # Last meeting info (games sorted most recent first)
    last_game = games[0]
    last_meeting_winner = None
    if last_game.get("team_a_won") is True:
        last_meeting_winner = team_a_label
    elif last_game.get("team_a_won") is False:
        last_meeting_winner = team_b_label

    # Build recent games summary (last 5)
    recent_games = []
    for g in games[:5]:
        recent_games.append({
            "date": g.get("date"),
            "score": f"{team_a_label} {g.get('team_a_points')} - {g.get('team_b_points')} {team_b_label}",
            "winner": team_a_label if g.get("team_a_won") else team_b_label,
            "location": "home" if g.get("team_a_home") else "away",
        })

    return {
        "team_a": team_a_label,
        "team_b": team_b_label,
        "window": window,
        "games_played": games_played,
        "team_a_wins": team_a_wins,
        "team_b_wins": team_b_wins,
        "record": f"{team_a_label} {team_a_wins}-{team_b_wins} vs {team_b_label}",
        "team_a_home_wins": team_a_home_wins,
        "team_a_away_wins": team_a_away_wins,
        "team_a_avg_points": round(team_a_total_pts / games_played, 1) if games_played > 0 else 0,
        "team_b_avg_points": round(team_b_total_pts / games_played, 1) if games_played > 0 else 0,
        "avg_margin": round((team_a_total_pts - team_b_total_pts) / games_played, 1) if games_played > 0 else 0,
        "last_meeting_date": last_game.get("date"),
        "last_meeting_winner": last_meeting_winner,
        "recent_games": recent_games,
    }

