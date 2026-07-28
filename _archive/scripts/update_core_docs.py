import os

repo_root = "c:\\Genesis_Harness"

# Step 6: Benchmark definitions
benchmark_dir = os.path.join(repo_root, "prompts", "benchmarks", "harvester_evaluation")
os.makedirs(benchmark_dir, exist_ok=True)

eval_content = """# Harvester Knowledge Benchmark

This benchmark evaluates the quality of patterns extracted by the Harvester module.

## Metrics
1. **Abstraction Level**: Does the extracted pattern contain copyrighted implementation code? (Fail if yes).
2. **Reusability**: Can the extracted pattern be applied to a different domain within Genesis?
3. **Complexity**: Is the pattern overly complex or properly modular?
4. **Integration**: How easily can it be translated into a Genesis ADR or Agent configuration?
"""
with open(os.path.join(benchmark_dir, "benchmark_01.md"), "w", encoding="utf-8") as f:
    f.write(eval_content)

# Step 7: Update Core Docs
# README.md
readme_path = os.path.join(repo_root, "README.md")
with open(readme_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Subsystems\n- **Genesis Intelligence Harvester**: An autonomous sub-system that continuously scans GitHub to learn and ingest new AI architecture patterns without copying implementation code.\n")

# ROADMAP.md
roadmap_path = os.path.join(repo_root, "docs", "ROADMAP.md")
with open(roadmap_path, "r", encoding="utf-8") as f:
    roadmap = f.read()

roadmap = roadmap.replace("Phase 4: Harvester Integration [ ]", "Phase 4: Harvester Integration [x]")
with open(roadmap_path, "w", encoding="utf-8") as f:
    f.write(roadmap)

# ARCHITECTURE.md
arch_path = os.path.join(repo_root, "docs", "ARCHITECTURE.md")
with open(arch_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Genesis Intelligence Harvester\nThe Harvester sits alongside the Agent layer. It comprises Discovery, Ranking, Analysis, Knowledge Graph, Engine, and Prompt Lab modules. It feeds abstract architectural patterns back into the Genesis Core via formal Improvement Proposals (ADRs).\n")

# CLAUDE.md
claude_path = os.path.join(repo_root, "CLAUDE.md")
with open(claude_path, "a", encoding="utf-8") as f:
    f.write("\n\n## Harvester Rules\n- The Harvester MUST NOT extract copyrighted source code.\n- Only structural patterns, workflows, and prompts may be ingested.\n- The Harvester operates via the `harvester-agent`.\n")

print("Docs updated.")
