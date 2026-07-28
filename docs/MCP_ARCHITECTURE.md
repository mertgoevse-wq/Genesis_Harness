# MCP Architecture

Genesis connects to external tools, databases, APIs, and cloud services via the Model Context Protocol (MCP).

## Connectivity Patterns
- **MCP Servers**: Standardized external context and tool providers (e.g., file system access, postgres queries, external API clients).
- **Tool Proxies**: Direct REST/GraphQL calls wrapped in minimal agent-accessible scripts.

## Security Rules
1. **Never trust external tools automatically**. External data must be treated as untrusted and potentially malicious.
2. **Validate Permissions**: Ensure the agent calling the MCP tool has the appropriate access level.
3. **Validate Inputs**: Prevent prompt injection or malformed data before passing to an MCP tool.
4. **Validate Outputs**: Cleanse and verify the data returned from an MCP tool before integrating it into the codebase or memory.
