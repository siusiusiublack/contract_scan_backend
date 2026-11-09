"""Orchestrate search → fetch → parse → normalize → dedupe → store."""

from __future__ import annotations

from dataclasses import dataclass, field

from judgment_ingest.config import Settings
from judgment_ingest.pipeline.dedupe import should_skip
from judgment_ingest.pipeline.fetch import RateLimitedError, RateLimiter, with_retries
from judgment_ingest.pipeline.parse import collapse_whitespace
from judgment_ingest.sources.registry import get_adapter, list_enabled
from judgment_ingest.storage.db import DocumentRepository
from judgment_ingest.storage.fs import FileStore


@dataclass
class IngestResult:
    messages: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    stored: int = 0
    skipped: int = 0


def status_summary(settings: Settings) -> dict[str, str]:
    repo = DocumentRepository(settings)
    repo.ensure_schema()
    return {
        "data_dir": str(settings.data_dir.resolve()),
        "raw_root": str(settings.raw_root.resolve()),
        "processed_root": str(settings.processed_root.resolve()),
        "db_dir": str(settings.db_dir.resolve()),
        "database_url": settings.database_url,
        "documents": str(repo.count()),
        "default_queries": ", ".join(settings.query_list),
        "enabled_sources": ", ".join(list_enabled(settings)) or "(none)",
        "rate_limit_seconds_fallback": str(settings.rate_limit_seconds),
        "fcl_rate_limit_seconds": str(settings.fcl_rate_limit_seconds),
        "bailii_rate_limit_seconds": str(settings.bailii_rate_limit_seconds),
    }


def run_ingest(
    *,
    settings: Settings,
    source: str,
    query: str | None,
    limit: int,
    dry_run: bool,
) -> IngestResult:
    """Run one source, or all enabled sources when source == 'all'."""
    result = IngestResult()
    if source == "all":
        targets = list_enabled(settings)
        if not targets:
            result.errors.append(
                "No enabled sources. Set JUDGMENT_INGEST_ENABLED_SOURCES "
                "and register adapters."
            )
            result.messages.append("Aborting.")
            return result
        for source_id in targets:
            partial = _run_one_source(
                settings=settings,
                source_id=source_id,
                query=query,
                limit=limit,
                dry_run=dry_run,
            )
            result.messages.extend(partial.messages)
            result.errors.extend(partial.errors)
            result.stored += partial.stored
            result.skipped += partial.skipped
        result.messages.append(
            f"all-sources done stored={result.stored} "
            f"skipped={result.skipped} errors={len(result.errors)}"
        )
        return result

    return _run_one_source(
        settings=settings,
        source_id=source,
        query=query,
        limit=limit,
        dry_run=dry_run,
    )


def _run_one_source(
    *,
    settings: Settings,
    source_id: str,
    query: str | None,
    limit: int,
    dry_run: bool,
) -> IngestResult:
    result = IngestResult()
    try:
        adapter = get_adapter(source_id, settings)
    except KeyError as exc:
        result.errors.append(str(exc))
        result.messages.append("Aborting.")
        return result

    store = FileStore(settings)
    store.ensure_dirs(source_id)
    repo = DocumentRepository(settings)
    repo.ensure_schema()
    interval = settings.rate_limit_for(source_id)
    limiter = RateLimiter(interval)

    queries = [query] if query else settings.query_list
    transport = getattr(adapter, "transport", "unknown")
    result.messages.append(
        f"source={source_id} transport={transport} "
        f"interval_s={interval} limit={limit} dry_run={dry_run}"
    )
    result.messages.append(f"queries={queries}")

    stubs = []
    remaining = limit
    for q in queries:
        if remaining <= 0:
            break
        try:
            batch = with_retries(
                lambda q=q, remaining=remaining: adapter.search(q, remaining),
                rate_limiter=limiter,
            )
        except RateLimitedError as exc:
            result.errors.append(f"search rate-limited for '{q}': {exc}")
            result.messages.append(
                f"Stopping source={source_id} after rate limit — "
                "increase interval or reduce --limit; do not probe for 429."
            )
            return result
        except Exception as exc:  # noqa: BLE001 — surface in CLI
            result.errors.append(f"search failed for '{q}': {exc}")
            continue
        stubs.extend(batch)
        remaining = limit - len(stubs)

    seen_urls: set[str] = set()
    unique_stubs = []
    for stub in stubs:
        if stub.url in seen_urls:
            continue
        seen_urls.add(stub.url)
        unique_stubs.append(stub)
    unique_stubs = unique_stubs[:limit]
    result.messages.append(f"search_hits={len(unique_stubs)}")

    if dry_run:
        for stub in unique_stubs:
            result.messages.append(f"DRY-RUN would fetch: {stub.title} ({stub.url})")
        return result

    for stub in unique_stubs:
        try:
            raw = with_retries(lambda s=stub: adapter.fetch(s), rate_limiter=limiter)
            clean = adapter.parse(raw)
            clean.text = collapse_whitespace(clean.text)
            skip, reason = should_skip(repo, clean)
            if skip:
                result.skipped += 1
                result.messages.append(f"skip {clean.doc_id} ({reason})")
                continue
            raw_path, clean_path = store.write(clean, raw_body=raw.body)
            clean.raw_path = str(raw_path)
            clean.clean_path = str(clean_path)
            repo.upsert(clean)
            result.stored += 1
            result.messages.append(
                f"stored {clean.doc_id} practice_area={clean.practice_area}"
            )
        except RateLimitedError as exc:
            result.errors.append(f"rate-limited on {stub.url}: {exc}")
            result.messages.append(
                f"Stopping source={source_id} after rate limit — "
                "increase interval or reduce --limit; do not probe for 429."
            )
            break
        except Exception as exc:  # noqa: BLE001
            result.errors.append(f"failed {stub.url}: {exc}")

    result.messages.append(
        f"done source={source_id} stored={result.stored} "
        f"skipped={result.skipped} errors={len(result.errors)}"
    )
    return result
