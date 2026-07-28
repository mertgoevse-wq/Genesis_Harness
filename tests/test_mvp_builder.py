import os
import unittest
from mvp_builder.builder_engine import MVPBuilderEngine
class TestMVPBuilder(unittest.TestCase):
    def test_build(self):
        mbe = MVPBuilderEngine()
        res = mbe.build_mvp("Customer Support AI", r"c:\Genesis_Harness\generated_products")
        self.assertEqual(res["status"], "MVP_BUILT_AND_READY")
if __name__ == "__main__":
    unittest.main()
