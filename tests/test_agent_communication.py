import unittest
from agent_collaboration.message_bus import MessageBus
class TestAgentCommunication(unittest.TestCase):
    def test_message_bus(self):
        mb = MessageBus()
        msg = mb.publish_message("CEO", "CTO", {"prd": "Medical SaaS"})
        self.assertEqual(msg["sender"], "CEO")
if __name__ == "__main__":
    unittest.main()
