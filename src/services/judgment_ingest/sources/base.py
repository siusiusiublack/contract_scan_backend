from typing import Protocol

from judgment_ingest.models import CleanDocument, DocumentStub, RawDocument


class SourceAdapter(Protocol):
    """Swap Find Case Law for BAILII later without rewriting the pipeline."""

    source_id: str

    def search(self, query: str, limit: int) -> list[DocumentStub]:
        ...

    def fetch(self, stub: DocumentStub) -> RawDocument:
        ...

    def parse(self, raw: RawDocument) -> CleanDocument:
        ...
