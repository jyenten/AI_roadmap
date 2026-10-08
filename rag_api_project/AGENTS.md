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