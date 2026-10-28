# Agent Instructions

## Evaluation dataset curation

When working on evaluation dataset generation or curation:

- Follow `docs/EVAL_CURATOR_AGENT.md`.
- Write generated evaluation candidates only to `eval/candidates/`.
- Never modify:
  - `eval/dev_questions.json`
  - `eval/random_questions.json`
  - `eval/test_questions.json`
  - retrieval implementation
  - evaluation metrics
- Never promote candidates automatically.
- Human approval is required before promotion.
- Every candidate batch must pass:

  python -m scripts.validate_eval_candidates <candidate-file>

- Do not weaken or bypass validation to make a candidate pass.
- Gold evidence must come only from local PDFs in `data/`.
- Use physical PDF page numbers.
- Use evidence -> question methodology.
## Operational and evaluation procedures

Use [OPERATIONS.md](docs/OPERATIONS.md) for the **English/Czech** setup, ingestion, API, Docker and test commands, and [EVALUATION.md](docs/EVALUATION.md) for golden evidence, metrics, validation and human-approved promotion. These documents explain procedures; this file sets agent permissions.

- Before suggesting or running ingest, inspect `scripts/ingest.py` and the selected corpus/collection. Ingest currently **deletes and recreates** the collection. Never run destructive ingest without explicit authorization and a backup decision.
- In evidence curation, retain the source-PDF-only, physical-page and evidence-first rules above. Candidate validation does **not** authorize candidate promotion.
- Never use held-out `eval/test_questions.json` to tune or repeatedly inspect retrieval errors.
- Never overwrite existing DEV/RANDOM/TEST gold evidence, metrics or baseline history as an automatic way to improve results.
- When changing evaluation validation code, add regression tests (including multiple evidence pages) and review the protected-file CI governance policy.
- Do not change `requirements.txt`, lockfiles, architecture or retrieval parameters merely to update documentation. Keep English and Czech usage instructions synchronized.
