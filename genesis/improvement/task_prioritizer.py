"""Task prioritization for the self-improvement loop."""

from dataclasses import dataclass
from typing import Any, List


@dataclass
class ImprovementTask:
    title: str
    category: str
    priority: int  # lower is higher priority
    effort: str  # 'small', 'medium', 'large'
    expected_impact: float  # 0.0 to 1.0


class TaskPrioritizer:
    """Prioritizes improvement tasks by impact and effort."""

    def prioritize(self, weaknesses: List[Any]) -> List[ImprovementTask]:
        """Convert weaknesses into prioritized improvement tasks."""
        tasks = []
        for weakness in weaknesses:
            if weakness.category == "none":
                continue
            tasks.append(
                ImprovementTask(
                    title=f"Improve {weakness.category}",
                    category=weakness.category,
                    priority=self._priority(weakness.severity),
                    effort="medium",
                    expected_impact=0.5 if weakness.severity == "high" else 0.3,
                )
            )

        if not tasks:
            tasks.append(
                ImprovementTask(
                    title="Refine evaluation metrics",
                    category="metrics",
                    priority=3,
                    effort="small",
                    expected_impact=0.2,
                )
            )

        return sorted(tasks, key=lambda t: (t.priority, -t.expected_impact))

    def _priority(self, severity: str) -> int:
        return {"high": 1, "medium": 2, "low": 3}.get(severity, 3)
