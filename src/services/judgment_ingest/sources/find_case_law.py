"""Find Case Law (National Archives) adapter.

Public endpoints (see TNA docs):
- GET /atom.xml?query=...
- GET /{uri}/data.xml
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from urllib.parse import urljoin

import httpx

from judgment_ingest.config import Settings
from judgment_ingest.models import CleanDocument, DocumentStub, RawDocument
from judgment_ingest.pipeline.normalize import assign_practice_areas, make_doc_id

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


class FindCaseLawAdapter:
    source_id = "fcl"

    def __init__(self, settings: Settings, client: httpx.Client | None = None) -> None:
        self.settings = settings
        self._client = client

    def _http(self) -> httpx.Client:
        if self._client is not None:
            return self._client
        return httpx.Client(
            base_url=self.settings.fcl_base_url,
            headers={
                "User-Agent": self.settings.user_agent,
                "Accept": "application/atom+xml, application/xml, text/xml, */*",
            },
            timeout=60.0,
        )

    def search(self, query: str, limit: int) -> list[DocumentStub]:
        """Search Atom feed. Raises if HTTP fails — caller handles errors."""
        owns_client = self._client is None
        client = self._http()
        try:
            response = client.get(
                "/atom.xml",
                params={"query": query, "order": "-date", "per_page": min(limit, 50)},
            )
            response.raise_for_status()
            return self._parse_atom(response.text, limit=limit)
        finally:
            if owns_client:
                client.close()

    def fetch(self, stub: DocumentStub) -> RawDocument:
        owns_client = self._client is None
        client = self._http()
        try:
            # Prefer /{uri}/data.xml when uri looks like a FCL path
            path = stub.extra.get("data_path") or f"/{stub.uri.strip('/')}/data.xml"
            response = client.get(path)
            response.raise_for_status()
            return RawDocument(
                stub=stub,
                content_type=response.headers.get("content-type", "application/xml"),
                body=response.text,
                fetched_at=datetime.now(timezone.utc),
            )
        finally:
            if owns_client:
                client.close()

    def parse(self, raw: RawDocument) -> CleanDocument:
        text = _xml_to_text(raw.body)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        practice = assign_practice_areas(raw.stub.title, text)
        return CleanDocument(
            doc_id=make_doc_id(self.source_id, raw.stub.uri),
            source=self.source_id,
            title=raw.stub.title,
            court=_extract_first(raw.body, ("court", "Court")),
            date=raw.stub.published,
            url=raw.stub.url,
            practice_area=practice,
            text=text,
            content_hash=content_hash,
            license_note=self.settings.license_note,
            fetched_at=raw.fetched_at,
            neutral_citation=raw.stub.extra.get("neutral_citation"),
        )

    def _parse_atom(self, xml_text: str, limit: int) -> list[DocumentStub]:
        root = ET.fromstring(xml_text)
        stubs: list[DocumentStub] = []
        for entry in root.findall("atom:entry", ATOM_NS):
            if len(stubs) >= limit:
                break
            title = _atom_text(entry.find("atom:title", ATOM_NS)) or "Untitled"
            entry_id = _atom_text(entry.find("atom:id", ATOM_NS)) or ""
            link = _best_link(entry)
            published = _parse_date(
                _atom_text(entry.find("atom:published", ATOM_NS))
                or _atom_text(entry.find("atom:updated", ATOM_NS))
            )
            summary = _atom_text(entry.find("atom:summary", ATOM_NS))
            uri = _uri_from_id_or_link(entry_id, link)
            url = link or urljoin(self.settings.fcl_base_url + "/", uri)
            stubs.append(
                DocumentStub(
                    source=self.source_id,
                    uri=uri,
                    title=title.strip(),
                    url=url,
                    published=published,
                    summary=summary,
                    extra={"data_path": f"/{uri.strip('/')}/data.xml" if uri else None},
                )
            )
        return stubs


def _atom_text(el: ET.Element | None) -> str | None:
    if el is None:
        return None
    return (el.text or "").strip() or None


def _best_link(entry: ET.Element) -> str | None:
    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href")
        if href:
            return href
    return None


def _uri_from_id_or_link(entry_id: str, link: str | None) -> str:
    # Atom id often looks like tag:... or a URL; prefer path-like segment
    for candidate in (entry_id, link or ""):
        if "caselaw.nationalarchives.gov.uk/" in candidate:
            return candidate.split("caselaw.nationalarchives.gov.uk/", 1)[1].strip("/")
        if re.match(r"^[a-z0-9_./-]+$", candidate, re.I) and "/" in candidate:
            return candidate.strip("/")
    return (entry_id or link or "unknown").strip("/")


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _extract_first(xml_text: str, tag_names: tuple[str, ...]) -> str | None:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None
    for el in root.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local in tag_names and (el.text or "").strip():
            return el.text.strip()
    return None


def _xml_to_text(xml_text: str) -> str:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return xml_text
    parts: list[str] = []
    for el in root.iter():
        if el.text and el.text.strip():
            parts.append(el.text.strip())
        if el.tail and el.tail.strip():
            parts.append(el.tail.strip())
    return "\n".join(parts)
