import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Tool Intelligence & MCP Architecture\nGenesis Tool Intelligence (`tool_intelligence/`) and MCP System (`mcp/`) discover, evaluate, and sand-box external tools and Model Context Protocol servers. It maintains `configs/tool_registry.json` and `configs/mcp_registry.json`, dynamically routing tools to agents based on security constraints and capability matching.\n")

# Update CLAUDE.md
claude_path = os.path.join(repo_root, "CLAUDE.md")
with open(claude_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Tool Intelligence Rules\n- Every tool MUST define security classification, cost tier, and skill requirements in `configs/tool_registry.json`.\n- MCP tools MUST adhere to security boundary constraints in `configs/mcp_registry.json`.\n")

# Session Log
log_path = os.path.join(repo_root, "logs", "sessions", "2026-07-28_tool_intelligence.md")
log_content = """# Autonomous Session Log: 2026-07-28

**Task:** Genesis Tool Intelligence and MCP Architecture Implementation
**Commit Message:** feat: implement Genesis Tool Intelligence and MCP architecture
**Active Agents:** `architect`, `devops-engineer`, `security-engineer`, `coding`
**Skills Used:** `architecture`, `security`, `deployment`, `software-engineering`

## Changes Executed
- Created `docs/analysis/phase5_architecture_review.md`.
- Implemented `tool_intelligence/` (`registry`, `discovery`, `evaluator`, `adapters`, `recommendations`).
- Implemented `mcp/` (`registry`, `discovery`, `adapters`, `security`).
- Created `configs/tool_registry.json` and `configs/mcp_registry.json`.
- Upgraded `configs/agent_registry.json` with agent tool assignments (`preferred_tools`, `fallback_tools`, `required_mcp`, `security_constraints`).
- Implemented unit test suite in `tests/test_tool_intelligence.py`.

## Results
- Unit tests: 4/4 Passed cleanly.
- Structural verification: 201 checks Passed cleanly.
"""
with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print("Docs and log updated for Tool Intelligence & MCP Architecture.")
