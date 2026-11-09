from __future__ import annotations

import json
from pathlib import Path

from judgment_ingest.config import Settings
from judgment_ingest.models import CleanDocument


class FileStore:
    """EL-T file landing: 1_raw/<source>/ then 2_processed/<source>/."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def ensure_dirs(self, source_id: str | None = None) -> None:
        self.settings.db_dir.mkdir(parents=True, exist_ok=True)
        sources = (
            [source_id]
            if source_id
            else list(dict.fromkeys([*self.settings.enabled_source_list, "fcl", "bailii"]))
        )
        for sid in sources:
            self.settings.raw_dir_for(sid).mkdir(parents=True, exist_ok=True)
            self.settings.processed_dir_for(sid).mkdir(parents=True, exist_ok=True)

    def write(self, doc: CleanDocument, *, raw_body: str) -> tuple[Path, Path]:
        source_id = doc.source or "unknown"
        self.ensure_dirs(source_id)
        safe_id = doc.doc_id.replace(":", "_").replace("/", "_")
        ext = ".html" if source_id == "bailii" else ".xml"
        raw_path = self.settings.raw_dir_for(source_id) / f"{safe_id}{ext}"
        clean_json = self.settings.processed_dir_for(source_id) / f"{safe_id}.json"
        clean_txt = self.settings.processed_dir_for(source_id) / f"{safe_id}.txt"
        raw_path.write_text(raw_body, encoding="utf-8")
        clean_txt.write_text(doc.text, encoding="utf-8")
        payload = doc.model_dump(mode="json")
        clean_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return raw_path, clean_json
