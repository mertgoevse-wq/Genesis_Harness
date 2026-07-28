import unittest
from orchestrator.master_orchestrator import MasterGenesisOrchestrator
class TestMasterOrchestrator(unittest.TestCase):
    def test_full_cycle(self):
        mo = MasterGenesisOrchestrator()
        res = mo.run_full_autonomous_cycle("Build AI Healthcare SaaS")
        self.assertEqual(res["status"], "COMPLETED")
        self.assertGreater(res["quality"]["Overall Score"], 90.0)
if __name__ == "__main__":
    unittest.main()
