import os

class PRDGenerator:
    def __init__(self, output_dir: str = "docs/products"):
        self.output_dir = output_dir

    def generate_prd_package(self, product_name: str, details: dict) -> str:
        slug = product_name.lower().replace(" ", "_")
        target_dir = os.path.join(self.output_dir, slug)
        os.makedirs(target_dir, exist_ok=True)

        files = {
            "README.md": f"# {product_name}\n\n{details.get('summary', 'Autonomous AI Product')}",
            "PRD.md": f"# Product Requirement Document: {product_name}\n\n## Target Audience\n{details.get('audience', 'Global Developers')}\n\n## Core Features\n- AI Automation Engine",
            "Technical_Architecture.md": f"# Technical Architecture: {product_name}\n\n- Stack: Genesis Runtime, FastHTML, Supabase",
            "Business_Model.md": f"# Business Model: {product_name}\n\n- Pricing: SaaS Freemium ($29/mo)",
            "Launch_Plan.md": f"# Launch Plan: {product_name}\n\n- Channels: ProductHunt, HackerNews, X",
            "Risk_Analysis.md": f"# Risk Analysis: {product_name}\n\n- Low technical risk, high market demand",
            "Implementation_Roadmap.md": f"# Implementation Roadmap: {product_name}\n\n- Phase 1: MVP (Week 1)\n- Phase 2: Launch (Week 2)"
        }

        for fname, content in files.items():
            with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        return target_dir
