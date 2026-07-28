import os
import unittest
from mvp_builder.builder_engine import MVPBuilderEngine
class TestGeneratedMVPWorkspace(unittest.TestCase):
    def test_mvp_structure(self):
        mbe = MVPBuilderEngine()
        res = mbe.build_mvp("Legal Doc AI", r"c:\Genesis_Harness\generated_products")
        self.assertIn("README.md", res["files_created"])
        self.assertIn("backend/main.py", res["files_created"])
if __name__ == "__main__":
    unittest.main()
