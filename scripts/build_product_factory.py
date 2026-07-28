import os
import json

repo_root = "c:\\Genesis_Harness"

# 1. Directories to create
pf_dirs = [
    "docs/analysis",
    "docs/products",
    "product_factory/discovery",
    "product_factory/validation",
    "product_factory/strategy",
    "product_factory/product_management",
    "product_factory/ux",
    "product_factory/architecture",
    "product_factory/development",
    "product_factory/deployment",
    "product_factory/marketing",
    "product_factory/analytics",
    "product_factory/evaluation",
    "product_factory/pipeline",
    "product_factory/tests",
    "tests"
]
for d in pf_dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Product Factory Module\n")

# 2. Architecture Review Document
rev_doc = """# Genesis Architecture Review: Product Factory Autonomous OS

## Existing Capabilities
- **Genesis Runtime Engine**: Executable agent state machine and lifecycle manager.
- **Tool Intelligence & MCP Systems**: Dynamic tool discovery, cost/security evaluations, and MCP server binding.
- **Persistent Intelligence Memory**: Retrospective knowledge store synced with Knowledge Graph.
- **Self Evolution Loop**: Performance analysis, A/B benchmark experiment runner, and report generator.

## Integration Strategy for Product Factory
The Autonomous Product Factory operates as the high-level orchestration layer over the entire Genesis OS:
1. **Idea Ingestion**: Harvester signals feed directly into `product_factory/discovery`.
2. **Lifecycle Management**: `product_lifecycle.py` drives the state transitions (`IDEA -> RESEARCHING -> VALIDATING -> DESIGNING -> BUILDING -> TESTING -> DEPLOYING -> LAUNCHED -> LEARNING`).
3. **Execution Delegation**: Product requirements automatically spawn task DAGs inside `genesis_runtime` with precise agent and skill assignments.
4. **Memory Loop**: Post-launch evaluation results persist to `memory_system` to refine future product creation rounds.
"""
with open(os.path.join(repo_root, "docs", "analysis", "product_factory_architecture_review.md"), "w", encoding="utf-8") as f:
    f.write(rev_doc)

# 3. Product Lifecycle State Machine: product_factory/pipeline/product_lifecycle.py
lifecycle_code = '''from enum import Enum
from typing import Dict, Any

class ProductState(Enum):
    IDEA = "IDEA"
    RESEARCHING = "RESEARCHING"
    VALIDATING = "VALIDATING"
    DESIGNING = "DESIGNING"
    BUILDING = "BUILDING"
    TESTING = "TESTING"
    DEPLOYING = "DEPLOYING"
    LAUNCHED = "LAUNCHED"
    LEARNING = "LEARNING"

class ProductLifecycleEngine:
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.state = ProductState.IDEA

    def transition_to(self, new_state: ProductState) -> Dict[str, Any]:
        self.state = new_state
        return {"product": self.product_name, "state": self.state.value}
'''
with open(os.path.join(repo_root, "product_factory", "pipeline", "product_lifecycle.py"), "w", encoding="utf-8") as f:
    f.write(lifecycle_code)

# 4. PRD Generator: product_factory/product_management/prd_generator.py
prd_code = '''import os

class PRDGenerator:
    def __init__(self, output_dir: str = "docs/products"):
        self.output_dir = output_dir

    def generate_prd_package(self, product_name: str, details: dict) -> str:
        slug = product_name.lower().replace(" ", "_")
        target_dir = os.path.join(self.output_dir, slug)
        os.makedirs(target_dir, exist_ok=True)

        files = {
            "README.md": f"# {product_name}\\n\\n{details.get('summary', 'Autonomous AI Product')}",
            "PRD.md": f"# Product Requirement Document: {product_name}\\n\\n## Target Audience\\n{details.get('audience', 'Global Developers')}\\n\\n## Core Features\\n- AI Automation Engine",
            "Technical_Architecture.md": f"# Technical Architecture: {product_name}\\n\\n- Stack: Genesis Runtime, FastHTML, Supabase",
            "Business_Model.md": f"# Business Model: {product_name}\\n\\n- Pricing: SaaS Freemium ($29/mo)",
            "Launch_Plan.md": f"# Launch Plan: {product_name}\\n\\n- Channels: ProductHunt, HackerNews, X",
            "Risk_Analysis.md": f"# Risk Analysis: {product_name}\\n\\n- Low technical risk, high market demand",
            "Implementation_Roadmap.md": f"# Implementation Roadmap: {product_name}\\n\\n- Phase 1: MVP (Week 1)\\n- Phase 2: Launch (Week 2)"
        }

        for fname, content in files.items():
            with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        return target_dir
'''
with open(os.path.join(repo_root, "product_factory", "product_management", "prd_generator.py"), "w", encoding="utf-8") as f:
    f.write(prd_code)

