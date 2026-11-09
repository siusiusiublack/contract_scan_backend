from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JUDGMENT_INGEST_",
        env_file=".env",
        extra="ignore",
    )

    user_agent: str = (
        "ContractScanBot/0.1 (+https://github.com/siusiusiublack/contract_scan_backend)"
    )
    # Global fallback when a source has no dedicated interval.
    rate_limit_seconds: float = 1.0
    fcl_rate_limit_seconds: float = 1.0
    # Conservative default for future BAILII HTML adapter (no public rate docs).
    bailii_rate_limit_seconds: float = 3.0
    database_url: str = "sqlite:///data/3_db/judgment_ingest.sqlite"
    data_dir: Path = Path("data")
    default_queries: str = Field(
        default="tenancy deposit,possession landlord,Housing Act tenancy"
    )
    # Comma-separated source ids to run for --source all (must also be registered).
    enabled_sources: str = Field(default="fcl")
    fcl_base_url: str = "https://caselaw.nationalarchives.gov.uk"
    license_note: str = (
        "Find Case Law / Open Justice Licence — computational analysis may need a "
        "separate National Archives licence. See docs/licensing.md."
    )

    @property
    def raw_root(self) -> Path:
        """EL-T stage 1: immutable raw landing zone."""
        return self.data_dir / "1_raw"

    @property
    def processed_root(self) -> Path:
        """EL-T stage 2: transformed clean JSON/txt."""
        return self.data_dir / "2_processed"

    @property
    def db_dir(self) -> Path:
        """EL-T stage 3: local SQLite (later Postgres/pgvector)."""
        return self.data_dir / "3_db"

    # Back-compat aliases used by older call sites / status output.
    @property
    def raw_dir(self) -> Path:
        return self.raw_root

    @property
    def clean_dir(self) -> Path:
        return self.processed_root

    def raw_dir_for(self, source_id: str) -> Path:
        return self.raw_root / source_id

    def processed_dir_for(self, source_id: str) -> Path:
        return self.processed_root / source_id

    @property
    def query_list(self) -> list[str]:
        return [q.strip() for q in self.default_queries.split(",") if q.strip()]

    @property
    def enabled_source_list(self) -> list[str]:
        return [s.strip() for s in self.enabled_sources.split(",") if s.strip()]

    def rate_limit_for(self, source_id: str) -> float:
        """Per-source polite interval; falls back to global then 1.0s."""
        dedicated = {
            "fcl": self.fcl_rate_limit_seconds,
            "bailii": self.bailii_rate_limit_seconds,
        }
        if source_id in dedicated:
            return float(dedicated[source_id])
        return float(self.rate_limit_seconds)


def get_settings() -> Settings:
    return Settings()
