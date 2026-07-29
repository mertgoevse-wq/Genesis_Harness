import json
import os
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List

class ExecutionLayer:
    """Provides real execution boundaries for agents. Loads skills, runs logic, writes logs."""
    
    def __init__(self, skill_loader):
        self.skill_loader = skill_loader
        self.log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "agent_runs")
        os.makedirs(self.log_dir, exist_ok=True)
        
    def _notify_dashboard(self, task_id: str, agent: str, status: str, files_changed: List[str]):
        """Sends webhook to dashboard."""
        try:
            data = json.dumps({
                "agent": agent,
                "task": task_id,
                "status": status,
                "files": files_changed
            }).encode('utf-8')
            req = urllib.request.Request("http://localhost:8000/agent/event", data=data, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=1)
        except Exception:
            pass # Ignore if dashboard is not running
            
    def execute_agent_task(self, task_id: str, agent: str, description: str, skills: List[str]):
        """Simulates agent execution step-by-step."""
        print(f"[ExecutionLayer] Starting Task '{task_id}' assigned to '{agent}'...")
        self._notify_dashboard(task_id, agent, "RUNNING", [])
        
        # 1. Load Skills
        loaded_skills = []
        for s in skills:
            content = self.skill_loader.get_skill_content(s)
            loaded_skills.append(s)
        
        # 2. Simulate Work
        time.sleep(1.5) # Simulate processing time
        
        output_text = f"Agent {agent} completed task '{task_id}'. Used skills: {', '.join(loaded_skills)}."
        files_changed = [f"docs/agent_output_{task_id}.md"]
        
        # Physically create the changed file
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", f"agent_output_{task_id}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_text)
            
        # 3. Log Audit
        log_data = {
            "agent_name": agent,
            "used_skills": loaded_skills,
            "input_task": description,
            "output_result": output_text,
            "changed_files": files_changed,
            "status": "COMPLETED",
            "timestamp": time.time()
        }
        
        log_path = os.path.join(self.log_dir, f"{agent}_{task_id}.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4)
            
        self._notify_dashboard(task_id, agent, "COMPLETED", files_changed)
        print(f"[ExecutionLayer] Finished Task '{task_id}'. Log saved.")
        return log_data
