from .base import BaseTool

class TerminalTool(BaseTool):
    name = "terminal_tool"
    description = "Allows the agent to run terminal commands."
    
    def execute(self, command: str) -> str:
        return f"[TerminalTool] Executed: {command} (Mocked Output: Success)"
