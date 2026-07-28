"""Opportunity discovery components."""

from .market_research_connector import MarketResearchConnector, MarketSignal
from .trend_monitor import TrendMonitor, Trend
from .competitor_analyzer import CompetitorAnalyzer, Competitor

__all__ = [
    "MarketResearchConnector",
    "MarketSignal",
    "TrendMonitor",
    "Trend",
    "CompetitorAnalyzer",
    "Competitor",
]
