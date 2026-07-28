import unittest
from agent_collaboration.team_coordinator import TeamCoordinator
class TestAgentCollaboration(unittest.TestCase):
    def test_handoff(self):
        tc = TeamCoordinator()
        res = tc.handoff_task("CEO", "CTO", {"prd": "Medical SaaS"})
        self.assertEqual(res["status"], "HANDOFF_SUCCESSFUL")
if __name__ == "__main__":
    unittest.main()
