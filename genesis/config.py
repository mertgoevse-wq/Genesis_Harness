"""Central configuration for the Genesis package.

Settings are loaded from environment variables or a ``.env`` file. No secrets are
hard-coded; anything missing simply falls back to safe defaults (e.g. the LLM
layer defaults to a deterministic offline client).
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from the environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # LLM provider configuration. The default is the offline fallback, which
    # keeps the system runnable without API keys and makes tests deterministic.
    llm_provider: str = Field(default="fallback", alias="LLM_PROVIDER")
    llm_model: str | None = Field(default=None, alias="LLM_MODEL")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_base_url: str | None = Field(default=None, alias="ANTHROPIC_BASE_URL")
    openai_base_url: str | None = Field(default=None, alias="OPENAI_BASE_URL")

    # Conservative request limits.
    llm_max_tokens: int = Field(default=1024, alias="LLM_MAX_TOKENS")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")


# Singleton exposed for import convenience. Consumers can also instantiate
# ``Settings()`` themselves when they need isolated configuration.
settings = Settings()
