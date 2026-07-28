"""Founder decision memory store."""

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class FounderDecision:
    idea: str
    verdict: str
    rationale: str
    confidence: float
    timestamp: str
    context: Dict[str, Any]


class FounderMemoryStore:
    """Persists founder-level decisions and learns from them."""

    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "..", "..", "logs", "founder_memory.json"
        )
        self._decisions: List[FounderDecision] = []
        self._load()

    def record_decision(
        self,
        idea: str,
        verdict: str,
        rationale: str,
        confidence: float,
        context: Dict[str, Any],
    ) -> FounderDecision:
        decision = FounderDecision(
            idea=idea,
            verdict=verdict,
            rationale=rationale,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc).isoformat(),
            context=context,
        )
        self._decisions.append(decision)
        self._save()
        return decision

    def successful_patterns(self) -> List[Dict[str, Any]]:
        return [asdict(d) for d in self._decisions if d.verdict == "GO" or d.verdict == "BUILD"]

    def failed_ideas(self) -> List[Dict[str, Any]]:
        return [asdict(d) for d in self._decisions if d.verdict == "REJECT" or d.verdict == "ABANDON"]

    def market_opportunities(self) -> List[Dict[str, Any]]:
        return [asdict(d) for d in self._decisions if "opportunity" in d.idea.lower()]

    def previous_decisions(self, idea: str = None) -> List[Dict[str, Any]]:
        if idea:
            return [asdict(d) for d in self._decisions if idea.lower() in d.idea.lower()]
        return [asdict(d) for d in self._decisions]

    def why_decision(self, idea: str) -> List[str]:
        return [
            f"{d.timestamp}: {d.verdict} — {d.rationale}"
            for d in self._decisions
            if idea.lower() in d.idea.lower()
        ]

    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._decisions = [FounderDecision(**item) for item in data]
            except Exception:
                self._decisions = []

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([asdict(d) for d in self._decisions], f, indent=2)
