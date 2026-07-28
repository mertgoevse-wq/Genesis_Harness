"""Tests for the revenue_intelligence subsystem."""

import unittest
from revenue_intelligence.pricing_engine import PricingEngine
from revenue_intelligence.subscription_models import SubscriptionModelSelector
from revenue_intelligence.acquisition_strategy import AcquisitionStrategy
from revenue_intelligence.growth_experiment_engine import GrowthExperimentEngine


class TestRevenueIntelligence(unittest.TestCase):
    def test_pricing_engine_recommend(self):
        engine = PricingEngine()
        result = engine.recommend({"base_price": 12.0})
        self.assertIn("tiers", result)
        self.assertIn("recommended_tier", result)
        self.assertEqual(len(result["tiers"]), 3)

    def test_subscription_selector(self):
        selector = SubscriptionModelSelector()
        result = selector.recommend({"product_type": "api"})
        self.assertEqual(result["recommended_model"], "usage_based")

    def test_acquisition_strategy(self):
        strategy = AcquisitionStrategy()
        result = strategy.recommend({"budget": "low"})
        self.assertIn("primary_channels", result)
        self.assertIn("tactics", result)

    def test_growth_experiments(self):
        engine = GrowthExperimentEngine()
        result = engine.recommend({})
        self.assertIn("experiments", result)
        self.assertGreater(len(result["experiments"]), 0)


if __name__ == "__main__":
    unittest.main()
