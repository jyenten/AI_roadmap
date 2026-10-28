# AI Engineering Portfolio — Python, RAG & Retrieval Evaluation

[**Český návod / Czech guide**](README.cs.md)

An evolving, hands-on AI engineering project focused on building **testable retrieval systems** and understanding how they behave—not just calling an LLM API.

**Tech stack:** Python 3.11 · FastAPI · Pydantic · ChromaDB · Sentence Transformers · BM25 · Pytest · Docker · GitHub Actions

## Featured project: RAG API and document search

**[Explore the RAG API project](rag_api_project/README.md)**

The project processes technical PDF documentation into searchable chunks and provides a FastAPI question-answering workflow. In parallel, it develops standalone retrieval strategies and a reproducible offline evaluation framework.

### What is implemented

- **API:** FastAPI endpoints for health, readiness, statistics and questions; typed request/response models.
- **Document pipeline:** PDF text extraction, chunking, ChromaDB indexing and source/page/chunk metadata.
- **Retrieval:** vector retrieval with sentence embeddings, a separately tested BM25 lexical retriever, and an earlier RAG retrieval/reranking workflow.
- **Evaluation:** labeled question datasets, Hit@1/3/5/8, MRR, latency mean/p50/p95, JSONL evaluation history, dataset hashes and Git provenance.
- **Testing:** pytest unit and regression tests with synthetic fixtures and fake Chroma collections; GitHub Actions CI configuration.
- **Deployment tooling:** Dockerfile and Compose configuration for the API.

### Verification

Latest *locally reported* full-suite run after BM25 integration: **210 passed, 1 skipped** (the skip was due to Windows symlink restrictions). This is not a claim about GitHub Actions status; see the Actions tab for remote CI runs.

### Architecture at a glance

~~~text
Technical PDF files
        |
  PDF ingestion & chunking
        |
  ChromaDB + metadata
        |
        +------------------------+
        |                        |
  Vector retriever        BM25 lexical retriever
        |                        |
        +------- retrieval evaluation
                     (MRR, Hit@K, latency)

  Existing RAG context pipeline
        |
  Rule-based answers / fallback generation
        |
  FastAPI response with source metadata
~~~

**Integration status:** `legacy`, `vector` and `bm25` are selectable in the **offline evaluation CLI** (DEV/RANDOM). BM25 is **not** an established selectable mode in HTTP `/ask`. Hybrid RRF remains in development and must not be presented as completed.

## Engineering approach

This is a hands-on learning project developed with substantial AI assistance. I use ChatGPT and Codex for explanations, design discussions, code suggestions and generation, debugging, tests, and reviews. I also implement and modify code, investigate failures, and validate changes. The repository documents the development process and the resulting system; it is not a claim that every component was independently conceived or written by me.

Collaboration rules are documented at two levels: [repository-wide AGENTS.md](AGENTS.md) defines the LEARN / IMPLEMENT / REVIEW modes and approval boundaries; [RAG project AGENTS.md](rag_api_project/AGENTS.md) adds safeguards for evaluation dataset curation. Progress and skill evidence are tracked in [LEARNING_LOG.md](LEARNING_LOG.md).

For the BM25 milestone, Codex prepared regression tests in an **isolated local Git worktree** on `agent/bm25-tests`. The reviewed tests were then integrated into the public development branch.

For ongoing agent experiments, a **separate private GitHub repository** (`jyenten/AI_roadmap_codex_mirror`) mirrors an approved public snapshot. Its `main` branch is the mirror baseline, while `agent/bm25-tests` is reserved for Codex work. The private repository is not publicly accessible and **synchronization is manual**; Codex changes are not automatically published or merged without review.

## Repository layout

- [rag_api_project/](rag_api_project/) — active FastAPI, RAG, retrieval and evaluation work.
- .github/ — CI workflow configuration.
- [archive/](archive/) — 29 earlier programming and machine-learning exercise folders (`ALG/` and `den_1/` through `den_28_Docker/`), moved without altering their contents; preserved for learning history and reference.

## Next steps

- Preserve the measured BM25/Vector DEV and RANDOM baselines from Phase 3.4.
- Implement and evaluate hybrid lexical + semantic retrieval (RRF) without tuning on TEST.
- Improve reproducibility, dependency pinning, operational metrics and onboarding documentation.

## Getting started

Start with the [project README](rag_api_project/README.md) or [Czech project README](rag_api_project/README.cs.md). Use the bilingual [operations runbook](rag_api_project/docs/OPERATIONS.md) for setup/ingestion and the [golden evidence guide](rag_api_project/docs/EVALUATION.md) for curation, validation, approvals and evaluation.

> **Project status:** educational engineering portfolio / actively developed prototype, not a production SaaS or hosted demo.
