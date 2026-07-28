import unittest
from research_benchmarks.benchmark_runner import ResearchBenchmarkRunner
class TestResearchBenchmark(unittest.TestCase):
    def test_novelty(self):
        rbr = ResearchBenchmarkRunner()
        scores = rbr.evaluate_novelty("Autonomous Venture OS")
        self.assertGreater(scores["novelty_score"], 90.0)
if __name__ == "__main__":
    unittest.main()
