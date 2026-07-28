import unittest
from harvester.connectors.multi_source import MultiSourceConnector
from harvester.ranking.scoring import RankingEngine
from harvester.analysis.extractor import PatternExtractor
from harvester.knowledge_graph.graph import KnowledgeGraph
from harvester.recommendation.gip_engine import GIPEngine

class TestHarvesterV2(unittest.TestCase):
    def test_connector(self):
        conn = MultiSourceConnector()
        data = conn.fetch_source_data("GitHub", "Multi-Agent")
        self.assertEqual(len(data), 1)

    def test_ranking(self):
        engine = RankingEngine()
        score = engine.score_repository({"stars": 2500, "forks": 500, "recency_days": 5, "documentation_quality": 0.9})
        self.assertGreater(score, 50.0)

    def test_knowledge_graph(self):
        kg = KnowledgeGraph()
        kg.add_node("agent_1", "Agent", {"name": "TestAgent"})
        kg.add_node("pattern_1", "Pattern", {"name": "TestPattern"})
        kg.add_edge("agent_1", "pattern_1", "USES")
        graph = kg.export_graph()
        self.assertIn("agent_1", graph["nodes"])

if __name__ == "__main__":
    unittest.main()
