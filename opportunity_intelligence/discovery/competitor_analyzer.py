"""Competitor landscape analysis for opportunity discovery."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Competitor:
    name: str
    domain: str
    strength: str  # 'dominant', 'strong', 'niche', 'emerging'
    weaknesses: List[str] = field(default_factory=list)


class CompetitorAnalyzer:
    """Maps the competitive landscape for a given market idea."""

    def analyze(self, topic: str) -> List[Competitor]:
        """Return a competitive landscape map for the topic."""
        return self._placeholder_landscape(topic)

    def _placeholder_landscape(self, topic: str) -> List[Competitor]:
        return [
            Competitor(
                name="IncumbentOne",
                domain=topic,
                strength="dominant",
                weaknesses=["High pricing", "Slow feature cycle"],
            ),
            Competitor(
                name="NicheUpstart",
                domain=topic,
                strength="niche",
                weaknesses=["Limited integrations", "Small team"],
            ),
        ]

    def gap_opportunities(self, competitors: List[Competitor]) -> List[str]:
        """Identify gaps based on common competitor weaknesses."""
        gaps = set()
        for competitor in competitors:
            for weakness in competitor.weaknesses:
                gaps.add(weakness)
        return list(gaps)
