import unittest
from skill_intelligence.skill_detector import SkillDetector
class TestSkillIntelligence(unittest.TestCase):
    def test_detection(self):
        sd = SkillDetector()
        skills = sd.detect_required_skills("Build AI medical SaaS")
        self.assertIn("security", skills)
if __name__ == "__main__":
    unittest.main()
