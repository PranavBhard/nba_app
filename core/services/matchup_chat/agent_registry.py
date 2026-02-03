from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass(frozen=True)
class AgentSpec:
    name: str
    runner: Callable[..., str]


class AgentRegistry:
    """
    Maps planner workflow `agent` names to callable runners.

    Runners are thin wrappers that return an agent output string (and can
    separately report tool calls to the Controller for UI/debug).
    """

    def __init__(self):
        self._agents: Dict[str, AgentSpec] = {}

    def register(self, name: str, runner: Callable[..., str]) -> None:
        self._agents[name] = AgentSpec(name=name, runner=runner)

    def get(self, name: str) -> Optional[AgentSpec]:
        return self._agents.get(name)

