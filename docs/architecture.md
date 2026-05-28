# Architecture

PaperDebate Agent is designed as a modular, local-first research assistant.

## Pipeline

```text
Topic + direction
  -> paper source connectors
  -> normalization and deduplication
  -> retrieval and ranking
  -> role-based debate
  -> gap synthesis
  -> report export
```

## Components

### 1. Search connectors

Connectors should return normalized `Paper` objects. The default offline connector is deterministic and used for tests.

Planned connectors:

- arXiv
- OpenAlex
- Semantic Scholar
- ACL Anthology
- local BibTeX / JSON import

### 2. Retrieval

The MVP uses lexical ranking. Future retrieval backends should preserve the `RankedPaper` schema.

Planned retrieval modes:

- lexical overlap
- BM25
- SentenceTransformers embeddings
- ChromaDB vector search
- reranking with local cross-encoders

### 3. Debate agents

The debate layer uses role-specific agents. Each agent must return:

- stance
- score
- evidence IDs
- comments

Initial agents:

- Novelty Agent
- Skeptic Reviewer
- Feasibility Agent

Planned agents:

- ML Security Agent
- Systems Feasibility Agent
- Experiment Design Agent
- ACL/EMNLP Reviewer Agent
- Positioning Agent

### 4. Synthesis

The synthesizer converts retrieved papers and debate findings into ranked research gaps.

Each gap should include:

- title
- problem
- why it matters
- proposed experiment
- novelty score
- feasibility score
- reviewer risk
- evidence IDs

## Reproducibility requirements

- All major outputs must be serializable to JSON.
- Every run should write a timestamped output folder.
- Offline tests must not use the network.
- Generated outputs must not be committed.

## Publication-level extension

To turn this into a serious research artifact, add evaluation against benchmark topics and compare against:

1. plain search,
2. search plus summarization,
3. single-agent ideation,
4. multi-agent debate without evidence constraints,
5. PaperDebate with evidence-grounded debate.
