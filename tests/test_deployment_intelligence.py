"""Tests for deployment_intelligence subsystem."""

import unittest

from deployment_intelligence.deployment_planner import DeploymentPlanner


class TestDeploymentPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = DeploymentPlanner()

    def test_plan_returns_providers(self):
        result = self.planner.plan(
            "ai-note-assistant",
            {"frontend": True, "backend": True, "database": True},
        )
        self.assertEqual(result["status"], "PLANNED")
        self.assertIn("docker", result["providers"])
        self.assertIn("vercel", result["providers"])
        self.assertIn("supabase", result["providers"])
        self.assertIn("artifacts", result)

    def test_docker_artifact_has_dockerfile(self):
        result = self.planner.plan(
            "ai-note-assistant",
            {"frontend": True, "backend": True, "database": True},
        )
        docker = result["artifacts"]["docker"]
        self.assertIn("Dockerfile", docker)
        self.assertIn("docker-compose.yml", docker)
        self.assertIn("PRODUCTION_CHECKLIST.md", docker)


if __name__ == "__main__":
    unittest.main()
