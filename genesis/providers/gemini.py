import os
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    name = "gemini"
    
    def _is_mock(self):
        return os.getenv("GENESIS_LIVE_API", "false").lower() != "true"
    
    def generate(self, prompt: str, **kwargs) -> str:
        return f"[Gemini Mock] Generate: {prompt[:30]}..." if self._is_mock() else "API Calls not yet implemented"
        
    def chat(self, messages: list) -> str:
        return "[Gemini Mock] Chat Response" if self._is_mock() else "API Calls not yet implemented"
        
    def analyze(self, context: str) -> str:
        return "[Gemini Mock] Analysis Complete" if self._is_mock() else "API Calls not yet implemented"
        
    def plan(self, goal: str, context: str) -> str:
        return "[Gemini Mock] Plan: Implement new component." if self._is_mock() else "API Calls not yet implemented"
        
    def generate_code(self, instructions: str, files: dict) -> str:
        return "[Gemini Mock] # Generated Code" if self._is_mock() else "API Calls not yet implemented"
        
    def review_code(self, diff: str) -> str:
        return "[Gemini Mock] Review: Missing tests." if self._is_mock() else "API Calls not yet implemented"
