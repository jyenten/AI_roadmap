# RAG API — český návod

[English project README](README.md) · [Hlavní český README](../README.cs.md)

Tento projekt přijímá technická PDF, extrahuje jejich text do chunků, indexuje je v ChromaDB a poskytuje FastAPI rozhraní pro otázky nad korpusem. Vedle existujícího RAG `/ask` existuje samostatné experimentální rozhraní pro evaluaci **legacy**, **vector** a **BM25** retrievalu.

## Rozcestník

| Úkol | Dokument |
| --- | --- |
| Kompletní instalace, `.env`, ingest, kontrola Chroma, API, Docker, testy | [Provozní příručka (CZ/EN)](docs/OPERATIONS.md) |
| Golden evidence, kandidáti, schvalování, validace, metriky | [Evaluace (CZ/EN)](docs/EVALUATION.md) |
| Architektura současná i plánovaná | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Stav a prioritizace vývoje | [ROADMAP.md](docs/ROADMAP.md) |
| Vývoj, testy, Git | [DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md) |
| Pravidla Codex/ChatGPT | [AGENTS.md](AGENTS.md), [globální AGENTS.md](../AGENTS.md) |

## Základní spuštění (PowerShell)

```powershell
cd D:\AI_roadmap\rag_api_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Vlož vhodné `*.pdf` soubory do `data/`. **Pozor: následující ingest destruktivně obnoví existující kolekci** se stejným názvem. Nejprve zkontroluj zálohy a konfiguraci.

```powershell
python -m scripts.ingest
python -m uvicorn app.main:app --reload
```

API dokumentace: http://127.0.0.1:8000/docs. Chroma kolekce má standardně název `ospf`. Nastavení modelů a cesty jsou v `app/config.py` a `.env`.

## Golden evidence a evaluace

```powershell
# Průzkum původních PDF stránek, bez Chroma indexu
python -m scripts.search_pdf "OSPF router ID" --top-k 10 --interactive

# Validace nových kandidátů (soubor musí existovat)
python -m scripts.validate_eval_candidates eval/candidates/new_batch.json

# Offline evaluace proti schválenému DEV datasetu
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev

# Robustnost na RANDOM
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

`eval/dev_questions.json`, `eval/random_questions.json` a `eval/test_questions.json` jsou chráněné. Candidate generator smí zapisovat jen do `eval/candidates/`; povýšení vyžaduje výslovné lidské schválení. **TEST se nepoužívá k ladění.** Podrobnosti a JSON schéma viz [EVALUATION.md](docs/EVALUATION.md).

## Kontrola kvality

```powershell
python -m pytest -q
git diff --check
# Po explicitním stagingu souborů:
python -m scripts.git_check
```

Předchozí hlášená regresní sada po Phase 3.4 prošla; počet testů se po dalších změnách může lišit. Výstupy evaluace ukládají MRR, Hit@K, latenci mean/P50/P95 a JSONL historii s Git provenance. Jednotlivé krátké latency běhy nejsou výkonnostní benchmark celé aplikace.

## Aktuální stav

**Dostupné:** standalone RAG API, chunkový Vector a BM25 retriever, offline CLI pro `legacy`, `vector`, `bm25` na DEV/RANDOM. **Zatím nepovažuj za dokončené:** integraci BM25/hybrid do `/ask` a hybridní RRF evaluaci. Rozpracovaná lokální změna nemusí být součástí zveřejněné větve.

Docker: `docker compose up --build` (host port 8001). Před provozem ověř kompatibilitu build contextu s aktuálními moduly. Projekt je výukový prototyp.
