import os
import unittest
from product_launch.launch_engine import ProductLaunchEngine

class TestGeneratedProductWorkspace(unittest.TestCase):
    def test_workspace_files(self):
        ple = ProductLaunchEngine()
        res = ple.launch_product("Customer Support AI", r"c:\Genesis_Harness\generated_products")
        self.assertIn("README.md", res["files_created"])
        self.assertIn("BUSINESS_PLAN.md", res["files_created"])

if __name__ == "__main__":
    unittest.main()
