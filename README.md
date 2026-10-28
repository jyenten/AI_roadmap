<a id="top"></a>

# AI Engineering Portfolio — Python, RAG & Retrieval Evaluation

[Česky](docs/cs/README.md#cz) · [English](#en) · [Documentation](docs/README.md)

> **Documentation and agent rules:** All other Markdown documents live in [docs/](docs/README.md). Before changing files, read the [repository agent rules](docs/en/AGENTS.md) and, for RAG work, the [project agent rules](docs/en/PROJECT_AGENTS.md).

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**English**

- [Featured project: RAG API and document search](#en-featured-project-rag-api-and-document-search)
- [What is implemented](#en-what-is-implemented)
- [Verification](#en-verification)
- [Architecture at a glance](#en-architecture-at-a-glance)
- [Engineering approach](#en-engineering-approach)
- [Repository layout](#en-repository-layout)
- [Next steps](#en-next-steps)
- [Getting started](#en-getting-started)

</details>

---

<a id="en"></a>

An evolving, hands-on AI engineering project focused on building **testable retrieval systems** and understanding how they behave—not just calling an LLM API.

**Tech stack:** Python 3.11 · FastAPI · Pydantic · ChromaDB · Sentence Transformers · BM25 · Pytest · Docker · GitHub Actions


<a id="en-featured-project-rag-api-and-document-search"></a>

## Featured project: RAG API and document search

**[Explore the RAG API project](docs/en/PROJECT.md)**

The project processes technical PDF documentation into searchable chunks and provides a FastAPI question-answering workflow. In parallel, it develops standalone retrieval strategies and a reproducible offline evaluation framework.


<a id="en-what-is-implemented"></a>

### What is implemented

- **API:** FastAPI endpoints for health, readiness, statistics and questions; typed request/response models.
- **Document pipeline:** PDF text extraction, chunking, ChromaDB indexing and source/page/chunk metadata.
- **Retrieval:** vector retrieval with sentence embeddings, a separately tested BM25 lexical retriever, and an earlier RAG retrieval/reranking workflow.
- **Evaluation:** labeled question datasets, Hit@1/3/5/8, MRR, latency mean/p50/p95, JSONL evaluation history, dataset hashes and Git provenance.
- **Testing:** pytest unit and regression tests with synthetic fixtures and fake Chroma collections; GitHub Actions CI configuration.
- **Deployment tooling:** Dockerfile and Compose configuration for the API.


<a id="en-verification"></a>

### Verification

Historical *locally reported* full-suite run after BM25 integration: **210 passed, 1 skipped** (the skip was due to Windows symlink restrictions). This is not a current test count or a claim about GitHub Actions status; see the dated [verified checkpoint](docs/en/LEARNING_LOG.md#en-current-project-checkpoint) and verify new runs on [GitHub Actions](https://github.com/jyenten/AI_roadmap/actions).


<a id="en-architecture-at-a-glance"></a>

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


<a id="en-engineering-approach"></a>

## Engineering approach

This is a hands-on learning project developed with substantial AI assistance. I use ChatGPT and Codex for explanations, design discussions, code suggestions and generation, debugging, tests, and reviews. I also implement and modify code, investigate failures, and validate changes. The repository documents the development process and the resulting system; it is not a claim that every component was independently conceived or written by me.

Collaboration rules are documented at two levels: [repository-wide AGENTS.md](docs/en/AGENTS.md) defines the LEARN / IMPLEMENT / REVIEW modes and approval boundaries; [RAG project AGENTS.md](docs/en/PROJECT_AGENTS.md) adds safeguards for evaluation dataset curation. Progress and skill evidence are tracked in [LEARNING_LOG.md](docs/en/LEARNING_LOG.md).

For the BM25 milestone, Codex prepared regression tests in an **isolated local Git worktree** on `agent/bm25-tests`. The reviewed tests were then integrated into the public development branch.

For ongoing agent experiments, a **separate private GitHub repository** (`jyenten/AI_roadmap_codex_mirror`) mirrors an approved public snapshot. Its `main` branch is the mirror baseline, while `agent/bm25-tests` is reserved for Codex work. The private repository is not publicly accessible and **synchronization is manual**; Codex changes are not automatically published or merged without review.


<a id="en-repository-layout"></a>

## Repository layout

- [rag_api_project/](rag_api_project/) — active FastAPI, RAG, retrieval and evaluation work.
- [docs/](docs/README.md) — Czech/English guides, agent rules and the learning log.
- .github/ — CI workflow configuration.
- [archive/](archive/) — 29 earlier programming and machine-learning exercise folders (`ALG/` and `den_1/` through `den_28_Docker/`), moved without altering their contents; preserved for learning history and reference.


<a id="en-next-steps"></a>

## Next steps

- Preserve the measured BM25/Vector DEV and RANDOM baselines from Phase 3.4.
- Implement and evaluate hybrid lexical + semantic retrieval (RRF) without tuning on TEST.
- Improve reproducibility, dependency pinning, operational metrics and onboarding documentation.


<a id="en-getting-started"></a>

## Getting started

Start with the [project overview](docs/en/PROJECT.md) or [Czech project overview](docs/cs/PROJECT.md). Use the bilingual [operations runbook](docs/en/OPERATIONS.md) for setup/ingestion and the [golden evidence guide](docs/en/EVALUATION.md) for curation, validation, approvals and evaluation.

> **Project status:** educational engineering portfolio / actively developed prototype, not a production SaaS or hosted demo.

[↑ Nahoru / Back to top](#top)
