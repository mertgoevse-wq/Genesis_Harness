import unittest
import os
from product_factory.pipeline.product_lifecycle import ProductLifecycleEngine, ProductState
from product_factory.product_management.prd_generator import PRDGenerator

class TestProductFactory(unittest.TestCase):
    def test_lifecycle_transitions(self):
        engine = ProductLifecycleEngine("ReviewPilot AI")
        self.assertEqual(engine.state, ProductState.IDEA)
        
        res = engine.transition_to(ProductState.RESEARCHING)
        self.assertEqual(res["state"], "RESEARCHING")

    def test_prd_generation(self):
        gen = PRDGenerator(output_dir="tests/test_products")
        out_dir = gen.generate_prd_package("AutoDoc SaaS", {"summary": "Automated documentation tool"})
        self.assertTrue(os.path.exists(os.path.join(out_dir, "PRD.md")))
        self.assertTrue(os.path.exists(os.path.join(out_dir, "Technical_Architecture.md")))

if __name__ == "__main__":
    unittest.main()
