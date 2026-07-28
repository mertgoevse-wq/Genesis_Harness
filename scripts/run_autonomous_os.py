import os
import sys

# Ensure repo root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from orchestrator.master_orchestrator import MasterGenesisOrchestrator

def main():
    goal = sys.argv[1] if len(sys.argv) > 1 else "Build a production AI SaaS business in Healthcare Automation"
    orchestrator = MasterGenesisOrchestrator()
    result = orchestrator.run_full_autonomous_cycle(goal)
    print("=" * 60)
    print("GENESIS AUTONOMOUS AI OPERATING SYSTEM EXECUTION RESULT:")
    print(f"Goal: {result['goal']}")
    print(f"Status: {result['status']}")
    print(f"Overall Quality Score: {result['quality']['Overall Score']}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
