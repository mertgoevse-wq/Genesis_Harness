# Agent Selection Protocol

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
