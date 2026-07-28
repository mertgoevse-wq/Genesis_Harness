"""Supabase deployment artifact generator."""

from typing import Dict, Any


class SupabaseGenerator:
    """Generates Supabase configuration for database and auth."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Supabase artifacts for the project."""
        schema = (
            "-- Supabase schema for " + project + "\n"
            "CREATE TABLE users (\n"
            "  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),\n"
            "  email text UNIQUE NOT NULL,\n"
            "  created_at timestamptz DEFAULT now()\n"
            ");\n"
        )
        env = (
            "SUPABASE_URL=https://your-project.supabase.co\n"
            "SUPABASE_ANON_KEY=your-anon-key\n"
        )
        return {
            "schema.sql": schema,
            ".env.example": env,
        }
