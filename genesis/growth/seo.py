"""SEO opportunity detection and content strategy for growth intelligence."""

from typing import Any, Dict, List


class SEOOpportunityEngine:
    """Identifies SEO opportunities and builds a content strategy."""

    def analyze(self, product: str, context: Dict[str, Any]) -> Dict[str, Any]:
        keywords = self._keywords(product, context)
        return {
            "product": product,
            "opportunity_score": self._opportunity_score(keywords, context),
            "keywords": keywords,
            "content_pillars": self._content_pillars(product, context),
            "competitor_gaps": self._competitor_gaps(context),
            "recommended_articles": self._article_ideas(product, context),
        }

    def _keywords(self, product: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        audience = context.get("target_audience", "businesses")
        return [
            {"keyword": f"{product} for {audience}", "volume": "high", "difficulty": "medium"},
            {"keyword": f"best {product} software", "volume": "medium", "difficulty": "high"},
            {"keyword": f"automate {product}", "volume": "low", "difficulty": "low"},
        ]

    def _opportunity_score(self, keywords: List[Dict[str, Any]], context: Dict[str, Any]) -> float:
        base = 60.0
        if context.get("keyword_research_done"):
            base += 15.0
        if context.get("blog_active"):
            base += 10.0
        return min(base, 100.0)

    def _content_pillars(self, product: str, context: Dict[str, Any]) -> List[str]:
        return [
            f"How to automate {product}",
            f"{product} best practices",
            f"{product} tools comparison",
        ]

    def _competitor_gaps(self, context: Dict[str, Any]) -> List[str]:
        return [
            "No authoritative guide exists for mid-market buyers",
            "Competitors lack video content",
            "Long-tail keyword coverage is weak",
        ]

    def _article_ideas(self, product: str, context: Dict[str, Any]) -> List[str]:
        audience = context.get("target_audience", "businesses")
        return [
            f"The complete guide to {product} for {audience}",
            f"10 ways to automate {product} in 2026",
            f"{product} vs. competitors: a detailed comparison",
        ]
