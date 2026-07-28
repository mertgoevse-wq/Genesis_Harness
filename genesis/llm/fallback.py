"""Deterministic offline LLM client.

The fallback client is not a mock: it returns structured, prompt-derived text
so the system remains useful in development, CI, and offline scenarios without
sending data to third parties.
"""

import hashlib
import json
from typing import Any, TypeVar

from genesis.llm.base import StructuredOutput

T = TypeVar("T")


class FallbackClient:
    """Offline LLM client that produces deterministic, prompt-derived output."""

    def complete(self, prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
        """Return a deterministic summary of the prompt."""
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        return (
            f"Fallback completion for prompt (digest {digest}). "
            f"Configure a real LLM provider to receive model-generated output."
        )

    def structured(self, prompt: str, schema: type[T], *, temperature: float | None = None) -> StructuredOutput:
        """Return a default instance of *schema* populated from the prompt hash.

        If the schema is a Pydantic model, ``model_validate`` is used; otherwise
        the result is built from the schema's fields or attributes.
        """
        data = self._synthetic_dict(prompt, schema)
        parsed = self._parse(schema, data)
        raw = json.dumps(data, default=str)
        return StructuredOutput(raw=raw, parsed=parsed)

    @staticmethod
    def _synthetic_dict(prompt: str, schema: type[Any]) -> dict[str, Any]:
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        base: dict[str, Any] = {
            "summary": f"Structured fallback response (digest {digest[:8]}).",
            "confidence": 0.5,
        }

        # If the schema is a Pydantic v2 model, use its field names as keys.
        try:
            fields = getattr(schema, "model_fields", None)
            if fields:
                for name in fields:
                    if name not in base:
                        base[name] = ""
        except Exception:
            pass
        return base

    @staticmethod
    def _parse(schema: type[T], data: dict[str, Any]) -> T:
        if hasattr(schema, "model_validate"):
            return schema.model_validate(data)  # type: ignore[no-any-return]
        return schema(**data)  # type: ignore[operator]
