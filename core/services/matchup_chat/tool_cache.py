from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, Optional


def _json_safe(obj: Any) -> Any:
    """
    Ensure values are Mongo/JSON-serializable (best-effort).
    """
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)


class ToolCache:
    """
    Mongo-backed tool result cache keyed by (game_id, tool_name, args_hash).

    Designed for agent DB tools that are frequently repeated within a matchup session
    (e.g. get_team_games, get_player_stats). Uses a TTL index on expires_at.
    """

    def __init__(self, *, db, league_id: str = "nba", ttl_s: int = 60 * 60 * 12):
        self.db = db
        self.league_id = (league_id or "nba").lower()
        self.ttl_s = int(ttl_s)
        # Bump this when cached tool output semantics change.
        self.cache_schema_version = 2
        self.coll_name = f"{self.league_id}_agent_tool_cache"
        self.coll = self.db[self.coll_name]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        try:
            # Unique identity per tool call within a game
            self.coll.create_index(
                [("game_id", 1), ("tool", 1), ("args_hash", 1)],
                unique=True,
                name="game_tool_args_unique",
            )
            # TTL expiration
            self.coll.create_index(
                [("expires_at", 1)],
                expireAfterSeconds=0,
                name="expires_at_ttl",
            )
        except Exception:
            # If index creation fails (permissions, etc.), cache still works best-effort.
            pass

    @staticmethod
    def _hash_args(args: Dict[str, Any], *, cache_schema_version: int = 1) -> str:
        payload = {"_v": int(cache_schema_version), "args": _json_safe(args or {})}
        s = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def get(self, *, game_id: str, tool: str, args: Dict[str, Any]) -> Optional[Any]:
        now = time.time()
        args_hash = self._hash_args(args, cache_schema_version=self.cache_schema_version)
        try:
            doc = self.coll.find_one({"game_id": str(game_id), "tool": str(tool), "args_hash": args_hash})
        except Exception:
            doc = None
        if not doc:
            return None
        try:
            expires_at = float(doc.get("expires_at") or 0)
        except Exception:
            expires_at = 0
        if expires_at and expires_at < now:
            return None
        return doc.get("output")

    def set(self, *, game_id: str, tool: str, args: Dict[str, Any], output: Any) -> None:
        now = time.time()
        args_hash = self._hash_args(args, cache_schema_version=self.cache_schema_version)
        doc = {
            "game_id": str(game_id),
            "tool": str(tool),
            "args_hash": args_hash,
            "cache_schema_version": self.cache_schema_version,
            "args": _json_safe(args or {}),
            "output": _json_safe(output),
            "created_at": now,
            "expires_at": now + float(self.ttl_s),
        }
        try:
            self.coll.update_one(
                {"game_id": doc["game_id"], "tool": doc["tool"], "args_hash": doc["args_hash"]},
                {"$set": doc},
                upsert=True,
            )
        except Exception:
            # Best-effort: cache miss is acceptable.
            return

