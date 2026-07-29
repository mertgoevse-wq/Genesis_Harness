class MCPAdapter:
    """Base Adapter for the Model Context Protocol (MCP)."""
    protocol_version = "1.0"
    
    def connect(self):
        print(f"[{self.__class__.__name__}] Connecting via MCP...")

class FilesystemMCP(MCPAdapter):
    """Adapter for local file system manipulation over MCP."""
    pass

class GithubMCP(MCPAdapter):
    """Adapter for remote GitHub operations over MCP."""
    pass

class BrowserMCP(MCPAdapter):
    """Adapter for headless browser interactions over MCP."""
    pass

class ImageMCP(MCPAdapter):
    """Adapter for visual understanding / generation over MCP."""
    pass

class VoiceMCP(MCPAdapter):
    """Adapter for text-to-speech and STT (OmniVoiceStudio) over MCP."""
    pass

class VideoMCP(MCPAdapter):
    """Adapter for video generation / avatar pipelines over MCP."""
    pass
