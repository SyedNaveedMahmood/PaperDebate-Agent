"""Report writers for pipeline outputs."""

from __future__ import annotations

import json
from pathlib import Path

from paperdebate_agent.schemas import PipelineResult


def write_json(result: PipelineResult, path: Path) -> None:
    """Write full structured result as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown(result: PipelineResult, path: Path) -> None:
    """Write a human-readable Markdown report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# PaperDebate Report: {result.topic}")
    lines.append("")
    if result.direction:
        lines.append(f"**Direction:** {result.direction}")
        lines.append("")

    lines.append("## Ranked papers")
    lines.append("")
    for index, ranked in enumerate(result.ranked_papers, start=1):
        paper = ranked.paper
        authors = ", ".join(paper.authors) if paper.authors else "Unknown authors"
        year = paper.year if paper.year is not None else "n.d."
        lines.append(f"### {index}. {paper.title}")
        lines.append(f"- **ID:** `{paper.paper_id}`")
        lines.append(f"- **Authors:** {authors}")
        lines.append(f"- **Year/Venue:** {year}, {paper.venue or 'Unknown venue'}")
        lines.append(f"- **Score:** {ranked.score} ({ranked.rationale})")
        lines.append(f"- **Abstract:** {paper.abstract}")
        lines.append("")

    lines.append("## Multi-agent debate")
    lines.append("")
    for finding in result.debate:
        lines.append(f"### {finding.agent_name}")
        lines.append(f"- **Stance:** {finding.stance}")
        lines.append(f"- **Score:** {finding.score}")
        lines.append(f"- **Evidence IDs:** {', '.join(finding.evidence_ids)}")
        for comment in finding.comments:
            lines.append(f"  - {comment}")
        lines.append("")

    lines.append("## Ranked research gaps")
    lines.append("")
    for index, gap in enumerate(result.gaps, start=1):
        lines.append(f"### {index}. {gap.title}")
        lines.append(f"- **Problem:** {gap.problem}")
        lines.append(f"- **Why it matters:** {gap.why_it_matters}")
        lines.append(f"- **Proposed experiment:** {gap.proposed_experiment}")
        lines.append(f"- **Novelty score:** {gap.novelty_score}")
        lines.append(f"- **Feasibility score:** {gap.feasibility_score}")
        lines.append(f"- **Reviewer risk:** {gap.reviewer_risk}")
        lines.append(f"- **Evidence IDs:** {', '.join(gap.evidence_ids)}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
