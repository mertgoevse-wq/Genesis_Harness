import os
import unittest
from product_launch.launch_engine import ProductLaunchEngine

class TestProductLaunchEngine(unittest.TestCase):
    def test_launch(self):
        ple = ProductLaunchEngine()
        res = ple.launch_product("Legal Doc AI SaaS", r"c:\Genesis_Harness\generated_products")
        self.assertEqual(res["status"], "LAUNCH_PACKAGE_CREATED")

if __name__ == "__main__":
    unittest.main()
