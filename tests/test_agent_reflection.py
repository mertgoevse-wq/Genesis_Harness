import unittest
from agent_runtime.reflection.performance_review import PerformanceReview
class TestAgentReflection(unittest.TestCase):
    def test_reflection(self):
        pr = PerformanceReview()
        res = pr.review_execution("CodingAgent")
        self.assertGreater(res["score"], 90.0)
if __name__ == "__main__":
    unittest.main()
