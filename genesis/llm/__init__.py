"""Genesis LLM client layer.

Provides a small, provider-agnostic interface over large language models.
The default implementation is a deterministic offline fallback so the system
remains testable and runnable without API keys. Real providers (Anthropic,
OpenAI) are loaded on demand when configured and available.
"""

from genesis.llm.base import LLMClient, StructuredOutput
from genesis.llm.client import get_llm_client
from genesis.llm.fallback import FallbackClient

__all__ = [
    "LLMClient",
    "FallbackClient",
    "get_llm_client",
    "StructuredOutput",
]
