"""Tests for growth intelligence enhancements."""

import unittest

from growth_intelligence.channel_analyzer import ChannelAnalyzer
from growth_intelligence.seo_opportunity_engine import SEOOpportunityEngine
from growth_intelligence.growth_loops import GrowthLoops


class TestChannelAnalyzer(unittest.TestCase):
    def test_analyze_returns_channels(self):
        analyzer = ChannelAnalyzer()
        result = analyzer.analyze("AI Tool", {"marketing_budget": "medium", "target_audience": "startups"})
        self.assertIn("channels", result)
        self.assertIn("recommended_mix", result)
        self.assertGreater(len(result["channels"]), 0)


class TestSEOOpportunityEngine(unittest.TestCase):
    def test_analyze_returns_opportunities(self):
        engine = SEOOpportunityEngine()
        result = engine.analyze("AI Tool", {"target_audience": "startups"})
        self.assertIn("keywords", result)
        self.assertIn("content_pillars", result)
        self.assertIn("competitor_gaps", result)


class TestGrowthLoops(unittest.TestCase):
    def test_design_returns_loops(self):
        loops = GrowthLoops()
        result = loops.design("AI Tool", {})
        self.assertIn("loops", result)
        self.assertIn("conversion_experiments", result)
        self.assertGreater(len(result["loops"]), 0)


if __name__ == "__main__":
    unittest.main()
