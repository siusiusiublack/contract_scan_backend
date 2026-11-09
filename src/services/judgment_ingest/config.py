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
    rate_limit_seconds: float = 1.0
    database_url: str = "sqlite:///data/db/judgment_ingest.sqlite"
    data_dir: Path = Path("data")
    default_queries: str = Field(
        default="tenancy deposit,possession landlord,Housing Act tenancy"
    )
    fcl_base_url: str = "https://caselaw.nationalarchives.gov.uk"
    license_note: str = (
        "Find Case Law / Open Justice Licence — computational analysis may need a "
        "separate National Archives licence. See docs/licensing.md."
    )

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def clean_dir(self) -> Path:
        return self.data_dir / "clean"

    @property
    def db_dir(self) -> Path:
        return self.data_dir / "db"

    @property
    def query_list(self) -> list[str]:
        return [q.strip() for q in self.default_queries.split(",") if q.strip()]


def get_settings() -> Settings:
    return Settings()
