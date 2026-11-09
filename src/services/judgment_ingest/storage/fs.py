from __future__ import annotations

import json
from pathlib import Path

from judgment_ingest.config import Settings
from judgment_ingest.models import CleanDocument


class FileStore:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def ensure_dirs(self) -> None:
        self.settings.raw_dir.mkdir(parents=True, exist_ok=True)
        self.settings.clean_dir.mkdir(parents=True, exist_ok=True)
        self.settings.db_dir.mkdir(parents=True, exist_ok=True)

    def write(self, doc: CleanDocument, *, raw_body: str) -> tuple[Path, Path]:
        self.ensure_dirs()
        safe_id = doc.doc_id.replace(":", "_").replace("/", "_")
        raw_path = self.settings.raw_dir / f"{safe_id}.xml"
        clean_json = self.settings.clean_dir / f"{safe_id}.json"
        clean_txt = self.settings.clean_dir / f"{safe_id}.txt"
        raw_path.write_text(raw_body, encoding="utf-8")
        clean_txt.write_text(doc.text, encoding="utf-8")
        payload = doc.model_dump(mode="json")
        clean_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return raw_path, clean_json
