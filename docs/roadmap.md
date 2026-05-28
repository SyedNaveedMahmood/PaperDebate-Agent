# Roadmap

## Phase 1: Offline MVP

- [x] Package scaffold
- [x] Codex instructions
- [x] Offline paper search stub
- [x] Lexical ranking
- [x] Deterministic debate agents
- [x] JSON and Markdown reports
- [x] Unit tests
- [x] CI workflow

## Phase 2: Real paper search

- [ ] arXiv connector
- [ ] OpenAlex connector
- [ ] Semantic Scholar connector
- [ ] ACL Anthology connector
- [ ] Deduplication across sources
- [ ] Citation and venue normalization

## Phase 3: Local LLM integration

- [ ] Ollama backend
- [ ] LM Studio backend
- [ ] llama.cpp server backend
- [ ] Prompt templates for each agent role
- [ ] Strict JSON-output parser with repair fallback

## Phase 4: Retrieval upgrade

- [ ] SentenceTransformers embedding backend
- [ ] ChromaDB vector store
- [ ] BM25 ranking
- [ ] Hybrid lexical + dense retrieval
- [ ] Optional local reranker

## Phase 5: UI

- [ ] Streamlit dashboard
- [ ] Literature graph visualization
- [ ] Debate transcript viewer
- [ ] Research-gap export
- [ ] BibTeX import/export

## Phase 6: Evaluation

- [ ] Benchmark topic suite
- [ ] Paper recall@k
- [ ] Duplicate rate
- [ ] Hallucinated-paper rate
- [ ] Evidence-grounding score
- [ ] Human usefulness rubric

## Phase 7: Research-grade system

- [ ] Compare with search-only and single-agent baselines
- [ ] Ablate agent roles
- [ ] Ablate evidence constraints
- [ ] Analyze failure cases
- [ ] Prepare technical report or workshop paper
