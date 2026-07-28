"""Tests for the master orchestrator integration."""

import unittest
from orchestrator.master_orchestrator import MasterGenesisOrchestrator


class TestMasterOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = MasterGenesisOrchestrator()

    def test_run_full_autonomous_cycle(self):
        result = self.orchestrator.run_full_autonomous_cycle(
            "AI-powered review management SaaS"
        )
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["goal"], "AI-powered review management SaaS")
        self.assertIn("opportunities", result)
        self.assertIn("venture_decision", result)
        self.assertIn("revenue", result)
        self.assertIn("deployment", result)
        self.assertIn("improvement", result)

    def test_build_revenue_intelligence(self):
        revenue = self.orchestrator._build_revenue_intelligence("test")
        self.assertIn("pricing", revenue)
        self.assertIn("subscription_model", revenue)
        self.assertIn("acquisition", revenue)
        self.assertIn("growth_experiments", revenue)


if __name__ == "__main__":
    unittest.main()
