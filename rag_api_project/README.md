# RAG API — Document Search & Retrieval Evaluation

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

**Integration boundary:** BM25 is implemented and tested but is not yet selectable through `/ask` or the existing evaluation CLI. Hybrid search is planned, not implemented.

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
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
~~~

**macOS/Linux**

~~~bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
~~~

Dependencies are currently unpinned; this is not yet a fully reproducible lockfile-based installation.

### Index local PDFs

Put technical PDF files in `data/` (ignored by Git), then run:

~~~bash
python -m scripts.ingest
~~~

The local Chroma collection is stored under `chroma_db/`. The example configuration uses the collection named `ospf`. The API requires suitable indexed data to answer corpus-specific questions.

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

Most recent **locally reported** full-suite run after BM25 integration: **210 passed, 1 skipped**. The skip was caused by unavailable Windows symlink privileges; external dependency deprecation warnings were reported. Remote CI results must be verified independently on the GitHub Actions tab.

BM25 tests use synthetic Chroma fixtures and cover pagination, ranking, deterministic tie-breaking, metadata alignment, invalid queries and records, and malformed batches.

## Offline retrieval evaluation

The framework reports MRR, Hit@1/3/5/8 and retrieval latency mean/p50/p95. Run metadata includes the dataset hash, Git commit and dirty-worktree state. Runtime evaluation results under `eval/results/` are excluded from version control.

Supported commands in the currently published evaluation CLI:

~~~bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
~~~

The documented CLI version accepts `legacy` or `vector`, and `dev` or `random`. A BM25 CLI option and hybrid retrieval evaluation are follow-up work. The held-out TEST set is reserved for final assessment, not iterative tuning.

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

**Known limitation:** review the Docker build context and copied modules before relying on newer retrieval/evaluation functionality inside the image. The current Dockerfile copies `app/` and `scripts/` rather than every newer top-level package.

## Current limitations and next steps

- Evaluate BM25 and vector retrieval on development data; compare MRR, Hit@K and latency.
- Experiment with hybrid lexical + semantic retrieval, based on measured results.
- Improve dependency pinning, Docker packaging coverage, and operational observability.
- Continue improving extraction robustness, error reporting and evaluation on unseen questions.

The [repository's agent collaboration rules](../AGENTS.md) and [learning log](../LEARNING_LOG.md) explain how independent learning work is separated from delegated AI-assisted tests and reviews.
