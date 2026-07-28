# Skill Loading Protocol

Genesis dynamically determines which knowledge modules (skills) are required for a task based on the Agent Selection Protocol. 

## Loading Rules
- **Proactive Loading**: Do not load all skills. Load only what the task dictates.
- **Dependency Loading**: If a skill requires another skill (e.g., `simulation` requires `physics`), load the dependency.

## Examples
- **Physics Simulation**:
  - Load: `physics`, `advanced-physics`, `simulation`, `animation`
- **Business Product**:
  - Load: `market-analysis`, `product-validation`, `customer-discovery`, `pricing`
