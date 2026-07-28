import os
import sys

# Ensure repo root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from product_launch.launch_engine import ProductLaunchEngine

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Create an AI SaaS for automated customer support"
    engine = ProductLaunchEngine()
    out_dir = os.path.join(repo_root, "generated_products")
    result = engine.launch_product(prompt, out_dir)
    
    print("=" * 60)
    print("GENESIS AUTONOMOUS PRODUCT LAUNCH RESULT:")
    print(f"Product: {result['product_name']}")
    print(f"Directory: {result['product_dir']}")
    print(f"Status: {result['status']}")
    print(f"Files Generated: {len(result['files_created'])}")
    print(f"Quality Score: {result['quality_score']}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
