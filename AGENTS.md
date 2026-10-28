
# AI Roadmap — Agent Collaboration Rules

## Objectives

This repository serves two purposes:

1. Build reliable, maintainable AI/RAG applications.
2. Develop the human owner's independent Python,
   software engineering and AI engineering skills.

Learning quality must not be sacrificed for coding speed.

## Collaboration modes

### LEARN — default

Use for new concepts, algorithms and engineering skills.

- Explain the problem and expected behavior first.
- Let the owner design and implement core learning logic.
- Provide focused guidance rather than immediate solutions.
- Implement supporting code or tests when authorized.
- Review the owner's implementation.
- Include a practical understanding check.

### IMPLEMENT — explicit delegation

Use when the owner delegates a bounded implementation task.

- Respect approved files and acceptance criteria.
- Write idiomatic, maintainable Python.
- Include meaningful regression tests.
- Preserve existing interfaces and user changes.
- Avoid unrelated refactoring and overengineering.
- Do not commit, push or merge without approval.

### REVIEW — audit

- Prefer read-only inspection.
- Identify concrete defects and reproducible scenarios.
- Distinguish verified bugs from potential risks.
- Recommend minimal fixes and regression tests.
- Do not modify files unless authorized.

## Engineering workflow

Follow:

Complete -> Measure -> Improve

- Keep modules cohesive and responsibilities clear.
- Test functionality, edge cases and data integrity.
- Never weaken tests merely to obtain a passing result.
- Preserve evaluation reproducibility.
- Do not access secrets or private data outside task scope.
- Respect nested AGENTS.md files.
- Never use git add . for automatic staging.

## Learning governance

Maintain LEARNING_LOG.md.

- Suggest updates after meaningful milestones.
- Distinguish completed project work from demonstrated skills.
- Never mark a skill as mastered without practical evidence.
- Prefer independent exercises and debugging tasks.
- Do not alter learning assessments without human approval.

## Completion report

For implementation work, report:

1. Files changed.
2. Tests executed and results.
3. Important design decisions.
4. Remaining limitations.
5. Concepts the owner should understand.

The human owner approves final integration and commits.
## Operational documentation and safety

For work inside `rag_api_project/`, read the project [README](rag_api_project/README.md), [operations runbook](rag_api_project/docs/OPERATIONS.md) and [evaluation guide](rag_api_project/docs/EVALUATION.md) as applicable. The English and Czech instructions must describe the same implemented behavior.

- Inspect the actual CLI and source code before documenting commands; never invent flags, paths or completed features.
- Treat `python -m scripts.ingest` as **destructive**: it deletes and recreates an existing named Chroma collection. Never launch it or replace a user's local index without explicit authorization.
- Do not expose or commit source PDFs, `.env`, private corpora, model caches or local Chroma data.
- Do not modify golden evidence, benchmark metrics or protected evaluation datasets to raise a retrieval score.
- Preserve DEV/RANDOM baselines and the independence of held-out TEST; report dataset hash, Git provenance and configuration when claiming a comparison.
- Keep documentation-only edits separate from validator fixes and dependency/version updates where practical.
- In REVIEW mode, report verified defects separately from risks; do not modify files unless the owner approved the change.
