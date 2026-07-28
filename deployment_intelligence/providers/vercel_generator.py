"""Vercel deployment artifact generator."""

from typing import Dict, Any


class VercelGenerator:
    """Generates Vercel configuration for frontend deployment."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Vercel artifacts for the project."""
        vercel_json = (
            '{\n'
            '  "version": 2,\n'
            '  "name": "' + project + '",\n'
            '  "builds": [\n'
            '    {\n'
            '      "src": "frontend/index.html",\n'
            '      "use": "@vercel/static"\n'
            '    }\n'
            '  ]\n'
            '}\n'
        )
        return {
            "vercel.json": vercel_json,
        }
