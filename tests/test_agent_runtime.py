import unittest
from agent_runtime.core.agent_executor import AgentExecutor
class TestAgentRuntime(unittest.TestCase):
    def test_executor(self):
        ae = AgentExecutor()
        res = ae.execute_agent("Architect", "Design Microservices")
        self.assertEqual(res["state"], "COMPLETED")
if __name__ == "__main__":
    unittest.main()
