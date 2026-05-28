"""Main orchestration pipeline."""

from __future__ import annotations

from paperdebate_agent.agents.debate import run_debate, synthesize_gaps
from paperdebate_agent.retrieval.ranker import rank_papers
from paperdebate_agent.schemas import PipelineResult
from paperdebate_agent.search import offline_search


def run_pipeline(topic: str, *, direction: str | None = None, max_papers: int = 10) -> PipelineResult:
    """Run the current offline MVP pipeline."""
    if not topic.strip():
        raise ValueError("topic must not be empty")
    if max_papers <= 0:
        raise ValueError("max_papers must be positive")

    papers = offline_search(topic, max_papers=max_papers)
    ranked = rank_papers(papers, topic=topic, direction=direction)
    debate = run_debate(ranked, topic=topic, direction=direction)
    gaps = synthesize_gaps(ranked, debate)
    return PipelineResult(
        topic=topic,
        direction=direction,
        ranked_papers=ranked,
        debate=debate,
        gaps=gaps,
    )
