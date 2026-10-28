# Golden evidence and retrieval evaluation / Golden evidence a evaluace retrievalu

> **Policy:** The real `eval/dev_questions.json`, `eval/random_questions.json` and `eval/test_questions.json` datasets are protected. Candidate generation never modifies these files. Promotion requires explicit human approval. The TEST set is held out and must not be used to tune retrieval.
>
> **Pravidlo:** Skutečné DEV/RANDOM/TEST datasety jsou chráněné. Generování kandidátů je nesmí upravovat. Povýšení kandidátů vyžaduje výslovný souhlas člověka a TEST nesmí sloužit k ladění.

## CZ — Česká metodika

### 1. Co je golden evidence?

Golden evidence (referenční důkaz) není odpověď vytvořená LLM. Je to **ověřitelný textový fragment z konkrétní fyzické PDF stránky**, který prokazatelně podporuje danou otázku. V tomto projektu ho tvoří trojice:

- `source`: přesný název zdrojového PDF;
- `pages`: seznam fyzických stránek PDF číslovaných od 1, nikoli čísla vytištěná uvnitř dokumentu;
- `contains_any`: jeden nebo více doslovných fragmentů podporujícího textu; mezi fragmenty platí logické **OR**.

Evaluační otázka má navíc `id`, `topic` a `question`. Příklad **pouze formátu** (není to ověřená golden evidence a nesmí se přímo přidat do datasetu):

```json
[
  {
    "id": "routing_dev_example",
    "topic": "routing",
    "question": "Example question about a documented routing fact?",
    "gold_evidence": [
      {
        "source": "Example_Manual.pdf",
        "pages": [12],
        "contains_any": ["Exact evidence fragment copied from the source PDF"]
      }
    ]
  }
]
```

Jedna otázka může mít více objektů `gold_evidence`, pokud ji nezávisle podporuje více pasáží. Fragmenty musí skutečně odpovídat textu ze zdrojového PDF; nevymýšlej je, neupravuj je podle retrieval výsledků a nevybírej fragmenty pouze proto, že je vyhledávač vrací.

### 2. Rozdělení datasetů

| Dataset | Soubor | Úloha |
| --- | --- | --- |
| DEV | `eval/dev_questions.json` | Vývoj a měřené změny |
| RANDOM | `eval/random_questions.json` | Robustnost, nové typy selhání |
| TEST | `eval/test_questions.json` | Oddělená závěrečná kontrola; nikoli tuning |

Historický rozsah projektu: DEV 20, RANDOM 25 a TEST 15 otázek. Konkrétní počet ověř při načtení datasetu a u každého měření zaznamenej hash. Přehledové soubory mohou obsahovat starší naměřené hodnoty; samotný nový běh je autoritativní pro daný commit a lokální korpus.

### 3. Jak vytvořit nový důkaz: evidence → question

1. Vezmi **původní lokální PDF** z `data/`. Nepoužívej internet jako zdroj referenčního textu.
2. Objev relevantní fyzickou stránku přes samostatný page explorer:
   
   ```powershell
   python -m scripts.search_pdf "OSPF router ID" --top-k 10 --interactive
   ```
3. Ručně ověř, zda pasáž opravdu odpovídá na jednu konkrétní otázku, a zapiš přesný název PDF, číslo fyzické stránky a stabilní doslovný fragment.
4. **Teprve podle ověřené pasáže** formuluj otázku (evidence → question). Nekonstruuj otázku a nehledáš dodatečně přibližně odpovídající text.
5. Zkontroluj duplicity vůči existujícím otázkám, vyváženost témat a jednoznačnost odpovědi.
6. Ulož kandidátní JSON pouze do `eval/candidates/`, například `eval/candidates/new_batch.json`. Kurátor má standardně připravit pět kandidátů na dávku, pokud zadání neurčuje jinak.

Page explorer používá BM25 index *stránek*. Vyhodnocované retrievery pracují s chunky z Chroma. Výsledek page exploreru **není automaticky správná golden evidence**.

### 4. Validace kandidátů

```powershell
cd D:\AI_roadmap\rag_api_project
python -m scripts.validate_eval_candidates eval/candidates/new_batch.json
```

