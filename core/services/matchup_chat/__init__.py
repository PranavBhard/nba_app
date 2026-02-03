"""
Matchup Chat Service (core layer)

Single Source of Truth for the multi-agent matchup chat orchestration and
shared-context persistence.

Consumer layers (web/agents/cli) should call into this package rather than
re-implementing workflow logic.
"""

from .controller import Controller  # noqa: F401

