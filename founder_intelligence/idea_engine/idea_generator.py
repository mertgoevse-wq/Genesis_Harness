import os
from typing import List, Dict, Any

class IdeaGenerator:
    def generate_startup_ideas(self, prompt: str = "Find profitable AI businesses") -> List[Dict[str, Any]]:
        ideas = []
        for i in range(1, 11):
            ideas.append({
                "id": i,
                "title": f"AI Startup Candidate #{i}",
                "problem_score": 9,
                "market_score": 9,
                "competition_score": 7,
                "monetization_score": 9,
                "build_difficulty": 4,
                "ai_advantage_score": 9,
                "startup_score": 85 + (i % 5)
            })
        return ideas

    def save_candidates(self, ideas: list, output_dir: str = "docs/products/candidates") -> str:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "2026_top_candidates.json")
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ideas, f, indent=2)
        return path
