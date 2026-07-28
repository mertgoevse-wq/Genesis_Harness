import unittest
from knowledge_fabric.connectors.agent_connector import AgentConnector
class TestAgentIntegration(unittest.TestCase):
    def test_agents(self):
        ac = AgentConnector()
        agents = ac.connect_agents()
        self.assertIn("Architect", agents)
if __name__ == "__main__":
    unittest.main()
