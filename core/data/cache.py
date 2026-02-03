"""
Cache Repositories - Data access for cached/precomputed data.

Handles:
- cached_league_stats: Precomputed league-level statistics for PER calculation
- nba_cached_elo_ratings: Cached Elo ratings per team/date/season
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from .base import BaseRepository

if TYPE_CHECKING:
    from nba_app.core.league_config import LeagueConfig


class LeagueStatsCache(BaseRepository):
    """Repository for cached_league_stats collection."""

    collection_name = 'cached_league_stats'

    def __init__(
        self,
        db,
        league: Optional["LeagueConfig"] = None,
        collection_name: Optional[str] = None,
    ):
        effective = collection_name
        if league is not None:
            effective = effective or league.collections["cached_league_stats"]
        super().__init__(db, collection_name=effective)

    # --- Query Methods ---

    def find_by_season(self, season: str) -> Optional[Dict]:
        """Get cached league stats for a season."""
        return self.find_one({'season': season})

    def find_all_seasons(self) -> List[Dict]:
        """Get cached stats for all seasons."""
        return self.find({}, sort=[('season', -1)])

    def get_cached_seasons(self) -> List[str]:
        """Get list of seasons that have cached stats."""
        return self.distinct('season')

    def get_league_constants(self, season: str) -> Optional[Dict]:
        """Get league constants (factor, VOP, DRB%) for a season."""
        doc = self.find_by_season(season)
        if doc and 'league_constants' in doc:
            return doc['league_constants']
        return None

    def get_team_pace(self, season: str, team: str) -> Optional[float]:
        """Get average pace for a team in a season."""
        doc = self.find_by_season(season)
        if doc and 'team_pace' in doc:
            return doc['team_pace'].get(team)
        return None

    def get_league_pace(self, season: str) -> Optional[float]:
        """Get league average pace for a season."""
        doc = self.find_by_season(season)
        if doc:
            return doc.get('lg_pace')
        return None

    # --- Update Methods ---

    def upsert_season_stats(
        self,
        season: str,
        league_totals: Dict,
        league_constants: Dict,
        lg_pace: float,
        team_pace: Dict[str, float],
        team_games: Dict[str, int]
    ) -> bool:
        """Insert or update cached stats for a season."""
        result = self.update_one(
            {'season': season},
            {'$set': {
                'season': season,
                'league_totals': league_totals,
                'league_constants': league_constants,
                'lg_pace': lg_pace,
                'team_pace': team_pace,
                'team_games': team_games,
                'computed_at': datetime.utcnow()
            }},
            upsert=True
        )
        return result.acknowledged

    def delete_season(self, season: str) -> bool:
        """Delete cached stats for a season."""
        result = self.delete_one({'season': season})
        return result.deleted_count > 0

    def clear_all(self) -> int:
        """Clear all cached stats. Returns number of docs deleted."""
        result = self.delete_many({})
        return result.deleted_count


class EloRatingsCache(BaseRepository):
    """Repository for nba_cached_elo_ratings collection."""

    collection_name = 'nba_cached_elo_ratings'

    def __init__(
        self,
        db,
        league: Optional["LeagueConfig"] = None,
        collection_name: Optional[str] = None,
    ):
        effective = collection_name
        if league is not None:
            effective = effective or league.collections["elo_cache"]
        super().__init__(db, collection_name=effective)
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Create required indexes if they don't exist."""
        # Unique compound index for lookups
        self._collection.create_index(
            [("team", ASCENDING), ("game_date", ASCENDING), ("season", ASCENDING)],
            unique=True,
            name="team_date_season_unique"
        )
        # Index for season-based queries
        self._collection.create_index(
            [("season", ASCENDING)],
            name="season_idx"
        )
        # Index for finding latest ratings
        self._collection.create_index(
            [("game_date", DESCENDING)],
            name="game_date_desc_idx"
        )

    # --- Query Methods ---

    def get_elo(
        self,
        team: str,
        game_date: str,
        season: str
    ) -> Optional[float]:
        """Get Elo rating for a team on a specific date."""
        doc = self.find_one({
            'team': team,
            'game_date': game_date,
            'season': season
        })
        return doc.get('elo') if doc else None

    def get_latest_elo(self, team: str, season: str) -> Optional[Dict]:
        """Get most recent Elo rating for a team in a season."""
        results = self.find(
            {'team': team, 'season': season},
            sort=[('game_date', DESCENDING)],
            limit=1
        )
        return results[0] if results else None

    def get_elos_before_date(
        self,
        team: str,
        game_date: str,
        season: str
    ) -> Optional[Dict]:
        """Get the most recent Elo rating for a team before a date."""
        results = self.find(
            {'team': team, 'season': season, 'game_date': {'$lt': game_date}},
            sort=[('game_date', DESCENDING)],
            limit=1
        )
        return results[0] if results else None

    def get_all_teams_elo(
        self,
        game_date: str,
        season: str
    ) -> Dict[str, float]:
        """Get Elo ratings for all teams on a specific date."""
        results = self.find({'game_date': game_date, 'season': season})
        return {doc['team']: doc['elo'] for doc in results}

    def get_season_elos(self, season: str) -> List[Dict]:
        """Get all Elo ratings for a season."""
        return self.find({'season': season}, sort=[('game_date', 1), ('team', 1)])

    def get_cached_seasons(self) -> List[str]:
        """Get list of seasons with cached Elo ratings."""
        return sorted(self.distinct('season'), reverse=True)

    def get_cached_dates(self, season: str) -> List[str]:
        """Get list of dates with cached ratings for a season."""
        return sorted(self.distinct('game_date', {'season': season}))

    # --- Update Methods ---

    def upsert_elo(
        self,
        team: str,
        game_date: str,
        season: str,
        elo: float
    ) -> bool:
        """Insert or update an Elo rating."""
        result = self.update_one(
            {'team': team, 'game_date': game_date, 'season': season},
            {'$set': {
                'team': team,
                'game_date': game_date,
                'season': season,
                'elo': elo,
                'created_at': datetime.utcnow()
            }},
            upsert=True
        )
        return result.acknowledged

    def bulk_upsert_elos(self, elo_records: List[Dict]) -> int:
        """
        Bulk upsert Elo ratings.

        Args:
            elo_records: List of dicts with keys: team, game_date, season, elo

        Returns:
            Number of records processed
        """
        if not elo_records:
            return 0

        from pymongo import UpdateOne
        operations = []
        for record in elo_records:
            operations.append(UpdateOne(
                {
                    'team': record['team'],
                    'game_date': record['game_date'],
                    'season': record['season']
                },
                {'$set': {
                    'team': record['team'],
                    'game_date': record['game_date'],
                    'season': record['season'],
                    'elo': record['elo'],
                    'created_at': datetime.utcnow()
                }},
                upsert=True
            ))

        if operations:
            result = self._collection.bulk_write(operations, ordered=False)
            return result.upserted_count + result.modified_count
        return 0

    def delete_season(self, season: str) -> int:
        """Delete all cached Elo ratings for a season."""
        result = self.delete_many({'season': season})
        return result.deleted_count

    def clear_all(self) -> int:
        """Clear all cached Elo ratings."""
        result = self.delete_many({})
        return result.deleted_count

    # --- Utility Methods ---

    def has_elo(self, team: str, game_date: str, season: str) -> bool:
        """Check if Elo rating exists for this team/date/season."""
        return self.exists({
            'team': team,
            'game_date': game_date,
            'season': season
        })

    def count_by_season(self, season: str) -> int:
        """Count cached ratings for a season."""
        return self.count({'season': season})
