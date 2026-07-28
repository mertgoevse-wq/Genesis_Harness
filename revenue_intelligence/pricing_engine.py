"""Pricing engine for revenue optimization."""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class PricingTier:
    name: str
    monthly_price: float
    features: List[str] = field(default_factory=list)
    target_segment: str = ""


class PricingEngine:
    """Recommends pricing tiers based on product context."""

    def recommend(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return recommended pricing strategy."""
        tiers = self._build_tiers(context)
        return {
            "model": "tiered_saas",
            "tiers": tiers,
            "recommended_tier": tiers[1].name if len(tiers) > 1 else tiers[0].name,
            "confidence": "ASSUMED",
        }

    def _build_tiers(self, context: Dict[str, Any]) -> List[PricingTier]:
        base = context.get("base_price", 9.0)
        return [
            PricingTier(
                name="Starter",
                monthly_price=round(base, 2),
                features=["Core features", "Email support"],
                target_segment="Individuals & small teams",
            ),
            PricingTier(
                name="Growth",
                monthly_price=round(base * 3, 2),
                features=["Advanced features", "Priority support", "Analytics"],
                target_segment="Growing teams",
            ),
            PricingTier(
                name="Enterprise",
                monthly_price=round(base * 9, 2),
                features=["Custom features", "SLA", "Dedicated support"],
                target_segment="Large organizations",
            ),
        ]
