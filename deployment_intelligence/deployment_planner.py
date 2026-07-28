"""Deployment planner: choose providers and generate deployment artifacts."""

from typing import Dict, Any, List

from .providers.docker_generator import DockerGenerator
from .providers.vercel_generator import VercelGenerator
from .providers.supabase_generator import SupabaseGenerator
from .providers.cloud_generator import CloudGenerator


class DeploymentPlanner:
    """Plans deployment configurations for generated products."""

    PROVIDERS = {
        "docker": DockerGenerator,
        "vercel": VercelGenerator,
        "supabase": SupabaseGenerator,
        "cloud": CloudGenerator,
    }

    def __init__(self):
        self.providers = {
            name: cls() for name, cls in self.PROVIDERS.items()
        }

    def plan(
        self, project: str, requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate deployment artifacts for a project.

        Args:
            project: The project name/slug.
            requirements: Dict with keys like 'frontend', 'backend', 'database'.

        Returns:
            Dict with chosen providers and generated artifacts.
        """
        chosen = self._select_providers(requirements)
        artifacts = {}
        for provider in chosen:
            generator = self.providers[provider]
            artifacts[provider] = generator.generate(project, requirements)

        return {
            "project": project,
            "providers": chosen,
            "artifacts": artifacts,
            "status": "PLANNED",
        }

    def _select_providers(self, requirements: Dict[str, Any]) -> List[str]:
        chosen = []
        if requirements.get("backend") or requirements.get("frontend"):
            chosen.append("docker")
        if requirements.get("frontend"):
            chosen.append("vercel")
        if requirements.get("database"):
            chosen.append("supabase")
        if not chosen:
            chosen.append("cloud")
        return chosen
