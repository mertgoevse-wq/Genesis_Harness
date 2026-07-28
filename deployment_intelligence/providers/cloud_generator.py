"""Generic cloud deployment artifact generator."""

from typing import Dict, Any


class CloudGenerator:
    """Generates generic cloud-agnostic deployment guidance."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return generic cloud deployment guidance."""
        readme = f"""# Cloud Deployment Guide: {project}

## Generic 3-Step Deploy

1. Build the Docker image.
2. Push to a container registry.
3. Deploy to your cloud provider (AWS, GCP, Azure).

## Example (AWS ECS with Fargate)

```bash
# Build and tag
docker build -t {project}:latest -f docker/Dockerfile .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag {project}:latest <account>.dkr.ecr.us-east-1.amazonaws.com/{project}:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/{project}:latest

# Deploy via ECS Fargate
aws ecs update-service --cluster {project}-cluster --service {project}-service --force-new-deployment
```

## Provider Quick Links

- AWS: https://aws.amazon.com
- GCP: https://cloud.google.com
- Azure: https://azure.microsoft.com
"""

        return {
            "CLOUD_DEPLOYMENT.md": readme,
        }
