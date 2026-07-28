"""Customer acquisition strategy generator."""

from typing import Any, Dict


class AcquisitionStrategy:
    """Recommends channels and tactics for acquiring customers."""

    CHANNELS = [
        {
            "channel": "content_marketing",
            "tactic": "Publish SEO-optimized guides and tutorials.",
            "expected_cac": "low",
        },
        {
            "channel": "product_hunt",
            "tactic": "Launch on Product Hunt with a compelling demo.",
            "expected_cac": "low",
        },
        {
            "channel": "paid_search",
            "tactic": "Run Google Ads for high-intent keywords.",
            "expected_cac": "medium",
        },
        {
            "channel": "cold_outreach",
            "tactic": "Targeted email/LinkedIn outreach to ideal personas.",
            "expected_cac": "high",
        },
    ]

    def recommend(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return an acquisition strategy."""
        budget = context.get("budget", "medium")
        if budget == "low":
            chosen = [c for c in self.CHANNELS if c["expected_cac"] == "low"]
        else:
            chosen = self.CHANNELS[:3]

        return {
            "primary_channels": [c["channel"] for c in chosen],
            "tactics": [c["tactic"] for c in chosen],
            "budget": budget,
        }
