import json
import os

repo_root = "c:\\Genesis_Harness"

# Task 3: Enrich agent_registry.json
agent_reg_path = os.path.join(repo_root, "configs", "agent_registry.json")
with open(agent_reg_path, "r", encoding="utf-8") as f:
    agent_reg = json.load(f)

# Enhance structure to include capabilities metadata
agent_reg["capabilities_schema"] = {
    "fields": ["capabilities", "required_skills", "preferred_model", "cost_tier", "quality_threshold"]
}

agent_reg["agent_capabilities"] = {
    "architect": {
        "capabilities": ["System Design", "ADR Creation", "Component Modularization"],
        "required_skills": ["architecture", "software-engineering"],
        "preferred_model": "Claude Opus 4.8",
        "cost_tier": "High",
        "quality_threshold": 0.95
    },
    "coding": {
        "capabilities": ["Python/JS Implementation", "Refactoring", "Bug Fixing"],
        "required_skills": ["software-engineering"],
        "preferred_model": "Claude Sonnet 4.6",
        "cost_tier": "Medium",
        "quality_threshold": 0.90
    },
    "ceo": {
        "capabilities": ["Strategic Decision Making", "Resource Allocation", "Vision"],
        "required_skills": ["business-analysis", "market-analysis"],
        "preferred_model": "Claude Opus 4.8",
        "cost_tier": "High",
        "quality_threshold": 0.95
    },
    "harvester-agent": {
        "capabilities": ["GitHub Crawling", "Pattern Extraction", "ADR Proposal"],
        "required_skills": ["evaluation", "architecture"],
        "preferred_model": "Gemini 3.6 Flash",
        "cost_tier": "Low",
        "quality_threshold": 0.85
    }
}

with open(agent_reg_path, "w", encoding="utf-8") as f:
    json.dump(agent_reg, f, indent=2)


# Enrich skill_registry.json
skill_reg_path = os.path.join(repo_root, "configs", "skill_registry.json")
with open(skill_reg_path, "r", encoding="utf-8") as f:
    skill_reg = json.load(f)

skill_reg["skill_metadata"] = {
    "software-engineering": {"category": "Technical", "complexity": "High"},
    "architecture": {"category": "Technical", "complexity": "High"},
    "business-analysis": {"category": "Business", "complexity": "Medium"},
    "market-analysis": {"category": "Business", "complexity": "Medium"}
}

with open(skill_reg_path, "w", encoding="utf-8") as f:
    json.dump(skill_reg, f, indent=2)


# Task 4: Session Logging engine in orchestration/logging/logger.py
logger_code = '''import os
import datetime
import subprocess

class SessionLogger:
    def __init__(self, log_dir: str = "logs/sessions"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_session(self, active_agents: list, used_skills: list, used_models: list, changes: list, results: str) -> str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        commit_hash = self._get_git_commit()
        filename = f"{date_str}_session.md"
        filepath = os.path.join(self.log_dir, filename)

        content = f"""# Autonomous Session Log: {date_str}

**Commit Hash:** {commit_hash}
**Active Agents:** {", ".join(active_agents)}
**Skills Used:** {", ".join(used_skills)}
**Models Routed:** {", ".join(used_models)}

## Changes Executed
{chr(10).join([f"- {c}" for c in changes])}

## Execution Results
{results}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def _get_git_commit(self) -> str:
        try:
            return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
        except Exception:
            return "unknown"
'''

with open(os.path.join(repo_root, "orchestration", "logging", "logger.py"), "w", encoding="utf-8") as f:
    f.write(logger_code)


# Task 5: Expand quality_gates.json
qg_path = os.path.join(repo_root, "configs", "quality_gates.json")
with open(qg_path, "r", encoding="utf-8") as f:
    qg = json.load(f)

qg["commitGates"]["securityScan"] = {"enabled": True, "blocking": True}
qg["commitGates"]["agentOutputEvaluation"] = {"enabled": True, "blocking": True, "minScore": 0.85}

with open(qg_path, "w", encoding="utf-8") as f:
    json.dump(qg, f, indent=2)

print("Agent capabilities, logger, and quality gates updated.")
