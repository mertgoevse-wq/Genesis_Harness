"""Product validation engine with GO / MODIFY / REJECT verdict."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .validation_scoring import ValidationScorer


@dataclass
class ValidationDecision:
    idea: str
    verdict: str  # GO, MODIFY, REJECT
    confidence: float  # 0.0 to 1.0
    overall_score: float
    market_demand_score: float
    competition_score: float
    pricing_potential_score: float
    customer_pain_score: float
    implementation_complexity_score: float
    acquisition_difficulty_score: float
    expected_revenue_score: float
    reasoning: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class ProductValidationEngine:
    """Evaluates a product idea and returns a validation decision."""

    WEIGHTS = {
        "market_demand": 0.18,
        "competition": 0.12,
        "pricing_potential": 0.15,
        "customer_pain": 0.18,
        "implementation_complexity": 0.12,
        "acquisition_difficulty": 0.10,
        "expected_revenue": 0.15,
    }

    def __init__(self):
        self.scorer = ValidationScorer()

    def evaluate(self, idea: str, context: Dict[str, Any]) -> ValidationDecision:
        """Evaluate a product idea and return a decision."""
        scores = {
            "market_demand": self.scorer.score_market_demand(context),
            "competition": self.scorer.score_competition(context),
            "pricing_potential": self.scorer.score_pricing_potential(context),
            "customer_pain": self.scorer.score_customer_pain(context),
            "implementation_complexity": self.scorer.score_implementation_complexity(
                context
            ),
            "acquisition_difficulty": self.scorer.score_acquisition_difficulty(
                context
            ),
            "expected_revenue": self.scorer.score_expected_revenue(context),
        }

        overall = sum(scores[k] * self.WEIGHTS[k] for k in scores)
        verdict, confidence = self._verdict(overall, scores, context)
        reasoning = self._reasoning(scores, verdict)
        recommendations = self._recommendations(scores)

        return ValidationDecision(
            idea=idea,
            verdict=verdict,
            confidence=round(confidence, 2),
            overall_score=round(overall, 2),
            market_demand_score=round(scores["market_demand"], 2),
            competition_score=round(scores["competition"], 2),
            pricing_potential_score=round(scores["pricing_potential"], 2),
            customer_pain_score=round(scores["customer_pain"], 2),
            implementation_complexity_score=round(
                scores["implementation_complexity"], 2
            ),
            acquisition_difficulty_score=round(scores["acquisition_difficulty"], 2),
            expected_revenue_score=round(scores["expected_revenue"], 2),
            reasoning=reasoning,
            recommendations=recommendations,
        )

    def _verdict(
        self, overall: float, scores: Dict[str, float], context: Dict[str, Any]
    ) -> tuple:
        low_scores = [k for k, v in scores.items() if v < 40.0]
        medium_scores = [k for k, v in scores.items() if 40.0 <= v < 60.0]

        if overall >= 70.0 and not low_scores:
            return "GO", 0.85
        if overall >= 50.0 and len(low_scores) <= 2:
            return "MODIFY", 0.70 if not medium_scores else 0.60
        return "REJECT", 0.80 if overall < 40.0 else 0.65

    def _reasoning(self, scores: Dict[str, float], verdict: str) -> List[str]:
        return [
            f"Verdict: {verdict}.",
            f"Market demand is {self._label(scores['market_demand'])}.",
            f"Competitive position is {self._label(scores['competition'])}.",
            f"Pricing potential is {self._label(scores['pricing_potential'])}.",
            f"Customer pain match is {self._label(scores['customer_pain'])}.",
            f"Implementation feasibility is {self._label(scores['implementation_complexity'])}.",
        ]

    def _recommendations(self, scores: Dict[str, float]) -> List[str]:
        recs = []
        if scores["market_demand"] < 50.0:
            recs.append("Validate market demand with customer interviews.")
        if scores["competition"] < 50.0:
            recs.append("Sharpen differentiation vs. incumbents.")
        if scores["implementation_complexity"] < 50.0:
            recs.append("Reduce technical scope for the MVP.")
        if scores["expected_revenue"] < 50.0:
            recs.append("Explore higher pricing or larger addressable market.")
        if not recs:
            recs.append("Proceed to build and launch the MVP.")
        return recs

    def _label(self, score: float) -> str:
        if score >= 75.0:
            return "strong"
        if score >= 50.0:
            return "moderate"
        return "weak"
