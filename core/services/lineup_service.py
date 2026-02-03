"""
Lineup Service - Fetches live game lineups from ESPN.

Provides structured lineup data for a game:
- Starters: players in starting lineup
- Bench: active players not starting
- Inactive: players who did not play (DNP, injury, etc.)

Usage:
    from core.services.lineup_service import LineupService

    service = LineupService("nba")
    lineups = service.get_game_lineups("401705051")

    # Access home team starters
    for player in lineups.home.starters:
        print(f"{player.name} ({player.position})")

    # Check inactive players
    for player in lineups.away.inactive:
        print(f"{player.name} - {player.dnp_reason}")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from nba_app.core.data.espn_client import ESPNClient
from nba_app.core.league_config import load_league_config

if TYPE_CHECKING:
    from nba_app.core.league_config import LeagueConfig

logger = logging.getLogger(__name__)


@dataclass
class PlayerLineup:
    """Individual player lineup information."""
    player_id: str
    name: str
    jersey: Optional[str] = None
    position: Optional[str] = None
    position_abbrev: Optional[str] = None
    is_starter: bool = False
    did_not_play: bool = False
    dnp_reason: Optional[str] = None
    is_ejected: bool = False
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "jersey": self.jersey,
            "position": self.position,
            "position_abbrev": self.position_abbrev,
            "is_starter": self.is_starter,
            "did_not_play": self.did_not_play,
            "dnp_reason": self.dnp_reason,
            "is_ejected": self.is_ejected,
            "is_active": self.is_active,
        }


@dataclass
class TeamLineup:
    """Lineup for a single team in a game."""
    team_id: str
    team_abbrev: str
    team_name: str
    starters: List[PlayerLineup] = field(default_factory=list)
    bench: List[PlayerLineup] = field(default_factory=list)
    inactive: List[PlayerLineup] = field(default_factory=list)

    @property
    def active_players(self) -> List[PlayerLineup]:
        """All players who played (starters + bench)."""
        return self.starters + self.bench

    @property
    def all_players(self) -> List[PlayerLineup]:
        """All players on roster for this game."""
        return self.starters + self.bench + self.inactive

    def to_dict(self) -> Dict[str, Any]:
        return {
            "team_id": self.team_id,
            "team_abbrev": self.team_abbrev,
            "team_name": self.team_name,
            "starters": [p.to_dict() for p in self.starters],
            "bench": [p.to_dict() for p in self.bench],
            "inactive": [p.to_dict() for p in self.inactive],
        }


@dataclass
class GameLineups:
    """Complete lineup data for a game."""
    game_id: str
    home: TeamLineup
    away: TeamLineup
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    game_status: Optional[str] = None  # 'pre', 'in', 'post'

    def to_dict(self) -> Dict[str, Any]:
        return {
            "game_id": self.game_id,
            "home": self.home.to_dict(),
            "away": self.away.to_dict(),
            "fetched_at": self.fetched_at.isoformat(),
            "game_status": self.game_status,
        }


class LineupService:
    """
    Service for fetching live game lineups from ESPN.

    Fetches lineup data directly from ESPN API at runtime,
    structured into starters, bench, and inactive players.
    """

    def __init__(
        self,
        league: Union[str, "LeagueConfig"] = "nba",
        timeout: int = 30,
    ):
        """
        Initialize the LineupService.

        Args:
            league: League ID string or LeagueConfig object
            timeout: Request timeout in seconds
        """
        if isinstance(league, str):
            self.league = load_league_config(league)
        else:
            self.league = league

        self.league_id = self.league.league_id
        self._client = ESPNClient(league=self.league, timeout=timeout)

    def get_game_lineups(self, game_id: str) -> Optional[GameLineups]:
        """
        Fetch lineups for a specific game from ESPN.

        Pulls live data from ESPN API and categorizes players into:
        - starters: players in starting lineup
        - bench: active players not starting
        - inactive: players who did not play (DNP, injury, etc.)

        Args:
            game_id: ESPN game ID

        Returns:
            GameLineups object with home and away team lineups,
            or None if the game data couldn't be fetched
        """
        summary = self._client.get_game_summary(game_id)
        if not summary:
            logger.warning(f"Could not fetch game summary for {game_id}")
            return None

        boxscore = summary.get("boxscore", {})
        players_data = boxscore.get("players", [])

        # Determine game status early for better error messages
        header = summary.get("header", {})
        competitions = header.get("competitions", [{}])
        status_info = competitions[0].get("status", {}) if competitions else {}
        game_status = status_info.get("type", {}).get("state", "pre")  # 'pre', 'in', 'post'

        if not players_data:
            if game_status == "pre":
                logger.info(f"Game {game_id} is pre-game - lineup data not yet available")
            else:
                logger.warning(f"No player data in game summary for {game_id} (status: {game_status})")
            return None

        # Determine game status from header
        header = summary.get("header", {})
        competitions = header.get("competitions", [{}])
        status_info = competitions[0].get("status", {}) if competitions else {}
        game_status = status_info.get("type", {}).get("state", "pre")  # 'pre', 'in', 'post'

        # Parse home and away teams
        home_lineup = None
        away_lineup = None

        for team_data in players_data:
            team_info = team_data.get("team", {})
            team_id = str(team_info.get("id", ""))
            team_abbrev = team_info.get("abbreviation", "")
            team_name = team_info.get("displayName", "")

            # Determine if home or away from header
            is_home = self._is_home_team(summary, team_id)

            # Parse players from statistics
            starters = []
            bench = []
            inactive = []

            statistics = team_data.get("statistics", [])
            if statistics:
                athletes = statistics[0].get("athletes", [])

                for athlete_data in athletes:
                    player = self._parse_player(athlete_data)
                    if player:
                        if player.did_not_play:
                            inactive.append(player)
                        elif player.is_starter:
                            starters.append(player)
                        else:
                            bench.append(player)

            team_lineup = TeamLineup(
                team_id=team_id,
                team_abbrev=team_abbrev,
                team_name=team_name,
                starters=starters,
                bench=bench,
                inactive=inactive,
            )

            if is_home:
                home_lineup = team_lineup
            else:
                away_lineup = team_lineup

        # Handle case where we couldn't determine home/away
        if home_lineup is None or away_lineup is None:
            if len(players_data) >= 2:
                # Fallback: use display order (usually away=0, home=1)
                team0 = self._parse_team_lineup(players_data[0])
                team1 = self._parse_team_lineup(players_data[1])

                order0 = players_data[0].get("displayOrder", 0)
                order1 = players_data[1].get("displayOrder", 1)

                if order0 < order1:
                    away_lineup = team0
                    home_lineup = team1
                else:
                    home_lineup = team0
                    away_lineup = team1
            else:
                logger.warning(f"Could not determine home/away teams for {game_id}")
                return None

        return GameLineups(
            game_id=game_id,
            home=home_lineup,
            away=away_lineup,
            game_status=game_status,
        )

    def _is_home_team(self, summary: Dict[str, Any], team_id: str) -> bool:
        """Determine if a team is the home team from game summary."""
        header = summary.get("header", {})
        competitions = header.get("competitions", [{}])
        if not competitions:
            return False

        competitors = competitions[0].get("competitors", [])
        for comp in competitors:
            if str(comp.get("id", "")) == team_id:
                return comp.get("homeAway") == "home"

        return False

    def _parse_player(self, athlete_data: Dict[str, Any]) -> Optional[PlayerLineup]:
        """Parse a player from ESPN athlete data."""
        athlete_info = athlete_data.get("athlete", {})
        if not athlete_info:
            return None

        player_id = str(athlete_info.get("id", ""))
        if not player_id:
            return None

        position_info = athlete_info.get("position", {})

        return PlayerLineup(
            player_id=player_id,
            name=athlete_info.get("displayName", ""),
            jersey=athlete_info.get("jersey"),
            position=position_info.get("displayName") if position_info else None,
            position_abbrev=position_info.get("abbreviation") if position_info else None,
            is_starter=bool(athlete_data.get("starter", False)),
            did_not_play=bool(athlete_data.get("didNotPlay", False)),
            dnp_reason=athlete_data.get("reason"),
            is_ejected=bool(athlete_data.get("ejected", False)),
            is_active=bool(athlete_data.get("active", True)),
        )

    def _parse_team_lineup(self, team_data: Dict[str, Any]) -> TeamLineup:
        """Parse a complete team lineup from ESPN team data."""
        team_info = team_data.get("team", {})
        team_id = str(team_info.get("id", ""))
        team_abbrev = team_info.get("abbreviation", "")
        team_name = team_info.get("displayName", "")

        starters = []
        bench = []
        inactive = []

        statistics = team_data.get("statistics", [])
        if statistics:
            athletes = statistics[0].get("athletes", [])

            for athlete_data in athletes:
                player = self._parse_player(athlete_data)
                if player:
                    if player.did_not_play:
                        inactive.append(player)
                    elif player.is_starter:
                        starters.append(player)
                    else:
                        bench.append(player)

        return TeamLineup(
            team_id=team_id,
            team_abbrev=team_abbrev,
            team_name=team_name,
            starters=starters,
            bench=bench,
            inactive=inactive,
        )

    def sync_game_lineups_to_rosters(
        self,
        game_id: str,
        db=None,
        season: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sync lineup data from ESPN to the rosters collection.

        Fetches live lineup data and updates the rosters collection with:
        - starter: True for starters, False for bench
        - injured: True for players who did not play (with reason)

        Args:
            game_id: ESPN game ID
            db: MongoDB database instance (if None, creates new connection)
            season: Season string (e.g., "2024-2025"). Auto-detected if not provided.

        Returns:
            Dict with sync results:
            {
                "success": bool,
                "game_id": str,
                "home": {"team": str, "updated": int, "starters": int, "bench": int, "inactive": int},
                "away": {"team": str, "updated": int, "starters": int, "bench": int, "inactive": int},
                "error": str (if failed)
            }
        """
        from nba_app.core.mongo import Mongo
        from nba_app.core.utils import get_season_from_date

        # Get database connection
        if db is None:
            db = Mongo().db

        # Check game status first for better error messages
        summary = self._client.get_game_summary(game_id)
        if not summary:
            return {
                "success": False,
                "game_id": game_id,
                "error": "Could not fetch game data from ESPN",
            }

        # Get game status
        header = summary.get("header", {})
        competitions = header.get("competitions", [{}])
        status_info = competitions[0].get("status", {}) if competitions else {}
        game_status = status_info.get("type", {}).get("state", "pre")
        status_detail = status_info.get("type", {}).get("shortDetail", "")

        # Fetch live lineups
        lineups = self.get_game_lineups(game_id)
        if not lineups:
            if game_status == "pre":
                return {
                    "success": False,
                    "game_id": game_id,
                    "game_status": game_status,
                    "error": f"Lineup data not available yet - game is pre-game ({status_detail}). Lineups typically become available shortly before tipoff.",
                }
            return {
                "success": False,
                "game_id": game_id,
                "game_status": game_status,
                "error": "Could not fetch lineup data from ESPN",
            }

        # Get game date for season detection
        games_collection = self.league.collections.get("games", "stats_nba")
        game_doc = db[games_collection].find_one({"game_id": game_id})

        if not game_doc and not season:
            return {
                "success": False,
                "game_id": game_id,
                "error": "Game not found in database and season not provided",
            }

        if not season:
            game_date_str = game_doc.get("date", "")
            try:
                from datetime import datetime as dt
                game_date = dt.strptime(game_date_str[:10], "%Y-%m-%d").date()
                season = get_season_from_date(game_date)
            except Exception as e:
                return {
                    "success": False,
                    "game_id": game_id,
                    "error": f"Could not parse game date: {e}",
                }

        rosters_collection = self.league.collections.get("rosters", "nba_rosters")
        results = {
            "success": True,
            "game_id": game_id,
            "season": season,
            "home": {},
            "away": {},
        }

        # Update both teams
        for team_key, team_lineup in [("home", lineups.home), ("away", lineups.away)]:
            team_abbrev = team_lineup.team_abbrev

            # Find roster document
            roster_doc = db[rosters_collection].find_one({
                "season": season,
                "team": team_abbrev,
            })

            if not roster_doc:
                results[team_key] = {
                    "team": team_abbrev,
                    "updated": 0,
                    "error": f"No roster found for {team_abbrev} in {season}",
                }
                continue

            roster = roster_doc.get("roster", [])
            updated_count = 0

            # Build a map of player_id -> lineup info
            lineup_map = {}
            for player in team_lineup.starters:
                lineup_map[player.player_id] = {"starter": True, "injured": False}
            for player in team_lineup.bench:
                lineup_map[player.player_id] = {"starter": False, "injured": False}
            for player in team_lineup.inactive:
                # Inactive players are marked as injured (or DNP)
                lineup_map[player.player_id] = {
                    "starter": False,
                    "injured": True,
                    "injury_status": player.dnp_reason,
                }

            # Update roster entries
            for roster_entry in roster:
                player_id = str(roster_entry.get("player_id", ""))
                if player_id in lineup_map:
                    info = lineup_map[player_id]
                    roster_entry["starter"] = info["starter"]
                    roster_entry["injured"] = info["injured"]
                    if "injury_status" in info:
                        roster_entry["injury_status"] = info["injury_status"]
                    updated_count += 1

            # Save updated roster
            db[rosters_collection].update_one(
                {"season": season, "team": team_abbrev},
                {
                    "$set": {
                        "roster": roster,
                        "updated_at": datetime.now(timezone.utc),
                        "lineup_sync_game_id": game_id,
                    }
                },
            )

            results[team_key] = {
                "team": team_abbrev,
                "team_name": team_lineup.team_name,
                "updated": updated_count,
                "starters": len(team_lineup.starters),
                "bench": len(team_lineup.bench),
                "inactive": len(team_lineup.inactive),
            }

            logger.info(
                f"Synced {team_abbrev} lineup: {len(team_lineup.starters)} starters, "
                f"{len(team_lineup.bench)} bench, {len(team_lineup.inactive)} inactive"
            )

        return results


    def get_projected_lineups(
        self,
        game_id: str,
        db=None,
        lookback_games: int = 10,
    ) -> Optional[GameLineups]:
        """
        Get projected lineups for a pre-game based on recent starter patterns.

        Uses historical data to identify likely starters:
        1. Queries last N games for each team
        2. Finds players who start most frequently
        3. Cross-references with current injury data
        4. Returns top 5 most frequent starters (excluding injured)

        Args:
            game_id: ESPN game ID
            db: MongoDB database instance (if None, creates new connection)
            lookback_games: Number of recent games to analyze (default: 10)

        Returns:
            GameLineups with projected starters, or None if data unavailable
        """
        from nba_app.core.mongo import Mongo
        from collections import Counter

        if db is None:
            db = Mongo().db

        # Get game info from database
        games_collection = self.league.collections.get("games", "stats_nba")
        player_stats_collection = self.league.collections.get("player_stats", "stats_nba_players")

        game_doc = db[games_collection].find_one({"game_id": game_id})
        if not game_doc:
            logger.warning(f"Game {game_id} not found in database")
            return None

        game_date = game_doc.get("date", "")
        away_abbrev = game_doc.get("awayTeam", {}).get("name", "")
        home_abbrev = game_doc.get("homeTeam", {}).get("name", "")

        if not away_abbrev or not home_abbrev:
            logger.warning(f"Could not determine teams for game {game_id}")
            return None

        # Get injury data from ESPN
        injuries_by_team = {}
        try:
            summary = self._client.get_game_summary(game_id)
            if summary:
                for team_inj in summary.get("injuries", []):
                    team_abbrev = team_inj.get("team", {}).get("abbreviation", "")
                    injured_players = {}
                    for inj in team_inj.get("injuries", []):
                        player_id = str(inj.get("athlete", {}).get("id", ""))
                        status = inj.get("status", "").lower()
                        # OUT and DOUBTFUL are unlikely to play
                        if status in ("out", "doubtful"):
                            injured_players[player_id] = status
                    injuries_by_team[team_abbrev] = injured_players
        except Exception as e:
            logger.warning(f"Could not fetch injury data: {e}")

        def get_projected_starters(team_abbrev: str) -> TeamLineup:
            """Get projected starters for a team based on recent games."""
            # Find recent games for this team
            recent_games = list(db[games_collection].find({
                "date": {"$lt": game_date},
                "$or": [
                    {"homeTeam.name": team_abbrev},
                    {"awayTeam.name": team_abbrev},
                ]
            }).sort("date", -1).limit(lookback_games))

            if not recent_games:
                return TeamLineup(
                    team_id="",
                    team_abbrev=team_abbrev,
                    team_name=team_abbrev,
                    starters=[],
                    bench=[],
                    inactive=[],
                )

            game_ids = [g["game_id"] for g in recent_games]

            # Get player stats for these games
            player_stats = list(db[player_stats_collection].find({
                "game_id": {"$in": game_ids},
                "team": team_abbrev,
                "starter": True,
            }))

            # Count starts per player
            start_counts = Counter()
            player_info = {}  # player_id -> {name, position}
            players_collection = self.league.collections.get("players", "players_nba")

            for ps in player_stats:
                player_id = str(ps.get("player_id", ""))
                if player_id:
                    start_counts[player_id] += 1
                    if player_id not in player_info:
                        # Position data is stored in players collection, not player_stats
                        pos_full = ""
                        pos_abbrev = ""

                        # Look up position from players collection
                        # Try both string and int player_id
                        player_doc = db[players_collection].find_one({"player_id": player_id}) or \
                                     db[players_collection].find_one({"player_id": int(player_id) if player_id.isdigit() else player_id})
                        if player_doc:
                            pos_full = player_doc.get("pos_display_name", "") or player_doc.get("pos_name", "") or player_doc.get("position_name", "")
                            pos_abbrev = player_doc.get("pos_abbreviation", "") or player_doc.get("position", "")

                        # Create abbreviation from full name if not already set
                        if not pos_abbrev and pos_full:
                            pos_abbrev = "".join(word[0] for word in pos_full.split())
                        player_info[player_id] = {
                            "name": ps.get("player_name", ""),
                            "position": pos_full,
                            "position_abbrev": pos_abbrev,
                        }

            # Get injured player IDs for this team
            injured = injuries_by_team.get(team_abbrev, {})

            # Build projected starters (top 5 by start frequency, excluding injured)
            starters = []
            bench = []

            for player_id, count in start_counts.most_common():
                info = player_info.get(player_id, {})
                is_injured = player_id in injured

                player = PlayerLineup(
                    player_id=player_id,
                    name=info.get("name", "Unknown"),
                    position=info.get("position"),
                    position_abbrev=info.get("position_abbrev"),
                    is_starter=not is_injured and len(starters) < 5,
                    did_not_play=is_injured,
                    dnp_reason=injured.get(player_id) if is_injured else None,
                    is_active=not is_injured,
                )

                if is_injured:
                    # Injured players go to inactive (projected)
                    pass  # We'll add them to inactive list
                elif len(starters) < 5:
                    starters.append(player)
                else:
                    bench.append(player)

            # Build inactive list from injured frequent starters
            inactive = []
            for player_id, status in injured.items():
                if player_id in player_info:
                    info = player_info[player_id]
                    inactive.append(PlayerLineup(
                        player_id=player_id,
                        name=info.get("name", "Unknown"),
                        position=info.get("position"),
                        position_abbrev=info.get("position_abbrev"),
                        is_starter=False,
                        did_not_play=True,
                        dnp_reason=status,
                        is_active=False,
                    ))

            return TeamLineup(
                team_id="",
                team_abbrev=team_abbrev,
                team_name=team_abbrev,
                starters=starters,
                bench=bench[:5],  # Limit bench to top 5 non-starters
                inactive=inactive,
            )

        away_lineup = get_projected_starters(away_abbrev)
        home_lineup = get_projected_starters(home_abbrev)

        return GameLineups(
            game_id=game_id,
            home=home_lineup,
            away=away_lineup,
            game_status="projected",
        )


