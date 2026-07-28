from harvester.knowledge_graph.graph import KnowledgeGraph

class AgentMemory:
    def __init__(self, kg: KnowledgeGraph = None):
        self.kg = kg or KnowledgeGraph()
        self.retrospectives = []

    def log_project_retrospective(self, project_name: str, worked: list, failed: list, skills_used: list, optimal_model: str):
        retro = {
            "project": project_name,
            "worked": worked,
            "failed": failed,
            "skills_used": skills_used,
            "optimal_model": optimal_model
        }
        self.retrospectives.append(retro)
        
        # Connect with Knowledge Graph
        self.kg.add_node(f"project_{project_name}", "Workflow", {"name": project_name})
        for skill in skills_used:
            self.kg.add_node(f"skill_{skill}", "Skill", {"name": skill})
            self.kg.add_edge(f"project_{project_name}", f"skill_{skill}", "USED_SKILL")

        return retro
