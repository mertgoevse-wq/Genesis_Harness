import unittest
from knowledge_fabric.connectors.skill_connector import SkillConnector
class TestSkillIntegration(unittest.TestCase):
    def test_skills(self):
        sc = SkillConnector()
        skills = sc.connect_skills()
        self.assertIn("software-architecture", skills)
if __name__ == "__main__":
    unittest.main()
