import json
class MCPRegistryManager:
    def __init__(self, path="configs/mcp_registry.json"):
        with open(path, "r") as f:
            self.servers = json.load(f).get("mcp_servers", [])
    def get_server(self, name: str):
        return next((s for s in self.servers if s["name"] == name), None)
