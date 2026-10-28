# Operations runbook / Provozní příručka

> **Scope / Rozsah:** Current Chroma-backed RAG project, Python 3.11. Commands below run from `rag_api_project/`. This is a local educational prototype, not a production deployment.
>
> **Safety / Bezpečnost:** `python -m scripts.ingest` **deletes and recreates** the existing Chroma collection with the configured name. Back up the index and confirm the PDF corpus and configuration before running. It is **not** an incremental ingest.

## CZ — Český návod

### 1. Předpoklady a instalace (Windows PowerShell)

Požadavky: Python 3.11, Git, přístup k potřebným Python balíčkům a modelům při první instalaci. Pracuj v adresáři `rag_api_project/`:

```powershell
# Z kořene klonovaného repozitáře (cd proveď pouze jednou):
cd rag_api_project
python --version  # Musí být 3.11.x.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

V PowerShellu lze příkazy spouštět i bez aktivace pomocí `.\.venv\Scripts\python.exe -m ...`. Instalaci lze ověřit pomocí `python -m pytest -q`.

**Linux / macOS:**

```bash
cd rag_api_project
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
test -f .env || cp .env.example .env
```

Před instalací zkontroluj použitý interpreter a kompatibilitu balíčků. Ve zveřejněné větvi je `requirements.txt` nepinovaný; lokálně vytvořené lockfily nelze automaticky pokládat za schválené ani přenositelné. Neměň verze závislostí jako součást dokumentační úpravy.

### 1a. Reprodukovatelnost závislostí (Windows Python 3.11)

Základní `requirements.txt` ve zveřejněné větvi obsahuje neomezené verze balíčků; lokálně může existovat `requirements-win-py311.lock.txt` s přesnými verzemi. Tento lockfile **není automaticky schválený ani verzovaný**. Nezacházej s ním jako s univerzálním instalačním návodem bez samostatné kontroly kompatibility a CI.

Před případným přijetím lockfilu je nutné ověřit podporovaný Python/OS, metodu vytvoření, čisté instalace na Windows a CI, soulad s `requirements.txt` a proces aktualizace balíčků. Změny balíčků patří do samostatného commitu a nesmí se slučovat s revizí dokumentace.

### 2. Konfigurace a zdroje

Aplikace čte `.env` z `rag_api_project/` přes `app/config.py`. Důležité proměnné:

| Proměnná | Příklad | Význam |
| --- | --- | --- |
| `RAG_COLLECTION_NAME` | `ospf` | Název Chroma kolekce |
| `RAG_EMBEDDING_MODEL_NAME` | `all-MiniLM-L6-v2` | Embedding model |
| `RAG_RETRIEVAL_RESULTS` | `8` | Počet vyhledaných chunků |
| `RAG_GENERATION_MODEL_NAME` | `google/flan-t5-base` | Generační model |
| `RAG_RERANKER_MODEL_NAME` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Reranking v RAG odpovědní pipeline |
| `RAG_DATA_DIR` | absolutní cesta k PDF | Volitelné přepsání adresáře pro ingest |
| `RAG_CHROMA_DIR` | absolutní cesta k indexu | Volitelné přepsání umístění Chroma |

Implicitní cesty z `app/config.py`: `data/` pro PDF a `chroma_db/` pro Chroma index. Obsah těchto adresářů může být lokální nebo neveřejný; necommituj soukromé PDF, databázi, `.env` ani modelové cache.

Vlož zdrojová PDF **přímo do** `data/` (nikoli do podadresářů). Současný ingest vyhledává soubory odpovídající vzoru `*.pdf`; před spuštěním ověř přesné názvy a přípony.

Proměnné prostředí mají přednost před `.env`. Po změně konfigurace restartuj API (nastavení se cachuje). Ingest a vector/legacy retrieval musí používat stejný embedding model jako index. Page explorer a validátor čtou standardně relativní `data/`, nikoli `RAG_DATA_DIR`; vlastní cestu jim předej pomocí `--data-dir <adresář>`.

### 3. Ingest PDF do ChromaDB

```powershell
python -m scripts.ingest
```

**Pozor — destruktivní operace:** `scripts/ingest.py` zavolá `delete_collection()`, pokud kolekce s daným názvem existuje, a následně vytvoří novou. Neprováděj ingest automaticky jako krok testů nebo rutinní evaluace. Pro opakovaný ingest nejdříve ověř zálohu a schválený záměr.

Aktuální pipeline: extrakce fyzických PDF stránek pomocí pypdf → čištění textu → chunkování (výchozí `chunk_size=1000`, `overlap=150`, ve znacích) → SentenceTransformer embeddingy → Chroma. Chunk metadata obsahují `source` (název PDF), `page` (fyzická stránka od 1) a `chunk_index` (pořadí v rámci PDF). Identifikátory chunků jsou v poli Chroma `ids`, nikoliv automaticky v metadatech.

Kolekce se maže **před** extrakcí a upsertem. Chyba čtení PDF nebo zápisu po smazání neobnoví starý index; obnova není transakční. Zálohu adresáře Chroma pořizuj při zastavených procesech, které index používají.

Po ingestu ověř počet záznamů a ukázku metadat **bez změny obsahu kolekce**:

```powershell
python -c "import chromadb; from app.config import get_settings; s=get_settings(); c=chromadb.PersistentClient(path=str(s.chroma_dir)).get_collection(name=s.collection_name); print('COLLECTION:', c.name, 'CHUNKS:', c.count()); print(c.get(limit=3, include=['metadatas']))"
```

`PersistentClient` není připojení v režimu read-only: při otevření může vytvořit adresář/databázi nebo provést migrace. Před kontrolou ověř existenci správného `RAG_CHROMA_DIR`; pro striktně neměnnou kontrolu pracuj s kopií indexu.

Počet chunků závisí na přesné verzi PDF, chunkování a konfiguraci; historické počty nejsou univerzálním očekáváním. U změn korpusu zaznamenej názvy/identitu zdrojových PDF a konfiguraci, aby šlo výsledky evaluace reprodukovat.

### 4. Spuštění API

```powershell
python -m uvicorn app.main:app --reload
```

OpenAPI: http://127.0.0.1:8000/docs. Příklady:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType 'application/json' -Body '{"question":"How does OSPF select the router ID?"}'
```

