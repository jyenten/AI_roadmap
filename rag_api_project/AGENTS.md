<a id="top"></a>

# Agent Instructions

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Kurátorství evaluačních datasetů](#cz-kurátorství-evaluačních-datasetů)
- [Provozní a evaluační postupy](#cz-provozní-a-evaluační-postupy)

**English**

- [Evaluation dataset curation](#en-evaluation-dataset-curation)
- [Operational and evaluation procedures](#en-operational-and-evaluation-procedures)

</details>

---

<a id="en"></a>
## EN — English


[↑ Obsah / Contents](#obsah)

<a id="en-evaluation-dataset-curation"></a>

## Evaluation dataset curation

When working on evaluation dataset generation or curation:

- Follow `docs/EVAL_CURATOR_AGENT.md`.
- Write generated evaluation candidates only to `eval/candidates/`.
- Never modify:
  - `eval/dev_questions.json`
  - `eval/random_questions.json`
  - `eval/test_questions.json`
  - retrieval implementation
  - evaluation metrics
- Never promote candidates automatically.
- Human approval is required before promotion.
- Every candidate batch must pass:

```bash
python -m scripts.validate_eval_candidates <candidate-file>
```

- Do not weaken or bypass validation to make a candidate pass.
- Gold evidence must come only from local PDFs in `data/`.
- Use physical PDF page numbers.
- Use evidence -> question methodology.


[↑ Obsah / Contents](#obsah)

<a id="en-operational-and-evaluation-procedures"></a>

## Operational and evaluation procedures

Use [OPERATIONS.md](docs/OPERATIONS.md) for the **English/Czech** setup, ingestion, API, Docker and test commands, and [EVALUATION.md](docs/EVALUATION.md) for golden evidence, metrics, validation and human-approved promotion. These documents explain procedures; this file sets agent permissions.

- Before suggesting or running ingest, inspect `scripts/ingest.py` and the selected corpus/collection. Ingest currently **deletes and recreates** the collection. Never run destructive ingest without explicit authorization and a backup decision.
- In evidence curation, retain the source-PDF-only, physical-page and evidence-first rules above. Candidate validation does **not** authorize candidate promotion.
- Never use held-out `eval/test_questions.json` to tune or repeatedly inspect retrieval errors.
- Never overwrite existing DEV/RANDOM/TEST gold evidence, metrics or baseline history as an automatic way to improve results.
- When changing evaluation validation code, add regression tests (including multiple evidence pages) and review the protected-file CI governance policy.
- Do not change `requirements.txt`, lockfiles, architecture or retrieval parameters merely to update documentation. Keep English and Czech usage instructions synchronized.


---

<a id="cz"></a>
## CZ — Česká verze


[↑ Obsah / Contents](#obsah)

<a id="cz-kurátorství-evaluačních-datasetů"></a>

## Kurátorství evaluačních datasetů

Při generování nebo správě evaluačních datasetů:

- Řiď se `docs/EVAL_CURATOR_AGENT.md`.
- Generované evaluační kandidáty zapisuj pouze do `eval/candidates/`.
- Nikdy neměň:
  - `eval/dev_questions.json`
  - `eval/random_questions.json`
  - `eval/test_questions.json`
  - implementaci retrievalu
  - evaluační metriky
- Nikdy automaticky nepovyšuj kandidáty.
- Povýšení vyžaduje lidské schválení.
- Každá dávka kandidátů musí úspěšně projít:

```bash
python -m scripts.validate_eval_candidates <candidate-file>
```

- Neoslabuj ani neobcházej validaci kvůli přijetí kandidáta.
- Gold evidence musí pocházet pouze z lokálních PDF v `data/`.
- Používej fyzická čísla stránek PDF.
- Dodržuj postup evidence -> otázka.


[↑ Obsah / Contents](#obsah)

<a id="cz-provozní-a-evaluační-postupy"></a>

## Provozní a evaluační postupy

[OPERATIONS.md](docs/OPERATIONS.md#cz) používej pro **anglické/české** příkazy instalace, ingestu, API, Dockeru a testů; [EVALUATION.md](docs/EVALUATION.md#cz) pro golden evidence, metriky, validaci a povýšení schválené člověkem. Tyto dokumenty vysvětlují postupy; tento soubor určuje oprávnění agentů.

- Před navržením nebo spuštěním ingestu zkontroluj `scripts/ingest.py` a vybraný korpus/kolekci. Ingest nyní kolekci **smaže a znovu vytvoří**. Destruktivní ingest nikdy nespouštěj bez výslovného oprávnění a rozhodnutí o záloze.
- Při správě evidence zachovej výše uvedená pravidla: pouze zdrojová PDF, fyzické stránky a nejprve evidence. Validace kandidáta **neopravňuje** k jeho povýšení.
- Oddělený `eval/test_questions.json` nikdy nepoužívej k ladění ani k opakovanému rozboru chyb retrievalu.
- Nikdy nepřepisuj existující DEV/RANDOM/TEST gold evidence, metriky ani historii baseline jako automatický způsob zlepšení výsledků.
- Při změně evaluačního validačního kódu přidej regresní testy (včetně více stránek evidence) a zkontroluj pravidla CI pro chráněné soubory.
- Kvůli aktualizaci dokumentace neměň `requirements.txt`, lock soubory, architekturu ani parametry retrievalu. Udržuj české a anglické návody synchronizované.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
