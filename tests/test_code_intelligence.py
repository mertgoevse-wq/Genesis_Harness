import unittest
from code_intelligence.repo_parser import CodeIntelligence
class TestCodeIntelligence(unittest.TestCase):
    def test_parse(self):
        ci = CodeIntelligence()
        res = ci.parse_repo_structure()
        self.assertGreater(res["quality_score"], 90.0)
if __name__ == "__main__":
    unittest.main()
