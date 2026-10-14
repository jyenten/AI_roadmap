# AI Engineering Portfolio — Python, RAG & Retrieval Evaluation

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

**Important:** BM25 is implemented and tested as a retriever; it is **not yet an integrated selectable retrieval mode in the RAG API or existing evaluation CLI**. Comparison and hybrid retrieval are planned follow-up work.

## Engineering approach

I use the project to develop practical Python and software engineering skills while applying systematic testing. Core learning implementations are written by me; narrowly scoped tests and reviews may be delegated to AI coding assistants. Agent contributions are reviewed before integration.

Project guidance is documented in [AGENTS.md](AGENTS.md), with progress and skill evidence in [LEARNING_LOG.md](LEARNING_LOG.md).

## Repository layout

- [rag_api_project/](rag_api_project/) — active FastAPI, RAG, retrieval and evaluation work.
- .github/ — CI workflow configuration.
- [archive/](archive/) — 29 earlier programming and machine-learning exercise folders (`ALG/` and `den_1/` through `den_28_Docker/`), moved without altering their contents; preserved for learning history and reference.

## Next steps

- Integrate BM25 into the offline evaluation workflow and compare it with vector retrieval on development data.
- Experiment with hybrid lexical + semantic retrieval, measuring quality and latency.
- Improve reproducibility, dependency pinning, operational metrics and onboarding documentation.

## Getting started

Start with the [project README](rag_api_project/README.md) for setup, API examples, tests, Docker and evaluation commands.

> **Project status:** educational engineering portfolio / actively developed prototype, not a production SaaS or hosted demo.
