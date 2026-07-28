"""Vercel deployment artifact generator."""

from typing import Dict, Any


class VercelGenerator:
    """Generates Vercel configuration for frontend deployment."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Vercel artifacts for the project."""
        vercel_json = {
            "version": 2,
            "name": project,
            "builds": [
                {"src": "frontend/index.html", "use": "@vercel/static"}
            ],
            "routes": [
                {"src": "/api/(.*)", "dest": "https://api.example.com/$1"},
                {"src": "/.*", "dest": "frontend/index.html"},
            ],
            "env": {
                "VITE_API_URL": "https://api.example.com",
            },
        }

        import json

        readme = f"""# Vercel Deployment Guide: {project}

## Prerequisites

- Vercel CLI installed: `npm i -g vercel`
- Vercel account linked

## Deploy

```bash
npx vercel --prod
```

## Environment Variables

Set `VITE_API_URL` to your production API URL in the Vercel dashboard.
"""

        return {
            "vercel.json": json.dumps(vercel_json, indent=2),
            "VERCEL_README.md": readme,
        }
