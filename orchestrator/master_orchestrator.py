from genesis_runtime.runtime.engine import GenesisRuntimeEngine
from product_factory.pipeline.product_lifecycle import ProductLifecycleEngine
from founder_intelligence.market_scanner.trend_detector import TrendDetector
from venture_execution.orchestrator.venture_executor import VentureExecutor
from software_factory.factory.software_factory_engine import SoftwareFactoryEngine
from research_intelligence.research_engine.research_orchestrator import ResearchIntelligenceEngine
from quality_intelligence.quality_evaluator import QualityEvaluator

from opportunity_intelligence.opportunity_detector import OpportunityDetector
from venture_decision.decision_engine import VentureDecisionEngine
from deployment_intelligence.deployment_planner import DeploymentPlanner
from revenue_intelligence.pricing_engine import PricingEngine
from revenue_intelligence.subscription_models import SubscriptionModelSelector
from revenue_intelligence.acquisition_strategy import AcquisitionStrategy
from revenue_intelligence.growth_experiment_engine import GrowthExperimentEngine
from self_improvement.improvement_engine import ImprovementEngine


class MasterGenesisOrchestrator:
    """Coordinates the autonomous venture operating system."""

    def __init__(self):
        self.runtime = GenesisRuntimeEngine()
        self.trend_detector = TrendDetector()
        self.venture_executor = VentureExecutor()
        self.software_factory = SoftwareFactoryEngine()
        self.research_engine = ResearchIntelligenceEngine()
        self.quality_evaluator = QualityEvaluator()

        # New business intelligence subsystems
        self.opportunity_detector = OpportunityDetector()
        self.venture_decision = VentureDecisionEngine()
        self.deployment_planner = DeploymentPlanner()
        self.pricing_engine = PricingEngine()
        self.subscription_selector = SubscriptionModelSelector()
        self.acquisition_strategy = AcquisitionStrategy()
        self.growth_experiments = GrowthExperimentEngine()
        self.self_improvement = ImprovementEngine()

    def run_full_autonomous_cycle(self, goal: str) -> dict:
        print(f"[MasterOrchestrator] Starting autonomous OS cycle for goal: {goal}")

        # 1. Product Lifecycle Initialization
        product_lifecycle = ProductLifecycleEngine(product_name=goal)

        # 2. Research Intelligence
        research = self.research_engine.analyze_advances(goal)

        # 3. Market & Trend Detection
        trends = (
            self.trend_detector.detect_trends(goal)
            if hasattr(self.trend_detector, "detect_trends")
            else {"trends": ["AI SaaS"]}
        )

        # 4. Product Lifecycle State
        product = (
            product_lifecycle.get_current_state()
            if hasattr(product_lifecycle, "get_current_state")
            else {"status": "DISCOVERY"}
        )

        # 5. Opportunity Discovery
        opportunities = self.opportunity_detector.detect(goal, limit=3)

        # 6. Venture Decision
        decision = self.venture_decision.evaluate(
            goal,
            context={
                "tam_billions": 2.5,
                "growth_rate": 0.22,
                "monetization_score": 75.0,
                "incumbent_count": 3,
                "differentiation_score": 70.0,
                "technical_complexity": 4,
                "technical_readiness": 6,
                "risk_scores": {
                    "market_risk": 5.0,
                    "technical_risk": 4.0,
                    "regulatory_risk": 3.0,
                    "team_risk": 4.0,
                    "competition_risk": 5.0,
                },
            },
        )

        # 7. Revenue Intelligence
        revenue = self._build_revenue_intelligence(goal)

        # 8. Deployment Planning
        deployment = self.deployment_planner.plan(
            goal,
            requirements={
                "frontend": True,
                "backend": True,
                "database": True,
            },
        )

        # 9. Venture Execution
        venture = self.venture_executor.execute_venture(goal)

        # 10. Software Factory Development
        software = self.software_factory.build_software(goal)

        # 11. Quality & Security Evaluation
        quality = self.quality_evaluator.calculate_quality_score(software)

        # 12. Self-Improvement Analysis
        improvement = self.self_improvement.analyze(
            {"quality_score": quality.get("score", 0.0), "tests": {"passed": True}}
        )

        return {
            "goal": goal,
            "status": "COMPLETED",
            "research": research,
            "trends": trends,
            "product": product,
            "opportunities": opportunities,
            "venture_decision": decision,
            "revenue": revenue,
            "deployment": deployment,
            "venture": venture,
            "software": software,
            "quality": quality,
            "improvement": improvement,
        }

    def _build_revenue_intelligence(self, goal: str) -> dict:
        """Aggregate revenue intelligence outputs for a venture."""
        context = {"base_price": 19.0, "product_type": "saas", "budget": "medium"}
        return {
            "pricing": self.pricing_engine.recommend(context),
            "subscription_model": self.subscription_selector.recommend(context),
            "acquisition": self.acquisition_strategy.recommend(context),
            "growth_experiments": self.growth_experiments.recommend(context),
        }
