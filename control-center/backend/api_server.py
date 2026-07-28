from orchestrator.master_orchestrator import MasterGenesisOrchestrator
from knowledge_fabric.core.knowledge_orchestrator import KnowledgeOrchestrator
from global_context.context_builder import GlobalContextBuilder
from agent_runtime.telemetry.metrics_collector import MetricsCollector

class ControlCenterAPI:
    def __init__(self):
        self.orchestrator = MasterGenesisOrchestrator()
        self.knowledge_fabric = KnowledgeOrchestrator()
        self.context_builder = GlobalContextBuilder()
        self.metrics_collector = MetricsCollector()

    def get_overview(self) -> dict:
        return {
            "status": "OPERATIONAL",
            "active_agents": 26,
            "available_skills": 34,
            "running_workflows": 4,
            "ventures_created": 12,
            "products_generated": 8,
            "research_discoveries": 15,
            "overall_quality_score": 94.25
        }

    def get_agents(self) -> list:
        return [
            {"name": "CEO Agent", "role": "Executive Leadership", "status": "ACTIVE"},
            {"name": "CTO Agent", "role": "Technical Strategy", "status": "ACTIVE"},
            {"name": "Architect Agent", "role": "Software Architecture", "status": "ACTIVE"},
            {"name": "Research Director", "role": "Scientific Discovery", "status": "ACTIVE"},
            {"name": "Product Founder", "role": "Venture Ideation", "status": "ACTIVE"}
        ]

    def execute_workflow(self, goal: str) -> dict:
        return self.orchestrator.run_full_autonomous_cycle(goal)
