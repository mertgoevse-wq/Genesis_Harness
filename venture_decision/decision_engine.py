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

    def evaluate(self, idea: str, context: Dict[str, Any] | None = None, customer_intelligence: Dict[str, Any] | None = None) -> VentureDecision:
        """Evaluate a venture idea and return a decision."""
        ctx = context or {}

        market = self.market_scorer.score(idea, ctx)
        competition = self.competition_scorer.score(idea, ctx)
        technical = self.technical_scorer.score(idea, ctx)
        risk = self.risk_scorer.score(idea, ctx)

        monetization = market.get("monetization_score", 50.0)

        # Integrate customer intelligence signals if available
        ci = customer_intelligence or {}
        icp = ci.get("icp", {})
        fit_score = icp.get("fit_score", 50.0)
        pain_points = ci.get("pain_points", [])
        avg_pain = sum(p.get("severity", 5.0) for p in pain_points) / max(len(pain_points), 1) if pain_points else 5.0
        customer_boost = (fit_score - 50.0) * 0.1 + (avg_pain - 5.0) * 2.0

        overall = (
            market["score"] * 0.25
            + competition["score"] * 0.20
            + monetization * 0.20
            + technical["score"] * 0.20
            + (100.0 - risk["score"]) * 0.15
            + customer_boost
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
            reasoning=reasoning + [f"Customer ICP fit score: {fit_score}."] if customer_intelligence else reasoning,
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
