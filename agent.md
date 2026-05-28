# agent.md

This file mirrors `AGENTS.md` for tools or workflows that look for a lowercase agent instruction file.

Use `AGENTS.md` as the canonical implementation guide.

## Build objective

Create a local-first LLM-agent research assistant that discovers papers, ranks evidence, runs a structured multi-agent debate, and produces grounded research-gap reports.

## Immediate Codex task sequence

1. Keep the offline MVP runnable.
2. Add real paper connectors behind config flags.
3. Add local LLM backends without making them required.
4. Add vector retrieval behind optional dependencies.
5. Strengthen evaluation and reporting.

## Core command

```bash
paperdebate run --topic "LLM unlearning with representation-level diagnostics" --max-papers 8
```

## Guardrails

- No paid API required by default.
- No network required for tests.
- No generated output committed.
- No secrets committed.
- Every future agent output should expose evidence IDs.
