"""Self-improvement engine: detect weaknesses, prioritize, and plan actions."""

from typing import Any, Dict

from .evaluator import ImprovementEvaluator
from .task_prioritizer import TaskPrioritizer
from .weakness_detector import WeaknessDetector


class ImprovementEngine:
    """Drives the self-improvement loop for Genesis."""

    def __init__(self):
        self.weakness_detector = WeaknessDetector()
        self.task_prioritizer = TaskPrioritizer()
        self.evaluator = ImprovementEvaluator()

    def analyze(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze execution results and produce an improvement plan."""
        weaknesses = self.weakness_detector.detect(execution_results)
        tasks = self.task_prioritizer.prioritize(weaknesses)
        score = self.evaluator.evaluate(execution_results, tasks)

        return {
            "status": "ANALYZED",
            "weaknesses": weaknesses,
            "tasks": tasks,
            "improvement_score": score,
            "next_action": tasks[0].title if tasks else "Maintain current state",
        }
