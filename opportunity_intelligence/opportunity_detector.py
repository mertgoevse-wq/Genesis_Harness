"""Opportunity detector: combines market signals, trends, and competitor gaps."""

from dataclasses import dataclass, field
from typing import List, Dict, Any

from .discovery.market_research_connector import MarketResearchConnector
from .discovery.trend_monitor import TrendMonitor
from .discovery.competitor_analyzer import CompetitorAnalyzer


@dataclass
class Opportunity:
    name: str
    description: str
    score: float  # 0.0 to 100.0
    market_momentum: float
    competition_intensity: str  # 'low', 'medium', 'high'
    confidence: str
    signals: List[str] = field(default_factory=list)


class OpportunityDetector:
    """Discovers and scores SaaS/venture opportunities from a high-level topic."""

    def __init__(self):
        self.market_connector = MarketResearchConnector()
        self.trend_monitor = TrendMonitor()
        self.competitor_analyzer = CompetitorAnalyzer()

    def detect(self, topic: str, limit: int = 5) -> List[Opportunity]:
        """Return a list of scored opportunities for the topic."""
        signals = self.market_connector.fetch_signals(topic)
        trends = self.trend_monitor.detect_trends(topic)
        competitors = self.competitor_analyzer.analyze(topic)
        gaps = self.competitor_analyzer.gap_opportunities(competitors)

        opportunities = []
        for trend in trends[:limit]:
            score = self._score_opportunity(trend, signals, gaps)
            opportunities.append(
                Opportunity(
                    name=f"{trend.name} for {topic}",
                    description=self._describe(trend, gaps),
                    score=score,
                    market_momentum=trend.momentum,
                    competition_intensity=self._competition_level(competitors),
                    confidence=trend.confidence,
                    signals=[s.headline for s in signals],
                )
            )

        return sorted(opportunities, key=lambda o: o.score, reverse=True)

    def _score_opportunity(
        self, trend, signals: List[Any], gaps: List[str]
    ) -> float:
        base = trend.momentum * 100.0
        signal_boost = min(len(signals) * 3.0, 15.0)
        gap_boost = min(len(gaps) * 5.0, 20.0)
        return round(min(base + signal_boost + gap_boost, 100.0), 2)

    def _describe(self, trend, gaps: List[str]) -> str:
        gap_text = (
            " Main gaps: " + ", ".join(gaps) + "."
            if gaps
            else " No clear gaps identified yet."
        )
        return f"{trend.name}.{gap_text}"

    def _competition_level(self, competitors: List[Any]) -> str:
        if not competitors:
            return "unknown"
        dominant = any(c.strength == "dominant" for c in competitors)
        strong = any(c.strength == "strong" for c in competitors)
        if dominant and strong:
            return "high"
        if dominant or strong:
            return "medium"
        return "low"
