from .base import BaseTool

class DocumentationTool(BaseTool):
    name = "documentation_tool"
    description = "Allows the agent to generate and update documentation."
    
    def execute(self, topic: str) -> str:
        return f"[DocumentationTool] Documentation for '{topic}' updated successfully."
