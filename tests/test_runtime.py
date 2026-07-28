import unittest
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
