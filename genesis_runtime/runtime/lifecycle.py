from enum import Enum

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
