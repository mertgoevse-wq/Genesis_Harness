# Templates

**Version:** 1.0.0 · **Last updated:** 2026-07-28

Structural templates for the artefacts this harness produces. Uniform structure is what lets an
agent consume an unfamiliar artefact without interpreting it.

| Template | Produces | Used by |
|---|---|---|
| [AGENT_TEMPLATE.md](AGENT_TEMPLATE.md) | A new agent charter | `prompts/generators/agent_generator.md` |
| [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) | A new skill | `prompts/generators/skill_generator.md` |
| [ADR_TEMPLATE.md](ADR_TEMPLATE.md) | An architecture decision record | Architect Agent |
| [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md) | An inter-agent handoff | Every agent |

The session log template lives with the logging system: [`logs/SESSION_TEMPLATE.md`](../logs/SESSION_TEMPLATE.md).

## Rules

1. **Fill every section or delete it.** A template section filled with "N/A" is noise — except
   `Not Done`, `Not Verified`, and `Open Questions`, where an explicit "none" is meaningful.
2. **Do not restructure a template per-use.** The uniformity is the value. If a template is
   wrong for a real case, change the template and say so in a session log.
3. **Templates are versioned.** Changing one is a repository change like any other: it needs a
   reason, a commit, and a log entry.
