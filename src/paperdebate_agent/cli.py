"""Command-line interface for PaperDebate Agent."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console

from paperdebate_agent.io.reports import write_json, write_markdown
from paperdebate_agent.pipelines.run import run_pipeline

app = typer.Typer(help="PaperDebate Agent CLI")
console = Console()


@app.command()
def run(
    topic: str = typer.Option(..., "--topic", "-t", help="Research topic to investigate."),
    direction: str | None = typer.Option(None, "--direction", "-d", help="Optional research direction."),
    max_papers: int = typer.Option(10, "--max-papers", min=1, help="Maximum papers to retrieve."),
    output_dir: Path = typer.Option(Path("outputs/runs"), "--output-dir", help="Output directory."),
) -> None:
    """Run the offline MVP pipeline and write JSON/Markdown reports."""
    result = run_pipeline(topic=topic, direction=direction, max_papers=max_papers)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / stamp
    json_path = run_dir / "result.json"
    md_path = run_dir / "report.md"
    write_json(result, json_path)
    write_markdown(result, md_path)

    console.print("[bold green]PaperDebate run complete.[/bold green]")
    console.print(f"Markdown report: {md_path}")
    console.print(f"JSON result: {json_path}")


if __name__ == "__main__":
    app()
