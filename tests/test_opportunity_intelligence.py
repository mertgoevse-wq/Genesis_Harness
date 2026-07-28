"""Tests for the opportunity_intelligence subsystem."""

import unittest
from opportunity_intelligence.opportunity_detector import OpportunityDetector
from opportunity_intelligence.discovery.trend_monitor import TrendMonitor
from opportunity_intelligence.discovery.competitor_analyzer import CompetitorAnalyzer
from opportunity_intelligence.discovery.market_research_connector import MarketResearchConnector


class TestOpportunityIntelligence(unittest.TestCase):
    def setUp(self):
        self.detector = OpportunityDetector()

    def test_detect_returns_opportunities(self):
        opportunities = self.detector.detect("healthcare ai")
        self.assertIsInstance(opportunities, list)
        self.assertGreater(len(opportunities), 0)
        first = opportunities[0]
        self.assertIn("score", dir(first))
        self.assertGreaterEqual(first.score, 0.0)
        self.assertLessEqual(first.score, 100.0)

    def test_trend_monitor_returns_trends(self):
        trends = TrendMonitor().detect_trends("fintech")
        self.assertIsInstance(trends, list)
        self.assertGreater(len(trends), 0)

    def test_competitor_analyzer_returns_landscape(self):
        analyzer = CompetitorAnalyzer()
        competitors = analyzer.analyze("fintech")
        self.assertIsInstance(competitors, list)
        self.assertGreater(len(competitors), 0)
        gaps = analyzer.gap_opportunities(competitors)
        self.assertIsInstance(gaps, list)

    def test_market_research_connector_signals(self):
        connector = MarketResearchConnector()
        signals = connector.fetch_signals("fintech", limit=5)
        self.assertIsInstance(signals, list)
        self.assertLessEqual(len(signals), 5)


if __name__ == "__main__":
    unittest.main()
