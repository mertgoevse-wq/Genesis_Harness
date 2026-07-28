from enum import Enum

class AgentState(Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    LOADING_CONTEXT = "LOADING_CONTEXT"
    EXECUTING = "EXECUTING"
    COMMUNICATING = "COMMUNICATING"
    WAITING = "WAITING"
    EVALUATING = "EVALUATING"
    LEARNING = "LEARNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgentStateManager:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.current_state = AgentState.CREATED

    def transition_to(self, new_state: AgentState):
        self.current_state = new_state
        return self.current_state
