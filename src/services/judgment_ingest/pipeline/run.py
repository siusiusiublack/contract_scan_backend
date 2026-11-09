"""Orchestrate search → fetch → parse → normalize → dedupe → store."""

from __future__ import annotations

from dataclasses import dataclass, field

from judgment_ingest.config import Settings
from judgment_ingest.pipeline.dedupe import should_skip
from judgment_ingest.pipeline.fetch import RateLimiter, with_retries
from judgment_ingest.pipeline.parse import collapse_whitespace
from judgment_ingest.sources.find_case_law import FindCaseLawAdapter
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
        "database_url": settings.database_url,
        "documents": str(repo.count()),
        "default_queries": ", ".join(settings.query_list),
        "rate_limit_seconds": str(settings.rate_limit_seconds),
    }


def run_ingest(
    *,
    settings: Settings,
    source: str,
    query: str | None,
    limit: int,
    dry_run: bool,
) -> IngestResult:
    result = IngestResult()
    if source != "fcl":
        result.errors.append(f"Unsupported source '{source}'. v0 supports: fcl")
        result.messages.append("Aborting.")
        return result

    FileStore(settings).ensure_dirs()
    repo = DocumentRepository(settings)
    repo.ensure_schema()
    adapter = FindCaseLawAdapter(settings)
    limiter = RateLimiter(settings.rate_limit_seconds)

    queries = [query] if query else settings.query_list
    result.messages.append(f"source={source} limit={limit} dry_run={dry_run}")
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
        except Exception as exc:  # noqa: BLE001 — surface in CLI
            result.errors.append(f"search failed for '{q}': {exc}")
            continue
        stubs.extend(batch)
        remaining = limit - len(stubs)

    # Deduplicate stubs by url within this run
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

    store = FileStore(settings)
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
        except Exception as exc:  # noqa: BLE001
            result.errors.append(f"failed {stub.url}: {exc}")

    result.messages.append(
        f"done stored={result.stored} skipped={result.skipped} errors={len(result.errors)}"
    )
    return result
