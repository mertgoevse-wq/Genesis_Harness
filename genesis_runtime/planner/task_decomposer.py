from typing import List, Dict, Any

class TaskDecomposer:
    def decompose(self, goal: str) -> List[Dict[str, Any]]:
        # High level goal decomposition
        return [
            {"agent": "market-research", "objective": "Market Analysis"},
            {"agent": "product-manager", "objective": "Product Requirements Document (PRD)"},
            {"agent": "architect", "objective": "System Design"},
            {"agent": "coding", "objective": "Core Feature Implementation"},
            {"agent": "qa", "objective": "Testing Suite Verification"},
            {"agent": "growth", "objective": "Go-to-Market Strategy"}
        ]
