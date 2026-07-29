"""OpenAI adapter for the Genesis LLM client protocol."""

import json
from typing import Any

from genesis.config import Settings
from genesis.llm.base import StructuredOutput
from genesis.llm.errors import LLMConfigError, LLMProviderError

try:
    import openai
except ImportError as exc:  # pragma: no cover - optional dependency
    raise LLMConfigError(
        "The OpenAI client is selected but the 'openai' package is not installed. "
        "Install it with: pip install openai"
    ) from exc


class OpenAIClient:
    """LLM client backed by the OpenAI-compatible API."""

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.openai_api_key:
            raise LLMConfigError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        self.client = openai.OpenAI(
            api_key=self.settings.openai_api_key.get_secret_value(),
            base_url=self.settings.openai_base_url or None,
            max_retries=self.settings.llm_max_retries,
            timeout=self.settings.llm_timeout,
        )
        self.model = self.settings.llm_model or self.DEFAULT_MODEL

    def complete(self, prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
        """Request a plain-text completion from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.settings.llm_max_tokens,
                temperature=temperature if temperature is not None else self.settings.llm_temperature,
            )
        except Exception as exc:
            raise LLMProviderError(f"OpenAI request failed: {exc}") from exc
        content = response.choices[0].message.content
        return content or ""

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
            raise LLMProviderError(f"OpenAI response was not valid JSON: {exc}") from exc
        validated = schema.model_validate(parsed) if hasattr(schema, "model_validate") else schema(**parsed)
        return StructuredOutput(raw=raw, parsed=validated)
