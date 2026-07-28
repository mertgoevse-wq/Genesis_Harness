import json
import os

repo_root = "c:\\Genesis_Harness"
harness_path = os.path.join(repo_root, "configs", "harness.config.json")
agent_reg_path = os.path.join(repo_root, "configs", "agent_registry.json")
skill_reg_path = os.path.join(repo_root, "configs", "skill_registry.json")

new_agents = [
    {"id": "ceo", "name": "CEO", "roleClass": "Executive"},
    {"id": "cto", "name": "CTO", "roleClass": "Executive"},
    {"id": "research-director", "name": "Research Director", "roleClass": "Executive"},
    {"id": "innovation", "name": "Innovation", "roleClass": "Executive"},
    {"id": "frontend-engineer", "name": "Frontend Engineer", "roleClass": "Implementation"},
    {"id": "backend-engineer", "name": "Backend Engineer", "roleClass": "Implementation"},
    {"id": "database-engineer", "name": "Database Engineer", "roleClass": "Implementation"},
    {"id": "security-engineer", "name": "Security Engineer", "roleClass": "Implementation"},
    {"id": "devops-engineer", "name": "DevOps Engineer", "roleClass": "Implementation"},
    {"id": "performance-engineer", "name": "Performance Engineer", "roleClass": "Implementation"},
    {"id": "market-research", "name": "Market Research", "roleClass": "Business"},
    {"id": "growth", "name": "Growth", "roleClass": "Business"},
    {"id": "seo", "name": "SEO", "roleClass": "Business"},
    {"id": "customer-research", "name": "Customer Research", "roleClass": "Business"},
    {"id": "revenue-optimization", "name": "Revenue Optimization", "roleClass": "Business"},
    {"id": "code-reviewer", "name": "Code Reviewer", "roleClass": "Verification"},
    {"id": "security-auditor", "name": "Security Auditor", "roleClass": "Verification"},
    {"id": "testing", "name": "Testing", "roleClass": "Verification"},
    {"id": "ux-reviewer", "name": "UX Reviewer", "roleClass": "Verification"}
]

new_skills = [
    {"id": "agent-design", "category": "meta"},
    {"id": "evaluation", "category": "meta"},
    {"id": "market-analysis", "category": "business"},
    {"id": "product-validation", "category": "business"},
    {"id": "pricing", "category": "business"},
    {"id": "customer-discovery", "category": "business"},
    {"id": "architecture", "category": "engineering"},
    {"id": "security", "category": "engineering"},
    {"id": "testing", "category": "engineering"},
    {"id": "deployment", "category": "engineering"},
    {"id": "ui-design", "category": "creative"},
    {"id": "image-generation", "category": "creative"},
    {"id": "animation", "category": "creative"},
    {"id": "advanced-physics", "category": "science"}
]

with open(harness_path, 'r', encoding='utf-8') as f:
    harness = json.load(f)

for a in new_agents:
    harness["agents"].append({
        "id": a["id"],
        "name": a["name"] + " Agent",
        "roleClass": a["roleClass"],
        "owns": f"Outputs for {a['roleClass']}",
        "canBlock": None,
        "charter": f"agents/{a['id']}/AGENT.md",
        "adapter": f".claude/agents/{a['id']}.md",
        "primarySkills": [],
        "supportingSkills": [],
        "masterPrompt": None
    })

for s in new_skills:
    harness["skills"].append({
        "id": s["id"],
        "category": s["category"],
        "path": f"skills/{s['id']}/SKILL.md"
    })
    
# Add new system layers to harness
new_layers = [
    {"id": "L6", "name": "Genesis Cognitive OS", "path": "prompts/system_layers/genesis_cognitive_os.md", "loadOrder": 6, "always": True},
    {"id": "L7", "name": "Agent Selection Protocol", "path": "prompts/system_layers/agent_selection_protocol.md", "loadOrder": 7, "always": True},
    {"id": "L8", "name": "Skill Loading Protocol", "path": "prompts/system_layers/skill_loading_protocol.md", "loadOrder": 8, "always": True},
    {"id": "L9", "name": "Self Improvement Protocol", "path": "prompts/system_layers/self_improvement_protocol.md", "loadOrder": 9, "always": True},
    {"id": "L10", "name": "Memory Architecture", "path": "prompts/system_layers/memory_architecture.md", "loadOrder": 10, "always": True}
]
harness["systemLayers"].extend(new_layers)

with open(harness_path, 'w', encoding='utf-8') as f:
    json.dump(harness, f, indent=2)


with open(agent_reg_path, 'r', encoding='utf-8') as f:
    agent_reg = json.load(f)

for a in new_agents:
    agent_reg["agents"].append(a["id"])

with open(agent_reg_path, 'w', encoding='utf-8') as f:
    json.dump(agent_reg, f, indent=2)
    
with open(skill_reg_path, 'r', encoding='utf-8') as f:
    skill_reg = json.load(f)

for s in new_skills:
    skill_reg["skills"].append(s["id"])
    
with open(skill_reg_path, 'w', encoding='utf-8') as f:
    json.dump(skill_reg, f, indent=2)

print("Registries updated")
