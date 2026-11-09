# Contract Scan Backend

Multi-service Python monorepo for a UK **contract-risk** product (AST / tenancy beachhead).

## Services

| Category | Service | Status |
| :--- | :--- | :--- |
| **Data pipeline** | `judgment_ingest` | Find Case Law → EL-T land + SQLite |
| Product (later) | `contract_scanner` | Planned — AST risk checklist |
| Product (later) | `api` | Planned — FastAPI thin trigger |
| Enrich (later) | `judgment_ingest/enrich` | PII redaction / embeddings when coded |

Only create a new folder under `src/services/` when that service has real code.

## Layout (merged EL-T + multi-service)

```text
data/
  1_raw/<source>/          # Extract → Load RAW (immutable)
  2_processed/<source>/    # Transform output (JSON/txt)
  3_db/                    # Local SQLite (later Postgres/pgvector)

src/services/
  judgment_ingest/
    sources/               # EXTRACT per publisher (FCL Atom, BAILII later)
    pipeline/              # shared rate-limit, normalize, dedupe, run
    storage/               # writes 1_raw + 2_processed + DB
    enrich/                # later: PII / embed
  # contract_scanner/      # later
  # api/                   # later
```

EL-T flow: **sources Extract → `1_raw` → parse/transform → `2_processed` → `3_db`**.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
judgment-ingest --help
judgment-ingest sources
judgment-ingest status
judgment-ingest run --source fcl --limit 5 --dry-run
judgment-ingest run --source fcl --limit 3
```

Sources are pluggable via a registry (not limited to four publishers). See `docs/architecture.md`.

## Licensing note (Find Case Law)

Judgments on [Find Case Law](https://caselaw.nationalarchives.gov.uk/) are generally available under the Open Justice Licence for reading, sharing, and many commercial product uses. **Bulk computational analysis** (including building vector indexes / LLM pipelines over many records) may require a separate free licence from The National Archives. See `docs/licensing.md`.

## Disclaimer

This project provides **risk tooling and research infrastructure**, not formal legal advice.
