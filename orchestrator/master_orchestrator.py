import sys
from genesis_runtime.runtime.engine import GenesisRuntimeEngine
from product_factory.pipeline.product_lifecycle import ProductLifecycleEngine
from founder_intelligence.market_scanner.trend_detector import TrendDetector
from venture_execution.orchestrator.venture_executor import VentureExecutor
from software_factory.factory.software_factory_engine import SoftwareFactoryEngine
from research_intelligence.research_engine.research_orchestrator import ResearchIntelligenceEngine
from quality_intelligence.quality_evaluator import QualityEvaluator

class MasterGenesisOrchestrator:
    def __init__(self):
        self.runtime = GenesisRuntimeEngine()
        self.trend_detector = TrendDetector()
        self.venture_executor = VentureExecutor()
        self.software_factory = SoftwareFactoryEngine()
        self.research_engine = ResearchIntelligenceEngine()
        self.quality_evaluator = QualityEvaluator()

    def run_full_autonomous_cycle(self, goal: str) -> dict:
        print(f"[MasterOrchestrator] Starting autonomous OS cycle for goal: {goal}")
        
        # 1. Product Lifecycle Initialization
        product_lifecycle = ProductLifecycleEngine(product_name=goal)
        
        # 2. Research Intelligence
        research = self.research_engine.analyze_advances(goal)
        
        # 3. Market & Trend Detection
        trends = self.trend_detector.detect_trends(goal) if hasattr(self.trend_detector, 'detect_trends') else {"trends": ["AI SaaS"]}
        
        # 4. Product Lifecycle State
        product = product_lifecycle.get_current_state() if hasattr(product_lifecycle, 'get_current_state') else {"status": "DISCOVERY"}
        
        # 5. Venture Execution
        venture = self.venture_executor.execute_venture(goal)
        
        # 6. Software Factory Development
        software = self.software_factory.build_software(goal)
        
        # 7. Quality & Security Evaluation
        quality = self.quality_evaluator.calculate_quality_score(software)
        
        return {
            "goal": goal,
            "status": "COMPLETED",
            "research": research,
            "trends": trends,
            "product": product,
            "venture": venture,
            "software": software,
            "quality": quality
        }
