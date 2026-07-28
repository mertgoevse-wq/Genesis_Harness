import os

repo_root = "c:\\Genesis_Harness"

# Update ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Autonomous Product Launch Engine (Phase 14)\nPhase 14 transforms Genesis into an autonomous **Product Launch Engine**:\n- **Autonomous Product Generation Pipeline (`product_launch/`)**: Idea processing, product spec generation, business plan generation, codebase planning, landing page creation, and marketing strategy.\n- **Generated Product Workspaces (`generated_products/<product_name>/`)**: Complete product packages containing `README.md`, `BUSINESS_PLAN.md`, `MARKET_ANALYSIS.md`, `PRD.md`, `TECHNICAL_ARCHITECTURE.md`, `ROADMAP.md`, `SECURITY_REVIEW.md`, `DEPLOYMENT_PLAN.md`, and `MARKETING_PLAN.md`.\n- **Real Standalone Demo Workflow (`scripts/run_product_launch.py`)**: End-to-end execution script creating complete product packages from high-level prompts.\n")

print("Docs updated for Phase 14 Product Launch Engine.")
