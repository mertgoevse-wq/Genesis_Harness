import unittest
from venture_execution.orchestrator.venture_executor import VentureExecutor
class TestVentureExecution(unittest.TestCase):
    def test_executor(self):
        ve = VentureExecutor()
        res = ve.execute_venture("Create a healthcare AI SaaS")
        self.assertEqual(res["status"], "EXECUTED")
if __name__ == "__main__":
    unittest.main()
