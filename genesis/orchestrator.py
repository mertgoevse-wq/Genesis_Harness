"""Simplified Genesis orchestrator using only the real subsystems."""

from typing import Any, Dict

from genesis.builder import DeploymentPlanner, MVPBuilderEngine
from genesis.decision import ProductValidationEngine, VentureDecisionEngine
from genesis.growth import CustomerIntelligenceEngine, GrowthEngine, ValidationLoop
from genesis.improvement import AutonomousImprovementLoop, ImprovementEngine
from genesis.intelligence import LiveIntelligenceOrchestrator, OpportunityDetector
from genesis.memory import FounderMemoryStore
from genesis.revenue import (
    AcquisitionStrategy,
    GrowthExperimentEngine,
    PricingEngine,
    SubscriptionModelSelector,
)


class MasterGenesisOrchestrator:
    """Coordinates the consolidated Genesis subsystems."""

    def __init__(self) -> None:
        self.opportunity_detector = OpportunityDetector()
        self.venture_decision = VentureDecisionEngine()
        self.product_validator = ProductValidationEngine()
        self.live_intelligence = LiveIntelligenceOrchestrator()
        self.pricing_engine = PricingEngine()
        self.subscription_selector = SubscriptionModelSelector()
        self.acquisition_strategy = AcquisitionStrategy()
        self.growth_experiments = GrowthExperimentEngine()
        self.growth_engine = GrowthEngine()
        self.validation_loop = ValidationLoop()
        self.customer_intelligence = CustomerIntelligenceEngine()
        self.deployment_planner = DeploymentPlanner()
        self.mvp_builder = MVPBuilderEngine()
        self.founder_memory = FounderMemoryStore()
        self.improvement_engine = ImprovementEngine()
        self.autonomous_improvement = AutonomousImprovementLoop()

    def evaluate_venture(self, idea: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Run a full venture evaluation for *idea*."""
        context = context or {}
        customer = self.customer_intelligence.analyze(idea, context)
        live = self.live_intelligence.gather(idea)
        opportunities = self.opportunity_detector.detect(idea, limit=3)
        validation = self.validation_loop.run(idea, context)
        decision = self.venture_decision.evaluate(idea, context, customer_intelligence=customer)
        revenue = self._build_revenue_intelligence(context)
        deployment = self.deployment_planner.plan(idea, {"frontend": True, "backend": True, "database": True})
        growth = self.growth_engine.recommend(idea, context)
        improvement = self.improvement_engine.analyze(
            {"quality_score": 90.0, "tests": {"passed": True}}
        )
        self.founder_memory.record_decision(
            idea=idea,
            verdict=validation["verdict"],
            rationale=f"Validation loop verdict: {validation['verdict']}",
            confidence=validation["decision"].confidence,
            context={
                "venture_decision": decision.verdict,
                "validation_verdict": validation["verdict"],
                "overall_score": validation["decision"].overall_score,
            },
        )
        autonomous = self.autonomous_improvement.run(
            {"quality_score": 90.0, "tests": {"passed": True}, "documentation_updated": True}
        )
        return {
            "idea": idea,
            "decision": {
                "verdict": decision.verdict,
                "overall_score": decision.overall_score,
                "confidence": decision.confidence,
            },
            "validation": {
                "verdict": validation["verdict"],
                "confidence": validation["decision"].confidence,
            },
            "opportunities": [
                {"name": o.name, "score": o.score} for o in opportunities
            ],
            "live_signals": live,
            "revenue": revenue,
            "deployment": deployment,
            "growth": growth,
            "improvement": improvement,
            "autonomous_improvement": autonomous,
        }

    def _build_revenue_intelligence(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {"base_price": 19.0, "product_type": "saas", "budget": "medium"}
        ctx.update(context)
        return {
            "pricing": self.pricing_engine.recommend(ctx),
            "subscription_model": self.subscription_selector.recommend(ctx),
            "acquisition": self.acquisition_strategy.recommend(ctx),
            "growth_experiments": self.growth_experiments.recommend(ctx),
        }


def run_full_autonomous_cycle(idea: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Legacy-compatible entry point."""
    return MasterGenesisOrchestrator().evaluate_venture(idea, context)
