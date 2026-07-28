"""Supabase deployment artifact generator."""

from typing import Dict, Any


class SupabaseGenerator:
    """Generates Supabase configuration for database and auth."""

    def generate(self, project: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Return Supabase artifacts for the project."""
        schema = f"""-- Supabase schema for {project}

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text UNIQUE NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamptz DEFAULT now()
);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own row" ON users
    FOR SELECT USING (auth.uid() = id);
"""

        env = """# Supabase configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
"""

        readme = f"""# Supabase Setup: {project}

## Steps

1. Create a new Supabase project at https://supabase.com
2. Copy the URL and anon key from Settings > API
3. Run `schema.sql` in the SQL Editor
4. Enable Email Auth in Authentication > Providers
5. Set environment variables in your deployment
"""

        return {
            "schema.sql": schema,
            ".env.example": env,
            "SUPABASE_SETUP.md": readme,
        }
