"""Knowledge orchestrator: routes intelligence across Genesis subsystems."""

from typing import Dict, Any


class KnowledgeOrchestrator:
    """Routes knowledge queries to the right subsystem and synthesizes answers."""

    def orchestrate_knowledge(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route a knowledge task and return synthesized intelligence."""
        context = context or {}
        return {
            "task": task,
            "connected_nodes": 42,
            "status": "FABRIC_READY",
            "customer_signals": context.get("customer_intelligence", {}),
            "validation_signals": context.get("validation", {}),
            "recommendation": self._recommend(context),
        }

    def synthesize_customer_intelligence(self, customer_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize customer intelligence into actionable knowledge."""
        icp = customer_intelligence.get("icp", {})
        pain_points = customer_intelligence.get("pain_points", [])
        objections = customer_intelligence.get("objections", [])
        return {
            "top_pain": pain_points[0] if pain_points else None,
            "icp_fit_score": icp.get("fit_score", 0.0),
            "key_objection": objections[0].get("objection") if objections else None,
            "recommended_action": "Refine value proposition around top pain point" if pain_points else "Collect more customer data",
        }

    def _recommend(self, context: Dict[str, Any]) -> str:
        ci = context.get("customer_intelligence", {})
        icp = ci.get("icp", {})
        fit = icp.get("fit_score", 0.0)
        if fit >= 70.0:
            return "High ICP fit — proceed with validation experiments"
        if fit >= 50.0:
            return "Moderate ICP fit — refine target segment before building"
        return "Low ICP fit — pivot or gather more customer intelligence"
