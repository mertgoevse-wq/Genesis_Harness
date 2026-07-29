from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import concurrent.futures

@dataclass
class Task:
    """Represents a work unit for an agent."""
    id: str
    name: str = "Unknown Task"
    owning_agent: str = "general-purpose"
    func: Optional[Callable[..., Any]] = None
    kwargs: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    status: str = "PENDING"
    result: Any = None
    error: Optional[Exception] = None

class TaskQueue:
    """Manages tasks and their dependencies for parallel execution."""
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Task:
        return self.tasks[task_id]

    def get_ready_tasks(self) -> List[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status == "PENDING":
                deps_met = all(self.tasks[dep].status == "COMPLETED" for dep in task.dependencies)
                if deps_met:
                    ready.append(task)
        return ready

    def has_pending_tasks(self) -> bool:
        return any(t.status in ("PENDING", "RUNNING") for t in self.tasks.values())

class WorkflowEngine:
    """Executes task queues safely supporting parallel evaluation."""
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.queue = TaskQueue()

    def submit_task(self, task: Task):
        self.queue.add_task(task)

    def run_all(self) -> Dict[str, Any]:
        """Runs all tasks, respecting dependencies."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task_id = {}
            
            while self.queue.has_pending_tasks():
                ready_tasks = self.queue.get_ready_tasks()
                for task in ready_tasks:
                    task.status = "RUNNING"
                    future = executor.submit(task.func, **task.kwargs)
                    future_to_task_id[future] = task.id
                
                if not future_to_task_id:
                    # Circular dependency or stuck
                    break
                
                # Wait for at least one to finish
                done, not_done = concurrent.futures.wait(
                    future_to_task_id.keys(), return_when=concurrent.futures.FIRST_COMPLETED
                )
                
                for future in done:
                    task_id = future_to_task_id.pop(future)
                    task = self.queue.get_task(task_id)
                    try:
                        result = future.result()
                        task.result = result
                        task.status = "COMPLETED"
                    except Exception as exc:
                        print(f"[WorkflowEngine] Task {task.id} FAILED with error: {exc}")
                        task.error = exc
                        task.status = "FAILED"
                        
        return {tid: t.result for tid, t in self.queue.tasks.items() if t.status == "COMPLETED"}
