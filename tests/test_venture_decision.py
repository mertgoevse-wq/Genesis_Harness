"""Tests for the venture_decision subsystem."""

import unittest
from venture_decision.decision_engine import VentureDecisionEngine


class TestVentureDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = VentureDecisionEngine()

    def test_evaluate_returns_decision(self):
        decision = self.engine.evaluate(
            "AI compliance assistant",
            context={
                "tam_billions": 5.0,
                "growth_rate": 0.25,
                "monetization_score": 80.0,
                "incumbent_count": 2,
                "differentiation_score": 75.0,
                "technical_complexity": 4,
                "technical_readiness": 7,
                "risk_scores": {
                    "market_risk": 4.0,
                    "technical_risk": 3.0,
                    "regulatory_risk": 6.0,
                    "team_risk": 4.0,
                    "competition_risk": 5.0,
                },
            },
        )
        self.assertIn(decision.verdict, ["GO", "NO-GO", "MAYBE"])
        self.assertGreaterEqual(decision.overall_score, 0.0)
        self.assertLessEqual(decision.overall_score, 100.0)
        self.assertGreaterEqual(decision.market_score, 0.0)
        self.assertGreaterEqual(decision.technical_score, 0.0)

    def test_verdict_no_go_for_low_score(self):
        decision = self.engine.evaluate(
            "bad idea",
            context={
                "tam_billions": 0.01,
                "growth_rate": 0.0,
                "monetization_score": 0.0,
                "incumbent_count": 10,
                "differentiation_score": 0.0,
                "technical_complexity": 9,
                "technical_readiness": 1,
                "risk_scores": {
                    "market_risk": 9.0,
                    "technical_risk": 9.0,
                    "regulatory_risk": 9.0,
                    "team_risk": 9.0,
                    "competition_risk": 9.0,
                },
            },
        )
        self.assertEqual(decision.verdict, "NO-GO")


if __name__ == "__main__":
    unittest.main()
