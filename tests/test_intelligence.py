"""Tests for genesis.intelligence."""

import unittest

from genesis.intelligence import (
    CompetitorAnalyzer,
    LiveIntelligenceOrchestrator,
    MarketResearchConnector,
    OpportunityDetector,
    TrendMonitor,
)


class TestOpportunityDetector(unittest.TestCase):
    def test_detect_returns_opportunities(self) -> None:
        detector = OpportunityDetector()
        opportunities = detector.detect("healthcare ai")
        self.assertIsInstance(opportunities, list)
        self.assertGreater(len(opportunities), 0)
        first = opportunities[0]
        self.assertGreaterEqual(first.score, 0.0)
        self.assertLessEqual(first.score, 100.0)

    def test_trend_monitor_returns_trends(self) -> None:
        trends = TrendMonitor().detect_trends("fintech")
        self.assertIsInstance(trends, list)
        self.assertGreater(len(trends), 0)

    def test_competitor_analyzer_returns_landscape(self) -> None:
        analyzer = CompetitorAnalyzer()
        competitors = analyzer.analyze("fintech")
        self.assertIsInstance(competitors, list)
        self.assertGreater(len(competitors), 0)
        gaps = analyzer.gap_opportunities(competitors)
        self.assertIsInstance(gaps, list)

    def test_market_research_connector_signals(self) -> None:
        connector = MarketResearchConnector()
        signals = connector.fetch_signals("fintech", limit=5)
        self.assertIsInstance(signals, list)
        self.assertLessEqual(len(signals), 5)


class TestLiveIntelligenceOrchestrator(unittest.TestCase):
    def test_gather_returns_signals(self) -> None:
        orchestrator = LiveIntelligenceOrchestrator()
        result = orchestrator.gather("test")
        self.assertIn("signals", result)
        self.assertEqual(len(result["signals"]), 4)
