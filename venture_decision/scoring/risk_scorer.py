"""Risk scoring for venture decisions."""

from typing import Dict, Any, List


class RiskScorer:
    """Scores a venture idea on execution, market, and regulatory risk."""

    RISK_CATEGORIES = [
        "market_risk",
        "technical_risk",
        "regulatory_risk",
        "team_risk",
        "competition_risk",
    ]

    def score(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return risk score and labels."""
        category_scores = context.get("risk_scores", {})
        scores = [
            category_scores.get(cat, 5.0) for cat in self.RISK_CATEGORIES
        ]
        average = sum(scores) / len(scores)

        risks = self._identify_risks(category_scores)

        return {
            "score": round(average, 2),
            "label": self._label(average),
            "category_scores": dict(zip(self.RISK_CATEGORIES, scores)),
            "risks": risks,
        }

    def _identify_risks(self, category_scores: Dict[str, float]) -> List[str]:
        risks = []
        if category_scores.get("market_risk", 0.0) > 6.0:
            risks.append("Market demand is uncertain.")
        if category_scores.get("technical_risk", 0.0) > 6.0:
            risks.append("Technical feasibility is uncertain.")
        if category_scores.get("regulatory_risk", 0.0) > 6.0:
            risks.append("Regulatory environment is risky.")
        if not risks:
            risks.append("No dominant risk categories identified.")
        return risks

    def _label(self, score: float) -> str:
        if score >= 7.0:
            return "high"
        if score >= 4.0:
            return "medium"
        return "low"
