"""Validation loop for product ideas, landing pages, pricing, and demand."""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime, timezone

from product_validation_engine.validation_engine import ProductValidationEngine


@dataclass
class ValidationExperiment:
    name: str
    hypothesis: str
    status: str  # planned, running, completed
    metric: str
    result: Any = None
    confidence: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ValidationLoop:
    """Runs continuous validation experiments for a product idea."""

    def __init__(self):
        self.product_validator = ProductValidationEngine()
        self.experiments: List[ValidationExperiment] = []
        self.memory: List[Dict[str, Any]] = []

    def run(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full validation loop and return a verdict."""
        decision = self.product_validator.evaluate(idea, context)

        experiments = [
            self._landing_page_experiment(idea, context),
            self._value_prop_experiment(idea, context),
            self._pricing_experiment(idea, context),
            self._demand_experiment(idea, context),
            self._competitor_experiment(idea, context),
        ]
        self.experiments.extend(experiments)

        experiment_summary = self._summarize_experiments(experiments)

        verdict = self._final_verdict(decision, experiments)

        self.memory.append(
            {
                "idea": idea,
                "decision": decision,
                "experiments": [self._exp_to_dict(e) for e in experiments],
                "verdict": verdict,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        return {
            "idea": idea,
            "verdict": verdict,
            "decision": decision,
            "experiments": experiment_summary,
            "recommendation": self._recommendation(verdict, experiments),
        }

    def _landing_page_experiment(self, idea: str, context: Dict[str, Any]) -> ValidationExperiment:
        headline = context.get("landing_headline", f"{idea} — automate your workflow")
        has_cta = context.get("has_cta", True)
        score = 70.0 + (10.0 if has_cta else 0.0)
        return ValidationExperiment(
            name="Landing Page Hypothesis",
            hypothesis=f"Headline '{headline}' will convert visitors above 2%",
            status="completed",
            metric="conversion_rate",
            result={"score": score, "headline": headline},
            confidence=0.65,
        )

    def _value_prop_experiment(self, idea: str, context: Dict[str, Any]) -> ValidationExperiment:
        clarity = context.get("value_prop_clarity", 70.0)
        return ValidationExperiment(
            name="Value Proposition Clarity",
            hypothesis="The value proposition is clear to the target audience",
            status="completed",
            metric="clarity_score",
            result={"score": clarity},
            confidence=0.60,
        )

    def _pricing_experiment(self, idea: str, context: Dict[str, Any]) -> ValidationExperiment:
        price = context.get("average_price", 29.0)
        willingness = context.get("willingness_to_pay", 60.0)
        score = min(willingness / price * 100.0, 100.0)
        return ValidationExperiment(
            name="Pricing Validation",
            hypothesis=f"Price ${price} is acceptable to target customers",
            status="completed",
            metric="price_acceptance",
            result={"score": score, "price": price},
            confidence=0.55,
        )

    def _demand_experiment(self, idea: str, context: Dict[str, Any]) -> ValidationExperiment:
        demand = context.get("demand_score", 50.0)
        return ValidationExperiment(
            name="Market Demand",
            hypothesis="There is sufficient market demand for this product",
            status="completed",
            metric="demand_score",
            result={"score": demand},
            confidence=0.70,
        )

    def _competitor_experiment(self, idea: str, context: Dict[str, Any]) -> ValidationExperiment:
        differentiation = context.get("differentiation_score", 50.0)
        return ValidationExperiment(
            name="Competitor Differentiation",
            hypothesis="The product is differentiated enough from competitors",
            status="completed",
            metric="differentiation_score",
            result={"score": differentiation},
            confidence=0.60,
        )

    def _summarize_experiments(self, experiments: List[ValidationExperiment]) -> Dict[str, Any]:
        total = len(experiments)
        avg_score = sum(
            e.result.get("score", 0.0) if isinstance(e.result, dict) else 0.0
            for e in experiments
        ) / max(total, 1)
        return {
            "experiment_count": total,
            "average_score": round(avg_score, 2),
            "items": [self._exp_to_dict(e) for e in experiments],
        }

    def _final_verdict(
        self, decision, experiments: List[ValidationExperiment]
    ) -> str:
        if decision.verdict == "REJECT":
            return "ABANDON"
        avg_score = sum(
            e.result.get("score", 0.0) if isinstance(e.result, dict) else 0.0
            for e in experiments
        ) / max(len(experiments), 1)
        if avg_score >= 65.0 and decision.verdict == "GO":
            return "BUILD"
        if avg_score >= 50.0:
            return "PIVOT/REFINE"
        return "ABANDON"

    def _recommendation(self, verdict: str, experiments: List[ValidationExperiment]) -> str:
        if verdict == "BUILD":
            return "Proceed to MVP. All validation signals are positive."
        if verdict == "PIVOT/REFINE":
            return "Refine value proposition and pricing before building."
        return "Abandon or significantly reshape the idea. Validation signals are too weak."

    def _exp_to_dict(self, experiment: ValidationExperiment) -> Dict[str, Any]:
        return {
            "name": experiment.name,
            "hypothesis": experiment.hypothesis,
            "status": experiment.status,
            "metric": experiment.metric,
            "result": experiment.result,
            "confidence": experiment.confidence,
            "created_at": experiment.created_at,
        }
