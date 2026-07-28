"""Tests for autonomous improvement loop."""

import unittest

from self_improvement.autonomous_improvement_loop import AutonomousImprovementLoop


class TestAutonomousImprovementLoop(unittest.TestCase):
    def setUp(self):
        self.loop = AutonomousImprovementLoop()

    def test_run_returns_audit(self):
        result = self.loop.run({"quality_score": 90.0, "tests": {"passed": True}})
        self.assertEqual(result["status"], "IMPROVEMENT_LOOP_RUN")
        self.assertIn("audit", result)
        self.assertIn("weaknesses", result)
        self.assertIn("prioritized_tasks", result)


if __name__ == "__main__":
    unittest.main()