`/ready` a `/stats` poskytují další diagnostiku prostředí a kolekce. **Důležitá hranice:** BM25 je volitelný v *offline evaluation CLI*, nikoliv automaticky jako možnost pro HTTP `/ask`. Rozpracovaný hybrid nepovažuj za implementovanou funkci API.

### 5. Vyhledání podkladů v původních PDF (page explorer)

```powershell
python -m scripts.search_pdf "OSPF router ID" --top-k 10 --interactive
```

`scripts.search_pdf` používá samostatný BM25 index *PDF stránek* z `data/`. Není to totéž jako `app/retrievers/bm25.py`, který řadí chunky uložené v Chroma. Page explorer slouží k průzkumu a ručnímu ověření důkazů, nikoli k automatickému přepisování golden evidence.

### 6. Testy a kontrola commitu

```powershell
python -m pytest -q
python -m pytest -q tests/retrievers/test_bm25.py
git diff --check
```

Před commitem připrav pouze zamýšlené soubory (nikdy automatické `git add .`), zkontroluj staging a případně spusť projektový pre-commit helper:

```powershell
git diff --cached --check
python -m scripts.git_check
```

`scripts.git_check` kontroluje staged whitespace a spouští pytest. Pro změny v `eval/` nebo pravidlech curatoru platí dodatečná pravidla v `AGENTS.md`, `docs/EVAL_CURATOR_AGENT.md` a CI governance.

Před prací použij `git status --short` a `git branch --show-current`. Pro pokračování PR #3 použij existující větev `docs/bilingual-rag-runbooks-20261028` (base `document-search-bm25`); nepřepínej větev přes nesouvisející WIP. Po explicitním `git add <cesty>` přečti `git diff --cached` i seznam souborů. Helper nekontroluje tajemství, schválení ani věcný rozsah změn. Commit/push prováděj jen v autorizovaném rozsahu, bez automatického merge.

