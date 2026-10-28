<a id="top"></a>

# AI RAG Project Development Guide

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Odpovědnosti dokumentace](#cz-odpovědnosti-dokumentace)
- [Vývojový postup](#cz-vývojový-postup)
- [Návrh kódu a modulů](#cz-návrh-kódu-a-modulů)
- [Chyby, vedlejší účinky a diagnostika](#cz-chyby-vedlejší-účinky-a-diagnostika)
- [Ověřování a regresní testy](#cz-ověřování-a-regresní-testy)
- [Disciplína retrievalu a evaluace](#cz-disciplína-retrievalu-a-evaluace)
- [Git, revize a integrace](#cz-git-revize-a-integrace)
- [Bezpečnost a správa závislostí](#cz-bezpečnost-a-správa-závislostí)
- [Spolupráce a učení](#cz-spolupráce-a-učení)
- [Dokončení a aktualizace dokumentace](#cz-dokončení-a-aktualizace-dokumentace)

**English**

- [Documentation responsibilities](#en-documentation-responsibilities)
- [Development workflow](#en-development-workflow)
- [Code and module design](#en-code-and-module-design)
- [Errors, side effects and diagnostics](#en-errors-side-effects-and-diagnostics)
- [Verification and regression tests](#en-verification-and-regression-tests)
- [Retrieval and evaluation discipline](#en-retrieval-and-evaluation-discipline)
- [Git, review and integration](#en-git-review-and-integration)
- [Security and dependency management](#en-security-and-dependency-management)
- [Collaboration and learning](#en-collaboration-and-learning)
- [Completion and documentation updates](#en-completion-and-documentation-updates)

</details>

---

<a id="en"></a>
## EN — English

This guide defines **how to develop and review changes**. Phase priorities and
current project status belong to [ROADMAP.md](ROADMAP.md); completed work and
learning evidence belong to [LEARNING_LOG.md](../../LEARNING_LOG.md).


[↑ Obsah / Contents](#obsah)

<a id="en-documentation-responsibilities"></a>

## Documentation responsibilities

| Document | Source of truth for |
| --- | --- |
| [ROADMAP.md](ROADMAP.md) | Approved phases, their goals and acceptance criteria, current development focus |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Implemented components, interfaces and explicitly marked target architecture |
| This guide | Development workflow, code quality, verification and Git practice |
| [OPERATIONS.md](OPERATIONS.md) | Setup, configuration, ingestion, API, Docker and runnable commands (CZ/EN) |
| [EVALUATION.md](EVALUATION.md) | Evidence construction, matching, metrics, evaluation and reproducibility (CZ/EN) |
| [LEARNING_LOG.md](../../LEARNING_LOG.md) | Dated milestones, branch provenance and demonstrated learning evidence |
| [Repository AGENTS.md](../../AGENTS.md), [project AGENTS.md](../AGENTS.md) | Agent permissions, collaboration modes and approval boundaries |

Do not maintain another milestone table, benchmark table or active-phase list
here. Link to the owning document when a procedure needs that context.


[↑ Obsah / Contents](#obsah)

<a id="en-development-workflow"></a>

## Development workflow

Follow **Complete → Measure → Improve**:

1. Inspect the implementation, applicable AGENTS rules, current branch and
   uncommitted changes. Identify the approved roadmap goal and affected files.
2. Define expected behavior, scope and acceptance criteria. Keep useful but
   unrelated ideas in the backlog; do not expand the current phase for them.
3. Complete a working vertical slice before optimizing individual components.
   Prefer one coherent change over a large speculative refactor.
4. Verify behavior with appropriate tests and, for retrieval changes, controlled
   DEV/RANDOM measurements. A manually selected successful query is insufficient.
5. Review the result, record evidence and limitations, then improve the measured
   weakness. Update the document that owns any changed behavior or status.

A new idea belongs in the current change only when it helps satisfy the current
Definition of Done. Do not reopen completed work merely because another design
is imaginable. Reopen it for a concrete evaluation/integration failure, a
security issue or a material requirement change.

The roadmap owns phase-specific goals and Definition of Done checklists. This
guide defines the shared implementation and verification practices below.


[↑ Obsah / Contents](#obsah)

<a id="en-code-and-module-design"></a>

## Code and module design

- Keep one cohesive responsibility per module and a small public interface per
  subsystem. Separate document loading, text processing, retrieval, reranking,
  generation, evaluation and HTTP transport.
- Prefer high cohesion and low coupling. Call public functions instead of
  reaching into another subsystem's internal models, caches or ranking arrays.
- Use explicit typed data models where tuple/dictionary positions obscure
  meaning. Prefer immutable records for document identity, source/page data,
  evidence and completed results; allow mutation only when it is intentional.
- Keep generic infrastructure independent of domain-specific routing terms.
  Domain rules belong at an explicit domain boundary, not in generic ranking.
- Centralize model names, paths and limits in configuration. Preserve published
  interfaces and user changes unless an approved task requires changing them.
- Use idiomatic, typed Python: clear names, small purposeful functions and
  comprehensions/generators where they remain readable. Avoid code golf,
  deeply nested expressions and abstractions without a current need.
- A helper does not automatically require its own file. Split it when reuse,
  independent responsibility, size or testing justifies the boundary.
- Use direct attributes for simple records. Add properties/getters/setters only
  when controlled access provides actual behavior; they are not security controls.
- Do not introduce inheritance, async code, design patterns or metaprogramming
  merely for architectural symmetry. For a large refactor, first establish the
  problem, target boundaries and interfaces in ARCHITECTURE.md.


[↑ Obsah / Contents](#obsah)

<a id="en-errors-side-effects-and-diagnostics"></a>

## Errors, side effects and diagnostics

Validate external input at the appropriate boundary and fail with a useful
reason. Do not silently swallow exceptions, discard failed inputs or report a
partially processed document as a successful ingestion.

Keep pure transformations separate from filesystem/database access, model
loading and history writes. Make significant side effects explicit in function
names, interfaces and operating instructions. Resource limits should cover the
relevant file, PDF-page, query, result-count and request boundaries; verify the
implemented limits rather than assuming a planned control already exists.

Keep security validation separate from text preprocessing: rejecting an unsafe
file must not silently change valid document semantics. Prefer logging in
reusable modules; CLI scripts may print user-facing output. Diagnostics should
identify failures without exposing secrets or private corpus content.


[↑ Obsah / Contents](#obsah)

<a id="en-verification-and-regression-tests"></a>

## Verification and regression tests

Use the verification layer that answers the actual question:

| Layer | Purpose |
| --- | --- |
| Unit tests | Deterministic module behavior, validation and edge cases |
| Integration tests | Behavior across component boundaries |
| Smoke tests | Basic application operation in the intended environment |
| Retrieval evaluation | Evidence-based quality and retrieval latency |

Prefer small synthetic fixtures, fake collections and explicit failure cases
for unit tests. Real PDFs/models belong in suitable integration, manual or
evaluation checks; passing synthetic tests does not prove real-corpus quality.

Add a meaningful regression for a verified defect. Confirm that it exposes the
original failure where practical. Never weaken assertions or validation merely
to obtain a passing result. Test data integrity and interface alignment as well
as the normal success path.

For code changes, run focused tests and the full project suite before commit.
From `rag_api_project/`:

```bash
python -m pytest tests -q
```

For documentation-only changes, verify facts, links, examples and affected
configuration rather than inventing tests that mirror the text. Report exactly
what ran, skips/warnings and material checks that could not be performed. Do not
claim GitHub CI success or real-corpus results from a local report alone.


[↑ Obsah / Contents](#obsah)

<a id="en-retrieval-and-evaluation-discipline"></a>

## Retrieval and evaluation discipline

Use [EVALUATION.md](EVALUATION.md) for the schema, matching rules, CLI commands,
approval/promotion procedure and reproducibility requirements. Use
[EVAL_CURATOR_AGENT.md](EVAL_CURATOR_AGENT.md) for candidate-curation constraints.

- Keep DEV development, RANDOM robustness exploration and held-out TEST separate.
  Do not repeatedly inspect TEST errors and then optimize for them.
- Establish a baseline before changing ranking. Compare DEV/RANDOM runs with
  controlled corpus, index, dataset and configuration; preserve provenance.
- Construct evidence from source PDFs before writing questions. Discovery scores
  do not establish factual validity, even when page and chunk retrieval use
  different implementations of BM25.
- Do not change existing golden evidence, metrics or baseline history to raise a
  score. Candidate validation does not authorize promotion.
- Distinguish measured `search()` latency from initialization and full answer/
  HTTP response cost; state which retrieval or reranking work the timed method
  includes. Do not combine incompatible raw relevance scores without a justified
  scoring method and measured evaluation.


[↑ Obsah / Contents](#obsah)

<a id="en-git-review-and-integration"></a>

## Git, review and integration

The default integration branch is `main`. Prepare new work on a suitable working
branch; preserve unrelated worktrees and uncommitted changes. Do not reset,
stash, switch across or stage someone else's WIP as an incidental cleanup.

Before staging, inspect `git status --short` and `git diff`. Stage exact intended
paths, then review the staged file list and content:

```bash
git diff --cached --stat
git diff --cached
git diff --cached --check
```

Do not use automatic `git add .`. Keep private PDFs, local indices, model caches,
`.env` and other secrets out of commits. Prefer coherent commits with messages
that describe completed behavior; separate unrelated documentation, dependency
and feature changes when practical.

From `rag_api_project/`, the project helper runs staged whitespace checks and
the project test suite:

```bash
python -m scripts.git_check
```

It does not grant approval or establish that secrets, scope, dependencies and
retrieval quality were reviewed. Before pushing, know the working-tree state,
review the intended changes and satisfy applicable AGENTS and repository rules.
Commit, push and merge only within explicit authorization; do not bypass
required reviews or CI policies.


[↑ Obsah / Contents](#obsah)

<a id="en-security-and-dependency-management"></a>

## Security and dependency management

Security applies throughout development, not only during the planned security
phase. Validate external inputs, enforce appropriate filesystem/resource
boundaries, handle secrets deliberately and make failures explicit.

Dependency auditing, Dependency Review, Gitleaks and Dependabot are already
configured. Treat their findings as evidence to investigate; passing Python
tests does not resolve a dependency vulnerability. Do not disable or weaken
checks to make a change appear healthy.

Version pinning and lockfile adoption remain separate, reviewed dependency work.
A platform-specific or locally generated lockfile is not automatically portable
or approved. Verify consistency, supported Python/OS, clean installation,
regression behavior and an update policy before adopting it.

Before recommending or running `python -m scripts.ingest`, explain that it
**deletes and recreates** the configured Chroma collection. Follow the backup,
configuration and authorization boundaries in [OPERATIONS.md](OPERATIONS.md).


[↑ Obsah / Contents](#obsah)

<a id="en-collaboration-and-learning"></a>

## Collaboration and learning

The repository and project AGENTS files govern permissions. Select the mode
appropriate to the owner's request rather than imposing a teaching procedure
on every implementation task:

- **LEARN:** explain the problem and behavior, support the owner's implementation,
  review it and obtain practical understanding evidence.
- **IMPLEMENT:** deliver the delegated bounded change, preserve interfaces/WIP,
  verify it and report the outcome and limitations.
- **REVIEW:** inspect and report reproducible findings; modify files only when
  the owner has authorized fixes.

In LEARN mode, use complete logical units with the goal, rationale, relevant new
concepts, scope and a clear verification step. Give large/risky components their
own focused review; avoid import-by-import conversational steps. Use idiomatic
Python without artificial simplification or unnecessary advanced machinery.

Record meaningful milestones, difficulties, assistance and test evidence in
[LEARNING_LOG.md](../../LEARNING_LOG.md). Separate a completed feature from an
independently demonstrated skill. Do not assign mastery or change learning
assessments without the required human evidence/approval.


[↑ Obsah / Contents](#obsah)

<a id="en-completion-and-documentation-updates"></a>

## Completion and documentation updates

A reusable module is normally complete when its responsibility and interface are
clear, expected behavior works, important inputs are validated, relevant tests
and project regression checks pass, and known intentional limits are documented.
Use the roadmap's specific acceptance criteria for completion of a subphase.
Do not declare it complete while a critical unresolved bug remains.

When behavior or an approved decision changes:

- Update the owning document from the responsibilities table.
- Keep current implementation distinct from target architecture and local WIP.
- Synchronize Czech and English operating/evaluation instructions.
- Put dates, measurements and branch provenance in the learning/evaluation
  records; link to them instead of copying volatile status into every document.
- Report changed files, verification, decisions and remaining limitations.

A phase's goals or priorities change only through an approved roadmap decision.
Do not silently redesign the plan as part of a documentation cleanup.


---

<a id="cz"></a>
## CZ — Česká verze

Tato příručka určuje, **jak vyvíjet a kontrolovat změny**. Priority fází a současný stav projektu patří do [ROADMAP.md](ROADMAP.md#cz); dokončená práce a doklady o učení do [LEARNING_LOG.md](../../LEARNING_LOG.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-odpovědnosti-dokumentace"></a>

## Odpovědnosti dokumentace

| Dokument | Určuje |
| --- | --- |
| [ROADMAP.md](ROADMAP.md#cz) | Schválené fáze, jejich cíle a kritéria přijetí, současné zaměření vývoje |
| [ARCHITECTURE.md](ARCHITECTURE.md#cz) | Implementované komponenty, rozhraní a výslovně označená cílová architektura |
| Tato příručka | Vývojový postup, kvalita kódu, ověřování a práce s Gitem |
| [OPERATIONS.md](OPERATIONS.md#cz) | Instalace, konfigurace, ingest, API, Docker a spustitelné příkazy (CZ/EN) |
| [EVALUATION.md](EVALUATION.md#cz) | Tvorba evidence, párování, metriky, evaluace a reprodukovatelnost (CZ/EN) |
| [LEARNING_LOG.md](../../LEARNING_LOG.md#cz) | Datované milníky, původ práce ve větvích a prokázané učební výsledky |
| [Globální AGENTS.md](../../AGENTS.md#cz), [projektový AGENTS.md](../AGENTS.md#cz) | Oprávnění agentů, režimy spolupráce a hranice schvalování |

Neudržuj zde další tabulku milníků, benchmarků ani seznam aktivních fází. Pokud postup potřebuje tento kontext, odkaž na příslušný dokument.


[↑ Obsah / Contents](#obsah)

<a id="cz-vývojový-postup"></a>

## Vývojový postup

Dodržuj **Complete → Measure → Improve**:

1. Zkontroluj implementaci, platná pravidla AGENTS, současnou větev a necommitnuté změny. Urči schválený cíl roadmapy a dotčené soubory.
2. Vymez očekávané chování, rozsah a kritéria přijetí. Užitečné nesouvisející nápady nech v backlogu; nerozšiřuj kvůli nim současnou fázi.
3. Před optimalizací jednotlivých komponent dokonči funkční celek napříč vrstvami. Upřednostni jednu soudržnou změnu před velkým spekulativním refaktoringem.
4. Ověř chování vhodnými testy a u změn retrievalu řízeným měřením DEV/RANDOM. Jeden ručně vybraný úspěšný dotaz nestačí.
5. Zkontroluj výsledek, zaznamenej důkazy a omezení a pak zlepšuj naměřenou slabinu. Aktualizuj dokument, který spravuje změněné chování nebo stav.

Nový nápad patří do současné změny pouze tehdy, pomáhá-li splnit nynější Definition of Done. Neotevírej dokončenou práci jen proto, že si lze představit jiný návrh. Znovu ji otevři při konkrétním selhání evaluace/integrace, bezpečnostním problému nebo podstatné změně požadavků.

Cíle a checklisty Definition of Done jednotlivých fází určuje roadmapa. Tato příručka níže stanovuje společné implementační a ověřovací postupy.


[↑ Obsah / Contents](#obsah)

<a id="cz-návrh-kódu-a-modulů"></a>

## Návrh kódu a modulů

- Každému modulu ponech jednu soudržnou odpovědnost a každému subsystému malé veřejné rozhraní. Odděluj načítání dokumentů, zpracování textu, retrieval, reranking, generování, evaluaci a HTTP přenos.
- Upřednostni vysokou soudržnost a malou provázanost. Volej veřejné funkce místo přístupu k interním modelům, cache nebo polím pořadí jiného subsystému.
- Používej výslovné typované modely, pokud pozice v n-tici/slovníku zakrývají význam. Pro identitu dokumentu, zdroj/stránku, evidenci a hotové výsledky preferuj neměnné záznamy; mutaci povol pouze záměrně.
- Obecnou infrastrukturu udržuj nezávislou na doménových směrovacích pojmech. Doménová pravidla patří na výslovnou doménovou hranici, nikoli do obecného řazení.
- Názvy modelů, cesty a limity centralizuj v konfiguraci. Zachovej zveřejněná rozhraní a uživatelské změny, pokud schválený úkol nevyžaduje jejich změnu.
- Piš idiomatický typovaný Python: jasné názvy, malé účelné funkce, comprehensions/generátory tam, kde zůstávají čitelné. Vyhni se samoúčelně krátkému kódu, hluboce vnořeným výrazům a abstrakcím bez současné potřeby.
- Pomocná funkce automaticky nepotřebuje vlastní soubor. Odděl ji, pokud hranici odůvodní opakované použití, samostatná odpovědnost, velikost nebo testování.
- Pro jednoduché záznamy používej přímé atributy. Properties/gettery/settery přidávej jen tehdy, přináší-li řízený přístup skutečné chování; nejsou bezpečnostním opatřením.
- Nezaváděj dědičnost, asynchronní kód, návrhové vzory ani metaprogramování pouze kvůli architektonické symetrii. Před velkým refaktoringem nejprve popiš problém, cílové hranice a rozhraní v ARCHITECTURE.md.


[↑ Obsah / Contents](#obsah)

<a id="cz-chyby-vedlejší-účinky-a-diagnostika"></a>

## Chyby, vedlejší účinky a diagnostika

Externí vstup validuj na vhodné hranici a při selhání uveď užitečný důvod. Nepotlačuj výjimky potichu, nezahazuj neúspěšné vstupy a neoznačuj částečně zpracovaný dokument za úspěšný ingest.

Odděl čisté transformace od přístupu k souborům/databázi, načítání modelů a zápisu historie. Významné vedlejší účinky vyjádři v názvech funkcí, rozhraních a provozních pokynech. Limity prostředků mají pokrývat relevantní hranice souboru, PDF stránky, dotazu, počtu výsledků a požadavku; ověř implementované limity, nepředpokládej existenci plánovaných kontrol.

Bezpečnostní validaci odděl od předzpracování textu: odmítnutí nebezpečného souboru nesmí potichu měnit význam platného dokumentu. Ve znovupoužitelných modulech preferuj logování; CLI může vypisovat uživatelské výstupy. Diagnostika má určit selhání bez vyzrazení tajných údajů či soukromého obsahu korpusu.


[↑ Obsah / Contents](#obsah)

<a id="cz-ověřování-a-regresní-testy"></a>

## Ověřování a regresní testy

Použij vrstvu ověření, která odpovídá skutečné otázce:

| Vrstva | Účel |
| --- | --- |
| Jednotkové testy | Deterministické chování modulů, validace a okrajové případy |
| Integrační testy | Chování přes hranice komponent |
| Smoke testy | Základní fungování aplikace v zamýšleném prostředí |
| Evaluace retrievalu | Kvalita podložená evidencí a latence retrievalu |

Pro jednotkové testy preferuj malé syntetické fixtures, falešné kolekce a výslovné chybové scénáře. Skutečná PDF/modely patří do vhodných integračních, ručních nebo evaluačních kontrol; úspěšné syntetické testy neprokazují kvalitu nad skutečným korpusem.

Pro ověřenou vadu přidej smysluplný regresní test. Kde je to praktické, ověř, že odhaluje původní selhání. Nikdy neoslabuj assertions ani validaci kvůli úspěšnému výsledku. Kromě běžného úspěšného průchodu testuj integritu dat a soulad rozhraní.

Při změně kódu spusť cílené testy a celou projektovou sadu před commitem. Z `rag_api_project/`:

```bash
python -m pytest tests -q
```

U změn pouze v dokumentaci ověř fakta, odkazy, příklady a dotčenou konfiguraci; nevymýšlej testy kopírující text. Přesně uveď spuštěné kontroly, přeskočení/varování a důležité kontroly, které provést nešlo. Z lokálního hlášení samotného nevyvozuj úspěch GitHub CI ani výsledky nad skutečným korpusem.


[↑ Obsah / Contents](#obsah)

<a id="cz-disciplína-retrievalu-a-evaluace"></a>

## Disciplína retrievalu a evaluace

[EVALUATION.md](EVALUATION.md#cz) určuje schéma, pravidla párování, CLI příkazy, schvalování/povýšení a požadavky na reprodukovatelnost. [EVAL_CURATOR_AGENT.md](EVAL_CURATOR_AGENT.md#cz) určuje omezení kurátorství kandidátů.

- Odděluj vývoj DEV, průzkum robustnosti RANDOM a závěrečný TEST. Neprohlížej opakovaně chyby TEST a pak pro ně neoptimalizuj.
- Před změnou řazení stanov baseline. Běhy DEV/RANDOM porovnávej při kontrolovaném korpusu, indexu, datasetu a konfiguraci; uchovej původ výsledků.
- Evidenci vytvoř ze zdrojových PDF před psaním otázek. Skóre průzkumu neprokazuje věcnou platnost, ani když stránkové a chunkové vyhledávání používají různé implementace BM25.
- Neměň existující golden evidence, metriky ani historii baseline za účelem zvýšení skóre. Validace kandidátů neopravňuje k povýšení.
- Rozlišuj naměřenou latenci `search()` od inicializace a ceny celé odpovědi/HTTP požadavku; uveď, kterou práci retrievalu či rerankingu měřená metoda zahrnuje. Neslučuj neslučitelná surová skóre relevance bez odůvodněné metody a naměřené evaluace.


[↑ Obsah / Contents](#obsah)

<a id="cz-git-revize-a-integrace"></a>

## Git, revize a integrace

Výchozí integrační větev je `main`. Novou práci připravuj na vhodné pracovní větvi; zachovej nesouvisející worktrees a necommitnuté změny. V rámci vedlejšího úklidu neresetuj, nestashuj, nepřepínej ani nestaguj cizí rozpracovanou práci.

Před stagingem zkontroluj `git status --short` a `git diff`. Přidej přesné zamýšlené cesty a pak zkontroluj seznam i obsah připravených souborů:

```bash
git diff --cached --stat
git diff --cached
git diff --cached --check
```

Nepoužívej automatické `git add .`. Soukromá PDF, lokální indexy, cache modelů, `.env` a další tajné údaje nepatří do commitů. Preferuj soudržné commity se zprávou popisující dokončené chování; kde je to praktické, odděl nesouvisející dokumentaci, závislosti a funkce.

Z `rag_api_project/` projektový pomocník spouští kontrolu bílých znaků ve staged změnách a projektovou testovací sadu:

```bash
python -m scripts.git_check
```

Neuděluje oprávnění ani nedokládá kontrolu tajných údajů, rozsahu, závislostí a kvality retrievalu. Před pushem znej stav pracovního stromu, zkontroluj zamýšlené změny a splň platná pravidla AGENTS a repozitáře. Commit, push a merge prováděj pouze v rozsahu výslovného oprávnění; neobcházej povinné revize ani pravidla CI.


[↑ Obsah / Contents](#obsah)

<a id="cz-bezpečnost-a-správa-závislostí"></a>

## Bezpečnost a správa závislostí

Bezpečnost platí v celém vývoji, nejen v plánované bezpečnostní fázi. Validuj externí vstupy, vynucuj vhodné hranice souborového systému/prostředků, zacházej uvážlivě s tajnými údaji a selhání uváděj výslovně.

Audit závislostí, Dependency Review, Gitleaks a Dependabot jsou již nakonfigurované. Jejich nálezy považuj za podněty k šetření; úspěšné Python testy neřeší zranitelnost závislosti. Nevypínej ani neoslabuj kontroly, aby změna vypadala zdravě.

Pinování verzí a přijetí lock souboru zůstávají samostatnou revidovanou prací na závislostech. Platformně specifický nebo lokálně vytvořený lock není automaticky přenositelný ani schválený. Před přijetím ověř konzistenci, podporovaný Python/OS, čistou instalaci, regrese a pravidla aktualizace.

Před doporučením či spuštěním `python -m scripts.ingest` vysvětli, že nakonfigurovanou Chroma kolekci **smaže a znovu vytvoří**. Dodrž zálohovací, konfigurační a schvalovací hranice v [OPERATIONS.md](OPERATIONS.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-spolupráce-a-učení"></a>

## Spolupráce a učení

Oprávnění určují globální a projektový AGENTS. Zvol režim odpovídající požadavku vlastníka; nevnucuj výukový postup každému implementačnímu úkolu:

- **LEARN:** vysvětli problém a chování, podpoř implementaci vlastníka, zkontroluj ji a získej praktický doklad porozumění.
- **IMPLEMENT:** dokonči delegovanou ohraničenou změnu, zachovej rozhraní/WIP, ověř ji a popiš výsledek i omezení.
- **REVIEW:** kontroluj a uváděj reprodukovatelné nálezy; soubory měň jen po schválení oprav vlastníkem.

V LEARN používej úplné logické celky s cílem, odůvodněním, novými relevantními pojmy, rozsahem a jasným ověřením. Velkým/rizikovým komponentám věnuj samostatnou cílenou revizi; vyhni se konverzačnímu postupu import po importu. Používej idiomatický Python bez umělého zjednodušování a nepotřebných pokročilých mechanismů.

Zaznamenávej významné milníky, obtíže, pomoc a testovací důkazy do [LEARNING_LOG.md](../../LEARNING_LOG.md#cz). Odděluj hotovou funkci od samostatně prokázané dovednosti. Bez požadovaných lidských důkazů/schválení neuděluj hodnocení zvládnutí ani neměň hodnocení učení.


[↑ Obsah / Contents](#obsah)

<a id="cz-dokončení-a-aktualizace-dokumentace"></a>

## Dokončení a aktualizace dokumentace

Znovupoužitelný modul je obvykle hotový, když má jasnou odpovědnost a rozhraní, funguje očekávané chování, validuje důležité vstupy, procházejí relevantní testy i projektové regrese a známá záměrná omezení jsou zdokumentovaná. Dokončení podfáze posuzuj podle konkrétních kritérií roadmapy. Neoznačuj ji za hotovou při zásadní nevyřešené chybě.

Při změně chování nebo schváleného rozhodnutí:

- Aktualizuj odpovědný dokument z tabulky.
- Odliš současnou implementaci od cílové architektury a lokální rozpracované práce.
- Synchronizuj české a anglické provozní/evaluační pokyny.
- Data, měření a původ práce ve větvích uváděj v učebních/evaluačních záznamech; odkazuj na ně místo kopírování proměnlivého stavu do všech dokumentů.
- Uveď změněné soubory, ověření, rozhodnutí a zbývající omezení.

Cíle nebo priority fáze se mění pouze schváleným rozhodnutím o roadmapě. Při úklidu dokumentace plán potichu nepřepracovávej.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
