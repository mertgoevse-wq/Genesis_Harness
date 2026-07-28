import yaml
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
