"""Tests for growth_intelligence subsystem."""

import unittest

from growth_intelligence.growth_engine import GrowthEngine


class TestGrowthEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GrowthEngine()

    def test_recommend_returns_strategy(self):
        result = self.engine.recommend(
            "AI Note Assistant",
            {
                "target_audience": "small businesses",
                "marketing_budget": "medium",
                "available_channels": 4,
            },
        )
        self.assertEqual(result["product"], "AI Note Assistant")
        self.assertIn("landing_page", result)
        self.assertIn("seo", result)
        self.assertIn("acquisition_channels", result)
        self.assertIn("experiments", result)
        self.assertIn("recommendations", result)
        self.assertGreaterEqual(result["landing_page"]["score"], 0.0)
        self.assertGreaterEqual(result["seo"]["score"], 0.0)

    def test_low_budget_channels(self):
        result = self.engine.recommend(
            "Budget Tool",
            {
                "target_audience": "startups",
                "marketing_budget": "low",
                "available_channels": 1,
            },
        )
        channels = result["acquisition_channels"]
        self.assertTrue(any("organic" in c.lower() for c in channels))


if __name__ == "__main__":
    unittest.main()
