import typer

from judgment_ingest import __version__
from judgment_ingest.config import get_settings
from judgment_ingest.pipeline.run import run_ingest, status_summary

app = typer.Typer(
    name="judgment-ingest",
    help="Housing-focused UK judgment ingest (Find Case Law first).",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Contract Scan — judgment ingest CLI."""


@app.command("status")
def status_cmd() -> None:
    """Show config paths and document counts (scaffold-safe)."""
    settings = get_settings()
    summary = status_summary(settings)
    typer.echo(f"judgment-ingest {__version__}")
    for key, value in summary.items():
        typer.echo(f"  {key}: {value}")


@app.command("run")
def run_cmd(
    source: str = typer.Option("fcl", help="Source adapter id (v0: fcl only)"),
    query: str | None = typer.Option(
        None, help="Search query; default uses housing query list from config"
    ),
    limit: int = typer.Option(5, help="Max documents to ingest this run"),
    dry_run: bool = typer.Option(
        False, help="Search/plan only — full fetch wired in a follow-up commit"
    ),
) -> None:
    """Run ingest pipeline (v0 scaffold: validates wiring; fetch land next)."""
    settings = get_settings()
    result = run_ingest(
        settings=settings,
        source=source,
        query=query,
        limit=limit,
        dry_run=dry_run,
    )
    for line in result.messages:
        typer.echo(line)
    if result.errors:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
