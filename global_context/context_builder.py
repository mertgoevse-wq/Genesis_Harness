class GlobalContextBuilder:
    def build_context(self, task_prompt: str) -> dict:
        return {
            "task": task_prompt,
            "agents_needed": ["CEO", "CTO", "Architect", "Coding", "QA", "Security"],
            "skills_needed": ["software-architecture", "backend-engineering", "security-engineering"],
            "tools_needed": ["GitHub", "Supabase", "Vercel"],
            "historical_patterns": ["Microservices Blueprint v2"],
            "model_preferences": {"architecture": "Claude Opus", "coding": "Claude Sonnet"}
        }

class GlobalContextRanker:
    def rank_context_items(self, items: list) -> list:
        return sorted(items, key=lambda x: x.get("relevance", 1.0), reverse=True)

class GlobalContextRetriever:
    def retrieve(self, task_prompt: str) -> dict:
        builder = GlobalContextBuilder()
        return builder.build_context(task_prompt)
