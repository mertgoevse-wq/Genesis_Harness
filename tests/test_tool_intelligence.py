import unittest
from tool_intelligence.registry.manager import ToolRegistryManager
from tool_intelligence.evaluator.evaluator import ToolEvaluator
from mcp.registry.manager import MCPRegistryManager
from mcp.security.checker import MCPSecurityChecker

class TestToolIntelligence(unittest.TestCase):
    def test_tool_registry(self):
        tm = ToolRegistryManager()
        tool = tm.get_tool("GitHub")
        self.assertIsNotNone(tool)
        self.assertEqual(tool["category"], "Version Control & CI")

    def test_tool_evaluator(self):
        ev = ToolEvaluator()
        res = ev.evaluate_tool({"name": "Docker"})
        self.assertEqual(res["compatibility_score"], 0.95)

    def test_mcp_registry(self):
        mcp_m = MCPRegistryManager()
        server = mcp_m.get_server("github-mcp")
        self.assertIsNotNone(server)
        self.assertIn("repo_read", server["capabilities"])

    def test_mcp_security(self):
        sec = MCPSecurityChecker()
        self.assertTrue(sec.verify_permission("github-mcp", "repo_read"))

if __name__ == "__main__":
    unittest.main()