Skript načte existující DEV/RANDOM/TEST datasety a porovná ID a normalizované texty otázek. Validátor porovnává doslovné fragmenty s původním lokálním PDF textem po normalizaci velikosti písmen a whitespace. Současná opravená implementace ověřuje každou deklarovanou stránku a odmítá duplicitní normalizované otázky uvnitř jedné dávky.

Úspěch vypíše například `VALID: 5 candidate(s)`. To **neznamená automatické schválení kvality**: člověk musí stále ověřit, zda fragment skutečně dokládá celou odpověď a zda stránka a otázka dávají věcný smysl.

Pokud validace selže, oprav **pouze kandidátní JSON**, ne validátor ani stávající golden evidence. Validátor nemá být oslabován kvůli průchodu chybné dávky.

### 5. Povýšení schválených kandidátů

Povýšení do skutečného datasetu je **zvláštní, zapisující a chráněná operace**. Kurátorský agent ji nesmí provádět. Následující syntaxe je určena výhradně pro člověkem schválené ID a cílový dataset (příklady jsou zástupné):

```powershell
python -m scripts.promote_eval_candidates eval/candidates/new_batch.json eval/dev_questions.json --ids routing_dev_101
```

Před spuštěním zkontroluj zdroj, cílový soubor a seznam ID; zálohuj schválený dataset a počítej s tím, že příkaz soubor **změní**. U změn chráněných souborů platí GitHub governance v `.github/workflows/eval-governance.yml` včetně lidského schválení. Nikdy automaticky nepovyšuj kandidáty do TEST pro následné ladění.

### 6. Jak se důkaz páruje s chunkem

`evaluation/evidence.py` normalizuje text pomocí `casefold()` a sjednocení whitespace. Chunk se považuje za shodný, pokud v rámci **jednoho GoldEvidence objektu** sedí název zdroje, jeho fyzická stránka patří do `pages`, a text chunku obsahuje alespoň jeden fragment z `contains_any`.

`first_evidence_rank` je první pozice shodného chunku v seřazených výsledcích, od 1; `None` znamená, že se shodný důkaz v kontrolovaných výsledcích nenašel. **Neznamená to**, že retriever nevrátil žádné dokumenty. Z prvních pozic se počítají MRR a Hit@1/3/5/8.

Pozor: validátor fragmenty ověřuje vůči textu extrahovanému ze *stránky*, zatímco evaluátor požaduje přítomnost fragmentu uvnitř konkrétního *chunku*. Příliš dlouhý fragment přes hranici chunků může dát falešné neúspěchy. Při tvorbě referencí proto používej krátké, ale dostatečně specifické, nezávisle ověřené pasáže.

### 7. Spuštění offline evaluace

