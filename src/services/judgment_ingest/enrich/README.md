# enrich (reserved)

Optional post-`2_processed` transforms before vector load.

Planned modules (create only when implementing):

- `pii_redactor.py` — redact personal data before embeddings
- `embedder.py` — chunk + embed for pgvector

The EL-T path remains: `1_raw` → parse → `2_processed` → (optional enrich) → DB / vectors.
