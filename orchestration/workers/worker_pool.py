import concurrent.futures
from typing import Dict, Any, Callable

class AgentWorkerPool:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def execute_parallel(self, task_fn: Callable, tasks: list) -> list:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(task_fn, task): task for task in tasks}
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    res = future.result()
                    results.append(res)
                except Exception as exc:
                    results.append({"error": str(exc)})
        return results
