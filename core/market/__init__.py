"""
Market data integration for prediction markets (Kalshi, etc.)

This module provides:
- KalshiPublicClient: Unauthenticated client for reading market data
- MarketConnector: Authenticated client for trading (requires API keys)
- get_game_market_data(): High-level function to get market data for a game
"""

from .kalshi import KalshiPublicClient, get_game_market_data, build_event_ticker
from .connector import MarketConnector

__all__ = [
    "KalshiPublicClient",
    "MarketConnector",
    "get_game_market_data",
    "build_event_ticker",
]
