class LLMProvider:
    """Base Interface for all LLM backends."""
    name = "base_llm"
    
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError()
        
    def chat(self, messages: list) -> str:
        raise NotImplementedError()
        
    def analyze(self, context: str) -> str:
        raise NotImplementedError()
        
    def plan(self, goal: str, context: str) -> str:
        raise NotImplementedError()
        
    def generate_code(self, instructions: str, files: dict) -> str:
        raise NotImplementedError()
        
    def review_code(self, diff: str) -> str:
        raise NotImplementedError()
