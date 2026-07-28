from typing import List, Dict, Any

class VectorStore:
    def __init__(self):
        self.index = []

    def add_vector(self, item_id: str, text: str, embedding: List[float] = None):
        self.index.append({"id": item_id, "text": text, "embedding": embedding or [0.1]*10})

    def search_similar(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Simplified similarity ranking
        results = []
        for item in self.index:
            if any(w.lower() in item["text"].lower() for w in query_text.split()):
                results.append(item)
        return results[:top_k]
