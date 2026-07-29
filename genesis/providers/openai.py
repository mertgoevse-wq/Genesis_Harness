import os
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    name = "openai"
    
    def _is_mock(self):
        return not bool(os.getenv("OPENAI_API_KEY"))
    
    def generate(self, prompt: str, **kwargs) -> str:
        return f"[OpenAI Mock] Generate: {prompt[:30]}..." if self._is_mock() else "API Calls not yet implemented"
        
    def chat(self, messages: list) -> str:
        return "[OpenAI Mock] Chat Response" if self._is_mock() else "API Calls not yet implemented"
        
    def analyze(self, context: str) -> str:
        return "[OpenAI Mock] Analysis Complete" if self._is_mock() else "API Calls not yet implemented"
        
    def plan(self, goal: str, context: str) -> str:
        return "[OpenAI Mock] Plan." if self._is_mock() else "API Calls not yet implemented"
        
    def generate_code(self, instructions: str, files: dict) -> str:
        return "[OpenAI Mock] # Generated Code" if self._is_mock() else "API Calls not yet implemented"
        
    def review_code(self, diff: str) -> str:
        return "[OpenAI Mock] Review Passed." if self._is_mock() else "API Calls not yet implemented"
