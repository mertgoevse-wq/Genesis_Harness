import json
import os
from typing import Any, Dict, List


class KnowledgeStore:
    def __init__(self, db_path: str = "memory_system/storage/knowledge_db.json"):
        self.db_path = db_path
        self.records: List[Dict[str, Any]] = self._load()

    def _load(self) -> list:
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_record(self, category: str, data: dict):
        record = {
            "id": len(self.records) + 1,
            "category": category,
            "data": data
        }
        self.records.append(record)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
        return record
