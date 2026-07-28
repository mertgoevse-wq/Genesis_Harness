from genesis_runtime.runtime.lifecycle import AgentLifecycle, AgentState
from genesis_runtime.runtime.execution_context import ExecutionContext
from genesis_runtime.planner.task_decomposer import TaskDecomposer
from genesis_runtime.skill_system.skill_loader import DynamicSkillLoader

class GenesisRuntimeEngine:
    def __init__(self):
        self.decomposer = TaskDecomposer()
        self.skill_loader = DynamicSkillLoader()

    def execute_goal(self, goal: str) -> dict:
        ctx = ExecutionContext(goal)
        subtasks = self.decomposer.decompose(goal)

        results = []
        for task in subtasks:
            lifecycle = AgentLifecycle(task["agent"])
            lifecycle.transition_to(AgentState.PLANNING)
            
            skills = self.skill_loader.load_skills_for_agent(task["agent"])
            ctx.loaded_skills.extend(skills)
            
            lifecycle.transition_to(AgentState.READY)
            lifecycle.transition_to(AgentState.RUNNING)
            
            # Simulated Execution
            task_result = f"Executed {task['objective']} using skills: {skills}"
            
            lifecycle.transition_to(AgentState.EVALUATING)
            lifecycle.transition_to(AgentState.COMPLETED)
            
            results.append({
                "agent": task["agent"],
                "lifecycle_history": [s.value for s in lifecycle.history],
                "result": task_result
            })

        return {"goal": goal, "subtasks": results}
