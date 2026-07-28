import os

repo_root = "c:\\Genesis_Harness"

# Directories to ensure
dirs = [
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "branding",
    "docs"
]
for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)

# 1. .github/workflows/ci.yml
ci_yml = '''name: Genesis Harness CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PowerShell
        uses: powershell/action-ps-build@v1.1
        
      - name: Run Structure Verification Gate
        shell: pwsh
        run: ./scripts/verify_structure.ps1
'''
with open(os.path.join(repo_root, ".github", "workflows", "ci.yml"), "w", encoding="utf-8") as f:
    f.write(ci_yml)

# 2. .github/workflows/release.yml
release_yml = '''name: Release & Changelog Automation

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Release Notes
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
'''
with open(os.path.join(repo_root, ".github", "workflows", "release.yml"), "w", encoding="utf-8") as f:
    f.write(release_yml)

# 3. .github/ISSUE_TEMPLATE/bug_report.md
bug_report = '''---
name: Bug Report
about: Create a report to help us improve Genesis Harness
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Description
A clear and concise description of what the bug is.

## System Context
- Genesis Harness Version:
- Operating System:
- Active Agents:

## Steps to Reproduce
1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior
A clear description of what you expected to happen.
'''
with open(os.path.join(repo_root, ".github", "ISSUE_TEMPLATE", "bug_report.md"), "w", encoding="utf-8") as f:
    f.write(bug_report)

# 4. .github/ISSUE_TEMPLATE/feature_request.md
feature_request = '''---
name: Feature / Agent Request
about: Suggest an idea, agent, or skill for Genesis Harness
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## Feature / Agent / Skill Concept
Describe the proposed addition to Genesis Harness.

## Business / Architectural Rationale
Why is this feature valuable? Which agent role or skill tier does it enhance?

## Proposed Implementation Details
Include any potential charters, adapters, or pipeline workflows.
'''
with open(os.path.join(repo_root, ".github", "ISSUE_TEMPLATE", "feature_request.md"), "w", encoding="utf-8") as f:
    f.write(feature_request)

# 5. .github/PULL_REQUEST_TEMPLATE.md
pr_template = '''# Pull Request

## Summary
Brief description of the changes introduced by this PR.

## Checklist
- [ ] Ran `verify_structure.ps1` and passed all structural gates.
- [ ] Updated `docs/ARCHITECTURE.md` or `docs/ROADMAP.md` if applicable.
- [ ] Included or updated relevant session logs under `logs/sessions/`.
- [ ] Ensured no copyrighted implementation code was added.
'''
with open(os.path.join(repo_root, ".github", "PULL_REQUEST_TEMPLATE.md"), "w", encoding="utf-8") as f:
    f.write(pr_template)

# 6. branding/IDENTITY.md
branding_md = '''# Genesis Harness - Visual & Brand Identity

## Vision & Philosophy
Genesis Harness is an autonomous AI Operating System designed for multi-agent engineering, research automation, and continuous ecosystem evolution. The brand reflects precision, high-tech intelligence, and autonomous modularity.

## Color System
- **Deep Space Black (`#0B0F19`)**: Primary background representing depth and security.
- **Electric Cyan (`#00F2FE`)**: Primary accent representing intelligence, energy, and execution.
- **Nebula Purple (`#4FACFE`)**: Secondary gradient accent representing orchestration and intelligence.
- **Cyber Gray (`#1E293B`)**: Card & container background.

## Logo Concept
A stylized abstract monogram representing interlocked neural autonomous nodes forming an uppercase 'G'.

```
    .---.      .---.
   /     \    /     \
  |  (G)  |--|  (H)  |
   \     /    \     /
    '---'      '---'
```

## Banner Concept
Dark background with electric cyan nodes interconnected via glowing DAG edges, featuring the headline: **"GENESIS HARNESS - Autonomous AI Operating System"**.
'''
with open(os.path.join(repo_root, "branding", "IDENTITY.md"), "w", encoding="utf-8") as f:
    f.write(branding_md)

# 7. docs/github_profile.md
github_profile = '''# Genesis Harness - GitHub Metadata & Profile

## Repository Description
"Genesis Harness is an autonomous AI Operating System for multi-agent engineering, research automation, business intelligence and continuous AI ecosystem evolution."

## Short Description (1-Liner)
"Autonomous AI Operating System for Multi-Agent Orchestration & Intelligence Harvesting."

## Recommended GitHub Topics / Tags
`ai-agents`, `multi-agent-system`, `autonomous-os`, `model-routing`, `claude`, `llm-orchestration`, `ai-harness`, `intelligence-harvester`, `dag-scheduler`, `deepseek`, `gemini-api`

## Social Preview Text
Genesis Harness evolves static AI prompts into an autonomous multi-agent engineering OS featuring DAG task scheduling, dynamic multi-model routing, and automatic GitHub intelligence harvesting.
'''
with open(os.path.join(repo_root, "docs", "github_profile.md"), "w", encoding="utf-8") as f:
    f.write(github_profile)

