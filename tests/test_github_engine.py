import unittest
from github_engine.repo_analyzer import GitHubEngine
class TestGitHubEngine(unittest.TestCase):
    def test_repo_analysis(self):
        ghe = GitHubEngine()
        res = ghe.analyze_repo("Genesis_Harness")
        self.assertEqual(res["status"], "HEALTHY")
if __name__ == "__main__":
    unittest.main()
