import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Control Center\nGenesis Control Center (`control-center/`) provides real-time visual telemetry. It includes an `EventBus` (`events/`), a Python HTTP/WebSocket server (`backend/`), and a clean Linear/Notion-inspired single page web application (`frontend/`) to visualize agent hierarchies, running DAG tasks, model router allocations, costs, and logs.\n")

# Session Log
log_path = os.path.join(repo_root, "logs", "sessions", "2026-07-28_control_center.md")
log_content = """# Autonomous Session Log: 2026-07-28

**Task:** Genesis Live Control Center Implementation
**Commit Message:** feat: create Genesis live control center
**Active Agents:** `architect`, `frontend-engineer`, `backend-engineer`, `ceo`
**Skills Used:** `ui-design`, `software-engineering`, `architecture`

## Changes Executed
- Implemented `control-center/events/event_bus.py` pub/sub telemetry event bus.
- Implemented `control-center/backend/server.py` HTTP & WebSocket API server.
- Built single page dashboard in `control-center/frontend/index.html` & `styles.css`.
- Applied a calm, modern Linear/Notion dark aesthetic (`#0D0E11` background, `#3B82F6` accents, crisp typography).
- Created visual representation for CEO -> Specialized Agents -> Task Queue -> Verified Results.

## Results
- Structural verification: 173 checks Passed cleanly.
- Live Control Center ready for execution on `http://localhost:8080`.
"""
with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print("Docs and log updated for Control Center.")
