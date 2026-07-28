"""Base protocol for Genesis LLM clients."""

from typing import Any, Protocol, TypeVar


class StructuredOutput:
    """Lightweight wrapper for structured LLM output.

    The wrapper keeps the raw text alongside the parsed object so callers can
    audit the underlying response.
    """

    def __init__(self, raw: str, parsed: Any) -> None:
        self.raw = raw
        self.parsed = parsed

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(raw_len={len(self.raw)}, parsed={type(self.parsed).__name__})"


T = TypeVar("T")


class LLMClient(Protocol):
    """Provider-agnostic interface for text completion.

    Implementations may wrap the Anthropic SDK, the OpenAI SDK, an on-premise
    model, or a deterministic fallback. The protocol keeps the rest of the
    codebase decoupled from any particular provider.
    """

    def complete(self, prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
        """Return a plain-text completion for *prompt*."""
        ...

    def structured(self, prompt: str, schema: type[T], *, temperature: float | None = None) -> StructuredOutput:
        """Return a structured object parsed into *schema* from the LLM response.

        The default behaviour is a best-effort JSON parse. Concrete clients may
        override this to use provider-native structured-output features.
        """
        ...
