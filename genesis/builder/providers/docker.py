"""Docker deployment artifact generator."""

from typing import Any, Dict


class DockerGenerator:
    """Generates Docker and Docker Compose configurations."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Docker artifacts for the project."""
        backend_path = requirements.get("backend_path", "backend")
        dockerfile = self._dockerfile(backend_path)
        compose = self._compose(project, backend_path)
        prod_checklist = self._prod_checklist(project)

        return {
            "Dockerfile": dockerfile,
            "docker-compose.yml": compose,
            "docker-compose.prod.yml": self._compose_prod(project, backend_path),
            "PRODUCTION_CHECKLIST.md": prod_checklist,
        }

    def _dockerfile(self, backend_path: str) -> str:
        return f"""FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY {backend_path}/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PATH=/root/.local/bin:$PATH

COPY --from=builder /root/.local /root/.local
COPY {backend_path}/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _compose(self, project: str, backend_path: str) -> str:
        return f"""version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ../.env
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db/{project}
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {project}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""

    def _compose_prod(self, project: str, backend_path: str) -> str:
        return f"""version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ../.env
    environment:
      DATABASE_URL: ${{DATABASE_URL}}
      SECRET_KEY: ${{SECRET_KEY}}
    restart: unless-stopped
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${{POSTGRES_USER}}
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD}}
      POSTGRES_DB: {project}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
"""

    def _prod_checklist(self, project: str) -> str:
        return f"""# Production Checklist: {project}

## Before deploying

- [ ] Set a strong `SECRET_KEY` in environment
- [ ] Use a managed PostgreSQL instance or persistent volume
- [ ] Enable HTTPS (TLS termination)
- [ ] Configure CORS to allow only known origins
- [ ] Run database migrations
- [ ] Set up monitoring and log aggregation
- [ ] Configure backups
"""
