class ToolRecommender:
    def recommend_for_agent(self, agent_role: str) -> list:
        return ["GitHub", "Anthropic API"] if agent_role == "coding" else ["Supabase"]
