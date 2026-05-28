"""Offline search stub and normalization utilities.

Real arXiv/OpenAlex/Semantic Scholar connectors should be added later behind config flags.
This module intentionally has no network dependency so tests and demos stay deterministic.
"""

from __future__ import annotations

import hashlib
import re

from paperdebate_agent.schemas import Paper


_SEED_PAPERS = [
    {
        "title": "Representation-Level Diagnostics for Language Model Unlearning",
        "authors": ["A. Researcher", "B. Systems"],
        "year": 2025,
        "venue": "Synthetic Offline Corpus",
        "abstract": "Studies whether language model unlearning removes target representations or only suppresses surface generations. Evaluates activation signatures, utility drift, and adversarial recovery.",
        "tags": ["unlearning", "representation", "diagnostics"],
    },
    {
        "title": "Sparse Autoencoders as Interfaces for Mechanistic Interpretability",
        "authors": ["C. Feature", "D. Circuit"],
        "year": 2024,
        "venue": "Synthetic Offline Corpus",
        "abstract": "Explores sparse autoencoders for decomposing residual stream activations into interpretable features, with discussion of monosemanticity and downstream model analysis.",
        "tags": ["sparse autoencoders", "interpretability", "features"],
    },
    {
        "title": "Training Data Extraction Risks in Large Language Models",
        "authors": ["E. Privacy", "F. Attack"],
        "year": 2023,
        "venue": "Synthetic Offline Corpus",
        "abstract": "Analyzes memorization and extraction attacks against language models, including prompt-based attacks, verbatim sequence recovery, and privacy leakage measurement.",
        "tags": ["privacy", "memorization", "extraction"],
    },
    {
        "title": "Local Multi-Agent Systems for Scientific Literature Review",
        "authors": ["G. Agent", "H. Review"],
        "year": 2026,
        "venue": "Synthetic Offline Corpus",
        "abstract": "Presents local agents for paper triage, debate, research gap synthesis, and reviewer-style critique without relying on paid cloud APIs.",
        "tags": ["agents", "literature review", "research ideation"],
    },
    {
        "title": "Reviewer-Centric Evaluation of Research Idea Generation",
        "authors": ["I. Evaluation", "J. Novelty"],
        "year": 2025,
        "venue": "Synthetic Offline Corpus",
        "abstract": "Defines metrics for idea generation systems including novelty, feasibility, evidence grounding, reviewer risk, and hallucinated citation rate.",
        "tags": ["evaluation", "novelty", "reviewer risk"],
    },
]


def stable_id(title: str) -> str:
    """Create a stable short identifier from a paper title."""
    digest = hashlib.sha1(title.lower().encode("utf-8")).hexdigest()[:10]
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
    return f"{slug}-{digest}"


def offline_search(topic: str, *, max_papers: int = 10) -> list[Paper]:
    """Return deterministic synthetic papers ranked roughly by lexical overlap."""
    query_terms = set(_tokenize(topic))
    scored: list[tuple[float, dict[str, object]]] = []
    for row in _SEED_PAPERS:
        haystack = " ".join(
            [str(row["title"]), str(row["abstract"]), " ".join(row.get("tags", []))]
        )
        overlap = len(query_terms.intersection(_tokenize(haystack)))
        scored.append((float(overlap), row))

    scored.sort(key=lambda item: (-item[0], str(item[1]["title"])))
    papers: list[Paper] = []
    for _, row in scored[:max_papers]:
        title = str(row["title"])
        papers.append(
            Paper(
                paper_id=stable_id(title),
                title=title,
                authors=list(row["authors"]),
                year=int(row["year"]),
                venue=str(row["venue"]),
                abstract=str(row["abstract"]),
                url=None,
                source="offline_stub",
                tags=list(row.get("tags", [])),
            )
        )
    return papers


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
