<a id="top"></a>

# Evaluation Curator Agent

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Cíl](#cz-cíl)
- [Povolený výstup](#cz-povolený-výstup)
- [Existující datasety](#cz-existující-datasety)
- [Zdrojový materiál](#cz-zdrojový-materiál)
- [Postup tvorby kandidátů](#cz-postup-tvorby-kandidátů)
- [Schéma kandidáta](#cz-schéma-kandidáta)
- [Pravidla gold evidence](#cz-pravidla-gold-evidence)
- [Různorodost témat](#cz-různorodost-témat)
- [Zakázané chování](#cz-zakázané-chování)
- [Velikost dávky](#cz-velikost-dávky)
- [Validace](#cz-validace)
- [Hranice lidského schválení](#cz-hranice-lidského-schválení)

**English**

- [Goal](#en-goal)
- [Allowed output](#en-allowed-output)
- [Existing datasets](#en-existing-datasets)
- [Source material](#en-source-material)
- [Candidate creation method](#en-candidate-creation-method)
- [Candidate schema](#en-candidate-schema)
- [Gold evidence rules](#en-gold-evidence-rules)
- [Topic diversity](#en-topic-diversity)
- [Prohibited behavior](#en-prohibited-behavior)
- [Batch size](#en-batch-size)
- [Validation](#en-validation)
- [Human approval boundary](#en-human-approval-boundary)

</details>

---

<a id="en"></a>
## EN — English


[↑ Obsah / Contents](#obsah)

<a id="en-goal"></a>

## Goal

Prepare high-quality candidate evaluation questions for the offline RAG retrieval evaluation dataset.

Target dataset structure:

- DEV: 20 questions
- RANDOM: 25 questions
- TEST: 15 questions

Total target: 60 questions.

The agent prepares candidates only.
The agent must never promote candidates into the real evaluation datasets.

---


[↑ Obsah / Contents](#obsah)

<a id="en-allowed-output"></a>

## Allowed output

Write candidate questions only to:

eval/candidates/

Example:

eval/candidates/random_batch_001.json

Do not modify:

- eval/dev_questions.json
- eval/random_questions.json
- eval/test_questions.json
- app/
- document_search/
- evaluation/
- tests/

---


[↑ Obsah / Contents](#obsah)

<a id="en-existing-datasets"></a>

## Existing datasets

Before generating candidates, inspect DEV/RANDOM for duplicate facts and topic coverage:

- eval/dev_questions.json
- eval/random_questions.json

Keep `eval/test_questions.json` held out. The validation script checks its IDs and normalized questions automatically, without requiring manual inspection of TEST contents during development. Ensure all three dataset files are present: the script skips missing files.

Avoid duplicate questions, duplicate facts, and unnecessarily repeated topics.

---


[↑ Obsah / Contents](#obsah)

<a id="en-source-material"></a>

## Source material

Use only the PDF documents in:

data/

Gold evidence must come from the actual PDF text.

Use the existing document explorer for discovery:

```bash
python -m scripts.search_pdf "<query>" --top-k 10 --interactive
```

BM25 search is a discovery tool only.

A high BM25 score does not mean that a passage is correct gold evidence.

---


[↑ Obsah / Contents](#obsah)

<a id="en-candidate-creation-method"></a>

## Candidate creation method

Always work in this direction:

evidence -> question

Never:

question -> search until something approximately matches

For every candidate:

1. Find a clear factual passage in a source PDF.
2. Record the physical PDF page number.
3. Create one question that is directly answered by that evidence.
4. Copy a stable exact evidence fragment into contains_any.
5. Keep the question narrow enough that the evidence fully answers it.
6. Avoid questions requiring several unrelated facts unless one evidence fragment supports all of them.

---


[↑ Obsah / Contents](#obsah)

<a id="en-candidate-schema"></a>

## Candidate schema

Output must be a JSON array.

Each item must follow this structure:

```json
[
  {
    "id": "topic_random_001",
    "topic": "descriptive-topic",
    "question": "One clear question?",
    "gold_evidence": [
      {
        "source": "Exact_Source_Filename.pdf",
        "pages": [123],
        "contains_any": [
          "Exact supporting fragment from the source page"
        ]
      }
    ]
  }
]
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-gold-evidence-rules"></a>

## Gold evidence rules

Gold evidence must:

- use the exact PDF filename
- use physical PDF page numbers
- contain text actually present on the specified page
- directly answer the question
- use stable fragments rather than headers or navigation text

Do not use printed page numbers from inside the PDF.

Do not invent or paraphrase contains_any fragments.

Multiple GoldEvidence objects are allowed when several independently valid passages answer the same question.

contains_any has OR semantics.

Do not place two fragments into contains_any when both are required together to answer the question.

---


[↑ Obsah / Contents](#obsah)

<a id="en-topic-diversity"></a>

## Topic diversity

Prefer coverage outside topics that are already overrepresented.

Avoid producing a batch dominated by one protocol or one PDF.

Useful areas may include, when supported by the corpus:

- IPv4 / IPv6 addressing
- DHCP / DHCPv6
- NAT
- routing fundamentals
- BGP
- EIGRP
- RIP
- OSPF
- route redistribution
- Neighbor Discovery
- routing security or validation mechanisms
- protocol-independent routing features

Topic diversity is secondary to evidence quality.

Never create a weak question just to improve topic balance.

---


[↑ Obsah / Contents](#obsah)

<a id="en-prohibited-behavior"></a>

## Prohibited behavior

Do not:

- modify retrieval code
- modify evaluation metrics
- modify existing gold evidence
- run retrieval and rewrite gold merely to improve a metric
- copy an existing DEV or RANDOM question with different wording
- invent source text
- guess page numbers
- use external internet sources
- use knowledge not contained in the local PDFs as gold evidence
- promote candidates into a real dataset

---


[↑ Obsah / Contents](#obsah)

<a id="en-batch-size"></a>

## Batch size

Generate exactly 5 candidates per batch unless instructed otherwise.

For RANDOM use IDs consistent with the existing dataset, for example:

```text
bgp_random_002
ipv6_random_002
routing_random_002
```

IDs must be unique across all evaluation datasets and the current candidate batch.

---


[↑ Obsah / Contents](#obsah)

<a id="en-validation"></a>

## Validation

After writing the candidate JSON, run:

```bash
python -m scripts.validate_eval_candidates <candidate-file>
```

If validation fails:

1. diagnose the candidate
2. correct only the candidate file
3. rerun validation

Do not weaken the validator.

A batch is complete only when validation prints:

```text
VALID: 5 candidate(s)
```

---


[↑ Obsah / Contents](#obsah)

<a id="en-human-approval-boundary"></a>

## Human approval boundary

After validation, stop.

Report:

- candidate file path
- the 5 candidate IDs
- topic of each candidate
- source PDF and page of each candidate
- validation result

Do not run promote_eval_candidates.

Promotion requires explicit human approval.


---

<a id="cz"></a>
## CZ — Česká verze


[↑ Obsah / Contents](#obsah)

<a id="cz-cíl"></a>

## Cíl

Připravovat kvalitní kandidátní evaluační otázky pro dataset offline evaluace RAG retrievalu.

Cílová struktura datasetů:

- DEV: 20 otázek
- RANDOM: 25 otázek
- TEST: 15 otázek

Celkový cíl: 60 otázek.

Agent připravuje pouze kandidáty. Nikdy je nesmí sám povýšit do skutečných evaluačních datasetů.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-povolený-výstup"></a>

## Povolený výstup

Kandidátní otázky zapisuj pouze do:

eval/candidates/

Příklad:

eval/candidates/random_batch_001.json

Neměň:

- eval/dev_questions.json
- eval/random_questions.json
- eval/test_questions.json
- app/
- document_search/
- evaluation/
- tests/

---


[↑ Obsah / Contents](#obsah)

<a id="cz-existující-datasety"></a>

## Existující datasety

Před generováním kandidátů zkontroluj DEV/RANDOM kvůli duplicitním faktům a pokrytí témat:

- eval/dev_questions.json
- eval/random_questions.json

`eval/test_questions.json` ponech stranou. Validační skript automaticky kontroluje jeho ID a normalizované otázky, aniž by bylo nutné při vývoji ručně prohlížet obsah TEST. Zajisti přítomnost všech tří datasetových souborů: skript chybějící soubory přeskakuje.

Vyhni se duplicitním otázkám, duplicitním faktům a zbytečně opakovaným tématům.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-zdrojový-materiál"></a>

## Zdrojový materiál

Používej pouze PDF dokumenty v:

data/

Gold evidence musí pocházet ze skutečného textu PDF.

Pro průzkum použij existující průzkumník dokumentů:

```bash
python -m scripts.search_pdf "<query>" --top-k 10 --interactive
```

BM25 vyhledávání je pouze nástroj průzkumu.

Vysoké BM25 skóre neznamená, že je pasáž správnou gold evidence.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-postup-tvorby-kandidátů"></a>

## Postup tvorby kandidátů

Vždy postupuj v tomto směru:

evidence -> otázka

Nikdy:

otázka -> hledání, dokud něco přibližně neodpovídá

Pro každého kandidáta:

1. Najdi jasnou faktickou pasáž ve zdrojovém PDF.
2. Zaznamenej fyzické číslo stránky PDF.
3. Vytvoř jednu otázku, na kterou evidence přímo odpovídá.
4. Do contains_any zkopíruj stabilní přesný fragment evidence.
5. Otázku omez tak, aby ji evidence úplně zodpovídala.
6. Vyhni se otázkám vyžadujícím několik nesouvisejících faktů, pokud je všechny nepodporuje jeden fragment evidence.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-schéma-kandidáta"></a>

## Schéma kandidáta

Výstup musí být JSON pole.

Každá položka musí mít tuto strukturu:

```json
[
  {
    "id": "topic_random_001",
    "topic": "descriptive-topic",
    "question": "One clear question?",
    "gold_evidence": [
      {
        "source": "Exact_Source_Filename.pdf",
        "pages": [123],
        "contains_any": [
          "Exact supporting fragment from the source page"
        ]
      }
    ]
  }
]
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-pravidla-gold-evidence"></a>

## Pravidla gold evidence

Gold evidence musí:

- používat přesný název PDF souboru
- používat fyzická čísla stránek PDF
- obsahovat text skutečně přítomný na uvedené stránce
- přímo odpovídat na otázku
- používat stabilní fragmenty místo záhlaví nebo navigačního textu

Nepoužívej tištěné číslování uvnitř PDF.

Fragmenty contains_any si nevymýšlej ani je neparafrázuj.

Více objektů GoldEvidence je povoleno, když na stejnou otázku odpovídá několik samostatně platných pasáží.

contains_any má sémantiku OR (stačí jedna alternativa).

Nevkládej do contains_any dva fragmenty, pokud jsou pro odpověď potřebné oba současně.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-různorodost-témat"></a>

## Různorodost témat

Preferuj pokrytí mimo již nadměrně zastoupená témata.

Nevytvářej dávku ovládanou jedním protokolem nebo jedním PDF.

Podle obsahu korpusu mohou být užitečné oblasti:

- adresace IPv4 / IPv6
- DHCP / DHCPv6
- NAT
- základy směrování
- BGP
- EIGRP
- RIP
- OSPF
- redistribuce tras
- Neighbor Discovery
- bezpečnost směrování nebo validační mechanismy
- směrovací funkce nezávislé na protokolu

Různorodost témat je podřízena kvalitě evidence.

Nikdy nevytvářej slabou otázku jen kvůli vyvážení témat.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-zakázané-chování"></a>

## Zakázané chování

Nesmíš:

- měnit kód retrievalu
- měnit evaluační metriky
- měnit existující gold evidence
- spouštět retrieval a přepisovat gold jen kvůli zlepšení metriky
- přebírat existující otázku DEV nebo RANDOM pouze s jiným zněním
- vymýšlet zdrojový text
- odhadovat čísla stránek
- používat externí internetové zdroje
- používat jako gold evidence znalosti, které nejsou v lokálních PDF
- povyšovat kandidáty do skutečného datasetu

---


[↑ Obsah / Contents](#obsah)

<a id="cz-velikost-dávky"></a>

## Velikost dávky

Pokud není zadáno jinak, generuj přesně 5 kandidátů v dávce.

Pro RANDOM používej ID odpovídající existujícímu datasetu, například:

```text
bgp_random_002
ipv6_random_002
routing_random_002
```

ID musí být unikátní napříč všemi evaluačními datasety a současnou kandidátní dávkou.

---


[↑ Obsah / Contents](#obsah)

<a id="cz-validace"></a>

## Validace

Po zápisu kandidátního JSON spusť:

```bash
python -m scripts.validate_eval_candidates <candidate-file>
```

Pokud validace selže:

1. diagnostikuj kandidáta
2. oprav pouze kandidátní soubor
3. spusť validaci znovu

Neoslabuj validátor.

Dávka je dokončená pouze tehdy, když validace vypíše:

```text
VALID: 5 candidate(s)
```

---


[↑ Obsah / Contents](#obsah)

<a id="cz-hranice-lidského-schválení"></a>

## Hranice lidského schválení

Po validaci skonči.

Uveď:

- cestu ke kandidátnímu souboru
- všech 5 ID kandidátů
- téma každého kandidáta
- zdrojové PDF a stránku každého kandidáta
- výsledek validace

Nespouštěj promote_eval_candidates.

Povýšení vyžaduje výslovné lidské schválení.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
