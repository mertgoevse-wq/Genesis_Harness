"""Factory for the configured Genesis LLM client."""

import os
from typing import TYPE_CHECKING

from genesis.config import Settings
from genesis.llm.base import LLMClient
from genesis.llm.fallback import FallbackClient

if TYPE_CHECKING:
    pass  # concrete clients are imported lazily below

# Module-level cache so a single process reuses the same LLM client. Tests can
# call ``clear_llm_client_cache()`` to avoid state leaking between cases.
_client_cache: LLMClient | None = None


def clear_llm_client_cache() -> None:
    """Clear the globally cached LLM client instance."""
    global _client_cache  # noqa: PLW0603 - cache mutation is intentional
    _client_cache = None


def get_llm_client(settings: Settings | None = None, *, _provider: str | None = None) -> LLMClient:
    """Return a concrete LLM client based on configuration.

    The provider is resolved in this order:
        1. The ``_provider`` override (useful for tests).
        2. The ``LLM_PROVIDER`` setting.
        3. The ``LLM_PROVIDER`` environment variable.
        4. The offline ``FallbackClient``.

    API keys are read from the environment or ``.env`` via ``Settings``. No
    key is hard-coded. If a provider is configured but its SDK is missing, a
    ``LLMConfigError`` is raised so the operator knows to install the extra.

    The default ``_provider=None`` path caches the resulting client so the same
    process can reuse SDK connections. Call ``clear_llm_client_cache()`` to
    reset it.
    """
    global _client_cache  # noqa: PLW0603 - cache mutation is intentional

    if settings is None and _provider is None and _client_cache is not None:
        return _client_cache

    settings = settings or Settings()
    provider = _provider or settings.llm_provider or os.getenv("LLM_PROVIDER", "fallback")
    provider = provider.lower()

    if provider == "anthropic":
        from genesis.llm.anthropic_client import AnthropicClient

        return AnthropicClient(settings)

    if provider == "openai":
        from genesis.llm.openai_client import OpenAIClient

        return OpenAIClient(settings)

    client: LLMClient = FallbackClient()
    if settings is not None and _provider is None:
        _client_cache = client
    return client
