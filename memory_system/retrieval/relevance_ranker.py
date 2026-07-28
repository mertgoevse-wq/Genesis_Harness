class RelevanceRanker:
    def rank(self, results: list) -> list:
        return sorted(results, key=lambda x: len(x.get("text", "")), reverse=True)
