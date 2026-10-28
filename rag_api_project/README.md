# RAG API — Document Search & Retrieval Evaluation

[**Český návod / Czech guide**](README.cs.md) · [Bilingual operations](docs/OPERATIONS.md) · [Bilingual evaluation](docs/EVALUATION.md)

A Python/FastAPI project for answering questions about technical PDF documentation, focusing on retrieval quality, source traceability, and regression testing.

**Status:** actively developed educational prototype, not a production service. The existing `/ask` pipeline uses Chroma retrieval, context selection, reranking, and rule-based/model-generated responses. Separately, the repository includes a vector retriever, BM25 lexical retriever, and offline retrieval evaluation tools.

## Tech stack

Python 3.11 · FastAPI · Pydantic · ChromaDB · Sentence Transformers · `rank-bm25` · Transformers/PyTorch · pypdf · pytest · Docker · GitHub Actions.

## Architecture and modules

| Component | Path | Purpose |
| --- | --- | --- |
| HTTP API | `app/main.py` | `/`, `/health`, `/ready`, `/stats`, `/ask` |
| Configuration | `app/config.py` | Environment-based Pydantic settings |
| RAG orchestration | `app/rag.py` | Answers and supporting context |
| Existing retrieval pipeline | `app/retrieval.py` | Retrieval, context-line selection and reranking |
| Vector retrieval | `app/retrievers/vector.py` | Chroma vector baseline |
| BM25 retrieval | `app/retrievers/bm25.py` | Lexical ranking over Chroma chunks |
| PDF ingestion | `scripts/ingest.py` | Extract and index PDF text |
| PDF search CLI | `scripts/search_pdf.py` | Independent local BM25 page search |
| Retrieval evaluation | `evaluation/`, `scripts/evaluate_retrieval.py` | Rank-based quality, latency and provenance |
| Tests | `tests/` | Unit and regression tests |

### Data flow

~~~text
PDF documents --> text extraction / chunking --> ChromaDB + metadata
                                                   |
                   +-------------------------------+----------------------+
                   |                                                      |
             Existing RAG API                                     Retrieval experiments
          context -> answer -> sources                           vector and BM25 retrievers
                                                                  |
                                                          offline evaluation
                                                           MRR / Hit@K / latency
~~~

**Integration boundary:** BM25 is implemented and selectable in the **offline evaluation CLI** together with `legacy` and `vector`. The HTTP `/ask` API has not been switched to a BM25 or hybrid retrieval mode. Hybrid RRF is work in progress, not an established released feature.

## Key engineering decisions

- Indexed chunks carry source, physical PDF page, and chunk metadata for traceability.
- BM25 loads stored chunks in bounded batches, validates data consistency, filters non-matching documents, and breaks score ties using ascending chunk IDs.
- Vector search returns distance-like scores (lower typically closer); BM25 returns ranking scores (higher ranks first). Raw scores should not be compared directly.
- Evaluation is split into development, random-sample, and held-out test data, with dataset hashes and Git provenance.
- Model-based generation is a fallback to task-specific answer logic; the system is not a general-purpose, production-grade QA engine.

## Local setup

Run from `rag_api_project/` using Python 3.11.

**Windows PowerShell**

~~~powershell
python --version  # Must be 3.11.x.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
~~~

**macOS/Linux**

~~~bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
test -f .env || cp .env.example .env
~~~

Dependencies are currently unpinned; this is not yet a fully reproducible lockfile-based installation.

### Index local PDFs

Put technical PDF files in `data/` (ignored by Git), then run:

~~~bash
python -m scripts.ingest
~~~

The local Chroma collection is stored under `chroma_db/`. The example configuration uses the collection named `ospf`. **Warning: `scripts.ingest` deletes and recreates an existing collection with that name**, rather than incrementally updating it. Back up the index if it must be preserved. The API requires suitable indexed data to answer corpus-specific questions. Full procedure: [OPERATIONS.md](docs/OPERATIONS.md).

## Running the API

~~~bash
python -m uvicorn app.main:app --reload
~~~

Open `http://127.0.0.1:8000/docs` for interactive OpenAPI documentation.

