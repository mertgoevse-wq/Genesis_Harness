"""Tests for the deployment_intelligence subsystem."""

import unittest
from deployment_intelligence.deployment_planner import DeploymentPlanner


class TestDeploymentIntelligence(unittest.TestCase):
    def setUp(self):
        self.planner = DeploymentPlanner()

    def test_plan_returns_artifacts(self):
        plan = self.planner.plan(
            "reviewpilot",
            requirements={
                "frontend": True,
                "backend": True,
                "database": True,
            },
        )
        self.assertEqual(plan["status"], "PLANNED")
        self.assertIn("providers", plan)
        self.assertIn("artifacts", plan)
        self.assertIn("docker", plan["providers"])
        self.assertIn("docker", plan["artifacts"])

    def test_plan_with_no_requirements_defaults(self):
        plan = self.planner.plan("minimal", requirements={})
        self.assertEqual(plan["status"], "PLANNED")
        self.assertGreater(len(plan["providers"]), 0)


if __name__ == "__main__":
    unittest.main()
