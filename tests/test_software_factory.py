import unittest
from software_factory.factory.software_factory_engine import SoftwareFactoryEngine
class TestSoftwareFactory(unittest.TestCase):
    def test_factory_build(self):
        sfe = SoftwareFactoryEngine()
        res = sfe.build_software("Build a SaaS app for customer support")
        self.assertEqual(res["status"], "BUILT")
if __name__ == "__main__":
    unittest.main()
