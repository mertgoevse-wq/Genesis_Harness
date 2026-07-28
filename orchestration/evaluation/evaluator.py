from typing import Dict, Any

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
