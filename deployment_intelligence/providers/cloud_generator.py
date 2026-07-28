"""Generic cloud deployment artifact generator."""

from typing import Dict, Any


class CloudGenerator:
    """Generates generic cloud-agnostic deployment guidance."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return generic cloud deployment guidance."""
        readme = (
            "# Cloud Deployment Guide\n\n"
            "1. Build the Docker image.\n"
            "2. Push to a container registry.\n"
            "3. Deploy to your cloud provider (AWS, GCP, Azure).\n"
        )
        return {
            "CLOUD_DEPLOYMENT.md": readme,
        }
