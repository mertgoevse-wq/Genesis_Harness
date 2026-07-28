import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Live Control Center + Product Interface (Phase 13)\nPhase 13 delivers a live human-facing dashboard and product interface:\n- **Control Center Backend API (`control-center/backend/api_server.py`)**: REST endpoints serving system status, active agents, skills, workflows, projects, telemetry, and quality scores.\n- **Genesis Dashboard Application (`control-center/frontend/`)**: Modern dark-mode Web Dashboard UI (`index.html`, `style.css`, `app.js`).\n- **Real User Workflow (`scripts/run_saas_idea_workflow.py`)**: End-to-end execution script triggering Founder Intelligence & Research Intelligence to produce validated SaaS venture specifications.\n")

print("Docs updated for Phase 13 Control Center.")
