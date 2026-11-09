import datetime as dt
from datetime import timezone

from judgment_ingest.config import Settings
from judgment_ingest.models import CleanDocument
from judgment_ingest.pipeline.dedupe import should_skip
from judgment_ingest.storage.db import DocumentRepository


def _doc(url: str, content_hash: str) -> CleanDocument:
    return CleanDocument(
        doc_id=f"fcl:{content_hash[:8]}",
        source="fcl",
        title="Test",
        url=url,
        text="hello",
        content_hash=content_hash,
        license_note="test",
        fetched_at=dt.datetime.now(timezone.utc),
        practice_area=["housing"],
    )


def test_dedupe_by_url(tmp_path) -> None:
    db_path = tmp_path / "t.sqlite"
    settings = Settings(database_url=f"sqlite:///{db_path.as_posix()}", data_dir=tmp_path)
    repo = DocumentRepository(settings)
    repo.ensure_schema()
    first = _doc("https://example.com/a", "hash1")
    repo.upsert(first)
    skip, reason = should_skip(repo, _doc("https://example.com/a", "hash2"))
    assert skip is True
    assert reason == "duplicate_url"
