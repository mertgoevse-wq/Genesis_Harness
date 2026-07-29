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

## Registered MCP Categories (Phase 4 Extension)

### 1. System MCPs
- **Filesystem MCP**: Direct disk interaction under restrictive sandbox.
- **Terminal MCP**: Shell execution with isolated execution bounds.
- **Docker MCP**: Container generation and lifecycle management.
- **Database MCP**: Secure querying against internal databases (PostgreSQL/Supabase).

### 2. External Integration MCPs
- **GitHub MCP**: Pull Requests, Issues, Repository state reading/writing.
- **Browser MCP**: Playwright-based DOM interaction for Live Previews and Visual QA.

### 3. AI & Media MCPs (Islam Tutor Expansion)
- **AI Backend MCP**: Routing to Claude, Gemini, GPT, Ollama.
- **Video MCP**: Integration with Wan Video, Wan2.1, HeyGem.
- **Voice MCP**: OmniVoiceStudio, STT, TTS for Arabic pronunciation.
- **Mobile MCP**: Android emulator control, Camera input (Pose Detection), Microphone input.
