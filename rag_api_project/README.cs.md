<a id="top"></a>

# RAG API — vyhledávání v dokumentech a evaluace retrievalu

[Česky](#cz) · [English](README.md#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Technologie](#cz-technologie)
- [Architektura a moduly](#cz-architektura-a-moduly)
- [Tok dat](#cz-tok-dat)
- [Hlavní návrhová rozhodnutí](#cz-hlavní-návrhová-rozhodnutí)
- [Lokální instalace](#cz-lokální-instalace)
- [Indexování lokálních PDF](#cz-indexování-lokálních-pdf)
- [Spuštění API](#cz-spuštění-api)
- [Testy](#cz-testy)
- [Offline evaluace retrievalu](#cz-offline-evaluace-retrievalu)
- [Samostatné BM25 vyhledávání v PDF](#cz-samostatné-bm25-vyhledávání-v-pdf)
- [Docker a Compose](#cz-docker-a-compose)
- [Současná omezení a další kroky](#cz-současná-omezení-a-další-kroky)
- [Vývoj s pomocí AI a hranice spolupráce](#cz-vývoj-s-pomocí-ai-a-hranice-spolupráce)
- [Rozcestník](#cz-rozcestník)

</details>

---

<a id="cz"></a>

Projekt Python/FastAPI pro odpovídání na otázky nad technickou PDF dokumentací se zaměřením na kvalitu retrievalu, dohledatelnost zdrojů a regresní testování.

**Stav:** aktivně vyvíjený výukový prototyp, nikoli produkční služba. Existující `/ask` pipeline používá Chroma retrieval, výběr kontextu, reranking a odpovědi podle pravidel nebo modelu. Vedle toho repozitář obsahuje vektorový retriever, lexikální BM25 retriever a nástroje offline evaluace retrievalu.


[↑ Obsah / Contents](#obsah)

<a id="cz-technologie"></a>

## Technologie

Python 3.11 · FastAPI · Pydantic · ChromaDB · Sentence Transformers · `rank-bm25` · Transformers/PyTorch · pypdf · pytest · Docker · GitHub Actions.


[↑ Obsah / Contents](#obsah)

<a id="cz-architektura-a-moduly"></a>

## Architektura a moduly

| Komponenta | Cesta | Účel |
| --- | --- | --- |
| HTTP API | `app/main.py` | `/`, `/health`, `/ready`, `/stats`, `/ask` |
| Konfigurace | `app/config.py` | Nastavení Pydantic podle prostředí |
| Koordinace RAG | `app/rag.py` | Odpovědi a podpůrný kontext |
| Existující retrieval pipeline | `app/retrieval.py` | Retrieval, výběr řádků kontextu a reranking |
| Vektorový retrieval | `app/retrievers/vector.py` | Vektorový baseline Chroma |
| BM25 retrieval | `app/retrievers/bm25.py` | Lexikální řazení nad Chroma chunky |
| Ingest PDF | `scripts/ingest.py` | Extrakce a indexování textu PDF |
| CLI vyhledávání v PDF | `scripts/search_pdf.py` | Nezávislé lokální BM25 vyhledávání stránek |
| Evaluace retrievalu | `evaluation/`, `scripts/evaluate_retrieval.py` | Kvalita pořadí, latence a původ výsledků |
| Testy | `tests/` | Jednotkové a regresní testy |


[↑ Obsah / Contents](#obsah)

<a id="cz-tok-dat"></a>

### Tok dat

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

**Hranice integrace:** BM25 je implementované a volitelné v **offline evaluačním CLI** společně s `legacy` a `vector`. HTTP `/ask` API nebylo přepnuto na BM25 ani hybridní režim. Hybridní RRF je rozpracované, nikoli zavedená vydaná funkce.


[↑ Obsah / Contents](#obsah)

<a id="cz-hlavní-návrhová-rozhodnutí"></a>

## Hlavní návrhová rozhodnutí

- Indexované chunky nesou zdroj, fyzickou PDF stránku a metadata chunku pro dohledatelnost.
- BM25 načítá uložené chunky v omezených dávkách, validuje konzistenci dat, filtruje dokumenty bez lexikální shody a při shodě skóre řadí podle vzestupného ID chunku.
- Vektorové vyhledávání vrací skóre typu vzdálenosti (nižší bývá bližší); BM25 vrací skóre relevance (vyšší je první). Surová skóre se nemají přímo porovnávat.
- Evaluace se dělí na vývojová, náhodně vybraná a oddělená testovací data s hashi datasetů a Git původem.
- Modelové generování je záloha k odpovědím podle úlohových pravidel; systém není univerzální produkční QA engine.


[↑ Obsah / Contents](#obsah)

<a id="cz-lokální-instalace"></a>

## Lokální instalace

Spouštěj z `rag_api_project/` s Pythonem 3.11.

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

Verze závislostí nyní nejsou pinované; zatím nejde o plně reprodukovatelnou instalaci podle lock souboru.


[↑ Obsah / Contents](#obsah)

<a id="cz-indexování-lokálních-pdf"></a>

### Indexování lokálních PDF

Vlož technická PDF do `data/` (ignorováno Gitem), potom spusť:

~~~bash
python -m scripts.ingest
~~~

Lokální Chroma kolekce je uložená v `chroma_db/`. Ukázková konfigurace používá název `ospf`. **Pozor: `scripts.ingest` existující kolekci tohoto jména smaže a znovu vytvoří**, místo průběžného doplňování. Pokud je nutné index zachovat, zálohuj jej. API potřebuje vhodná indexovaná data pro odpovědi nad korpusem. Úplný postup: [OPERATIONS.md](docs/OPERATIONS.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-spuštění-api"></a>

## Spuštění API

~~~bash
python -m uvicorn app.main:app --reload
~~~

Interaktivní OpenAPI dokumentaci otevři na `http://127.0.0.1:8000/docs`.

- `GET /` a `GET /health` — životnost služby a informace o prostředí.
- `GET /ready` — ověření dostupnosti RAG služby; vyžaduje funkční korpus/konfiguraci.
- `GET /stats` — informace o kolekci.
- `POST /ask` — přijme JSON otázku a vrátí odpověď s podpůrným kontextem a náhledy zdrojů.

Příklad požadavku:

~~~bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"How does OSPF select the router ID?"}'
~~~

Ve Windows PowerShell použij `Invoke-RestMethod`, pokud se liší shellové uvozování `curl`:

~~~powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType 'application/json' -Body '{"question":"How does OSPF select the router ID?"}'
~~~


[↑ Obsah / Contents](#obsah)

<a id="cz-testy"></a>

## Testy

Z `rag_api_project/`:

~~~bash
python -m pytest -q tests
~~~

Historický **lokálně hlášený** úplný běh po integraci BM25 ve fázi 3.3: **210 úspěšných testů, 1 přeskočený**. Přeskočení způsobila nedostupná oprávnění symlinků ve Windows; hlášena byla deprekační varování externích závislostí. Datované ověřené výsledky jsou v [deníku učení](../LEARNING_LOG.md#cz-ověřený-stav-projektu); nové běhy ověř samostatně na [GitHub Actions](https://github.com/jyenten/AI_roadmap/actions).

BM25 testy používají syntetické Chroma fixtures a pokrývají stránkování, řazení, deterministické rozhodování při shodě skóre, soulad metadat, neplatné dotazy a záznamy i vadné dávky.


[↑ Obsah / Contents](#obsah)

<a id="cz-offline-evaluace-retrievalu"></a>

## Offline evaluace retrievalu

Framework hlásí MRR, Hit@1/3/5/8 a latenci retrievalu mean/p50/p95. Metadata běhu obsahují hash datasetu, Git commit a stav necommitnutých změn. Běhové výsledky pod `eval/results/` jsou vyloučené z verzování.

Podporované příkazy ve zveřejněném evaluačním CLI:

~~~bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
~~~

CLI přijímá `legacy`, `vector`, `bm25` a `dev`/`random`. Zapisuje JSONL historii běhů, proto nejde o operaci pouze pro čtení. Oddělený TEST je vyhrazen závěrečnému hodnocení, nikoli iterativnímu ladění. Postup tvorby evidence a porovnávání viz [EVALUATION.md](docs/EVALUATION.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-samostatné-bm25-vyhledávání-v-pdf"></a>

## Samostatné BM25 vyhledávání v PDF

Samostatné průzkumné CLI indexuje lokální PDF stránky:

~~~bash
python -m scripts.search_pdf "router ID" --top-k 5 --interactive
~~~

Nástroj čte PDF v `data/` a liší se od `BM25Retriever`, který pracuje s Chroma chunky.


[↑ Obsah / Contents](#obsah)

<a id="cz-docker-a-compose"></a>

## Docker a Compose

Repozitář obsahuje Dockerfile a `compose.yaml`:

~~~bash
docker compose up --build
docker compose down
~~~

Compose mapuje hostitelský port `8001` na kontejnerový `8000` a připojuje lokální adresáře Chroma/modelové cache. Jde o lokální kontejnerovou konfiguraci, nikoli hostovanou ukázku.

**Známá omezení:** obraz kopíruje `app/` a `scripts/`, ale vynechává `document_search/`, `evaluation/`, `eval/` a zdrojová PDF. Compose nepředává hostitelský `.env` do kontejneru. Ingest a evaluaci spouštěj nativně; kontejnerové API vyžaduje kompatibilní připojený index. Konfigurační a balíčkové hranice viz [OPERATIONS.md](docs/OPERATIONS.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-současná-omezení-a-další-kroky"></a>

## Současná omezení a další kroky

- Zachovat naměřený baseline fáze 3.4 BM25 oproti Vector na DEV/RANDOM (DEV MRR: 0.7171 oproti 0.8321; RANDOM MRR: 0.8133 oproti 0.6050).
- Experimentovat s hybridním lexikálním + sémantickým retrievalem (RRF) podle měření bez ladění na odděleném TEST.
- Zlepšit pinování závislostí, úplnost Docker balíčku a provozní observabilitu.
- Pokračovat ve zlepšování robustnosti extrakce, hlášení chyb a evaluace na dosud neviděných otázkách.


[↑ Obsah / Contents](#obsah)

<a id="cz-vývoj-s-pomocí-ai-a-hranice-spolupráce"></a>

## Vývoj s pomocí AI a hranice spolupráce

Tento výukový projekt používá ChatGPT a Codex pro vysvětlování, návrh, implementační pomoc, diagnostiku, testy a revize; ne každou komponentu vlastník repozitáře samostatně vymyslel nebo napsal.

[Globální AGENTS.md](../AGENTS.md#cz) popisuje režimy LEARN, IMPLEMENT a REVIEW a vyžaduje lidské schválení integrace. [Projektový AGENTS.md](AGENTS.md#cz) přidává konkrétní pravidla kurátorství evaluačních datasetů včetně lidského schválení povýšení kandidátů. Důkazy dovedností a pokrok jsou v [LEARNING_LOG.md](../LEARNING_LOG.md#cz).

Pro BM25 funkci napsal Codex syntetické regresní testy v izolovaném **lokálním** worktree (`agent/bm25-tests`); zkontrolované testy byly integrovány do veřejné vývojové větve spolu s implementací BM25.

Průběžné experimenty Codexu používají samostatné **soukromé GitHub zrcadlo** (`jyenten/AI_roadmap_codex_mirror`). Jeho `main` uchovává schválený veřejný snapshot a `agent/bm25-tests` je izolovaná vzdálená větev pro práci agenta. Původní lokální worktree je od této nové vzdálené větve oddělený. Synchronizace a integrace jsou ruční a podléhají schvalovacím pravidlům v `AGENTS.md`.


[↑ Obsah / Contents](#obsah)

<a id="cz-rozcestník"></a>

## Rozcestník

| Úkol | Dokument |
| --- | --- |
| Kompletní instalace, `.env`, ingest, kontrola Chroma, API, Docker, testy | [Provozní příručka (CZ/EN)](docs/OPERATIONS.md#cz) |
| Golden evidence, kandidáti, schvalování, validace, metriky | [Evaluace (CZ/EN)](docs/EVALUATION.md#cz) |
| Architektura současná i plánovaná | [ARCHITECTURE.md](docs/ARCHITECTURE.md#cz) |
| Stav a prioritizace vývoje | [ROADMAP.md](docs/ROADMAP.md#cz) |
| Vývoj, testy, Git | [DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md#cz) |
| Pravidla Codex/ChatGPT | [AGENTS.md](AGENTS.md#cz), [globální AGENTS.md](../AGENTS.md#cz) |

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
