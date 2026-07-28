"""Evaluator for self-improvement results."""

from typing import Dict, Any, List


class ImprovementEvaluator:
    """Evaluates the quality of an improvement plan."""

    def evaluate(
        self, execution_results: Dict[str, Any], tasks: List[Any]
    ) -> float:
        """Return an improvement score based on execution state and tasks."""
        base = execution_results.get("quality_score", 50.0)
        task_value = min(len(tasks) * 5.0, 25.0)
        return round(min(base + task_value, 100.0), 2)
