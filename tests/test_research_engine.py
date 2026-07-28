import unittest
from research_intelligence.research_engine.research_orchestrator import ResearchIntelligenceEngine
class TestResearchEngine(unittest.TestCase):
    def test_engine_analysis(self):
        rie = ResearchIntelligenceEngine()
        res = rie.analyze_advances("AI Agents")
        self.assertEqual(res["topic"], "AI Agents")
if __name__ == "__main__":
    unittest.main()
