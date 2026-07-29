import time
from typing import Any, Dict, Optional
from enum import Enum

class AgentState(Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgentStateStore:
    """Tracks the state of agents across the autonomous loop."""
    
    def __init__(self):
        self._states: Dict[str, Dict[str, Any]] = {}

    def transition_state(self, agent_id: str, new_state: AgentState, context: Optional[Dict[str, Any]] = None) -> None:
        """Transitions an agent to a new state and records the timestamp."""
        if agent_id not in self._states:
            self._states[agent_id] = {
                "history": [],
                "current_state": None,
                "context": {}
            }
        
        record = {
            "state": new_state.value,
            "timestamp": time.time(),
            "context": context or {}
        }
        
        self._states[agent_id]["history"].append(record)
        self._states[agent_id]["current_state"] = new_state.value
        if context:
            self._states[agent_id]["context"].update(context)

    def get_state(self, agent_id: str) -> Optional[str]:
        if agent_id in self._states:
            return self._states[agent_id]["current_state"]
        return None

    def get_full_history(self, agent_id: str) -> list:
        if agent_id in self._states:
            return self._states[agent_id]["history"]
        return []
