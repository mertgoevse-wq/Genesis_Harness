"""Growth experiment engine for revenue optimization."""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class GrowthExperiment:
    name: str
    hypothesis: str
    metric: str
    duration_weeks: int
    expected_uplift: float


class GrowthExperimentEngine:
    """Designs growth experiments for a product."""

    def design_experiments(self, context: Dict[str, Any]) -> List[GrowthExperiment]:
        """Return a list of prioritized growth experiments."""
        return [
            GrowthExperiment(
                name="Free trial onboarding",
                hypothesis="Reducing onboarding friction increases activation.",
                metric="activation_rate",
                duration_weeks=2,
                expected_uplift=0.10,
            ),
            GrowthExperiment(
                name="Annual billing discount",
                hypothesis="Annual discount improves cash flow and retention.",
                metric="annual_plan_share",
                duration_weeks=4,
                expected_uplift=0.15,
            ),
            GrowthExperiment(
                name="Referral program",
                hypothesis="Referral incentives reduce blended CAC.",
                metric="referral_rate",
                duration_weeks=6,
                expected_uplift=0.08,
            ),
        ]

    def recommend(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return recommended growth strategy and experiments."""
        experiments = self.design_experiments(context)
        return {
            "experiments": experiments,
            "prioritized_experiment": experiments[0].name,
            "expected_total_uplift": round(
                sum(e.expected_uplift for e in experiments), 2
            ),
        }
