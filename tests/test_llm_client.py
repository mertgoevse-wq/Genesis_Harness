"""Tests for the Genesis LLM client layer."""

from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

from genesis.config import Settings
from genesis.llm import FallbackClient, get_llm_client
from genesis.llm.base import StructuredOutput

if TYPE_CHECKING:
    pass


class _SampleSchema(BaseModel):
    summary: str
    confidence: float


def test_get_llm_client_defaults_to_fallback() -> None:
    client = get_llm_client(Settings(llm_provider="fallback"))
    assert isinstance(client, FallbackClient)


def test_get_llm_client_unknown_provider_falls_back() -> None:
    client = get_llm_client(Settings(llm_provider="unknown"))
    assert isinstance(client, FallbackClient)


def test_get_llm_client_anthropic_without_sdk_raises_import_error() -> None:
    try:
        import anthropic  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError):
            get_llm_client(Settings(anthropic_api_key="fake"), _provider="anthropic")
    else:
        # Anthropic is installed; the factory will succeed with a fake key.
        client = get_llm_client(Settings(anthropic_api_key="fake"), _provider="anthropic")
        assert client is not None


def test_get_llm_client_openai_without_sdk_raises_import_error() -> None:
    try:
        import openai  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError):
            get_llm_client(Settings(openai_api_key="fake"), _provider="openai")
    else:
        client = get_llm_client(Settings(openai_api_key="fake"), _provider="openai")
        assert client is not None


def test_fallback_complete_is_deterministic() -> None:
    client = FallbackClient()
    prompt = "What is the best AI business model?"
    result = client.complete(prompt)
    assert "Fallback completion" in result
    assert prompt not in result  # output is based on the hash, not the raw prompt
    # Same prompt yields the same response.
    assert client.complete(prompt) == result


def test_fallback_structured_parses_schema() -> None:
    client = FallbackClient()
    out = client.structured("Analyze this idea.", _SampleSchema)
    assert isinstance(out, StructuredOutput)
    assert isinstance(out.parsed, _SampleSchema)
    assert out.parsed.summary.startswith("Structured fallback")


def test_settings_loads_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    settings = Settings()
    assert settings.llm_provider == "openai"
    assert settings.openai_api_key == "sk-test-key"


def test_settings_default_provider_is_fallback() -> None:
    settings = Settings()
    assert settings.llm_provider == "fallback"
    assert settings.anthropic_api_key is None
    assert settings.openai_api_key is None
