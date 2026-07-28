"""Replace legacy tests with a focused genesis package test suite."""

import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS = REPO_ROOT / "tests"

if TESTS.exists():
    shutil.rmtree(TESTS)
TESTS.mkdir()
(TESTS / "__init__.py").write_text("", encoding="utf-8")


def write(name: str, content: str) -> None:
    (TESTS / name).write_text(content, encoding="utf-8")


write(
    "test_decision.py",
    '''"""Tests for genesis.decision."""

import unittest

from genesis.decision import (
    VentureDecisionEngine,
    ProductValidationEngine,
    ValidationScorer,
)


class TestVentureDecisionEngine(unittest.TestCase):
    def test_evaluate_returns_decision(self) -> None:
        engine = VentureDecisionEngine()
        decision = engine.evaluate(
            "AI compliance assistant",
            context={
                "tam_billions": 5.0,
                "growth_rate": 0.25,
                "monetization_score": 80.0,
                "incumbent_count": 2,
                "differentiation_score": 75.0,
                "technical_complexity": 4,
                "technical_readiness": 7,
                "risk_scores": {
                    "market_risk": 4.0,
                    "technical_risk": 3.0,
                    "regulatory_risk": 6.0,
                    "team_risk": 4.0,
                    "competition_risk": 5.0,
                },
            },
        )
        self.assertIn(decision.verdict, {"GO", "NO-GO", "MAYBE"})
        self.assertGreaterEqual(decision.overall_score, 0.0)
        self.assertLessEqual(decision.overall_score, 100.0)

    def test_verdict_no_go_for_low_score(self) -> None:
        engine = VentureDecisionEngine()
        decision = engine.evaluate(
            "bad idea",
            context={
                "tam_billions": 0.01,
                "growth_rate": 0.0,
                "monetization_score": 0.0,
                "incumbent_count": 10,
                "differentiation_score": 0.0,
                "technical_complexity": 9,
                "technical_readiness": 1,
                "risk_scores": {
                    "market_risk": 9.0,
                    "technical_risk": 9.0,
                    "regulatory_risk": 9.0,
                    "team_risk": 9.0,
                    "competition_risk": 9.0,
                },
            },
        )
        self.assertEqual(decision.verdict, "NO-GO")


class TestProductValidationEngine(unittest.TestCase):
    def test_evaluate_returns_verdict(self) -> None:
        engine = ProductValidationEngine()
        result = engine.evaluate(
            "AI note assistant",
            context={
                "demand_score": 80.0,
                "incumbent_count": 3,
                "differentiation_score": 70.0,
                "monetization_score": 80.0,
                "pain_score": 80.0,
                "urgency_score": 75.0,
                "technical_complexity": 4,
                "technical_readiness": 6,
                "marketing_budget": "medium",
                "available_channels": 3,
                "tam_billions": 1.0,
                "average_price": 29.0,
                "conversion_rate": 0.02,
            },
        )
        self.assertIn(result.verdict, {"GO", "MODIFY", "REJECT"})
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)


class TestValidationScorer(unittest.TestCase):
    def test_scores_are_bounded(self) -> None:
        scorer = ValidationScorer()
        context = {
            "demand_score": 110.0,
            "incumbent_count": 20,
            "differentiation_score": 50.0,
            "pain_score": 80.0,
            "urgency_score": 90.0,
            "technical_complexity": 2,
            "technical_readiness": 5,
            "marketing_budget": "high",
            "available_channels": 10,
            "tam_billions": 5.0,
            "average_price": 50.0,
            "conversion_rate": 0.05,
        }
        self.assertEqual(scorer.score_market_demand(context), 100.0)
        self.assertGreaterEqual(scorer.score_competition(context), 0.0)
        self.assertLessEqual(scorer.score_competition(context), 100.0)
''',
)

