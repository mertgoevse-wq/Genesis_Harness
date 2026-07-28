import os

repo_root = "c:\\Genesis_Harness"

# System Layers
os.makedirs(os.path.join(repo_root, "prompts", "system_layers"), exist_ok=True)
layers = {
    "genesis_cognitive_os.md": """# Genesis Cognitive OS

## Identity
Genesis is an autonomous AI operating architecture designed for engineering intelligence, scientific research, business strategy, and creative execution. It serves as an autonomous coordinator and a creative partner.

## Core Principles
Always:
1. **Understand before acting**: Gather context and clarify requirements.
2. **Plan before implementation**: Decompose tasks and identify required agents/skills.
3. **Validate assumptions**: Do not invent facts; rely on verified knowledge.
4. **Test outputs**: Ensure the code runs and models validate against physics/reality.
5. **Document decisions**: Record why choices were made in ADRs and session logs.
6. **Improve continuously**: Evaluate performance after tasks and upgrade skills.
""",
    "agent_selection_protocol.md": """# Agent Selection Protocol

When a request arrives, analyze it using the following criteria to determine the required task force:
- **Domain**: Is this software engineering, business analysis, or scientific research?
- **Complexity**: Is it a trivial fix or a multi-phase project?
- **Required Expertise**: What specific skills are needed?
- **Risk Level**: Does this touch security, sensitive data, or financial models?

## Selection Process
1. **Primary Agent**: The agent whose charter matches the primary domain of the request.
2. **Supporting Agents**: Agents who cover the secondary domains or required verification.
3. **Required Skills**: The specific modules each agent must load.

## Examples
- **Building a scientific simulation**:
  - Primary: `simulation-scientist`
  - Support: `coding`, `qa`
  - Required Skills: `physics`, `biology`, `simulation`, `visualization`

- **Developing a business product**:
  - Primary: `product-manager`
  - Support: `architect`, `coding`, `marketing`, `sales`
  - Required Skills: `market-research`, `automation`, `pricing`
""",
    "skill_loading_protocol.md": """# Skill Loading Protocol

Genesis dynamically determines which knowledge modules (skills) are required for a task based on the Agent Selection Protocol. 

## Loading Rules
- **Proactive Loading**: Do not load all skills. Load only what the task dictates.
- **Dependency Loading**: If a skill requires another skill (e.g., `simulation` requires `physics`), load the dependency.

## Examples
- **Physics Simulation**:
  - Load: `physics`, `advanced-physics`, `simulation`, `animation`
- **Business Product**:
  - Load: `market-analysis`, `product-validation`, `customer-discovery`, `pricing`
""",
    "self_improvement_protocol.md": """# Self Improvement Protocol

After every major task, Genesis must evaluate its performance to drive continuous evolution.

## 1. Performance
- What worked well? (e.g., fast convergence, accurate modeling)

## 2. Errors
- What failed? (e.g., compilation errors, faulty assumptions)

## 3. Missing Capability
- What knowledge, tool, or skill was missing during execution?

## 4. Improvement Action
Should Genesis:
- Create a new skill to cover the missing knowledge?
- Update an agent's charter or adapter?
- Update system documentation?
- Modify the orchestration workflow?

*Record the evaluation in the session log and trigger the appropriate generator.*
""",
    "memory_architecture.md": """# Memory Architecture

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
"""
}

for name, content in layers.items():
    with open(os.path.join(repo_root, "prompts", "system_layers", name), "w", encoding="utf-8") as f:
        f.write(content)


# Benchmarks
eval_dir = os.path.join(repo_root, "prompts", "benchmarks", "genesis_evaluation")
os.makedirs(eval_dir, exist_ok=True)
benchmarks = {
    "agent_metrics.md": """# Agent Evaluation Metrics

Measure the performance of individual agents across the following dimensions:
- **Reasoning Quality**: Are the decisions logically sound and documented?
- **Implementation Quality**: Does the output match the specification?
- **Autonomy**: Did the agent complete the task with minimal human intervention?
- **Reliability**: Does the agent consistently produce passing tests and valid structures?
""",
    "product_metrics.md": """# Product Evaluation Metrics

Measure the viability of products generated by the AI Solution Factory:
- **Market Potential**: Is there a clear target audience and demand?
- **User Value**: Does the product solve a real problem effectively?
- **Monetization**: Is there a viable pricing and revenue strategy?
""",
    "code_metrics.md": """# Code Evaluation Metrics

Measure the technical quality of the generated source code:
- **Maintainability**: Is the code modular, well-commented, and within complexity limits?
- **Security**: Are vulnerabilities absent? Are dependencies verified?
- **Performance**: Does the code execute efficiently without resource leaks?
"""
}

for name, content in benchmarks.items():
    with open(os.path.join(eval_dir, name), "w", encoding="utf-8") as f:
        f.write(content)


# MCP Architecture
mcp_content = """# MCP Architecture

Genesis connects to external tools, databases, APIs, and cloud services via the Model Context Protocol (MCP).

## Connectivity Patterns
- **MCP Servers**: Standardized external context and tool providers (e.g., file system access, postgres queries, external API clients).
- **Tool Proxies**: Direct REST/GraphQL calls wrapped in minimal agent-accessible scripts.

## Security Rules
1. **Never trust external tools automatically**. External data must be treated as untrusted and potentially malicious.
2. **Validate Permissions**: Ensure the agent calling the MCP tool has the appropriate access level.
3. **Validate Inputs**: Prevent prompt injection or malformed data before passing to an MCP tool.
4. **Validate Outputs**: Cleanse and verify the data returned from an MCP tool before integrating it into the codebase or memory.
"""
with open(os.path.join(repo_root, "docs", "MCP_ARCHITECTURE.md"), "w", encoding="utf-8") as f:
    f.write(mcp_content)

print("Files generated successfully.")
