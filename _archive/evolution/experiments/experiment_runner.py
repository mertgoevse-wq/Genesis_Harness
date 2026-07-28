from typing import Dict, Any

class ExperimentRunner:
    def run_benchmark_experiment(self, candidate_id: str, baseline_score: float) -> Dict[str, Any]:
        # Simulated benchmark evaluation
        candidate_score = baseline_score + 0.05
        return {
            "candidate_id": candidate_id,
            "baseline_score": baseline_score,
            "candidate_score": candidate_score,
            "improvement": round(candidate_score - baseline_score, 4),
            "outcome": "PASSED" if candidate_score > baseline_score else "REJECTED"
        }
