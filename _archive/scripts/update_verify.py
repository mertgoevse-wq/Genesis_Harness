"""Update verify_structure.ps1 for the consolidated Genesis package."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "verify_structure.ps1"

if not SCRIPT.exists():
    raise FileNotFoundError(SCRIPT)

content = SCRIPT.read_text(encoding="utf-8")

required_dirs = [
    ".claude",
    ".claude/agents",
    "agents",
    "skills",
    "prompts",
    "prompts/system_layers",
    "prompts/master_prompts",
    "prompts/generators",
    "prompts/benchmarks",
    "logs",
    "logs/sessions",
    "docs",
    "scripts",
    "configs",
    "templates",
    "genesis",
    "genesis/decision",
    "genesis/decision/scorers",
    "genesis/intelligence",
    "genesis/intelligence/discovery",
    "genesis/intelligence/connectors",
    "genesis/revenue",
    "genesis/growth",
    "genesis/builder",
    "genesis/builder/providers",
    "genesis/memory",
    "genesis/improvement",
    "genesis/api",
    "genesis/core",
    "tests",
]

new_dirs = "\n$RequiredDirectories = @(\n    " + ",\n    ".join(repr(d) for d in required_dirs) + "\n)\n"

content = re.sub(
    r"\$RequiredDirectories = @\([^)]*\)\n",
    new_dirs,
    content,
    flags=re.DOTALL,
)

content = re.sub(
    r"\$RequiredRootFiles = @\([^)]*\)\n",
    "\n$RequiredRootFiles = @(\n    'CLAUDE.md',\n    'README.md',\n    'pyproject.toml'\n)\n",
    content,
    flags=re.DOTALL,
)

SCRIPT.write_text(content, encoding="utf-8")
print("Updated scripts/verify_structure.ps1")
