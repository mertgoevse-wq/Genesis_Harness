import os
import json

repo_root = "c:\\Genesis_Harness"

# Step 4: Create Harvester Agent
harvester_agent_dir = os.path.join(repo_root, "agents", "harvester-agent")
os.makedirs(harvester_agent_dir, exist_ok=True)

charter_content = """---
name: harvester-agent
description: Autonomous GitHub Intelligence Harvester
---

# Harvester Agent Charter

## Role
You are the Harvester Agent, part of the Executive Layer of the Genesis Architecture. Your goal is to scan GitHub for state-of-the-art AI architectural patterns, evaluate them, extract non-copyrighted structural ideas, and propose improvements to the Genesis system.

## Responsibilities
- Execute the Harvester modules: Discovery, Ranking, Analysis, Knowledge Graph, Engine, Prompt Lab.
- Never blindly copy implementation code. Only extract abstract concepts (prompt structures, agent roles, workflows).
- Compare harvested knowledge against Genesis configuration and formulate ADRs (Improvement Proposals) for the CEO and Architect.
- Automatically trigger tests and benchmarks on extracted prompt structures.
"""
with open(os.path.join(harvester_agent_dir, "AGENT.md"), "w", encoding="utf-8") as f:
    f.write(charter_content)

adapter_content = """---
name: harvester-agent
description: Autonomous GitHub Intelligence Harvester
---

# Instructions

You are the Harvester Agent. Refer to your charter in `agents/harvester-agent/AGENT.md` and the architecture documentation in `harvester/README.md`.
Use the `harness.config.json` registry and `configs/harvester.config.json` to configure your searches.
"""
with open(os.path.join(repo_root, ".claude", "agents", "harvester-agent.md"), "w", encoding="utf-8") as f:
    f.write(adapter_content)


# Step 5: Update Registries
harness_path = os.path.join(repo_root, "configs", "harness.config.json")
agent_reg_path = os.path.join(repo_root, "configs", "agent_registry.json")

with open(harness_path, 'r', encoding='utf-8') as f:
    harness = json.load(f)

# Avoid duplicates if script runs twice
if not any(a["id"] == "harvester-agent" for a in harness["agents"]):
    harness["agents"].append({
        "id": "harvester-agent",
        "name": "Harvester Agent",
        "roleClass": "Executive",
        "owns": "Genesis Improvement Engine",
        "canBlock": "System upgrades with poor architecture",
        "charter": "agents/harvester-agent/AGENT.md",
        "adapter": ".claude/agents/harvester-agent.md",
        "primarySkills": ["evaluation", "architecture"],
        "supportingSkills": ["prompt-engineering"],
        "masterPrompt": None
    })
with open(harness_path, 'w', encoding='utf-8') as f:
    json.dump(harness, f, indent=2)


with open(agent_reg_path, 'r', encoding='utf-8') as f:
    agent_reg = json.load(f)

if "harvester-agent" not in agent_reg["agents"]:
    agent_reg["agents"].append("harvester-agent")

with open(agent_reg_path, 'w', encoding='utf-8') as f:
    json.dump(agent_reg, f, indent=2)

print("Harvester agent and registries updated.")
