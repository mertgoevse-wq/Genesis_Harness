import os
import sys

# Add root to pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genesis.core.agent_registry import AgentRegistry
from genesis.core.skill_loader import SkillLoader
from genesis.core.task_queue import WorkflowEngine
from genesis.core.meta_loop import MetaAgent

def main():
    print("==================================================")
    print("PHASE 15: AGENT EXECUTION VALIDATION")
    print("Test: ISLAM_TUTOR_ITERATION_002")
    print("Task: Verbessere den Namaz Trainer")
    print("==================================================\n")
    
    agent_registry = AgentRegistry()
    skill_loader = SkillLoader()
    workflow_engine = WorkflowEngine(max_workers=4)
    
    meta_agent = MetaAgent(
        agent_registry=agent_registry,
        skill_loader=skill_loader,
        workflow_engine=workflow_engine
    )
    
    meta_agent.run_development_loop("Verbessere den Namaz Trainer")

if __name__ == "__main__":
    main()
