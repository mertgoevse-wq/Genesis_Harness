import unittest
from agent_runtime.telemetry.metrics_collector import MetricsCollector
class TestRuntimeIntegration(unittest.TestCase):
    def test_metrics(self):
        mc = MetricsCollector()
        m = mc.get_metrics()
        self.assertIn("latency_ms", m)
if __name__ == "__main__":
    unittest.main()
