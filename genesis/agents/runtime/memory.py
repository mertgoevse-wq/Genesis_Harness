import json
import os
import time
from typing import Dict, Any, List

class AgentStateStore:
    """Manages short-term (context) and long-term (logs/knowledge) memory for an agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.context: List[Dict[str, Any]] = []
        self.memory_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs", "memory", self.agent_id)
        os.makedirs(self.memory_dir, exist_ok=True)
        
    def add_to_context(self, role: str, content: str):
        """Adds a short-term memory observation or thought to the active context."""
        self.context.append({"role": role, "content": content, "timestamp": time.time()})
        
    def get_context(self) -> List[Dict[str, Any]]:
        return self.context
        
    def clear_context(self):
        self.context = []

    def save_long_term_memory(self, task_id: str, success: bool, used_skills: List[str], learnings: str):
        """Stores persistent findings after task completion."""
        memory_entry = {
            "task_id": task_id,
            "success": success,
            "used_skills": used_skills,
            "learnings": learnings,
            "timestamp": time.time()
        }
        
        file_path = os.path.join(self.memory_dir, f"memory_{task_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(memory_entry, f, indent=4)
            
    def retrieve_past_learnings(self) -> List[Dict[str, Any]]:
        """Loads past memories for context."""
        learnings = []
        if not os.path.exists(self.memory_dir):
            return learnings
            
        for file in os.listdir(self.memory_dir):
            if file.endswith(".json"):
                with open(os.path.join(self.memory_dir, file), "r", encoding="utf-8") as f:
                    learnings.append(json.load(f))
        return learnings
