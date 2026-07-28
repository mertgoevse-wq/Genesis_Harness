import unittest
from quality_intelligence.quality_evaluator import QualityEvaluator
class TestQualityIntelligence(unittest.TestCase):
    def test_scoring(self):
        qe = QualityEvaluator()
        score = qe.calculate_quality_score({})
        self.assertGreater(score["Overall Score"], 90.0)
if __name__ == "__main__":
    unittest.main()
