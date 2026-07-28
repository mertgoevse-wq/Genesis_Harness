"""Tests for MVP builder."""

import os
import shutil
import tempfile
import unittest

from mvp_builder.builder_engine import MVPBuilderEngine


class TestMVPBuilderEngine(unittest.TestCase):
    def setUp(self):
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_build_mvp_creates_files(self):
        engine = MVPBuilderEngine()
        result = engine.build_mvp("AI Note Assistant", self.output_dir)
        self.assertEqual(result["status"], "MVP_BUILT_AND_READY")
        self.assertTrue(os.path.exists(result["mvp_dir"]))
        self.assertIn("backend/main.py", result["files_created"])
        self.assertIn("frontend/index.html", result["files_created"])
        self.assertIn("docker/Dockerfile", result["files_created"])

    def test_backend_main_contains_fastapi(self):
        engine = MVPBuilderEngine()
        result = engine.build_mvp("Test Product", self.output_dir)
        main_path = os.path.join(result["mvp_dir"], "backend", "main.py")
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("FastAPI", content)
        self.assertIn("health", content)


if __name__ == "__main__":
    unittest.main()
