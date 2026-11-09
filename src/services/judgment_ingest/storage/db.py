from __future__ import annotations

import sqlite3
from pathlib import Path

from judgment_ingest.config import Settings
from judgment_ingest.models import CleanDocument

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    court TEXT,
    date TEXT,
    url TEXT NOT NULL UNIQUE,
    practice_area TEXT,
    text TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    license_note TEXT,
    raw_path TEXT,
    clean_path TEXT,
    fetched_at TEXT NOT NULL,
    neutral_citation TEXT
);
CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(content_hash);
CREATE INDEX IF NOT EXISTS idx_documents_practice ON documents(practice_area);
"""


class DocumentRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._path = self._sqlite_path(settings.database_url)

    @staticmethod
    def _sqlite_path(database_url: str) -> Path:
        prefix = "sqlite:///"
        if not database_url.startswith(prefix):
            raise ValueError("v0 only supports sqlite:/// paths")
        return Path(database_url.removeprefix(prefix))

    def connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def count(self) -> int:
        with self.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()
            return int(row["c"]) if row else 0

    def exists_url(self, url: str) -> bool:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM documents WHERE url = ? LIMIT 1", (url,)
            ).fetchone()
            return row is not None

    def exists_hash(self, content_hash: str) -> bool:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM documents WHERE content_hash = ? LIMIT 1",
                (content_hash,),
            ).fetchone()
            return row is not None

    def upsert(self, doc: CleanDocument) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO documents (
                    doc_id, source, title, court, date, url, practice_area, text,
                    content_hash, license_note, raw_path, clean_path, fetched_at,
                    neutral_citation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(doc_id) DO UPDATE SET
                    title=excluded.title,
                    text=excluded.text,
                    content_hash=excluded.content_hash,
                    practice_area=excluded.practice_area,
                    raw_path=excluded.raw_path,
                    clean_path=excluded.clean_path,
                    fetched_at=excluded.fetched_at
                """,
                (
                    doc.doc_id,
                    doc.source,
                    doc.title,
                    doc.court,
                    doc.date.isoformat() if doc.date else None,
                    doc.url,
                    ",".join(doc.practice_area),
                    doc.text,
                    doc.content_hash,
                    doc.license_note,
                    doc.raw_path,
                    doc.clean_path,
                    doc.fetched_at.isoformat(),
                    doc.neutral_citation,
                ),
            )
