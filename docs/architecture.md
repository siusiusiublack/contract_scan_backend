# Architecture

## Multi-service monorepo

```text
src/services/
  judgment_ingest/     # data pipeline (now)
  # contract_scanner/  # product (later — create when coding)
  # api/
  # rag_worker/
```

## Judgment ingest flow

```text
CLI run
  → sources/find_case_law (Atom search + data.xml)
  → pipeline/fetch (rate limit, retry)
  → adapter.parse + pipeline/parse cleanup
  → pipeline/normalize (housing practice_area)
  → pipeline/dedupe (url / content_hash)
  → storage/fs (raw + clean) + storage/db (SQLite)
```

## Design rules

- One service folder only when it has behaviour.
- Inner layers: `sources` / `pipeline` / `storage`.
- Category “data pipeline” is documented in README — not an extra parent folder.
