<a id="top"></a>

# AI Engineering Portfolio — Python, RAG a evaluace retrievalu

[Česky](#cz) · [English](../../README.md#en) · [Dokumentace](../README.md)

> **Dokumentace a pravidla agentů:** Ostatní Markdown dokumenty jsou v [docs/](../README.md). Před změnou souborů načti [globální pravidla agentů](AGENTS.md) a pro RAG také [projektová pravidla](PROJECT_AGENTS.md).

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Hlavní projekt: RAG API a vyhledávání v dokumentech](#cz-hlavní-projekt-rag-api-a-vyhledávání-v-dokumentech)
- [Co je implementováno](#cz-co-je-implementováno)
- [Ověření](#cz-ověření)
- [Architektura v přehledu](#cz-architektura-v-přehledu)
- [Inženýrský přístup](#cz-inženýrský-přístup)
- [Struktura repozitáře](#cz-struktura-repozitáře)
- [Další kroky](#cz-další-kroky)
- [Jak začít](#cz-jak-začít)
- [Rychlý start na Windows](#cz-rychlý-start-na-windows)

</details>

---

<a id="cz"></a>

Průběžně rozvíjený praktický projekt AI inženýrství zaměřený na **testovatelné vyhledávací systémy** a porozumění jejich chování, nejen na volání LLM API.

**Technologie:** Python 3.11 · FastAPI · Pydantic · ChromaDB · Sentence Transformers · BM25 · Pytest · Docker · GitHub Actions


<a id="cz-hlavní-projekt-rag-api-a-vyhledávání-v-dokumentech"></a>

## Hlavní projekt: RAG API a vyhledávání v dokumentech

**[Otevřít projekt RAG API](PROJECT.md)**

Projekt zpracovává technickou PDF dokumentaci do prohledávatelných chunků a poskytuje FastAPI postup pro otázky a odpovědi. Současně vyvíjí samostatné strategie retrievalu a reprodukovatelný framework offline evaluace.


<a id="cz-co-je-implementováno"></a>

### Co je implementováno

- **API:** FastAPI endpointy pro health, readiness, statistiky a otázky; typované modely požadavků/odpovědí.
- **Dokumentová pipeline:** extrakce textu PDF, chunkování, indexování do ChromaDB a metadata zdroje/stránky/chunku.
- **Retrieval:** vektorový retrieval pomocí větných embeddingů, samostatně testovaný lexikální BM25 retriever a dřívější RAG postup retrievalu/rerankingu.
- **Evaluace:** označené datasety otázek, Hit@1/3/5/8, MRR, latence mean/p50/p95, JSONL historie evaluace, hashe datasetů a Git původ.
- **Testování:** jednotkové a regresní pytest testy se syntetickými fixtures a falešnými Chroma kolekcemi; konfigurace GitHub Actions CI.
- **Nástroje nasazení:** Dockerfile a Compose konfigurace pro API.


<a id="cz-ověření"></a>

### Ověření

Historický *lokálně hlášený* úplný běh po integraci BM25: **210 úspěšných testů, 1 přeskočený** (omezení symlinků ve Windows). Nejde o aktuální počet testů ani tvrzení o současném GitHub Actions. Datované ověřené výsledky jsou v [deníku učení](LEARNING_LOG.md#cz-ověřený-stav-projektu); nové běhy ověř na [GitHub Actions](https://github.com/jyenten/AI_roadmap/actions).


<a id="cz-architektura-v-přehledu"></a>

### Architektura v přehledu

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

**Stav integrace:** `legacy`, `vector` a `bm25` jsou volitelné v **offline evaluačním CLI** (DEV/RANDOM). BM25 **není** zavedený volitelný režim HTTP `/ask`. Hybridní RRF je ve vývoji a nesmí být prezentovaný jako hotový.


<a id="cz-inženýrský-přístup"></a>

## Inženýrský přístup

Jde o praktický výukový projekt vyvíjený s výraznou pomocí AI. ChatGPT a Codex používám pro vysvětlování, návrhové diskuse, návrhy a generování kódu, diagnostiku, testy a revize. Také sám implementuji a upravuji kód, zkoumám selhání a ověřuji změny. Repozitář dokumentuje vývojový proces i výsledný systém; netvrdí, že jsem každou komponentu samostatně vymyslel či napsal.

Pravidla spolupráce jsou ve dvou úrovních: [globální AGENTS.md](AGENTS.md#cz) určuje režimy LEARN / IMPLEMENT / REVIEW a hranice schvalování; [projektový AGENTS.md](PROJECT_AGENTS.md#cz) přidává ochrany kurátorství evaluačních datasetů. Pokrok a doklady dovedností jsou v [LEARNING_LOG.md](LEARNING_LOG.md#cz).

Pro BM25 milník připravil Codex regresní testy v **izolovaném lokálním Git worktree** na `agent/bm25-tests`. Zkontrolované testy byly poté integrovány do veřejné vývojové větve.

Pro průběžné experimenty agentů zrcadlí **samostatný soukromý GitHub repozitář** (`jyenten/AI_roadmap_codex_mirror`) schválený veřejný snapshot. Jeho `main` je základ zrcadla, `agent/bm25-tests` je vyhrazená práci Codexu. Soukromý repozitář není veřejně přístupný a **synchronizace je ruční**; změny Codexu se bez revize automaticky nezveřejňují ani neslučují.


<a id="cz-struktura-repozitáře"></a>

## Struktura repozitáře

- [rag_api_project/](../../rag_api_project/) — aktivní vývoj FastAPI, RAG, retrievalu a evaluace.
- [docs/](../README.md) — české a anglické příručky, pravidla agentů a deník učení.
- .github/ — konfigurace CI workflow.
- [archive/](../../archive/) — 29 dřívějších složek programovacích a ML cvičení (`ALG/` a `den_1/` až `den_28_Docker/`), přesunutých bez změny obsahu; zachovaných jako historie učení a reference.


<a id="cz-další-kroky"></a>

## Další kroky

- Zachovat naměřené baseline BM25/Vector na DEV a RANDOM z fáze 3.4.
- Implementovat a vyhodnotit hybridní lexikální + sémantický retrieval (RRF) bez ladění na TEST.
- Zlepšovat reprodukovatelnost, pinování závislostí, provozní metriky a úvodní dokumentaci.


<a id="cz-jak-začít"></a>

## Jak začít

Začni [českým přehledem projektu](PROJECT.md) ([English](../en/PROJECT.md)). Pro instalaci/ingest použij dvojjazyčný [provozní návod](OPERATIONS.md#cz); pro tvorbu evidence, validaci, schvalování a evaluaci [příručku golden evidence](EVALUATION.md#cz).

> **Stav projektu:** výukové inženýrské portfolio / aktivně vyvíjený prototyp, nikoli produkční SaaS nebo hostovaná ukázka.


<a id="cz-rychlý-start-na-windows"></a>

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

[↑ Nahoru / Back to top](#top)