### 7. Offline evaluace

```powershell
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

Výstup: MRR, Hit@1/3/5/8, latence mean/P50/P95 a první pozice relevantního důkazu pro jednotlivé otázky. Běhy se zapisují do `eval/results/*_runs.jsonl` podle strategie a datasetu; obsahují hash datasetu, Git commit a příznak dirty worktree. Zápis do historie je vedlejší efekt: příkaz není čistě read-only. **TEST je held-out** a úmyslně není volbou tohoto CLI. Podrobnosti: [EVALUATION.md](EVALUATION.md).

### 8. Docker a provozní omezení

```powershell
docker compose up --build
docker compose down
```

Compose zpřístupňuje API na http://127.0.0.1:8001/docs a připojuje `chroma_db/` a modelovou cache. Dockerfile kopíruje pouze `app/`, `scripts/` a `.env.example`; nekopíruje `document_search/`, `evaluation/`, `eval/` ani PDF. Ingest, page explorer a evaluaci proto spouštěj nativně. Kontejner potřebuje hotový kompatibilní index a přístup k modelům při prvním použití.

Compose nepředává hostitelský `.env` aplikaci: nemá `env_file` ani `environment` a obraz `.env` neobsahuje. Pro vlastní nastavení je nutné explicitní předání `RAG_*` proměnných v lokální Compose konfiguraci, s cestami platnými uvnitř kontejneru. Samotný start nebo `/health` nepotvrzuje funkčnost `/ask`; zkontroluj také `/ready` a `/stats`.

**Diagnostika:** `No PDF files found` znamená zkontrolovat adresář `data/` a příponu souborů. Chybějící Chroma kolekce může znamenat nesprávnou cestu nebo neprovedený ingest. `ModuleNotFoundError` typicky znamená nesprávné prostředí či pracovní adresář. `FIRST_EVIDENCE_RANK=None` neznamená automaticky prázdný retrieval — pouze že žádný z hodnocených chunků neodpovídal golden evidence.

---

## EN — English instructions

### 1. Setup and configuration

Use Python 3.11 and run commands from `rag_api_project/`. On Windows PowerShell:

```powershell
# From the cloned repository root (change directory only once):
cd rag_api_project
python --version  # Must be 3.11.x.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

On Linux/macOS:

```bash
cd rag_api_project
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
test -f .env || cp .env.example .env
```

The configuration lives in `.env` (see `.env.example` and `app/config.py`). Defaults include `data/`, `chroma_db/`, collection `ospf`, embedding model `all-MiniLM-L6-v2` and eight retrieval results. Verify your active Python environment before installing packages. This published branch does not yet provide an approved universal dependency lockfile.

`RAG_GENERATION_MODEL_NAME` defaults to `google/flan-t5-base`; `RAG_RERANKER_MODEL_NAME` to `cross-encoder/ms-marco-MiniLM-L-6-v2`. Optional `RAG_DATA_DIR` / `RAG_CHROMA_DIR` override paths (prefer absolute paths). Environment variables override `.env`; restart the API after changes because settings are cached. Ingest and vector/legacy retrieval must use the index's embedding model. Page discovery and candidate validation default to relative `data/`, independently of `RAG_DATA_DIR`; pass `--data-dir <directory>` for a custom corpus.

### 1a. Dependency reproducibility (Windows Python 3.11)

The published `requirements.txt` does not pin versions. A locally generated `requirements-win-py311.lock.txt` may exist but is **not automatically approved, tracked or portable**. Before adopting such a lockfile, independently verify the generation method, Python/OS support, clean Windows installs, CI compatibility, consistency with the requirements file, and an update policy. Keep dependency changes in a separate reviewed commit.

### 2. Prepare and ingest PDF sources

Place PDF files directly in `data/` using the `*.pdf` extension. Review source filenames, configuration and backups **before** ingest:

```bash
python -m scripts.ingest
```

**Destructive operation:** The script drops an existing collection with the configured name and recreates it. It does not append incrementally. It extracts physical PDF pages, cleans text, chunks it (1000 characters / 150 overlap by default), embeds and upserts into Chroma, preserving source/page/chunk metadata.

Deletion happens **before** PDF extraction and upsert. A later failure does not restore the old index; ingestion is not transactional. Back up the Chroma directory while processes using it are stopped.

Verify count and sample metadata **without changing collection records**:

```bash
python -c "import chromadb; from app.config import get_settings; s=get_settings(); c=chromadb.PersistentClient(path=str(s.chroma_dir)).get_collection(name=s.collection_name); print('COLLECTION:', c.name, 'CHUNKS:', c.count()); print(c.get(limit=3, include=['metadatas']))"
```

`PersistentClient` is not read-only: opening it may create a directory/database or run migrations. Check that the intended `RAG_CHROMA_DIR` exists first; use an index copy for strictly immutable inspection.

Keep private PDFs, indices, `.env` secrets and model caches out of Git. Document corpus/configuration changes before comparing evaluation runs.

### 3. Run and inspect the application

```bash
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs. Supported endpoints include `/`, `/health`, `/ready`, `/stats` and `/ask`. Example PowerShell request:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType 'application/json' -Body '{"question":"How does OSPF select the router ID?"}'
```

BM25 is selectable in the offline evaluation CLI, **not** as an established `/ask` retrieval mode. Hybrid RRF integration is experimental, not a documented deployed endpoint.

### 4. PDF evidence discovery and offline evaluation

Explore source *pages* independently of Chroma-backed chunk retrieval:

```bash
python -m scripts.search_pdf "OSPF router ID" --top-k 10 --interactive
```

Evaluate existing golden-evidence datasets:

```bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

Evaluation prints MRR, Hit@K and retrieval-only latency. It appends JSONL run history with dataset hash and Git provenance. **TEST is intentionally unavailable for iterative tuning.** Follow [EVALUATION.md](EVALUATION.md) for ground-truth construction, validation, approval and interpretation.

### 5. Tests, Git and Docker

```bash
python -m pytest -q
python -m pytest -q tests/retrievers/test_bm25.py
git diff --check
git diff --cached --check
python -m scripts.git_check
```

Use explicit `git add <paths>`, review staged changes, and follow project agent/governance rules. Never silently modify gold evidence to improve a score.

Inspect `git status --short` and `git branch --show-current` first. Continue PR #3 on `docs/bilingual-rag-runbooks-20261028`, based on `document-search-bm25`; do not switch across unrelated WIP. After staging exact paths, inspect `git diff --cached` and its file list. The helper checks staged whitespace and runs tests; it does not verify secrets, approvals or scope. Commit/push only within authorized scope; never merge automatically.

Docker commands (from the project directory):

```bash
docker compose up --build
docker compose down
```

Compose exposes http://127.0.0.1:8001/docs and mounts Chroma/model-cache directories. The image omits `document_search/`, `evaluation/`, `eval/` and PDFs. Run ingestion, page discovery and evaluation natively; the API container needs a compatible existing index and model access on first use.

Compose does **not** pass the host `.env` to the application: it defines neither `env_file` nor `environment`, and the image contains only `.env.example`. Custom `RAG_*` values require explicit local Compose configuration with container-valid paths. Startup or `/health` alone does not verify `/ask`; also inspect `/ready` and `/stats`.

### 6. Troubleshooting and limits

- Missing PDFs: inspect `data/`, exact filenames and `*.pdf` extension.
- Missing collection: check `RAG_COLLECTION_NAME`, `chroma_db/` and whether ingestion completed.
- Package import errors: check Python interpreter, virtual environment and project working directory.
- `FIRST_EVIDENCE_RANK=None`: no ranked result matched the declared source/page/text evidence; this does not prove the retriever returned no documents.
- Fast latency measurements exclude initialization and full answer generation; compare repeated warmed runs for operational conclusions.
