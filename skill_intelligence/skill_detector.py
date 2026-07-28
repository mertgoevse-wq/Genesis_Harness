class SkillDetector:
    def detect_required_skills(self, prompt: str) -> list:
        skills = ["software-engineering", "saas-development", "startup-validation"]
        if "medical" in prompt.lower():
            skills.extend(["security", "privacy"])
        return skills
