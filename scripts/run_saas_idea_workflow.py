import os
import sys
import importlib.util

# Ensure repo root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

api_path = os.path.join(repo_root, "control-center", "backend", "api_server.py")
spec = importlib.util.spec_from_file_location("api_server", api_path)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)
ControlCenterAPI = api_module.ControlCenterAPI

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Create a profitable AI SaaS idea in Healthcare Automation"
    api = ControlCenterAPI()
    print(f"[User Workflow] Triggering AI SaaS Venture Creation for prompt: '{prompt}'")
    res = api.execute_workflow(prompt)
    print("=" * 60)
    print("GENESIS CONTROL CENTER - WORKFLOW EXECUTION SUMMARY:")
    print(f"Goal: {res['goal']}")
    print(f"Status: {res['status']}")
    print(f"Overall Quality Score: {res['quality']['Overall Score']}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
