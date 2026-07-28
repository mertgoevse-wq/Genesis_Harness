import json
class ToolRegistryManager:
    def __init__(self, path="configs/tool_registry.json"):
        with open(path, "r") as f:
            self.tools = json.load(f).get("tools", [])
    def get_tool(self, name: str):
        return next((t for t in self.tools if t["name"].lower() == name.lower()), None)
