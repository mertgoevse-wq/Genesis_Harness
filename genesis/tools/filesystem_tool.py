from .base import BaseTool

class FileSystemTool(BaseTool):
    name = "filesystem_tool"
    description = "Allows the agent to read and write files."
    
    def execute(self, action: str, path: str, content: str = "") -> str:
        if action == "read":
            return f"[FilesystemTool] Read content from {path}"
        elif action == "write":
            return f"[FilesystemTool] Wrote {len(content)} bytes to {path}"
        return "[FilesystemTool] Unknown action"
