import os
import json

repo_root = "c:\\Genesis_Harness"

# Directories
dirs = [
    "memory_system/storage",
    "memory_system/retrieval",
    "memory_system/learning",
    "tests"
]
for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Genesis Memory System Module\n")

# 1. Storage: memory_system/storage/knowledge_store.py
ks_code = '''import json
import os
from typing import Dict, Any, List

class KnowledgeStore:
    def __init__(self, db_path: str = "memory_system/storage/knowledge_db.json"):
        self.db_path = db_path
        self.records: List[Dict[str, Any]] = self._load()

    def _load(self) -> list:
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_record(self, category: str, data: dict):
        record = {
            "id": len(self.records) + 1,
            "category": category,
            "data": data
        }
        self.records.append(record)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
        return record
'''
with open(os.path.join(repo_root, "memory_system", "storage", "knowledge_store.py"), "w", encoding="utf-8") as f:
    f.write(ks_code)

# Vector Store: memory_system/storage/vector_store.py
vs_code = '''from typing import List, Dict, Any

class VectorStore:
    def __init__(self):
        self.index = []

    def add_vector(self, item_id: str, text: str, embedding: List[float] = None):
        self.index.append({"id": item_id, "text": text, "embedding": embedding or [0.1]*10})

    def search_similar(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Simplified similarity ranking
        results = []
        for item in self.index:
            if any(w.lower() in item["text"].lower() for w in query_text.split()):
                results.append(item)
        return results[:top_k]
'''
with open(os.path.join(repo_root, "memory_system", "storage", "vector_store.py"), "w", encoding="utf-8") as f:
    f.write(vs_code)

# Metadata Store: memory_system/storage/metadata_store.py
with open(os.path.join(repo_root, "memory_system", "storage", "metadata_store.py"), "w", encoding="utf-8") as f:
    f.write('''class MetadataStore:\n    def __init__(self):\n        self.tags = {}\n''')

# 2. Retrieval: memory_system/retrieval/semantic_search.py & relevance_ranker.py
search_code = '''from memory_system.storage.vector_store import VectorStore

class SemanticSearch:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def query(self, search_term: str) -> list:
        return self.vector_store.search_similar(search_term)
'''
with open(os.path.join(repo_root, "memory_system", "retrieval", "semantic_search.py"), "w", encoding="utf-8") as f:
    f.write(search_code)

with open(os.path.join(repo_root, "memory_system", "retrieval", "relevance_ranker.py"), "w", encoding="utf-8") as f:
    f.write('''class RelevanceRanker:\n    def rank(self, results: list) -> list:\n        return sorted(results, key=lambda x: len(x.get("text", "")), reverse=True)\n''')

# 3. Learning & Retrospectives: memory_system/learning/agent_memory.py & pattern_memory.py
retrospective_code = '''from harvester.knowledge_graph.graph import KnowledgeGraph

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
'''
with open(os.path.join(repo_root, "memory_system", "learning", "agent_memory.py"), "w", encoding="utf-8") as f:
    f.write(retrospective_code)

with open(os.path.join(repo_root, "memory_system", "learning", "pattern_memory.py"), "w", encoding="utf-8") as f:
    f.write('''class PatternMemory:\n    def __init__(self):\n        self.patterns = []\n''')

# 4. Unit Tests: tests/test_memory_system.py
test_memory_code = '''import unittest
from memory_system.storage.knowledge_store import KnowledgeStore
from memory_system.storage.vector_store import VectorStore
from memory_system.retrieval.semantic_search import SemanticSearch
from memory_system.learning.agent_memory import AgentMemory

class TestMemorySystem(unittest.TestCase):
    def test_knowledge_store(self):
        ks = KnowledgeStore(db_path="tests/test_db.json")
        rec = ks.save_record("Workflow", {"name": "Test Workflow"})
        self.assertEqual(rec["category"], "Workflow")

    def test_vector_search(self):
        vs = VectorStore()
        vs.add_vector("1", "Architecture decision for Claude Opus")
        search = SemanticSearch(vs)
        res = search.query("Architecture")
        self.assertEqual(len(res), 1)

    def test_agent_retrospective(self):
        mem = AgentMemory()
        retro = mem.log_project_retrospective(
            project_name="ReviewPilot AI",
            worked=["Free tier hosting", "Claude 3.5 Haiku"],
            failed=["Complex regex"],
            skills_used=["software-engineering", "marketing"],
            optimal_model="Claude Sonnet 4.6"
        )
        self.assertEqual(retro["optimal_model"], "Claude Sonnet 4.6")
        self.assertIn("project_ReviewPilot AI", mem.kg.nodes)

if __name__ == "__main__":
    unittest.main()
'''
with open(os.path.join(repo_root, "tests", "test_memory_system.py"), "w", encoding="utf-8") as f:
    f.write(test_memory_code)

print("Memory System modules and tests successfully built.")
