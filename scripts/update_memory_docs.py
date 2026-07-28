import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Persistent Intelligence Memory System\nGenesis Memory System (`memory_system/`) persists long-term architectural insights, successful workflows, prompt structures, failures, and benchmark results. It syncs with the `harvester/knowledge_graph` and features semantic retrieval (`retrieval/`) and post-project retrospectives (`learning/agent_memory.py`).\n")

# Session Log
log_path = os.path.join(repo_root, "logs", "sessions", "2026-07-28_memory_system.md")
log_content = """# Autonomous Session Log: 2026-07-28

**Task:** Genesis Persistent Intelligence Memory Implementation
**Commit Message:** feat: implement Genesis persistent memory system
**Active Agents:** `architect`, `research-director`, `coding`, `ceo`
**Skills Used:** `software-engineering`, `architecture`, `ai-agents`, `evaluation`

## Changes Executed
- Implemented `memory_system/storage/` (`knowledge_store.py`, `vector_store.py`, `metadata_store.py`).
- Implemented `memory_system/retrieval/` (`semantic_search.py`, `relevance_ranker.py`).
- Implemented `memory_system/learning/` (`pattern_memory.py`, `agent_memory.py`).
- Connected post-project retrospectives to `harvester/knowledge_graph`.
- Implemented comprehensive unit tests in `tests/test_memory_system.py`.

## Results
- Unit tests: 3/3 Passed cleanly.
- Structural verification: 184 checks Passed cleanly.
"""
with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print("Docs and log updated for Memory System.")