write(
    "test_intelligence.py",
    '''"""Tests for genesis.intelligence."""

import unittest

from genesis.intelligence import (
    OpportunityDetector,
    TrendMonitor,
    CompetitorAnalyzer,
    MarketResearchConnector,
    LiveIntelligenceOrchestrator,
)


class TestOpportunityDetector(unittest.TestCase):
    def test_detect_returns_opportunities(self) -> None:
        detector = OpportunityDetector()
        opportunities = detector.detect("healthcare ai")
        self.assertIsInstance(opportunities, list)
        self.assertGreater(len(opportunities), 0)
        first = opportunities[0]
        self.assertGreaterEqual(first.score, 0.0)
        self.assertLessEqual(first.score, 100.0)

    def test_trend_monitor_returns_trends(self) -> None:
        trends = TrendMonitor().detect_trends("fintech")
        self.assertIsInstance(trends, list)
        self.assertGreater(len(trends), 0)

    def test_competitor_analyzer_returns_landscape(self) -> None:
        analyzer = CompetitorAnalyzer()
        competitors = analyzer.analyze("fintech")
        self.assertIsInstance(competitors, list)
        self.assertGreater(len(competitors), 0)
        gaps = analyzer.gap_opportunities(competitors)
        self.assertIsInstance(gaps, list)

    def test_market_research_connector_signals(self) -> None:
        connector = MarketResearchConnector()
        signals = connector.fetch_signals("fintech", limit=5)
        self.assertIsInstance(signals, list)
        self.assertLessEqual(len(signals), 5)


class TestLiveIntelligenceOrchestrator(unittest.TestCase):
    def test_gather_returns_signals(self) -> None:
        orchestrator = LiveIntelligenceOrchestrator()
        result = orchestrator.gather("test")
        self.assertIn("signals", result)
        self.assertEqual(len(result["signals"]), 4)
''',
)

write(
    "test_revenue.py",
    '''"""Tests for genesis.revenue."""

import unittest

from genesis.revenue import (
    PricingEngine,
    SubscriptionModelSelector,
    AcquisitionStrategy,
    GrowthExperimentEngine,
)


class TestRevenue(unittest.TestCase):
    def test_pricing_engine_recommend(self) -> None:
        engine = PricingEngine()
        result = engine.recommend({"base_price": 12.0})
        self.assertIn("tiers", result)
        self.assertIn("recommended_tier", result)
        self.assertEqual(len(result["tiers"]), 3)

    def test_subscription_selector(self) -> None:
        selector = SubscriptionModelSelector()
        result = selector.recommend({"product_type": "api"})
        self.assertEqual(result["recommended_model"], "usage_based")

    def test_acquisition_strategy(self) -> None:
        strategy = AcquisitionStrategy()
        result = strategy.recommend({"budget": "low"})
        self.assertIn("primary_channels", result)
        self.assertIn("tactics", result)

    def test_growth_experiments(self) -> None:
        engine = GrowthExperimentEngine()
        result = engine.recommend({})
        self.assertIn("experiments", result)
        self.assertGreater(len(result["experiments"]), 0)
''',
)

write(
    "test_growth.py",
    '''"""Tests for genesis.growth."""

import unittest

from genesis.growth import (
    GrowthEngine,
    ChannelAnalyzer,
    SEOOpportunityEngine,
    GrowthLoops,
    CustomerIntelligenceEngine,
    ValidationLoop,
)


class TestGrowth(unittest.TestCase):
    def test_growth_engine_recommend(self) -> None:
        engine = GrowthEngine()
        result = engine.recommend("AI Tool", {"target_audience": "startups"})
        self.assertIn("landing_page", result)
        self.assertIn("seo", result)
        self.assertIn("acquisition_channels", result)

    def test_channel_analyzer(self) -> None:
        analyzer = ChannelAnalyzer()
        result = analyzer.analyze("AI Tool", {"marketing_budget": "medium", "target_audience": "startups"})
        self.assertIn("channels", result)
        self.assertGreater(len(result["channels"]), 0)

    def test_seo_opportunity_engine(self) -> None:
        engine = SEOOpportunityEngine()
        result = engine.analyze("AI Tool", {"target_audience": "startups"})
        self.assertIn("keywords", result)
        self.assertIn("content_pillars", result)

    def test_growth_loops(self) -> None:
        loops = GrowthLoops()
        result = loops.design("AI Tool", {})
        self.assertIn("loops", result)
        self.assertGreater(len(result["loops"]), 0)

    def test_customer_intelligence(self) -> None:
        engine = CustomerIntelligenceEngine()
        result = engine.analyze("AI assistant", {"target_audience": "lawyers"})
        self.assertIn("personas", result)
        self.assertIn("icp", result)

    def test_validation_loop(self) -> None:
        loop = ValidationLoop()
        result = loop.run(
            "AI note assistant",
            {
                "demand_score": 80.0,
                "differentiation_score": 75.0,
                "monetization_score": 80.0,
                "average_price": 29.0,
                "willingness_to_pay": 60.0,
            },
        )
        self.assertIn(result["verdict"], {"BUILD", "PIVOT/REFINE", "ABANDON"})
''',
)

