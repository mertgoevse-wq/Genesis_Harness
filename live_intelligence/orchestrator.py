"""Orchestrator for live intelligence connectors."""

from typing import Dict, Any, List

from .base import LiveConnector, ConnectorResult
from .connectors.market_data import MarketDataConnector
from .connectors.saas_trends import SaaSTrendsConnector
from .connectors.github_signals import GitHubSignalsConnector
from .connectors.startup_signals import StartupSignalsConnector


class LiveIntelligenceOrchestrator:
    """Aggregates signals from multiple live intelligence connectors."""

    def __init__(self):
        self.connectors: List[LiveConnector] = [
            MarketDataConnector(),
            SaaSTrendsConnector(),
            GitHubSignalsConnector(),
            StartupSignalsConnector(),
        ]

    def gather(self, query: str, **kwargs) -> Dict[str, Any]:
        """Gather signals from all connectors."""
        signals = {}
        for connector in self.connectors:
            result = connector.fetch(query, **kwargs)
            signals[connector.name] = {
                "data": result.data,
                "confidence": result.confidence,
                "cached": result.cached,
                "fallback": result.fallback,
                "timestamp": result.timestamp,
            }

        return {
            "query": query,
            "signals": signals,
            "sources_used": [c.name for c in self.connectors],
        }

    def get_connector(self, name: str) -> LiveConnector:
        for connector in self.connectors:
            if connector.name == name:
                return connector
        raise ValueError(f"Unknown connector: {name}")
