# ADR-0002: Provider-Agnostic LLM Client Layer

**Status:** Accepted
**Date:** 2026-07-28
**Author:** Genesis AI Session

---

## Context

Phase 1 consolidated the Genesis Harness runtime into a single `genesis/`
Python package. The system still operated entirely on deterministic heuristics;
there was no way to call a large language model. Phase 2 requires intelligent,
prompt-specific reasoning while remaining testable and deployable.

The project constitution forbids duplicating existing work and requires that
external integrations use proper interfaces, dependency injection, and
configuration without hardcoded secrets.

## Decision

Introduce a small `genesis/llm/` package that defines a provider-agnostic
protocol and ships concrete adapters for Anthropic, OpenAI, and an offline
fallback.

```
genesis/llm/
├── base.py            # LLMClient protocol + StructuredOutput
├── fallback.py       # deterministic offline client
├── anthropic_client.py # Anthropic SDK adapter
├── openai_client.py   # OpenAI SDK adapter
└── client.py         # factory driven by Settings
```

Key design points:

1. **Protocol-first.** Business modules depend on `LLMClient`, not on any SDK.
2. **Configuration via environment.** API keys and provider are loaded through
   `genesis.config.Settings` (`pydantic-settings`). No secrets are in source.
3. **Offline fallback by default.** The system works out of the box without API
   keys; real providers are opt-in.
4. **Lazy provider loading.** Anthropic and OpenAI SDKs are imported only when
   selected, so the core package does not require them.
5. **Structured output support.** The protocol returns both raw text and parsed
   structured objects.

## Consequences

- **Positive:** Tests run offline; real reasoning is one configuration change
  away; the codebase is not coupled to a single LLM vendor.
- **Positive:** Adding a new provider only requires a new module implementing
  the protocol.
- **Negative:** The LLM client is currently unused by the orchestrator. The next
  step is to wire it into `decision/engine.py` and `builder/mvp.py`.
- **Neutral:** SDKs remain optional extras in `pyproject.toml`
  (`pip install -e ".[llm]"`).

## Alternatives Considered

- **Vendor-specific SDK only.** Rejected because it couples the runtime to a
  single provider and makes testing harder.
- **Vendored third-party code.** Rejected by the constitution; we import official
  SDKs or use the fallback.
- **LangChain/LlamaIndex wrapper.** Rejected as overkill at this stage; the
  protocol can be replaced later without touching business modules.