write(
    "test_builder.py",
    '''"""Tests for genesis.builder."""

import os
import shutil
import tempfile
import unittest

from genesis.builder import MVPBuilderEngine, DeploymentPlanner


class TestMVPBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_build_mvp_creates_files(self) -> None:
        engine = MVPBuilderEngine()
        result = engine.build_mvp("AI Note Assistant", self.output_dir)
        self.assertEqual(result["status"], "MVP_BUILT_AND_READY")
        self.assertTrue(os.path.exists(result["mvp_dir"]))
        self.assertIn("backend/main.py", result["files_created"])
        self.assertIn("frontend/index.html", result["files_created"])
        self.assertIn("docker/Dockerfile", result["files_created"])

    def test_backend_main_contains_fastapi(self) -> None:
        engine = MVPBuilderEngine()
        result = engine.build_mvp("Test Product", self.output_dir)
        main_path = os.path.join(result["mvp_dir"], "backend", "main.py")
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("FastAPI", content)
        self.assertIn("health", content)


class TestDeploymentPlanner(unittest.TestCase):
    def test_plan_returns_providers(self) -> None:
        planner = DeploymentPlanner()
        result = planner.plan(
            "ai-note-assistant",
            {"frontend": True, "backend": True, "database": True},
        )
        self.assertEqual(result["status"], "PLANNED")
        self.assertIn("docker", result["providers"])
        self.assertIn("artifacts", result)
''',
)

write(
    "test_memory.py",
    '''"""Tests for genesis.memory."""

import os
import tempfile
import unittest

from genesis.memory import FounderMemoryStore, KnowledgeStore


class TestFounderMemoryStore(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.store = FounderMemoryStore(storage_path=self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.close()
        os.unlink(self.tmp.name)

    def test_record_decision(self) -> None:
        self.store.record_decision("idea", "GO", "strong market", 0.8, {})
        self.assertEqual(len(self.store.previous_decisions()), 1)

    def test_successful_patterns(self) -> None:
        self.store.record_decision("good idea", "GO", "strong", 0.9, {})
        self.store.record_decision("bad idea", "REJECT", "weak", 0.3, {})
        self.assertEqual(len(self.store.successful_patterns()), 1)
        self.assertEqual(len(self.store.failed_ideas()), 1)


class TestKnowledgeStore(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.store = KnowledgeStore(db_path=self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.close()
        os.unlink(self.tmp.name)

    def test_save_record(self) -> None:
        record = self.store.save_record("test", {"key": "value"})
        self.assertEqual(record["category"], "test")
        self.assertEqual(len(self.store.records), 1)
''',
)

write(
    "test_improvement.py",
    '''"""Tests for genesis.improvement."""

import unittest

from genesis.improvement import (
    ImprovementEngine,
    AutonomousImprovementLoop,
    WeaknessDetector,
)


class TestImprovement(unittest.TestCase):
    def test_engine_analyze(self) -> None:
        engine = ImprovementEngine()
        result = engine.analyze({"quality_score": 90.0, "tests": {"passed": True}})
        self.assertEqual(result["status"], "ANALYZED")
        self.assertIn("weaknesses", result)

    def test_autonomous_loop(self) -> None:
        loop = AutonomousImprovementLoop()
        result = loop.run({"quality_score": 90.0, "tests": {"passed": True}})
        self.assertEqual(result["status"], "IMPROVEMENT_LOOP_RUN")
        self.assertIn("weaknesses", result)

    def test_weakness_detector(self) -> None:
        detector = WeaknessDetector()
        weaknesses = detector.detect({"quality_score": 70.0, "tests": {"passed": False}})
        self.assertGreater(len(weaknesses), 0)
''',
)

write(
    "test_orchestrator.py",
    '''"""Tests for genesis.orchestrator."""

import unittest
from unittest.mock import patch

from genesis.orchestrator import MasterGenesisOrchestrator


class TestMasterGenesisOrchestrator(unittest.TestCase):
    def test_evaluate_venture(self) -> None:
        orchestrator = MasterGenesisOrchestrator()
        result = orchestrator.evaluate_venture("AI Note Assistant")
        self.assertIn("idea", result)
        self.assertIn("decision", result)
        self.assertIn("validation", result)
        self.assertIn("opportunities", result)
        self.assertIn("revenue", result)
        self.assertIn("deployment", result)
        self.assertIn("growth", result)

    def test_memory_records_decision(self) -> None:
        orchestrator = MasterGenesisOrchestrator()
        with patch.object(orchestrator.founder_memory, "record_decision") as mock:
            orchestrator.evaluate_venture("AI Note Assistant")
            mock.assert_called_once()
''',
)

write(
    "test_cli.py",
    '''"""Tests for the CLI entry point."""

import json
import unittest
from io import StringIO
from unittest.mock import patch

from genesis.__main__ import main


class TestCLI(unittest.TestCase):
    def test_cli_analyze(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(["analyze", "AI Customer Support"])
            output = mock_stdout.getvalue()
        result = json.loads(output)
        self.assertIn("idea", result)
        self.assertIn("decision", result)
''',
)

print("Test suite created.")
