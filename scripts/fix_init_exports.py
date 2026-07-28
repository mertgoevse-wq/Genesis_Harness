"""Make package __init__.py re-exports ruff-clean with explicit aliases."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FILES = {
    REPO_ROOT / "genesis/decision/__init__.py": """\"\"\"Decision subsystem for Genesis.\"\"\"
from .engine import VentureDecision as VentureDecision
from .engine import VentureDecisionEngine as VentureDecisionEngine
from .validation import ProductValidationEngine as ProductValidationEngine
from .validation import ValidationDecision as ValidationDecision
from .validation_scoring import ValidationScorer as ValidationScorer

__all__ = [
    "VentureDecision",
    "VentureDecisionEngine",
    "ProductValidationEngine",
    "ValidationDecision",
    "ValidationScorer",
]
""",
    REPO_ROOT / "genesis/intelligence/__init__.py": """\"\"\"Intelligence subsystem for Genesis.\"\"\"
from .connectors.base import ConnectorResult as ConnectorResult
from .connectors.base import LiveConnector as LiveConnector
from .connectors.orchestrator import LiveIntelligenceOrchestrator as LiveIntelligenceOrchestrator
from .discovery.competitors import Competitor as Competitor
from .discovery.competitors import CompetitorAnalyzer as CompetitorAnalyzer
from .discovery.market_research import MarketResearchConnector as MarketResearchConnector
from .discovery.market_research import MarketSignal as MarketSignal
from .discovery.trends import Trend as Trend
from .discovery.trends import TrendMonitor as TrendMonitor
from .opportunity import Opportunity as Opportunity
from .opportunity import OpportunityDetector as OpportunityDetector

__all__ = [
    "ConnectorResult",
    "LiveConnector",
    "LiveIntelligenceOrchestrator",
    "Competitor",
    "CompetitorAnalyzer",
    "MarketResearchConnector",
    "MarketSignal",
    "Trend",
    "TrendMonitor",
    "Opportunity",
    "OpportunityDetector",
]
""",
    REPO_ROOT / "genesis/revenue/__init__.py": """\"\"\"Revenue subsystem for Genesis.\"\"\"
from .acquisition import AcquisitionStrategy as AcquisitionStrategy
from .experiments import GrowthExperiment as GrowthExperiment
from .experiments import GrowthExperimentEngine as GrowthExperimentEngine
from .pricing import PricingEngine as PricingEngine
from .pricing import PricingTier as PricingTier
from .subscriptions import SubscriptionModelSelector as SubscriptionModelSelector

__all__ = [
    "AcquisitionStrategy",
    "GrowthExperiment",
    "GrowthExperimentEngine",
    "PricingEngine",
    "PricingTier",
    "SubscriptionModelSelector",
]
""",
    REPO_ROOT / "genesis/growth/__init__.py": """\"\"\"Growth subsystem for Genesis.\"\"\"
from .channels import ChannelAnalyzer as ChannelAnalyzer
from .customer import CustomerIntelligenceEngine as CustomerIntelligenceEngine
from .customer import CustomerPersona as CustomerPersona
from .customer import IdealCustomerProfile as IdealCustomerProfile
from .engine import GrowthEngine as GrowthEngine
from .engine import GrowthStrategy as GrowthStrategy
from .loops import GrowthLoops as GrowthLoops
from .seo import SEOOpportunityEngine as SEOOpportunityEngine
from .validation_loop import ValidationExperiment as ValidationExperiment
from .validation_loop import ValidationLoop as ValidationLoop

__all__ = [
    "ChannelAnalyzer",
    "CustomerIntelligenceEngine",
    "CustomerPersona",
    "IdealCustomerProfile",
    "GrowthEngine",
    "GrowthStrategy",
    "GrowthLoops",
    "SEOOpportunityEngine",
    "ValidationExperiment",
    "ValidationLoop",
]
""",
    REPO_ROOT / "genesis/builder/__init__.py": """\"\"\"Builder subsystem for Genesis.\"\"\"
from .deploy import DeploymentPlanner as DeploymentPlanner
from .mvp import MVPBuilderEngine as MVPBuilderEngine

__all__ = [
    "DeploymentPlanner",
    "MVPBuilderEngine",
]
""",
    REPO_ROOT / "genesis/memory/__init__.py": """\"\"\"Memory subsystem for Genesis.\"\"\"
from .founder import FounderDecision as FounderDecision
from .founder import FounderMemoryStore as FounderMemoryStore
from .store import KnowledgeStore as KnowledgeStore

__all__ = [
    "FounderDecision",
    "FounderMemoryStore",
    "KnowledgeStore",
]
""",
    REPO_ROOT / "genesis/improvement/__init__.py": """\"\"\"Improvement subsystem for Genesis.\"\"\"
from .autonomous_loop import AutonomousImprovementLoop as AutonomousImprovementLoop
from .engine import ImprovementEngine as ImprovementEngine
from .evaluator import ImprovementEvaluator as ImprovementEvaluator
from .task_prioritizer import ImprovementTask as ImprovementTask
from .task_prioritizer import TaskPrioritizer as TaskPrioritizer
from .weakness_detector import Weakness as Weakness
from .weakness_detector import WeaknessDetector as WeaknessDetector

__all__ = [
    "AutonomousImprovementLoop",
    "ImprovementEngine",
    "ImprovementEvaluator",
    "ImprovementTask",
    "TaskPrioritizer",
    "Weakness",
    "WeaknessDetector",
]
""",
}

for path, content in FILES.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print("Package __init__ exports updated.")