# 5. Create 7 New Agents (AGENT.md & .claude/agents/ adapters)
new_agents = [
    ("product-founder", "Acts as startup founder. Evaluates ideas and market positioning."),
    ("customer-researcher", "Finds customer pain points and conducts user interviews."),
    ("business-modeler", "Creates pricing and revenue models."),
    ("ux-researcher", "Creates user flows and UI wireframes."),
    ("growth-strategist", "Creates acquisition strategies and GTM plans."),
    ("financial-analyst", "Performs revenue calculations and unit economics."),
    ("investor-agent", "Evaluates investment potential and pitch decks.")
]

for name, desc in new_agents:
    agent_dir = os.path.join(repo_root, "agents", name)
    os.makedirs(agent_dir, exist_ok=True)
    with open(os.path.join(agent_dir, "AGENT.md"), "w", encoding="utf-8") as f:
        f.write(f"# Agent Charter: {name}\n\n**Role:** {desc}\n")
    
    claude_agent_file = os.path.join(repo_root, ".claude", "agents", f"{name}.json")
    adapter_content = {
        "name": name,
        "description": desc,
        "prompt": f"You are the Genesis {name}. {desc}"
    }
    with open(claude_agent_file, "w", encoding="utf-8") as f:
        json.dump(adapter_content, f, indent=2)

# 6. Create 7 New Skills (SKILL.md)
new_skills = [
    ("startup-validation", "Validates market demand and problem-solution fit."),
    ("customer-development", "Guides customer interview synthesis and pain point mapping."),
    ("pricing-strategy", "Formulates tier pricing and revenue models."),
    ("ux-research", "Designs user journeys and interaction flows."),
    ("growth-marketing", "Defines GTM acquisition strategies and viral loops."),
    ("saas-development", "Guides fullstack SaaS architecture and development."),
    ("analytics", "Sets up retention, conversion, and telemetry metrics.")
]

for name, desc in new_skills:
    skill_dir = os.path.join(repo_root, "skills", name)
    os.makedirs(skill_dir, exist_ok=True)
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(f"""---
name: {name}
description: {desc}
---

# Skill: {name}
{desc}

## Purpose
Automate {name} within the Genesis Product Factory.
""")

# 7. Unit Tests: tests/test_product_factory.py
test_pf_code = '''import unittest
import os
from product_factory.pipeline.product_lifecycle import ProductLifecycleEngine, ProductState
from product_factory.product_management.prd_generator import PRDGenerator

class TestProductFactory(unittest.TestCase):
    def test_lifecycle_transitions(self):
        engine = ProductLifecycleEngine("ReviewPilot AI")
        self.assertEqual(engine.state, ProductState.IDEA)
        
        res = engine.transition_to(ProductState.RESEARCHING)
        self.assertEqual(res["state"], "RESEARCHING")

    def test_prd_generation(self):
        gen = PRDGenerator(output_dir="tests/test_products")
        out_dir = gen.generate_prd_package("AutoDoc SaaS", {"summary": "Automated documentation tool"})
        self.assertTrue(os.path.exists(os.path.join(out_dir, "PRD.md")))
        self.assertTrue(os.path.exists(os.path.join(out_dir, "Technical_Architecture.md")))

if __name__ == "__main__":
    unittest.main()
'''
with open(os.path.join(repo_root, "tests", "test_product_factory.py"), "w", encoding="utf-8") as f:
    f.write(test_pf_code)

print("Product Factory modules, agents, skills, and tests successfully built.")
