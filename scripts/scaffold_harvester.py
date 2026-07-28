import os
import json

repo_root = "c:\\Genesis_Harness"
harvester_dir = os.path.join(repo_root, "harvester")

# Step 1: Folder structure
dirs = [
    "discovery",
    "ranking",
    "analysis",
    "knowledge_graph",
    "engine",
    "prompt_lab",
    "scheduler"
]
for d in dirs:
    os.makedirs(os.path.join(harvester_dir, d), exist_ok=True)
    with open(os.path.join(harvester_dir, d, ".gitkeep"), "w") as f:
        pass

# Step 2: Config
config = {
    "search_categories": [
        "AI Agents", "MCP", "Claude Skills", "Prompt Engineering", 
        "Multi Agent", "Reasoning", "LangGraph", "CrewAI", "AutoGen", 
        "OpenHands", "Continue", "Open Interpreter", "Aider", "RAG", 
        "Evaluation", "Benchmarks", "Scientific AI", "Simulation", "Coding Agents"
    ],
    "ranking_weights": {
        "stars": 0.2,
        "forks": 0.1,
        "recent_activity": 0.3,
        "documentation": 0.2,
        "architecture_quality": 0.1,
        "tests": 0.05,
        "maintainability": 0.05
    },
    "scheduler": {
        "cron_interval": "0 0 * * 0" # Weekly
    }
}
with open(os.path.join(repo_root, "configs", "harvester.config.json"), "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

# Step 3: Harvester README
readme_content = """# Genesis Intelligence Harvester

The Harvester is an autonomous subsystem that continuously searches GitHub for state-of-the-art AI architectural patterns, extracts conceptual designs, and proposes integrations into Genesis.

## Modules

1. **Discovery**: Queries GitHub API across predefined AI categories.
2. **Ranking**: Scores repositories based on a weighted algorithm (Stars, Forks, Recency, Docs, Architecture).
3. **Analysis**: Parses `README.md`, `docs`, `yaml`, `json`, and prompt files to extract structural patterns, omitting copyrighted implementation code.
4. **Knowledge Graph**: Stores extracted patterns (Agent, Skill, Workflow, Prompt Pattern, MCP) in a relational graph.
5. **Engine**: Compares the knowledge graph against Genesis and generates improvement proposals.
6. **Prompt Laboratory**: Extracts and converts prompt structures into Genesis templates.
7. **Scheduler**: Manages automatic update intervals.
"""
with open(os.path.join(harvester_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Harvester scaffolded successfully.")
