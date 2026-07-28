from memory_system.storage.vector_store import VectorStore

class SemanticSearch:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def query(self, search_term: str) -> list:
        return self.vector_store.search_similar(search_term)
