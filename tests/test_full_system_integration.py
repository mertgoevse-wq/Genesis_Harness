import unittest
from orchestrator.master_orchestrator import MasterGenesisOrchestrator
class TestFullSystemIntegration(unittest.TestCase):
    def test_integration(self):
        mo = MasterGenesisOrchestrator()
        res = mo.run_full_autonomous_cycle("Full Integration Test")
        self.assertIn("software", res)
        self.assertIn("research", res)
if __name__ == "__main__":
    unittest.main()
