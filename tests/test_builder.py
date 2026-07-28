"""Tests for genesis.builder."""

import os
import shutil
import tempfile
import unittest

from genesis.builder import DeploymentPlanner, MVPBuilderEngine


class TestMVPBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_build_mvp_creates_files(self) -> None:
        engine = MVPBuilderEngine()
        result = engine.build_mvp("AI Note Assistant", self.output_dir)
        self.assertEqual(result["status"], "MVP_BUILT_AND_READY")
        self.assertTrue(os.path.exists(result["mvp_dir"]))
        self.assertIn("backend/main.py", result["files_created"])
        self.assertIn("frontend/index.html", result["files_created"])
        self.assertIn("docker/Dockerfile", result["files_created"])

    def test_backend_main_contains_fastapi(self) -> None:
        engine = MVPBuilderEngine()
        result = engine.build_mvp("Test Product", self.output_dir)
        main_path = os.path.join(result["mvp_dir"], "backend", "main.py")
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("FastAPI", content)
        self.assertIn("health", content)


class TestDeploymentPlanner(unittest.TestCase):
    def test_plan_returns_providers(self) -> None:
        planner = DeploymentPlanner()
        result = planner.plan(
            "ai-note-assistant",
            {"frontend": True, "backend": True, "database": True},
        )
        self.assertEqual(result["status"], "PLANNED")
        self.assertIn("docker", result["providers"])
        self.assertIn("artifacts", result)
