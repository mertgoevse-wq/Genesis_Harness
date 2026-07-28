import os
import json

agents = [
    {"id": "ceo", "name": "CEO", "roleClass": "Executive", "category": "Executive"},
    {"id": "cto", "name": "CTO", "roleClass": "Executive", "category": "Executive"},
    {"id": "research-director", "name": "Research Director", "roleClass": "Executive", "category": "Executive"},
    {"id": "innovation", "name": "Innovation", "roleClass": "Executive", "category": "Executive"},
    {"id": "frontend-engineer", "name": "Frontend Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "backend-engineer", "name": "Backend Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "database-engineer", "name": "Database Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "security-engineer", "name": "Security Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "devops-engineer", "name": "DevOps Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "performance-engineer", "name": "Performance Engineer", "roleClass": "Implementation", "category": "Development"},
    {"id": "market-research", "name": "Market Research", "roleClass": "Business", "category": "Business"},
    {"id": "growth", "name": "Growth", "roleClass": "Business", "category": "Business"},
    {"id": "seo", "name": "SEO", "roleClass": "Business", "category": "Business"},
    {"id": "customer-research", "name": "Customer Research", "roleClass": "Business", "category": "Business"},
    {"id": "revenue-optimization", "name": "Revenue Optimization", "roleClass": "Business", "category": "Business"},
    {"id": "code-reviewer", "name": "Code Reviewer", "roleClass": "Verification", "category": "Quality"},
    {"id": "security-auditor", "name": "Security Auditor", "roleClass": "Verification", "category": "Quality"},
    {"id": "testing", "name": "Testing", "roleClass": "Verification", "category": "Quality"},
    {"id": "ux-reviewer", "name": "UX Reviewer", "roleClass": "Verification", "category": "Quality"}
]

skills = [
    {"id": "agent-design", "name": "Agent Design", "category": "meta"},
    {"id": "evaluation", "name": "Evaluation", "category": "meta"},
    {"id": "market-analysis", "name": "Market Analysis", "category": "business"},
    {"id": "product-validation", "name": "Product Validation", "category": "business"},
    {"id": "pricing", "name": "Pricing", "category": "business"},
    {"id": "customer-discovery", "name": "Customer Discovery", "category": "business"},
    {"id": "architecture", "name": "Architecture", "category": "engineering"},
    {"id": "security", "name": "Security", "category": "engineering"},
    {"id": "testing", "name": "Testing", "category": "engineering"},
    {"id": "deployment", "name": "Deployment", "category": "engineering"},
    {"id": "ui-design", "name": "UI Design", "category": "creative"},
    {"id": "image-generation", "name": "Image Generation", "category": "creative"},
    {"id": "animation", "name": "Animation", "category": "creative"},
    {"id": "advanced-physics", "name": "Advanced Physics", "category": "science"}
]

repo_root = "c:\\Genesis_Harness"
agent_template_path = os.path.join(repo_root, "templates", "AGENT_TEMPLATE.md")
skill_template_path = os.path.join(repo_root, "templates", "SKILL_TEMPLATE.md")

with open(agent_template_path, 'r', encoding='utf-8') as f:
    agent_template = f.read()

with open(skill_template_path, 'r', encoding='utf-8') as f:
    skill_template = f.read()

# Generate Agents
for agent in agents:
    agent_dir = os.path.join(repo_root, "agents", agent['id'])
    os.makedirs(agent_dir, exist_ok=True)
    
    agent_content = agent_template.replace("<Agent Name>", agent['name'])
    agent_content = agent_content.replace("<kebab-case-id>", agent['id'])
    agent_content = agent_content.replace("<Software Architect | Research Lead | Implementation | Domain Science | Systems Design | Verification>", agent['roleClass'])
    
    # Save AGENT.md
    with open(os.path.join(agent_dir, "AGENT.md"), "w", encoding="utf-8") as f:
        f.write(agent_content)
        
    # Generate .claude/agents adapter
    adapter_content = f"""---
name: {agent['id']}
description: {agent['name']} agent handles {agent['category']} level tasks. Use PROACTIVELY when {agent['category']} tasks are required. Produces outputs for {agent['category']} workflows.
tools: bash, edit, read
---
"""
    claude_agents_dir = os.path.join(repo_root, ".claude", "agents")
    os.makedirs(claude_agents_dir, exist_ok=True)
    with open(os.path.join(claude_agents_dir, f"{agent['id']}.md"), "w", encoding="utf-8") as f:
        f.write(adapter_content)

# Generate Skills
for skill in skills:
    skill_dir = os.path.join(repo_root, "skills", skill['id'])
    os.makedirs(skill_dir, exist_ok=True)
    
    skill_content = skill_template.replace("<kebab-case-id>", skill['id'])
    skill_content = skill_content.replace("<Name>", skill['name'])
    skill_content = skill_content.replace("science | engineering | meta", skill['category'])
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
