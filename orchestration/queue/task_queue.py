import uuid
from typing import Dict, Any, List

class TaskQueue:
    def __init__self:
        self.queue: Dict[str, Dict[str, Any]] = {}

    def add_task(self, agent_name: str, objective: str, payload: Dict[str, Any] = None, dependencies: List[str] = None) -> str:
        task_id = str(uuid.uuid4())
        self.queue[task_id] = {
            "id": task_id,
            "agent": agent_name,
            "objective": objective,
            "payload": payload or {},
            "dependencies": dependencies or [],
            "status": "PENDING",
            "result": None
        }
        return task_id

    def get_pending_tasks(self -> List[Dict[str, Any]]:
        return [t for t in self.queue.values() if t["status"] == "PENDING"]

    def update_status(self, task_id: str, status: str, result: Any = None):
        if task_id in self.queue:
            self.queue[task_id]["status"] = status
            if result is not None:
                self.queue[task_id]["result"] = result
