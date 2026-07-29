"""Exceptions raised by the Genesis LLM client layer."""


class LLMError(Exception):
    """Base exception for all LLM-related errors."""


class LLMConfigError(LLMError):
    """Raised when the LLM layer is misconfigured or a dependency is missing."""


class LLMProviderError(LLMError):
    """Raised when an LLM provider call fails.

    This wraps native SDK exceptions (network, authentication, rate limit,
    etc.) so the rest of the codebase is not coupled to Anthropic/OpenAI
    specific error types.
    """
