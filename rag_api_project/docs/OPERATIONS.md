# Operations runbook / Provozní příručka

> **Scope / Rozsah:** Current Chroma-backed RAG project, Python 3.11. Commands below run from `rag_api_project/`. This is a local educational prototype, not a production deployment.
>
> **Safety / Bezpečnost:** `python -m scripts.ingest` **deletes and recreates** the existing Chroma collection with the configured name. Back up the index and confirm the PDF corpus and configuration before running. It is **not** an incremental ingest.

## CZ — Český návod

### 1. Předpoklady a instalace (Windows PowerShell)

Požadavky: Python 3.11, Git, přístup k potřebným Python balíčkům a modelům při první instalaci. Pracuj v adresáři `rag_api_project/`:

```powershell
cd D:\AI_roadmap\rag_api_project
python --version
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

Implicitní cesty z `app/config.py`: `data/` pro PDF a `chroma_db/` pro Chroma index. Obsah těchto adresářů může být lokální nebo neveřejný; necommituj soukromé PDF, databázi, `.env` ani modelové cache.

Vlož zdrojová PDF **přímo do** `data/` (nikoli do podadresářů). Současný ingest vyhledává soubory odpovídající vzoru `*.pdf`; před spuštěním ověř přesné názvy a přípony.

### 3. Ingest PDF do ChromaDB

```powershell
python -m scripts.ingest
```

**Pozor — destruktivní operace:** `scripts/ingest.py` zavolá `delete_collection()`, pokud kolekce s daným názvem existuje, a následně vytvoří novou. Neprováděj ingest automaticky jako krok testů nebo rutinní evaluace. Pro opakovaný ingest nejdříve ověř zálohu a schválený záměr.

Aktuální pipeline: extrakce fyzických PDF stránek pomocí pypdf → čištění textu → chunkování (výchozí `chunk_size=1000`, `overlap=150`, ve znacích) → SentenceTransformer embeddingy → Chroma. Chunk metadata obsahují `source` (název PDF), `page` (fyzická stránka od 1) a `chunk_index` (pořadí v rámci PDF). Identifikátory chunků jsou v poli Chroma `ids`, nikoliv automaticky v metadatech.

Po ingestu ověř počet záznamů **bez úpravy databáze**:

```powershell
python -c "import chromadb; from app.config import get_settings; s=get_settings(); c=chromadb.PersistentClient(path=str(s.chroma_dir)).get_collection(name=s.collection_name); print('COLLECTION:', c.name, 'CHUNKS:', c.count())"
```

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

Compose zpřístupňuje API na hostitelském portu 8001. Před používáním Dockeru ověř Dockerfile, build context, umístění lokálních PDF/indexu a dostupnost novějších modulů; nejde o náhradu testu nativního prostředí.

**Diagnostika:** `No PDF files found` znamená zkontrolovat adresář `data/` a příponu souborů. Chybějící Chroma kolekce může znamenat nesprávnou cestu nebo neprovedený ingest. `ModuleNotFoundError` typicky znamená nesprávné prostředí či pracovní adresář. `FIRST_EVIDENCE_RANK=None` neznamená automaticky prázdný retrieval — pouze že žádný z hodnocených chunků neodpovídal golden evidence.

---

## EN — English instructions

### 1. Setup and configuration

Use Python 3.11 and run commands from `rag_api_project/`. On Windows PowerShell:

```powershell
cd D:\AI_roadmap\rag_api_project
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

### 1a. Dependency reproducibility (Windows Python 3.11)

The published `requirements.txt` does not pin versions. A locally generated `requirements-win-py311.lock.txt` may exist but is **not automatically approved, tracked or portable**. Before adopting such a lockfile, independently verify the generation method, Python/OS support, clean Windows installs, CI compatibility, consistency with the requirements file, and an update policy. Keep dependency changes in a separate reviewed commit.

### 2. Prepare and ingest PDF sources

Place PDF files directly in `data/` using the `*.pdf` extension. Review source filenames, configuration and backups **before** ingest:

```bash
python -m scripts.ingest
```

**Destructive operation:** The script drops an existing collection with the configured name and recreates it. It does not append incrementally. It extracts physical PDF pages, cleans text, chunks it (1000 characters / 150 overlap by default), embeds and upserts into Chroma, preserving source/page/chunk metadata.

Verify without writing:

```bash
python -c "import chromadb; from app.config import get_settings; s=get_settings(); c=chromadb.PersistentClient(path=str(s.chroma_dir)).get_collection(name=s.collection_name); print('COLLECTION:', c.name, 'CHUNKS:', c.count())"
```

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

Use explicit `git add <paths>`, review staged changes, and follow project agent/governance rules. Never silently modify gold evidence to improve a score. Docker is available with `docker compose up --build`; Compose exposes the service on host port 8001. Review Docker build coverage before relying on new retriever/evaluation modules inside the image.

### 6. Troubleshooting and limits

- Missing PDFs: inspect `data/`, exact filenames and `*.pdf` extension.
- Missing collection: check `RAG_COLLECTION_NAME`, `chroma_db/` and whether ingestion completed.
- Package import errors: check Python interpreter, virtual environment and project working directory.
- `FIRST_EVIDENCE_RANK=None`: no ranked result matched the declared source/page/text evidence; this does not prove the retriever returned no documents.
- Fast latency measurements exclude initialization and full answer generation; compare repeated warmed runs for operational conclusions.