```powershell
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

Aktuální zveřejněné CLI podporuje retrievery `legacy`, `vector`, `bm25` a datasety `dev`, `random`. Experimentální hybrid ani `test` nejsou publikovanou volbou.

Každý běh: vypíše individuální `FIRST_EVIDENCE_RANK`, `RECIPROCAL_RANK`, agregované MRR, Hit@K, latency mean/P50/P95 a **zapíše** JSONL historii do `eval/results/`. Historie je rozdělená podle retrieveru a datasetu, uchovává maximálně 10 běhů na soubor a obsahuje timestamp, Git commit/dirty, hash datasetu a retrieval config. Při porovnávání musí souhlasit verze PDF, indexu, dataset hash i konfigurace.

**Výkonnost:** reportovaná latency měří vyhledávací `search()`, nikoli inicializaci indexu, generování LLM nebo celý HTTP request. Pro seriózní porovnání používej warm-up a opakování.

### 8. Historický baseline Phase 3.4 (2026-10-20)

| Dataset | Retriever | MRR | Hit@1 | Hit@3 | Hit@5 | Hit@8 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| DEV (20) | BM25 | 0.7171 | 0.60 | 0.80 | 0.85 | 0.90 |
| DEV (20) | Vector | 0.8321 | 0.75 | 0.90 | 0.90 | 0.95 |
| RANDOM (25) | BM25 | 0.8133 | 0.72 | 0.92 | 0.92 | 0.92 |
| RANDOM (25) | Vector | 0.6050 | 0.44 | 0.72 | 0.80 | 0.84 |

Tato čísla vycházejí z dřívějších lokálně hlášených běhů. Nejsou zárukou stejného výsledku při změně dat nebo prostředí. Latency jednotlivých krátkých běhů nepovažuj za finální benchmark. TEST zůstává nedotčený.

---

## EN — English methodology

### 1. Definition and source of truth

A **gold evidence** record is a source-grounded passage, not an LLM-generated answer. It stores `source` (exact PDF filename), `pages` (physical 1-based PDF page numbers, not printed page labels) and `contains_any` (literal evidence fragments with **OR** semantics). An evaluation question also has `id`, `topic` and `question`. Multiple GoldEvidence records may support independent valid passages.

The JSON example above illustrates the **schema only**; it is not real evidence. Evidence text must be copied from the actual local PDF and must genuinely answer the question.

### 2. Dataset separation

- `eval/dev_questions.json` — development and measured tuning.
- `eval/random_questions.json` — reproducible robustness exploration.
- `eval/test_questions.json` — held-out final assessment, never used for iterative tuning.

Historically the project uses 20 DEV, 25 RANDOM and 15 TEST questions. Dataset count and SHA-256 hash belong to the run's provenance.

### 3. Evidence-first curation workflow

1. Inspect original PDFs in `data/`; use no external source for gold evidence.
2. Discover candidate *pages* with `python -m scripts.search_pdf "routing query" --top-k 10 --interactive`.
3. Manually verify the exact filename, physical page and directly supporting verbatim fragment.
4. Formulate **one question from that evidence** (evidence → question).
5. Check topic diversity and avoid duplicate questions or facts.
6. Write candidates **only** to `eval/candidates/<batch>.json`, normally five per curator batch.

Page-level BM25 discovery is distinct from Chroma-backed chunk-level BM25 evaluation. A high search score never proves gold validity.

### 4. Validation, approval and promotion

```bash
python -m scripts.validate_eval_candidates eval/candidates/new_batch.json
```

Validation checks IDs, duplicate question text, local source/page existence and literal fragments (normalized for case/whitespace). The validator now checks **each** listed page; tests cover missing pages and unsupported fragments. A successful `VALID: 5 candidate(s)` is necessary but not sufficient: human factual review is required.

**Do not automatically run promotion.** Only after explicit human approval may the owner use the writing command below with an approved target and IDs:

```bash
python -m scripts.promote_eval_candidates eval/candidates/new_batch.json eval/dev_questions.json --ids routing_dev_101
```

This changes a protected dataset. GitHub evaluation governance requires human review/authorization. Never alter existing gold to make a retriever score higher.

### 5. Matching and metrics

`evaluation/evidence.py` matches a retrieved *chunk* only when its source name equals the evidence source, its physical page is allowed, and at least one normalized `contains_any` fragment occurs in the chunk. `FIRST_EVIDENCE_RANK=None` means no evaluated result matched the gold evidence; it does not mean zero results were retrieved.

MRR averages reciprocal rank of the first match (0 for no match); Hit@K counts questions with a match at or before position K. Extracted page text and indexed chunk text can differ; avoid fragments crossing chunk boundaries.

### 6. Repeatable evaluation and historical baseline

```bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

The CLI **writes** strategy-specific JSONL histories under `eval/results/`; each file retains up to 10 runs. Provenance includes timestamp, Git commit and dirty state, dataset hash and retrieval configuration. Keep source corpus, indexing and dataset fixed when comparing retrievers.

The historical Phase 3.4 metrics are in the table above (2026-10-20). They are recorded baselines, not current guarantees or production performance claims. Latency is retrieval-only; do not infer full-pipeline cost or response time from it. No TEST tuning.

### 7. Governance references

Read [EVAL_CURATOR_AGENT.md](EVAL_CURATOR_AGENT.md), [../AGENTS.md](../AGENTS.md), the [repository-wide AGENTS.md](../../AGENTS.md), [OPERATIONS.md](OPERATIONS.md) and `.github/workflows/eval-governance.yml` (repository root). Respect human approval boundaries even when a validation script passes.