# Convenience function for quick access
def get_game_lineups(
    game_id: str,
    league: str = "nba",
) -> Optional[GameLineups]:
    """
    Fetch lineups for a game.

    Convenience wrapper around LineupService.

    Args:
        game_id: ESPN game ID
        league: League ID (default: "nba")

    Returns:
        GameLineups object or None
    """
    service = LineupService(league)
    return service.get_game_lineups(game_id)


def get_projected_lineups(
    game_id: str,
    league: str = "nba",
    lookback_games: int = 10,
) -> Optional[GameLineups]:
    """
    Get projected lineups for a pre-game.

    Convenience wrapper around LineupService.

    Args:
        game_id: ESPN game ID
        league: League ID (default: "nba")
        lookback_games: Number of recent games to analyze

    Returns:
        GameLineups object with projected starters or None
    """
    service = LineupService(league)
    return service.get_projected_lineups(game_id, lookback_games=lookback_games)


if __name__ == "__main__":
    # Simple test
    import sys

    game_id = sys.argv[1] if len(sys.argv) > 1 else "401705051"
    league = sys.argv[2] if len(sys.argv) > 2 else "nba"

    print(f"Fetching lineups for game {game_id} ({league})...")

    service = LineupService(league)
    lineups = service.get_game_lineups(game_id)

    if lineups:
        print(f"\nGame Status: {lineups.game_status}")

        print(f"\n=== {lineups.away.team_name} (Away) ===")
        print("Starters:")
        for p in lineups.away.starters:
            print(f"  {p.jersey or '--'} {p.name} ({p.position_abbrev or 'N/A'})")
        print("Bench:")
        for p in lineups.away.bench:
            print(f"  {p.jersey or '--'} {p.name} ({p.position_abbrev or 'N/A'})")
        print("Inactive:")
        for p in lineups.away.inactive:
            reason = f" - {p.dnp_reason}" if p.dnp_reason else ""
            print(f"  {p.jersey or '--'} {p.name}{reason}")

        print(f"\n=== {lineups.home.team_name} (Home) ===")
        print("Starters:")
        for p in lineups.home.starters:
            print(f"  {p.jersey or '--'} {p.name} ({p.position_abbrev or 'N/A'})")
        print("Bench:")
        for p in lineups.home.bench:
            print(f"  {p.jersey or '--'} {p.name} ({p.position_abbrev or 'N/A'})")
        print("Inactive:")
        for p in lineups.home.inactive:
            reason = f" - {p.dnp_reason}" if p.dnp_reason else ""
            print(f"  {p.jersey or '--'} {p.name}{reason}")
    else:
        print("Failed to fetch lineups")
