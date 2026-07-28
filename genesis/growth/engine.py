"""Growth intelligence engine for landing pages, SEO, and acquisition."""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class GrowthStrategy:
    product: str
    landing_page_score: float
    seo_score: float
    acquisition_channels: List[str]
    experiments: List[str]
    recommendations: List[str]


class GrowthEngine:
    """Generates growth and customer acquisition strategy for a SaaS product."""

    def recommend(self, product: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return a growth strategy for the given product."""
        target_audience = context.get("target_audience", "small businesses")
        budget = context.get("marketing_budget", "medium")
        channel_count = context.get("available_channels", 3)

        landing_page_score = self._landing_page_score(context)
        seo_score = self._seo_score(context)
        channels = self._channels(target_audience, budget)
        experiments = self._experiments(product, target_audience)
        recommendations = self._recommendations(
            landing_page_score, seo_score, budget, channel_count
        )

        return {
            "product": product,
            "target_audience": target_audience,
            "landing_page": {
                "score": landing_page_score,
                "headline": f"{product} — automate your workflow",
                "cta": "Start free trial",
                "social_proof": ["Trusted by 500+ teams", "No credit card required"],
            },
            "seo": {
                "score": seo_score,
                "keywords": self._keywords(product, target_audience),
                "content_pillars": [
                    f"How to automate {product}",
                    f"Best {product} tools for {target_audience}",
                ],
            },
            "acquisition_channels": channels,
            "experiments": experiments,
            "recommendations": recommendations,
        }

    def _landing_page_score(self, context: Dict[str, Any]) -> float:
        base = 70.0
        if context.get("has_testimonials"):
            base += 10.0
        if context.get("has_demo_video"):
            base += 10.0
        return min(base, 100.0)

    def _seo_score(self, context: Dict[str, Any]) -> float:
        base = 65.0
        if context.get("keyword_research_done"):
            base += 15.0
        if context.get("blog_active"):
            base += 10.0
        return min(base, 100.0)

    def _channels(self, target_audience: str, budget: str) -> List[str]:
        channels = {
            "low": [
                "Organic content marketing",
                "Community engagement (Reddit, IndieHackers)",
                "SEO long-tail keywords",
            ],
            "medium": [
                "Organic content marketing",
                "SEO + content clusters",
                "Product Hunt launch",
                "LinkedIn ads for " + target_audience,
            ],
            "high": [
                "Paid search (Google Ads)",
                "LinkedIn ads",
                "Product Hunt launch",
                "Influencer partnerships",
                "Webinars & events",
            ],
        }
        return channels.get(budget, channels["medium"])

    def _experiments(self, product: str, target_audience: str) -> List[str]:
        return [
            f"A/B test headline on {product} landing page",
            f"Run a 7-day LinkedIn campaign targeting {target_audience}",
            "Launch on Product Hunt with a dedicated landing page",
            f"Create a comparison page: {product} vs. competitors",
        ]

    def _keywords(self, product: str, target_audience: str) -> List[str]:
        return [
            f"{product} for {target_audience}",
            f"best {product} software",
            f"{product} tool",
            f"automate {product}",
        ]

    def _recommendations(
        self,
        landing_page_score: float,
        seo_score: float,
        budget: str,
        channel_count: int,
    ) -> List[str]:
        recs = []
        if landing_page_score < 80.0:
            recs.append("Add testimonials and a demo video to the landing page.")
        if seo_score < 80.0:
            recs.append("Invest in keyword research and publish 2 pillar posts monthly.")
        if budget == "low":
            recs.append("Focus on organic channels and SEO before paid ads.")
        if channel_count < 3:
            recs.append("Diversify acquisition channels to reduce dependency.")
        if not recs:
            recs.append("Scale winning channels and double down on conversion optimization.")
        return recs
