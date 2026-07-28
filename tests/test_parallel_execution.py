import unittest
from agent_runtime.execution.parallel_executor import ParallelExecutor
class TestParallelExecution(unittest.TestCase):
    def test_parallel(self):
        pe = ParallelExecutor()
        tasks = [{"agent": "MarketResearch", "task": "Scan"}, {"agent": "Architect", "task": "Design"}]
        res = pe.execute_parallel(tasks)
        self.assertEqual(len(res), 2)
if __name__ == "__main__":
    unittest.main()
