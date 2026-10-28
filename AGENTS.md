<a id="top"></a>

# AI Roadmap — Agent Collaboration Rules

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Cíle](#cz-cíle)
- [Režimy spolupráce](#cz-režimy-spolupráce)
- [LEARN — výchozí režim](#cz-learn--výchozí-režim)
- [IMPLEMENT — výslovné zadání implementace](#cz-implement--výslovné-zadání-implementace)
- [REVIEW — audit](#cz-review--audit)
- [Inženýrský postup](#cz-inženýrský-postup)
- [Pravidla záznamů o učení](#cz-pravidla-záznamů-o-učení)
- [Závěrečný přehled](#cz-závěrečný-přehled)
- [Provozní dokumentace a bezpečnost](#cz-provozní-dokumentace-a-bezpečnost)

**English**

- [Objectives](#en-objectives)
- [Collaboration modes](#en-collaboration-modes)
- [LEARN — default](#en-learn--default)
- [IMPLEMENT — explicit delegation](#en-implement--explicit-delegation)
- [REVIEW — audit](#en-review--audit)
- [Engineering workflow](#en-engineering-workflow)
- [Learning governance](#en-learning-governance)
- [Completion report](#en-completion-report)
- [Operational documentation and safety](#en-operational-documentation-and-safety)

</details>

---

<a id="en"></a>
## EN — English


[↑ Obsah / Contents](#obsah)

<a id="en-objectives"></a>

## Objectives

This repository serves two purposes:

1. Build reliable, maintainable AI/RAG applications.
2. Develop the human owner's independent Python,
   software engineering and AI engineering skills.

Learning quality must not be sacrificed for coding speed.


[↑ Obsah / Contents](#obsah)

<a id="en-collaboration-modes"></a>

## Collaboration modes


[↑ Obsah / Contents](#obsah)

<a id="en-learn--default"></a>

### LEARN — default

Use for new concepts, algorithms and engineering skills.

- Explain the problem and expected behavior first.
- Let the owner design and implement core learning logic.
- Provide focused guidance rather than immediate solutions.
- Implement supporting code or tests when authorized.
- Review the owner's implementation.
- Include a practical understanding check.


[↑ Obsah / Contents](#obsah)

<a id="en-implement--explicit-delegation"></a>

### IMPLEMENT — explicit delegation

Use when the owner delegates a bounded implementation task.

- Respect approved files and acceptance criteria.
- Write idiomatic, maintainable Python.
- Include meaningful regression tests.
- Preserve existing interfaces and user changes.
- Avoid unrelated refactoring and overengineering.
- Do not commit, push or merge without approval.


[↑ Obsah / Contents](#obsah)

<a id="en-review--audit"></a>

### REVIEW — audit

- Prefer read-only inspection.
- Identify concrete defects and reproducible scenarios.
- Distinguish verified bugs from potential risks.
- Recommend minimal fixes and regression tests.
- Do not modify files unless authorized.


[↑ Obsah / Contents](#obsah)

<a id="en-engineering-workflow"></a>

## Engineering workflow

Follow:

Complete -> Measure -> Improve

- Keep modules cohesive and responsibilities clear.
- Test functionality, edge cases and data integrity.
- Never weaken tests merely to obtain a passing result.
- Preserve evaluation reproducibility.
- Do not access secrets or private data outside task scope.
- Respect nested AGENTS.md files.
- Never use git add . for automatic staging.


[↑ Obsah / Contents](#obsah)

<a id="en-learning-governance"></a>

## Learning governance

Maintain LEARNING_LOG.md.

- Suggest updates after meaningful milestones.
- Distinguish completed project work from demonstrated skills.
- Never mark a skill as mastered without practical evidence.
- Prefer independent exercises and debugging tasks.
- Do not alter learning assessments without human approval.


[↑ Obsah / Contents](#obsah)

<a id="en-completion-report"></a>

## Completion report

For implementation work, report:

1. Files changed.
2. Tests executed and results.
3. Important design decisions.
4. Remaining limitations.
5. Concepts the owner should understand.

The human owner approves final integration and commits.


[↑ Obsah / Contents](#obsah)

<a id="en-operational-documentation-and-safety"></a>

## Operational documentation and safety

For work inside `rag_api_project/`, read the project [README](rag_api_project/README.md), [operations runbook](rag_api_project/docs/OPERATIONS.md) and [evaluation guide](rag_api_project/docs/EVALUATION.md) as applicable. The English and Czech instructions must describe the same implemented behavior.

- Inspect the actual CLI and source code before documenting commands; never invent flags, paths or completed features.
- Treat `python -m scripts.ingest` as **destructive**: it deletes and recreates an existing named Chroma collection. Never launch it or replace a user's local index without explicit authorization.
- Do not expose or commit source PDFs, `.env`, private corpora, model caches or local Chroma data.
- Do not modify golden evidence, benchmark metrics or protected evaluation datasets to raise a retrieval score.
- Preserve DEV/RANDOM baselines and the independence of held-out TEST; report dataset hash, Git provenance and configuration when claiming a comparison.
- Keep documentation-only edits separate from validator fixes and dependency/version updates where practical.
- In REVIEW mode, report verified defects separately from risks; do not modify files unless the owner approved the change.


---

<a id="cz"></a>
## CZ — Česká verze


[↑ Obsah / Contents](#obsah)

<a id="cz-cíle"></a>

## Cíle

Tento repozitář má dva cíle:

1. Vytvářet spolehlivé a udržovatelné AI/RAG aplikace.
2. Rozvíjet samostatné dovednosti vlastníka projektu v Pythonu, softwarovém a AI inženýrství.

Kvalita učení se nesmí obětovat rychlosti psaní kódu.


[↑ Obsah / Contents](#obsah)

<a id="cz-režimy-spolupráce"></a>

## Režimy spolupráce


[↑ Obsah / Contents](#obsah)

<a id="cz-learn--výchozí-režim"></a>

### LEARN — výchozí režim

Používej pro nové pojmy, algoritmy a inženýrské dovednosti.

- Nejprve vysvětli problém a očekávané chování.
- Nech vlastníka navrhnout a implementovat hlavní výukovou logiku.
- Poskytuj cílené vedení místo okamžitých řešení.
- Podpůrný kód nebo testy implementuj po schválení.
- Zkontroluj implementaci vlastníka.
- Zařaď praktické ověření porozumění.


[↑ Obsah / Contents](#obsah)

<a id="cz-implement--výslovné-zadání-implementace"></a>

### IMPLEMENT — výslovné zadání implementace

Používej, když vlastník deleguje ohraničený implementační úkol.

- Respektuj schválené soubory a kritéria přijetí.
- Piš idiomatický, udržovatelný Python.
- Přidej smysluplné regresní testy.
- Zachovej existující rozhraní a uživatelské změny.
- Vyhni se nesouvisejícímu refaktoringu a zbytečně složitému návrhu.
- Bez schválení neprováděj commit, push ani merge.


[↑ Obsah / Contents](#obsah)

<a id="cz-review--audit"></a>

### REVIEW — audit

- Upřednostni kontrolu bez úprav.
- Urči konkrétní vady a reprodukovatelné scénáře.
- Rozlišuj ověřené chyby od možných rizik.
- Doporuč minimální opravy a regresní testy.
- Soubory neupravuj bez oprávnění.


[↑ Obsah / Contents](#obsah)

<a id="cz-inženýrský-postup"></a>

## Inženýrský postup

Dodržuj:

Complete -> Measure -> Improve

- Udržuj soudržné moduly a jasné odpovědnosti.
- Testuj funkčnost, okrajové případy a integritu dat.
- Nikdy neoslabuj testy jen kvůli úspěšnému výsledku.
- Zachovej reprodukovatelnost evaluace.
- Nepřistupuj k tajným ani soukromým datům mimo rozsah úkolu.
- Respektuj vnořené soubory AGENTS.md.
- Nikdy nepoužívej git add . pro automatický staging.


[↑ Obsah / Contents](#obsah)

<a id="cz-pravidla-záznamů-o-učení"></a>

## Pravidla záznamů o učení

Udržuj LEARNING_LOG.md.

- Navrhuj aktualizace po významných milnících.
- Odděluj dokončenou projektovou práci od prokázaných dovedností.
- Bez praktických důkazů nikdy neoznačuj dovednost za zvládnutou.
- Upřednostni samostatná cvičení a diagnostické úkoly.
- Bez lidského schválení neměň hodnocení dovedností.


[↑ Obsah / Contents](#obsah)

<a id="cz-závěrečný-přehled"></a>

## Závěrečný přehled

U implementační práce uveď:

1. Změněné soubory.
2. Spuštěné testy a výsledky.
3. Důležitá návrhová rozhodnutí.
4. Zbývající omezení.
5. Pojmy, kterým má vlastník rozumět.

Konečnou integraci a commity schvaluje lidský vlastník.


[↑ Obsah / Contents](#obsah)

<a id="cz-provozní-dokumentace-a-bezpečnost"></a>

## Provozní dokumentace a bezpečnost

Při práci v `rag_api_project/` si podle úkolu přečti projektový [README](rag_api_project/README.cs.md), [provozní návod](rag_api_project/docs/OPERATIONS.md#cz) a [evaluační příručku](rag_api_project/docs/EVALUATION.md#cz). Anglické a české pokyny musí popisovat stejné implementované chování.

- Před dokumentováním příkazů zkontroluj skutečné CLI a zdrojový kód; nevymýšlej parametry, cesty ani dokončené funkce.
- Považuj `python -m scripts.ingest` za **destruktivní** operaci: existující pojmenovanou Chroma kolekci smaže a znovu vytvoří. Bez výslovného oprávnění jej nespouštěj ani nenahrazuj uživatelův lokální index.
- Nezveřejňuj ani necommituj zdrojová PDF, `.env`, soukromé korpusy, cache modelů ani lokální Chroma data.
- Neměň golden evidence, benchmarkové metriky ani chráněné evaluační datasety za účelem zvýšení skóre retrievalu.
- Zachovej baseline DEV/RANDOM a nezávislost odděleného TEST; při tvrzení o porovnání uveď hash datasetu, Git původ a konfiguraci.
- Kde je to praktické, odděl úpravy dokumentace od oprav validátoru a změn závislostí či jejich verzí.
- V režimu REVIEW uváděj ověřené vady odděleně od rizik; soubory upravuj jen po schválení vlastníkem.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
