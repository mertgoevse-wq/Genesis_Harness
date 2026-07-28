"""Anthropic adapter for the Genesis LLM client protocol."""

from typing import Any

from genesis.config import Settings
from genesis.llm.base import StructuredOutput

try:
    import anthropic
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "The Anthropic client is selected but the 'anthropic' package is not installed. "
        "Install it with: pip install anthropic"
    ) from exc


class AnthropicClient:
    """LLM client backed by the Anthropic API."""

    DEFAULT_MODEL = "claude-3-5-sonnet-20240620"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
        self.client = anthropic.Anthropic(
            api_key=self.settings.anthropic_api_key,
            base_url=self.settings.anthropic_base_url or None,
        )
        self.model = self.settings.llm_model or self.DEFAULT_MODEL

    def complete(self, prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
        """Request a plain-text completion from Anthropic."""
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens or self.settings.llm_max_tokens,
            temperature=temperature if temperature is not None else self.settings.llm_temperature,
        )
        content = response.content
        if content and isinstance(content[0], anthropic.types.TextBlock):
            return content[0].text
        return ""

    def structured(self, prompt: str, schema: type[Any], *, temperature: float | None = None) -> StructuredOutput:
        """Return a structured object by asking the model for JSON output."""
        json_prompt = (
            f"{prompt}\n\n"
            "Respond with a single JSON object matching this schema. "
            "Do not include markdown formatting, code fences, or commentary."
        )
        raw = self.complete(json_prompt, temperature=temperature, max_tokens=self.settings.llm_max_tokens)
        import json

        parsed = json.loads(raw)
        if hasattr(schema, "model_validate"):
            return StructuredOutput(raw=raw, parsed=schema.model_validate(parsed))
        return StructuredOutput(raw=raw, parsed=schema(**parsed))
