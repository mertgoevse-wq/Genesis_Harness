import unittest
from knowledge_fabric.reasoning.recommendation_engine import RecommendationEngine
class TestModelRouting(unittest.TestCase):
    def test_routing(self):
        re = RecommendationEngine()
        recs = re.recommend()
        self.assertGreater(len(recs), 0)
if __name__ == "__main__":
    unittest.main()
