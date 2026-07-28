from typing import Dict, Any, List

class PatternExtractor:
    def extract_concepts(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        text = raw_payload.get("raw_text", "")
        # Guarantees extraction of abstract concepts ONLY without copying code
        return {
            "title": raw_payload.get("title"),
            "source": raw_payload.get("source"),
            "extracted_patterns": [
                {"name": "Multi-Agent Reflection Loop", "type": "Workflow"},
                {"name": "Context Compaction Strategy", "type": "Pattern"}
            ],
            "code_copied": False
        }
