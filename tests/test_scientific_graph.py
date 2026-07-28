import unittest
from knowledge_graph.relationship_engine import KnowledgeGraphEngine
class TestScientificGraph(unittest.TestCase):
    def test_graph(self):
        kg = KnowledgeGraphEngine()
        kg.add_relation("Paper:arXiv2607", "Theory:AgenticAI", "SUPPORTS")
        self.assertEqual(len(kg.relationships), 1)
if __name__ == "__main__":
    unittest.main()
