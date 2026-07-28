"""GitHub ecosystem signals connector."""

from datetime import datetime, timezone

from genesis.intelligence.connectors.base import ConnectorResult, LiveConnector


class GitHubSignalsConnector(LiveConnector):
    """Connector for GitHub open-source activity signals."""

    def __init__(self, **kwargs):
        super().__init__(name="github_signals", **kwargs)

    def _fetch_live(self, query: str, **kwargs):
        raise NotImplementedError("Live GitHub API not configured.")

    def _fallback(self, query: str, **kwargs):
        return ConnectorResult(
            source=self.name,
            data={
                "topic": query,
                "repos_created_30d": 12,
                "top_languages": ["Python", "TypeScript", "JavaScript"],
                "activity_score": 68.0,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
            confidence="ASSUMED",
        )
