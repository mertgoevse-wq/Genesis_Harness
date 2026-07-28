import unittest
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
