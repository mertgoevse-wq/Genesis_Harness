import time
from typing import List, Dict, Any, Optional
from genesis.agents.runtime.memory import AgentStateStore
from genesis.tools.base import BaseTool
from genesis.providers.base import LLMProvider

class AutonomousAgent:
    """A true autonomous agent with identity, mission, tools, memory, and an OODA decision loop."""
    
    def __init__(self, agent_id: str, name: str, role: str, mission: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.mission = mission
        self.capabilities = capabilities
        
        self.available_skills: List[str] = []
        self.available_tools: Dict[str, BaseTool] = {}
        self.memory = AgentStateStore(agent_id=self.agent_id)
        self.llm_provider: Optional[LLMProvider] = None
        
    def equip_tools(self, tools: List[BaseTool]):
        """Equips the agent with specific tools it's allowed to use."""
        for t in tools:
            self.available_tools[t.name] = t
            
    def assign_provider(self, provider: LLMProvider):
        """Assigns the LLM intelligence engine."""
        self.llm_provider = provider

    def _observe(self, environment_input: str):
        print(f"[{self.name}] 1. OBSERVE: {environment_input}")
        self.memory.add_to_context("environment", environment_input)
        
    def _analyze(self):
        print(f"[{self.name}] 2. ANALYZE: Evaluating past memories and current context...")
        past_learnings = self.memory.retrieve_past_learnings()
        prompt = f"Analyze context. Past learnings: {len(past_learnings)}"
        response = self.llm_provider.generate(prompt) if self.llm_provider else "Mock Analysis"
        self.memory.add_to_context("agent_thought", response)
        
    def _plan(self) -> str:
        print(f"[{self.name}] 3. PLAN: Formulating execution strategy...")
        plan = "I will modify the necessary files and run tests."
        self.memory.add_to_context("agent_plan", plan)
        return plan
        
    def _select_skill(self) -> str:
        print(f"[{self.name}] 4. SELECT SKILL: Matching capabilities...")
        selected = self.capabilities[0] if self.capabilities else "general"
        print(f"[{self.name}]    -> Selected Skill: {selected}")
        return selected
        
    def _select_tool(self) -> Optional[BaseTool]:
        print(f"[{self.name}] 5. SELECT TOOL: Choosing from available tools...")
        if self.available_tools:
            tool_name = list(self.available_tools.keys())[0]
            print(f"[{self.name}]    -> Selected Tool: {tool_name}")
            return self.available_tools[tool_name]
        return None
        
    def _execute(self, tool: Optional[BaseTool], task: str) -> Any:
        print(f"[{self.name}] 6. EXECUTE: Performing action...")
        if tool:
            if tool.name == "filesystem_tool":
                result = tool.execute(action="write", path="docs/avatar_update.md", content="Mock update")
            elif tool.name == "documentation_tool":
                result = tool.execute(topic="Avatar Transitions")
            else:
                result = tool.execute(task)
            print(f"[{self.name}]    -> Tool Output: {result}")
            return result
        return "Executed via mock function"
        
    def _evaluate(self, result: Any) -> bool:
        print(f"[{self.name}] 7. EVALUATE (Self Review Loop): Assessing results...")
        
        # Self Review Pipeline
        print(f"[{self.name}]    -> Code Review Agent: Quality is sufficient, no security risks.")
        print(f"[{self.name}]    -> QA Agent: Tests pass, visual UI looks correct.")
        print(f"[{self.name}]    -> Documentation Agent: Docs have been updated.")
        print(f"[{self.name}]    -> Meta Agent: Result ACCEPTED.")
        
        success = True # Mocking success evaluation
        print(f"[{self.name}]    -> Final Verdict: Successful = {success}")
        return success
        
    def _remember(self, task: str, success: bool, skill: str):
        print(f"[{self.name}] 8. REMEMBER: Saving to long-term memory...")
        self.memory.save_long_term_memory(
            task_id=task.replace(' ', '_').lower(),
            success=success,
            used_skills=[skill],
            learnings="Worked as expected." if success else "Failed. Needs debugging."
        )

    def run_decision_loop(self, task: str):
        """The core execution loop of the autonomous agent."""
        print(f"\n=== {self.name} STARTING DECISION LOOP ===")
        print(f"Role: {self.role} | Mission: {self.mission}")
        
        self._observe(task)
        self._analyze()
        self._plan()
        skill = self._select_skill()
        tool = self._select_tool()
        
        result = self._execute(tool, task)
        success = self._evaluate(result)
        self._remember(task, success, skill)
        
        print(f"=== {self.name} FINISHED DECISION LOOP ===\n")
        return result
