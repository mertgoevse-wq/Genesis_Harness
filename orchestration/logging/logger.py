import os
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
