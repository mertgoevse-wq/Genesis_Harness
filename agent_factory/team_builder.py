from knowledge_graph.relationship_engine import KnowledgeGraphEngine

class TeamBuilder:
    def __init__(self, kg: KnowledgeGraphEngine = None):
        self.kg = kg or KnowledgeGraphEngine()

    def assemble_team(self, user_prompt: str) -> dict:
        recommended_roles = self.kg.recommend_best_agents(user_prompt)
        return {
            "prompt": user_prompt,
            "team_name": f"Dynamic Team for {user_prompt}",
            "assigned_agents": recommended_roles
        }
