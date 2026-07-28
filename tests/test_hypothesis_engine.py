import unittest
from research_intelligence.hypothesis.hypothesis_generator import HypothesisGenerator
class TestHypothesisEngine(unittest.TestCase):
    def test_generation(self):
        hg = HypothesisGenerator()
        h = hg.generate_hypotheses()
        self.assertGreater(len(h), 0)
if __name__ == "__main__":
    unittest.main()
