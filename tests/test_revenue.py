"""Tests for genesis.revenue."""

import unittest

from genesis.revenue import (
    AcquisitionStrategy,
    GrowthExperimentEngine,
    PricingEngine,
    SubscriptionModelSelector,
)


class TestRevenue(unittest.TestCase):
    def test_pricing_engine_recommend(self) -> None:
        engine = PricingEngine()
        result = engine.recommend({"base_price": 12.0})
        self.assertIn("tiers", result)
        self.assertIn("recommended_tier", result)
        self.assertEqual(len(result["tiers"]), 3)

    def test_subscription_selector(self) -> None:
        selector = SubscriptionModelSelector()
        result = selector.recommend({"product_type": "api"})
        self.assertEqual(result["recommended_model"], "usage_based")

    def test_acquisition_strategy(self) -> None:
        strategy = AcquisitionStrategy()
        result = strategy.recommend({"budget": "low"})
        self.assertIn("primary_channels", result)
        self.assertIn("tactics", result)

    def test_growth_experiments(self) -> None:
        engine = GrowthExperimentEngine()
        result = engine.recommend({})
        self.assertIn("experiments", result)
        self.assertGreater(len(result["experiments"]), 0)
