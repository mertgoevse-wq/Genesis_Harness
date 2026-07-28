from typing import Dict, Any

class RankingEngine:
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "stars": 0.3,
            "forks": 0.15,
            "activity": 0.25,
            "docs": 0.30
        }

    def score_repository(self, item: Dict[str, Any]) -> float:
        stars_norm = min(item.get("stars", 0) / 5000.0, 1.0)
        forks_norm = min(item.get("forks", 0) / 1000.0, 1.0)
        activity_norm = max(0.0, 1.0 - (item.get("recency_days", 30) / 365.0))
        docs_norm = item.get("documentation_quality", 0.5)

        total_score = (
            (stars_norm * self.weights["stars"]) +
            (forks_norm * self.weights["forks"]) +
            (activity_norm * self.weights["activity"]) +
            (docs_norm * self.weights["docs"])
        ) * 100.0
        return round(total_score, 2)
