"""Weakness detection for the self-improvement loop."""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Weakness:
    category: str
    description: str
    severity: str  # 'high', 'medium', 'low'
    evidence: List[str] = field(default_factory=list)


class WeaknessDetector:
    """Inspects execution results and identifies weaknesses."""

    CATEGORIES = [
        "quality_score",
        "test_coverage",
        "documentation",
        "agent_coordination",
        "deployment_readiness",
    ]

    def detect(self, execution_results: Dict[str, Any]) -> List[Weakness]:
        """Return a list of weaknesses found in execution results."""
        weaknesses = []
        quality = execution_results.get("quality_score", 100.0)
        if quality < 80.0:
            weaknesses.append(
                Weakness(
                    category="quality_score",
                    description="Overall quality score is below target threshold.",
                    severity="high",
                    evidence=[f"Quality score: {quality}"],
                )
            )

        tests = execution_results.get("tests", {})
        if not tests.get("passed", True):
            weaknesses.append(
                Weakness(
                    category="test_coverage",
                    description="Tests are failing or missing.",
                    severity="high",
                    evidence=["Test report indicates failures."],
                )
            )

        docs = execution_results.get("documentation_updated", True)
        if not docs:
            weaknesses.append(
                Weakness(
                    category="documentation",
                    description="Documentation was not updated.",
                    severity="medium",
                    evidence=["documentation_updated flag is false."],
                )
            )

        if not weaknesses:
            weaknesses.append(
                Weakness(
                    category="none",
                    description="No major weaknesses detected.",
                    severity="low",
                    evidence=["All tracked metrics within acceptable range."],
                )
            )

        return weaknesses
