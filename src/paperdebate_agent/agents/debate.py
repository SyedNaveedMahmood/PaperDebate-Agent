"""Deterministic role-based debate agents for the MVP."""

from __future__ import annotations

from paperdebate_agent.schemas import AgentFinding, RankedPaper, ResearchGap


def run_debate(ranked_papers: list[RankedPaper], topic: str, direction: str | None = None) -> list[AgentFinding]:
    """Run lightweight role-based analysis over ranked evidence."""
    evidence_ids = [item.paper.paper_id for item in ranked_papers[:5]]
    top_titles = [item.paper.title for item in ranked_papers[:3]]
    direction_text = direction or "No explicit direction supplied."

    return [
        AgentFinding(
            agent_name="Novelty Agent",
            stance="Promising if the final idea is framed around a specific underexplored mechanism, not only paper aggregation.",
            score=7.5,
            evidence_ids=evidence_ids,
            comments=[
                f"Topic: {topic}",
                f"Direction: {direction_text}",
                "Top evidence suggests value in connecting adjacent threads rather than summarizing one thread.",
                f"Most relevant papers: {', '.join(top_titles)}",
            ],
        ),
        AgentFinding(
            agent_name="Skeptic Reviewer",
            stance="Main risk is generic novelty. The project must show traceable evidence, explicit reviewer-risk analysis, and measurable quality criteria.",
            score=6.8,
            evidence_ids=evidence_ids,
            comments=[
                "Avoid presenting a simple paper-search wrapper as an agentic research contribution.",
                "Require evidence IDs for every synthesized claim.",
                "Add evaluation metrics such as hallucinated-paper rate and evidence-grounding score.",
            ],
        ),
        AgentFinding(
            agent_name="Feasibility Agent",
            stance="Feasible on CPU if the default path uses metadata, lexical retrieval, and optional local LLM backends.",
            score=8.4,
            evidence_ids=evidence_ids,
            comments=[
                "Keep network connectors optional.",
                "Keep embeddings optional until the deterministic MVP is stable.",
                "Use JSON and Markdown outputs for easy inspection and GitHub demos.",
            ],
        ),
    ]


def synthesize_gaps(ranked_papers: list[RankedPaper], debate: list[AgentFinding]) -> list[ResearchGap]:
    """Create ranked research-gap proposals from evidence and debate."""
    evidence_ids = [item.paper.paper_id for item in ranked_papers[:5]]
    novelty = _average_score(debate, "Novelty Agent")
    feasibility = _average_score(debate, "Feasibility Agent")

    return [
        ResearchGap(
            title="Evidence-Grounded Multi-Agent Literature Debate",
            problem="Current literature-review agents often summarize papers without making the evidentiary basis of their research-gap claims auditable.",
            why_it_matters="A researcher needs to know whether a proposed gap is supported by retrieved papers, contradicted by prior work, or merely hallucinated.",
            proposed_experiment="Build a benchmark of topics and evaluate paper recall, duplicate rate, hallucinated-paper rate, evidence-grounding score, and human usefulness of generated gaps.",
            novelty_score=round(novelty, 2),
            feasibility_score=round(feasibility, 2),
            reviewer_risk="Medium: the system must demonstrate measurable improvement over search-plus-summary baselines.",
            evidence_ids=evidence_ids,
        ),
        ResearchGap(
            title="Local-First Research Ideation Without Paid APIs",
            problem="Many agentic research assistants assume cloud LLM APIs, which limits reproducibility, privacy, and accessibility for students or independent researchers.",
            why_it_matters="A CPU-friendly local baseline makes research tooling more accessible and easier to evaluate under controlled settings.",
            proposed_experiment="Compare deterministic, local-LLM, and cloud-LLM modes under the same retrieval corpus and scoring rubric.",
            novelty_score=7.0,
            feasibility_score=8.5,
            reviewer_risk="Low-to-medium: useful as an engineering contribution, but needs strong evaluation for publication-level claims.",
            evidence_ids=evidence_ids,
        ),
    ]


def _average_score(debate: list[AgentFinding], agent_name: str) -> float:
    scores = [finding.score for finding in debate if finding.agent_name == agent_name]
    return sum(scores) / len(scores) if scores else 0.0
