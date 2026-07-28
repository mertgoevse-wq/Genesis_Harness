import unittest
from agent_factory.team_builder import TeamBuilder
class TestAgentFactory(unittest.TestCase):
    def test_team_assembly(self):
        tb = TeamBuilder()
        team = tb.assemble_team("Build an AI medical SaaS")
        self.assertIn("Compliance Analyst", team["assigned_agents"])
if __name__ == "__main__":
    unittest.main()
