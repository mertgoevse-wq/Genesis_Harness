"""Genesis Opportunity Intelligence subsystem.

Discovers market opportunities, technology trends, and SaaS venture candidates
through lightweight research connectors and scoring heuristics.
"""

from .opportunity_detector import OpportunityDetector
from .discovery.trend_monitor import TrendMonitor
from .discovery.competitor_analyzer import CompetitorAnalyzer
from .discovery.market_research_connector import MarketResearchConnector

__all__ = [
    "OpportunityDetector",
    "TrendMonitor",
    "CompetitorAnalyzer",
    "MarketResearchConnector",
]
