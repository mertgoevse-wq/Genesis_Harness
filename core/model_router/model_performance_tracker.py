class ModelPerformanceTracker:
    def __init__(self):
        self.metrics = {
            "Claude Opus": {"tasks": 120, "avg_quality": 0.98, "preferred_task": "Architecture"},
            "Claude Sonnet": {"tasks": 450, "avg_quality": 0.95, "preferred_task": "Coding"},
            "Gemini Flash": {"tasks": 800, "avg_quality": 0.91, "preferred_task": "Documentation"}
        }

    def route_by_complexity(self, task_type: str, complexity_score: float) -> str:
        if complexity_score > 0.8:
            return "Claude Opus"
        elif complexity_score > 0.4:
            return "Claude Sonnet"
        return "Gemini Flash"
