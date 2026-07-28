"""Factory for the configured Genesis LLM client."""

import os
from typing import TYPE_CHECKING

from genesis.config import Settings
from genesis.llm.base import LLMClient
from genesis.llm.fallback import FallbackClient

if TYPE_CHECKING:
    pass  # concrete clients are imported lazily below


def get_llm_client(settings: Settings | None = None, *, _provider: str | None = None) -> LLMClient:
    """Return an concrete LLM client based on configuration.

    The provider is resolved in this order:
        1. The ``_provider`` override (useful for tests).
        2. The ``LLM_PROVIDER`` setting.
        3. The ``LLM_PROVIDER`` environment variable.
        4. The offline ``FallbackClient``.

    API keys are read from the environment or ``.env`` via ``Settings``. No
    key is hard-coded. If a provider is configured but its SDK is missing, an
    ``ImportError`` is raised so the operator knows to install the extra.
    """
    settings = settings or Settings()
    provider = _provider or settings.llm_provider or os.getenv("LLM_PROVIDER", "fallback")
    provider = provider.lower()

    if provider == "anthropic":
        from genesis.llm.anthropic_client import AnthropicClient

        return AnthropicClient(settings)

    if provider == "openai":
        from genesis.llm.openai_client import OpenAIClient

        return OpenAIClient(settings)

    return FallbackClient()
