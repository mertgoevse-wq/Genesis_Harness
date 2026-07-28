"""Live Intelligence subsystem.

Provides modular data connectors for market data, SaaS trends, competitor
monitoring, technology trends, GitHub ecosystem signals, and startup signals.

Each connector implements a common base class with caching and fallback mode.
"""

from .base import LiveConnector, ConnectorResult
from .orchestrator import LiveIntelligenceOrchestrator

__all__ = [
    "LiveConnector",
    "ConnectorResult",
    "LiveIntelligenceOrchestrator",
]
