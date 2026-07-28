from typing import Dict, Any, List

class DependencyResolver:
    @staticmethod
    def get_executable_tasks(tasks: Dict[str, Dict[str, Any]]) -> List[str]:
        executable = []
        completed_ids = {t_id for t_id, t in tasks.items() if t["status"] == "COMPLETED"}

        for t_id, task in tasks.items():
            if task["status"] == "PENDING":
                deps = set(task.get("dependencies", []))
                if deps.issubset(completed_ids):
                    executable.append(t_id)
        return executable
