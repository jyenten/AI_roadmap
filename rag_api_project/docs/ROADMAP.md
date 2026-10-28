<a id="top"></a>

# AI RAG Project Roadmap

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Stavový přehled — 2026-10-28](#cz-stavový-přehled--2026-10-28)
- [Aktuální zaměření vývoje](#cz-aktuální-zaměření-vývoje)
- [Jak číst a aktualizovat schválený plán](#cz-jak-číst-a-aktualizovat-schválený-plán)
- [FÁZE 1 - Funkční kostra RAG](#cz-fáze-1---funkční-kostra-rag)
- [FÁZE 2 - Základ evaluace](#cz-fáze-2---základ-evaluace)
- [FÁZE 2A - Univerzální průzkumník dokumentů](#cz-fáze-2a---univerzální-průzkumník-dokumentů)
- [FÁZE 2A.0 - Zmrazení architektury](#cz-fáze-2a0---zmrazení-architektury)
- [FÁZE 2A.1 - Datové modely](#cz-fáze-2a1---datové-modely)
- [FÁZE 2A.2 - Zpracování textu](#cz-fáze-2a2---zpracování-textu)
- [FÁZE 2A.3 - Základy bezpečnosti](#cz-fáze-2a3---základy-bezpečnosti)
- [FÁZE 2A.4 - Načítání PDF a validace PDF](#cz-fáze-2a4---načítání-pdf-a-validace-pdf)
- [FÁZE 2A.5 - BM25 index](#cz-fáze-2a5---bm25-index)
- [FÁZE 2A.6 - Vyhledávací modul](#cz-fáze-2a6---vyhledávací-modul)
- [FÁZE 2A.7 - CLI](#cz-fáze-2a7---cli)
- [FÁZE 2A.8 - Integrace](#cz-fáze-2a8---integrace)
- [FÁZE 2B - Evaluační datové modely](#cz-fáze-2b---evaluační-datové-modely)
- [FÁZE 2C - Metriky retrievalu](#cz-fáze-2c---metriky-retrievalu)
- [FÁZE 2D - Evaluační runner a historie](#cz-fáze-2d---evaluační-runner-a-historie)
- [FÁZE 2E - Evaluace RANDOM](#cz-fáze-2e---evaluace-random)
- [FÁZE 2F - Kompletní evaluační dataset](#cz-fáze-2f---kompletní-evaluační-dataset)
- [FÁZE 3 - Refaktoring retrievalu](#cz-fáze-3---refaktoring-retrievalu)
- [FÁZE 3.1 - Retrieval modely](#cz-fáze-31---retrieval-modely)
- [FÁZE 3.2 - Embeddingy](#cz-fáze-32---embeddingy)
- [FÁZE 3.3 - Vektorové vyhledávání](#cz-fáze-33---vektorové-vyhledávání)
- [FÁZE 3.4 - Zpracování dotazu](#cz-fáze-34---zpracování-dotazu)
- [FÁZE 3.5 - Reranker](#cz-fáze-35---reranker)
- [FÁZE 3.6 - Skórování](#cz-fáze-36---skórování)
- [FÁZE 3.7 - Retrieval služba](#cz-fáze-37---retrieval-služba)
- [FÁZE 4 - Zodolnění API](#cz-fáze-4---zodolnění-api)
- [FÁZE 4.1 - Životní cyklus aplikace](#cz-fáze-41---životní-cyklus-aplikace)
- [FÁZE 4.2 - Routy](#cz-fáze-42---routy)
- [FÁZE 4.3 - Vkládání závislostí](#cz-fáze-43---vkládání-závislostí)
- [FÁZE 4.4 - Chyby](#cz-fáze-44---chyby)
- [FÁZE 4.5 - Middleware](#cz-fáze-45---middleware)
- [FÁZE 5 - Produkční inženýrství](#cz-fáze-5---produkční-inženýrství)
- [FÁZE 5.1 - Linux / WSL2](#cz-fáze-51---linux--wsl2)
- [FÁZE 5.2 - Strukturované logování](#cz-fáze-52---strukturované-logování)
- [FÁZE 5.3 - Běhové metriky](#cz-fáze-53---běhové-metriky)
- [FÁZE 5.4 - Zodolnění Dockeru](#cz-fáze-54---zodolnění-dockeru)
- [FÁZE 5.5 - CI/CD](#cz-fáze-55---cicd)
- [FÁZE 6 - Bezpečnost](#cz-fáze-6---bezpečnost)
- [FÁZE 6.1 - Modelování hrozeb](#cz-fáze-61---modelování-hrozeb)
- [FÁZE 6.2 - Validace běhových vstupů](#cz-fáze-62---validace-běhových-vstupů)
- [FÁZE 6.3 - Běhové limity](#cz-fáze-63---běhové-limity)
- [FÁZE 6.4 - Tajemství](#cz-fáze-64---tajemství)
- [FÁZE 6.5 - Bezpečnost závislostí](#cz-fáze-65---bezpečnost-závislostí)
- [FÁZE 6.6 - Bezpečnost kontejneru](#cz-fáze-66---bezpečnost-kontejneru)
- [FÁZE 6.7 - Bezpečnost HTTP](#cz-fáze-67---bezpečnost-http)
- [FÁZE 6.8 - Bezpečnost specifická pro RAG](#cz-fáze-68---bezpečnost-specifická-pro-rag)
- [FÁZE 7 - Produkční verze v1](#cz-fáze-7---produkční-verze-v1)
- [FÁZE 7.1 - Health a readiness](#cz-fáze-71---health-a-readiness)
- [FÁZE 7.2 - Produkční smoke test](#cz-fáze-72---produkční-smoke-test)
- [FÁZE 7.3 - Dokumentace](#cz-fáze-73---dokumentace)
- [FÁZE 8 - Rozšíření](#cz-fáze-8---rozšíření)
- [FÁZE 8A - Průzkum agentů](#cz-fáze-8a---průzkum-agentů)
- [FÁZE 8B - SQL a ETL](#cz-fáze-8b---sql-a-etl)
- [FÁZE 8C - MLOps](#cz-fáze-8c---mlops)
- [FÁZE 8D - Pokročilí agenti](#cz-fáze-8d---pokročilí-agenti)
- [Původní plánovací odhady — historické](#cz-původní-plánovací-odhady--historické)
- [Historie plánování](#cz-historie-plánování)

**English**

- [Status snapshot — 2026-10-28](#en-status-snapshot--2026-10-28)
- [Current development focus](#en-current-development-focus)
- [Reading and updating the approved plan](#en-reading-and-updating-the-approved-plan)
- [PHASE 1 - Functional RAG Skeleton](#en-phase-1---functional-rag-skeleton)
- [PHASE 2 - Evaluation Foundation](#en-phase-2---evaluation-foundation)
- [PHASE 2A - Universal Document Explorer](#en-phase-2a---universal-document-explorer)
- [PHASE 2A.0 - Architecture Freeze](#en-phase-2a0---architecture-freeze)
- [PHASE 2A.1 - Data Models](#en-phase-2a1---data-models)
- [PHASE 2A.2 - Text Processing](#en-phase-2a2---text-processing)
- [PHASE 2A.3 - Security Foundations](#en-phase-2a3---security-foundations)
- [PHASE 2A.4 - PDF Loading and PDF Validation](#en-phase-2a4---pdf-loading-and-pdf-validation)
- [PHASE 2A.5 - BM25 Index](#en-phase-2a5---bm25-index)
- [PHASE 2A.6 - Search Engine](#en-phase-2a6---search-engine)
- [PHASE 2A.7 - CLI](#en-phase-2a7---cli)
- [PHASE 2A.8 - Integration](#en-phase-2a8---integration)
- [PHASE 2B - Evaluation Data Models](#en-phase-2b---evaluation-data-models)
- [PHASE 2C - Retrieval Metrics](#en-phase-2c---retrieval-metrics)
- [PHASE 2D - Evaluation Runner and History](#en-phase-2d---evaluation-runner-and-history)
- [PHASE 2E - RANDOM Evaluation](#en-phase-2e---random-evaluation)
- [PHASE 2F - Complete Evaluation Dataset](#en-phase-2f---complete-evaluation-dataset)
- [PHASE 3 - Retrieval Refactor](#en-phase-3---retrieval-refactor)
- [PHASE 3.1 - Retrieval Models](#en-phase-31---retrieval-models)
- [PHASE 3.2 - Embeddings](#en-phase-32---embeddings)
- [PHASE 3.3 - Vector Search](#en-phase-33---vector-search)
- [PHASE 3.4 - Query Processing](#en-phase-34---query-processing)
- [PHASE 3.5 - Reranker](#en-phase-35---reranker)
- [PHASE 3.6 - Scoring](#en-phase-36---scoring)
- [PHASE 3.7 - Retrieval Service](#en-phase-37---retrieval-service)
- [PHASE 4 - API Hardening](#en-phase-4---api-hardening)
- [PHASE 4.1 - Application Lifecycle](#en-phase-41---application-lifecycle)
- [PHASE 4.2 - Routes](#en-phase-42---routes)
- [PHASE 4.3 - Dependency Injection](#en-phase-43---dependency-injection)
- [PHASE 4.4 - Errors](#en-phase-44---errors)
- [PHASE 4.5 - Middleware](#en-phase-45---middleware)
- [PHASE 5 - Production Engineering](#en-phase-5---production-engineering)
- [PHASE 5.1 - Linux / WSL2](#en-phase-51---linux--wsl2)
- [PHASE 5.2 - Structured Logging](#en-phase-52---structured-logging)
- [PHASE 5.3 - Runtime Metrics](#en-phase-53---runtime-metrics)
- [PHASE 5.4 - Docker Hardening](#en-phase-54---docker-hardening)
- [PHASE 5.5 - CI/CD](#en-phase-55---cicd)
- [PHASE 6 - Security](#en-phase-6---security)
- [PHASE 6.1 - Threat Modeling](#en-phase-61---threat-modeling)
- [PHASE 6.2 - Runtime Input Validation](#en-phase-62---runtime-input-validation)
- [PHASE 6.3 - Runtime Limits](#en-phase-63---runtime-limits)
- [PHASE 6.4 - Secrets](#en-phase-64---secrets)
- [PHASE 6.5 - Dependency Security](#en-phase-65---dependency-security)
- [PHASE 6.6 - Container Security](#en-phase-66---container-security)
- [PHASE 6.7 - HTTP Security](#en-phase-67---http-security)
- [PHASE 6.8 - RAG-Specific Security](#en-phase-68---rag-specific-security)
- [PHASE 7 - Production v1](#en-phase-7---production-v1)
- [PHASE 7.1 - Health and Readiness](#en-phase-71---health-and-readiness)
- [PHASE 7.2 - Production Smoke Test](#en-phase-72---production-smoke-test)
- [PHASE 7.3 - Documentation](#en-phase-73---documentation)
- [PHASE 8 - Expansion](#en-phase-8---expansion)
- [PHASE 8A - Agent Exploration](#en-phase-8a---agent-exploration)
- [PHASE 8B - SQL and ETL](#en-phase-8b---sql-and-etl)
- [PHASE 8C - MLOps](#en-phase-8c---mlops)
- [PHASE 8D - Advanced Agents](#en-phase-8d---advanced-agents)
- [Original planning estimates — historical](#en-original-planning-estimates--historical)
- [Planning history](#en-planning-history)

</details>

---

<a id="en"></a>
## EN — English

This document owns **what to build, phase order, goals and acceptance criteria**.
Use [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for how to implement/review work,
[ARCHITECTURE.md](ARCHITECTURE.md) for component boundaries and
[LEARNING_LOG.md](../../LEARNING_LOG.md) for dated work and learning evidence.


[↑ Obsah / Contents](#obsah)

<a id="en-status-snapshot--2026-10-28"></a>

## Status snapshot — 2026-10-28

This is the current planning checkpoint, not a renumbering or replacement of the
approved phase specifications below. Completion of a milestone does not certify
all acceptance criteria of its broader phase or production readiness.

| Milestone | Observed status | Evidence / procedure |
| --- | --- | --- |
| RAG API, PDF ingestion and Chroma storage | Implemented prototype; hardening remains planned | [Project README](../README.md), [architecture](ARCHITECTURE.md) |
| Independent PDF page explorer | Implemented | `document_search/`, [operations](OPERATIONS.md) |
| Evidence-based retrieval evaluation | Implemented: metrics, history, latency and provenance | `evaluation/`, [evaluation guide](EVALUATION.md) |
| Chunk-level BM25 and Vector comparison | Implemented in the offline CLI on DEV/RANDOM | `app/retrievers/`, [recorded milestones](../../LEARNING_LOG.md#project-and-learning-history) |
| Hybrid lexical/semantic retrieval with RRF | Local work in progress; not a published CLI/API mode | [Uncommitted-work record](../../LEARNING_LOG.md#uncommitted-work-observed-on-2026-10-28) |
| Held-out TEST evaluation | Reserved for final assessment, not iterative tuning | [Evaluation policy](EVALUATION.md) |
| Bilingual runbooks and validator regressions | Integrated through [PR #3](https://github.com/jyenten/AI_roadmap/pull/3) | [Operations](OPERATIONS.md), [evaluation](EVALUATION.md) |
| Dependency/security automation | Enabled; ChromaDB dependency findings remain open | `.github/workflows/`, [current project checkpoint](../../LEARNING_LOG.md#current-project-checkpoint) |

Detailed results and historical MRR/Hit@K belong to the evaluation guide and
learning log; this roadmap does not maintain a second benchmark table.


[↑ Obsah / Contents](#obsah)

<a id="en-current-development-focus"></a>

## Current development focus

The next recorded development milestone is hybrid BM25 + Vector retrieval with
RRF. Complete and review the implementation, then measure DEV/RANDOM against the
preserved baselines before deciding on improvements. Keep TEST held out.
Separate local/backend experiments and unmerged dependency proposals remain
subject to their own review; their presence is not integration into `main` or
approval to replace the retrieval architecture.

The learning journal historically used labels such as Phase 3.3 for BM25,
Phase 3.4 for retrieval evaluation and Phase 3.5 for hybrid RRF. Those journal
labels are **not IDs in this roadmap**. Here, the original phase numbers and
names remain authoritative: 3.3 Vector Search, 3.4 Query Processing and
3.5 Reranker. Use the full milestone name when referring to journal work.


[↑ Obsah / Contents](#obsah)

<a id="en-reading-and-updating-the-approved-plan"></a>

## Reading and updating the approved plan

The phase specifications below preserve the approved order, planned modules,
learning concepts and Definition of Done checklists. Their original **Status**,
estimates and unchecked boxes are a planning baseline, not a second live status
tracker. Use the snapshot above for observed progress; do not infer that an
existing module is missing just because an original checkbox remains unchecked.
Do not mark acceptance criteria satisfied without the necessary evidence.

The working method is **Complete → Measure → Improve**. Shared scope, backlog,
freeze, testing and review rules live in the
[development workflow](DEVELOPMENT_GUIDE.md#development-workflow), not here.
Changes to phase goals, priorities or acceptance criteria require an explicit
planning decision; editorial cleanup does not authorize them.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-1---functional-rag-skeleton"></a>

# PHASE 1 - Functional RAG Skeleton

**Status:** Mostly complete

**Estimated remaining work:** 2-4 hours

## Goal

Maintain a working end-to-end RAG application.

Core runtime pipeline:

```text
PDF documents
    ->
ingestion
    ->
text preprocessing
    ->
chunking
    ->
embeddings
    ->
ChromaDB
    ->
retrieval
    ->
reranking
    ->
context construction
    ->
generation
    ->
FastAPI response
```

The purpose of PHASE 1 is not architectural perfection.

The purpose is a working system that can later be measured and improved.

---

## 1.1 `app/config.py`

### Responsibilities

- application configuration
- model names
- Chroma collection configuration
- retrieval limits
- generation limits
- environment configuration

### Important concepts

- centralized configuration
- environment variables
- configuration validation
- Pydantic Settings

### Future direction

Configuration should eventually be loaded through a validated settings
object rather than duplicated constants.

Possible public access:

```python
get_settings()
```

---

## 1.2 `app/schemas.py`

### Current models

- `QuestionRequest`
- `SourceChunk`
- `AnswerResponse`

### Future possible models

- `ErrorResponse`
- `HealthResponse`

### Important concept

API schemas describe data crossing the HTTP boundary.

They should remain separate from internal retrieval models.

---

## 1.3 `app/retrieval.py`

### Current responsibilities

- embedding model loading
- query preparation
- Chroma retrieval
- candidate selection
- CrossEncoder reranking
- heuristic scoring
- result selection

### Current technical debt

This module currently contains multiple responsibilities and
domain-specific logic.

That is intentionally not refactored during PHASE 1.

Major retrieval refactoring belongs to:

```text
PHASE 3
```

---

## 1.4 `app/generation.py`

### Main responsibilities

- generator model loading
- prompt construction
- model inference
- answer generation

Core flow:

```text
question
+
retrieved context
    ->
prompt
    ->
generation model
    ->
answer
```

Possible future separation:

```text
prompt construction
model inference
output processing
```

This split should only be introduced if complexity requires it.

---

## 1.5 `app/rag.py`

### Responsibility

RAG orchestration.

Target conceptual flow:

```text
question
    ->
retrieval
    ->
context selection
    ->
generation
    ->
sources
    ->
final response
```

### Current technical debt

The current implementation contains OSPF-specific behavior.

Removal belongs to:

```text
PHASE 3
```

---

## 1.6 `app/main.py`

### Responsibility

FastAPI application entry point.

Current endpoints:

```text
GET /
GET /health
POST /ask
```

Target responsibility:

```text
HTTP request
    ->
validation
    ->
application service
    ->
HTTP response
```

Business logic should eventually move out of the API entry point.

---

## 1.7 `scripts/ingest.py`

### Current pipeline

```text
PDF
    ->
extract text
    ->
clean text
    ->
chunk
    ->
embed
    ->
store in ChromaDB
```

### Existing improvements

- PDF text cleanup
- URL protection/restoration
- word-based chunking
- chunk overlap
- overlap validation

### Important rule

Do not refactor ingestion only for architectural symmetry.

Refactor it only when:

- testing becomes difficult
- reuse is required
- complexity grows significantly
- evaluation exposes an ingestion problem

---

## PHASE 1 Definition of Done

- [x] PDF documents can be ingested
- [x] text extraction works
- [x] chunking works
- [x] embeddings can be generated
- [x] ChromaDB stores searchable chunks
- [x] retrieval works
- [x] reranking works
- [x] generation works
- [x] `POST /ask` works
- [x] responses contain source information
- [x] smoke tests pass
- [ ] remaining technical debt is documented

When these conditions are satisfied, PHASE 1 is frozen.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2---evaluation-foundation"></a>

# PHASE 2 - Evaluation Foundation

**Status:** In progress

**Estimated remaining work:** 8-12 hours

## Goal

Create a reliable evaluation framework before major retrieval changes.

Retrieval should no longer be improved only by inspecting a few manually
selected questions.

Target development flow:

```text
baseline
    ->
evaluation
    ->
retrieval change
    ->
evaluation
    ->
comparison
```

---

## Evaluation Dataset Roles

Three dataset categories have intentionally different purposes.

### DEV

Used during development and tuning.

DEV results may influence implementation decisions.

Target size:

```text
approximately 20 manually validated questions
```

---

### RANDOM

Used for:

- robustness exploration
- unexpected failure discovery
- corpus coverage exploration

Random sampling must be reproducible through a stored seed.

RANDOM is not a replacement for TEST.

---

### TEST

Held-out final evaluation.

TEST should not be repeatedly inspected and tuned against.

Its purpose is to estimate generalization after tuning is complete.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a---universal-document-explorer"></a>

# PHASE 2A - Universal Document Explorer

**Status:** Current active subphase

**Estimated work:** 3-4 hours

## Goal

Build a reusable, domain-independent lexical corpus explorer used for:

- finding candidate evidence
- inspecting PDF content
- manually validating gold evidence
- helping construct DEV / RANDOM / TEST datasets

The explorer must continue to work if the entire PDF corpus is replaced.

Example future domains:

```text
Kubernetes
cybersecurity
Linux
law
manufacturing
accounting
networking
```

The explorer must not contain OSPF-specific ranking logic.

---

## Target Structure

```text
document_search/
|
+-- __init__.py
+-- models.py
+-- normalize.py
+-- tokenize.py
+-- load_pages.py
+-- build_index.py
+-- search.py
|
+-- security/
    +-- __init__.py
    +-- paths.py
    +-- pdf_validation.py
    +-- input_validation.py
```

CLI:

```text
scripts/
+-- search_pdf.py
```

Tests:

```text
tests/
+-- document_search/
    +-- test_models.py
    +-- test_normalize.py
    +-- test_tokenize.py
    +-- test_load_pages.py
    +-- test_build_index.py
    +-- test_search.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a0---architecture-freeze"></a>

# PHASE 2A.0 - Architecture Freeze

## Goal

Before implementation, define:

- module responsibilities
- data models
- public interfaces
- dependency direction
- security boundaries
- Definition of Done

Documentation:

```text
docs/ROADMAP.md
docs/ARCHITECTURE.md
docs/DEVELOPMENT_GUIDE.md
```

No production code should be redesigned repeatedly while dependent modules
are already being implemented unless a concrete technical issue requires
it.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a1---data-models"></a>

# PHASE 2A.1 - Data Models

## File

```text
document_search/models.py
```

## Planned models

```python
PageDocument
SearchResult
BM25SearchIndex
```

### `PageDocument`

Conceptually:

```python
PageDocument(
    source="manual.pdf",
    page=26,
    text="...",
)
```

Represents one searchable source page.

---

### `SearchResult`

Conceptually:

```python
SearchResult(
    document=document,
    score=12.5,
)
```

Represents one ranked BM25 result.

---

### `BM25SearchIndex`

Owns:

```text
page corpus
+
BM25 model
```

This prevents callers from manually keeping those objects synchronized.

---

## New Concept - Immutable Dataclasses

Preferred pattern:

```python
@dataclass(frozen=True)
```

Benefits:

- prevents accidental mutation
- improves reasoning about state
- makes tests more predictable
- clearly represents factual data

Examples of immutable facts:

```text
source filename
page number
document text
completed search score
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a2---text-processing"></a>

# PHASE 2A.2 - Text Processing

**Estimated work:** less than 1 hour

Because these modules are small and closely related, they may be
implemented together.

---

## File

```text
document_search/normalize.py
```

Main function:

```python
normalize_text(
    text: str,
) -> str
```

Responsibilities:

- lowercase normalization
- whitespace normalization
- generic text cleanup

Must not contain:

```text
OSPF terminology
Cisco rules
manual ranking boosts
domain-specific vocabulary
```

---

## File

```text
document_search/tokenize.py
```

Main function:

```python
tokenize(
    text: str,
) -> list[str]
```

Example:

```text
"OSPF calculates interface cost."
```

becomes approximately:

```python
[
    "ospf",
    "calculates",
    "interface",
    "cost",
]
```

---

## Important Concepts

- pure functions
- deterministic preprocessing
- reusable text processing
- separation between normalization and retrieval

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a3---security-foundations"></a>

# PHASE 2A.3 - Security Foundations

**Estimated work:** approximately 1 hour

## Goal

Protect filesystem and user-controlled search inputs before PDF parsing
and ranking.

---

## File

```text
document_search/security/paths.py
```

Planned functions:

```python
resolve_safe_path(...)
validate_data_directory(...)
```

Responsibilities:

- allowed directory boundaries
- path traversal prevention
- resolved path validation
- symlink-aware checks

---

## New Concept - Path Traversal

Unsafe input example:

```text
../../private_file
```

A path that appears to be inside a directory may also resolve outside it
through a symbolic link.

Security therefore must validate resolved filesystem paths, not only the
original input string.

---

## File

```text
document_search/security/input_validation.py
```

Planned functions:

```python
validate_query(...)
validate_top_k(...)
```

Responsibilities:

- reject empty queries
- reject oversized queries
- reject invalid `top_k`
- prevent unreasonable resource requests

---

## New Concept - Validation Boundary

External input should be validated near the system boundary.

Internal functions can then operate on values that already satisfy the
expected contract.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a4---pdf-loading-and-pdf-validation"></a>

# PHASE 2A.4 - PDF Loading and PDF Validation

**Estimated work:** 1-2 hours

## File

```text
document_search/security/pdf_validation.py
```

Planned functions:

```python
validate_pdf_extension(...)
validate_pdf_signature(...)
validate_pdf_limits(...)
```

Responsibilities:

- verify `.pdf` extension
- verify that the file actually looks like a PDF
- enforce file size limits
- enforce page count limits

---

## New Concept - File Signature

A filename such as:

```text
document.pdf
```

does not prove that the file is actually a PDF.

Validation should inspect the file header/signature as well as the file
extension.

---

## New Concept - Resource Exhaustion

A valid-looking file may still consume unreasonable resources.

Examples:

```text
multi-gigabyte file
hundreds of thousands of pages
extremely large extracted text
```

Resource limits protect:

- RAM
- CPU
- latency
- service availability

---

## File

```text
document_search/load_pages.py
```

Main function:

```python
load_pdf_pages(
    data_dir: Path,
) -> list[PageDocument]
```

Core flow:

```text
data directory
    ->
discover PDF files
    ->
security validation
    ->
PdfReader
    ->
extract each page
    ->
PageDocument
```

Important rule:

The loader must not silently truncate documents.

If a file cannot be processed safely or completely, failure should be
explicit.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a5---bm25-index"></a>

# PHASE 2A.5 - BM25 Index

**Estimated work:** less than 1 hour

## File

```text
document_search/build_index.py
```

Main function:

```python
build_bm25_index(
    pages: list[PageDocument],
) -> BM25SearchIndex
```

External dependency:

```text
rank-bm25
```

---

## New Concept - BM25

BM25 is a standard lexical information retrieval algorithm.

It considers:

- term frequency
- inverse document frequency
- document length normalization

Conceptually:

```text
query terms
    +
how often they appear in a page
    +
how rare they are across the corpus
    +
page/document length
    ->
relevance score
```

This is preferable to hand-written ranking such as:

```text
neighbor = +1
DROTHER = +5
distance below 200 chars = +3
```

because BM25 ranking is derived from corpus statistics rather than
domain-specific manual heuristics.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a6---search-engine"></a>

# PHASE 2A.6 - Search Engine

**Estimated work:** approximately 1 hour

## File

```text
document_search/search.py
```

Public function:

```python
search_pages(
    index: BM25SearchIndex,
    query: str,
    top_k: int = 10,
) -> list[SearchResult]
```

Core flow:

```text
query
    ->
validation
    ->
tokenization
    ->
BM25 scores
    ->
descending ranking
    ->
TOP K
    ->
SearchResult
```

---

## Important New Concept - Public API Boundary

Other modules should use:

```python
search_pages(...)
```

without manually accessing:

```text
BM25 internals
page arrays
raw score arrays
sorting logic
```

This allows internal implementation to change without changing every
caller.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a7---cli"></a>

# PHASE 2A.7 - CLI

**Estimated work:** less than 1 hour

## File

```text
scripts/search_pdf.py
```

Planned functions:

```python
build_parser()
print_results()
select_result()
print_result_detail()
main()
```

Target usage:

```text
python -m scripts.search_pdf "how does OSPF calculate interface cost"
```

Optional:

```text
--top-k 5
```

The CLI should contain:

- argument parsing
- human-readable output
- interactive selection

It should not contain:

- BM25 implementation
- PDF parsing internals
- ranking heuristics

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2a8---integration"></a>

# PHASE 2A.8 - Integration

## Tasks

- add `rank-bm25` dependency
- run document-search unit tests
- run full project tests
- search real Cisco corpus
- inspect several result rankings manually
- verify generic behavior
- confirm no OSPF-specific ranking rules remain

---

## PHASE 2A Definition of Done

- [ ] arbitrary PDFs can be discovered
- [ ] filesystem boundaries are validated
- [ ] PDF extension is validated
- [ ] PDF signature is validated
- [ ] PDF resource limits exist
- [ ] pages are represented by typed data models
- [ ] normalization is domain-independent
- [ ] tokenization works
- [ ] BM25 index can be created
- [ ] arbitrary text queries can be ranked
- [ ] results expose source, page, score, and text
- [ ] CLI works
- [ ] relevant unit tests pass
- [ ] complete project tests pass
- [ ] no OSPF-specific ranking heuristics exist

Once these conditions are satisfied, PHASE 2A is frozen.

Out of scope:

```text
fuzzy retrieval
semantic document explorer
LLM reranking
query rewriting
synonym dictionaries
hybrid BM25 + embedding explorer
advanced UI
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2b---evaluation-data-models"></a>

# PHASE 2B - Evaluation Data Models

**Estimated work:** 1-2 hours

## Goal

Move reusable evaluation logic out of loose scripts and dictionaries into
typed project modules.

Target structure:

```text
evaluation/
|
+-- __init__.py
+-- models.py
+-- dataset.py
+-- evidence.py
+-- metrics.py
+-- runner.py
+-- history.py
+-- random_eval.py
```

---

## File

```text
evaluation/models.py
```

Planned models:

```python
GoldEvidence
EvaluationQuestion
QuestionResult
EvaluationMetrics
EvaluationRun
```

---

## New Concept - Typed Evaluation Models

Instead of:

```python
question["gold_evidence"][0]["source"]
```

prefer:

```python
question.gold_evidence
```

Benefits:

- clearer code
- better IDE support
- fewer key-name errors
- easier validation
- safer refactoring

---

## File

```text
evaluation/dataset.py
```

Planned functions:

```python
load_dataset(...)
validate_dataset(...)
calculate_dataset_hash(...)
```

Responsibilities:

- load DEV / TEST datasets
- schema validation
- dataset identity
- reproducibility

---

## New Concept - Dataset Hashing

A SHA256 hash can identify the exact dataset version used for an
evaluation run.

This prevents ambiguity such as:

```text
"MRR was 0.82 on the DEV dataset"
```

when the DEV dataset may have changed since the run.

Instead:

```text
dataset_hash = abc123...
MRR = 0.82
```

---

## File

```text
evaluation/evidence.py
```

Planned functions:

```python
normalize_evidence_text(...)
matches_gold_evidence(...)
find_gold_rank(...)
```

A valid evidence match should require:

```text
source
AND
page
AND
expected text fragment
```

within the same accepted evidence variant.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2c---retrieval-metrics"></a>

# PHASE 2C - Retrieval Metrics

**Estimated work:** approximately 1 hour

## File

```text
evaluation/metrics.py
```

Planned functions:

```python
reciprocal_rank(...)
mean_reciprocal_rank(...)
hit_at_k(...)
aggregate_metrics(...)
```

---

## Metric - Hit@K

Question:

```text
Did the correct evidence appear in the first K results?
```

Examples:

```text
Hit@1
Hit@3
Hit@5
Hit@8
```

---

## Metric - Reciprocal Rank

If correct evidence appears at:

```text
rank 1 -> 1.0
rank 2 -> 0.5
rank 4 -> 0.25
```

Formula conceptually:

```text
1 / rank
```

---

## Metric - MRR

Mean Reciprocal Rank:

```text
average reciprocal rank
across all evaluation questions
```

MRR rewards systems that place relevant evidence near the top of the
ranking.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2d---evaluation-runner-and-history"></a>

# PHASE 2D - Evaluation Runner and History

**Estimated work:** approximately 1 hour

## File

```text
evaluation/runner.py
```

Planned functions:

```python
evaluate_question(...)
evaluate_dataset(...)
build_run_metadata(...)
```

Conceptual flow:

```text
EvaluationQuestion
    ->
retrieval
    ->
ranked results
    ->
gold evidence matching
    ->
question metrics
```

---

## File

```text
evaluation/history.py
```

Planned functions:

```python
load_history(...)
append_run(...)
save_history(...)
```

Stored metadata should include:

- Git commit SHA
- dirty working-tree state
- dataset SHA256
- timestamp
- configuration
- evaluation metrics

Example:

```text
commit A
MRR = 0.71

commit B
MRR = 0.82
```

This allows retrieval changes to be compared with evidence.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2e---random-evaluation"></a>

# PHASE 2E - RANDOM Evaluation

**Estimated work:** 2-3 hours

## File

```text
evaluation/random_eval.py
```

Possible functions:

```python
sample_pages(...)
build_random_sample(...)
save_seed(...)
```

---

## New Concept - Reproducible Randomness

Use a dedicated seeded random generator.

Example:

```python
random.Random(seed)
```

The same seed should produce the same sample.

This allows a surprising RANDOM failure to be reproduced later.

---

## RANDOM Purpose

RANDOM is intended for:

```text
robustness
coverage
failure discovery
```

It is not intended for:

```text
final generalization claims
```

That remains the role of TEST.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-2f---complete-evaluation-dataset"></a>

# PHASE 2F - Complete Evaluation Dataset

**Estimated work:** included in PHASE 2 estimate

## Tasks

- expand DEV to approximately 20 questions
- manually validate gold evidence
- diversify question topics
- implement RANDOM workflow
- create TEST dataset
- freeze TEST dataset
- document dataset roles

---

## PHASE 2 Definition of Done

- [ ] universal BM25 document explorer complete
- [ ] DEV dataset sufficiently broad
- [ ] DEV gold evidence manually validated
- [ ] RANDOM workflow implemented
- [ ] RANDOM runs reproducible
- [ ] TEST dataset created
- [ ] TEST dataset frozen
- [ ] MRR implemented
- [ ] Hit@1 implemented
- [ ] Hit@3 implemented
- [ ] Hit@5 implemented
- [ ] Hit@8 implemented
- [ ] dataset hashing implemented
- [ ] Git metadata recorded
- [ ] evaluation history available
- [ ] evaluation tests pass

After PHASE 2, evaluation infrastructure is frozen unless a concrete
measurement problem appears.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-3---retrieval-refactor"></a>

# PHASE 3 - Retrieval Refactor

**Status:** Planned

**Estimated work:** 8-14 hours

## Goal

Refactor the main RAG retrieval system only after reliable evaluation is
available.

Current large module:

```text
app/retrieval.py
```

Target structure:

```text
app/
+-- retrieval/
    +-- __init__.py
    +-- models.py
    +-- embeddings.py
    +-- vector_search.py
    +-- query.py
    +-- reranker.py
    +-- scoring.py
    +-- service.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-31---retrieval-models"></a>

# PHASE 3.1 - Retrieval Models

## File

```text
app/retrieval/models.py
```

Planned models:

```python
RetrievedChunk
ScoredChunk
RetrievalResult
```

Purpose:

replace loosely structured dictionaries/tuples with explicit internal
retrieval data types.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-32---embeddings"></a>

# PHASE 3.2 - Embeddings

## File

```text
app/retrieval/embeddings.py
```

Planned functions:

```python
load_embedding_model(...)
embed_query(...)
embed_documents(...)
```

Responsibility:

embedding operations only.

Must not:

- communicate with FastAPI
- decide ranking
- format API responses

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-33---vector-search"></a>

# PHASE 3.3 - Vector Search

## File

```text
app/retrieval/vector_search.py
```

Planned functions:

```python
search_vector_store(...)
convert_chroma_results(...)
```

Responsibility:

communication with ChromaDB.

Important architectural rule:

Higher layers should not depend directly on Chroma's response structure.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-34---query-processing"></a>

# PHASE 3.4 - Query Processing

## File

```text
app/retrieval/query.py
```

Possible function:

```python
normalize_query(...)
```

Potential future query expansion is allowed only if DEV evaluation shows
a measurable benefit.

Domain-specific hardcoding should be removed.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-35---reranker"></a>

# PHASE 3.5 - Reranker

## File

```text
app/retrieval/reranker.py
```

Planned functions:

```python
load_reranker(...)
rerank(...)
```

Core flow:

```text
query
+
candidate chunk
    ->
CrossEncoder
    ->
relevance score
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-36---scoring"></a>

# PHASE 3.6 - Scoring

## File

```text
app/retrieval/scoring.py
```

Goal:

remove pathological score combinations.

Current known issue:

```text
raw CrossEncoder score
+
large heuristic bonus
```

can cause the heuristic scale to dominate model relevance.

Possible approaches to evaluate:

- pure CrossEncoder ranking
- normalized score combination
- rank fusion

Choice must be driven by DEV metrics.

---

## New Concept - Rank Fusion

Instead of directly adding incompatible raw scores, ranking systems may
combine relative rank positions.

This avoids some score-scale problems.

It should only be introduced if evaluation justifies it.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-37---retrieval-service"></a>

# PHASE 3.7 - Retrieval Service

## File

```text
app/retrieval/service.py
```

Target public API:

```python
retrieve(
    query: str,
) -> list[RetrievalResult]
```

Pipeline:

```text
query
    ->
vector search
    ->
candidate set
    ->
reranking
    ->
score handling
    ->
TOP K
```

Higher-level code should primarily call this public interface.

---

## PHASE 3 Definition of Done

- [ ] OSPF-specific retrieval hardcoding removed
- [ ] retrieval data models exist
- [ ] embedding responsibility separated
- [ ] Chroma responsibility separated
- [ ] reranking separated
- [ ] scoring isolated
- [ ] stable retrieval public API exists
- [ ] baseline metrics recorded
- [ ] refactored retrieval evaluated on DEV
- [ ] retrieval regression tests pass
- [ ] TEST is not used during tuning
- [ ] final TEST run performed after tuning

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-4---api-hardening"></a>

# PHASE 4 - API Hardening

**Status:** Planned

**Estimated work:** 5-8 hours

## Goal

Turn the existing FastAPI wrapper into a more production-like application
boundary.

Target structure:

```text
app/
|
+-- main.py
+-- lifecycle.py
|
+-- api/
    +-- __init__.py
    +-- routes.py
    +-- dependencies.py
    +-- errors.py
    +-- middleware.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-41---application-lifecycle"></a>

# PHASE 4.1 - Application Lifecycle

## File

```text
app/lifecycle.py
```

Main function:

```python
lifespan(...)
```

Responsibilities:

```text
startup
->
load models
load vector store
initialize services

shutdown
->
release resources
```

---

## New Concept - FastAPI Lifespan

Expensive models should normally be initialized once during application
startup rather than independently for every request.

Benefits:

- lower latency
- lower memory overhead
- clearer resource lifecycle
- easier startup failure detection

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-42---routes"></a>

# PHASE 4.2 - Routes

## File

```text
app/api/routes.py
```

Responsibilities:

```text
GET /health
POST /ask
```

Routes translate:

```text
HTTP
<->
application services
```

They should not contain retrieval implementation.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-43---dependency-injection"></a>

# PHASE 4.3 - Dependency Injection

## File

```text
app/api/dependencies.py
```

Possible functions:

```python
get_settings(...)
get_rag_service(...)
```

---

## New Concept - Dependency Injection

Instead of creating dependencies inside every endpoint, FastAPI can
provide them.

Benefits:

- easier testing
- reduced global state
- replaceable services
- clearer ownership

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-44---errors"></a>

# PHASE 4.4 - Errors

## File

```text
app/api/errors.py
```

Possible exceptions:

```python
InvalidQueryError
RetrievalError
GenerationError
```

Also:

```text
FastAPI exception handlers
```

Goal:

convert internal failures into controlled structured HTTP responses.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-45---middleware"></a>

# PHASE 4.5 - Middleware

## File

```text
app/api/middleware.py
```

Responsibilities may include:

- request ID
- request timing
- basic HTTP logging

---

## PHASE 4 Definition of Done

- [ ] models initialize once
- [ ] application lifecycle defined
- [ ] routes separated from business logic
- [ ] dependency injection used where appropriate
- [ ] structured application errors exist
- [ ] request IDs exist
- [ ] API timing available
- [ ] health endpoint defined
- [ ] readiness semantics defined
- [ ] API integration tests pass

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-5---production-engineering"></a>

# PHASE 5 - Production Engineering

**Status:** Planned

**Estimated work:** 10-16 hours

## Goal

Make the system reproducible, observable, containerized, and deployable.

This phase includes Python code and infrastructure work.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-51---linux--wsl2"></a>

# PHASE 5.1 - Linux / WSL2

## Goal

Validate that the application works outside the Windows development
environment.

Tasks:

- create Linux/WSL2 environment
- install dependencies
- run unit tests
- run ingestion
- run API
- verify filesystem assumptions
- verify model loading

---

## New Concept - Environment Portability

A system that only runs in one local development environment is not yet
reproducible.

Linux compatibility also prepares the project for Docker and cloud
deployment.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-52---structured-logging"></a>

# PHASE 5.2 - Structured Logging

Target structure:

```text
app/
+-- observability/
    +-- __init__.py
    +-- logging.py
    +-- metrics.py
    +-- middleware.py
```

---

## File

```text
app/observability/logging.py
```

Planned functions:

```python
configure_logging(...)
get_logger(...)
```

---

## New Concept - Structured Logging

Instead of only:

```text
"Retrieval finished"
```

a structured event may contain:

```text
event = retrieval_complete
request_id = ...
latency_ms = 143
candidate_count = 30
```

Structured logs are easier to:

- search
- aggregate
- monitor
- analyze automatically

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-53---runtime-metrics"></a>

# PHASE 5.3 - Runtime Metrics

## File

```text
app/observability/metrics.py
```

Possible functions:

```python
record_request(...)
record_latency(...)
record_retrieval_latency(...)
record_generation_latency(...)
record_error(...)
```

Operational metrics should include:

- request count
- error count
- response latency
- retrieval latency
- reranking latency
- generation latency

Where applicable later:

- token usage
- model usage
- API cost

---

## New Concept - Quality vs Operational Metrics

Quality metrics:

```text
MRR
Hit@K
answer groundedness
```

Operational metrics:

```text
latency
request count
error rate
resource usage
cost
```

A system can have high retrieval quality but poor production latency.

Both dimensions matter.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-54---docker-hardening"></a>

# PHASE 5.4 - Docker Hardening

Files:

```text
Dockerfile
compose.yaml
.dockerignore
```

Tasks:

- reproducible build
- correct dependency installation
- explicit configuration
- healthcheck
- non-root user
- reduce unnecessary image contents

---

## New Concept - Multi-stage Docker Build

A build stage can contain tools required only to build dependencies.

The final runtime image can contain only what is needed to run the
application.

Potential benefits:

- smaller image
- smaller attack surface
- cleaner runtime

Use only if it provides practical value for this project.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-55---cicd"></a>

# PHASE 5.5 - CI/CD

Current CI already runs project tests.

Future flow may become:

```text
push
    ->
tests
    ->
static checks
    ->
security checks
    ->
Docker build
    ->
deployment
```

Possible improvements:

- formatter check
- Ruff
- type checking
- coverage
- dependency scan

---

## PHASE 5 Definition of Done

- [ ] application works under Linux / WSL2
- [ ] Docker build is reproducible
- [ ] container starts successfully
- [ ] container healthcheck works
- [ ] non-root execution configured
- [ ] CI runs project tests
- [ ] structured logging exists
- [ ] request latency can be measured
- [ ] retrieval latency can be measured
- [ ] generation latency can be measured
- [ ] deployment process is defined

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-6---security"></a>

# PHASE 6 - Security

**Status:** Planned

**Estimated work:** 6-10 hours

## Goal

Perform a dedicated security hardening review after the production
architecture exists.

Security is also considered during earlier phases, but PHASE 6 performs
the deeper review.

Target structure may include:

```text
app/
+-- security/
    +-- __init__.py
    +-- validation.py
    +-- limits.py
    +-- headers.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-61---threat-modeling"></a>

# PHASE 6.1 - Threat Modeling

## New Concept - Threat Model

Explicitly identify:

```text
assets
trust boundaries
attack surfaces
possible attackers
failure modes
impact
mitigations
```

Example system boundaries:

```text
user
->
FastAPI

PDF corpus
->
PDF parser

environment variables
->
application configuration

RAG context
->
generation model
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-62---runtime-input-validation"></a>

# PHASE 6.2 - Runtime Input Validation

## File

```text
app/security/validation.py
```

Possible functions:

```python
validate_query(...)
validate_input_size(...)
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-63---runtime-limits"></a>

# PHASE 6.3 - Runtime Limits

## File

```text
app/security/limits.py
```

Possible limits:

```text
maximum query length
maximum context size
maximum top_k
maximum request size
```

Future possible rate limiting may be evaluated here.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-64---secrets"></a>

# PHASE 6.4 - Secrets

Tasks:

- verify no secrets committed to Git
- use environment variables
- define production secret strategy
- review `.env.example`
- avoid logging secrets

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-65---dependency-security"></a>

# PHASE 6.5 - Dependency Security

Tasks may include:

- vulnerability scanning
- dependency review
- version pinning strategy
- security update process

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-66---container-security"></a>

# PHASE 6.6 - Container Security

Review:

- non-root execution
- filesystem permissions
- exposed ports
- unnecessary packages
- writable directories
- secret injection
- attack surface

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-67---http-security"></a>

# PHASE 6.7 - HTTP Security

Review:

- CORS
- security headers
- request limits
- error information leakage
- authentication requirements if introduced

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-68---rag-specific-security"></a>

# PHASE 6.8 - RAG-Specific Security

## New Concept - Indirect Prompt Injection

A retrieved document may contain text such as:

```text
Ignore previous instructions...
```

The document itself becomes an untrusted model input.

Security review should consider:

- separation between instructions and retrieved data
- prompt construction
- source trust
- model behavior
- tool access in future agent systems

---

## PHASE 6 Definition of Done

- [ ] threat model documented
- [ ] input limits reviewed
- [ ] filesystem boundaries reviewed
- [ ] PDF handling reviewed
- [ ] dependency security reviewed
- [ ] secret handling reviewed
- [ ] container permissions reviewed
- [ ] non-root execution verified
- [ ] HTTP controls reviewed
- [ ] indirect prompt injection reviewed
- [ ] major mitigations documented

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-7---production-v1"></a>

# PHASE 7 - Production v1

**Status:** Planned

**Estimated work:** 4-6 hours

## Goal

Integrate all completed layers into the first production-style release.

Production v1 does not mean enterprise completeness.

It means the project is:

```text
reproducible
tested
deployable
observable
documented
reasonably hardened
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-71---health-and-readiness"></a>

# PHASE 7.1 - Health and Readiness

Possible file:

```text
app/health.py
```

Possible functions:

```python
check_vector_store(...)
check_models(...)
build_readiness_status(...)
```

---

## New Concept - Liveness vs Readiness

### Liveness

Question:

```text
Is the process alive?
```

### Readiness

Question:

```text
Can the application actually serve a valid RAG request?
```

An application may be alive while its model or vector store is not ready.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-72---production-smoke-test"></a>

# PHASE 7.2 - Production Smoke Test

## File

```text
scripts/production_smoke.py
```

Possible flow:

```text
health check
    ->
known question
    ->
validate HTTP response
    ->
validate answer structure
    ->
validate sources
    ->
record latency
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-73---documentation"></a>

# PHASE 7.3 - Documentation

README should explain:

- project purpose
- architecture summary
- installation
- environment setup
- ingestion
- running API
- running tests
- Docker usage
- evaluation usage
- security considerations

Links:

```text
docs/ROADMAP.md
docs/ARCHITECTURE.md
docs/DEVELOPMENT_GUIDE.md
```

---

## PHASE 7 Definition of Done

A fresh environment can:

- [ ] clone the repository
- [ ] configure environment variables
- [ ] install/build dependencies
- [ ] start the application
- [ ] ingest a corpus
- [ ] query the API
- [ ] receive a grounded answer with sources
- [ ] run tests
- [ ] run evaluation
- [ ] produce structured logs
- [ ] expose runtime metrics
- [ ] follow documented setup instructions

At this point the project reaches:

```text
Production v1
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-8---expansion"></a>

# PHASE 8 - Expansion

PHASE 8 begins only after Production v1.

The purpose is to expand skills and system capabilities without
destabilizing the core RAG project.

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-8a---agent-exploration"></a>

# PHASE 8A - Agent Exploration

**Estimated work:** 4-6 hours

## Goal

Demonstrate the transition from a normal RAG application to an agentic
workflow.

The first agent should use the existing RAG system as a tool.

Target structure:

```text
agent/
|
+-- __init__.py
+-- models.py
+-- tools.py
+-- agent.py
```

---

## File

```text
agent/tools.py
```

Example function:

```python
search_knowledge_base(
    question: str,
)
```

Possible implementation:

```text
agent
    ->
FastAPI /ask
```

or:

```text
agent
    ->
RAG service
```

---

## New Concept - Tool Calling

A language model no longer only generates text.

It can decide:

```text
which tool to use
which arguments to provide
how to use the tool result
```

Example flow:

```text
user request
    ->
model decision
    ->
tool call
    ->
RAG system
    ->
tool result
    ->
final response
```

---

## PHASE 8A Definition of Done

- [ ] one agent exists
- [ ] agent can call the existing RAG system
- [ ] tool arguments are structured
- [ ] tool result returns to the model
- [ ] agent behavior is testable
- [ ] scope remains intentionally small

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-8b---sql-and-etl"></a>

# PHASE 8B - SQL and ETL

**Estimated work:** 6-10 hours

## Goal

Add practical data-engineering foundations after the production RAG
system is complete.

Target structure:

```text
data_pipeline/
|
+-- __init__.py
+-- database.py
+-- extract.py
+-- transform.py
+-- load.py
+-- pipeline.py
```

---

## File

```text
data_pipeline/database.py
```

Concepts:

```text
database connections
SELECT
JOIN
GROUP BY
indexes
transactions
```

---

## File

```text
data_pipeline/extract.py
```

Possible function:

```python
extract_from_source(...)
```

---

## File

```text
data_pipeline/transform.py
```

Possible functions:

```python
clean_records(...)
transform_records(...)
validate_records(...)
```

---

## File

```text
data_pipeline/load.py
```

Possible function:

```python
load_to_database(...)
```

---

## New Concept - ETL

ETL means:

```text
Extract
    ->
Transform
    ->
Load
```

It represents a common data-engineering pipeline pattern.

---

## PHASE 8B Definition of Done

- [ ] basic SQL workflow implemented
- [ ] data can be extracted
- [ ] data can be transformed
- [ ] validation exists
- [ ] transformed data can be loaded
- [ ] simple end-to-end ETL pipeline works

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-8c---mlops"></a>

# PHASE 8C - MLOps

**Estimated work:** 8-12 hours

## Goal

Introduce systematic experiment and model tracking.

Possible structure:

```text
mlops/
|
+-- __init__.py
+-- experiment.py
+-- artifacts.py
+-- model_metadata.py
```

---

## File

```text
mlops/experiment.py
```

Experiment records should contain:

- model
- model parameters
- retrieval configuration
- dataset hash
- Git commit
- timestamp
- quality metrics
- operational metrics
- cost metrics where applicable

---

## New Concept - Experiment Tracking

Instead of:

```text
"This version seemed better."
```

store:

```text
commit = abc123
dataset_hash = xyz456
embedding_model = ...
reranker = ...
MRR = 0.84
Hit@3 = 0.93
latency = 190 ms
```

Possible future technology:

```text
MLflow
```

A simpler local experiment tracker may be implemented first.

---

## File

```text
mlops/artifacts.py
```

Possible responsibilities:

- evaluation artifacts
- model metadata
- configuration snapshots
- run outputs

---

## PHASE 8C Definition of Done

- [ ] experiments have unique identity
- [ ] dataset version is recorded
- [ ] Git commit is recorded
- [ ] model configuration is recorded
- [ ] quality metrics are recorded
- [ ] operational metrics are recorded
- [ ] runs can be compared

---


[↑ Obsah / Contents](#obsah)

<a id="en-phase-8d---advanced-agents"></a>

# PHASE 8D - Advanced Agents

**Status:** Future

Detailed architecture is intentionally deferred.

Possible topics:

- multiple tools
- persistent state
- planning
- workflow graphs
- human approval
- agent evaluation
- multi-agent coordination

Potential technologies should be selected only after the simpler agent
workflow is understood.

This phase must not be designed prematurely.

---


[↑ Obsah / Contents](#obsah)

<a id="en-original-planning-estimates--historical"></a>

# Original planning estimates — historical

These values are preserved from the original plan. They are not a current
remaining-work forecast or a delivery commitment; reassessment requires a
separate planning decision.

Original active-development estimates (not recalculated):

| Phase | Estimated time |
|---|---:|
| PHASE 1 completion | 2-4 h |
| PHASE 2 evaluation foundation | 8-12 h |
| PHASE 3 retrieval refactor | 8-14 h |
| PHASE 4 API hardening | 5-8 h |
| PHASE 5 production engineering | 10-16 h |
| PHASE 6 security | 6-10 h |
| PHASE 7 Production v1 | 4-6 h |
| PHASE 8A agent exploration | 4-6 h |
| PHASE 8B SQL / ETL | 6-10 h |
| PHASE 8C MLOps | 8-12 h |

Original estimate of remaining effort to Production v1:

```text
43-70 hours
```

These estimates include:

- implementation
- explanation
- manual code entry
- testing
- debugging
- integration

They are not pure typing estimates.

---


[↑ Obsah / Contents](#obsah)

<a id="en-planning-history"></a>

## Planning history

The previous Phase 2A status and step-by-step immediate-task list are retained in
[the pre-cleanup roadmap revision](https://github.com/jyenten/AI_roadmap/blob/d7c3b4f71711c798646bd0a878b96b9c46c92d93/rag_api_project/docs/ROADMAP.md#historical-project-status-original-phase-2a-plan).
They describe an earlier checkpoint, not today's next steps. Completed work is
recorded in [LEARNING_LOG.md](../../LEARNING_LOG.md); the current focus belongs
only to this roadmap's [current development focus](#current-development-focus).


---

<a id="cz"></a>
## CZ — Česká verze

Tento dokument určuje **co budovat, pořadí fází, cíle a kritéria přijetí**. Postup implementace a revize patří do [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md#cz), hranice komponent do [ARCHITECTURE.md](ARCHITECTURE.md#cz) a datované výsledky práce a učení do [LEARNING_LOG.md](../../LEARNING_LOG.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-stavový-přehled--2026-10-28"></a>

## Stavový přehled — 2026-10-28

Jde o aktuální plánovací bod, nikoli o přečíslování nebo náhradu schválených specifikací fází níže. Dokončení milníku nepotvrzuje splnění všech kritérií širší fáze ani připravenost do produkce.

| Milník | Zjištěný stav | Důkazy / postup |
| --- | --- | --- |
| RAG API, ingest PDF a úložiště Chroma | Implementovaný prototyp; další zodolnění je plánované | [README projektu](../README.cs.md), [architektura](ARCHITECTURE.md#cz) |
| Samostatný průzkumník PDF stránek | Implementovaný | `document_search/`, [provoz](OPERATIONS.md#cz) |
| Evaluace retrievalu podle důkazů | Implementované metriky, historie, latence a provenance | `evaluation/`, [evaluační metodika](EVALUATION.md#cz) |
| Porovnání chunkového BM25 a Vector | Implementované v offline CLI nad DEV/RANDOM | `app/retrievers/`, [zapsané milníky](../../LEARNING_LOG.md#cz-historie-projektu-a-učení) |
| Hybridní lexikální/sémantický retrieval s RRF | Lokálně rozpracovaný; nejde o zveřejněný režim CLI/API | [Záznam necommitnuté práce](../../LEARNING_LOG.md#cz-necommitnutá-práce-pozorovaná-28-10-2026) |
| Evaluace na odděleném TEST | Vyhrazena pro závěrečné posouzení, nikoli průběžné ladění | [Evaluační pravidla](EVALUATION.md#cz) |
| Dvojjazyčné příručky a regrese validátoru | Začleněné přes [PR #3](https://github.com/jyenten/AI_roadmap/pull/3) | [Provoz](OPERATIONS.md#cz), [evaluace](EVALUATION.md#cz) |
| Automatizace závislostí a bezpečnosti | Zapnutá; nálezy závislosti ChromaDB zůstávají otevřené | `.github/workflows/`, [aktuální projektový bod](../../LEARNING_LOG.md#cz-ověřený-stav-projektu) |

Podrobné výsledky a historické MRR/Hit@K patří do evaluační metodiky a deníku učení; roadmapa neudržuje další kopii benchmarkové tabulky.


[↑ Obsah / Contents](#obsah)

<a id="cz-aktuální-zaměření-vývoje"></a>

## Aktuální zaměření vývoje

Dalším zaznamenaným milníkem je hybridní BM25 + Vector retrieval s RRF. Nejprve dokonči a zkontroluj implementaci, potom změř DEV/RANDOM proti zachovaným baseline a až pak rozhoduj o zlepšeních. TEST ponech oddělený. Lokální experimenty s backendem a nezačleněné návrhy závislostí podléhají vlastní revizi; jejich existence není začleněním do `main` ani schválením náhrady retrieval architektury.

Deník učení historicky označoval BM25 jako Phase 3.3, evaluaci retrievalu jako Phase 3.4 a hybridní RRF jako Phase 3.5. Tato označení **nejsou identifikátory fází této roadmapy**. Zde nadále platí původní čísla a názvy: 3.3 Vektorové vyhledávání, 3.4 Zpracování dotazu a 3.5 Reranker. Při odkazu na práci v deníku používej celý název milníku.


[↑ Obsah / Contents](#obsah)

<a id="cz-jak-číst-a-aktualizovat-schválený-plán"></a>

## Jak číst a aktualizovat schválený plán

Specifikace fází níže zachovávají schválené pořadí, plánované moduly, výukové koncepty a checklisty Definition of Done. Jejich původní **stav**, odhady a nezaškrtnutá políčka jsou výchozím plánem, nikoli dalším živým přehledem postupu. Zjištěný pokrok čti v přehledu výše; nezaškrtnuté historické políčko samo nedokazuje, že modul chybí. Kritéria neoznačuj za splněná bez potřebných důkazů.

Pracovní postup je **Complete → Measure → Improve**. Společná pravidla rozsahu, backlogu, zmrazení, testování a revize patří do [vývojového postupu](DEVELOPMENT_GUIDE.md#cz-vývojový-postup). Změna cílů, priorit nebo kritérií přijetí vyžaduje výslovné plánovací rozhodnutí; redakční úprava ji neschvaluje.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-1---funkční-kostra-rag"></a>

# FÁZE 1 - Funkční kostra RAG

**Stav:** Z větší části dokončeno

**Původní odhad zbývající práce:** 2–4 hodiny

<a id="cz-cíl"></a>

## Cíl

Udržovat funkční RAG aplikaci od vstupu až po odpověď.

Hlavní běhová pipeline:

```text
PDF documents
    ->
ingestion
    ->
text preprocessing
    ->
chunking
    ->
embeddings
    ->
ChromaDB
    ->
retrieval
    ->
reranking
    ->
context construction
    ->
generation
    ->
FastAPI response
```

Smyslem FÁZE 1 není architektonická dokonalost.

Smyslem je funkční systém, který lze následně měřit a zlepšovat.

---

<a id="cz-11-appconfigpy"></a>

## 1.1 `app/config.py`

<a id="cz-odpovědnosti"></a>

### Odpovědnosti

- konfigurace aplikace
- názvy modelů
- konfigurace kolekce Chroma
- limity retrievalu
- limity generování
- konfigurace prostředí

<a id="cz-důležité-koncepty"></a>

### Důležité koncepty

- centralizovaná konfigurace
- proměnné prostředí
- validace konfigurace
- Pydantic Settings

<a id="cz-budoucí-směr"></a>

### Budoucí směr

Konfigurace se má načítat přes validovaný objekt nastavení, nikoli přes duplicitní konstanty.

Možný veřejný přístup:

```python
get_settings()
```

---

<a id="cz-12-appschemaspy"></a>

## 1.2 `app/schemas.py`

<a id="cz-současné-modely"></a>

### Současné modely

- `QuestionRequest`
- `SourceChunk`
- `AnswerResponse`

<a id="cz-možné-budoucí-modely"></a>

### Možné budoucí modely

- `ErrorResponse`
- `HealthResponse`

<a id="cz-důležitý-koncept"></a>

### Důležitý koncept

API schémata popisují data přenášená přes hranici HTTP.

Mají zůstat oddělená od interních retrieval modelů.

---

<a id="cz-13-appretrievalpy"></a>

## 1.3 `app/retrieval.py`

<a id="cz-současné-odpovědnosti"></a>

### Současné odpovědnosti

- načítání embedding modelu
- příprava dotazu
- retrieval z Chroma
- výběr kandidátů
- přerovnání pomocí CrossEncoderu
- heuristické skórování
- výběr výsledků

<a id="cz-současný-technický-dluh"></a>

### Současný technický dluh

Tento modul nyní spojuje více odpovědností a logiku specifickou pro doménu.

Ve FÁZI 1 se záměrně nerefactoruje.

Větší refaktoring retrievalu patří do:

```text
PHASE 3
```

---

<a id="cz-14-appgenerationpy"></a>

## 1.4 `app/generation.py`

<a id="cz-hlavní-odpovědnosti"></a>

### Hlavní odpovědnosti

- načítání generativního modelu
- sestavení promptu
- inference modelu
- generování odpovědi

Hlavní tok:

```text
question
+
retrieved context
    ->
prompt
    ->
generation model
    ->
answer
```

Možné budoucí oddělení:

```text
prompt construction
model inference
output processing
```

K tomuto rozdělení přistup pouze tehdy, vyžaduje-li je složitost.

---

<a id="cz-15-appragpy"></a>

## 1.5 `app/rag.py`

<a id="cz-odpovědnost"></a>

### Odpovědnost

Orchestrace RAG.

Cílový konceptuální tok:

```text
question
    ->
retrieval
    ->
context selection
    ->
generation
    ->
sources
    ->
final response
```

<a id="cz-současný-technický-dluh-1"></a>

### Současný technický dluh

Současná implementace obsahuje chování specifické pro OSPF.

Jeho odstranění patří do:

```text
PHASE 3
```

---

<a id="cz-16-appmainpy"></a>

## 1.6 `app/main.py`

<a id="cz-odpovědnost-1"></a>

### Odpovědnost

Vstupní bod aplikace FastAPI.

Současné endpointy:

```text
GET /
GET /health
POST /ask
```

Cílová odpovědnost:

```text
HTTP request
    ->
validation
    ->
application service
    ->
HTTP response
```

Aplikační logika se má postupně přesunout mimo vstupní bod API.

---

<a id="cz-17-scriptsingestpy"></a>

## 1.7 `scripts/ingest.py`

<a id="cz-současná-pipeline"></a>

### Současná pipeline

```text
PDF
    ->
extract text
    ->
clean text
    ->
chunk
    ->
embed
    ->
store in ChromaDB
```

<a id="cz-dosavadní-zlepšení"></a>

### Dosavadní zlepšení

- čištění textu PDF
- ochrana a obnova URL
- chunkování podle slov
- překryv chunků
- validace překryvu

<a id="cz-důležité-pravidlo"></a>

### Důležité pravidlo

Ingest nerefactoruj pouze kvůli architektonické symetrii.

Refactoruj ho pouze tehdy, když:

- je obtížné testování
- je nutné opětovné použití
- výrazně roste složitost
- evaluace odhalí problém ingestu

---

<a id="cz-fáze-1--podmínky-dokončení"></a>

## FÁZE 1 — Podmínky dokončení

- [x] PDF dokumenty lze ingestovat
- [x] extrakce textu funguje
- [x] chunkování funguje
- [x] lze generovat embeddingy
- [x] ChromaDB ukládá prohledávatelné chunky
- [x] retrieval funguje
- [x] přerovnání funguje
- [x] generování funguje
- [x] `POST /ask` funguje
- [x] odpovědi obsahují informace o zdrojích
- [x] smoke testy procházejí
- [ ] zbývající technický dluh je zdokumentovaný

Po splnění těchto podmínek je FÁZE 1 zmrazená.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2---základ-evaluace"></a>

# FÁZE 2 - Základ evaluace

**Stav:** Rozpracováno

**Původní odhad zbývající práce:** 8–12 hodin

<a id="cz-cíl-1"></a>

## Cíl

Vytvořit spolehlivý evaluační rámec před většími změnami retrievalu.

Retrieval se už nemá zlepšovat pouze podle několika ručně vybraných otázek.

Cílový vývojový tok:

```text
baseline
    ->
evaluation
    ->
retrieval change
    ->
evaluation
    ->
comparison
```

---

<a id="cz-úlohy-evaluačních-datasetů"></a>

## Úlohy evaluačních datasetů

Tři kategorie datasetů mají záměrně odlišné účely.

<a id="cz-dev"></a>

### DEV

Používá se při vývoji a ladění.

Výsledky DEV mohou ovlivnit implementační rozhodnutí.

Cílová velikost:

```text
approximately 20 manually validated questions
```

---

<a id="cz-random"></a>

### RANDOM

Používá se pro:

- průzkum robustnosti
- hledání neočekávaných selhání
- průzkum pokrytí korpusu

Náhodné vzorkování musí být reprodukovatelné pomocí uloženého seedu.

RANDOM nenahrazuje TEST.

---

<a id="cz-test"></a>

### TEST

Oddělená závěrečná evaluace.

TEST se nesmí opakovaně procházet a používat k ladění.

Jeho účelem je odhad generalizace po dokončení ladění.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a---univerzální-průzkumník-dokumentů"></a>

# FÁZE 2A - Univerzální průzkumník dokumentů

**Historický stav plánu:** Aktuální aktivní podfáze

**Odhad práce:** 3–4 hodiny

<a id="cz-cíl-2"></a>

## Cíl

Vytvořit opakovaně použitelný lexikální průzkumník korpusu nezávislý na doméně pro:

- hledání kandidátních důkazů
- prohlížení obsahu PDF
- ruční validaci referenčních důkazů
- pomoc při sestavování datasetů DEV / RANDOM / TEST

Průzkumník musí fungovat i po nahrazení celého PDF korpusu.

Příklady budoucích domén:

```text
Kubernetes
cybersecurity
Linux
law
manufacturing
accounting
networking
```

Průzkumník nesmí obsahovat pravidla řazení specifická pro OSPF.

---

<a id="cz-cílová-struktura"></a>

## Cílová struktura

```text
document_search/
|
+-- __init__.py
+-- models.py
+-- normalize.py
+-- tokenize.py
+-- load_pages.py
+-- build_index.py
+-- search.py
|
+-- security/
    +-- __init__.py
    +-- paths.py
    +-- pdf_validation.py
    +-- input_validation.py
```

CLI:

```text
scripts/
+-- search_pdf.py
```

Testy:

```text
tests/
+-- document_search/
    +-- test_models.py
    +-- test_normalize.py
    +-- test_tokenize.py
    +-- test_load_pages.py
    +-- test_build_index.py
    +-- test_search.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a0---zmrazení-architektury"></a>

# FÁZE 2A.0 - Zmrazení architektury

<a id="cz-cíl-3"></a>

## Cíl

Před implementací definovat:

- odpovědnosti modulů
- datové modely
- veřejná rozhraní
- směr závislostí
- bezpečnostní hranice
- podmínky dokončení

Dokumentace:

```text
docs/ROADMAP.md
docs/ARCHITECTURE.md
docs/DEVELOPMENT_GUIDE.md
```

Produkční kód nepřepracovávej opakovaně, když už vznikají závislé moduly, pokud to nevyžaduje konkrétní technický problém.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a1---datové-modely"></a>

# FÁZE 2A.1 - Datové modely

<a id="cz-soubor"></a>

## Soubor

```text
document_search/models.py
```

<a id="cz-plánované-modely"></a>

## Plánované modely

```python
PageDocument
SearchResult
BM25SearchIndex
```

<a id="cz-pagedocument"></a>

### `PageDocument`

Konceptuálně:

```python
PageDocument(
    source="manual.pdf",
    page=26,
    text="...",
)
```

Představuje jednu prohledávatelnou zdrojovou stránku.

---

<a id="cz-searchresult"></a>

### `SearchResult`

Konceptuálně:

```python
SearchResult(
    document=document,
    score=12.5,
)
```

Představuje jeden seřazený výsledek BM25.

---

<a id="cz-bm25searchindex"></a>

### `BM25SearchIndex`

Vlastní:

```text
page corpus
+
BM25 model
```

Volající tak nemusí tyto objekty ručně udržovat v souladu.

---

<a id="cz-nový-koncept---neměnné-datové-třídy"></a>

## Nový koncept - Neměnné datové třídy

Preferovaný vzor:

```python
@dataclass(frozen=True)
```

Přínosy:

- brání nechtěným změnám
- usnadňuje uvažování o stavu
- činí testy předvídatelnějšími
- jasně reprezentuje faktická data

Příklady neměnných faktů:

```text
source filename
page number
document text
completed search score
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a2---zpracování-textu"></a>

# FÁZE 2A.2 - Zpracování textu

**Odhad práce:** Méně než 1 hodina

Tyto moduly jsou malé a úzce souvisejí, proto je lze implementovat společně.

---

<a id="cz-soubor-1"></a>

## Soubor

```text
document_search/normalize.py
```

Hlavní funkce:

```python
normalize_text(
    text: str,
) -> str
```

Odpovědnosti:

- převod na malá písmena
- sjednocení whitespace
- obecné čištění textu

Nesmí obsahovat:

```text
OSPF terminology
Cisco rules
manual ranking boosts
domain-specific vocabulary
```

---

<a id="cz-soubor-2"></a>

## Soubor

```text
document_search/tokenize.py
```

Hlavní funkce:

```python
tokenize(
    text: str,
) -> list[str]
```

Příklad:

```text
"OSPF calculates interface cost."
```

se přibližně změní na:

```python
[
    "ospf",
    "calculates",
    "interface",
    "cost",
]
```

---

<a id="cz-důležité-koncepty-1"></a>

## Důležité koncepty

- čisté funkce
- deterministické předzpracování
- opakovaně použitelné zpracování textu
- oddělení normalizace a retrievalu

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a3---základy-bezpečnosti"></a>

# FÁZE 2A.3 - Základy bezpečnosti

**Odhad práce:** Přibližně 1 hodina

<a id="cz-cíl-4"></a>

## Cíl

Chránit souborový systém a uživatelské vstupy vyhledávání ještě před parsováním PDF a řazením.

---

<a id="cz-soubor-3"></a>

## Soubor

```text
document_search/security/paths.py
```

Plánované funkce:

```python
resolve_safe_path(...)
validate_data_directory(...)
```

Odpovědnosti:

- hranice povolených adresářů
- zabránění path traversal
- validace vyhodnocených cest
- kontroly zohledňující symbolické odkazy

---

<a id="cz-nový-koncept---path-traversal"></a>

## Nový koncept - Path traversal

Příklad nebezpečného vstupu:

```text
../../private_file
```

Cesta, která zdánlivě vede dovnitř adresáře, může přes symbolický odkaz ve skutečnosti směřovat mimo něj.

Bezpečnost proto musí ověřovat vyhodnocené souborové cesty, nikoli pouze původní vstupní řetězec.

---

<a id="cz-soubor-4"></a>

## Soubor

```text
document_search/security/input_validation.py
```

Plánované funkce:

```python
validate_query(...)
validate_top_k(...)
```

Odpovědnosti:

- odmítat prázdné dotazy
- odmítat příliš dlouhé dotazy
- odmítat neplatné `top_k`
- bránit nepřiměřeným požadavkům na prostředky

---

<a id="cz-nový-koncept---validační-hranice"></a>

## Nový koncept - Validační hranice

Externí vstup se má validovat poblíž hranice systému.

Interní funkce pak mohou pracovat s hodnotami, které už splňují očekávaný kontrakt.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a4---načítání-pdf-a-validace-pdf"></a>

# FÁZE 2A.4 - Načítání PDF a validace PDF

**Odhad práce:** 1–2 hodiny

<a id="cz-soubor-5"></a>

## Soubor

```text
document_search/security/pdf_validation.py
```

Plánované funkce:

```python
validate_pdf_extension(...)
validate_pdf_signature(...)
validate_pdf_limits(...)
```

Odpovědnosti:

- ověřit příponu `.pdf`
- ověřit, že soubor skutečně vypadá jako PDF
- vynutit limit velikosti souboru
- vynutit limit počtu stránek

---

<a id="cz-nový-koncept---signatura-souboru"></a>

## Nový koncept - Signatura souboru

Název souboru jako:

```text
document.pdf
```

nedokazuje, že soubor skutečně je PDF.

Validace má vedle přípony kontrolovat i hlavičku nebo signaturu souboru.

---

<a id="cz-nový-koncept---vyčerpání-prostředků"></a>

## Nový koncept - Vyčerpání prostředků

I zdánlivě platný soubor může spotřebovat nepřiměřené prostředky.

Příklady:

```text
multi-gigabyte file
hundreds of thousands of pages
extremely large extracted text
```

Limity prostředků chrání:

- RAM
- CPU
- latenci
- dostupnost služby

---

<a id="cz-soubor-6"></a>

## Soubor

```text
document_search/load_pages.py
```

Hlavní funkce:

```python
load_pdf_pages(
    data_dir: Path,
) -> list[PageDocument]
```

Hlavní tok:

```text
data directory
    ->
discover PDF files
    ->
security validation
    ->
PdfReader
    ->
extract each page
    ->
PageDocument
```

Důležité pravidlo:

Loader nesmí dokumenty potichu zkracovat.

Pokud nelze soubor zpracovat bezpečně nebo celý, musí být selhání výslovné.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a5---bm25-index"></a>

# FÁZE 2A.5 - BM25 index

**Odhad práce:** Méně než 1 hodina

<a id="cz-soubor-7"></a>

## Soubor

```text
document_search/build_index.py
```

Hlavní funkce:

```python
build_bm25_index(
    pages: list[PageDocument],
) -> BM25SearchIndex
```

Externí závislost:

```text
rank-bm25
```

---

<a id="cz-nový-koncept---bm25"></a>

## Nový koncept - BM25

BM25 je standardní lexikální algoritmus pro vyhledávání informací.

Zohledňuje:

- četnost termínu
- inverzní četnost dokumentů
- normalizaci podle délky dokumentu

Konceptuálně:

```text
query terms
    +
how often they appear in a page
    +
how rare they are across the corpus
    +
page/document length
    ->
relevance score
```

Je vhodnější než ručně napsané řazení typu:

```text
neighbor = +1
DROTHER = +5
distance below 200 chars = +3
```

protože řazení BM25 vychází ze statistik korpusu, nikoli z ručně zadaných doménových heuristik.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a6---vyhledávací-modul"></a>

# FÁZE 2A.6 - Vyhledávací modul

**Odhad práce:** Přibližně 1 hodina

<a id="cz-soubor-8"></a>

## Soubor

```text
document_search/search.py
```

Veřejná funkce:

```python
search_pages(
    index: BM25SearchIndex,
    query: str,
    top_k: int = 10,
) -> list[SearchResult]
```

Hlavní tok:

```text
query
    ->
validation
    ->
tokenization
    ->
BM25 scores
    ->
descending ranking
    ->
TOP K
    ->
SearchResult
```

---

<a id="cz-důležitý-nový-koncept---hranice-veřejného-api"></a>

## Důležitý nový koncept - Hranice veřejného API

Ostatní moduly mají používat:

```python
search_pages(...)
```

aniž by ručně přistupovaly k:

```text
BM25 internals
page arrays
raw score arrays
sorting logic
```

Interní implementaci pak lze změnit bez změny každého volajícího.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a7---cli"></a>

# FÁZE 2A.7 - CLI

**Odhad práce:** Méně než 1 hodina

<a id="cz-soubor-9"></a>

## Soubor

```text
scripts/search_pdf.py
```

Plánované funkce:

```python
build_parser()
print_results()
select_result()
print_result_detail()
main()
```

Cílové použití:

```text
python -m scripts.search_pdf "how does OSPF calculate interface cost"
```

Volitelně:

```text
--top-k 5
```

CLI má obsahovat:

- parsování argumentů
- čitelný výstup pro člověka
- interaktivní výběr

Nemá obsahovat:

- implementaci BM25
- vnitřnosti parsování PDF
- heuristiky řazení

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2a8---integrace"></a>

# FÁZE 2A.8 - Integrace

<a id="cz-úkoly"></a>

## Úkoly

- přidat závislost `rank-bm25`
- spustit unit testy dokumentového vyhledávání
- spustit všechny projektové testy
- prohledat skutečný Cisco korpus
- ručně prohlédnout několik pořadí výsledků
- ověřit obecné chování
- potvrdit odstranění heuristik řazení specifických pro OSPF

---

<a id="cz-fáze-2a--podmínky-dokončení"></a>

## FÁZE 2A — Podmínky dokončení

- [ ] lze najít libovolná PDF
- [ ] hranice souborového systému jsou validované
- [ ] přípona PDF je validovaná
- [ ] signatura PDF je validovaná
- [ ] existují limity prostředků PDF
- [ ] stránky reprezentují typované datové modely
- [ ] normalizace je nezávislá na doméně
- [ ] tokenizace funguje
- [ ] lze vytvořit BM25 index
- [ ] lze řadit libovolné textové dotazy
- [ ] výsledky zpřístupňují zdroj, stránku, skóre a text
- [ ] CLI funguje
- [ ] příslušné unit testy procházejí
- [ ] všechny projektové testy procházejí
- [ ] neexistují heuristiky řazení specifické pro OSPF

Po splnění těchto podmínek je FÁZE 2A zmrazená.

Mimo rozsah:

```text
fuzzy retrieval
semantic document explorer
LLM reranking
query rewriting
synonym dictionaries
hybrid BM25 + embedding explorer
advanced UI
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2b---evaluační-datové-modely"></a>

# FÁZE 2B - Evaluační datové modely

**Odhad práce:** 1–2 hodiny

<a id="cz-cíl-5"></a>

## Cíl

Přesunout opakovaně použitelnou evaluační logiku z volných skriptů a slovníků do typovaných projektových modulů.

Cílová struktura:

```text
evaluation/
|
+-- __init__.py
+-- models.py
+-- dataset.py
+-- evidence.py
+-- metrics.py
+-- runner.py
+-- history.py
+-- random_eval.py
```

---

<a id="cz-soubor-10"></a>

## Soubor

```text
evaluation/models.py
```

Plánované modely:

```python
GoldEvidence
EvaluationQuestion
QuestionResult
EvaluationMetrics
EvaluationRun
```

---

<a id="cz-nový-koncept---typované-evaluační-modely"></a>

## Nový koncept - Typované evaluační modely

Namísto:

```python
question["gold_evidence"][0]["source"]
```

preferuj:

```python
question.gold_evidence
```

Přínosy:

- čitelnější kód
- lepší podporu IDE
- méně chyb v názvech klíčů
- jednodušší validaci
- bezpečnější refaktoring

---

<a id="cz-soubor-11"></a>

## Soubor

```text
evaluation/dataset.py
```

Plánované funkce:

```python
load_dataset(...)
validate_dataset(...)
calculate_dataset_hash(...)
```

Odpovědnosti:

- načítání datasetů DEV / TEST
- validace schématu
- identita datasetu
- reprodukovatelnost

---

<a id="cz-nový-koncept---hashování-datasetu"></a>

## Nový koncept - Hashování datasetu

SHA256 hash identifikuje přesnou verzi datasetu použitou v evaluačním běhu.

Odstraňuje nejednoznačnost tvrzení typu:

```text
"MRR was 0.82 on the DEV dataset"
```

pokud se DEV dataset od tohoto běhu změnil.

Namísto toho:

```text
dataset_hash = abc123...
MRR = 0.82
```

---

<a id="cz-soubor-12"></a>

## Soubor

```text
evaluation/evidence.py
```

Plánované funkce:

```python
normalize_evidence_text(...)
matches_gold_evidence(...)
find_gold_rank(...)
```

Platná shoda důkazu má vyžadovat:

```text
source
AND
page
AND
expected text fragment
```

v rámci jedné přijatelné varianty důkazu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2c---metriky-retrievalu"></a>

# FÁZE 2C - Metriky retrievalu

**Odhad práce:** Přibližně 1 hodina

<a id="cz-soubor-13"></a>

## Soubor

```text
evaluation/metrics.py
```

Plánované funkce:

```python
reciprocal_rank(...)
mean_reciprocal_rank(...)
hit_at_k(...)
aggregate_metrics(...)
```

---

<a id="cz-metrika---hitk"></a>

## Metrika - Hit@K

Otázka:

```text
Did the correct evidence appear in the first K results?
```

Příklady:

```text
Hit@1
Hit@3
Hit@5
Hit@8
```

---

<a id="cz-metrika---reciproční-pořadí"></a>

## Metrika - Reciproční pořadí

Pokud se správný důkaz objeví na:

```text
rank 1 -> 1.0
rank 2 -> 0.5
rank 4 -> 0.25
```

Konceptuální vzorec:

```text
1 / rank
```

---

<a id="cz-metrika---mrr"></a>

## Metrika - MRR

Průměrné reciproční pořadí:

```text
average reciprocal rank
across all evaluation questions
```

MRR odměňuje systémy, které umisťují relevantní důkazy poblíž začátku pořadí.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2d---evaluační-runner-a-historie"></a>

# FÁZE 2D - Evaluační runner a historie

**Odhad práce:** Přibližně 1 hodina

<a id="cz-soubor-14"></a>

## Soubor

```text
evaluation/runner.py
```

Plánované funkce:

```python
evaluate_question(...)
evaluate_dataset(...)
build_run_metadata(...)
```

Konceptuální tok:

```text
EvaluationQuestion
    ->
retrieval
    ->
ranked results
    ->
gold evidence matching
    ->
question metrics
```

---

<a id="cz-soubor-15"></a>

## Soubor

```text
evaluation/history.py
```

Plánované funkce:

```python
load_history(...)
append_run(...)
save_history(...)
```

Ukládaná metadata mají zahrnovat:

- SHA Git commitu
- příznak necommitnutých změn
- SHA256 datasetu
- časové razítko
- konfiguraci
- evaluační metriky

Příklad:

```text
commit A
MRR = 0.71

commit B
MRR = 0.82
```

Změny retrievalu tak lze porovnávat podle důkazů.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2e---evaluace-random"></a>

# FÁZE 2E - Evaluace RANDOM

**Odhad práce:** 2–3 hodiny

<a id="cz-soubor-16"></a>

## Soubor

```text
evaluation/random_eval.py
```

Možné funkce:

```python
sample_pages(...)
build_random_sample(...)
save_seed(...)
```

---

<a id="cz-nový-koncept---reprodukovatelná-náhodnost"></a>

## Nový koncept - Reprodukovatelná náhodnost

Použij samostatný generátor náhodných čísel se seedem.

Příklad:

```python
random.Random(seed)
```

Stejný seed má vytvořit stejný vzorek.

Neočekávané selhání RANDOM pak lze později zopakovat.

---

<a id="cz-účel-random"></a>

## Účel RANDOM

RANDOM je určen pro:

```text
robustness
coverage
failure discovery
```

Není určen pro:

```text
final generalization claims
```

To zůstává úlohou TEST.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-2f---kompletní-evaluační-dataset"></a>

# FÁZE 2F - Kompletní evaluační dataset

**Odhad práce:** Zahrnut v odhadu FÁZE 2

<a id="cz-úkoly-1"></a>

## Úkoly

- rozšířit DEV přibližně na 20 otázek
- ručně ověřit referenční důkazy
- rozšířit témata otázek
- implementovat workflow RANDOM
- vytvořit TEST dataset
- zmrazit TEST dataset
- zdokumentovat role datasetů

---

<a id="cz-fáze-2--podmínky-dokončení"></a>

## FÁZE 2 — Podmínky dokončení

- [ ] univerzální BM25 průzkumník dokumentů je dokončený
- [ ] DEV dataset je dostatečně široký
- [ ] referenční důkazy DEV jsou ručně ověřené
- [ ] workflow RANDOM je implementované
- [ ] běhy RANDOM jsou reprodukovatelné
- [ ] TEST dataset je vytvořený
- [ ] TEST dataset je zmrazený
- [ ] MRR je implementované
- [ ] Hit@1 je implementované
- [ ] Hit@3 je implementované
- [ ] Hit@5 je implementované
- [ ] Hit@8 je implementované
- [ ] hashování datasetu je implementované
- [ ] Git metadata se zaznamenávají
- [ ] historie evaluace je dostupná
- [ ] evaluační testy procházejí

Po FÁZI 2 se evaluační infrastruktura zmrazí, pokud se neobjeví konkrétní problém měření.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-3---refaktoring-retrievalu"></a>

# FÁZE 3 - Refaktoring retrievalu

**Stav:** Plánováno

**Odhad práce:** 8–14 hodin

<a id="cz-cíl-6"></a>

## Cíl

Hlavní RAG retrieval refactorovat až po vytvoření spolehlivé evaluace.

Současný velký modul:

```text
app/retrieval.py
```

Cílová struktura:

```text
app/
+-- retrieval/
    +-- __init__.py
    +-- models.py
    +-- embeddings.py
    +-- vector_search.py
    +-- query.py
    +-- reranker.py
    +-- scoring.py
    +-- service.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-31---retrieval-modely"></a>

# FÁZE 3.1 - Retrieval modely

<a id="cz-soubor-17"></a>

## Soubor

```text
app/retrieval/models.py
```

Plánované modely:

```python
RetrievedChunk
ScoredChunk
RetrievalResult
```

Účel:

nahradit volně strukturované slovníky a n-tice explicitními interními typy pro retrieval.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-32---embeddingy"></a>

# FÁZE 3.2 - Embeddingy

<a id="cz-soubor-18"></a>

## Soubor

```text
app/retrieval/embeddings.py
```

Plánované funkce:

```python
load_embedding_model(...)
embed_query(...)
embed_documents(...)
```

Odpovědnost:

pouze operace s embeddingy.

Nesmí:

- komunikovat s FastAPI
- rozhodovat o pořadí
- formátovat API odpovědi

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-33---vektorové-vyhledávání"></a>

# FÁZE 3.3 - Vektorové vyhledávání

<a id="cz-soubor-19"></a>

## Soubor

```text
app/retrieval/vector_search.py
```

Plánované funkce:

```python
search_vector_store(...)
convert_chroma_results(...)
```

Odpovědnost:

komunikace s ChromaDB.

Důležité architektonické pravidlo:

Vyšší vrstvy nemají přímo záviset na struktuře odpovědí Chroma.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-34---zpracování-dotazu"></a>

# FÁZE 3.4 - Zpracování dotazu

<a id="cz-soubor-20"></a>

## Soubor

```text
app/retrieval/query.py
```

Možná funkce:

```python
normalize_query(...)
```

Budoucí rozšiřování dotazů je přípustné pouze při měřitelném přínosu prokázaném evaluací DEV.

Doménové podmínky pevně zakódované v retrievalu mají být odstraněny.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-35---reranker"></a>

# FÁZE 3.5 - Reranker

<a id="cz-soubor-21"></a>

## Soubor

```text
app/retrieval/reranker.py
```

Plánované funkce:

```python
load_reranker(...)
rerank(...)
```

Hlavní tok:

```text
query
+
candidate chunk
    ->
CrossEncoder
    ->
relevance score
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-36---skórování"></a>

# FÁZE 3.6 - Skórování

<a id="cz-soubor-22"></a>

## Soubor

```text
app/retrieval/scoring.py
```

Cíl:

odstranit nevhodné kombinace skóre.

Současný známý problém:

```text
raw CrossEncoder score
+
large heuristic bonus
```

může způsobit, že heuristická škála převáží relevanci modelu.

Možné přístupy k vyhodnocení:

- řazení pouze podle CrossEncoderu
- normalizovaná kombinace skóre
- slučování pořadí

Volba musí vycházet z metrik DEV.

---

<a id="cz-nový-koncept---slučování-pořadí"></a>

## Nový koncept - Slučování pořadí

Místo přímého sčítání neslučitelných hrubých skóre mohou systémy kombinovat relativní pozice v pořadí.

Tím se omezují některé problémy rozdílných škál skóre.

Zavést je lze pouze při odůvodnění evaluací.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-37---retrieval-služba"></a>

# FÁZE 3.7 - Retrieval služba

<a id="cz-soubor-23"></a>

## Soubor

```text
app/retrieval/service.py
```

Cílové veřejné API:

```python
retrieve(
    query: str,
) -> list[RetrievalResult]
```

Pipeline:

```text
query
    ->
vector search
    ->
candidate set
    ->
reranking
    ->
score handling
    ->
TOP K
```

Vyšší vrstvy mají primárně volat toto veřejné rozhraní.

---

<a id="cz-fáze-3--podmínky-dokončení"></a>

## FÁZE 3 — Podmínky dokončení

- [ ] retrieval neobsahuje pevně zakódované OSPF podmínky
- [ ] existují retrieval datové modely
- [ ] práce s embeddingy je oddělená
- [ ] komunikace s Chroma je oddělená
- [ ] reranking je oddělený
- [ ] skórování je izolované
- [ ] existuje stabilní veřejné retrieval API
- [ ] baseline metriky jsou zaznamenané
- [ ] refactorovaný retrieval je vyhodnocený na DEV
- [ ] retrieval regresní testy procházejí
- [ ] TEST se nepoužívá při ladění
- [ ] po ladění proběhl závěrečný TEST běh

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-4---zodolnění-api"></a>

# FÁZE 4 - Zodolnění API

**Stav:** Plánováno

**Odhad práce:** 5–8 hodin

<a id="cz-cíl-7"></a>

## Cíl

Přeměnit stávající FastAPI obálku na aplikační hranici bližší produkčnímu provozu.

Cílová struktura:

```text
app/
|
+-- main.py
+-- lifecycle.py
|
+-- api/
    +-- __init__.py
    +-- routes.py
    +-- dependencies.py
    +-- errors.py
    +-- middleware.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-41---životní-cyklus-aplikace"></a>

# FÁZE 4.1 - Životní cyklus aplikace

<a id="cz-soubor-24"></a>

## Soubor

```text
app/lifecycle.py
```

Hlavní funkce:

```python
lifespan(...)
```

Odpovědnosti:

```text
startup
->
load models
load vector store
initialize services

shutdown
->
release resources
```

---

<a id="cz-nový-koncept---fastapi-lifespan"></a>

## Nový koncept - FastAPI lifespan

Náročné modely se obvykle inicializují jednou při startu aplikace, ne zvlášť pro každý požadavek.

Přínosy:

- nižší latence
- menší paměťová režie
- jasnější životní cyklus prostředků
- jednodušší zjištění chyby při startu

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-42---routy"></a>

# FÁZE 4.2 - Routy

<a id="cz-soubor-25"></a>

## Soubor

```text
app/api/routes.py
```

Odpovědnosti:

```text
GET /health
POST /ask
```

Routy převádějí:

```text
HTTP
<->
application services
```

Nemají obsahovat implementaci retrievalu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-43---vkládání-závislostí"></a>

# FÁZE 4.3 - Vkládání závislostí

<a id="cz-soubor-26"></a>

## Soubor

```text
app/api/dependencies.py
```

Možné funkce:

```python
get_settings(...)
get_rag_service(...)
```

---

<a id="cz-nový-koncept---dependency-injection"></a>

## Nový koncept - Dependency injection

Místo vytváření závislostí v každém endpointu je může poskytnout FastAPI.

Přínosy:

- jednodušší testování
- méně globálního stavu
- zaměnitelné služby
- jasnější vlastnictví

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-44---chyby"></a>

# FÁZE 4.4 - Chyby

<a id="cz-soubor-27"></a>

## Soubor

```text
app/api/errors.py
```

Možné výjimky:

```python
InvalidQueryError
RetrievalError
GenerationError
```

Dále:

```text
FastAPI exception handlers
```

Cíl:

převádět interní selhání na řízené strukturované HTTP odpovědi.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-45---middleware"></a>

# FÁZE 4.5 - Middleware

<a id="cz-soubor-28"></a>

## Soubor

```text
app/api/middleware.py
```

Možné odpovědnosti:

- ID požadavku
- měření času požadavku
- základní HTTP logování

---

<a id="cz-fáze-4--podmínky-dokončení"></a>

## FÁZE 4 — Podmínky dokončení

- [ ] modely se inicializují jednou
- [ ] životní cyklus aplikace je definovaný
- [ ] routy jsou oddělené od aplikační logiky
- [ ] dependency injection se používá tam, kde je vhodná
- [ ] existují strukturované aplikační chyby
- [ ] existují ID požadavků
- [ ] měření času API je dostupné
- [ ] health endpoint je definovaný
- [ ] význam readiness je definovaný
- [ ] integrační testy API procházejí

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-5---produkční-inženýrství"></a>

# FÁZE 5 - Produkční inženýrství

**Stav:** Plánováno

**Odhad práce:** 10–16 hodin

<a id="cz-cíl-8"></a>

## Cíl

Zajistit reprodukovatelnost, pozorovatelnost, kontejnerizaci a nasaditelnost systému.

Fáze zahrnuje Python i infrastrukturu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-51---linux--wsl2"></a>

# FÁZE 5.1 - Linux / WSL2

<a id="cz-cíl-9"></a>

## Cíl

Ověřit funkčnost aplikace mimo vývojové prostředí Windows.

Úkoly:

- vytvořit prostředí Linux/WSL2
- nainstalovat závislosti
- spustit unit testy
- spustit ingest
- spustit API
- ověřit předpoklady o souborovém systému
- ověřit načítání modelů

---

<a id="cz-nový-koncept---přenositelnost-prostředí"></a>

## Nový koncept - Přenositelnost prostředí

Systém funkční pouze v jediném lokálním prostředí ještě není reprodukovatelný.

Kompatibilita s Linuxem připravuje projekt také pro Docker a cloudové nasazení.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-52---strukturované-logování"></a>

# FÁZE 5.2 - Strukturované logování

Cílová struktura:

```text
app/
+-- observability/
    +-- __init__.py
    +-- logging.py
    +-- metrics.py
    +-- middleware.py
```

---

<a id="cz-soubor-29"></a>

## Soubor

```text
app/observability/logging.py
```

Plánované funkce:

```python
configure_logging(...)
get_logger(...)
```

---

<a id="cz-nový-koncept---strukturované-logování"></a>

## Nový koncept - Strukturované logování

Namísto pouhého:

```text
"Retrieval finished"
```

může strukturovaná událost obsahovat:

```text
event = retrieval_complete
request_id = ...
latency_ms = 143
candidate_count = 30
```

Strukturované logy se snáze:

- prohledávají
- agregují
- monitorují
- automaticky analyzují

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-53---běhové-metriky"></a>

# FÁZE 5.3 - Běhové metriky

<a id="cz-soubor-30"></a>

## Soubor

```text
app/observability/metrics.py
```

Možné funkce:

```python
record_request(...)
record_latency(...)
record_retrieval_latency(...)
record_generation_latency(...)
record_error(...)
```

Provozní metriky mají zahrnovat:

- počet požadavků
- počet chyb
- latenci odpovědi
- latenci retrievalu
- latenci rerankingu
- latenci generování

Později tam, kde je to relevantní:

- spotřebu tokenů
- využití modelu
- cenu API

---

<a id="cz-nový-koncept---kvalitativní-a-provozní-metriky"></a>

## Nový koncept - Kvalitativní a provozní metriky

Metriky kvality:

```text
MRR
Hit@K
answer groundedness
```

Provozní metriky:

```text
latency
request count
error rate
resource usage
cost
```

Systém může dosahovat vysoké kvality retrievalu, ale nevyhovující produkční latence.

Důležité jsou oba rozměry.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-54---zodolnění-dockeru"></a>

# FÁZE 5.4 - Zodolnění Dockeru

Soubory:

```text
Dockerfile
compose.yaml
.dockerignore
```

Úkoly:

- reprodukovatelný build
- správná instalace závislostí
- explicitní konfigurace
- healthcheck
- uživatel bez oprávnění root
- omezení zbytečného obsahu obrazu

---

<a id="cz-nový-koncept---vícestupňový-docker-build"></a>

## Nový koncept - Vícestupňový Docker build

Build fáze může obsahovat nástroje potřebné jen pro sestavení závislostí.

Výsledný běhový obraz může obsahovat pouze to, co je nutné pro spuštění aplikace.

Možné přínosy:

- menší obraz
- menší útočná plocha
- čistší běhové prostředí

Použij pouze tehdy, přinese-li to projektu praktickou hodnotu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-55---cicd"></a>

# FÁZE 5.5 - CI/CD

Současné CI už spouští projektové testy.

Budoucí tok může být:

```text
push
    ->
tests
    ->
static checks
    ->
security checks
    ->
Docker build
    ->
deployment
```

Možná zlepšení:

- kontrola formátování
- Ruff
- typová kontrola
- coverage
- audit závislostí

---

<a id="cz-fáze-5--podmínky-dokončení"></a>

## FÁZE 5 — Podmínky dokončení

- [ ] aplikace funguje pod Linuxem / WSL2
- [ ] Docker build je reprodukovatelný
- [ ] kontejner úspěšně startuje
- [ ] healthcheck kontejneru funguje
- [ ] běh bez root oprávnění je nastavený
- [ ] CI spouští projektové testy
- [ ] existuje strukturované logování
- [ ] lze měřit latenci požadavku
- [ ] lze měřit latenci retrievalu
- [ ] lze měřit latenci generování
- [ ] postup nasazení je definovaný

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-6---bezpečnost"></a>

# FÁZE 6 - Bezpečnost

**Stav:** Plánováno

**Odhad práce:** 6–10 hodin

<a id="cz-cíl-10"></a>

## Cíl

Provést samostatnou důkladnou bezpečnostní revizi po vytvoření produkční architektury.

Bezpečnost se řeší i v předchozích fázích; FÁZE 6 provádí hlubší kontrolu.

Cílová struktura může obsahovat:

```text
app/
+-- security/
    +-- __init__.py
    +-- validation.py
    +-- limits.py
    +-- headers.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-61---modelování-hrozeb"></a>

# FÁZE 6.1 - Modelování hrozeb

<a id="cz-nový-koncept---model-hrozeb"></a>

## Nový koncept - Model hrozeb

Výslovně určit:

```text
assets
trust boundaries
attack surfaces
possible attackers
failure modes
impact
mitigations
```

Příklady systémových hranic:

```text
user
->
FastAPI

PDF corpus
->
PDF parser

environment variables
->
application configuration

RAG context
->
generation model
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-62---validace-běhových-vstupů"></a>

# FÁZE 6.2 - Validace běhových vstupů

<a id="cz-soubor-31"></a>

## Soubor

```text
app/security/validation.py
```

Možné funkce:

```python
validate_query(...)
validate_input_size(...)
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-63---běhové-limity"></a>

# FÁZE 6.3 - Běhové limity

<a id="cz-soubor-32"></a>

## Soubor

```text
app/security/limits.py
```

Možné limity:

```text
maximum query length
maximum context size
maximum top_k
maximum request size
```

Zde lze posoudit případné budoucí omezení frekvence požadavků.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-64---tajemství"></a>

# FÁZE 6.4 - Tajemství

Úkoly:

- ověřit, že Git neobsahuje tajemství
- používat proměnné prostředí
- definovat produkční strategii pro tajemství
- zkontrolovat `.env.example`
- nelogovat tajemství

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-65---bezpečnost-závislostí"></a>

# FÁZE 6.5 - Bezpečnost závislostí

Možné úkoly:

- skenování zranitelností
- revize závislostí
- strategie pinování verzí
- proces bezpečnostních aktualizací

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-66---bezpečnost-kontejneru"></a>

# FÁZE 6.6 - Bezpečnost kontejneru

Zkontrolovat:

- běh bez root oprávnění
- souborová oprávnění
- zveřejněné porty
- zbytečné balíčky
- zapisovatelné adresáře
- předávání tajemství
- útočnou plochu

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-67---bezpečnost-http"></a>

# FÁZE 6.7 - Bezpečnost HTTP

Zkontrolovat:

- CORS
- bezpečnostní hlavičky
- limity požadavků
- únik informací v chybách
- požadavky na autentizaci, bude-li zavedena

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-68---bezpečnost-specifická-pro-rag"></a>

# FÁZE 6.8 - Bezpečnost specifická pro RAG

<a id="cz-nový-koncept---nepřímá-prompt-injection"></a>

## Nový koncept - Nepřímá prompt injection

Vyhledaný dokument může obsahovat text jako:

```text
Ignore previous instructions...
```

Samotný dokument se stává nedůvěryhodným vstupem modelu.

Bezpečnostní revize má zvážit:

- oddělení instrukcí a vyhledaných dat
- sestavování promptu
- důvěryhodnost zdrojů
- chování modelu
- přístup k nástrojům v budoucích agentních systémech

---

<a id="cz-fáze-6--podmínky-dokončení"></a>

## FÁZE 6 — Podmínky dokončení

- [ ] model hrozeb je zdokumentovaný
- [ ] vstupní limity jsou zkontrolované
- [ ] hranice souborového systému jsou zkontrolované
- [ ] zpracování PDF je zkontrolované
- [ ] bezpečnost závislostí je zkontrolovaná
- [ ] správa tajemství je zkontrolovaná
- [ ] oprávnění kontejneru jsou zkontrolovaná
- [ ] běh bez root oprávnění je ověřený
- [ ] HTTP kontroly jsou zkontrolované
- [ ] nepřímá prompt injection je zkontrolovaná
- [ ] hlavní opatření jsou zdokumentovaná

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-7---produkční-verze-v1"></a>

# FÁZE 7 - Produkční verze v1

**Stav:** Plánováno

**Odhad práce:** 4–6 hodin

<a id="cz-cíl-11"></a>

## Cíl

Propojit dokončené vrstvy do první verze připomínající produkční vydání.

Produkční v1 neznamená úplnost podnikového řešení.

Znamená, že projekt je:

```text
reproducible
tested
deployable
observable
documented
reasonably hardened
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-71---health-a-readiness"></a>

# FÁZE 7.1 - Health a readiness

Možný soubor:

```text
app/health.py
```

Možné funkce:

```python
check_vector_store(...)
check_models(...)
build_readiness_status(...)
```

---

<a id="cz-nový-koncept---liveness-a-readiness"></a>

## Nový koncept - Liveness a readiness

<a id="cz-liveness--běh-procesu"></a>

### Liveness — běh procesu

Otázka:

```text
Is the process alive?
```

<a id="cz-readiness--připravenost-služby"></a>

### Readiness — připravenost služby

Otázka:

```text
Can the application actually serve a valid RAG request?
```

Aplikace může běžet, ale její model nebo vektorové úložiště nemusí být připravené.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-72---produkční-smoke-test"></a>

# FÁZE 7.2 - Produkční smoke test

<a id="cz-soubor-33"></a>

## Soubor

```text
scripts/production_smoke.py
```

Možný tok:

```text
health check
    ->
known question
    ->
validate HTTP response
    ->
validate answer structure
    ->
validate sources
    ->
record latency
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-73---dokumentace"></a>

# FÁZE 7.3 - Dokumentace

README má vysvětlovat:

- účel projektu
- shrnutí architektury
- instalaci
- přípravu prostředí
- ingest
- spuštění API
- spuštění testů
- použití Dockeru
- použití evaluace
- bezpečnostní hlediska

Odkazy:

```text
docs/ROADMAP.md
docs/ARCHITECTURE.md
docs/DEVELOPMENT_GUIDE.md
```

---

<a id="cz-fáze-7--podmínky-dokončení"></a>

## FÁZE 7 — Podmínky dokončení

V čistém prostředí lze:

- [ ] naklonovat repozitář
- [ ] nakonfigurovat proměnné prostředí
- [ ] nainstalovat nebo sestavit závislosti
- [ ] spustit aplikaci
- [ ] ingestovat korpus
- [ ] poslat dotaz do API
- [ ] získat podloženou odpověď se zdroji
- [ ] spustit testy
- [ ] spustit evaluaci
- [ ] vytvořit strukturované logy
- [ ] zpřístupnit běhové metriky
- [ ] postupovat podle zdokumentované instalace

V tomto bodě projekt dosahuje:

```text
Production v1
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-8---rozšíření"></a>

# FÁZE 8 - Rozšíření

FÁZE 8 začíná až po produkční v1.

Účelem je rozšířit dovednosti a schopnosti systému bez destabilizace hlavního RAG projektu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-8a---průzkum-agentů"></a>

# FÁZE 8A - Průzkum agentů

**Odhad práce:** 4–6 hodin

<a id="cz-cíl-12"></a>

## Cíl

Ukázat přechod z běžné RAG aplikace na agentní workflow.

První agent má používat existující RAG systém jako nástroj.

Cílová struktura:

```text
agent/
|
+-- __init__.py
+-- models.py
+-- tools.py
+-- agent.py
```

---

<a id="cz-soubor-34"></a>

## Soubor

```text
agent/tools.py
```

Příklad funkce:

```python
search_knowledge_base(
    question: str,
)
```

Možná implementace:

```text
agent
    ->
FastAPI /ask
```

nebo:

```text
agent
    ->
RAG service
```

---

<a id="cz-nový-koncept---volání-nástrojů"></a>

## Nový koncept - Volání nástrojů

Jazykový model už pouze negeneruje text.

Může rozhodnout:

```text
which tool to use
which arguments to provide
how to use the tool result
```

Příklad toku:

```text
user request
    ->
model decision
    ->
tool call
    ->
RAG system
    ->
tool result
    ->
final response
```

---

<a id="cz-fáze-8a--podmínky-dokončení"></a>

## FÁZE 8A — Podmínky dokončení

- [ ] existuje jeden agent
- [ ] agent umí zavolat existující RAG systém
- [ ] argumenty nástroje jsou strukturované
- [ ] výsledek nástroje se vrací modelu
- [ ] chování agenta je testovatelné
- [ ] rozsah zůstává záměrně malý

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-8b---sql-a-etl"></a>

# FÁZE 8B - SQL a ETL

**Odhad práce:** 6–10 hodin

<a id="cz-cíl-13"></a>

## Cíl

Po dokončení produkčního RAG systému doplnit praktické základy datového inženýrství.

Cílová struktura:

```text
data_pipeline/
|
+-- __init__.py
+-- database.py
+-- extract.py
+-- transform.py
+-- load.py
+-- pipeline.py
```

---

<a id="cz-soubor-35"></a>

## Soubor

```text
data_pipeline/database.py
```

Koncepty:

```text
database connections
SELECT
JOIN
GROUP BY
indexes
transactions
```

---

<a id="cz-soubor-36"></a>

## Soubor

```text
data_pipeline/extract.py
```

Možná funkce:

```python
extract_from_source(...)
```

---

<a id="cz-soubor-37"></a>

## Soubor

```text
data_pipeline/transform.py
```

Možné funkce:

```python
clean_records(...)
transform_records(...)
validate_records(...)
```

---

<a id="cz-soubor-38"></a>

## Soubor

```text
data_pipeline/load.py
```

Možná funkce:

```python
load_to_database(...)
```

---

<a id="cz-nový-koncept---etl"></a>

## Nový koncept - ETL

ETL znamená:

```text
Extract
    ->
Transform
    ->
Load
```

Jde o běžný vzor pipeline v datovém inženýrství.

---

<a id="cz-fáze-8b--podmínky-dokončení"></a>

## FÁZE 8B — Podmínky dokončení

- [ ] základní SQL workflow je implementované
- [ ] data lze extrahovat
- [ ] data lze transformovat
- [ ] existuje validace
- [ ] transformovaná data lze načíst do cíle
- [ ] jednoduchá ETL pipeline funguje od začátku do konce

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-8c---mlops"></a>

# FÁZE 8C - MLOps

**Odhad práce:** 8–12 hodin

<a id="cz-cíl-14"></a>

## Cíl

Zavést systematické sledování experimentů a modelů.

Možná struktura:

```text
mlops/
|
+-- __init__.py
+-- experiment.py
+-- artifacts.py
+-- model_metadata.py
```

---

<a id="cz-soubor-39"></a>

## Soubor

```text
mlops/experiment.py
```

Záznamy experimentů mají obsahovat:

- model
- parametry modelu
- konfiguraci retrievalu
- hash datasetu
- Git commit
- časové razítko
- metriky kvality
- provozní metriky
- metriky nákladů tam, kde jsou relevantní

---

<a id="cz-nový-koncept---sledování-experimentů"></a>

## Nový koncept - Sledování experimentů

Namísto:

```text
"This version seemed better."
```

ukládat:

```text
commit = abc123
dataset_hash = xyz456
embedding_model = ...
reranker = ...
MRR = 0.84
Hit@3 = 0.93
latency = 190 ms
```

Možná budoucí technologie:

```text
MLflow
```

Nejprve lze implementovat jednodušší lokální sledování experimentů.

---

<a id="cz-soubor-40"></a>

## Soubor

```text
mlops/artifacts.py
```

Možné odpovědnosti:

- evaluační artefakty
- metadata modelů
- snímky konfigurace
- výstupy běhů

---

<a id="cz-fáze-8c--podmínky-dokončení"></a>

## FÁZE 8C — Podmínky dokončení

- [ ] experimenty mají jedinečnou identitu
- [ ] verze datasetu se zaznamenává
- [ ] Git commit se zaznamenává
- [ ] konfigurace modelu se zaznamenává
- [ ] metriky kvality se zaznamenávají
- [ ] provozní metriky se zaznamenávají
- [ ] běhy lze porovnávat

---


[↑ Obsah / Contents](#obsah)

<a id="cz-fáze-8d---pokročilí-agenti"></a>

# FÁZE 8D - Pokročilí agenti

**Stav:** Budoucí

Podrobná architektura je záměrně odložena.

Možná témata:

- více nástrojů
- trvalý stav
- plánování
- grafy workflow
- lidské schvalování
- evaluace agentů
- koordinace více agentů

Technologie vybírej až po pochopení jednoduššího agentního workflow.

Tuto fázi nenavrhuj předčasně.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-původní-plánovací-odhady--historické"></a>

# Původní plánovací odhady — historické

Hodnoty jsou zachované z původního plánu. Nejde o aktuální předpověď zbývající práce ani termínový závazek; nové posouzení vyžaduje samostatné plánovací rozhodnutí.

Původní odhady aktivního vývoje (nepřepočítané):

| Fáze | Odhad času |
|---|---:|
| Dokončení FÁZE 1 | 2-4 h |
| FÁZE 2 — základ evaluace | 8-12 h |
| FÁZE 3 — refaktoring retrievalu | 8-14 h |
| FÁZE 4 — zodolnění API | 5-8 h |
| FÁZE 5 — produkční inženýrství | 10-16 h |
| FÁZE 6 — bezpečnost | 6-10 h |
| FÁZE 7 — produkční v1 | 4-6 h |
| FÁZE 8A — průzkum agentů | 4-6 h |
| FÁZE 8B — SQL / ETL | 6-10 h |
| FÁZE 8C — MLOps | 8-12 h |

Původní odhad zbývající práce do produkční v1:

```text
43-70 hours
```

Tyto odhady zahrnují:

- implementaci
- vysvětlení
- ruční zápis kódu
- testování
- ladění
- integraci

Nejde o odhady samotného psaní kódu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-historie-plánování"></a>

## Historie plánování

Předchozí stav FÁZE 2A a podrobný seznam nejbližších úkolů zůstávají v [roadmapě před zkrácením](https://github.com/jyenten/AI_roadmap/blob/d7c3b4f71711c798646bd0a878b96b9c46c92d93/rag_api_project/docs/ROADMAP.md#historical-project-status-original-phase-2a-plan). Popisují starší bod, nikoli dnešní další kroky. Dokončená práce je v [LEARNING_LOG.md](../../LEARNING_LOG.md#cz); aktuální zaměření patří pouze do [aktuálního zaměření vývoje](#cz-aktuální-zaměření-vývoje) této roadmapy.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
