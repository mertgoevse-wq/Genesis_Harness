import os
from typing import Dict, Any

class ImprovementGenerator:
    def __init__(self, doc_dir: str = "docs/evolution"):
        self.doc_dir = doc_dir
        os.makedirs(self.doc_dir, exist_ok=True)

    def create_report(self, title: str, analysis: dict, experiment: dict) -> str:
        filename = f"EVO_{title.lower().replace(' ', '_')}.md"
        filepath = os.path.join(self.doc_dir, filename)

        content = f"""# Genesis Evolution Report: {title}

**Target Agent:** {analysis.get('agent', 'Global')}
**Baseline Score:** {experiment.get('baseline_score')}
**Optimized Score:** {experiment.get('candidate_score')}
**Improvement:** +{experiment.get('improvement')}

## Pinpointed Weaknesses
{chr(10).join([f"- {w}" for w in analysis.get('weaknesses', [])])}

## Benchmark Experiment Outcome
- Status: **{experiment.get('outcome')}**

## Safety & Governance
> Approval Status: **PENDING REVIEW** (Requires CEO Agent / Human signoff before applying).
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath
