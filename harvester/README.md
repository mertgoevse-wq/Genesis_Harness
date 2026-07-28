# Genesis Intelligence Harvester

The Harvester is an autonomous subsystem that continuously searches GitHub for state-of-the-art AI architectural patterns, extracts conceptual designs, and proposes integrations into Genesis.

## Modules

1. **Discovery**: Queries GitHub API across predefined AI categories.
2. **Ranking**: Scores repositories based on a weighted algorithm (Stars, Forks, Recency, Docs, Architecture).
3. **Analysis**: Parses `README.md`, `docs`, `yaml`, `json`, and prompt files to extract structural patterns, omitting copyrighted implementation code.
4. **Knowledge Graph**: Stores extracted patterns (Agent, Skill, Workflow, Prompt Pattern, MCP) in a relational graph.
5. **Engine**: Compares the knowledge graph against Genesis and generates improvement proposals.
6. **Prompt Laboratory**: Extracts and converts prompt structures into Genesis templates.
7. **Scheduler**: Manages automatic update intervals.
