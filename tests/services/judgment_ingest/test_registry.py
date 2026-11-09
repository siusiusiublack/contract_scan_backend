from judgment_ingest.config import Settings
from judgment_ingest.sources.find_case_law import FindCaseLawAdapter
from judgment_ingest.sources.registry import (
    describe_sources,
    get_adapter,
    list_enabled,
    registered_ids,
)


def test_fcl_registered() -> None:
    assert "fcl" in registered_ids()


def test_get_adapter_fcl() -> None:
    settings = Settings()
    adapter = get_adapter("fcl", settings)
    assert isinstance(adapter, FindCaseLawAdapter)
    assert adapter.source_id == "fcl"
    assert adapter.transport == "atom_api"
    assert adapter.default_min_interval_s == 1.0


def test_get_adapter_unknown() -> None:
    settings = Settings()
    try:
        get_adapter("nope", settings)
        assert False, "expected KeyError"
    except KeyError as exc:
        assert "nope" in str(exc)


def test_enabled_intersection() -> None:
    settings = Settings(enabled_sources="fcl,ghost")
    assert list_enabled(settings) == ["fcl"]
    rows = describe_sources(settings)
    by_id = {r["id"]: r for r in rows}
    assert by_id["fcl"]["enabled"] == "yes"
    assert by_id["fcl"]["transport"] == "atom_api"
    assert by_id["fcl"]["interval_s"] == "1.0"
    assert by_id["ghost"]["registered"] == "no"


def test_per_source_rate_limits() -> None:
    settings = Settings(
        fcl_rate_limit_seconds=1.5,
        bailii_rate_limit_seconds=4.0,
        rate_limit_seconds=9.0,
    )
    assert settings.rate_limit_for("fcl") == 1.5
    assert settings.rate_limit_for("bailii") == 4.0
    assert settings.rate_limit_for("other") == 9.0
