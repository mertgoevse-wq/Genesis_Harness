# Memory Architecture

Genesis maintains a continuous memory of its operations to ensure context is never lost across sessions.

## Storage Locations
- **`docs/`**: The canonical truth. High-level architecture, roadmaps, and agent definitions.
- **`logs/sessions/`**: Chronological append-only logs of every session, including reasoning and test outputs.
- **`docs/adr/`**: Architecture Decision Records (ADRs). Immutable records of technical decisions and their justifications.
- **Repository History**: Git history provides the raw evolution of the codebase.

## Retrieval Protocol
Before beginning a task:
1. Search `logs/sessions/` for related past work.
2. Review relevant ADRs in `docs/adr/`.
3. Consult `docs/ARCHITECTURE.md` to ensure alignment with existing patterns.
