import unittest
from venture_pipeline.pipeline.pipeline_orchestrator import PipelineOrchestrator
class TestVenturePipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        po = PipelineOrchestrator()
        res = po.run_pipeline("AI Medical SaaS")
        self.assertEqual(res["final_stage"], "BUILD")
if __name__ == "__main__":
    unittest.main()
