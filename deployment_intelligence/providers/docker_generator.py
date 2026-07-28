"""Docker deployment artifact generator."""

from typing import Dict, Any


class DockerGenerator:
    """Generates Docker and Docker Compose configurations."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Docker artifacts for the project."""
        dockerfile = (
            "FROM python:3.12-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install -r requirements.txt\n"
            "COPY . .\n"
            'CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]\n'
        )
        compose = (
            "version: '3.8'\n"
            "services:\n"
            "  app:\n"
            "    build: .\n"
            "    ports:\n"
            "      - \"8000:8000\"\n"
            "    env_file:\n"
            "      - .env\n"
        )
        return {
            "Dockerfile": dockerfile,
            "docker-compose.yml": compose,
        }
