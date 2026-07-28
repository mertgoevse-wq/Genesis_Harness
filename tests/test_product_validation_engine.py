"""Tests for product validation engine."""

import unittest

from product_validation_engine.validation_engine import ProductValidationEngine


class TestProductValidationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ProductValidationEngine()

    def _context(self, **overrides):
        defaults = {
            "demand_score": 80.0,
            "incumbent_count": 2,
            "differentiation_score": 75.0,
            "monetization_score": 80.0,
            "pain_score": 85.0,
            "urgency_score": 80.0,
            "technical_complexity": 3,
            "technical_readiness": 7,
            "marketing_budget": "medium",
            "available_channels": 4,
            "tam_billions": 2.5,
            "average_price": 29.0,
            "conversion_rate": 0.02,
        }
        defaults.update(overrides)
        return defaults

    def test_go_verdict(self):
        decision = self.engine.evaluate("AI note-taking assistant", self._context())
        self.assertEqual(decision.verdict, "GO")
        self.assertGreaterEqual(decision.confidence, 0.0)
        self.assertGreaterEqual(decision.overall_score, 0.0)
        self.assertGreater(len(decision.reasoning), 0)

    def test_reject_verdict(self):
        context = self._context(
            demand_score=10.0,
            differentiation_score=10.0,
            monetization_score=10.0,
            pain_score=10.0,
            urgency_score=10.0,
        )
        decision = self.engine.evaluate("Weak idea", context)
        self.assertEqual(decision.verdict, "REJECT")

    def test_modify_verdict(self):
        context = self._context(
            demand_score=55.0,
            differentiation_score=55.0,
            monetization_score=55.0,
        )
        decision = self.engine.evaluate("Maybe idea", context)
        self.assertIn(decision.verdict, ("GO", "MODIFY", "REJECT"))


if __name__ == "__main__":
    unittest.main()
