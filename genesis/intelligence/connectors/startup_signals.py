"""Startup signal connector for live intelligence."""

from datetime import datetime, timezone

from genesis.intelligence.connectors.base import ConnectorResult, LiveConnector


class StartupSignalsConnector(LiveConnector):
    """Connector for startup ecosystem signals (funding, launches)."""

    def __init__(self, **kwargs):
        super().__init__(name="startup_signals", **kwargs)

    def _fetch_live(self, query: str, **kwargs):
        raise NotImplementedError("Live startup signal API not configured.")

    def _fallback(self, query: str, **kwargs):
        return ConnectorResult(
            source=self.name,
            data={
                "topic": query,
                "recent_funding_rounds": 3,
                "avg_seed_round_m": 1.8,
                "signal_strength": 0.62,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
            confidence="ASSUMED",
        )
