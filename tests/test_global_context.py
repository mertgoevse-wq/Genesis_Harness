import unittest
from global_context.context_builder import GlobalContextBuilder
class TestGlobalContext(unittest.TestCase):
    def test_build_context(self):
        gcb = GlobalContextBuilder()
        ctx = gcb.build_context("Build AI SaaS")
        self.assertIn("agents_needed", ctx)
if __name__ == "__main__":
    unittest.main()
