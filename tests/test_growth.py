"""Tests for genesis.growth."""

import unittest

from genesis.growth import (
    ChannelAnalyzer,
    CustomerIntelligenceEngine,
    GrowthEngine,
    GrowthLoops,
    SEOOpportunityEngine,
    ValidationLoop,
)


class TestGrowth(unittest.TestCase):
    def test_growth_engine_recommend(self) -> None:
        engine = GrowthEngine()
        result = engine.recommend("AI Tool", {"target_audience": "startups"})
        self.assertIn("landing_page", result)
        self.assertIn("seo", result)
        self.assertIn("acquisition_channels", result)

    def test_channel_analyzer(self) -> None:
        analyzer = ChannelAnalyzer()
        result = analyzer.analyze("AI Tool", {"marketing_budget": "medium", "target_audience": "startups"})
        self.assertIn("channels", result)
        self.assertGreater(len(result["channels"]), 0)

    def test_seo_opportunity_engine(self) -> None:
        engine = SEOOpportunityEngine()
        result = engine.analyze("AI Tool", {"target_audience": "startups"})
        self.assertIn("keywords", result)
        self.assertIn("content_pillars", result)

    def test_growth_loops(self) -> None:
        loops = GrowthLoops()
        result = loops.design("AI Tool", {})
        self.assertIn("loops", result)
        self.assertGreater(len(result["loops"]), 0)

    def test_customer_intelligence(self) -> None:
        engine = CustomerIntelligenceEngine()
        result = engine.analyze("AI assistant", {"target_audience": "lawyers"})
        self.assertIn("personas", result)
        self.assertIn("icp", result)

    def test_validation_loop(self) -> None:
        loop = ValidationLoop()
        result = loop.run(
            "AI note assistant",
            {
                "demand_score": 80.0,
                "differentiation_score": 75.0,
                "monetization_score": 80.0,
                "average_price": 29.0,
                "willingness_to_pay": 60.0,
            },
        )
        self.assertIn(result["verdict"], {"BUILD", "PIVOT/REFINE", "ABANDON"})
