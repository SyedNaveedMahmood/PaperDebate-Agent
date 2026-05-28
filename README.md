# PaperDebate Agent

**PaperDebate Agent** is a local-first multi-agent literature review system for paper discovery, evidence-grounded summarization, reviewer-style critique, and research-gap generation.

The project is designed to be useful for ML, NLP, AI safety, interpretability, and systems research workflows where the user wants to move from a broad topic to a defensible research direction.

## Core idea

Given a research topic, PaperDebate Agent:

1. searches public paper sources,
2. normalizes and stores paper metadata,
3. embeds paper abstracts into a local vector index,
4. runs multiple role-based agents over the retrieved evidence,
5. makes the agents debate novelty, feasibility, and reviewer risk,
6. outputs ranked research gaps and concrete experiment plans.

## Current status

This repository contains a clean MVP scaffold that can run without a GPU and without paid LLM APIs. The first implementation uses deterministic local heuristics by default, with optional adapters for local LLM backends such as Ollama or LM Studio added later.

## Why this project exists

Most research-assistant agent demos produce generic paper lists or hallucinated ideas. PaperDebate Agent is designed around stricter constraints:

- every generated idea should be tied to retrieved papers,
- every agent decision should expose its evidence,
- novelty and feasibility should be scored separately,
- reviewer risks should be explicit,
- the pipeline should be reproducible from a config file.

## Features in this scaffold

- Modular Python package under `src/paperdebate_agent/`
- Codex-ready implementation instructions in `AGENTS.md`
- CLI entry point: `paperdebate run --topic "..."`
- Deterministic paper search stub for offline development
- Paper normalization and deduplication
- Heuristic retrieval and ranking
- Role-based debate agents
- Research-gap synthesis
- JSON and Markdown report export
- Unit tests
- GitHub Actions CI

## Quick start

```bash
git clone https://github.com/SyedNaveedMahmood/PaperDebate-Agent.git
cd PaperDebate-Agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
cp .env.example .env
paperdebate run --topic "LLM unlearning with representation-level diagnostics" --max-papers 8
```

The run will create outputs under:

```text
outputs/runs/<timestamp>/
```

## Example command

```bash
paperdebate run \
  --topic "Sparse autoencoders for memorization and privacy leakage" \
  --direction "attack plus defense, not benchmark-only" \
  --max-papers 12
```

## Repository layout

```text
.
├── AGENTS.md
├── agent.md
├── README.md
├── configs/
│   └── default.yaml
├── docs/
│   ├── architecture.md
│   └── roadmap.md
├── src/paperdebate_agent/
│   ├── agents/
│   ├── io/
│   ├── pipelines/
│   ├── retrieval/
│   ├── schemas.py
│   └── cli.py
├── tests/
└── .github/workflows/ci.yml
```

## Design philosophy

PaperDebate Agent should be built as a serious research tool, not a chatbot wrapper. Each module should be independently testable, every output should be reproducible, and every claim should be traceable to retrieved evidence.

## License

MIT License.
