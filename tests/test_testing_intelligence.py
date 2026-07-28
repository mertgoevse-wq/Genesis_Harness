import unittest
from testing_intelligence.coverage_analyzer import CoverageAnalyzer
class TestTestingIntelligence(unittest.TestCase):
    def test_coverage(self):
        ca = CoverageAnalyzer()
        cov = ca.get_coverage()
        self.assertGreater(cov, 95.0)
if __name__ == "__main__":
    unittest.main()
