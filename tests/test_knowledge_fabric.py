import unittest
from knowledge_fabric.core.knowledge_orchestrator import KnowledgeOrchestrator
class TestKnowledgeFabric(unittest.TestCase):
    def test_orchestration(self):
        ko = KnowledgeOrchestrator()
        res = ko.orchestrate_knowledge("Unify All Subsystems")
        self.assertEqual(res["status"], "FABRIC_READY")
if __name__ == "__main__":
    unittest.main()