- `GET /` and `GET /health` — liveness and environment information.
- `GET /ready` — verifies the RAG service is available; requires working corpus/configuration.
- `GET /stats` — reports collection information.
- `POST /ask` — accepts a JSON question and returns an answer with supporting context and source previews.

Example request:

~~~bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"How does OSPF select the router ID?"}'
~~~

On Windows PowerShell, use `Invoke-RestMethod` if shell-specific `curl` quoting differs:

~~~powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType 'application/json' -Body '{"question":"How does OSPF select the router ID?"}'
~~~

## Tests

From `rag_api_project/`:

~~~bash
python -m pytest -q tests
~~~

Historical **locally reported** full-suite run after Phase 3.3 BM25 integration: **210 passed, 1 skipped**. The skip was caused by unavailable Windows symlink privileges; external dependency deprecation warnings were reported. Remote CI results must be verified independently on the GitHub Actions tab.

BM25 tests use synthetic Chroma fixtures and cover pagination, ranking, deterministic tie-breaking, metadata alignment, invalid queries and records, and malformed batches.

## Offline retrieval evaluation

The framework reports MRR, Hit@1/3/5/8 and retrieval latency mean/p50/p95. Run metadata includes the dataset hash, Git commit and dirty-worktree state. Runtime evaluation results under `eval/results/` are excluded from version control.

Supported commands in the published evaluation CLI:

~~~bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
~~~

The CLI accepts `legacy`, `vector`, `bm25` and `dev`/`random`. It writes JSONL run history, so it is not read-only. The held-out TEST set is reserved for final assessment, not iterative tuning. See [EVALUATION.md](docs/EVALUATION.md) for evidence creation and comparison discipline.

## Standalone BM25 PDF search

A separate discovery CLI indexes local PDF pages:

~~~bash
python -m scripts.search_pdf "router ID" --top-k 5 --interactive
~~~

This tool reads PDF files in `data/` and is distinct from the Chroma-backed `BM25Retriever`.

## Docker and Compose

The repository contains a Dockerfile and `compose.yaml`:

~~~bash
docker compose up --build
docker compose down
~~~

Compose maps host port `8001` to container port `8000` and mounts local Chroma/model-cache directories. This is a local container configuration, not a hosted demo.

**Known limitations:** the image copies `app/` and `scripts/`, but omits `document_search/`, `evaluation/`, `eval/` and source PDFs. Compose does not pass the host `.env` into the container. Run ingestion and evaluation natively; the container API requires a compatible mounted index. See [OPERATIONS.md](docs/OPERATIONS.md) for configuration and packaging boundaries.

## Current limitations and next steps

- Preserve the measured Phase 3.4 BM25 vs. Vector DEV/RANDOM baseline (DEV MRR: 0.7171 vs 0.8321; RANDOM MRR: 0.8133 vs 0.6050).
- Experiment with hybrid lexical + semantic retrieval (RRF), based on measured results, without tuning on held-out TEST.
- Improve dependency pinning, Docker packaging coverage, and operational observability.
- Continue improving extraction robustness, error reporting and evaluation on unseen questions.

## AI-assisted development and contributor boundaries

This learning project uses ChatGPT and Codex for explanations, design, implementation assistance, debugging, tests, and review; not every component was independently conceived or written by the repository owner.

The [repository-level AGENTS.md](../AGENTS.md) describes LEARN, IMPLEMENT and REVIEW modes and requires human approval for integration. The [project-level AGENTS.md](AGENTS.md) adds specific rules for evaluation dataset curation, including human approval before promoting candidate questions. Skill evidence and progress are documented in [LEARNING_LOG.md](../LEARNING_LOG.md).

For the BM25 feature, Codex authored synthetic regression tests in an isolated **local** worktree (`agent/bm25-tests`); the reviewed tests were integrated into the public development branch alongside the BM25 implementation.

Ongoing Codex experiments use a separate **private GitHub mirror** (`jyenten/AI_roadmap_codex_mirror`). Its `main` holds an approved public snapshot and `agent/bm25-tests` provides an isolated remote branch for agent work. The original local worktree is separate from this new remote branch. Synchronization and integration are manual, subject to the approval rules in `AGENTS.md`.
