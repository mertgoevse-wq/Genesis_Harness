class ArxivConnector:
    def fetch_latest(self, topic: str): return [{"title": f"Latest on {topic}", "source": "arXiv"}]
