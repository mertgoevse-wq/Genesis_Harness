import os
from .base import LLMProvider

class OllamaProvider(LLMProvider):
    name = "ollama"
    
    def _is_mock(self):
        # We could check if ollama process is running, but let's mock it for now
        return not bool(os.getenv("OLLAMA_HOST"))
    
    def generate(self, prompt: str, **kwargs) -> str:
        return f"[Ollama Mock] Generate: {prompt[:30]}..." if self._is_mock() else "API Calls not yet implemented"
        
    def chat(self, messages: list) -> str:
        return "[Ollama Mock] Chat Response" if self._is_mock() else "API Calls not yet implemented"
        
    def analyze(self, context: str) -> str:
        return "[Ollama Mock] Analysis Complete" if self._is_mock() else "API Calls not yet implemented"
        
    def plan(self, goal: str, context: str) -> str:
        return "[Ollama Mock] Plan." if self._is_mock() else "API Calls not yet implemented"
        
    def generate_code(self, instructions: str, files: dict) -> str:
        return "[Ollama Mock] # Generated Code" if self._is_mock() else "API Calls not yet implemented"
        
    def review_code(self, diff: str) -> str:
        return "[Ollama Mock] Review Passed." if self._is_mock() else "API Calls not yet implemented"
