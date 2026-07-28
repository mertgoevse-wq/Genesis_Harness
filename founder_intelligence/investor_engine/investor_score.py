import os

class InvestorEngine:
    def evaluate_and_pitch(self, idea_title: str, score: float, output_dir: str = "docs/investment_reviews") -> str:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"review_{idea_title.lower().replace(' ', '_')}.md")
        content = f"""# VC Investment Review: {idea_title}

**Simulated VC Score:** {score}/100
**Recommendation:** CONDITIONAL TERM SHEET ISSUED

## Evaluation Breakdown
- Market Opportunity: 9/10
- AI Moat: 9/10
- Founder/Agent Fit: 9/10
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
