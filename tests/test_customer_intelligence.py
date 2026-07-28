"""Tests for customer_intelligence subsystem."""

import unittest

from customer_intelligence.customer_intelligence_engine import CustomerIntelligenceEngine


class TestCustomerIntelligenceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CustomerIntelligenceEngine()

    def test_analyze_returns_personas(self):
        result = self.engine.analyze(
            "AI note-taking assistant",
            {"target_audience": "lawyers", "industry": "Legal"},
        )
        self.assertEqual(result["idea"], "AI note-taking assistant")
        self.assertGreater(len(result["personas"]), 0)
        self.assertIn("icp", result)
        self.assertIn("pain_points", result)
        self.assertIn("objections", result)
        self.assertIn("buying_signals", result)
        self.assertIn("interview_script", result)

    def test_discover_icp(self):
        icp = self.engine.discover_icp("tool", {"pain_score": 80.0, "willingness_to_pay": 70.0, "budget_score": 75.0})
        self.assertGreater(icp.fit_score, 0.0)


if __name__ == "__main__":
    unittest.main()
