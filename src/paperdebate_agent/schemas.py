"""Shared data schemas for PaperDebate Agent."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Paper:
    """Normalized paper metadata used across connectors and agents."""

    paper_id: str
    title: str
    authors: list[str]
    year: int | None
    venue: str | None
    abstract: str
    url: str | None = None
    source: str = "unknown"
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RankedPaper:
    """A paper plus relevance score and rationale."""

    paper: Paper
    score: float
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "paper": self.paper.to_dict(),
            "score": self.score,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class AgentFinding:
    """Single role-agent judgment."""

    agent_name: str
    stance: str
    score: float
    evidence_ids: list[str]
    comments: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResearchGap:
    """Synthesized research-gap proposal."""

    title: str
    problem: str
    why_it_matters: str
    proposed_experiment: str
    novelty_score: float
    feasibility_score: float
    reviewer_risk: str
    evidence_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PipelineResult:
    """Complete pipeline result."""

    topic: str
    direction: str | None
    ranked_papers: list[RankedPaper]
    debate: list[AgentFinding]
    gaps: list[ResearchGap]

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "direction": self.direction,
            "ranked_papers": [item.to_dict() for item in self.ranked_papers],
            "debate": [item.to_dict() for item in self.debate],
            "gaps": [item.to_dict() for item in self.gaps],
        }
