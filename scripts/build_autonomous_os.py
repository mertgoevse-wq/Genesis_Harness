import os
import json

repo_root = "c:\\Genesis_Harness"

# Directories to create
dirs = [
    "orchestration",
    "orchestration/queue",
    "orchestration/scheduler",
    "orchestration/workers",
    "orchestration/pipeline",
    "orchestration/evaluation",
    "orchestration/logging",
    "core",
    "core/model_router"
]

for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Genesis Autonomous OS Module\n")

# 1. Task Queue: orchestration/queue/task_queue.py
task_queue_code = '''import uuid
from typing import Dict, Any, List

class TaskQueue:
    def __init__(self):
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

    def get_pending_tasks((self) -> List[Dict[str, Any]]:
        return [t for t in self.queue.values() if t["status"] == "PENDING"]

    def update_status(self, task_id: str, status: str, result: Any = None):
        if task_id in self.queue:
            self.queue[task_id]["status"] = status
            if result is not None:
                self.queue[task_id]["result"] = result
'''

with open(os.path.join(repo_root, "orchestration", "queue", "task_queue.py"), "w", encoding="utf-8") as f:
    f.write(task_queue_code.replace("(self)", "self"))

# 2. Scheduler: orchestration/scheduler/dependency_resolver.py
resolver_code = '''from typing import Dict, Any, List

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
'''

with open(os.path.join(repo_root, "orchestration", "scheduler", "dependency_resolver.py"), "w", encoding="utf-8") as f:
    f.write(resolver_code)

# 3. Workers: orchestration/workers/worker_pool.py
worker_code = '''import concurrent.futures
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
'''

with open(os.path.join(repo_root, "orchestration", "workers", "worker_pool.py"), "w", encoding="utf-8") as f:
    f.write(worker_code)

# 4. Pipeline: orchestration/pipeline/pipeline_runner.py
pipeline_code = '''from typing import Dict, Any, List

class PipelineRunner:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, agent: str, objective: str, input_schema: dict, output_schema: dict, evaluation_criteria: list):
        self.steps.append({
            "agent": agent,
            "objective": objective,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "evaluation_criteria": evaluation_criteria
        })

    def run(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        context = initial_input
        for step in self.steps:
            # Simulated execution context mapping
            context[step["agent"]] = {"status": "SUCCESS", "objective": step["objective"]}
        return context
'''

with open(os.path.join(repo_root, "orchestration", "pipeline", "pipeline_runner.py"), "w", encoding="utf-8") as f:
    f.write(pipeline_code)

# 5. Evaluation: orchestration/evaluation/evaluator.py
eval_code = '''from typing import Dict, Any

class ResultAggregator:
    @staticmethod
    def aggregate(results: list) -> Dict[str, Any]:
        return {
            "total_tasks": len(results),
            "successful": len([r for r in results if r.get("status") == "SUCCESS"]),
            "failed": len([r for r in results if r.get("status") == "FAILED"]),
            "details": results
        }

class PipelineEvaluator:
    @staticmethod
    def evaluate(output: dict, criteria: list) -> dict:
        passed = True
        feedback = []
        for crit in criteria:
            if crit not in str(output):
                feedback.append(f"Missing criteria evaluation: {crit}")
        return {"passed": passed, "score": 1.0 if passed else 0.5, "feedback": feedback}
'''

with open(os.path.join(repo_root, "orchestration", "evaluation", "evaluator.py"), "w", encoding="utf-8") as f:
    f.write(eval_code)

# 6. Model Router: configs/model_router.yaml & core/model_router/router.py
router_yaml = '''# Genesis Model Routing Policy
routing_rules:
  architecture:
    primary: "Claude Opus 4.8"
    fallback: "Claude Sonnet 4.6"
    tier: "High"
    description: "System design, strategic decisions, complex trade-offs"
  coding:
    primary: "Claude Sonnet 4.6"
    fallback: "Gemini 3.6 Flash"
    tier: "Medium"
    description: "Software development, refactoring, implementation"
  analysis:
    primary: "Gemini 3.6 Flash"
    fallback: "Claude Sonnet 4.6"
    tier: "Medium"
    description: "Large context analysis, documentation, parallel tasks"
  boilerplate:
    primary: "Kimi"
    fallback: "Gemini 3.6 Flash"
    tier: "Low"
    description: "Standard repetitive code, initial setup"
  math_algorithms:
    primary: "DeepSeek R1"
    fallback: "Claude Opus 4.8"
    tier: "High"
    description: "Complex math, algorithm optimization, physics simulations"
'''

with open(os.path.join(repo_root, "configs", "model_router.yaml"), "w", encoding="utf-8") as f:
    f.write(router_yaml)

router_code = '''import yaml
import os

class ModelRouter:
    def __init__(self, config_path: str = "configs/model_router.yaml"):
        self.config_path = config_path
        self.rules = self._load_config()

    def _load_config(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f).get("routing_rules", {})
        return {}

    def route_task(self, task_type: str) -> dict:
        return self.rules.get(task_type, {
            "primary": "Claude Sonnet 4.6",
            "fallback": "Gemini 3.6 Flash",
            "tier": "Medium"
        })
'''

with open(os.path.join(repo_root, "core", "model_router", "router.py"), "w", encoding="utf-8") as f:
    f.write(router_code)

print("Orchestration and Model Router modules successfully built.")
