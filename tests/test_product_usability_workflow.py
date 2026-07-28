import os
import sys
import unittest
import importlib.util

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_path = os.path.join(repo_root, "control-center", "backend", "api_server.py")
spec = importlib.util.spec_from_file_location("api_server", api_path)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)
ControlCenterAPI = api_module.ControlCenterAPI

class TestProductUsabilityWorkflow(unittest.TestCase):
    def test_saas_workflow(self):
        api = ControlCenterAPI()
        res = api.execute_workflow("Create a profitable AI SaaS idea")
        self.assertEqual(res["status"], "COMPLETED")

if __name__ == "__main__":
    unittest.main()
