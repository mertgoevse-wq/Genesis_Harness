"""Tests for genesis.decision."""

import unittest

from genesis.decision import (
    ProductValidationEngine,
    ValidationScorer,
    VentureDecisionEngine,
)


class TestVentureDecisionEngine(unittest.TestCase):
    def test_evaluate_returns_decision(self) -> None:
        engine = VentureDecisionEngine()
        decision = engine.evaluate(
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
        self.assertIn(decision.verdict, {"GO", "NO-GO", "MAYBE"})
        self.assertGreaterEqual(decision.overall_score, 0.0)
        self.assertLessEqual(decision.overall_score, 100.0)

    def test_verdict_no_go_for_low_score(self) -> None:
        engine = VentureDecisionEngine()
        decision = engine.evaluate(
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


class TestProductValidationEngine(unittest.TestCase):
    def test_evaluate_returns_verdict(self) -> None:
        engine = ProductValidationEngine()
        result = engine.evaluate(
            "AI note assistant",
            context={
                "demand_score": 80.0,
                "incumbent_count": 3,
                "differentiation_score": 70.0,
                "monetization_score": 80.0,
                "pain_score": 80.0,
                "urgency_score": 75.0,
                "technical_complexity": 4,
                "technical_readiness": 6,
                "marketing_budget": "medium",
                "available_channels": 3,
                "tam_billions": 1.0,
                "average_price": 29.0,
                "conversion_rate": 0.02,
            },
        )
        self.assertIn(result.verdict, {"GO", "MODIFY", "REJECT"})
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)


class TestValidationScorer(unittest.TestCase):
    def test_scores_are_bounded(self) -> None:
        scorer = ValidationScorer()
        context = {
            "demand_score": 110.0,
            "incumbent_count": 20,
            "differentiation_score": 50.0,
            "pain_score": 80.0,
            "urgency_score": 90.0,
            "technical_complexity": 2,
            "technical_readiness": 5,
            "marketing_budget": "high",
            "available_channels": 10,
            "tam_billions": 5.0,
            "average_price": 50.0,
            "conversion_rate": 0.05,
        }
        self.assertEqual(scorer.score_market_demand(context), 100.0)
        self.assertGreaterEqual(scorer.score_competition(context), 0.0)
        self.assertLessEqual(scorer.score_competition(context), 100.0)
