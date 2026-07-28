from typing import List

class DynamicSkillLoader:
    def __init__(self):
        self.mappings = {
            "coding": ["software-engineering", "testing", "security"],
            "architect": ["architecture", "software-engineering"],
            "market-research": ["market-analysis", "customer-discovery"],
            "product-manager": ["product-validation", "pricing"],
            "qa": ["testing", "security"],
            "growth": ["marketing", "sales"]
        }

    def load_skills_for_agent(self, agent_name: str) -> List[str]:
        return self.mappings.get(agent_name, ["software-engineering"])
