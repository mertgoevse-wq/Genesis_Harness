import unittest
from core.model_router.model_performance_tracker import ModelPerformanceTracker
class TestModelRouterV2(unittest.TestCase):
    def test_complexity_routing(self):
        mpt = ModelPerformanceTracker()
        model = mpt.route_by_complexity("Architecture", 0.9)
        self.assertEqual(model, "Claude Opus")
if __name__ == "__main__":
    unittest.main()
