"""Anthropic adapter for the Genesis LLM client protocol."""

import json
from typing import Any

from genesis.config import Settings
from genesis.llm.base import StructuredOutput
from genesis.llm.errors import LLMConfigError, LLMProviderError

try:
    import anthropic
except ImportError as exc:  # pragma: no cover - optional dependency
    raise LLMConfigError(
        "The Anthropic client is selected but the 'anthropic' package is not installed. "
        "Install it with: pip install anthropic"
    ) from exc


class AnthropicClient:
    """LLM client backed by the Anthropic API."""

    DEFAULT_MODEL = "claude-3-5-sonnet-20240620"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.anthropic_api_key:
            raise LLMConfigError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
        self.client = anthropic.Anthropic(
            api_key=self.settings.anthropic_api_key.get_secret_value(),
            base_url=self.settings.anthropic_base_url or None,
            max_retries=self.settings.llm_max_retries,
            timeout=self.settings.llm_timeout,
        )
        self.model = self.settings.llm_model or self.DEFAULT_MODEL

    def complete(self, prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
        """Request a plain-text completion from Anthropic."""
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.settings.llm_max_tokens,
                temperature=temperature if temperature is not None else self.settings.llm_temperature,
            )
        except Exception as exc:
            raise LLMProviderError(f"Anthropic request failed: {exc}") from exc
        content = response.content
        if content and isinstance(content[0], anthropic.types.TextBlock):
            return content[0].text
        return ""

    def structured(self, prompt: str, schema: type[Any], *, temperature: float | None = None) -> StructuredOutput:
        """Return a structured object by asking the model for JSON output."""
        schema_json = json.dumps(getattr(schema, "model_json_schema", lambda: {})())
        json_prompt = (
            f"{prompt}\n\n"
            f"Respond with a single JSON object matching this schema: {schema_json}. "
            "Do not include markdown formatting, code fences, or commentary."
        )
        raw = self.complete(json_prompt, temperature=temperature, max_tokens=self.settings.llm_max_tokens)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMProviderError(f"Anthropic response was not valid JSON: {exc}") from exc
        validated = schema.model_validate(parsed) if hasattr(schema, "model_validate") else schema(**parsed)
        return StructuredOutput(raw=raw, parsed=validated)
