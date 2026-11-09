import typer

from judgment_ingest import __version__
from judgment_ingest.config import get_settings
from judgment_ingest.pipeline.run import run_ingest, status_summary
from judgment_ingest.sources.registry import describe_sources

app = typer.Typer(
    name="judgment-ingest",
    help="Housing-focused UK judgment ingest (pluggable sources; FCL first).",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Contract Scan — judgment ingest CLI."""


@app.command("status")
def status_cmd() -> None:
    """Show config paths and document counts."""
    settings = get_settings()
    summary = status_summary(settings)
    typer.echo(f"judgment-ingest {__version__}")
    for key, value in summary.items():
        typer.echo(f"  {key}: {value}")


@app.command("sources")
def sources_cmd() -> None:
    """List registered adapters and which are enabled in config."""
    settings = get_settings()
    rows = describe_sources(settings)
    if not rows:
        typer.echo("No sources registered.")
        return
    typer.echo(
        f"{'id':<12} {'registered':<12} {'enabled':<22} {'transport':<12} {'interval_s'}"
    )
    for row in rows:
        typer.echo(
            f"{row['id']:<12} {row['registered']:<12} {row['enabled']:<22} "
            f"{row.get('transport', '-'):<12} {row.get('interval_s', '-')}"
        )


@app.command("run")
def run_cmd(
    source: str = typer.Option(
        "fcl",
        help="Source id, or 'all' for every ENABLED_SOURCES entry",
    ),
    query: str | None = typer.Option(
        None, help="Search query; default uses housing query list from config"
    ),
    limit: int = typer.Option(5, help="Max documents to ingest per source this run"),
    dry_run: bool = typer.Option(
        False, help="Search/plan only — do not fetch or store"
    ),
) -> None:
    """Run ingest via the source registry (pipeline stays source-agnostic)."""
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
    for err in result.errors:
        typer.secho(err, fg=typer.colors.RED, err=True)
    if result.errors:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
