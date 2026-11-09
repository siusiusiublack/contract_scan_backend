-- Reference DDL for judgment_ingest documents (SQLite v0).
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
