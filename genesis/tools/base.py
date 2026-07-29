from typing import Any

class BaseTool:
    """Base interface for all tools an agent can use."""
    name = "base_tool"
    description = "A generic tool interface."
    
    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Tools must implement the execute method.")
