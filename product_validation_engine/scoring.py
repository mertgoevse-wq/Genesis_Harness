"""Scoring utilities for product validation."""

from typing import Dict, Any


class ValidationScorer:
    """Scores individual validation dimensions for a product idea."""

    def score_market_demand(self, context: Dict[str, Any]) -> float:
        demand = context.get("demand_score", 50.0)
        return min(max(demand, 0.0), 100.0)

    def score_competition(self, context: Dict[str, Any]) -> float:
        incumbent_count = context.get("incumbent_count", 3)
        differentiation = context.get("differentiation_score", 50.0)
        penalty = max(0, (incumbent_count - 1) * 5.0)
        return min(max(differentiation - penalty, 0.0), 100.0)

    def score_pricing_potential(self, context: Dict[str, Any]) -> float:
        return min(max(context.get("monetization_score", 50.0), 0.0), 100.0)

    def score_customer_pain(self, context: Dict[str, Any]) -> float:
        pain = context.get("pain_score", 50.0)
        urgency = context.get("urgency_score", 50.0)
        return min(max((pain + urgency) / 2.0, 0.0), 100.0)

    def score_implementation_complexity(self, context: Dict[str, Any]) -> float:
        complexity = context.get("technical_complexity", 5)
        readiness = context.get("technical_readiness", 5)
        complexity_penalty = max(0, (complexity - 3) * 5.0)
        readiness_bonus = min(readiness * 6.0, 60.0)
        return min(max(readiness_bonus - complexity_penalty, 0.0), 100.0)

    def score_acquisition_difficulty(self, context: Dict[str, Any]) -> float:
        budget = context.get("marketing_budget", "medium")
        channel_count = context.get("available_channels", 3)
        budget_score = {"low": 30.0, "medium": 60.0, "high": 90.0}.get(
            budget, 60.0
        )
        channel_bonus = min(channel_count * 5.0, 30.0)
        return min(max(budget_score + channel_bonus, 0.0), 100.0)

    def score_expected_revenue(self, context: Dict[str, Any]) -> float:
        tam = context.get("tam_billions", 1.0)
        price = context.get("average_price", 29.0)
        conversion = context.get("conversion_rate", 0.02)
        return min(max(tam * price * conversion * 100.0, 0.0), 100.0)
