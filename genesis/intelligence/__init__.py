"""Intelligence subsystem for Genesis."""
from .connectors.base import ConnectorResult as ConnectorResult
from .connectors.base import LiveConnector as LiveConnector
from .connectors.orchestrator import LiveIntelligenceOrchestrator as LiveIntelligenceOrchestrator
from .discovery.competitors import Competitor as Competitor
from .discovery.competitors import CompetitorAnalyzer as CompetitorAnalyzer
from .discovery.market_research import MarketResearchConnector as MarketResearchConnector
from .discovery.market_research import MarketSignal as MarketSignal
from .discovery.trends import Trend as Trend
from .discovery.trends import TrendMonitor as TrendMonitor
from .opportunity import Opportunity as Opportunity
from .opportunity import OpportunityDetector as OpportunityDetector

__all__ = [
    "ConnectorResult",
    "LiveConnector",
    "LiveIntelligenceOrchestrator",
    "Competitor",
    "CompetitorAnalyzer",
    "MarketResearchConnector",
    "MarketSignal",
    "Trend",
    "TrendMonitor",
    "Opportunity",
    "OpportunityDetector",
]
