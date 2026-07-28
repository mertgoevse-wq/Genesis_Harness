# Genesis Harness 🚀

[![Python](https://img.shields.io/badge/Python-3.10%2B-cyan.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Genesis Harness** is an autonomous AI Operating System for venture creation:
> a consolidated Python package that discovers opportunities, scores venture
> ideas, recommends revenue and growth strategies, and builds MVP artefacts.

---

## 🌟 Key Features

- 🤖 **Opportunity Intelligence**: Detect market opportunities, trends, and
  competitor gaps.
- 🧠 **LLM Client Layer**: Provider-agnostic wrapper for Anthropic, OpenAI, and an
  offline fallback. No hardcoded secrets.
- 📊 **Venture Decision Engine**: Weighted scoring across market, competition,
  technical, and risk dimensions.
- ✅ **Product Validation Engine**: GO / MODIFY / REJECT verdicts with
  confidence scores.
- 💰 **Revenue Intelligence**: Pricing tiers, subscription models, acquisition
  channels, and growth experiments.
- 📈 **Growth Intelligence**: Landing-page and SEO recommendations, channel
  analysis, and growth loops.
- 🛠️ **MVP Builder**: Generates FastAPI/SQLAlchemy/Pydantic scaffolds with
  Docker and deployment artefacts.
- 🧠 **Founder Memory**: Persists decisions and learns from successful and
  failed ideas.
- 🔄 **Self-Improvement Loop**: Detects weaknesses and prioritizes improvement
  tasks.

---

## 🏛️ Architecture

The runtime is packaged as a single installable `genesis/` Python package.

```
genesis/
├── __main__.py         # CLI entry point
├── orchestrator.py     # MasterGenesisOrchestrator
├── config.py           # Central settings (Pydantic BaseSettings)
├── llm/                # Provider-agnostic LLM client layer
├── decision/           # Venture + product validation
├── intelligence/       # Opportunity detection + live connectors
├── revenue/            # Pricing, subscriptions, acquisition, experiments
├── growth/             # Growth, SEO, customer intelligence, validation loop
├── builder/            # MVP builder + deployment planner
├── memory/             # Founder memory + knowledge store
├── improvement/        # Self-improvement loop
├── api/                # API surface (Phase 2)
└── core/               # Shared core utilities
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design and
[`docs/ROADMAP.md`](docs/ROADMAP.md) for the current phase.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/mertgoevse-wq/Genesis_Harness.git
cd Genesis_Harness
pip install -e ".[dev]"
```

### Run an analysis

```bash
python -m genesis analyze "AI Customer Support SaaS"
```

### Configure an LLM provider (optional)

Copy the example environment file and add your API key if you want real
LLM-backed reasoning instead of the deterministic offline fallback:

```bash
cp .env.example .env
# edit .env with your provider and API key
```

Supported providers:

| Provider | Environment variable |
|---|---|
| `fallback` (default, offline) | none |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `openai` | `OPENAI_API_KEY` |

### Run tests

```bash
pytest tests/ -v
```

### Run the structure verification gate

```powershell
pwsh -File scripts/verify_structure.ps1
```

---

## 🧪 Development

- Python >= 3.10 is required.
- Code is formatted and linted with `ruff`.
- Tests use `pytest`.
- The repository follows the Genesis Constitution in `CLAUDE.md`.

---

## ️ Roadmap

Current phase: **Phase 2 — LLM Core & API** (in progress).

- [x] Consolidate 60+ directories into the `genesis/` Python package.
- [x] Add `pyproject.toml`, CLI entry point, and test suite.
- [x] Add a provider-agnostic LLM client layer with offline fallback.
- [ ] Phase 2 — LLM-backed analysis and FastAPI service.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for details.

---

##  Contributing

Please review our [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
and run `pwsh -File scripts/verify_structure.ps1` before submitting pull requests.

---

## 📄 License

Distributed under the MIT License.
