import time
from typing import List, Dict, Any
from .task_queue import WorkflowEngine, Task
from .agent_registry import AgentRegistry
from .skill_loader import SkillLoader

class MetaAgent:
    """Orchestrates the entire development loop: Goal -> Plan -> Distribute -> Execute -> QA."""
    
    def __init__(self, agent_registry: AgentRegistry, skill_loader: SkillLoader, workflow_engine: WorkflowEngine):
        self.agent_registry = agent_registry
        self.skill_loader = skill_loader
        self.workflow_engine = workflow_engine

    def analyze_goal(self, goal: str) -> List[Dict[str, Any]]:
        """Mock: MetaAgent analyzes goal and generates tasks."""
        print(f"[MetaAgent] Analysiere Ziel: {goal}")
        
        if "Verbessere den Namaz Trainer" in goal:
            return [
                {"id": "arch_analysis", "required_skills": ["python-fastapi-backend", "architecture"], "description": "Analysiert aktuelle Architektur.", "target_agent": "Software Architect"},
                {"id": "research_ux", "required_skills": ["research-analysis"], "description": "Analysiert beste Lösungen für interaktive Gebetslernapps.", "target_agent": "Research Agent"},
                {"id": "arabic_check", "required_skills": ["islamic-knowledge"], "description": "Prüft Arabisch/Tajweed Anforderungen.", "target_agent": "Arabic Agent"},
                {"id": "ui_planning", "required_skills": ["ui-design"], "description": "Plant Avatar Interface.", "dependencies": ["arch_analysis", "research_ux"], "target_agent": "UI Agent"},
                {"id": "animation_plan", "required_skills": ["ui-design"], "description": "Plant Bewegungsabläufe.", "dependencies": ["ui_planning"], "target_agent": "Animation Agent"},
                {"id": "voice_sync", "required_skills": ["text-to-speech"], "description": "Plant Audio Synchronisation.", "dependencies": ["arabic_check"], "target_agent": "Voice Agent"},
                {"id": "qa_testing", "required_skills": ["software-testing"], "description": "Erstellt Tests.", "dependencies": ["animation_plan", "voice_sync"], "target_agent": "QA Agent"},
                {"id": "visual_qa", "required_skills": ["visual-testing"], "description": "Erstellt UI Bewertungsprozess.", "dependencies": ["ui_planning"], "target_agent": "Visual QA Agent"}
            ]
        
        # Fallback
        return [
            {"id": "content_validation", "required_skills": ["islamic-knowledge"], "description": "Prüfe Quran-Texte", "target_agent": "general-purpose"}
        ]

    def create_workflow(self, task_definitions: List[Dict[str, Any]]):
        """Creates Tasks and assigns Agents dynamically using AgentRegistry."""
        # Need execution layer to bind function
        from genesis.core.execution_layer import ExecutionLayer
        exec_layer = ExecutionLayer(self.skill_loader)
        
        for td in task_definitions:
            # Capability match (Simulation for now, or just use explicitly requested agent)
            best_agent = td.get("target_agent", self.agent_registry.match_capabilities(td.get("required_skills", [])))
            if not best_agent:
                best_agent = "general-purpose"
                
            task = Task(
                id=td["id"],
                name=td["description"],
                owning_agent=best_agent,
                dependencies=td.get("dependencies", []),
                func=exec_layer.execute_agent_task,
                kwargs={
                    "task_id": td["id"],
                    "agent": best_agent,
                    "description": td["description"],
                    "skills": td.get("required_skills", [])
                }
            )
            self.workflow_engine.queue.add_task(task)
            print(f"[MetaAgent] Task {task.id} an Agent {best_agent} zugewiesen.")

    def run_development_loop(self, goal: str):
        """Runs the fully autonomous project loop."""
        print("\n--- START AUTONOMOUS PROJECT LOOP ---")
        
        # 1. Analyse Target
        task_defs = self.analyze_goal(goal)
        
        # 2. Planner (Create Tasks & Assign Agents)
        self.create_workflow(task_defs)
        
        # 3. Agents get tasks (Parallel Execution)
        print("\n[MetaAgent] Starte Workflow Engine für parallele Ausführung...")
        results = self.workflow_engine.run_all()
        
        # 4. Mocking Test, QA, Docs, Status Iteration
        print("\n[MetaAgent] Ausführung abgeschlossen. Resultate:")
        print(results)
        
        print("[MetaAgent] Dokumentation aktualisiert. Status: COMPLETED.")
        print("--- END AUTONOMOUS PROJECT LOOP ---\n")
