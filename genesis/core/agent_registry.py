import os
import json
from typing import Any, Dict, List, Optional

class AgentRegistry:
    """Discovers agents and performs skill and capability matching."""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = agents_dir
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.discover_agents()

    def discover_agents(self) -> None:
        """Automatically scans for available agents."""
        if not os.path.exists(self.agents_dir):
            return
            
        for d in os.listdir(self.agents_dir):
            agent_path = os.path.join(self.agents_dir, d)
            if os.path.isdir(agent_path):
                config_path = os.path.join(agent_path, "config.json")
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            self.agents[d] = json.load(f)
                    except Exception:
                        pass

    def match_capabilities(self, required_capabilities: List[str]) -> Optional[str]:
        """Finds the best agent that matches required capabilities (skills)."""
        best_match = None
        best_score = -1
        
        for agent_id, config in self.agents.items():
            agent_skills = set(config.get("skills", []))
            required = set(required_capabilities)
            intersection = agent_skills.intersection(required)
            score = len(intersection)
            
            if score > best_score and score > 0:
                best_score = score
                best_match = agent_id
                
        return best_match

    def load_agent(self, agent_id: str) -> Dict[str, Any]:
        """Loads a specific agent and its metadata."""
        if agent_id in self.agents:
            return self.agents[agent_id]
        raise ValueError(f"Agent {agent_id} not found in registry.")

    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        return self.agents
