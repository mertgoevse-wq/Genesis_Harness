"""Tests for the self_improvement subsystem."""

import unittest
from self_improvement.improvement_engine import ImprovementEngine


class TestSelfImprovement(unittest.TestCase):
    def setUp(self):
        self.engine = ImprovementEngine()

    def test_analyze_with_weakness(self):
        result = self.engine.analyze(
            {
                "quality_score": 50.0,
                "tests": {"passed": False},
                "documentation_updated": False,
            }
        )
        self.assertEqual(result["status"], "ANALYZED")
        self.assertGreater(len(result["weaknesses"]), 0)
        self.assertGreater(len(result["tasks"]), 0)
        self.assertIn("improvement_score", result)

    def test_analyze_with_good_state(self):
        result = self.engine.analyze(
            {
                "quality_score": 95.0,
                "tests": {"passed": True},
                "documentation_updated": True,
            }
        )
        self.assertEqual(result["status"], "ANALYZED")
        self.assertGreaterEqual(result["improvement_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
