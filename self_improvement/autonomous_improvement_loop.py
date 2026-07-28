"""Autonomous improvement loop: audit, detect, prioritize, execute, evaluate."""

from typing import Dict, Any, List
from datetime import datetime, timezone

from .weakness_detector import WeaknessDetector
from .task_prioritizer import TaskPrioritizer, ImprovementTask
from .evaluator import ImprovementEvaluator


class AutonomousImprovementLoop:
    """Continuously audits the system and drives improvements."""

    def __init__(self):
        self.weakness_detector = WeaknessDetector()
        self.task_prioritizer = TaskPrioritizer()
        self.evaluator = ImprovementEvaluator()
        self.audit_log: List[Dict[str, Any]] = []

    def run(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        audit = self.audit()
        weaknesses = self.weakness_detector.detect(execution_results)
        tasks = self.task_prioritizer.prioritize(weaknesses)
        prioritized = self.prioritize(tasks)
        executed = self.execute(prioritized)
        score = self.evaluator.evaluate(execution_results, executed)

        self.audit_log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "weaknesses": [w.category for w in weaknesses],
                "tasks": [t.title for t in executed],
                "score": score,
            }
        )

        return {
            "status": "IMPROVEMENT_LOOP_RUN",
            "audit": audit,
            "weaknesses": [self._weakness_to_dict(w) for w in weaknesses],
            "prioritized_tasks": [self._task_to_dict(t) for t in prioritized],
            "executed_tasks": [self._task_to_dict(t) for t in executed],
            "improvement_score": score,
        }

    def audit(self) -> Dict[str, Any]:
        return {
            "subsystems_audited": [
                "opportunity_intelligence",
                "venture_decision",
                "product_validation",
                "customer_intelligence",
                "validation_engine",
                "growth_intelligence",
                "deployment_intelligence",
                "revenue_intelligence",
                "self_improvement",
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "health_score": 85.0,
        }

    def prioritize(self, tasks: List[ImprovementTask]) -> List[ImprovementTask]:
        """Sort tasks by priority and expected impact."""
        return sorted(tasks, key=lambda t: (t.priority, -t.expected_impact))

    def execute(self, tasks: List[ImprovementTask]) -> List[ImprovementTask]:
        """Simulate execution of improvement tasks."""
        return tasks[:3]

    def _weakness_to_dict(self, weakness) -> Dict[str, Any]:
        return {
            "category": weakness.category,
            "description": weakness.description,
            "severity": weakness.severity,
            "evidence": weakness.evidence,
        }

    def _task_to_dict(self, task: ImprovementTask) -> Dict[str, Any]:
        return {
            "title": task.title,
            "category": task.category,
            "priority": task.priority,
            "effort": task.effort,
            "expected_impact": task.expected_impact,
        }
