import os
from .base import LLMProvider

class ClaudeProvider(LLMProvider):
    name = "claude"
    
    def _is_mock(self):
        return not bool(os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, prompt: str, **kwargs) -> str:
        return f"[Claude Mock] Generate: {prompt[:30]}..." if self._is_mock() else "API Calls not yet implemented"
        
    def chat(self, messages: list) -> str:
        return "[Claude Mock] Chat Response" if self._is_mock() else "API Calls not yet implemented"
        
    def analyze(self, context: str) -> str:
        return "[Claude Mock] Analysis Complete" if self._is_mock() else "API Calls not yet implemented"
        
    def plan(self, goal: str, context: str) -> str:
        return "[Claude Mock] Plan: Refactor avatar pipeline and update frontend." if self._is_mock() else "API Calls not yet implemented"
        
    def generate_code(self, instructions: str, files: dict) -> str:
        return "[Claude Mock] # New Avatar Animation Code Generated" if self._is_mock() else "API Calls not yet implemented"
        
    def review_code(self, diff: str) -> str:
        return "[Claude Mock] Review: Code looks good, LGTM!" if self._is_mock() else "API Calls not yet implemented"
