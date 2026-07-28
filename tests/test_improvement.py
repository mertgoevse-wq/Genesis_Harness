"""Tests for genesis.improvement."""

import unittest

from genesis.improvement import (
    AutonomousImprovementLoop,
    ImprovementEngine,
    WeaknessDetector,
)


class TestImprovement(unittest.TestCase):
    def test_engine_analyze(self) -> None:
        engine = ImprovementEngine()
        result = engine.analyze({"quality_score": 90.0, "tests": {"passed": True}})
        self.assertEqual(result["status"], "ANALYZED")
        self.assertIn("weaknesses", result)

    def test_autonomous_loop(self) -> None:
        loop = AutonomousImprovementLoop()
        result = loop.run({"quality_score": 90.0, "tests": {"passed": True}})
        self.assertEqual(result["status"], "IMPROVEMENT_LOOP_RUN")
        self.assertIn("weaknesses", result)

    def test_weakness_detector(self) -> None:
        detector = WeaknessDetector()
        weaknesses = detector.detect({"quality_score": 70.0, "tests": {"passed": False}})
        self.assertGreater(len(weaknesses), 0)
