<a id="top"></a>

# AI RAG Project Architecture

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Přehled implementace k 28. 10. 2026](#cz-přehled-implementace-k-28-10-2026)
- [Identita a hranice evaluace](#cz-identita-a-hranice-evaluace)
- [1. Účel](#cz-1-účel)
- [2. Architektonické principy](#cz-2-architektonické-principy)
- [3. Celková architektura systému](#cz-3-celková-architektura-systému)
- [4. Offline datová pipeline](#cz-4-offline-datová-pipeline)
- [5. Běhová aplikace](#cz-5-běhová-aplikace)
- [6. Cílová architektura retrievalu](#cz-6-cílová-architektura-retrievalu)
- [7. Architektura generování](#cz-7-architektura-generování)
- [8. Koordinace RAG](#cz-8-koordinace-rag)
- [9. Architektura API](#cz-9-architektura-api)
- [10. Architektura evaluace](#cz-10-architektura-evaluace)
- [11. Role evaluačních datasetů](#cz-11-role-evaluačních-datasetů)
- [12. Průběh evaluace](#cz-12-průběh-evaluace)
- [13. Univerzální průzkumník dokumentů](#cz-13-univerzální-průzkumník-dokumentů)
- [14. Tok dat průzkumníku dokumentů](#cz-14-tok-dat-průzkumníku-dokumentů)
- [15. Modely vyhledávání v dokumentech](#cz-15-modely-vyhledávání-v-dokumentech)
- [16. Bezpečnostní hranice průzkumníku dokumentů](#cz-16-bezpečnostní-hranice-průzkumníku-dokumentů)
- [17. Bezpečnostní architektura](#cz-17-bezpečnostní-architektura)
- [18. Architektura observability](#cz-18-architektura-observability)
- [19. Architektura testování](#cz-19-architektura-testování)
- [20. Architektura infrastruktury](#cz-20-architektura-infrastruktury)
- [21. Směr závislostí](#cz-21-směr-závislostí)
- [22. Veřejná rozhraní](#cz-22-veřejná-rozhraní)
- [23. Současný technický dluh](#cz-23-současný-technický-dluh)
- [24. Cílová struktura projektu](#cz-24-cílová-struktura-projektu)
- [25. Pravidlo změn architektury](#cz-25-pravidlo-změn-architektury)
- [26. Historické architektonické zaměření fáze 2A](#cz-26-historické-architektonické-zaměření-fáze-2a)

**English**

- [Current implementation snapshot (2026-10-28)](#en-current-implementation-snapshot-2026-10-28)
- [Identity and evaluation boundary](#en-identity-and-evaluation-boundary)
- [1. Purpose](#en-1-purpose)
- [2. Architectural Principles](#en-2-architectural-principles)
- [3. High-Level System Architecture](#en-3-high-level-system-architecture)
- [4. Offline Data Pipeline](#en-4-offline-data-pipeline)
- [5. Runtime Application](#en-5-runtime-application)
- [6. Target Retrieval Architecture](#en-6-target-retrieval-architecture)
- [7. Generation Architecture](#en-7-generation-architecture)
- [8. RAG Orchestration](#en-8-rag-orchestration)
- [9. API Architecture](#en-9-api-architecture)
- [10. Evaluation Architecture](#en-10-evaluation-architecture)
- [11. Evaluation Dataset Roles](#en-11-evaluation-dataset-roles)
- [12. Evaluation Flow](#en-12-evaluation-flow)
- [13. Universal Document Explorer](#en-13-universal-document-explorer)
- [14. Document Explorer Data Flow](#en-14-document-explorer-data-flow)
- [15. Document Search Models](#en-15-document-search-models)
- [16. Document Explorer Security Boundary](#en-16-document-explorer-security-boundary)
- [17. Security Architecture](#en-17-security-architecture)
- [18. Observability Architecture](#en-18-observability-architecture)
- [19. Testing Architecture](#en-19-testing-architecture)
- [20. Infrastructure Architecture](#en-20-infrastructure-architecture)
- [21. Dependency Direction](#en-21-dependency-direction)
- [22. Public Interfaces](#en-22-public-interfaces)
- [23. Current Technical Debt](#en-23-current-technical-debt)
- [24. Target Project Structure](#en-24-target-project-structure)
- [25. Architecture Change Rule](#en-25-architecture-change-rule)
- [26. Historical Phase 2A Architectural Focus](#en-26-historical-phase-2a-architectural-focus)

</details>

---

<a id="en"></a>
## EN — English


[↑ Obsah / Contents](#obsah)

<a id="en-current-implementation-snapshot-2026-10-28"></a>

## Current implementation snapshot (2026-10-28)

The sections marked **target** below describe planned design, not necessarily shipped code. The default `main` branch currently contains:

- Runtime: `app/main.py`, `app/rag.py`, `app/retrieval.py` for the existing FastAPI RAG path.
- Experiment retrievers: `app/retrievers/vector.py` and `app/retrievers/bm25.py` over the same Chroma collection.
- Offline evaluation: `scripts/evaluate_retrieval.py` selects `legacy`, `vector` or `bm25` on DEV/RANDOM.
- Evidence: `evaluation/evidence.py`, `evaluation/candidates.py`, approved JSON datasets and independent page-based `scripts/search_pdf.py`.
- Hybrid RRF is **in progress** and is not yet an established selectable CLI or `/ask` mode.
- PDF ingestion `scripts/ingest.py` **deletes and recreates** its target Chroma collection.

Architecture boundaries: the standalone page explorer is not the chunk-level BM25 retriever; retrieval evaluation is independent of the HTTP answer pipeline; no raw BM25 relevance score may be added directly to vector distances. The separate bilingual [OPERATIONS.md](OPERATIONS.md) and [EVALUATION.md](EVALUATION.md) contain verified commands and golden-evidence governance.


[↑ Obsah / Contents](#obsah)

<a id="en-identity-and-evaluation-boundary"></a>

## Identity and evaluation boundary

A Chroma chunk has an `id` distinct from `chunk_index`. `source`, physical `page` and chunk metadata preserve provenance. Planned hybrid fusion should match the same chunk by stable Chroma ID, not by text equality or page number alone. When changes to retrieval ranking or chunk identity are introduced, compare DEV and RANDOM results under controlled corpus/configuration and keep TEST held out.

---



[↑ Obsah / Contents](#obsah)

<a id="en-1-purpose"></a>

## 1. Purpose

This document describes the architecture of the AI RAG project.

It defines:

- major system components
- module responsibilities
- dependency boundaries
- public interfaces between subsystems
- data flow
- evaluation architecture
- security boundaries
- future target structure

The architecture should remain domain-independent wherever possible.

Domain-specific behavior must not be embedded into generic retrieval,
evaluation, document loading, or infrastructure components.

---


[↑ Obsah / Contents](#obsah)

<a id="en-2-architectural-principles"></a>

## 2. Architectural Principles

The project follows the architectural principles described below.

### 2.1 Separation of Concerns

Each module should have one primary responsibility.

Examples:

```text
PDF loading
≠
text normalization
≠
retrieval
≠
reranking
≠
generation
≠
API transport
```

A module should not contain unrelated responsibilities simply because
they are currently used together.

---

### 2.2 Explicit Module Boundaries

Higher-level modules should interact with lower-level subsystems through
defined public interfaces.

Preferred:

```text
RAG service
    ↓
retrieval service
    ↓
retrieval internals
```

Not preferred:

```text
RAG service
    ↓
embedding model
    ↓
ChromaDB internals
    ↓
reranker internals
    ↓
scoring helpers
```

The caller should not need to understand implementation details of the
subsystem it uses.

---

### 2.3 Domain Independence

Generic infrastructure must not depend on OSPF-specific terms or rules.

For example, generic components must not contain hardcoded logic for:

```text
OSPF
DROTHER
designated router
virtual links
Cisco-specific terminology
```

Such terms may appear in:

- source documents
- evaluation datasets
- user queries

but not in generic ranking or infrastructure code.

---

### 2.4 Prefer Immutable Data

Data objects that represent facts should be immutable whenever practical.

Examples:

```text
PageDocument
SearchResult
RetrievedChunk
EvaluationQuestion
GoldEvidence
```

Preferred implementation:

```python
@dataclass(frozen=True)
```

This reduces accidental state changes and makes the system easier to
reason about and test.

---

### 2.5 Configuration Outside Business Logic

Configuration should be centralized.

Examples:

```text
model names
retrieval limits
collection names
file limits
API settings
security limits
```

Business logic should not contain duplicated hardcoded configuration.

---

### 2.6 Measure Before Optimizing

Retrieval changes must be evaluated using the evaluation framework.

The project should not introduce ranking heuristics only because they
appear useful for one manually inspected query.

Development flow:

```text
baseline
    ↓
measurement
    ↓
change
    ↓
measurement
    ↓
comparison
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-3-high-level-system-architecture"></a>

## 3. High-Level System Architecture

The main runtime architecture is:

```text
                         USER / CLIENT
                              │
                              ▼
                           FastAPI
                              │
                              ▼
                         RAG SERVICE
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
         RETRIEVAL SERVICE              GENERATION
                │                           │
                ▼                           │
         VECTOR RETRIEVAL                   │
                │                           │
                ▼                           │
            RERANKING                       │
                │                           │
                ▼                           │
       SELECTED CONTEXT ────────────────────┘
                │
                ▼
          FINAL RESPONSE
                │
                ▼
        ANSWER + SOURCES
```

The runtime application does not directly depend on the evaluation
system or the document explorer.

---


[↑ Obsah / Contents](#obsah)

<a id="en-4-offline-data-pipeline"></a>

## 4. Offline Data Pipeline

The ingestion pipeline is separate from online query processing.

```text
PDF DOCUMENTS
      │
      ▼
TEXT EXTRACTION
      │
      ▼
PREPROCESSING
      │
      ▼
CHUNKING
      │
      ▼
EMBEDDING
      │
      ▼
VECTOR STORE
   ChromaDB
```

Current implementation:

```text
scripts/ingest.py
```

Future refactoring may split ingestion into additional modules, but this
is not required until measurements or complexity justify it.

---


[↑ Obsah / Contents](#obsah)

<a id="en-5-runtime-application"></a>

## 5. Runtime Application

Current application structure:

```text
app/
├── __init__.py
├── config.py
├── generation.py
├── main.py
├── rag.py
├── retrieval.py
└── schemas.py
```

Current responsibilities are described below.

---

### 5.1 `app/config.py`

Owns application configuration.

Examples:

```text
embedding model
reranker model
generation model
Chroma collection
candidate count
returned result count
context limits
```

Target rule:

Other modules should read configuration rather than duplicate constants.

---

### 5.2 `app/schemas.py`

Owns external API data schemas.

Examples:

```text
QuestionRequest
SourceChunk
AnswerResponse
```

These schemas describe data exchanged across the HTTP boundary.

They are separate from internal retrieval models.

For example:

```text
API SourceChunk
```

does not need to be identical to:

```text
internal RetrievalResult
```

---

### 5.3 `app/retrieval.py`

Current retrieval implementation.

Current responsibilities include several concerns:

```text
query processing
embedding retrieval
candidate selection
reranking
heuristic scoring
result selection
```

This file remains operational alongside the experiment retrievers in `app/retrievers/`.

The approved PHASE 3 target proposes decomposition into:

```text
app/
└── retrieval/
    ├── __init__.py
    ├── models.py
    ├── embeddings.py
    ├── vector_search.py
    ├── query.py
    ├── reranker.py
    ├── scoring.py
    └── service.py
```

The final public entry point should be located in:

```text
app/retrieval/service.py
```

with an interface similar to:

```python
retrieve(
    query: str,
) -> list[RetrievalResult]
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-6-target-retrieval-architecture"></a>

## 6. Target Retrieval Architecture

The planned retrieval flow is:

```text
QUERY
  │
  ▼
query.py
normalize / prepare query
  │
  ▼
embeddings.py
query embedding
  │
  ▼
vector_search.py
retrieve candidate chunks
  │
  ▼
reranker.py
CrossEncoder scoring
  │
  ▼
scoring.py
optional score combination
  │
  ▼
service.py
select TOP K results
  │
  ▼
RetrievalResult
```

Each layer has one primary responsibility.

---

### 6.1 `retrieval/models.py`

Internal retrieval data models.

Planned types:

```text
RetrievedChunk
ScoredChunk
RetrievalResult
```

These models represent internal retrieval data and should not depend on
FastAPI.

---

### 6.2 `retrieval/embeddings.py`

Owns embedding-model operations.

Functions may include:

```python
load_embedding_model()
embed_query()
embed_documents()
```

This module must not know how FastAPI works.

It should also not decide final ranking.

---

### 6.3 `retrieval/vector_search.py`

Owns communication with the vector store.

Functions may include:

```python
search_vector_store()
convert_chroma_results()
```

Chroma-specific result formats should be converted into project-owned
data models here.

Higher layers should not depend directly on Chroma response structure.

---

### 6.4 `retrieval/query.py`

Owns generic query preparation.

Possible functions:

```python
normalize_query()
```

Query expansion may only be added if evaluation demonstrates a measurable
benefit.

Domain-specific expansion rules must not be hardcoded into the generic
retrieval layer.

---

### 6.5 `retrieval/reranker.py`

Owns CrossEncoder reranking.

Functions:

```python
load_reranker()
rerank()
```

Input:

```text
query
+
candidate chunks
```

Output:

```text
scored candidates
```

---

### 6.6 `retrieval/scoring.py`

Owns score combination if score fusion is required.

This layer exists specifically to prevent scoring rules from being
distributed throughout the retrieval pipeline.

Any combination of:

```text
vector score
CrossEncoder score
other retrieval score
```

must account for score scale and meaning.

Raw incompatible scores must not simply be added together.

---

### 6.7 `retrieval/service.py`

Public retrieval interface.

It orchestrates retrieval internals:

```text
query
↓
candidate retrieval
↓
reranking
↓
score handling
↓
TOP K
```

Other application layers should primarily depend on this service rather
than individual retrieval internals.

---


[↑ Obsah / Contents](#obsah)

<a id="en-7-generation-architecture"></a>

## 7. Generation Architecture

Current file:

```text
app/generation.py
```

Current responsibility:

```text
question
+
retrieved context
↓
prompt
↓
generation model
↓
answer
```

Possible future internal separation:

```text
prompt construction
model inference
output processing
```

This split should only be introduced if complexity justifies it.

---


[↑ Obsah / Contents](#obsah)

<a id="en-8-rag-orchestration"></a>

## 8. RAG Orchestration

Current file:

```text
app/rag.py
```

The RAG layer coordinates other services.

Target responsibility:

```text
question
    │
    ▼
retrieval service
    │
    ▼
context construction
    │
    ▼
generation service
    │
    ▼
answer + sources
```

The RAG layer must not implement:

```text
vector search details
embedding internals
CrossEncoder internals
Chroma response parsing
HTTP transport
```

Its role is orchestration.

---


[↑ Obsah / Contents](#obsah)

<a id="en-9-api-architecture"></a>

## 9. API Architecture

Current entry point:

```text
app/main.py
```

Target PHASE 4 structure:

```text
app/
├── main.py
├── lifecycle.py
│
└── api/
    ├── __init__.py
    ├── routes.py
    ├── dependencies.py
    ├── errors.py
    └── middleware.py
```

---

### 9.1 `app/main.py`

Should eventually become a small composition root.

Responsibilities:

```text
create FastAPI application
register routes
register middleware
register lifecycle
register exception handlers
```

It should not contain business logic.

---

### 9.2 `app/lifecycle.py`

Owns process lifecycle.

Examples:

```text
startup
↓
load models
load vector store
initialize services

shutdown
↓
release resources
```

Models should normally be initialized once, not once per HTTP request.

---

### 9.3 `app/api/routes.py`

Owns HTTP routes.

Examples:

```text
GET /health
POST /ask
```

Routes should translate:

```text
HTTP
↔
application services
```

but should not implement retrieval logic.

---

### 9.4 `app/api/dependencies.py`

Owns FastAPI dependency injection.

Possible interfaces:

```python
get_settings()
get_rag_service()
```

This allows application components to be replaced during testing without
rewriting endpoints.

---

### 9.5 `app/api/errors.py`

Owns application/API error translation.

Examples:

```text
InvalidQueryError
RetrievalError
GenerationError
```

Internal exceptions can be mapped to controlled HTTP responses.

---

### 9.6 `app/api/middleware.py`

Possible responsibilities:

```text
request ID
request timing
basic HTTP logging
```

Middleware should handle cross-cutting HTTP concerns rather than business
logic.

---


[↑ Obsah / Contents](#obsah)

<a id="en-10-evaluation-architecture"></a>

## 10. Evaluation Architecture

Evaluation is independent from the runtime application.

Target structure:

```text
evaluation/
├── __init__.py
├── models.py
├── dataset.py
├── evidence.py
├── metrics.py
├── runner.py
├── history.py
└── random_eval.py
```

Primary rule:

```text
evaluation measures retrieval
```

but:

```text
retrieval must not depend on evaluation
```

Dependency direction:

```text
evaluation
    ↓
retrieval
```

Never:

```text
retrieval
    ↓
evaluation
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-11-evaluation-dataset-roles"></a>

## 11. Evaluation Dataset Roles

Three dataset categories are intentionally separated.

### DEV

Used during development.

May influence design and tuning.

The DEV dataset is allowed to influence implementation decisions.

---

### RANDOM

Used for:

```text
robustness exploration
unexpected failure discovery
coverage exploration
```

Random sampling must be reproducible through a stored seed.

---

### TEST

Held-out evaluation.

TEST must not become another tuning dataset.

Repeated manual inspection of TEST results during optimization would
reduce its value as an independent generalization check.

---


[↑ Obsah / Contents](#obsah)

<a id="en-12-evaluation-flow"></a>

## 12. Evaluation Flow

```text
EvaluationQuestion
       │
       ▼
retrieval service
       │
       ▼
ranked results
       │
       ▼
gold evidence matching
       │
       ▼
rank of correct evidence
       │
       ▼
metrics
       │
       ├── Hit@K
       └── MRR
```

Evaluation run metadata should also contain:

```text
Git commit
working-tree dirty state
dataset hash
timestamp
configuration
```

This makes results reproducible and comparable.

---


[↑ Obsah / Contents](#obsah)

<a id="en-13-universal-document-explorer"></a>

## 13. Universal Document Explorer

The document explorer is not part of the runtime RAG retrieval path.

Its purpose is:

```text
corpus exploration
+
gold evidence discovery
+
manual benchmark construction
```

Target structure:

```text
document_search/
├── __init__.py
├── models.py
├── normalize.py
├── tokenize.py
├── load_pages.py
├── build_index.py
├── search.py
│
└── security/
    ├── __init__.py
    ├── paths.py
    ├── pdf_validation.py
    └── input_validation.py
```

CLI:

```text
scripts/search_pdf.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-14-document-explorer-data-flow"></a>

## 14. Document Explorer Data Flow

```text
PDF CORPUS
    │
    ▼
security validation
    │
    ▼
load_pdf_pages()
    │
    │ list[PageDocument]
    ▼
normalize_text()
    │
    ▼
tokenize()
    │
    ▼
build_bm25_index()
    │
    │ BM25SearchIndex
    ▼
search_pages()
    │
    │ list[SearchResult]
    ▼
CLI
    │
    ▼
human evidence validation
    │
    ▼
evaluation dataset
```

This architecture intentionally differs from the RAG retrieval stack.

Document exploration:

```text
BM25 lexical retrieval
+
human validation
```

Main RAG:

```text
embedding retrieval
+
CrossEncoder reranking
```

This separation reduces circular benchmark construction.

---


[↑ Obsah / Contents](#obsah)

<a id="en-15-document-search-models"></a>

## 15. Document Search Models

### 15.1 `PageDocument`

Represents one source page.

Conceptually:

```python
PageDocument(
    source="manual.pdf",
    page=26,
    text="...",
)
```

The combination:

```text
source
+
page
+
text
```

represents the identity and content of the searchable source unit.

---

### 15.2 `SearchResult`

Represents a ranked search result.

Conceptually:

```text
document
+
score
```

The result should reference the original `PageDocument` rather than
duplicate document metadata across multiple structures.

---

### 15.3 `BM25SearchIndex`

Owns:

```text
page corpus
+
BM25 model
```

The rest of the application should not need to manage these two objects
independently.

---


[↑ Obsah / Contents](#obsah)

<a id="en-16-document-explorer-security-boundary"></a>

## 16. Document Explorer Security Boundary

The PDF corpus is treated as external input.

Security flow:

```text
filesystem input
      │
      ▼
path validation
      │
      ▼
file validation
      │
      ▼
resource limits
      │
      ▼
PDF parser
```

Important controls:

```text
allowed directory boundary
path traversal prevention
symlink resolution
PDF extension validation
PDF signature validation
file size limits
page count limits
query limits
top_k limits
```

Security validation must not silently modify document semantics.

If a document cannot be safely or completely loaded, the failure should
be explicit.

---


[↑ Obsah / Contents](#obsah)

<a id="en-17-security-architecture"></a>

## 17. Security Architecture

Security is a cross-cutting concern.

Some controls belong close to the data source:

```text
document_search/security/
```

Other controls belong to the runtime application:

```text
app/security/
```

Future target:

```text
app/
└── security/
    ├── __init__.py
    ├── validation.py
    ├── limits.py
    └── headers.py
```

Security is not implemented through getters and setters.

Primary mechanisms include:

```text
input validation
immutability
filesystem boundaries
resource limits
dependency controls
secrets handling
permissions
container isolation
HTTP controls
```

---

### 17.1 Future Threat Modeling

A dedicated security phase should identify:

```text
assets
trust boundaries
attack surfaces
possible attackers
failure modes
impact
mitigations
```

RAG-specific threats may include:

```text
indirect prompt injection
malicious document content
resource exhaustion
unsafe file handling
oversized requests
dependency vulnerabilities
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-18-observability-architecture"></a>

## 18. Observability Architecture

Target structure:

```text
app/
└── observability/
    ├── __init__.py
    ├── logging.py
    ├── metrics.py
    └── middleware.py
```

Observability should cover both quality and operation.

Operational metrics include:

```text
request count
error count
response latency
retrieval latency
reranking latency
generation latency
```

Where relevant:

```text
token usage
model usage
cost
```

Observability must not change retrieval results.

---

### 18.1 Structured Logging

Runtime logs should eventually contain structured fields such as:

```text
request_id
event
latency_ms
candidate_count
model
error_type
```

rather than relying only on free-form text.

---

### 18.2 Quality Metrics vs Operational Metrics

Quality metrics:

```text
MRR
Hit@K
groundedness
answer quality
```

Operational metrics:

```text
latency
request count
error rate
resource usage
token usage
cost
```

These measure different aspects of the system and should not be mixed.

---


[↑ Obsah / Contents](#obsah)

<a id="en-19-testing-architecture"></a>

## 19. Testing Architecture

Current tests live in:

```text
tests/
```

Future tests should increasingly mirror production modules.

Example:

```text
document_search/normalize.py
        ↕
tests/document_search/test_normalize.py
```

and:

```text
document_search/search.py
        ↕
tests/document_search/test_search.py
```

Testing layers:

```text
UNIT TESTS
    ↓
individual functions/modules

INTEGRATION TESTS
    ↓
multiple modules together

SMOKE TESTS
    ↓
basic end-to-end system operation

EVALUATION
    ↓
retrieval quality
```

These are different responsibilities.

A passing unit test does not prove retrieval quality.

A good MRR score does not prove API correctness.

---

### 19.1 Test Independence

Where practical, unit tests should avoid depending on:

```text
large real PDF corpora
network access
production vector databases
external APIs
```

Small synthetic inputs should be preferred for deterministic unit tests.

Real corpus tests belong in integration or manual validation workflows.

---


[↑ Obsah / Contents](#obsah)

<a id="en-20-infrastructure-architecture"></a>

## 20. Infrastructure Architecture

Current infrastructure includes:

```text
Dockerfile
compose.yaml
.github/workflows/ci.yml
```

Target production path:

```text
SOURCE CODE
    │
    ▼
Git
    │
    ▼
CI
    │
    ├── tests
    ├── static checks
    └── later security checks
    │
    ▼
Docker image
    │
    ▼
deployment
    │
    ▼
runtime monitoring
```

---

### 20.1 Container Architecture

Future production containers should aim for:

```text
reproducible builds
minimal runtime dependencies
non-root execution
health checks
explicit configuration
small attack surface
```

Multi-stage Docker builds may be introduced when useful.

---

### 20.2 CI/CD

Current CI primarily validates the project.

Future CI/CD may extend the flow to:

```text
push
↓
tests
↓
static checks
↓
security checks
↓
image build
↓
deployment
```

Deployment automation should be added only after the runtime architecture
is stable enough to deploy reliably.

---


[↑ Obsah / Contents](#obsah)

<a id="en-21-dependency-direction"></a>

## 21. Dependency Direction

The intended dependency direction is:

```text
API
 ↓
RAG
 ↓
Retrieval / Generation
 ↓
Models / Infrastructure integrations
```

Evaluation may call retrieval:

```text
Evaluation
    ↓
Retrieval
```

Document explorer is independent:

```text
Document Explorer
    ↓
PDF / BM25 libraries
```

The following dependency directions should be avoided:

```text
retrieval → API
retrieval → evaluation
generation → FastAPI
document_search → RAG
document_search → OSPF logic
```

This reduces coupling.

---


[↑ Obsah / Contents](#obsah)

<a id="en-22-public-interfaces"></a>

## 22. Public Interfaces

The architecture should expose a small number of stable entry points.

Planned examples are listed below.

### 22.1 Document Search

```python
load_pdf_pages(...)
build_bm25_index(...)
search_pages(...)
```

---

### 22.2 Retrieval

```python
retrieve(...)
```

---

### 22.3 RAG

Conceptually:

```python
answer_question(...)
```

---

### 22.4 Evaluation

Conceptually:

```python
evaluate_dataset(...)
```

Internal helper functions may change without requiring all callers to
change.

---


[↑ Obsah / Contents](#obsah)

<a id="en-23-current-technical-debt"></a>

## 23. Current Technical Debt

Known architectural debt is documented below.

### 23.1 Retrieval

Current:

```text
app/retrieval.py
```

contains multiple responsibilities and domain-specific rules.

Resolution:

```text
PHASE 3
```

---

### 23.2 RAG

Current:

```text
app/rag.py
```

contains OSPF-specific behavior.

Resolution:

```text
PHASE 3
```

---

### 23.3 Evaluation — foundation implemented

Reusable dataset loading, evidence matching, metrics, latency and history already live in `evaluation/`; CLI orchestration remains in `scripts/`. The older `scripts.evaluate_random` still contains history-path, Git-status and metric-output defects. The supported comparison workflow is `scripts.evaluate_retrieval` on DEV/RANDOM; see [EVALUATION.md](EVALUATION.md).

---

### 23.4 Document Search — historical prototype replaced

The previous heuristic search prototype experimented with:

```text
required terms
boost terms
manual proximity scoring
anchor terms
manual exclusions
```

That historical prototype has been replaced by the generic page-based BM25 implementation in `document_search/`.

Current discovery workflow:

```text
generic BM25 search
+
human evidence validation
```

Source-PDF evidence still requires human validation, independently of search ranking.

---

### 23.5 Ingestion

The current ingestion pipeline remains concentrated in:

```text
scripts/ingest.py
```

This is acceptable for the current phase.

It should only be decomposed when:

```text
complexity increases
testing becomes difficult
reuse is required
or measurements expose a concrete problem
```

Avoid refactoring ingestion only for architectural symmetry.

---


[↑ Obsah / Contents](#obsah)

<a id="en-24-target-project-structure"></a>

## 24. Target Project Structure

Long-term target structure:

```text
rag_api_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── lifecycle.py
│   ├── schemas.py
│   ├── generation.py
│   ├── rag.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── middleware.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── embeddings.py
│   │   ├── vector_search.py
│   │   ├── query.py
│   │   ├── reranker.py
│   │   ├── scoring.py
│   │   └── service.py
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   └── middleware.py
│   │
│   └── security/
│       ├── __init__.py
│       ├── validation.py
│       ├── limits.py
│       └── headers.py
│
├── document_search/
│   ├── __init__.py
│   ├── models.py
│   ├── normalize.py
│   ├── tokenize.py
│   ├── load_pages.py
│   ├── build_index.py
│   ├── search.py
│   │
│   └── security/
│       ├── __init__.py
│       ├── paths.py
│       ├── pdf_validation.py
│       └── input_validation.py
│
├── evaluation/
│   ├── __init__.py
│   ├── models.py
│   ├── dataset.py
│   ├── evidence.py
│   ├── metrics.py
│   ├── runner.py
│   ├── history.py
│   └── random_eval.py
│
├── scripts/
│   ├── __init__.py
│   ├── ingest.py
│   ├── search_pdf.py
│   ├── evaluate_retrieval.py
│   ├── production_smoke.py
│   └── git_check.py
│
├── tests/
│   ├── document_search/
│   ├── evaluation/
│   ├── retrieval/
│   ├── integration/
│   └── test_smoke.py
│
├── eval/
│   ├── dev_questions.json
│   ├── random/
│   └── test_questions.json
│
├── docs/
│   ├── ROADMAP.md
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT_GUIDE.md
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── README.md
└── .env.example
```

This is a target structure.

Directories should be created only when their corresponding development
phase begins.

The project should not create empty architecture merely to match the
diagram.

---


[↑ Obsah / Contents](#obsah)

<a id="en-25-architecture-change-rule"></a>

## 25. Architecture Change Rule

Architecture may evolve.

However, significant architecture changes should follow this process:

```text
identify concrete problem
        ↓
measure or demonstrate problem
        ↓
propose architectural change
        ↓
update architecture documentation
        ↓
implement change
        ↓
test
```

Architecture should not be changed only because another design appears
more sophisticated.

The simplest architecture that satisfies current requirements is
preferred.

---


[↑ Obsah / Contents](#obsah)

<a id="en-26-historical-phase-2a-architectural-focus"></a>

## 26. Historical Phase 2A Architectural Focus

The sequence below preserves the original plan. It is no longer the active step; see the [current implementation snapshot](#current-implementation-snapshot-2026-10-28) and [current development focus](ROADMAP.md#current-development-focus). The current work is the hybrid RRF experiment described in the development log; this does not renumber the approved roadmap.

Current development phase:

```text
PHASE 2 — Evaluation Foundation
```

Current architectural task:

```text
PHASE 2A — Universal Document Explorer
```

Immediate target:

```text
document_search/
```

with:

```text
immutable data models
domain-independent text processing
safe PDF loading
BM25 retrieval
small public API
unit tests
```

The main RAG retrieval implementation remains unchanged until the
evaluation foundation is sufficiently complete.

The next architectural milestone is:

```text
PHASE 2A.0
architecture freeze

↓

PHASE 2A.1
document_search/models.py
```


---

<a id="cz"></a>
## CZ — Česká verze


[↑ Obsah / Contents](#obsah)

<a id="cz-přehled-implementace-k-28-10-2026"></a>

## Přehled implementace k 28. 10. 2026

Části níže označené jako **cílové** popisují plánovaný návrh, nikoli nutně hotový kód. Výchozí větev `main` nyní obsahuje:

- Běhová aplikace: `app/main.py`, `app/rag.py`, `app/retrieval.py` pro existující FastAPI RAG pipeline.
- Experimentální retrievery: `app/retrievers/vector.py` a `app/retrievers/bm25.py` nad stejnou Chroma kolekcí.
- Offline evaluace: `scripts/evaluate_retrieval.py` vybírá `legacy`, `vector` nebo `bm25` pro DEV/RANDOM.
- Evidence: `evaluation/evidence.py`, `evaluation/candidates.py`, schválené JSON datasety a nezávislý stránkový průzkumník `scripts/search_pdf.py`.
- Hybridní RRF je **rozpracovaný** a zatím není zavedeným volitelným režimem CLI ani `/ask`.
- Ingest PDF v `scripts/ingest.py` cílovou Chroma kolekci **smaže a znovu vytvoří**.

Hranice architektury: samostatný průzkumník stránek není chunkový BM25 retriever; evaluace retrievalu je nezávislá na HTTP pipeline odpovědi; surové skóre relevance BM25 se nesmí přímo sčítat s vektorovými vzdálenostmi. Samostatné dvojjazyčné dokumenty [OPERATIONS.md](OPERATIONS.md#cz) a [EVALUATION.md](EVALUATION.md#cz) obsahují ověřené příkazy a pravidla správy golden evidence.


[↑ Obsah / Contents](#obsah)

<a id="cz-identita-a-hranice-evaluace"></a>

## Identita a hranice evaluace

Chunk v Chroma má `id` odlišné od `chunk_index`. `source`, fyzická `page` a metadata chunku uchovávají původ. Plánovaná hybridní fúze má spojovat stejný chunk podle stabilního Chroma ID, nikoli pouze podle shodného textu nebo čísla stránky. Při změně řazení retrievalu nebo identity chunku porovnej DEV a RANDOM za kontrolovaných podmínek korpusu a konfigurace; TEST ponech stranou.

---



[↑ Obsah / Contents](#obsah)

<a id="cz-1-účel"></a>

## 1. Účel

Tento dokument popisuje architekturu projektu AI RAG.

Vymezuje:

- hlavní součásti systému
- odpovědnosti modulů
- hranice závislostí
- veřejná rozhraní subsystémů
- tok dat
- architekturu evaluace
- bezpečnostní hranice
- budoucí cílovou strukturu

Architektura má být všude, kde je to možné, nezávislá na konkrétní doméně.

Doménové chování nesmí být vloženo do obecných komponent retrievalu, evaluace, načítání dokumentů ani infrastruktury.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-2-architektonické-principy"></a>

## 2. Architektonické principy

Projekt se řídí následujícími architektonickými principy.

<a id="cz-21-oddělení-odpovědností"></a>

### 2.1 Oddělení odpovědností

Každý modul má mít jednu hlavní odpovědnost.

Příklady:

```text
PDF loading
≠
text normalization
≠
retrieval
≠
reranking
≠
generation
≠
API transport
```

Modul nemá spojovat nesouvisející odpovědnosti jen proto, že se nyní používají společně.

---

<a id="cz-22-výslovné-hranice-modulů"></a>

### 2.2 Výslovné hranice modulů

Vyšší vrstvy mají s nižšími subsystémy komunikovat prostřednictvím definovaných veřejných rozhraní.

Preferované řešení:

```text
RAG service
    ↓
retrieval service
    ↓
retrieval internals
```

Nevhodné řešení:

```text
RAG service
    ↓
embedding model
    ↓
ChromaDB internals
    ↓
reranker internals
    ↓
scoring helpers
```

Volající nemá potřebovat znalost vnitřní implementace používaného subsystému.

---

<a id="cz-23-nezávislost-na-doméně"></a>

### 2.3 Nezávislost na doméně

Obecná infrastruktura nesmí záviset na pojmech nebo pravidlech specifických pro OSPF.

Obecné komponenty například nesmí obsahovat natvrdo zapsanou logiku pro:

```text
OSPF
DROTHER
designated router
virtual links
Cisco-specific terminology
```

Tyto pojmy se mohou vyskytovat v:

- zdrojových dokumentech
- evaluačních datasetech
- uživatelských dotazech

nikoli však v obecném kódu řazení nebo infrastruktury.

---

<a id="cz-24-upřednostnění-neměnných-dat"></a>

### 2.4 Upřednostnění neměnných dat

Datové objekty představující fakta mají být pokud možno neměnné.

Příklady:

```text
PageDocument
SearchResult
RetrievedChunk
EvaluationQuestion
GoldEvidence
```

Preferovaná implementace:

```python
@dataclass(frozen=True)
```

Omezuje to náhodné změny stavu a usnadňuje porozumění systému i jeho testování.

---

<a id="cz-25-konfigurace-mimo-aplikační-logiku"></a>

### 2.5 Konfigurace mimo aplikační logiku

Konfigurace má být centralizovaná.

Příklady:

```text
model names
retrieval limits
collection names
file limits
API settings
security limits
```

Aplikační logika nemá obsahovat duplicitní natvrdo zapsaná nastavení.

---

<a id="cz-26-měření-před-optimalizací"></a>

### 2.6 Měření před optimalizací

Změny retrievalu se musí vyhodnocovat evaluačním frameworkem.

Projekt nemá zavádět heuristiky řazení jen proto, že vypadají užitečně pro jeden ručně zkontrolovaný dotaz.

Vývojový postup:

```text
baseline
    ↓
measurement
    ↓
change
    ↓
measurement
    ↓
comparison
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-3-celková-architektura-systému"></a>

## 3. Celková architektura systému

Hlavní běhová architektura:

```text
                         USER / CLIENT
                              │
                              ▼
                           FastAPI
                              │
                              ▼
                         RAG SERVICE
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
         RETRIEVAL SERVICE              GENERATION
                │                           │
                ▼                           │
         VECTOR RETRIEVAL                   │
                │                           │
                ▼                           │
            RERANKING                       │
                │                           │
                ▼                           │
       SELECTED CONTEXT ────────────────────┘
                │
                ▼
          FINAL RESPONSE
                │
                ▼
        ANSWER + SOURCES
```

Běhová aplikace přímo nezávisí na evaluačním systému ani na průzkumníku dokumentů.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-4-offline-datová-pipeline"></a>

## 4. Offline datová pipeline

Ingest pipeline je oddělená od online zpracování dotazů.

```text
PDF DOCUMENTS
      │
      ▼
TEXT EXTRACTION
      │
      ▼
PREPROCESSING
      │
      ▼
CHUNKING
      │
      ▼
EMBEDDING
      │
      ▼
VECTOR STORE
   ChromaDB
```

Současná implementace:

```text
scripts/ingest.py
```

Budoucí refaktoring může ingest rozdělit do dalších modulů, ale není to nutné, dokud takovou změnu neodůvodní měření nebo složitost.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-5-běhová-aplikace"></a>

## 5. Běhová aplikace

Současná struktura aplikace:

```text
app/
├── __init__.py
├── config.py
├── generation.py
├── main.py
├── rag.py
├── retrieval.py
└── schemas.py
```

Následují současné odpovědnosti modulů.

---

<a id="cz-51-appconfigpy"></a>

### 5.1 `app/config.py`

Spravuje konfiguraci aplikace.

Příklady:

```text
embedding model
reranker model
generation model
Chroma collection
candidate count
returned result count
context limits
```

Cílové pravidlo:

Ostatní moduly mají nastavení číst z konfigurace místo duplikace konstant.

---

<a id="cz-52-appschemaspy"></a>

### 5.2 `app/schemas.py`

Spravuje datová schémata vnějšího API.

Příklady:

```text
QuestionRequest
SourceChunk
AnswerResponse
```

Tato schémata popisují data přenášená přes HTTP hranici.

Jsou oddělená od interních modelů retrievalu.

Například:

```text
API SourceChunk
```

nemusí být totožné s:

```text
internal RetrievalResult
```

---

<a id="cz-53-appretrievalpy"></a>

### 5.3 `app/retrieval.py`

Současná implementace retrievalu.

Nynější odpovědnosti zahrnují více oblastí:

```text
query processing
embedding retrieval
candidate selection
reranking
heuristic scoring
result selection
```

Soubor zůstává v provozu vedle experimentálních retrieverů v `app/retrievers/`.

Schválený cíl FÁZE 3 navrhuje rozdělení na:

```text
app/
└── retrieval/
    ├── __init__.py
    ├── models.py
    ├── embeddings.py
    ├── vector_search.py
    ├── query.py
    ├── reranker.py
    ├── scoring.py
    └── service.py
```

Výsledný veřejný vstupní bod má být v:

```text
app/retrieval/service.py
```

s rozhraním podobným:

```python
retrieve(
    query: str,
) -> list[RetrievalResult]
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-6-cílová-architektura-retrievalu"></a>

## 6. Cílová architektura retrievalu

Plánovaný tok retrievalu:

```text
QUERY
  │
  ▼
query.py
normalize / prepare query
  │
  ▼
embeddings.py
query embedding
  │
  ▼
vector_search.py
retrieve candidate chunks
  │
  ▼
reranker.py
CrossEncoder scoring
  │
  ▼
scoring.py
optional score combination
  │
  ▼
service.py
select TOP K results
  │
  ▼
RetrievalResult
```

Každá vrstva má jednu hlavní odpovědnost.

---

<a id="cz-61-retrievalmodelspy"></a>

### 6.1 `retrieval/models.py`

Interní datové modely retrievalu.

Plánované typy:

```text
RetrievedChunk
ScoredChunk
RetrievalResult
```

Tyto modely představují interní data retrievalu a nemají záviset na FastAPI.

---

<a id="cz-62-retrievalembeddingspy"></a>

### 6.2 `retrieval/embeddings.py`

Spravuje operace embeddingového modelu.

Možné funkce:

```python
load_embedding_model()
embed_query()
embed_documents()
```

Tento modul nesmí znát fungování FastAPI.

Nemá ani rozhodovat o konečném pořadí výsledků.

---

<a id="cz-63-retrievalvector_searchpy"></a>

### 6.3 `retrieval/vector_search.py`

Spravuje komunikaci s vektorovým úložištěm.

Možné funkce:

```python
search_vector_store()
convert_chroma_results()
```

Zde se mají formáty odpovědí specifické pro Chroma převést do vlastních datových modelů projektu.

Vyšší vrstvy nemají přímo záviset na struktuře odpovědi Chroma.

---

<a id="cz-64-retrievalquerypy"></a>

### 6.4 `retrieval/query.py`

Spravuje obecnou přípravu dotazů.

Možné funkce:

```python
normalize_query()
```

Rozšiřování dotazů lze přidat jen tehdy, prokáže-li evaluace měřitelný přínos.

Doménová pravidla rozšiřování nesmí být natvrdo zapsána do obecné vrstvy retrievalu.

---

<a id="cz-65-retrievalrerankerpy"></a>

### 6.5 `retrieval/reranker.py`

Spravuje přerovnání pomocí CrossEncoderu.

Funkce:

```python
load_reranker()
rerank()
```

Vstup:

```text
query
+
candidate chunks
```

Výstup:

```text
scored candidates
```

---

<a id="cz-66-retrievalscoringpy"></a>

### 6.6 `retrieval/scoring.py`

Spravuje kombinování skóre, pokud je fúze skóre potřebná.

Tato vrstva má zabránit rozptýlení pravidel skórování napříč celou retrieval pipeline.

Při jakékoli kombinaci:

```text
vector score
CrossEncoder score
other retrieval score
```

je nutné zohlednit měřítko a význam skóre.

Neslučitelná surová skóre se nesmějí jednoduše sečíst.

---

<a id="cz-67-retrievalservicepy"></a>

### 6.7 `retrieval/service.py`

Veřejné rozhraní retrievalu.

Koordinuje vnitřní části retrievalu:

```text
query
↓
candidate retrieval
↓
reranking
↓
score handling
↓
TOP K
```

Ostatní vrstvy aplikace mají primárně záviset na této službě, nikoli na jednotlivých vnitřních částech retrievalu.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-7-architektura-generování"></a>

## 7. Architektura generování

Současný soubor:

```text
app/generation.py
```

Současná odpovědnost:

```text
question
+
retrieved context
↓
prompt
↓
generation model
↓
answer
```

Možné budoucí vnitřní rozdělení:

```text
prompt construction
model inference
output processing
```

Rozdělení se má zavést pouze tehdy, odůvodňuje-li je složitost.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-8-koordinace-rag"></a>

## 8. Koordinace RAG

Současný soubor:

```text
app/rag.py
```

Vrstva RAG koordinuje ostatní služby.

Cílová odpovědnost:

```text
question
    │
    ▼
retrieval service
    │
    ▼
context construction
    │
    ▼
generation service
    │
    ▼
answer + sources
```

Vrstva RAG nesmí implementovat:

```text
vector search details
embedding internals
CrossEncoder internals
Chroma response parsing
HTTP transport
```

Její úlohou je koordinace.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-9-architektura-api"></a>

## 9. Architektura API

Současný vstupní bod:

```text
app/main.py
```

Cílová struktura FÁZE 4:

```text
app/
├── main.py
├── lifecycle.py
│
└── api/
    ├── __init__.py
    ├── routes.py
    ├── dependencies.py
    ├── errors.py
    └── middleware.py
```

---

<a id="cz-91-appmainpy"></a>

### 9.1 `app/main.py`

Postupně se má stát malým místem sestavení aplikace (composition root).

Odpovědnosti:

```text
create FastAPI application
register routes
register middleware
register lifecycle
register exception handlers
```

Nemá obsahovat aplikační logiku.

---

<a id="cz-92-applifecyclepy"></a>

### 9.2 `app/lifecycle.py`

Spravuje životní cyklus procesu.

Příklady:

```text
startup
↓
load models
load vector store
initialize services

shutdown
↓
release resources
```

Modely se mají běžně inicializovat jednou, nikoli pro každý HTTP požadavek.

---

<a id="cz-93-appapiroutespy"></a>

### 9.3 `app/api/routes.py`

Spravuje HTTP routy.

Příklady:

```text
GET /health
POST /ask
```

Routy mají překládat:

```text
HTTP
↔
application services
```

nemají však implementovat logiku retrievalu.

---

<a id="cz-94-appapidependenciespy"></a>

### 9.4 `app/api/dependencies.py`

Spravuje vkládání závislostí ve FastAPI.

Možná rozhraní:

```python
get_settings()
get_rag_service()
```

To umožňuje při testování vyměnit komponenty aplikace bez přepisování endpointů.

---

<a id="cz-95-appapierrorspy"></a>

### 9.5 `app/api/errors.py`

Spravuje převod aplikačních chyb na chyby API.

Příklady:

```text
InvalidQueryError
RetrievalError
GenerationError
```

Interní výjimky lze mapovat na řízené HTTP odpovědi.

---

<a id="cz-96-appapimiddlewarepy"></a>

### 9.6 `app/api/middleware.py`

Možné odpovědnosti:

```text
request ID
request timing
basic HTTP logging
```

Middleware má řešit průřezové záležitosti HTTP, nikoli aplikační logiku.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-10-architektura-evaluace"></a>

## 10. Architektura evaluace

Evaluace je nezávislá na běhové aplikaci.

Cílová struktura:

```text
evaluation/
├── __init__.py
├── models.py
├── dataset.py
├── evidence.py
├── metrics.py
├── runner.py
├── history.py
└── random_eval.py
```

Hlavní pravidlo:

```text
evaluation measures retrieval
```

ale:

```text
retrieval must not depend on evaluation
```

Směr závislostí:

```text
evaluation
    ↓
retrieval
```

Nikdy:

```text
retrieval
    ↓
evaluation
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-11-role-evaluačních-datasetů"></a>

## 11. Role evaluačních datasetů

Tři kategorie datasetů jsou záměrně oddělené.

<a id="cz-dev"></a>

### DEV

Používá se při vývoji.

Může ovlivňovat návrh a ladění.

Dataset DEV smí ovlivňovat implementační rozhodnutí.

---

<a id="cz-random"></a>

### RANDOM

Používá se pro:

```text
robustness exploration
unexpected failure discovery
coverage exploration
```

Náhodný výběr musí být reprodukovatelný díky uloženému seedu.

---

<a id="cz-test"></a>

### TEST

Oddělená závěrečná evaluace.

TEST se nesmí stát dalším ladicím datasetem.

Opakované ruční prohlížení výsledků TEST při optimalizaci by snížilo jeho hodnotu jako nezávislé kontroly zobecnění.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-12-průběh-evaluace"></a>

## 12. Průběh evaluace

```text
EvaluationQuestion
       │
       ▼
retrieval service
       │
       ▼
ranked results
       │
       ▼
gold evidence matching
       │
       ▼
rank of correct evidence
       │
       ▼
metrics
       │
       ├── Hit@K
       └── MRR
```

Metadata evaluačního běhu mají dále obsahovat:

```text
Git commit
working-tree dirty state
dataset hash
timestamp
configuration
```

Díky tomu jsou výsledky reprodukovatelné a porovnatelné.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-13-univerzální-průzkumník-dokumentů"></a>

## 13. Univerzální průzkumník dokumentů

Průzkumník dokumentů není součástí běhové RAG retrieval pipeline.

Jeho účel:

```text
corpus exploration
+
gold evidence discovery
+
manual benchmark construction
```

Cílová struktura:

```text
document_search/
├── __init__.py
├── models.py
├── normalize.py
├── tokenize.py
├── load_pages.py
├── build_index.py
├── search.py
│
└── security/
    ├── __init__.py
    ├── paths.py
    ├── pdf_validation.py
    └── input_validation.py
```

CLI:

```text
scripts/search_pdf.py
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-14-tok-dat-průzkumníku-dokumentů"></a>

## 14. Tok dat průzkumníku dokumentů

```text
PDF CORPUS
    │
    ▼
security validation
    │
    ▼
load_pdf_pages()
    │
    │ list[PageDocument]
    ▼
normalize_text()
    │
    ▼
tokenize()
    │
    ▼
build_bm25_index()
    │
    │ BM25SearchIndex
    ▼
search_pages()
    │
    │ list[SearchResult]
    ▼
CLI
    │
    ▼
human evidence validation
    │
    ▼
evaluation dataset
```

Tato architektura se záměrně liší od RAG retrieval stacku.

Průzkum dokumentů:

```text
BM25 lexical retrieval
+
human validation
```

Hlavní RAG:

```text
embedding retrieval
+
CrossEncoder reranking
```

Oddělení omezuje kruhovou konstrukci benchmarku.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-15-modely-vyhledávání-v-dokumentech"></a>

## 15. Modely vyhledávání v dokumentech

<a id="cz-151-pagedocument"></a>

### 15.1 `PageDocument`

Představuje jednu zdrojovou stránku.

Koncepčně:

```python
PageDocument(
    source="manual.pdf",
    page=26,
    text="...",
)
```

Kombinace:

```text
source
+
page
+
text
```

představuje identitu a obsah prohledávané zdrojové jednotky.

---

<a id="cz-152-searchresult"></a>

### 15.2 `SearchResult`

Představuje seřazený výsledek vyhledávání.

Koncepčně:

```text
document
+
score
```

Výsledek má odkazovat na původní `PageDocument`, nikoli duplikovat metadata dokumentu v několika strukturách.

---

<a id="cz-153-bm25searchindex"></a>

### 15.3 `BM25SearchIndex`

Spravuje:

```text
page corpus
+
BM25 model
```

Zbytek aplikace nemá potřebovat spravovat tyto dva objekty samostatně.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-16-bezpečnostní-hranice-průzkumníku-dokumentů"></a>

## 16. Bezpečnostní hranice průzkumníku dokumentů

PDF korpus se považuje za externí vstup.

Bezpečnostní tok:

```text
filesystem input
      │
      ▼
path validation
      │
      ▼
file validation
      │
      ▼
resource limits
      │
      ▼
PDF parser
```

Důležité kontroly:

```text
allowed directory boundary
path traversal prevention
symlink resolution
PDF extension validation
PDF signature validation
file size limits
page count limits
query limits
top_k limits
```

Bezpečnostní validace nesmí potichu měnit význam dokumentu.

Pokud dokument nelze bezpečně nebo úplně načíst, musí být selhání výslovné.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-17-bezpečnostní-architektura"></a>

## 17. Bezpečnostní architektura

Bezpečnost je průřezové téma.

Některé kontroly patří blízko ke zdroji dat:

```text
document_search/security/
```

Jiné kontroly patří do běhové aplikace:

```text
app/security/
```

Budoucí cíl:

```text
app/
└── security/
    ├── __init__.py
    ├── validation.py
    ├── limits.py
    └── headers.py
```

Bezpečnost se neimplementuje pomocí getterů a setterů.

Mezi hlavní mechanismy patří:

```text
input validation
immutability
filesystem boundaries
resource limits
dependency controls
secrets handling
permissions
container isolation
HTTP controls
```

---

<a id="cz-171-budoucí-modelování-hrozeb"></a>

### 17.1 Budoucí modelování hrozeb

Samostatná bezpečnostní fáze má určit:

```text
assets
trust boundaries
attack surfaces
possible attackers
failure modes
impact
mitigations
```

Hrozby specifické pro RAG mohou zahrnovat:

```text
indirect prompt injection
malicious document content
resource exhaustion
unsafe file handling
oversized requests
dependency vulnerabilities
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-18-architektura-observability"></a>

## 18. Architektura observability

Cílová struktura:

```text
app/
└── observability/
    ├── __init__.py
    ├── logging.py
    ├── metrics.py
    └── middleware.py
```

Observabilita má pokrývat kvalitu i provoz.

Provozní metriky zahrnují:

```text
request count
error count
response latency
retrieval latency
reranking latency
generation latency
```

Kde je to relevantní:

```text
token usage
model usage
cost
```

Observabilita nesmí měnit výsledky retrievalu.

---

<a id="cz-181-strukturované-logování"></a>

### 18.1 Strukturované logování

Běhové logy mají postupně obsahovat strukturovaná pole, například:

```text
request_id
event
latency_ms
candidate_count
model
error_type
```

místo spoléhání pouze na volný text.

---

<a id="cz-182-metriky-kvality-a-provozní-metriky"></a>

### 18.2 Metriky kvality a provozní metriky

Metriky kvality:

```text
MRR
Hit@K
groundedness
answer quality
```

Provozní metriky:

```text
latency
request count
error rate
resource usage
token usage
cost
```

Měří různé vlastnosti systému a nemají se zaměňovat.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-19-architektura-testování"></a>

## 19. Architektura testování

Současné testy jsou v:

```text
tests/
```

Budoucí testy mají stále více odpovídat produkčním modulům.

Příklad:

```text
document_search/normalize.py
        ↕
tests/document_search/test_normalize.py
```

a:

```text
document_search/search.py
        ↕
tests/document_search/test_search.py
```

Vrstvy testování:

```text
UNIT TESTS
    ↓
individual functions/modules

INTEGRATION TESTS
    ↓
multiple modules together

SMOKE TESTS
    ↓
basic end-to-end system operation

EVALUATION
    ↓
retrieval quality
```

Jde o různé odpovědnosti.

Úspěšný jednotkový test neprokazuje kvalitu retrievalu.

Dobré skóre MRR neprokazuje správnost API.

---

<a id="cz-191-nezávislost-testů"></a>

### 19.1 Nezávislost testů

Jednotkové testy mají pokud možno omezit závislost na:

```text
large real PDF corpora
network access
production vector databases
external APIs
```

Pro deterministické jednotkové testy se mají upřednostnit malé syntetické vstupy.

Testy se skutečným korpusem patří do integračních nebo ručních ověřovacích postupů.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-20-architektura-infrastruktury"></a>

## 20. Architektura infrastruktury

Současná infrastruktura zahrnuje:

```text
Dockerfile
compose.yaml
.github/workflows/ci.yml
```

Cílová cesta k produkci:

```text
SOURCE CODE
    │
    ▼
Git
    │
    ▼
CI
    │
    ├── tests
    ├── static checks
    └── later security checks
    │
    ▼
Docker image
    │
    ▼
deployment
    │
    ▼
runtime monitoring
```

---

<a id="cz-201-architektura-kontejnerů"></a>

### 20.1 Architektura kontejnerů

Budoucí produkční kontejnery mají usilovat o:

```text
reproducible builds
minimal runtime dependencies
non-root execution
health checks
explicit configuration
small attack surface
```

Vícefázové Docker buildy lze zavést, budou-li užitečné.

---

<a id="cz-202-cicd"></a>

### 20.2 CI/CD

Současné CI především ověřuje projekt.

Budoucí CI/CD může rozšířit tok na:

```text
push
↓
tests
↓
static checks
↓
security checks
↓
image build
↓
deployment
```

Automatizace nasazení se má přidat až tehdy, bude-li běhová architektura dostatečně stabilní pro spolehlivé nasazování.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-21-směr-závislostí"></a>

## 21. Směr závislostí

Zamýšlený směr závislostí:

```text
API
 ↓
RAG
 ↓
Retrieval / Generation
 ↓
Models / Infrastructure integrations
```

Evaluace smí volat retrieval:

```text
Evaluation
    ↓
Retrieval
```

Průzkumník dokumentů je nezávislý:

```text
Document Explorer
    ↓
PDF / BM25 libraries
```

Následujícím směrům závislostí je třeba se vyhnout:

```text
retrieval → API
retrieval → evaluation
generation → FastAPI
document_search → RAG
document_search → OSPF logic
```

Tím se omezuje provázanost.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-22-veřejná-rozhraní"></a>

## 22. Veřejná rozhraní

Architektura má nabízet malý počet stabilních vstupních bodů.

Následují plánované příklady.

<a id="cz-221-vyhledávání-v-dokumentech"></a>

### 22.1 Vyhledávání v dokumentech

```python
load_pdf_pages(...)
build_bm25_index(...)
search_pages(...)
```

---

<a id="cz-222-retrieval"></a>

### 22.2 Retrieval

```python
retrieve(...)
```

---

<a id="cz-223-rag"></a>

### 22.3 RAG

Koncepčně:

```python
answer_question(...)
```

---

<a id="cz-224-evaluace"></a>

### 22.4 Evaluace

Koncepčně:

```python
evaluate_dataset(...)
```

Interní pomocné funkce se mohou měnit, aniž by se museli měnit všichni volající.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-23-současný-technický-dluh"></a>

## 23. Současný technický dluh

Níže je uveden známý architektonický dluh.

<a id="cz-231-retrieval"></a>

### 23.1 Retrieval

Současný stav:

```text
app/retrieval.py
```

obsahuje více odpovědností a doménová pravidla.

Řešení:

```text
PHASE 3
```

---

<a id="cz-232-rag"></a>

### 23.2 RAG

Současný stav:

```text
app/rag.py
```

obsahuje chování specifické pro OSPF.

Řešení:

```text
PHASE 3
```

---

<a id="cz-233-evaluace--základ-je-implementován"></a>

### 23.3 Evaluace — základ je implementován

Znovupoužitelné načítání datasetů, párování evidence, metriky, latence a historie jsou již v `evaluation/`; koordinace CLI zůstává v `scripts/`. Starší `scripts.evaluate_random` stále obsahuje vady v cestě historie, kontrole Git stavu a výpisu metrik. Podporovaným postupem porovnání je `scripts.evaluate_retrieval` nad DEV/RANDOM; viz [EVALUATION.md](EVALUATION.md#cz).

---

<a id="cz-234-vyhledávání-v-dokumentech--historický-prototyp-nahrazen"></a>

### 23.4 Vyhledávání v dokumentech — historický prototyp nahrazen

Předchozí heuristický prototyp vyhledávání experimentoval s:

```text
required terms
boost terms
manual proximity scoring
anchor terms
manual exclusions
```

Tento historický prototyp byl nahrazen obecným stránkovým BM25 v `document_search/`.

Současný postup průzkumu:

```text
generic BM25 search
+
human evidence validation
```

nezávisle na pořadí výsledků vyhledávání.

---

<a id="cz-235-ingest"></a>

### 23.5 Ingest

Současná ingest pipeline zůstává soustředěná v:

```text
scripts/ingest.py
```

Pro současnou fázi je to přijatelné.

Rozdělit se má až tehdy, když:

```text
complexity increases
testing becomes difficult
reuse is required
or measurements expose a concrete problem
```

Nerefaktoruj ingest pouze kvůli architektonické symetrii.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-24-cílová-struktura-projektu"></a>

## 24. Cílová struktura projektu

Dlouhodobá cílová struktura:

```text
rag_api_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── lifecycle.py
│   ├── schemas.py
│   ├── generation.py
│   ├── rag.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── middleware.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── embeddings.py
│   │   ├── vector_search.py
│   │   ├── query.py
│   │   ├── reranker.py
│   │   ├── scoring.py
│   │   └── service.py
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   └── middleware.py
│   │
│   └── security/
│       ├── __init__.py
│       ├── validation.py
│       ├── limits.py
│       └── headers.py
│
├── document_search/
│   ├── __init__.py
│   ├── models.py
│   ├── normalize.py
│   ├── tokenize.py
│   ├── load_pages.py
│   ├── build_index.py
│   ├── search.py
│   │
│   └── security/
│       ├── __init__.py
│       ├── paths.py
│       ├── pdf_validation.py
│       └── input_validation.py
│
├── evaluation/
│   ├── __init__.py
│   ├── models.py
│   ├── dataset.py
│   ├── evidence.py
│   ├── metrics.py
│   ├── runner.py
│   ├── history.py
│   └── random_eval.py
│
├── scripts/
│   ├── __init__.py
│   ├── ingest.py
│   ├── search_pdf.py
│   ├── evaluate_retrieval.py
│   ├── production_smoke.py
│   └── git_check.py
│
├── tests/
│   ├── document_search/
│   ├── evaluation/
│   ├── retrieval/
│   ├── integration/
│   └── test_smoke.py
│
├── eval/
│   ├── dev_questions.json
│   ├── random/
│   └── test_questions.json
│
├── docs/
│   ├── ROADMAP.md
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT_GUIDE.md
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── README.md
└── .env.example
```

Jde o cílovou strukturu.

Adresáře se mají vytvářet až při zahájení příslušné vývojové fáze.

Projekt nemá vytvářet prázdnou architekturu jen kvůli shodě s diagramem.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-25-pravidlo-změn-architektury"></a>

## 25. Pravidlo změn architektury

Architektura se může vyvíjet.

Významné architektonické změny však mají dodržet tento postup:

```text
identify concrete problem
        ↓
measure or demonstrate problem
        ↓
propose architectural change
        ↓
update architecture documentation
        ↓
implement change
        ↓
test
```

Architektura se nemá měnit pouze proto, že jiný návrh vypadá propracovaněji.

Upřednostňuje se nejjednodušší architektura, která splní současné požadavky.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-26-historické-architektonické-zaměření-fáze-2a"></a>

## 26. Historické architektonické zaměření fáze 2A

Následující sled zachovává původní plán. Již nejde o aktivní krok; viz [přehled současné implementace](#cz-přehled-implementace-k-28-10-2026) a [současné zaměření vývoje](ROADMAP.md#cz-aktuální-zaměření-vývoje). Nynější prací je hybridní RRF experiment popsaný ve vývojovém logu; tím se nemění číslování schválené roadmapy.

Současná vývojová fáze:

```text
PHASE 2 — Evaluation Foundation
```

Současný architektonický úkol:

```text
PHASE 2A — Universal Document Explorer
```

Nejbližší cíl:

```text
document_search/
```

s:

```text
immutable data models
domain-independent text processing
safe PDF loading
BM25 retrieval
small public API
unit tests
```

Hlavní implementace RAG retrievalu zůstává beze změny, dokud nebude dostatečně dokončen evaluační základ.

Další architektonický milník:

```text
PHASE 2A.0
architecture freeze

↓

PHASE 2A.1
document_search/models.py
```

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
