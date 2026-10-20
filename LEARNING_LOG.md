
# AI Engineering — Learning Log

## Goal

Develop independent proficiency in:

- Python programming
- Software architecture and testing
- Git, CI/CD and Docker
- RAG systems and information retrieval
- AI evaluation and observability
- AI agents and agent-assisted development

## Skill levels

- NOT ASSESSED — no independent demonstration yet
- GUIDED — completed with explanations or assistance
- INDEPENDENT — implemented and explained without assistance
- PROFICIENT — independently applied in a different problem

A completed project feature does not automatically
mean the corresponding skill is mastered.

## Current project checkpoint

Date: 2026-10-12
Branch: document-search-bm25
Commit: 9ed9985

Completed in the project:

- FastAPI RAG foundation
- PDF processing and Chroma vector storage
- Vector retrieval baseline
- Evaluation datasets and retrieval metrics
- DEV / RANDOM / held-out TEST separation
- Retrieval latency measurement
- JSONL evaluation history
- Git provenance checks
- Automated testing and GitHub CI

Last verified full test suite:
142 passed, 1 skipped.

These are project achievements, not independent
skill assessments.

## Active learning: Phase 3.3 — BM25

Topic:
Lexical retrieval over existing Chroma chunks.

Learning objectives:

- Explain how BM25 ranks documents.
- Understand tokenization, TF, IDF and document length.
- Implement retrieval ranking in Python.
- Preserve source and page metadata.
- Write meaningful unit and integration tests.
- Compare BM25 with vector retrieval.

Independent exercise:

Implement BM25Retriever.search() and explain the
ranking and tie-breaking behavior.

Current skill assessment:
NOT ASSESSED

## Learning entry template

### YYYY-MM-DD — Topic

What I worked on:
-

Concepts I learned:
-

What I implemented independently:
-

What Codex or ChatGPT implemented:
-

Problems I diagnosed:
-

Tests and evidence:
-

Skill level:
NOT ASSESSED / GUIDED / INDEPENDENT / PROFICIENT

Next exercise:
-

## Learning rules

Update this log after meaningful milestones,
not after every small code change.

Record difficulties and misunderstandings.
Do not inflate skill assessments.
Revisit weak topics through independent exercises.


### 2026-10-13 — Phase 3.3: BM25 Retriever

**Project milestone:** Completed

- Implemented `BM25Retriever` over existing Chroma chunks with guided learning.
- Implemented corpus loading, validation, tokenization, lexical matching, ranking and top-k selection.
- Codex independently prepared regression tests.
- Tests passed code review and were integrated.
- Full regression: 210 passed, 1 skipped, 2 warnings.
- Commit: `c101680` (pushed to origin/document-search-bm25).

**Learning evidence:**

- Practiced Python collections, list comprehensions, `enumerate()`, `sorted()`, `lambda` and data validation.
- Practiced distinguishing document indices from relevance scores.
- Understood the purpose of deterministic tie-breaking and lexical filtering.
- Required guidance and corrections during implementation.

**Skill assessment:** GUIDED

**Next independent exercise:** Explain and modify retrieval ranking without step-by-step assistance.

**Next project milestone:** BM25 vs. Vector evaluation on DEV, followed by RANDOM.

### 2026-10-20 — Phase 3.4: Retrieval Evaluation

**Project milestone:** Completed

- Integrated BM25 into the evaluation CLI using a retriever registry.
- Extended parametrized CLI tests for legacy, vector and BM25.
- Full regression suite passed.
- Evaluated BM25 and Vector on DEV (20 questions)
  and RANDOM (25 questions).
- Preserved the held-out TEST dataset.

**Baseline MRR:**

- DEV: BM25 0.7171, Vector 0.8321
- RANDOM: BM25 0.8133, Vector 0.6050

**Learning evidence:**

- Practiced dictionary lookup and registry pattern.
- Practiced exception chaining with `raise ... from exc`.
- Practiced `getattr()`, parametrized pytest tests
  and debugging `KeyError` and `ImportError`.
- Required guidance during implementation.

**Skill assessment:** GUIDED

**Next project milestone:** Hybrid retrieval using RRF.