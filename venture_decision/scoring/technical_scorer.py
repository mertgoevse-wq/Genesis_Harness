"""Technical complexity scoring for venture decisions."""

from typing import Dict, Any


class TechnicalScorer:
    """Scores a venture idea on technical feasibility and complexity."""

    def score(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return technical score and labels."""
        complexity = context.get("technical_complexity", 5)  # 1-10
        readiness = context.get("technical_readiness", 5)  # 1-10

        complexity_penalty = max(0, (complexity - 3) * 5.0)
        readiness_bonus = min(readiness * 6.0, 60.0)
        total = max(0.0, readiness_bonus - complexity_penalty)

        return {
            "score": round(total, 2),
            "label": self._label(total),
            "complexity_penalty": round(complexity_penalty, 2),
            "readiness_bonus": round(readiness_bonus, 2),
        }

    def _label(self, score: float) -> str:
        if score >= 65:
            return "straightforward"
        if score >= 40:
            return "moderate"
        return "challenging"
