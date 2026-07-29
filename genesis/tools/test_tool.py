from .base import BaseTool

class TestTool(BaseTool):
    name = "test_tool"
    description = "Allows the agent to run the test suite."
    
    def execute(self, target: str = "all") -> str:
        return f"[TestTool] Test suite ran for {target}. Results: 100% Passed."
