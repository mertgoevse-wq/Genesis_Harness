import os
import sys

# Ensure repo root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from mvp_builder.builder_engine import MVPBuilderEngine

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Create an AI customer support SaaS"
    engine = MVPBuilderEngine()
    out_dir = os.path.join(repo_root, "generated_products")
    result = engine.build_mvp(prompt, out_dir)
    
    print("=" * 60)
    print("GENESIS AUTONOMOUS MVP BUILDER RESULT:")
    print(f"Product: {result['product_name']}")
    print(f"MVP Directory: {result['mvp_dir']}")
    print(f"Status: {result['status']}")
    print(f"Codebase Files Generated: {len(result['files_created'])}")
    print(f"Quality Score: {result['quality_score']}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
