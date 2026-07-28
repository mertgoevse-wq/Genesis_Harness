"""Subscription model selection for revenue intelligence."""

from typing import Any, Dict


class SubscriptionModelSelector:
    """Selects subscription and billing models for a product."""

    MODELS = [
        {
            "name": "flat_rate",
            "description": "Single price for all features.",
            "best_for": "Simple products with one persona.",
        },
        {
            "name": "tiered",
            "description": "Multiple plans with increasing features.",
            "best_for": "Products with diverse user segments.",
        },
        {
            "name": "usage_based",
            "description": "Billing scales with consumption.",
            "best_for": "APIs and infrastructure products.",
        },
        {
            "name": "freemium",
            "description": "Free tier with paid upgrades.",
            "best_for": "Acquisition-heavy products.",
        },
    ]

    def recommend(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return recommended subscription model."""
        product_type = context.get("product_type", "saas")
        if product_type == "api":
            model = self.MODELS[2]
        elif context.get("acquisition_heavy"):
            model = self.MODELS[3]
        else:
            model = self.MODELS[1]

        return {
            "recommended_model": model["name"],
            "description": model["description"],
            "best_for": model["best_for"],
            "alternatives": [m["name"] for m in self.MODELS if m != model],
        }
