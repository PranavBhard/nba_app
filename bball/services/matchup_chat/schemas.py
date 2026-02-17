from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional, TypedDict


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ToolCall(TypedDict):
    name: str
    args: Dict[str, Any]
    output: Any


class HistoryEntry(TypedDict, total=False):
    agent: str
    system: str
    messages: List[Dict[str, Any]]
    tools: List[ToolCall]
    output: Any
    timestamp: str


class LatestPointer(TypedDict, total=False):
    history_idx: int
    timestamp: str
    short_summary: str


class SharedGameSide(TypedDict, total=False):
    name: str  # abbreviation (e.g. "MIL")
    full_name: str  # teams collection displayName
    team_id: str


class SharedGame(TypedDict, total=False):
    away: SharedGameSide
    home: SharedGameSide
    date: str  # YYYY-MM-DD


class EnsembleModelContext(TypedDict, total=False):
    p_home: float
    # NOTE: We intentionally do NOT persist large model artifacts in shared context.
    # Model Inspector retrieves prediction artifacts via tools (SSoT is model predictions collection).


class SharedContext(TypedDict, total=False):
    game_id: str
    game: SharedGame
    ensemble_model: EnsembleModelContext
    market_snapshot: Dict[str, Any]
    history: List[HistoryEntry]
    latest_by_agent: Dict[str, LatestPointer]


class AgentAction(TypedDict, total=False):
    kind: Literal["agent_output", "tool_call"]
    agent: str
    timestamp: str
    # tool_call only
    name: str
    args: Any
    output: Any
    # agent_output only
    text: str


class TurnPlanStep(TypedDict):
    agent: str
    instruction: str


class TurnPlan(TypedDict, total=False):
    narrative: str
    workflow: List[TurnPlanStep]
    final_synthesis_instructions: str


@dataclass(frozen=True)
class ControllerOptions:
    force_web_refresh: bool = False
    show_agent_actions: bool = False

