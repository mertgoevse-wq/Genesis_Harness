import subprocess
from .base import BaseTool

class GitTool(BaseTool):
    name = "git_tool"
    description = "Allows the agent to perform real git operations like commit, push, pull."
    
    def _run(self, cmd: list) -> str:
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
    
    def execute(self, action: str, *args) -> str:
        if action == "status":
            return self._run(["git", "status"])
        elif action == "diff":
            return self._run(["git", "diff"])
        elif action == "add":
            return self._run(["git", "add", "."])
        elif action == "commit":
            message = args[0] if args else "Automated commit by Genesis Agent"
            return self._run(["git", "commit", "-m", message])
        elif action == "branch":
            branch_name = args[0] if args else "agent-branch"
            return self._run(["git", "checkout", "-b", branch_name])
        
        return f"[GitTool] Git {action} not fully supported."
