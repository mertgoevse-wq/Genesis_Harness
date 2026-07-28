"""Competition dimension scoring for venture decisions."""

from typing import Dict, Any


class CompetitionScorer:
    """Scores a venture idea on competitive differentiation."""

    def score(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return competition score and labels."""
        incumbent_count = context.get("incumbent_count", 3)
        differentiation = context.get("differentiation_score", 50.0)

        concentration_penalty = max(0, (incumbent_count - 1) * 5.0)
        diff_score = min(differentiation, 70.0)
        total = max(0.0, diff_score - concentration_penalty)

        return {
            "score": round(total, 2),
            "label": self._label(total),
            "concentration_penalty": round(concentration_penalty, 2),
            "differentiation_score": round(diff_score, 2),
        }

    def _label(self, score: float) -> str:
        if score >= 65:
            return "differentiated"
        if score >= 40:
            return "crowded"
        return "dominated"
