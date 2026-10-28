# AI Engineering Portfolio — Python, RAG a evaluace retrievalu

Český vstupní bod k výukovému projektu AI/RAG a dokumentovému vyhledávání. [English README](README.md).

## Co je implementováno

- FastAPI RAG aplikace nad technickými PDF se zdrojovými informacemi.
- Ingest a chunkování dokumentů do ChromaDB s embeddingy.
- Samostatné strategie pro offline porovnání: **legacy**, **vector**, **BM25**.
- DEV/RANDOM evaluace s golden evidence, MRR, Hit@K, latencí, hashováním datasetu a Git provenance.
- Automatizované testy, Docker/Compose a řízená spolupráce s Codexem.

**Hranice integrace:** BM25 je dostupný v offline evaluačním CLI, nikoliv automaticky v HTTP `/ask`. Hybridní RRF vyhledávání je rozpracované a není součástí potvrzené zveřejněné funkcionality.

## Dokumentace

- [Český přehled RAG projektu](rag_api_project/README.cs.md) / [English project README](rag_api_project/README.md)
- [Provozní návod — CZ + EN](rag_api_project/docs/OPERATIONS.md): instalace, `.env`, ingest, kontrola Chroma, spuštění API, testování.
- [Golden evidence a evaluace — CZ + EN](rag_api_project/docs/EVALUATION.md): tvorba kandidátů, validace, lidské schválení, MRR/Hit@K.
- [Architektura](rag_api_project/docs/ARCHITECTURE.md) · [Roadmapa](rag_api_project/docs/ROADMAP.md) · [Vývojová pravidla](rag_api_project/docs/DEVELOPMENT_GUIDE.md).
- [Pravidla agentů](AGENTS.md) a [projektová pravidla](rag_api_project/AGENTS.md) · [Learning Log](LEARNING_LOG.md).

## Rychlý start na Windows

```powershell
# Z kořene klonovaného repozitáře:
cd rag_api_project
python --version  # Musí být 3.11.x.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Potom vlož vlastní PDF do `data/`. **Před ingestem čti varování v provozním návodu: existující Chroma kolekce je smazána a znovu vytvořena.**

```powershell
python -m scripts.ingest
python -m uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs. Offline evaluaci můžeš spustit samostatně nad již existujícím indexem:

```powershell
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
```

Tyto evaluace zapisují JSONL historii. TEST dataset je záměrně vyhrazen pro závěrečné ověření.

## Vývoj a výsledky

Pracovní pravidlo: **Complete → Measure → Improve**. Historický baseline Phase 3.4 (20. 10. 2026): DEV MRR BM25 `0.7171` vs Vector `0.8321`; RANDOM MRR BM25 `0.8133` vs Vector `0.6050`. Jde o lokálně hlášené výsledky pro konkrétní korpus a konfiguraci, nikoliv univerzální tvrzení o výkonu.

Tento repozitář je aktivně vyvíjený výukový prototyp, ne produkční SaaS. ChatGPT a Codex pomáhají s vysvětlením, testováním a kontrolou; pokrok samostatného programování je veden v `LEARNING_LOG.md`.
