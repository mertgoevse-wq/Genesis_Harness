class IdeaRanker:
    def rank_ideas(self, ideas: list) -> list: return sorted(ideas, key=lambda x: x.get("startup_score", 0), reverse=True)
