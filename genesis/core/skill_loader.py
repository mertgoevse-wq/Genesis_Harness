import json
import os
import subprocess
from typing import Any, Dict, List, Optional

class SkillLoader:
    """Dynamically loads skills for agents at runtime from multiple sources."""
    
    def __init__(self, registry_path: str = "configs/skill_registry.json", skills_dir: str = "skills"):
        self.registry_path = registry_path
        self.skills_dir = skills_dir
        self.registry: Dict[str, Any] = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def fetch_github_skill(self, repo_url: str, skill_name: str) -> None:
        """Downloads a skill from a GitHub repository."""
        target_dir = os.path.join(self.skills_dir, skill_name)
        if not os.path.exists(target_dir):
            try:
                subprocess.run(["git", "clone", repo_url, target_dir], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                pass

    def get_skill_content(self, skill_name: str, source: str = "local", repo_url: str = "") -> Optional[str]:
        """Loads the content of SKILL.md for a given skill based on its source."""
        if source == "github" and repo_url:
            self.fetch_github_skill(repo_url, skill_name)
            
        skill_path = os.path.join(self.skills_dir, skill_name, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
                
        # Claude source means the skill is part of Claude's native system prompts, handled externally
        if source == "claude":
            return f"[{skill_name} is a native Claude skill and is injected automatically]"
            
        return None

    def load_skills_for_agent(self, agent_name: str, required_skills: List[Dict[str, str]]) -> Dict[str, str]:
        """Loads all required skills and returns their contents."""
        loaded = {}
        for skill_def in required_skills:
            name = skill_def.get("name")
            source = skill_def.get("source", "local")
            repo_url = skill_def.get("repo_url", "")
            
            if name:
                content = self.get_skill_content(name, source, repo_url)
                if content:
                    loaded[name] = content
        return loaded
