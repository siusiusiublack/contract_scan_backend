# Contract Scan Backend

Multi-service Python monorepo for a UK **contract-risk** product (AST / tenancy beachhead).

## Services

| Category | Service | Status |
| :--- | :--- | :--- |
| **Data pipeline** | `judgment_ingest` | v0 scaffold — Find Case Law → raw/clean + DB |
| Product (later) | `contract_scanner` | Planned — AST risk checklist |
| Product (later) | `api` | Planned — FastAPI demo surface |
| Workers (later) | `rag_worker` | Planned — chunk / embed / cite |

Only create a new folder under `src/services/` when that service has real code.

## Layout

```text
src/services/
  judgment_ingest/
    sources/      # Find Case Law adapter (extensible protocol)
    pipeline/     # fetch → parse → normalize → dedupe
    storage/      # raw/clean files + SQLite
data/             # local artefacts (gitignored payloads)
docs/             # architecture + licensing notes
```

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
judgment-ingest --help
judgment-ingest status
# Later: judgment-ingest run --source fcl --limit 5
```

## Licensing note (Find Case Law)

Judgments on [Find Case Law](https://caselaw.nationalarchives.gov.uk/) are generally available under the Open Justice Licence for reading, sharing, and many commercial product uses. **Bulk computational analysis** (including building vector indexes / LLM pipelines over many records) may require a separate free licence from The National Archives. See `docs/licensing.md`.

## Disclaimer

This project provides **risk tooling and research infrastructure**, not formal legal advice.
