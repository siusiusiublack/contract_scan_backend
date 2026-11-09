from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class DocumentStub(BaseModel):
    """Lightweight search hit before full fetch."""

    source: str = "fcl"
    uri: str
    title: str
    url: str
    published: date | None = None
    summary: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class RawDocument(BaseModel):
    stub: DocumentStub
    content_type: str
    body: str
    fetched_at: datetime


class CleanDocument(BaseModel):
    doc_id: str
    source: str
    title: str
    court: str | None = None
    date: date | None = None
    url: str
    practice_area: list[str] = Field(default_factory=list)
    text: str
    content_hash: str
    license_note: str
    raw_path: str | None = None
    clean_path: str | None = None
    fetched_at: datetime
    neutral_citation: str | None = None
