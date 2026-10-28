<a id="top"></a>

# Golden evidence and retrieval evaluation / Golden evidence a evaluace retrievalu

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [CZ — Česká metodika](#cz-cz--česká-metodika)
- [1. Co je golden evidence?](#cz-1-co-je-golden-evidence)
- [2. Rozdělení datasetů](#cz-2-rozdělení-datasetů)
- [3. Jak vytvořit nový důkaz: evidence → question](#cz-3-jak-vytvořit-nový-důkaz-evidence--question)
- [4. Validace kandidátů](#cz-4-validace-kandidátů)
- [5. Povýšení schválených kandidátů](#cz-5-povýšení-schválených-kandidátů)
- [6. Jak se důkaz páruje s chunkem](#cz-6-jak-se-důkaz-páruje-s-chunkem)
- [7. Spuštění offline evaluace](#cz-7-spuštění-offline-evaluace)
- [8. Historický baseline Phase 3.4 (2026-10-20)](#cz-8-historický-baseline-phase-34-2026-10-20)

**English**

- [EN — English methodology](#en-en--english-methodology)
- [1. Definition and source of truth](#en-1-definition-and-source-of-truth)
- [2. Dataset separation](#en-2-dataset-separation)
- [3. Evidence-first curation workflow](#en-3-evidence-first-curation-workflow)
- [4. Validation, approval and promotion](#en-4-validation-approval-and-promotion)
- [5. Matching and metrics](#en-5-matching-and-metrics)
- [6. Repeatable evaluation and historical baseline](#en-6-repeatable-evaluation-and-historical-baseline)
- [7. Governance references](#en-7-governance-references)

</details>

---

> **Policy:** The real `eval/dev_questions.json`, `eval/random_questions.json` and `eval/test_questions.json` datasets are protected. Candidate generation never modifies these files. Promotion requires explicit human approval. The TEST set is held out and must not be used to tune retrieval.
>
> **Pravidlo:** Skutečné DEV/RANDOM/TEST datasety jsou chráněné. Generování kandidátů je nesmí upravovat. Povýšení kandidátů vyžaduje výslovný souhlas člověka a TEST nesmí sloužit k ladění.


<a id="cz"></a>


[↑ Obsah / Contents](#obsah)

<a id="cz-cz--česká-metodika"></a>

## CZ — Česká metodika


[↑ Obsah / Contents](#obsah)

<a id="cz-1-co-je-golden-evidence"></a>

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


[↑ Obsah / Contents](#obsah)

<a id="cz-2-rozdělení-datasetů"></a>

### 2. Rozdělení datasetů

| Dataset | Soubor | Úloha |
| --- | --- | --- |
| DEV | `eval/dev_questions.json` | Vývoj a měřené změny |
| RANDOM | `eval/random_questions.json` | Robustnost, nové typy selhání |
| TEST | `eval/test_questions.json` | Oddělená závěrečná kontrola; nikoli tuning |

Historický rozsah projektu: DEV 20, RANDOM 25 a TEST 15 otázek. Konkrétní počet ověř při načtení datasetu a u každého měření zaznamenej hash. Přehledové soubory mohou obsahovat starší naměřené hodnoty; samotný nový běh je autoritativní pro daný commit a lokální korpus.


[↑ Obsah / Contents](#obsah)

<a id="cz-3-jak-vytvořit-nový-důkaz-evidence--question"></a>

### 3. Jak vytvořit nový důkaz: evidence → question

1. Vezmi **původní lokální PDF** z `data/`. Nepoužívej internet jako zdroj referenčního textu.
2. Objev relevantní fyzickou stránku přes samostatný page explorer:
   
   ```powershell
   python -m scripts.search_pdf "OSPF router ID" --top-k 10 --interactive
   ```
3. Ručně ověř, zda pasáž opravdu odpovídá na jednu konkrétní otázku, a zapiš přesný název PDF, číslo fyzické stránky a stabilní doslovný fragment.
4. **Teprve podle ověřené pasáže** formuluj otázku (evidence → question). Nekonstruuj nejprve otázku a nehledej dodatečně přibližně odpovídající text.
5. Zkontroluj duplicity vůči DEV/RANDOM, vyváženost témat a jednoznačnost odpovědi. Duplicity vůči TEST nech ověřit skriptem; ručně jeho obsah při ladění neprocházej.
6. Ulož kandidátní JSON pouze do `eval/candidates/`, například `eval/candidates/new_batch.json`. Kurátor má standardně připravit pět kandidátů na dávku, pokud zadání neurčuje jinak.

Page explorer používá BM25 index *stránek*. Vyhodnocované retrievery pracují s chunky z Chroma. Výsledek page exploreru **není automaticky správná golden evidence**.


[↑ Obsah / Contents](#obsah)

<a id="cz-4-validace-kandidátů"></a>

### 4. Validace kandidátů

```powershell
# Spusť z rag_api_project/; new_batch.json je zástupný název.
python -m scripts.validate_eval_candidates eval/candidates/new_batch.json
```

Skript načte existující DEV/RANDOM/TEST datasety a porovná ID a normalizované texty otázek. Validátor porovnává doslovné fragmenty s původním lokálním PDF textem po normalizaci velikosti písmen a whitespace. Současná opravená implementace ověřuje každou deklarovanou stránku a odmítá duplicitní normalizované otázky uvnitř jedné dávky.

Strukturální loader vyžaduje neprázdné texty, neprázdné seznamy důkazů/fragmentů a kladná celočíselná čísla stránek (ne `true`/`false`). Na **každé** uvedené stránce musí být alespoň jeden fragment; různé stránky mohou odpovídat různým fragmentům. Validátor však nezaručuje ověření **každého** fragmentu z `contains_any`: všechny alternativy musí ručně ověřit kurátor. Prázdné stránky bez extrahovatelného textu nejsou v lookupu; hláška o chybějícím source/page tak nemusí znamenat neexistující fyzickou stránku. OCR není součástí workflow.

Skripty kontrolují pouze existující chráněné datasety, nikoli ostatní dávky v `eval/candidates/`; chybějící dataset přeskočí. Před validací ověř přítomnost všech tří datasetů. Duplicity faktů/parafrází vyžadují ruční kontrolu DEV/RANDOM. `--data-dir <adresář>` určuje korpus pro validaci i povýšení a nepřebírá `RAG_DATA_DIR`.

Revize 2026-10-28: všech sedm verzovaných dávek má platnou strukturu (5 položek každá), ale všech 35 ID už existuje v chráněných datasetech. Jde o historické dávky, nikoli nové kandidáty k opětovnému povýšení; úplná validace je správně odmítne jako kolize ID. Skutečnou shodu fragmentů s PDF tím tato revize nepotvrzuje.

Úspěch vypíše například `VALID: 5 candidate(s)`. To **neznamená automatické schválení kvality**: člověk musí stále ověřit, zda fragment skutečně dokládá celou odpověď a zda stránka a otázka dávají věcný smysl.

Pokud validace selže, oprav **pouze kandidátní JSON**, ne validátor ani stávající golden evidence. Validátor nemá být oslabován kvůli průchodu chybné dávky.


[↑ Obsah / Contents](#obsah)

<a id="cz-5-povýšení-schválených-kandidátů"></a>

### 5. Povýšení schválených kandidátů

Povýšení do skutečného datasetu je **zvláštní, zapisující a chráněná operace**. Kurátorský agent ji nesmí provádět. Následující syntaxe je určena výhradně pro člověkem schválené ID a cílový dataset (příklady jsou zástupné):

```powershell
python -m scripts.promote_eval_candidates eval/candidates/new_batch.json eval/dev_questions.json --ids routing_dev_101
```

Před spuštěním zkontroluj zdroj, cílový soubor a seznam ID; zálohuj schválený dataset a počítej s tím, že příkaz soubor **změní**. U změn chráněných souborů platí GitHub governance v `.github/workflows/eval-governance.yml` včetně lidského schválení. Nikdy automaticky nepovyšuj kandidáty do TEST pro následné ladění.

`--ids` přijímá jedno nebo více ID oddělených mezerami. Skript znovu validuje pouze vybrané kandidáty a přepíše celý cílový JSON bez automatické zálohy a bez kontroly lidského schválení. Schválení je procesní hranice, nikoli CLI přepínač. CI kontroluje u kandidátů pouze **strukturu**, ne shodu se soukromými PDF. Po lidské revizi chráněných změn musí oprávněný člověk přidat label `human-approved-eval-change`. Workflow nereaguje na samotné přidání labelu a opakování starého běhu může používat starý payload; pro ověření zajisti nový PR běh s aktuálními labely.


[↑ Obsah / Contents](#obsah)

<a id="cz-6-jak-se-důkaz-páruje-s-chunkem"></a>

### 6. Jak se důkaz páruje s chunkem

`evaluation/evidence.py` normalizuje text pomocí `casefold()` a sjednocení whitespace. Chunk se považuje za shodný, pokud v rámci **jednoho GoldEvidence objektu** sedí název zdroje, jeho fyzická stránka patří do `pages`, a text chunku obsahuje alespoň jeden fragment z `contains_any`.

`first_evidence_rank` je první pozice shodného chunku v seřazených výsledcích, od 1; `None` znamená, že se shodný důkaz v kontrolovaných výsledcích nenašel. **Neznamená to**, že retriever nevrátil žádné dokumenty. Z prvních pozic se počítají MRR a Hit@1/3/5/8.

Pozor: validátor fragmenty ověřuje vůči textu extrahovanému ze *stránky*, zatímco evaluátor požaduje přítomnost fragmentu uvnitř konkrétního *chunku*. Příliš dlouhý fragment přes hranici chunků může dát falešné neúspěchy. Při tvorbě referencí proto používej krátké, ale dostatečně specifické, nezávisle ověřené pasáže.


[↑ Obsah / Contents](#obsah)

<a id="cz-7-spuštění-offline-evaluace"></a>

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

Pro reprodukci ulož mimo automatickou historii také SHA-256 každého PDF, identitu/snapshot indexu a počet chunků, parametry ingestu, verze a revize modelů, Python/balíčky, OS/hardware a postup warm-upu. Tyto údaje se automaticky neukládají a dirty příznak neuchovává samotný diff. Historii exportuj před rotací. CLI neprovádí warm-up ani nemá parametr pro opakování; měří i první `search()`. `--dataset random` zde vyhodnotí **celý** pevný RANDOM dataset, nikoli nový náhodný vzorek. Starší `scripts.evaluate_random` má samostatné neopravené chyby v historii, Git statusu a výpisu metrik; pro tento postup použij `scripts.evaluate_retrieval --dataset random`.


[↑ Obsah / Contents](#obsah)

<a id="cz-8-historický-baseline-phase-34-2026-10-20"></a>

### 8. Historický baseline Phase 3.4 (2026-10-20)

| Dataset | Retriever | MRR | Hit@1 | Hit@3 | Hit@5 | Hit@8 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| DEV (20) | BM25 | 0.7171 | 0.60 | 0.80 | 0.85 | 0.90 |
| DEV (20) | Vector | 0.8321 | 0.75 | 0.90 | 0.90 | 0.95 |
| RANDOM (25) | BM25 | 0.8133 | 0.72 | 0.92 | 0.92 | 0.92 |
| RANDOM (25) | Vector | 0.6050 | 0.44 | 0.72 | 0.80 | 0.84 |

MRR jsou doložena v [LEARNING_LOG.md](../../LEARNING_LOG.md). Hodnoty Hit@K pocházejí z předchozího pracovního reportu a bez původních JSONL běhů je nelze nezávisle potvrdit. Nejsou zárukou stejného výsledku při změně dat nebo prostředí. Latency jednotlivých krátkých běhů nepovažuj za finální benchmark. TEST zůstává nedotčený.

---


<a id="en"></a>


[↑ Obsah / Contents](#obsah)

<a id="en-en--english-methodology"></a>

## EN — English methodology


[↑ Obsah / Contents](#obsah)

<a id="en-1-definition-and-source-of-truth"></a>

### 1. Definition and source of truth

A **gold evidence** record is a source-grounded passage, not an LLM-generated answer. It stores `source` (exact PDF filename), `pages` (physical 1-based PDF page numbers, not printed page labels) and `contains_any` (literal evidence fragments with **OR** semantics). An evaluation question also has `id`, `topic` and `question`. Multiple GoldEvidence records may support independent valid passages.

The [JSON example](#cz-1-co-je-golden-evidence) illustrates the **schema only**; it is not real evidence. Evidence text must be copied from the actual local PDF and must genuinely answer the question.


[↑ Obsah / Contents](#obsah)

<a id="en-2-dataset-separation"></a>

### 2. Dataset separation

- `eval/dev_questions.json` — development and measured tuning.
- `eval/random_questions.json` — reproducible robustness exploration.
- `eval/test_questions.json` — held-out final assessment, never used for iterative tuning.

Historically the project uses 20 DEV, 25 RANDOM and 15 TEST questions. Dataset count and SHA-256 hash belong to the run's provenance.


[↑ Obsah / Contents](#obsah)

<a id="en-3-evidence-first-curation-workflow"></a>

### 3. Evidence-first curation workflow

1. Inspect original PDFs in `data/`; use no external source for gold evidence.
2. Discover candidate *pages* with `python -m scripts.search_pdf "routing query" --top-k 10 --interactive`.
3. Manually verify the exact filename, physical page and directly supporting verbatim fragment.
4. Formulate **one question from that evidence** (evidence → question).
5. Check topic diversity and avoid duplicate questions or facts.
6. Write candidates **only** to `eval/candidates/<batch>.json`, normally five per curator batch.

Page-level BM25 discovery is distinct from Chroma-backed chunk-level BM25 evaluation. A high search score never proves gold validity.


[↑ Obsah / Contents](#obsah)

<a id="en-4-validation-approval-and-promotion"></a>

### 4. Validation, approval and promotion

```bash
python -m scripts.validate_eval_candidates eval/candidates/new_batch.json
```

Validation checks IDs, duplicate question text, local source/page existence and literal fragments (normalized for case/whitespace). The validator now checks **each** listed page; tests cover missing pages and unsupported fragments. A successful `VALID: 5 candidate(s)` is necessary but not sufficient: human factual review is required.

The structural loader rejects empty text/evidence/fragment lists and non-positive or non-integer pages (including booleans). Each declared page must match **at least one** fragment; different pages may match different alternatives. This does not verify **every** `contains_any` fragment, so manually verify all alternatives. Pages without extractable text are absent from the lookup; a missing source/page error can also mean an image-only or blank page. OCR is not implemented.

Only existing protected datasets are checked for duplicates; missing datasets are skipped and other candidate batches are not scanned. Ensure all three datasets exist. Review DEV/RANDOM for repeated facts and paraphrases; use the automatic duplicate check for TEST without manually inspecting its contents during tuning. Validation/promotion use `--data-dir <directory>` independently of `RAG_DATA_DIR`.

As of the 2026-10-28 review, all seven tracked batches pass structural loading (five items each), but all 35 IDs already exist in protected datasets. Treat these as historical batches, not new candidates for promotion; full validation correctly rejects those ID collisions. This review does not confirm their fragments against source PDFs.

**Do not automatically run promotion.** Only after explicit human approval may the owner use the writing command below with an approved target and IDs:

```bash
python -m scripts.promote_eval_candidates eval/candidates/new_batch.json eval/dev_questions.json --ids routing_dev_101
```

This changes a protected dataset. GitHub evaluation governance requires human review/authorization. Never alter existing gold to make a retriever score higher.

`--ids` accepts space-separated IDs. Promotion revalidates only selected candidates and rewrites the target JSON without an automatic backup or an approval check. Human approval is a procedural boundary, not a CLI flag. CI checks candidate **structure only**, not source-PDF truth. After reviewing protected changes, an authorized human must add `human-approved-eval-change`. The workflow does not trigger on labeling alone; rerunning an old run may retain its old event payload, so ensure a fresh PR run sees the current labels.


[↑ Obsah / Contents](#obsah)

<a id="en-5-matching-and-metrics"></a>

### 5. Matching and metrics

`evaluation/evidence.py` matches a retrieved *chunk* only when its source name equals the evidence source, its physical page is allowed, and at least one normalized `contains_any` fragment occurs in the chunk. `FIRST_EVIDENCE_RANK=None` means no evaluated result matched the gold evidence; it does not mean zero results were retrieved.

MRR averages reciprocal rank of the first match (0 for no match); Hit@K counts questions with a match at or before position K. Extracted page text and indexed chunk text can differ; avoid fragments crossing chunk boundaries.


[↑ Obsah / Contents](#obsah)

<a id="en-6-repeatable-evaluation-and-historical-baseline"></a>

### 6. Repeatable evaluation and historical baseline

```bash
python -m scripts.evaluate_retrieval --retriever legacy --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset dev
python -m scripts.evaluate_retrieval --retriever bm25 --dataset dev
python -m scripts.evaluate_retrieval --retriever vector --dataset random
python -m scripts.evaluate_retrieval --retriever bm25 --dataset random
```

The CLI **writes** strategy-specific JSONL histories under `eval/results/`; each file retains up to 10 runs. Provenance includes timestamp, Git commit and dirty state, dataset hash and retrieval configuration. Keep source corpus, indexing and dataset fixed when comparing retrievers.

Also archive PDF SHA-256 hashes, an index snapshot/identity and chunk count, ingest parameters, model versions/revisions, Python/packages, OS/hardware and warm-up procedure. These are not automatically recorded; a dirty flag does not preserve the diff. Export histories before rotation. There is no built-in warm-up or repetition flag; the first `search()` is included. `--dataset random` evaluates the **entire fixed** RANDOM set. The older `scripts.evaluate_random` has unresolved history-path, Git-status and metric-output defects; use `scripts.evaluate_retrieval --dataset random` for this workflow.

The historical Phase 3.4 metrics are in the [baseline table](#cz-8-historický-baseline-phase-34-2026-10-20) (2026-10-20). MRR is recorded in [LEARNING_LOG.md](../../LEARNING_LOG.md); Hit@K values are from an earlier working report and cannot be independently confirmed without its original JSONL runs. These are not current guarantees or production performance claims. Latency is retrieval-only; do not infer full-pipeline cost or response time from it. No TEST tuning.


[↑ Obsah / Contents](#obsah)

<a id="en-7-governance-references"></a>

### 7. Governance references

Read [EVAL_CURATOR_AGENT.md](EVAL_CURATOR_AGENT.md), [../AGENTS.md](../AGENTS.md), the [repository-wide AGENTS.md](../../AGENTS.md), [OPERATIONS.md](OPERATIONS.md) and `.github/workflows/eval-governance.yml` (repository root). Respect human approval boundaries even when a validation script passes.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
