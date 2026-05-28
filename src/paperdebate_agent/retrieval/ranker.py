"""Simple deterministic ranking utilities."""

from __future__ import annotations

import re

from paperdebate_agent.schemas import Paper, RankedPaper


def rank_papers(papers: list[Paper], topic: str, direction: str | None = None) -> list[RankedPaper]:
    """Rank papers using lexical overlap and small recency bonus.

    This is intentionally lightweight. Embedding-based retrieval can replace this later while
    preserving the same output schema.
    """
    query = f"{topic} {direction or ''}"
    query_terms = set(_tokenize(query))
    ranked: list[RankedPaper] = []
    for paper in papers:
        text = f"{paper.title} {paper.abstract} {' '.join(paper.tags)}"
        terms = set(_tokenize(text))
        overlap = len(query_terms & terms)
        recency = 0.0 if paper.year is None else max(0.0, min((paper.year - 2020) / 10.0, 1.0))
        score = overlap + recency
        rationale = f"lexical_overlap={overlap}, recency_bonus={recency:.2f}"
        ranked.append(RankedPaper(paper=paper, score=round(score, 3), rationale=rationale))

    ranked.sort(key=lambda item: (-item.score, item.paper.title.lower()))
    return ranked


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
