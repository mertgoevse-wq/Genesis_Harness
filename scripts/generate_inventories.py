import os
import json

def get_directories(base_path):
    if not os.path.exists(base_path):
        return []
    return [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

def generate_agent_inventory():
    agents = get_directories("agents")
    inventory = ["# Agent Inventory\n"]
    
    for agent in agents:
        agent_dir = os.path.join("agents", agent)
        config_path = os.path.join(agent_dir, "config.json")
        desc = "No description"
        skills = []
        layer = "Unknown"
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    desc = config.get("description", desc)
                    skills = config.get("skills", skills)
                    layer = config.get("layer", layer)
            except Exception:
                pass
                
        inventory.append(f"## {agent}")
        inventory.append(f"- **Layer:** {layer}")
        inventory.append(f"- **Description:** {desc}")
        inventory.append(f"- **Skills:** {', '.join(skills) if skills else 'None specified'}")
        inventory.append("")
        
    with open("docs/AGENT_INVENTORY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(inventory))
    print(f"Generated docs/AGENT_INVENTORY.md with {len(agents)} agents.")

def generate_skill_inventory():
    skills = get_directories("skills")
    inventory = ["# Skill Inventory\n"]
    
    for skill in skills:
        skill_dir = os.path.join("skills", skill)
        config_path = os.path.join(skill_dir, "config.json")
        desc = "No description"
        capabilities = []
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    desc = config.get("description", desc)
                    capabilities = config.get("capabilities", capabilities)
            except Exception:
                pass
                
        inventory.append(f"## {skill}")
        inventory.append(f"- **Description:** {desc}")
        inventory.append(f"- **Capabilities:** {', '.join(capabilities) if capabilities else 'None specified'}")
        inventory.append("")
        
    with open("docs/SKILL_INVENTORY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(inventory))
    print(f"Generated docs/SKILL_INVENTORY.md with {len(skills)} skills.")

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    generate_agent_inventory()
    generate_skill_inventory()
