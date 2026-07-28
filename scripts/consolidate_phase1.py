"""Phase 1 consolidation script for Genesis Harness.

Copies the surviving real modules into a single ``genesis`` package, rewrites
imports, archives the harvester, removes stub/old directories, and prepares the
repository for ``pip install -e .`` and ``pytest``.

Run from the repository root::

    python scripts/consolidate_phase1.py

The script is intentionally cautious: it aborts on unexpected existing state.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GENESIS = REPO_ROOT / "genesis"

# Directories that are no longer part of the consolidated runtime.
DIRS_TO_REMOVE = [
    "agent_runtime",
    "knowledge_fabric",
    "global_context",
    "software_factory",
    "venture_execution",
    "product_launch",
    "agent_factory",
    "agent_collaboration",
    "coding_pipeline",
    "code_intelligence",
    "engineering_team",
    "execution_tools",
    "founder_intelligence",
    "github_engine",
    "knowledge_graph",
    "quality_intelligence",
    "research_benchmarks",
    "research_connectors",
    "research_intelligence",
    "security_intelligence",
    "skill_intelligence",
    "testing_intelligence",
    "tool_intelligence",
    "venture_pipeline",
    "product_factory",
    "genesis_runtime",
    "orchestration",
    "control-center",
    "orchestrator",
    "venture_decision",
    "product_validation_engine",
    "opportunity_intelligence",
    "live_intelligence",
    "revenue_intelligence",
    "growth_intelligence",
    "customer_intelligence",
    "validation_engine",
    "mvp_builder",
    "deployment_intelligence",
    "self_improvement",
    "memory_system",
    "core",
]

# Files to copy: source -> destination inside genesis/
FILE_MIGRATIONS: dict[Path, Path] = {
    # Decision
    Path("venture_decision/__init__.py"): GENESIS / "decision/__init__.py",
    Path("venture_decision/decision_engine.py"): GENESIS / "decision/engine.py",
    Path("venture_decision/scoring/market_scorer.py"): GENESIS / "decision/scorers/market.py",
    Path("venture_decision/scoring/competition_scorer.py"): GENESIS / "decision/scorers/competition.py",
    Path("venture_decision/scoring/technical_scorer.py"): GENESIS / "decision/scorers/technical.py",
    Path("venture_decision/scoring/risk_scorer.py"): GENESIS / "decision/scorers/risk.py",
    Path("product_validation_engine/validation_engine.py"): GENESIS / "decision/validation.py",
    Path("product_validation_engine/scoring.py"): GENESIS / "decision/validation_scoring.py",
    # Intelligence
    Path("opportunity_intelligence/__init__.py"): GENESIS / "intelligence/__init__.py",
    Path("opportunity_intelligence/opportunity_detector.py"): GENESIS / "intelligence/opportunity.py",
    Path("opportunity_intelligence/discovery/market_research_connector.py"): GENESIS / "intelligence/discovery/market_research.py",
    Path("opportunity_intelligence/discovery/trend_monitor.py"): GENESIS / "intelligence/discovery/trends.py",
    Path("opportunity_intelligence/discovery/competitor_analyzer.py"): GENESIS / "intelligence/discovery/competitors.py",
    Path("live_intelligence/base.py"): GENESIS / "intelligence/connectors/base.py",
    Path("live_intelligence/orchestrator.py"): GENESIS / "intelligence/connectors/orchestrator.py",
    Path("live_intelligence/connectors/market_data.py"): GENESIS / "intelligence/connectors/market_data.py",
    Path("live_intelligence/connectors/saas_trends.py"): GENESIS / "intelligence/connectors/saas_trends.py",
    Path("live_intelligence/connectors/github_signals.py"): GENESIS / "intelligence/connectors/github_signals.py",
    Path("live_intelligence/connectors/startup_signals.py"): GENESIS / "intelligence/connectors/startup_signals.py",
    # Revenue
    Path("revenue_intelligence/__init__.py"): GENESIS / "revenue/__init__.py",
    Path("revenue_intelligence/pricing_engine.py"): GENESIS / "revenue/pricing.py",
    Path("revenue_intelligence/subscription_models.py"): GENESIS / "revenue/subscriptions.py",
    Path("revenue_intelligence/acquisition_strategy.py"): GENESIS / "revenue/acquisition.py",
    Path("revenue_intelligence/growth_experiment_engine.py"): GENESIS / "revenue/experiments.py",
    # Growth
    Path("growth_intelligence/__init__.py"): GENESIS / "growth/__init__.py",
    Path("growth_intelligence/growth_engine.py"): GENESIS / "growth/engine.py",
    Path("growth_intelligence/channel_analyzer.py"): GENESIS / "growth/channels.py",
    Path("growth_intelligence/seo_opportunity_engine.py"): GENESIS / "growth/seo.py",
    Path("growth_intelligence/growth_loops.py"): GENESIS / "growth/loops.py",
    Path("customer_intelligence/customer_intelligence_engine.py"): GENESIS / "growth/customer.py",
    Path("validation_engine/validation_loop.py"): GENESIS / "growth/validation_loop.py",
    # Builder
    Path("mvp_builder/builder_engine.py"): GENESIS / "builder/mvp.py",
    Path("deployment_intelligence/deployment_planner.py"): GENESIS / "builder/deploy.py",
    Path("deployment_intelligence/providers/docker_generator.py"): GENESIS / "builder/providers/docker.py",
    Path("deployment_intelligence/providers/vercel_generator.py"): GENESIS / "builder/providers/vercel.py",
    Path("deployment_intelligence/providers/supabase_generator.py"): GENESIS / "builder/providers/supabase.py",
    Path("deployment_intelligence/providers/cloud_generator.py"): GENESIS / "builder/providers/cloud.py",
    # Memory
    Path("memory_system/founder_memory/founder_memory_store.py"): GENESIS / "memory/founder.py",
    Path("memory_system/storage/knowledge_store.py"): GENESIS / "memory/store.py",
    # Improvement
    Path("self_improvement/__init__.py"): GENESIS / "improvement/__init__.py",
    Path("self_improvement/improvement_engine.py"): GENESIS / "improvement/engine.py",
    Path("self_improvement/weakness_detector.py"): GENESIS / "improvement/weakness_detector.py",
    Path("self_improvement/task_prioritizer.py"): GENESIS / "improvement/task_prioritizer.py",
    Path("self_improvement/evaluator.py"): GENESIS / "improvement/evaluator.py",
    Path("self_improvement/autonomous_improvement_loop.py"): GENESIS / "improvement/autonomous_loop.py",
}

# Rewrite rules are applied after copying. Order matters: longer prefixes first.
IMPORT_REPLACEMENTS = [
    ("from validation_engine.validation_loop", "from genesis.growth.validation_loop"),
    ("from product_validation_engine.validation_engine", "from genesis.decision.validation"),
    ("from product_validation_engine.scoring", "from genesis.decision.validation_scoring"),
    ("from venture_decision", "from genesis.decision"),
    ("from live_intelligence", "from genesis.intelligence.connectors"),
    ("from opportunity_intelligence", "from genesis.intelligence"),
    ("from revenue_intelligence", "from genesis.revenue"),
    ("from growth_intelligence", "from genesis.growth"),
    ("from customer_intelligence", "from genesis.growth"),
    ("from mvp_builder", "from genesis.builder"),
    ("from deployment_intelligence", "from genesis.builder"),
    ("from memory_system.founder_memory", "from genesis.memory"),
    ("from memory_system.storage", "from genesis.memory"),
    ("from self_improvement", "from genesis.improvement"),
    # Internal relative fixes after the moves above.
    ("from .connectors.market_data", "from .market_data"),
    ("from .connectors.saas_trends", "from .saas_trends"),
    ("from .connectors.github_signals", "from .github_signals"),
    ("from .connectors.startup_signals", "from .startup_signals"),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def copy_with_import_rewrites(src: Path, dst: Path) -> None:
    content = src.read_text(encoding="utf-8")
    for old, new in IMPORT_REPLACEMENTS:
        content = content.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")


def create_package_init(path: Path, imports: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = ['"""Genesis package."""', ""]
    if imports:
        for imp in imports:
            lines.append(imp)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if (REPO_ROOT / "genesis" / "__init__.py").exists():
        fail("genesis/ already exists. Remove it before running consolidation.")

    # 1. Copy real modules.
    for src, dst in FILE_MIGRATIONS.items():
        if not src.exists():
            fail(f"Source file missing: {src}")
        copy_with_import_rewrites(src, dst)

    # 2. Create new package __init__ files.
    create_package_init(GENESIS / "__init__.py")
    create_package_init(GENESIS / "api/__init__.py")
    create_package_init(GENESIS / "config.py")
    create_package_init(GENESIS / "core/__init__.py")
    create_package_init(GENESIS / "decision/__init__.py", [
        "from .engine import VentureDecisionEngine, VentureDecision",
        "from .validation import ProductValidationEngine, ValidationDecision",
        "from .validation_scoring import ValidationScorer",
    ])
    create_package_init(GENESIS / "decision/scorers/__init__.py")
    create_package_init(GENESIS / "intelligence/__init__.py", [
        "from .opportunity import OpportunityDetector, Opportunity",
        "from .discovery.market_research import MarketResearchConnector, MarketSignal",
        "from .discovery.trends import TrendMonitor, Trend",
        "from .discovery.competitors import CompetitorAnalyzer, Competitor",
        "from .connectors.base import LiveConnector, ConnectorResult",
        "from .connectors.orchestrator import LiveIntelligenceOrchestrator",
    ])
    create_package_init(GENESIS / "intelligence/discovery/__init__.py")
    create_package_init(GENESIS / "intelligence/connectors/__init__.py")
    create_package_init(GENESIS / "revenue/__init__.py", [
        "from .pricing import PricingEngine, PricingTier",
        "from .subscriptions import SubscriptionModelSelector",
        "from .acquisition import AcquisitionStrategy",
        "from .experiments import GrowthExperimentEngine, GrowthExperiment",
    ])
    create_package_init(GENESIS / "growth/__init__.py", [
        "from .engine import GrowthEngine, GrowthStrategy",
        "from .channels import ChannelAnalyzer",
        "from .seo import SEOOpportunityEngine",
        "from .loops import GrowthLoops",
        "from .customer import CustomerIntelligenceEngine, CustomerPersona, IdealCustomerProfile",
        "from .validation_loop import ValidationLoop, ValidationExperiment",
    ])
    create_package_init(GENESIS / "builder/__init__.py", [
        "from .mvp import MVPBuilderEngine",
        "from .deploy import DeploymentPlanner",
    ])
    create_package_init(GENESIS / "builder/providers/__init__.py")
    create_package_init(GENESIS / "memory/__init__.py", [
        "from .founder import FounderMemoryStore, FounderDecision",
        "from .store import KnowledgeStore",
    ])
    create_package_init(GENESIS / "improvement/__init__.py", [
        "from .engine import ImprovementEngine",
        "from .weakness_detector import WeaknessDetector, Weakness",
        "from .task_prioritizer import TaskPrioritizer, ImprovementTask",
        "from .evaluator import ImprovementEvaluator",
        "from .autonomous_loop import AutonomousImprovementLoop",
    ])

    # 3. Write a slimmed orchestrator and CLI entry point.
    (GENESIS / "orchestrator.py").write_text(ORCHESTRATOR_SOURCE, encoding="utf-8")
    (GENESIS / "__main__.py").write_text(CLI_SOURCE, encoding="utf-8")

    # 4. Archive harvester.
    archive_dir = REPO_ROOT / "_archive"
    archive_dir.mkdir(exist_ok=True)
    harvester_src = REPO_ROOT / "harvester"
    if harvester_src.exists():
        shutil.move(str(harvester_src), str(archive_dir / "harvester"))

    # 5. Delete old directories.
    for name in DIRS_TO_REMOVE:
        path = REPO_ROOT / name
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

    # 6. Clean up pycache.
    for pycache in REPO_ROOT.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    print("Phase 1 consolidation complete. Run 'pip install -e .' then 'pytest'.")
    return 0


ORCHESTRATOR_SOURCE = '''"""Simplified Genesis orchestrator using only the real subsystems."""

from typing import Any, Dict

from genesis.decision import VentureDecisionEngine, ProductValidationEngine
from genesis.intelligence import OpportunityDetector, LiveIntelligenceOrchestrator
from genesis.revenue import (
    PricingEngine,
    SubscriptionModelSelector,
    AcquisitionStrategy,
    GrowthExperimentEngine,
)
from genesis.growth import GrowthEngine, ValidationLoop, CustomerIntelligenceEngine
from genesis.builder import DeploymentPlanner, MVPBuilderEngine
from genesis.memory import FounderMemoryStore
from genesis.improvement import ImprovementEngine, AutonomousImprovementLoop


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
'''


CLI_SOURCE = '''"""CLI entry point for Genesis."""

import argparse
import json
import sys
from typing import List

from genesis.orchestrator import MasterGenesisOrchestrator


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genesis AI Venture Operating System")
    parser.add_argument("command", choices=["analyze"], help="Command to run")
    parser.add_argument("prompt", help="Venture idea to analyze")
    parser.add_argument(
        "--context",
        default="{}",
        help="JSON context for the analysis",
    )
    args = parser.parse_args(argv)

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON context: {exc}", file=sys.stderr)
        return 1

    orchestrator = MasterGenesisOrchestrator()
    result = orchestrator.evaluate_venture(args.prompt, context)
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


if __name__ == "__main__":
    sys.exit(main())
