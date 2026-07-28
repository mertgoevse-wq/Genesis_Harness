"""Tests for validation_engine subsystem."""

import unittest

from validation_engine.validation_loop import ValidationLoop


class TestValidationLoop(unittest.TestCase):
    def setUp(self):
        self.loop = ValidationLoop()

    def test_run_returns_verdict(self):
        result = self.loop.run(
            "AI note assistant",
            {
                "demand_score": 80.0,
                "differentiation_score": 75.0,
                "monetization_score": 80.0,
                "average_price": 29.0,
                "willingness_to_pay": 60.0,
            },
        )
        self.assertIn(result["verdict"], ("BUILD", "PIVOT/REFINE", "ABANDON"))
        self.assertIn("experiments", result)
        self.assertIn("recommendation", result)
        self.assertGreater(len(result["experiments"]["items"]), 0)

    def test_memory_records_run(self):
        self.loop.run("test idea", {"demand_score": 80.0})
        self.assertEqual(len(self.loop.memory), 1)


if __name__ == "__main__":
    unittest.main()
