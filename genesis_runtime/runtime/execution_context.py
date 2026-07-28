from typing import Dict, Any, List

class ExecutionContext:
    def __init__(self, goal: str):
        self.goal = goal
        self.loaded_skills: List[str] = []
        self.assigned_model: str = None
        self.payload: Dict[str, Any] = {}
        self.memory: Dict[str, Any] = {}