# 8. Redesign README.md
readme_content = '''# Genesis Harness 🚀

[![CI](https://github.com/mertgoevse-wq/Genesis_Harness/actions/workflows/ci.yml/badge.svg)](https://github.com/mertgoevse-wq/Genesis_Harness/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-cyan.svg)](https://python.org)
[![Architecture: Autonomous OS](https://img.shields.io/badge/Architecture-Autonomous--OS-purple.svg)](#architecture)
[![Multi-Model Router](https://img.shields.io/badge/Router-Opus%20%7C%20Sonnet%20%7C%20Gemini%20%7C%20DeepSeek-brightgreen.svg)](#multi-model-routing)

> **Genesis Harness** is an autonomous AI Operating System for multi-agent engineering, research automation, business intelligence, and continuous AI ecosystem evolution.

---

## 🌟 Key Features

- 🤖 **Autonomous Multi-Agent Orchestration**: Parallel execution of specialized agents (CEO, CTO, Architect, Coding, QA, Harvester) using Directed Acyclic Graph (DAG) dependency resolution.
- 🚦 **Dynamic Multi-Model Routing**: Intelligent prompt routing to **Claude Opus 4.8**, **Claude Sonnet 4.6**, **Gemini 3.6 Flash**, **Kimi**, or **DeepSeek R1** based on task complexity.
- 🌾 **Intelligence Harvester**: Continuous autonomous scanning of the GitHub AI ecosystem to extract state-of-the-art workflows, patterns, and prompt structures.
- 🛡️ **Autonomous Quality Gates**: Built-in structural verification (`verify_structure.ps1`), secret scanning, and automated evaluation metrics.
- 📜 **Automatic Session Logs**: Immutable logging of active agents, model routing decisions, git commit hashes, and step results.

---

## 🏛️ System Architecture

```mermaid
graph TD
    User([User Request / Goal]) --> CEO[CEO Agent / Orchestrator]
    CEO --> Router{Intelligent Model Router}
    
    Router -->|System Architecture| Opus[Claude Opus 4.8]
    Router -->|Coding & Engineering| Sonnet[Claude Sonnet 4.6]
    Router -->|Large Context & Docs| Gemini[Gemini 3.6 Flash]
    Router -->|Math & Algorithms| DeepSeek[DeepSeek R1]

    Opus --> DAG[DAG Scheduler & Queue]
    Sonnet --> DAG
    Gemini --> DAG
    DeepSeek --> DAG

    DAG --> WorkerPool[Agent Worker Pool]
    WorkerPool --> Harvester[Intelligence Harvester Subsystem]
    WorkerPool --> QA[QA & Verification Gate]
    
    QA --> Output([Verified Commit & Artifacts])
```

---

## 🧩 Subsystems Overview

### 1. Multi-Agent Orchestration (`/orchestration/`)
Includes a persistent `TaskQueue`, `DependencyResolver`, multi-threaded `AgentWorkerPool`, `PipelineRunner`, and `PipelineEvaluator`.

### 2. Intelligence Harvester (`/harvester/`)
A 7-module subsystem (`discovery`, `ranking`, `analysis`, `knowledge_graph`, `engine`, `prompt_lab`, `scheduler`) designed to ingest public AI ecosystem advancements without copying implementation code.

### 3. Capability & Skill System (`configs/`)
Formally declares agent capabilities, required skills, model preferences, cost tiers, and quality thresholds in `agent_registry.json` and `skill_registry.json`.

---

## 📊 Capability Benchmarks

Genesis Harness is continuously evaluated against real-world product creation and architectural benchmarks:

| Benchmark | Focus | Output | Status |
|---|---|---|---|
| **Benchmark 01** | Autonomous AI Product Creation (< 5€ budget) | `ReviewPilot AI` SaaS | ✅ PASSED |
| **Harvester Benchmark** | Abstraction & Pattern Extraction | Knowledge Graph Proposals | ✅ PASSED |

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/mertgoevse-wq/Genesis_Harness.git
cd Genesis_Harness
```

### Run Structure Verification Gate

```powershell
pwsh -File scripts/verify_structure.ps1
```

---

## 🗺️ Roadmap

- [x] **Phase 1 & 2**: Technical & Business Agent Foundation
- [x] **Phase 3**: Autonomous Orchestration & Capability Benchmarking
- [x] **Phase 4**: Genesis Intelligence Harvester Architecture
- [x] **Phase 5**: Autonomous Multi-Agent Operating System & Model Router
- [ ] **Phase 6**: Autonomous Self-Correction & Live GitHub API Harvester Worker

---

## 🤝 Contributing

We welcome contributions! Please review our [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) and run `./scripts/verify_structure.ps1` before submitting pull requests.

---

## 📄 License

Distributed under the MIT License.
'''
with open(os.path.join(repo_root, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("GitHub Branding & README Redesign complete.")
