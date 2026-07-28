import unittest
from knowledge_graph.relationship_engine import KnowledgeGraphEngine
class TestKnowledgeGraph(unittest.TestCase):
    def test_recommendations(self):
        kg = KnowledgeGraphEngine()
        rec = kg.recommend_best_agents("medical saas")
        self.assertIn("Healthcare Researcher", rec)
if __name__ == "__main__":
    unittest.main()
