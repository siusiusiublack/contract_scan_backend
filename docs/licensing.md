# Find Case Law licensing notes

Source: [Find Case Law](https://caselaw.nationalarchives.gov.uk/) (The National Archives).

## Open Justice Licence

Most uses — reading, downloading, sharing, and incorporating judgments into commercial products — are covered by the Open Justice Licence. See TNA pages on [permissions and licensing](https://caselaw.nationalarchives.gov.uk/permissions-and-licensing).

## Computational analysis

Bulk programmatic analysis (text mining across many records, NLP, training, vector indexes for semantic search, LLM pipelines over the corpus) may require a **separate free licence**. Apply via The National Archives; see [when you need permission](https://caselaw.nationalarchives.gov.uk/when-you-need-permission).

## This project

- v0 uses small, housing-filtered ingest for product development.
- Each stored document keeps a `license_note` field.
- Before scaling corpus / embeddings in production, confirm whether a computational analysis licence is required for your use case (`caselawlicence@nationalarchives.gov.uk`).
