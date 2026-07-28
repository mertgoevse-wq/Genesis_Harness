class KnowledgeGraphEngine:
    def __init__(self):
        self.relationships = []

    def add_relation(self, source: str, target: str, rel_type: str):
        self.relationships.append({"source": source, "target": target, "type": rel_type})

    def recommend_best_agents(self, task_type: str) -> list:
        if "medical" in task_type.lower() or "saas" in task_type.lower():
            return ["CEO", "Healthcare Researcher", "Compliance Analyst", "Backend Engineer", "Security Auditor"]
        return ["coding", "architect", "qa"]
