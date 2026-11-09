"""Skip documents already stored by url or content_hash."""

from __future__ import annotations

from judgment_ingest.models import CleanDocument
from judgment_ingest.storage.db import DocumentRepository


def should_skip(repo: DocumentRepository, doc: CleanDocument) -> tuple[bool, str]:
    if repo.exists_url(doc.url):
        return True, "duplicate_url"
    if repo.exists_hash(doc.content_hash):
        return True, "duplicate_hash"
    return False, "new"
