import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Autonomous MVP Builder & Deployment Engine (Phase 15)\nPhase 15 transforms Genesis into an autonomous **MVP Builder**:\n- **Autonomous MVP Codebase Pipeline (`mvp_builder/`)**: Product analysis, system architecture design, schema design, API design, frontend generation, backend generation, test generation, and deployment packaging.\n- **Generated MVP Workspace (`generated_products/<product>/mvp/`)**: Fullstack application codebase containing `frontend/`, `backend/`, `database/`, `tests/`, `docker/`, `docs/`, `README.md`, `ARCHITECTURE.md`, `API_SPEC.md`, `DATABASE_SCHEMA.md`, and `DEPLOYMENT.md`.\n- **Real Standalone Demo Workflow (`scripts/run_mvp_builder.py`)**: End-to-end execution script creating complete application codebases from prompts.\n")

print("Docs updated for Phase 15 MVP Builder.")
