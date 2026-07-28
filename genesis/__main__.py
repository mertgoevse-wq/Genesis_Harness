"""CLI entry point for Genesis."""

import argparse
import json
import sys
from typing import List

from genesis.orchestrator import MasterGenesisOrchestrator


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genesis AI Venture Operating System")
    parser.add_argument("command", choices=["analyze"], help="Command to run")
    parser.add_argument("prompt", help="Venture idea to analyze")
    parser.add_argument(
        "--context",
        default="{}",
        help="JSON context for the analysis",
    )
    args = parser.parse_args(argv)

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON context: {exc}", file=sys.stderr)
        return 1

    orchestrator = MasterGenesisOrchestrator()
    result = orchestrator.evaluate_venture(args.prompt, context)
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
