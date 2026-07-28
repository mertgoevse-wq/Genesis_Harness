from typing import Dict, Any, List

class PerformanceAnalyzer:
    def analyze_execution(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        agent_name = execution_data.get("agent", "unknown")
        latency_ms = execution_data.get("latency_ms", 1200)
        score = execution_data.get("evaluation_score", 0.88)
        cost = execution_data.get("cost_usd", 0.02)

        weaknesses = []
        if score < 0.90:
            weaknesses.append(f"Low evaluation score ({score}) for agent {agent_name}")
        if latency_ms > 2000:
            weaknesses.append(f"High execution latency ({latency_ms}ms)")

        return {
            "agent": agent_name,
            "metrics": {"score": score, "latency_ms": latency_ms, "cost_usd": cost},
            "weaknesses": weaknesses,
            "requires_optimization": len(weaknesses) > 0
        }
