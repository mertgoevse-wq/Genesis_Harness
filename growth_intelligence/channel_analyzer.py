"""Marketing channel analysis for growth intelligence."""

from typing import Dict, Any, List


class ChannelAnalyzer:
    """Analyzes and recommends marketing channels for a SaaS product."""

    def analyze(self, product: str, context: Dict[str, Any]) -> Dict[str, Any]:
        budget = context.get("marketing_budget", "medium")
        audience = context.get("target_audience", "small businesses")
        channels = self._channels_for_budget(budget, audience)
        return {
            "product": product,
            "budget": budget,
            "audience": audience,
            "channels": channels,
            "expected_cac": self._cac(budget),
            "recommended_mix": channels[:3],
            "risk_notes": self._risks(budget),
        }

    def _channels_for_budget(self, budget: str, audience: str) -> List[Dict[str, Any]]:
        channels = {
            "low": [
                {"channel": "SEO", "potential": "high", "time_to_result": "months"},
                {"channel": "Content marketing", "potential": "high", "time_to_result": "months"},
                {"channel": "Community engagement", "potential": "medium", "time_to_result": "weeks"},
            ],
            "medium": [
                {"channel": "SEO", "potential": "high", "time_to_result": "months"},
                {"channel": "Product Hunt", "potential": "high", "time_to_result": "weeks"},
                {"channel": f"LinkedIn ads ({audience})", "potential": "medium", "time_to_result": "weeks"},
                {"channel": "Content partnerships", "potential": "medium", "time_to_result": "months"},
            ],
            "high": [
                {"channel": "Paid search", "potential": "high", "time_to_result": "days"},
                {"channel": "LinkedIn ads", "potential": "high", "time_to_result": "days"},
                {"channel": "Product Hunt", "potential": "high", "time_to_result": "weeks"},
                {"channel": "Influencer partnerships", "potential": "medium", "time_to_result": "weeks"},
                {"channel": "Webinars & events", "potential": "medium", "time_to_result": "months"},
            ],
        }
        return channels.get(budget, channels["medium"])

    def _cac(self, budget: str) -> Dict[str, float]:
        return {
            "low": {"min": 0.0, "max": 50.0, "unit": "USD"},
            "medium": {"min": 50.0, "max": 200.0, "unit": "USD"},
            "high": {"min": 200.0, "max": 500.0, "unit": "USD"},
        }.get(budget, {"min": 0.0, "max": 100.0, "unit": "USD"})

    def _risks(self, budget: str) -> List[str]:
        if budget == "low":
            return ["Slow ramp", "Requires patience and consistency"]
        if budget == "high":
            return ["High burn risk", "Requires strong conversion tracking"]
        return ["Moderate ramp speed", "Balance organic and paid"]
