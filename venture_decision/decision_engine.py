"""Venture decision engine: combine scoring dimensions into a go/no-go verdict."""

from dataclasses import dataclass, field
from typing import List, Dict, Any

from .scoring.market_scorer import MarketScorer
from .scoring.competition_scorer import CompetitionScorer
from .scoring.technical_scorer import TechnicalScorer
from .scoring.risk_scorer import RiskScorer


@dataclass
class VentureDecision:
    idea: str
    verdict: str  # 'GO', 'NO-GO', 'MAYBE'
    overall_score: float  # 0.0 to 100.0
    market_score: float
    competition_score: float
    monetization_score: float
    technical_score: float
    risk_score: float
    confidence: str
    reasoning: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


class VentureDecisionEngine:
    """Evaluates a venture idea and returns a structured decision."""

    def __init__(self):
        self.market_scorer = MarketScorer()
        self.competition_scorer = CompetitionScorer()
        self.technical_scorer = TechnicalScorer()
        self.risk_scorer = RiskScorer()

    def evaluate(self, idea: str, context: Dict[str, Any] | None = None) -> VentureDecision:
        """Evaluate a venture idea and return a decision."""
        ctx = context or {}

        market = self.market_scorer.score(idea, ctx)
        competition = self.competition_scorer.score(idea, ctx)
        technical = self.technical_scorer.score(idea, ctx)
        risk = self.risk_scorer.score(idea, ctx)

        monetization = market.get("monetization_score", 50.0)
        overall = (
            market["score"] * 0.25
            + competition["score"] * 0.20
            + monetization * 0.20
            + technical["score"] * 0.20
            + (100.0 - risk["score"]) * 0.15
        )

        verdict = self._verdict(overall, risk["score"])
        reasoning = self._reasoning(market, competition, technical, risk, verdict)

        return VentureDecision(
            idea=idea,
            verdict=verdict,
            overall_score=round(overall, 2),
            market_score=round(market["score"], 2),
            competition_score=round(competition["score"], 2),
            monetization_score=round(monetization, 2),
            technical_score=round(technical["score"], 2),
            risk_score=round(risk["score"], 2),
            confidence="ASSUMED",
            reasoning=reasoning,
            risks=risk.get("risks", []),
        )

    def _verdict(self, overall: float, risk_score: float) -> str:
        if overall >= 75 and risk_score < 60:
            return "GO"
        if overall >= 50 and risk_score < 80:
            return "MAYBE"
        return "NO-GO"

    def _reasoning(
        self, market, competition, technical, risk, verdict: str
    ) -> List[str]:
        return [
            f"Market attractiveness is {market['label']}.",
            f"Competitive position is {competition['label']}.",
            f"Technical feasibility is {technical['label']}.",
            f"Risk level is {risk['label']}.",
            f"Overall verdict: {verdict}.",
        ]
