"""Market dimension scoring for venture decisions."""

from typing import Any, Dict


class MarketScorer:
    """Scores a venture idea on market size, growth, and monetization potential."""

    def score(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return market score and labels."""
        tam = context.get("tam_billions", 1.0)
        growth = context.get("growth_rate", 0.15)
        monetization = context.get("monetization_score", 60.0)

        tam_score = min(tam * 20.0, 40.0)
        growth_score = min(growth * 200.0, 30.0)
        monetization_score = min(monetization, 30.0)

        total = tam_score + growth_score + monetization_score
        label = self._label(total)

        return {
            "score": round(total, 2),
            "label": label,
            "tam_score": round(tam_score, 2),
            "growth_score": round(growth_score, 2),
            "monetization_score": round(monetization_score, 2),
        }

    def _label(self, score: float) -> str:
        if score >= 75:
            return "strong"
        if score >= 50:
            return "moderate"
        return "weak"
