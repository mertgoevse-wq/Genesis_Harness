import os

repo_root = "c:\\Genesis_Harness"

# Directories
dirs = [
    "genesis_runtime/runtime",
    "genesis_runtime/planner",
    "genesis_runtime/agent_execution",
    "genesis_runtime/skill_system",
    "genesis_runtime/memory",
    "genesis_runtime/events",
    "tests"
]
for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Genesis Runtime Engine Module\n")

# 1. Lifecycle State Machine: genesis_runtime/runtime/lifecycle.py
lifecycle_code = '''from enum import Enum

class AgentState(Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    READY = "READY"
    RUNNING = "RUNNING"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgentLifecycle:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.current_state = AgentState.CREATED
        self.history = [AgentState.CREATED]

    def transition_to(self, new_state: AgentState):
        self.current_state = new_state
        self.history.append(new_state)
        return self.current_state
'''
with open(os.path.join(repo_root, "genesis_runtime", "runtime", "lifecycle.py"), "w", encoding="utf-8") as f:
    f.write(lifecycle_code)

# Execution Context: genesis_runtime/runtime/execution_context.py
context_code = '''from typing import Dict, Any, List

class ExecutionContext:
    def __init__(self, goal: str):
        self.goal = goal
        self.loaded_skills: List[str] = []
        self.assigned_model: str = None
        self.payload: Dict[str, Any] = {}
        self.memory: Dict[str, Any] = {}
'''
with open(os.path.join(repo_root, "genesis_runtime", "runtime", "execution_context.py"), "w", encoding="utf-8") as f:
    f.write(context_code)

# Engine Coordinator: genesis_runtime/runtime/engine.py
engine_code = '''from genesis_runtime.runtime.lifecycle import AgentLifecycle, AgentState
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
'''
with open(os.path.join(repo_root, "genesis_runtime", "runtime", "engine.py"), "w", encoding="utf-8") as f:
    f.write(engine_code)

# 2. Planner: genesis_runtime/planner/task_decomposer.py
decomposer_code = '''from typing import List, Dict, Any

class TaskDecomposer:
    def decompose(self, goal: str) -> List[Dict[str, Any]]:
        # High level goal decomposition
        return [
            {"agent": "market-research", "objective": "Market Analysis"},
            {"agent": "product-manager", "objective": "Product Requirements Document (PRD)"},
            {"agent": "architect", "objective": "System Design"},
            {"agent": "coding", "objective": "Core Feature Implementation"},
            {"agent": "qa", "objective": "Testing Suite Verification"},
            {"agent": "growth", "objective": "Go-to-Market Strategy"}
        ]
'''
with open(os.path.join(repo_root, "genesis_runtime", "planner", "task_decomposer.py"), "w", encoding="utf-8") as f:
    f.write(decomposer_code)

with open(os.path.join(repo_root, "genesis_runtime", "planner", "goal_analyzer.py"), "w", encoding="utf-8") as f:
    f.write('''class GoalAnalyzer:\n    def analyze(self, goal: str) -> dict:\n        return {"goal": goal, "complexity": "HIGH", "category": "AI SaaS"}\n''')

# 3. Agent Execution: genesis_runtime/agent_execution/agent_runner.py & sandbox.py
with open(os.path.join(repo_root, "genesis_runtime", "agent_execution", "agent_runner.py"), "w", encoding="utf-8") as f:
    f.write('''class AgentRunner:\n    def run(self, agent_name: str, context: dict) -> dict:\n        return {"status": "SUCCESS", "output": f"Runner executed {agent_name}"}\n''')

with open(os.path.join(repo_root, "genesis_runtime", "agent_execution", "sandbox.py"), "w", encoding="utf-8") as f:
    f.write('''class ExecutionSandbox:\n    def execute_safe(self, func, *args):\n        return func(*args)\n''')

# 4. Skill System: genesis_runtime/skill_system/skill_loader.py & skill_registry.py
skill_loader_code = '''from typing import List

class DynamicSkillLoader:
    def __init__(self):
        self.mappings = {
            "coding": ["software-engineering", "testing", "security"],
            "architect": ["architecture", "software-engineering"],
            "market-research": ["market-analysis", "customer-discovery"],
            "product-manager": ["product-validation", "pricing"],
            "qa": ["testing", "security"],
            "growth": ["marketing", "sales"]
        }

    def load_skills_for_agent(self, agent_name: str) -> List[str]:
        return self.mappings.get(agent_name, ["software-engineering"])
'''
with open(os.path.join(repo_root, "genesis_runtime", "skill_system", "skill_loader.py"), "w", encoding="utf-8") as f:
    f.write(skill_loader_code)

with open(os.path.join(repo_root, "genesis_runtime", "skill_system", "skill_registry.py"), "w", encoding="utf-8") as f:
    f.write('''class SkillRegistry:\n    def get_skill(self, name: str):\n        return {"name": name, "status": "LOADED"}\n''')

# 5. Memory: genesis_runtime/memory/short_term_memory.py & long_term_memory.py
with open(os.path.join(repo_root, "genesis_runtime", "memory", "short_term_memory.py"), "w", encoding="utf-8") as f:
    f.write('''class ShortTermMemory:\n    def __init__(self):\n        self.cache = {}\n''')

with open(os.path.join(repo_root, "genesis_runtime", "memory", "long_term_memory.py"), "w", encoding="utf-8") as f:
    f.write('''class LongTermMemory:\n    def __init__(self):\n        self.store = {}\n''')

# 6. Events: genesis_runtime/events/runtime_events.py
with open(os.path.join(repo_root, "genesis_runtime", "events", "runtime_events.py"), "w", encoding="utf-8") as f:
    f.write('''class RuntimeEvents:\n    def emit(self, event_name: str, payload: dict):\n        return {"event": event_name, "payload": payload}\n''')

# 7. Unit Tests: tests/test_runtime.py
test_runtime_code = '''import unittest
from genesis_runtime.runtime.lifecycle import AgentLifecycle, AgentState
from genesis_runtime.runtime.engine import GenesisRuntimeEngine
from genesis_runtime.planner.task_decomposer import TaskDecomposer
from genesis_runtime.skill_system.skill_loader import DynamicSkillLoader

class TestGenesisRuntime(unittest.TestCase):
    def test_agent_lifecycle(self):
        lc = AgentLifecycle("test_agent")
        self.assertEqual(lc.current_state, AgentState.CREATED)
        lc.transition_to(AgentState.RUNNING)
        self.assertEqual(lc.current_state, AgentState.RUNNING)
        self.assertEqual(len(lc.history), 2)

    def test_task_decomposition(self):
        decomposer = TaskDecomposer()
        subtasks = decomposer.decompose("Baue eine SaaS App")
        self.assertEqual(len(subtasks), 6)
        self.assertEqual(subtasks[0]["agent"], "market-research")

    def test_dynamic_skill_loading(self):
        loader = DynamicSkillLoader()
        skills = loader.load_skills_for_agent("coding")
        self.assertIn("software-engineering", skills)
        self.assertIn("testing", skills)
        self.assertIn("security", skills)

    def test_runtime_engine_execution(self):
        engine = GenesisRuntimeEngine()
        res = engine.execute_goal("Baue eine SaaS App")
        self.assertEqual(len(res["subtasks"]), 6)

if __name__ == "__main__":
    unittest.main()
'''
with open(os.path.join(repo_root, "tests", "test_runtime.py"), "w", encoding="utf-8") as f:
    f.write(test_runtime_code)

print("Genesis Runtime Engine files built successfully.")
