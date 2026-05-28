# AGENTS.md

This file tells Codex and future coding agents how to work on PaperDebate Agent.

## Project mission

PaperDebate Agent is a local-first multi-agent research assistant. It helps a researcher move from a broad topic to an evidence-grounded literature map, a reviewer-style debate, and ranked research-gap proposals.

The system must prioritize correctness, traceability, reproducibility, and modularity over flashy demos.

## Non-negotiable engineering rules

1. Keep the pipeline runnable on a CPU-only laptop.
2. Do not require paid APIs for the default path.
3. Every generated claim must be tied to retrieved evidence when possible.
4. Do not silently hallucinate paper metadata.
5. Prefer deterministic offline behavior for tests.
6. Keep modules small, typed, and independently testable.
7. Do not put secrets, API keys, `.env`, caches, vector DBs, or generated outputs into git.
8. All new functionality should have at least one unit test.
9. Use clear error messages and avoid broad bare `except` blocks.
10. Preserve backward-compatible CLI behavior unless intentionally changing it.

## Target architecture

```text
User topic
  -> search connectors
  -> paper normalization
  -> local corpus store
  -> retrieval/ranking
  -> role-based debate agents
  -> synthesis
  -> JSON/Markdown report
```

## Main modules

- `src/paperdebate_agent/connectors/`: public paper-source clients such as arXiv, OpenAlex, Semantic Scholar, and ACL Anthology.
- `src/paperdebate_agent/retrieval/`: embedding, lexical ranking, vector-store adapters, reranking.
- `src/paperdebate_agent/agents/`: role-specific agents such as novelty reviewer, skeptic reviewer, feasibility reviewer, and synthesizer.
- `src/paperdebate_agent/pipelines/`: orchestration logic.
- `src/paperdebate_agent/io/`: report writers and file utilities.
- `tests/`: unit tests with no network calls by default.

## Current MVP behavior

The current scaffold uses an offline deterministic paper-search stub and heuristic agents. This is intentional. It gives the repository a working baseline before adding external APIs and local LLM backends.

Future work should add real connectors behind explicit config flags, while keeping offline tests intact.

## Coding style

- Python 3.10+.
- Use type hints for public functions.
- Use dataclasses or Pydantic-style schemas for structured data. The current implementation uses dataclasses to keep dependencies minimal.
- Prefer pure functions where possible.
- Keep agent prompts, scoring rubrics, and report templates easy to inspect.
- Avoid hidden global state.

## CLI contract

The main CLI command should remain:

```bash
paperdebate run --topic "..." --direction "..." --max-papers 10
```

It should write:

```text
outputs/runs/<timestamp>/report.md
outputs/runs/<timestamp>/result.json
```

## Testing contract

Run:

```bash
pytest
ruff check .
```

Tests must not rely on internet access, external LLM APIs, GPUs, or large model downloads.

## Planned implementation phases

### Phase 1: Stable MVP

- Keep offline search stub.
- Implement deterministic debate and report generation.
- Add tests for normalization, ranking, and pipeline output.

### Phase 2: Public paper connectors

Add optional connectors:

- arXiv API
- OpenAlex API
- Semantic Scholar API
- ACL Anthology scraping or metadata ingestion

Each connector must return the shared `Paper` schema.

### Phase 3: Local LLM backend

Add optional local generation backends:

- Ollama
- LM Studio OpenAI-compatible endpoint
- llama.cpp server

Do not make these mandatory for the core tests.

### Phase 4: Retrieval improvements

Add optional embedding-based retrieval:

- SentenceTransformers
- ChromaDB
- local cache under `.cache/` or `data/`, ignored by git

### Phase 5: Evaluation

Add benchmark topics and metrics:

- paper recall at k
- duplicate rate
- hallucinated-paper rate
- evidence-grounding score
- idea diversity
- human reviewer usefulness score

## Definition of done for pull requests

A PR is acceptable when:

- code is formatted and lint-clean,
- tests pass locally,
- new behavior is documented,
- generated files are not committed,
- the README or docs are updated when user-facing behavior changes,
- the offline path still works.

## Safe defaults

When uncertain, choose the simplest deterministic implementation that preserves the architecture and can be replaced later with a stronger backend.
