from agent_runtime.core.agent_lifecycle import AgentStateManager, AgentState
class AgentExecutor:
    def execute_agent(self, agent_name: str, task: str):
        sm = AgentStateManager(agent_name)
        sm.transition_to(AgentState.INITIALIZING)
        sm.transition_to(AgentState.EXECUTING)
        sm.transition_to(AgentState.COMPLETED)
        return {"agent": agent_name, "task": task, "state": sm.current_state.value}
