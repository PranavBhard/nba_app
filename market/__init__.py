"""
DEPRECATED: Market functionality has moved to core/market/

This module provides backwards compatibility imports.
New code should import from nba_app.core.market instead.
"""

import warnings

warnings.warn(
    "nba_app.market is deprecated. Use nba_app.core.market instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location for backwards compatibility
from nba_app.core.market import MarketConnector, KalshiPublicClient, get_game_market_data

__all__ = ["MarketConnector", "KalshiPublicClient", "get_game_market_data"]
