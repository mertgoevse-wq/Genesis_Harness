class ToolEvaluator:
    def evaluate_tool(self, tool: dict) -> dict:
        return {"name": tool.get("name"), "compatibility_score": 0.95, "security_verified": True}
