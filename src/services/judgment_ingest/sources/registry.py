"""Pluggable source registry — add N adapters without rewriting the pipeline."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from judgment_ingest.config import Settings
from judgment_ingest.sources.base import SourceAdapter
from judgment_ingest.sources.find_case_law import FindCaseLawAdapter

AdapterFactory = Callable[[Settings], Any]

# Registered adapters (code may know many). Runtime runs ENABLED_SOURCES only.
_ADAPTERS: dict[str, AdapterFactory] = {
    "fcl": lambda settings: FindCaseLawAdapter(settings),
}


def register(source_id: str, factory: AdapterFactory) -> None:
    """Register or replace an adapter factory (useful in tests)."""
    _ADAPTERS[source_id] = factory


def registered_ids() -> list[str]:
    return sorted(_ADAPTERS.keys())


def get_adapter(source_id: str, settings: Settings) -> SourceAdapter:
    try:
        factory = _ADAPTERS[source_id]
    except KeyError as exc:
        known = ", ".join(registered_ids()) or "(none)"
        raise KeyError(
            f"Unknown source '{source_id}'. Registered: {known}"
        ) from exc
    return factory(settings)


def list_enabled(settings: Settings) -> list[str]:
    """Intersect config enable-list with registered adapters (stable order)."""
    enabled: list[str] = []
    for source_id in settings.enabled_source_list:
        if source_id in _ADAPTERS:
            enabled.append(source_id)
    return enabled


def _adapter_meta(adapter: Any, settings: Settings, source_id: str) -> dict[str, str]:
    transport = str(getattr(adapter, "transport", "unknown"))
    default_interval = getattr(adapter, "default_min_interval_s", None)
    configured = settings.rate_limit_for(source_id)
    interval = (
        str(configured)
        if configured is not None
        else str(default_interval if default_interval is not None else settings.rate_limit_seconds)
    )
    return {
        "transport": transport,
        "interval_s": interval,
    }


def describe_sources(settings: Settings) -> list[dict[str, str]]:
    enabled = set(list_enabled(settings))
    rows: list[dict[str, str]] = []
    for source_id in registered_ids():
        adapter = get_adapter(source_id, settings)
        meta = _adapter_meta(adapter, settings, source_id)
        rows.append(
            {
                "id": source_id,
                "registered": "yes",
                "enabled": "yes" if source_id in enabled else "no",
                "transport": meta["transport"],
                "interval_s": meta["interval_s"],
            }
        )
    for source_id in settings.enabled_source_list:
        if source_id not in _ADAPTERS:
            rows.append(
                {
                    "id": source_id,
                    "registered": "no",
                    "enabled": "configured-but-missing",
                    "transport": "-",
                    "interval_s": str(settings.rate_limit_for(source_id)),
                }
            )
    return rows
