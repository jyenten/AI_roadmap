<a id="top"></a>

# AI Engineering — Learning Log

[Česky](#cz) · [English](#en) · [Obsah / Contents](#obsah)

<a id="obsah"></a>

<details>
<summary>Obsah / Contents — kliknutím rozbalit / click to expand</summary>

**Česky**

- [Cíl](#cz-cíl)
- [Úrovně dovedností](#cz-úrovně-dovedností)
- [Ověřený stav projektu](#cz-ověřený-stav-projektu)
- [Historický stav projektu — 2026-10-12](#cz-historický-stav-projektu--2026-10-12)
- [Historický učební plán: fáze 3.3 — BM25 (2026-10-12)](#cz-historický-učební-plán-fáze-33--bm25-2026-10-12)
- [Šablona záznamu učení](#cz-šablona-záznamu-učení)
- [YYYY-MM-DD — téma](#cz-yyyy-mm-dd--téma)
- [Pravidla záznamů učení](#cz-pravidla-záznamů-učení)
- [Historie projektu a učení](#cz-historie-projektu-a-učení)
- [2026-05-12 až 2026-05-22 — Python, analýza dat a klasické ML](#cz-2026-05-12-až-2026-05-22--python-analýza-dat-a-klasické-ml)
- [2026-05-23 až 2026-06-09 — PyTorch, NLP, počáteční RAG a kontejnery](#cz-2026-05-23-až-2026-06-09--pytorch-nlp-počáteční-rag-a-kontejnery)
- [2026-07-27 až 2026-08-21 — Základ RAG API, diagnostika a CI](#cz-2026-07-27-až-2026-08-21--základ-rag-api-diagnostika-a-ci)
- [2026-09-01 až 2026-09-16 — Diagnostika retrievalu a základ evaluace](#cz-2026-09-01-až-2026-09-16--diagnostika-retrievalu-a-základ-evaluace)
- [2026-09-16 až 2026-09-17 — Nezávislý průzkumník PDF stránek](#cz-2026-09-16-až-2026-09-17--nezávislý-průzkumník-pdf-stránek)
- [2026-09-22 až 2026-10-08 — Párování evidence a řízená evaluace](#cz-2026-09-22-až-2026-10-08--párování-evidence-a-řízená-evaluace)
- [2026-10-11 až 2026-10-12 — Vektorový baseline, latence a pravidla agentů](#cz-2026-10-11-až-2026-10-12--vektorový-baseline-latence-a-pravidla-agentů)
- [2026-10-13 — Fáze 3.3: BM25 Retriever](#cz-2026-10-13--fáze-33-bm25-retriever)
- [2026-10-14 — Historie portfolia, původ práce agentů a bezpečnostní automatizace](#cz-2026-10-14--historie-portfolia-původ-práce-agentů-a-bezpečnostní-automatizace)
- [2026-10-15 až 2026-10-17 — Návrh reprodukovatelných Linux závislostí](#cz-2026-10-15-až-2026-10-17--návrh-reprodukovatelných-linux-závislostí)
- [2026-10-20 — Fáze 3.4: Evaluace retrievalu](#cz-2026-10-20--fáze-34-evaluace-retrievalu)
- [2026-10-26 — Experiment úložiště dokumentů a ověřeného FAISS balíčku](#cz-2026-10-26--experiment-úložiště-dokumentů-a-ověřeného-faiss-balíčku)
- [2026-10-26 — Automatizovaný návrh závislosti GitHub Actions](#cz-2026-10-26--automatizovaný-návrh-závislosti-github-actions)
- [2026-10-28 — Dvojjazyčné návody, regrese validátoru a výchozí main](#cz-2026-10-28--dvojjazyčné-návody-regrese-validátoru-a-výchozí-main)
- [2026-10-28 — Odpovědnosti dokumentace a česká navigace](#cz-2026-10-28--odpovědnosti-dokumentace-a-česká-navigace)
- [Necommitnutá práce pozorovaná 28. 10. 2026](#cz-necommitnutá-práce-pozorovaná-28-10-2026)
- [Pokrytí auditu větví — 2026-10-28](#cz-pokrytí-auditu-větví--2026-10-28)

**English**

- [Goal](#en-goal)
- [Skill levels](#en-skill-levels)
- [Current project checkpoint](#en-current-project-checkpoint)
- [Historical project checkpoint — 2026-10-12](#en-historical-project-checkpoint--2026-10-12)
- [Historical learning plan: Phase 3.3 — BM25 (2026-10-12)](#en-historical-learning-plan-phase-33--bm25-2026-10-12)
- [Learning entry template](#en-learning-entry-template)
- [YYYY-MM-DD — Topic](#en-yyyy-mm-dd--topic)
- [Learning rules](#en-learning-rules)
- [Project and learning history](#en-project-and-learning-history)
- [2026-05-12 to 2026-05-22 — Python, data analysis and classical ML](#en-2026-05-12-to-2026-05-22--python-data-analysis-and-classical-ml)
- [2026-05-23 to 2026-06-09 — PyTorch, NLP, initial RAG and containers](#en-2026-05-23-to-2026-06-09--pytorch-nlp-initial-rag-and-containers)
- [2026-07-27 to 2026-08-21 — RAG API foundation, diagnostics and CI](#en-2026-07-27-to-2026-08-21--rag-api-foundation-diagnostics-and-ci)
- [2026-09-01 to 2026-09-16 — Retrieval diagnostics and evaluation foundation](#en-2026-09-01-to-2026-09-16--retrieval-diagnostics-and-evaluation-foundation)
- [2026-09-16 to 2026-09-17 — Independent PDF page explorer](#en-2026-09-16-to-2026-09-17--independent-pdf-page-explorer)
- [2026-09-22 to 2026-10-08 — Evidence matching and governed evaluation](#en-2026-09-22-to-2026-10-08--evidence-matching-and-governed-evaluation)
- [2026-10-11 to 2026-10-12 — Vector baseline, latency and agent rules](#en-2026-10-11-to-2026-10-12--vector-baseline-latency-and-agent-rules)
- [2026-10-13 — Phase 3.3: BM25 Retriever](#en-2026-10-13--phase-33-bm25-retriever)
- [2026-10-14 — Portfolio history, agent provenance and security automation](#en-2026-10-14--portfolio-history-agent-provenance-and-security-automation)
- [2026-10-15 to 2026-10-17 — Linux dependency reproducibility proposal](#en-2026-10-15-to-2026-10-17--linux-dependency-reproducibility-proposal)
- [2026-10-20 — Phase 3.4: Retrieval Evaluation](#en-2026-10-20--phase-34-retrieval-evaluation)
- [2026-10-26 — Document store and verified FAISS bundle experiment](#en-2026-10-26--document-store-and-verified-faiss-bundle-experiment)
- [2026-10-26 — Automated GitHub Actions dependency proposal](#en-2026-10-26--automated-github-actions-dependency-proposal)
- [2026-10-28 — Bilingual runbooks, validator regressions and default main](#en-2026-10-28--bilingual-runbooks-validator-regressions-and-default-main)
- [2026-10-28 — Documentation responsibilities and Czech navigation](#en-2026-10-28--documentation-responsibilities-and-czech-navigation)
- [Uncommitted work observed on 2026-10-28](#en-uncommitted-work-observed-on-2026-10-28)
- [Branch audit coverage — 2026-10-28](#en-branch-audit-coverage--2026-10-28)

</details>

---

<a id="en"></a>
## EN — English


[↑ Obsah / Contents](#obsah)

<a id="en-goal"></a>

## Goal

Develop independent proficiency in:

- Python programming
- Software architecture and testing
- Git, CI/CD and Docker
- RAG systems and information retrieval
- AI evaluation and observability
- AI agents and agent-assisted development


[↑ Obsah / Contents](#obsah)

<a id="en-skill-levels"></a>

## Skill levels

- NOT ASSESSED — no independent demonstration yet
- GUIDED — completed with explanations or assistance
- INDEPENDENT — implemented and explained without assistance
- PROFICIENT — independently applied in a different problem

A completed project feature does not automatically
mean the corresponding skill is mastered.


[↑ Obsah / Contents](#obsah)

<a id="en-current-project-checkpoint"></a>

## Current project checkpoint

Date: 2026-10-28
Default branch: main
Reviewed project commit: bfb1d85 (before this log update)

- PR #3 is merged: bilingual runbooks, evidence-validator fixes and regressions.
- Latest verified GitHub CI on `main`: **223 passed in 4.99s**
  ([run 40744368854](https://github.com/jyenten/AI_roadmap/actions/runs/40744368854)).
- Gitleaks and CodeQL passed on that revision. Dependency Audit remains failing
  with open ChromaDB findings; it has not been disabled or given an exception.
- BM25 and Vector DEV/RANDOM baselines are preserved. They were not rerun for
  this log update; held-out TEST remains unchanged.
- Hybrid RRF and retriever-ID interface work remain local and uncommitted.
- The Linux dependency-lock proposal (PR #1), Dependabot proposal (PR #2) and
  local FAISS/storage experiment are separate from the integrated `main` state.

Project completion and human skill assessment remain separate. The existing
GUIDED assessments below are preserved; this history review assigns no new
INDEPENDENT or PROFICIENT rating.


[↑ Obsah / Contents](#obsah)

<a id="en-historical-project-checkpoint--2026-10-12"></a>

## Historical project checkpoint — 2026-10-12

Date: 2026-10-12
Branch: document-search-bm25
Commit: 9ed9985

Completed in the project:

- FastAPI RAG foundation
- PDF processing and Chroma vector storage
- Vector retrieval baseline
- Evaluation datasets and retrieval metrics
- DEV / RANDOM / held-out TEST separation
- Retrieval latency measurement
- JSONL evaluation history
- Git provenance checks
- Automated testing and GitHub CI

Last verified full test suite:
142 passed, 1 skipped.

These are project achievements, not independent
skill assessments.


[↑ Obsah / Contents](#obsah)

<a id="en-historical-learning-plan-phase-33--bm25-2026-10-12"></a>

## Historical learning plan: Phase 3.3 — BM25 (2026-10-12)

Topic:
Lexical retrieval over existing Chroma chunks.

Learning objectives:

- Explain how BM25 ranks documents.
- Understand tokenization, TF, IDF and document length.
- Implement retrieval ranking in Python.
- Preserve source and page metadata.
- Write meaningful unit and integration tests.
- Compare BM25 with vector retrieval.

Independent exercise:

Implement BM25Retriever.search() and explain the
ranking and tie-breaking behavior.

Current skill assessment:
NOT ASSESSED


[↑ Obsah / Contents](#obsah)

<a id="en-learning-entry-template"></a>

## Learning entry template


[↑ Obsah / Contents](#obsah)

<a id="en-yyyy-mm-dd--topic"></a>

### YYYY-MM-DD — Topic

What I worked on:

- To be filled in.

Concepts I learned:

- To be filled in.

What I implemented independently:

- To be filled in.

What Codex or ChatGPT implemented:

- To be filled in.

Problems I diagnosed:

- To be filled in.

Tests and evidence:

- To be filled in.

Skill level:
NOT ASSESSED / GUIDED / INDEPENDENT / PROFICIENT

Next exercise:

- To be filled in.


[↑ Obsah / Contents](#obsah)

<a id="en-learning-rules"></a>

## Learning rules

Update this log after meaningful milestones,
not after every small code change.

Record difficulties and misunderstandings.
Do not inflate skill assessments.
Revisit weak topics through independent exercises.


[↑ Obsah / Contents](#obsah)

<a id="en-project-and-learning-history"></a>

## Project and learning history

The retrospective entries added on 2026-10-28 are reconstructed from commit
history, selected source/test changes, PR state and local worktree status.
Dates describe recorded commits, not verified study time. Concepts listed are
present in the work; Git authorship alone does not prove independent human
implementation, understanding or the extent of AI assistance. Attribution is
stated only where the existing log or observed collaboration establishes it.
Historical scripts and experimental tests were not rerun during this log audit.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-05-12-to-2026-05-22--python-data-analysis-and-classical-ml"></a>

### 2026-05-12 to 2026-05-22 — Python, data analysis and classical ML

**Project evidence:** Exercises originally recorded on the history now retained
by `master`, subsequently inherited by `main` and moved under `archive/`.

- Python input, conditions, loops, functions and collections; later Pandas CSV
  analysis, filtering/grouping, missing values and Matplotlib plots.
- Linear regression, classification, cross-validation/overfitting,
  RandomForest, feature engineering and a complete ML exercise.
- Concepts to consolidate: train/test separation, reproducible splits,
  preprocessing and interpreting metrics rather than only fitting a model.
- Evidence: [initial days 1–4, 8daf3fa](https://github.com/jyenten/AI_roadmap/commit/8daf3fa),
  [Pandas, 909b475](https://github.com/jyenten/AI_roadmap/commit/909b475),
  [complete ML exercise, 1c852a6](https://github.com/jyenten/AI_roadmap/commit/1c852a6).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-05-23-to-2026-06-09--pytorch-nlp-initial-rag-and-containers"></a>

### 2026-05-23 to 2026-06-09 — PyTorch, NLP, initial RAG and containers

**Project evidence:** Archived learning exercises, already included in `main`.

- PyTorch networks, CNN/image classification, transfer learning and ResNet18.
- NLP sentiment classification, embeddings, BERT/tokenizers, attention and
  Hugging Face pipeline/QA experiments.
- Initial RAG experiments followed by FastAPI and Docker application exercises.
- Concepts to consolidate: tensor/model interfaces, tokenization, retrieval
  versus generation, package compatibility and container runtime boundaries.
- Evidence: [PyTorch, 1c05b12](https://github.com/jyenten/AI_roadmap/commit/1c05b12),
  [BERT, 4097483](https://github.com/jyenten/AI_roadmap/commit/4097483),
  [Hugging Face QA, 1441c8a](https://github.com/jyenten/AI_roadmap/commit/1441c8a),
  [Docker/RAG API, f57517e](https://github.com/jyenten/AI_roadmap/commit/f57517e).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-07-27-to-2026-08-21--rag-api-foundation-diagnostics-and-ci"></a>

### 2026-07-27 to 2026-08-21 — RAG API foundation, diagnostics and CI

**Project milestone:** Historical `master` foundation; included in `main`.

- Improved PDF cleaning/chunking, retrieved context and alignment of sources
  with selected context; added source metadata to API responses.
- Added health/stats/readiness endpoints, blank-question validation and handling
  for unavailable RAG services; added Docker and Compose setup.
- Added API checks, a test Chroma setup, smoke tests and GitHub Actions CI.
- Concepts covered: service readiness versus liveness, traceable responses,
  typed API boundaries, test isolation and repeatable development checks.
- Evidence: [source metadata, 581d6f6](https://github.com/jyenten/AI_roadmap/commit/581d6f6),
  [readiness, 6950495](https://github.com/jyenten/AI_roadmap/commit/6950495),
  [CI/smoke tests, 702c0ab](https://github.com/jyenten/AI_roadmap/commit/702c0ab),
  [`master` tip, 3c0bfdd](https://github.com/jyenten/AI_roadmap/commit/3c0bfdd).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-09-01-to-2026-09-16--retrieval-diagnostics-and-evaluation-foundation"></a>

### 2026-09-01 to 2026-09-16 — Retrieval diagnostics and evaluation foundation

**Project milestone:** Included in `main`; `retrieval-eval-refactor` retains an
early checkpoint of this development, not the final evaluation implementation.

- Added retrieval diagnostics, revised preprocessing/chunking with regression
  tests, initial DEV retrieval evaluation and evaluation-history tooling.
- Recorded architecture, roadmap and development rules.
- Concepts covered: diagnosing retrieval separately from generation, chunk
  boundaries/overlap, evidence-based evaluation and bounded development scope.
- Evidence: [chunking regressions, 26b39e6](https://github.com/jyenten/AI_roadmap/commit/26b39e6),
  [initial evaluation, 2fafcae](https://github.com/jyenten/AI_roadmap/commit/2fafcae),
  [`retrieval-eval-refactor` tip, 010d8d1](https://github.com/jyenten/AI_roadmap/commit/010d8d1).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-09-16-to-2026-09-17--independent-pdf-page-explorer"></a>

### 2026-09-16 to 2026-09-17 — Independent PDF page explorer

**Project milestone:** Implemented and included in `main`.

- Added page/search data models, normalization/tokenization, PDF loading,
  path/PDF/input validation, BM25 indexing/search and an interactive CLI.
- Added synthetic tests, development checks and automatic test watching.
- Concepts covered: immutable models, source/page identity, resource limits,
  lexical ranking and keeping page-level discovery separate from chunk retrieval.
- Evidence: [safe PDF loading, f05e080](https://github.com/jyenten/AI_roadmap/commit/f05e080),
  [BM25 search, 4a0fa06](https://github.com/jyenten/AI_roadmap/commit/4a0fa06),
  [page-explorer CLI, 1f3fad5](https://github.com/jyenten/AI_roadmap/commit/1f3fad5).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-09-22-to-2026-10-08--evidence-matching-and-governed-evaluation"></a>

### 2026-09-22 to 2026-10-08 — Evidence matching and governed evaluation

**Project milestone:** Implemented and included in `main`.

- Split evaluation into models, dataset loading, evidence matching, metrics,
  runner and JSONL history; added reproducible random sampling.
- Added DEV/RANDOM/held-out TEST separation, candidate validation/promotion
  tools, curator rules, CODEOWNERS and evaluation-governance CI.
- Concepts covered: physical PDF page numbers, normalized literal fragments,
  MRR/Hit@K, random seeds, dataset leakage and human approval boundaries.
- Evidence: [dataset models, f0b30b8](https://github.com/jyenten/AI_roadmap/commit/f0b30b8),
  [evidence matching, 8e93ce5](https://github.com/jyenten/AI_roadmap/commit/8e93ce5),
  [runner/metrics, ed6bf73](https://github.com/jyenten/AI_roadmap/commit/ed6bf73),
  [random sampling, 3247ab4](https://github.com/jyenten/AI_roadmap/commit/3247ab4),
  [governance, 8aae380](https://github.com/jyenten/AI_roadmap/commit/8aae380).
- Later review identified defects in the older `scripts.evaluate_random`;
  historical implementation does not mean every legacy CLI is currently sound.
  The supported comparison procedure is documented in
  [EVALUATION.md](rag_api_project/docs/EVALUATION.md).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-11-to-2026-10-12--vector-baseline-latency-and-agent-rules"></a>

### 2026-10-11 to 2026-10-12 — Vector baseline, latency and agent rules

**Project milestone:** Implemented and included in `main`.

- Added a standalone VectorRetriever baseline, retriever selection in evaluation,
  retrieval-only latency mean/p50/p95 and stricter run/history validation.
- Added tests for CLI selection, latency, models/history and Git provenance.
- Added repository-level LEARN/IMPLEMENT/REVIEW rules and this learning log.
- Concepts covered: stable retriever interfaces, measurement boundaries,
  reproducible run metadata and separating project completion from skill mastery.
- Evidence: [vector/observability, 9ed9985](https://github.com/jyenten/AI_roadmap/commit/9ed9985),
  [agent rules/log, 50797d4](https://github.com/jyenten/AI_roadmap/commit/50797d4).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-13--phase-33-bm25-retriever"></a>

### 2026-10-13 — Phase 3.3: BM25 Retriever

**Project milestone:** Completed

- Implemented `BM25Retriever` over existing Chroma chunks with guided learning.
- Implemented corpus loading, validation, tokenization, lexical matching, ranking and top-k selection.
- Codex independently prepared regression tests.
- Tests passed code review and were integrated.
- Full regression: 210 passed, 1 skipped, 2 warnings.
- Commit: `c101680` (pushed to origin/document-search-bm25).

**Learning evidence:**

- Practiced Python collections, list comprehensions, `enumerate()`, `sorted()`, `lambda` and data validation.
- Practiced distinguishing document indices from relevance scores.
- Understood the purpose of deterministic tie-breaking and lexical filtering.
- Required guidance and corrections during implementation.

**Skill assessment:** GUIDED

**Next independent exercise:** Explain and modify retrieval ranking without step-by-step assistance.

**Next project milestone:** BM25 vs. Vector evaluation on DEV, followed by RANDOM.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-14--portfolio-history-agent-provenance-and-security-automation"></a>

### 2026-10-14 — Portfolio history, agent provenance and security automation

**Project milestone:** Included in `main`.

- Moved earlier exercises under `archive/` without rewriting their contents;
  refreshed portfolio/project READMEs and disclosed AI-assisted development.
- Documented nested agent rules, the local BM25-test worktree and manually
  synchronized private-mirror workflow. The existing BM25 entry attributes
  regression-test preparation to Codex; no broader independent authorship is inferred.
- Added Gitleaks, Dependabot, Dependency Review and scheduled/PR dependency audit.
- Concepts covered: exact staging, preserving learning evidence, isolated agent
  work, secret scanning and distinguishing a passing test suite from dependency safety.
- Evidence: [archive move, d157023](https://github.com/jyenten/AI_roadmap/commit/d157023),
  [agent provenance, 646525d](https://github.com/jyenten/AI_roadmap/commit/646525d),
  [secret scanning, b032e9a](https://github.com/jyenten/AI_roadmap/commit/b032e9a),
  [dependency audit, 6a20b25](https://github.com/jyenten/AI_roadmap/commit/6a20b25).


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-15-to-2026-10-17--linux-dependency-reproducibility-proposal"></a>

### 2026-10-15 to 2026-10-17 — Linux dependency reproducibility proposal

**Project milestone:** Implemented on `chore/linux-lock-ci`, **not merged** into
`main`; [PR #1](https://github.com/jyenten/AI_roadmap/pull/1) remains open.

- Added a Linux/Python 3.11 dependency snapshot, clean Ubuntu installation
  verification, direct-dependency/lock consistency checks and CI lock installation.
- Added a separate ChromaDB risk-assessment document on that branch.
- Concepts covered: direct versus transitive dependencies, OS-specific locks,
  `pip check`, clean-environment validation and security risk tracking.
- Evidence: [snapshot workflow, 4b26db1](https://github.com/jyenten/AI_roadmap/commit/4b26db1),
  [lock checker, 8e2e7ec](https://github.com/jyenten/AI_roadmap/commit/8e2e7ec),
  [branch tip, a258e85](https://github.com/jyenten/AI_roadmap/commit/a258e85).
- [Historical PR CI](https://github.com/jyenten/AI_roadmap/actions/runs/39022965393)
  passed at that tip, while dependency-security checks failed. This is not
  approval of those dependency versions or proof that `main` uses the lock.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-20--phase-34-retrieval-evaluation"></a>

### 2026-10-20 — Phase 3.4: Retrieval Evaluation

**Project milestone:** Completed

- Integrated BM25 into the evaluation CLI using a retriever registry.
- Extended parametrized CLI tests for legacy, vector and BM25.
- Full regression suite passed.
- Evaluated BM25 and Vector on DEV (20 questions)
  and RANDOM (25 questions).
- Preserved the held-out TEST dataset.

**Baseline MRR:**

- DEV: BM25 0.7171, Vector 0.8321
- RANDOM: BM25 0.8133, Vector 0.6050

**Learning evidence:**

- Practiced dictionary lookup and registry pattern.
- Practiced exception chaining with `raise ... from exc`.
- Practiced `getattr()`, parametrized pytest tests
  and debugging `KeyError` and `ImportError`.
- Required guidance during implementation.

**Skill assessment:** GUIDED

**Next project milestone:** Hybrid retrieval using RRF.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-26--document-store-and-verified-faiss-bundle-experiment"></a>

### 2026-10-26 — Document store and verified FAISS bundle experiment

**Project milestone:** Committed only on local `experiment/vector-backend` at
`14159ce`; **not present in the public `main` branch**.

- Added `DocumentStore` with JSON loading, ID/text/source/page validation and
  duplicate-ID rejection.
- Added FAISS/index-record count checks and a verified-bundle loader that checks
  SHA-256 values against a manifest before loading the bundle.
- Added committed storage regression tests for valid/invalid records, bundles
  and checksums. Their presence was inspected; this audit did not execute them
  or establish a passing test count.
- Concepts covered: stable document IDs, separating vector index and metadata,
  integrity versus authenticity, validation before loading and regression tests.
- The branch descends from the **unmerged Linux-lock proposal**, so it cannot be
  treated as an isolated, reviewed change already integrated into `main`.
- An additional FAISS-retriever test is untracked in its worktree. A completed
  FAISS retriever or Chroma replacement is not established by this storage commit.
- Human/AI implementation split and independent explanation were not established
  from the available evidence; no new skill rating is assigned.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-26--automated-github-actions-dependency-proposal"></a>

### 2026-10-26 — Automated GitHub Actions dependency proposal

**Project milestone:** Bot-authored proposal, **not merged**.

- `dependabot/github_actions/actions/setup-python-7.1.0` at `21a5733` proposes
  `actions/setup-python` 7.0.0 → 7.1.0 in three workflows.
- [PR #2](https://github.com/jyenten/AI_roadmap/pull/2) is open. Its historical
  [CI run](https://github.com/jyenten/AI_roadmap/actions/runs/40291737972) passed;
  not all security/governance checks passed.
- This records automation activity and a review opportunity, not human
  implementation or a demonstrated new skill.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-28--bilingual-runbooks-validator-regressions-and-default-main"></a>

### 2026-10-28 — Bilingual runbooks, validator regressions and default main

**Project milestone:** Completed and integrated through
[PR #3](https://github.com/jyenten/AI_roadmap/pull/3), merge commit `cbb2928`.

- Codex audited/refined Czech and English READMEs, AGENTS rules, operations,
  architecture/development status and golden-evidence procedures under explicit
  IMPLEMENT + REVIEW delegation.
- Fixed validation of every evidence page and duplicate normalized questions;
  expanded synthetic candidate-validator coverage to 10 cases. Against the
  original validator, three cases reproduced the defects.
- Verified destructive ingest ordering with a fake client, source-page discovery
  and validation with synthetic data, relative links and Compose configuration.
  No real corpus benchmark, real-PDF evidence review or Docker runtime test was claimed.
- After the owner's explicit approval, Eval Governance passed including structure
  checks of all seven candidate batches. The owner separately authorized merge;
  dependency-audit findings remained open and the check stayed enabled.
- Preserved the old independent `main` as `archive/main-initial-20261028`, renamed
  the active default branch to `main`, and aligned CI/runbooks in `bfb1d85`.
  Existing open PR targets were updated; history and datasets were preserved.
- Evidence: [validator fix, 5dffd5b](https://github.com/jyenten/AI_roadmap/commit/5dffd5b),
  [regressions, aefaa40](https://github.com/jyenten/AI_roadmap/commit/aefaa40),
  [default-branch follow-up, bfb1d85](https://github.com/jyenten/AI_roadmap/commit/bfb1d85).
- Verification: Windows **222 passed, 1 skipped** (symlink privileges), two
  dependency warnings; GitHub CI on `main` **223 passed**. These results concern
  the integrated project, not the separate FAISS/lock experiments.
- Concepts covered: evidence-based documentation, meaningful regressions,
  governance boundaries, environment-dependent tests and preserving Git history.
- The observed implementation/audit was agent-assisted; it does not establish
  independent human mastery of these topics.


[↑ Obsah / Contents](#obsah)

<a id="en-2026-10-28--documentation-responsibilities-and-czech-navigation"></a>

### 2026-10-28 — Documentation responsibilities and Czech navigation

**Project evidence:** `da6b382` separates the development workflow from the approved
phase plan. DEVELOPMENT_GUIDE.md describes implementation/review practice;
ROADMAP.md owns phase goals and status. Original phase specifications were preserved.

- The subsequent documentation review adds complete Czech counterparts, language
  jumps, collapsible contents and section-return links across tracked Markdown files.
- API identifiers, examples, historical measurements, existing skill assessments
  and approval boundaries are preserved. Translation does not establish a new
  implementation milestone or an independent skill rating.
- Evidence: [documentation split, da6b382](https://github.com/jyenten/AI_roadmap/commit/da6b382).


[↑ Obsah / Contents](#obsah)

<a id="en-uncommitted-work-observed-on-2026-10-28"></a>

## Uncommitted work observed on 2026-10-28

These are worktree observations, not dated completed milestones. Their creation
dates and correctness are not inferred from file presence.

- Former `document-search-bm25` worktree: local `rrf_contribution`/`fuse_rankings`
  prototype with deterministic ID tie-breaking; BM25/Vector `search_with_ids`
  interface changes; modified requirements and an untracked Windows lockfile.
  There is no committed/released HybridRetriever integration or verified hybrid
  evaluation result from this work. Dependencies/lockfile are not approved by
  their existence. Other untracked agent experiments were not attributed to a
  versioned milestone.
- `agent/phase3-model-hardening`: the branch tip is the older `8aae380`, with
  uncommitted history/model/CLI/latency/retriever/test changes. Several concerns
  overlap the later integrated vector-baseline milestone; the dirty worktree is
  not evidence of another completed or merged feature.
- `experiment/vector-backend`: committed storage work is distinguished above
  from its untracked FAISS-retriever test. No experimental test-pass claim is made.

The original worktrees and their uncommitted changes were read only and preserved.
Next learning focus remains hybrid RRF with DEV/RANDOM measurement and no TEST
tuning; the storage/backend experiment remains a separate review track.


[↑ Obsah / Contents](#obsah)

<a id="en-branch-audit-coverage--2026-10-28"></a>

## Branch audit coverage — 2026-10-28

Seven current public GitHub branches were fetched and inspected. Ancestor
branches are counted once in the history above, rather than as separate
achievements. The inventory is a point-in-time snapshot, not a live status page.

| Public branch | Reviewed tip | Status relative to the reviewed `main` |
| --- | --- | --- |
| `main` | `bfb1d85` | Integrated project and current default |
| `master` | `3c0bfdd` | Historical API/CI foundation; ancestor of `main` |
| `retrieval-eval-refactor` | `010d8d1` | Early roadmap/evaluation checkpoint; ancestor of `main` |
| `docs/bilingual-rag-runbooks-20261028` | `9504b1e` | Merged through PR #3 |
| `chore/linux-lock-ci` | `a258e85` | Unmerged PR #1; lock proposal only |
| `dependabot/github_actions/actions/setup-python-7.1.0` | `21a5733` | Unmerged bot proposal, PR #2 |
| `archive/main-initial-20261028` | `0cb285c` | Preserved independent initial README history |

Eight local branches in the original project clone were also inspected, along
with all five registered worktrees. The current documentation checkout's
`main` and documentation branch are already represented in the public table.

| Original local branch | Reviewed tip | Evidence/state |
| --- | --- | --- |
| `agent/bm25-tests` | `646525d` | Clean worktree; tip already included in `main`; BM25 test provenance documented |
| `agent/phase3-model-hardening` | `8aae380` | Tip included in `main`; dirty audit worktree kept separate |
| `chore/linux-lock-ci` | `a258e85` | Clean worktree; same unmerged proposal as the public branch |
| `document-search-bm25` | `f9cc7e2` | Former default name; dirty hybrid/dependency worktree, not synchronized by this audit |
| `experiment/vector-backend` | `14159ce` | Local-only storage/FAISS commit plus an untracked retriever test |
| `master` | `3c0bfdd` | Same historical checkpoint as the public branch |
| `retrieval-eval-refactor` | `010d8d1` | Same historical checkpoint as the public branch |
| `retrieval-eval-refactor¨` | `3c0bfdd` | Local alias of the `master` checkpoint; no unique milestone |

Cached private-mirror refs `codex-private/main` and
`codex-private/agent/bm25-tests` both pointed to `646525d`, already included in
the public history. Only those local refs were inspected; the live private
remote was not fetched. The obsolete cached `origin/document-search-bm25` in
the documentation checkout is a pre-rename ref, not an eighth current public
branch. No branches, source code, datasets or dependency files were changed by
this learning-log audit.


---

<a id="cz"></a>
## CZ — Česká verze


[↑ Obsah / Contents](#obsah)

<a id="cz-cíl"></a>

## Cíl

Rozvíjet samostatnou zdatnost v:

- programování v Pythonu
- softwarové architektuře a testování
- Gitu, CI/CD a Dockeru
- RAG systémech a vyhledávání informací
- evaluaci AI a observabilitě
- AI agentech a vývoji s jejich pomocí


[↑ Obsah / Contents](#obsah)

<a id="cz-úrovně-dovedností"></a>

## Úrovně dovedností

- NOT ASSESSED — dosud bez samostatného prokázání
- GUIDED — dokončeno s vysvětlováním nebo pomocí
- INDEPENDENT — implementováno a vysvětleno bez pomoci
- PROFICIENT — samostatně použito na jiném problému

Dokončená funkce projektu automaticky neznamená zvládnutí příslušné dovednosti.


[↑ Obsah / Contents](#obsah)

<a id="cz-ověřený-stav-projektu"></a>

## Ověřený stav projektu

Datum: 2026-10-28
Výchozí větev: main
Zkontrolovaný commit projektu: bfb1d85 (před touto aktualizací deníku)

- PR #3 je sloučený: dvojjazyčné provozní návody, opravy validátoru evidence a regrese.
- Poslední ověřené GitHub CI na `main`: **223 úspěšných testů za 4,99 s** ([běh 40744368854](https://github.com/jyenten/AI_roadmap/actions/runs/40744368854)).
- Gitleaks a CodeQL na této revizi prošly. Dependency Audit nadále selhává kvůli otevřeným nálezům ChromaDB; nebyl vypnut ani pro něj nebyla udělena výjimka.
- Baseline BM25 a Vector na DEV/RANDOM zůstávají zachované. Při aktualizaci tohoto deníku nebyly znovu měřeny; oddělený TEST zůstává beze změny.
- Hybridní RRF a práce na rozhraní ID retrieverů zůstávají lokální a necommitnuté.
- Návrh Linux lock souboru (PR #1), návrh Dependabotu (PR #2) a lokální experiment FAISS/úložiště jsou oddělené od integrovaného stavu `main`.

Dokončení projektu a hodnocení lidských dovedností zůstávají oddělené. Níže uvedená existující hodnocení GUIDED jsou zachována; tato revize historie nepřiděluje nové INDEPENDENT ani PROFICIENT.


[↑ Obsah / Contents](#obsah)

<a id="cz-historický-stav-projektu--2026-10-12"></a>

## Historický stav projektu — 2026-10-12

Datum: 2026-10-12
Větev: document-search-bm25
Commit: 9ed9985

V projektu dokončeno:

- základ FastAPI RAG
- zpracování PDF a vektorové úložiště Chroma
- baseline vektorového retrievalu
- evaluační datasety a metriky retrievalu
- oddělení DEV / RANDOM / závěrečného TEST
- měření latence retrievalu
- JSONL historie evaluace
- kontroly Git původu
- automatizované testování a GitHub CI

Poslední ověřená úplná testovací sada: 142 úspěšných testů, 1 přeskočený.

Jde o dosažené výsledky projektu, nikoli o hodnocení samostatných dovedností.


[↑ Obsah / Contents](#obsah)

<a id="cz-historický-učební-plán-fáze-33--bm25-2026-10-12"></a>

## Historický učební plán: fáze 3.3 — BM25 (2026-10-12)

Téma: Lexikální retrieval nad existujícími Chroma chunky.

Cíle učení:

- Vysvětlit řazení dokumentů v BM25.
- Rozumět tokenizaci, TF, IDF a délce dokumentu.
- Implementovat řazení retrievalu v Pythonu.
- Zachovat metadata zdroje a stránky.
- Psát smysluplné jednotkové a integrační testy.
- Porovnat BM25 s vektorovým retrievalem.

Samostatné cvičení:

Implementovat BM25Retriever.search() a vysvětlit řazení i rozhodování při shodě skóre.

Dosavadní hodnocení dovednosti: NOT ASSESSED


[↑ Obsah / Contents](#obsah)

<a id="cz-šablona-záznamu-učení"></a>

## Šablona záznamu učení


[↑ Obsah / Contents](#obsah)

<a id="cz-yyyy-mm-dd--téma"></a>

### YYYY-MM-DD — téma

Na čem jsem pracoval:

- doplnit

Co jsem se naučil:

- doplnit

Co jsem implementoval samostatně:

- doplnit

Co implementoval Codex nebo ChatGPT:

- doplnit

Jaké problémy jsem diagnostikoval:

- doplnit

Testy a důkazy:

- doplnit

Úroveň dovednosti: NOT ASSESSED / GUIDED / INDEPENDENT / PROFICIENT

Další cvičení:

- doplnit


[↑ Obsah / Contents](#obsah)

<a id="cz-pravidla-záznamů-učení"></a>

## Pravidla záznamů učení

Deník aktualizuj po významných milnících, nikoli po každé malé změně kódu.

Zaznamenávej obtíže a neporozumění. Nenadhodnocuj dovednosti. Ke slabým tématům se vracej samostatnými cvičeními.


[↑ Obsah / Contents](#obsah)

<a id="cz-historie-projektu-a-učení"></a>

## Historie projektu a učení

Retrospektivní záznamy přidané 28. 10. 2026 jsou rekonstruované z historie commitů, vybraných změn zdrojů/testů, stavu PR a lokálních worktrees. Data označují zaznamenané commity, nikoli ověřenou dobu studia. Uvedené pojmy se v práci vyskytují; samotné Git autorství neprokazuje samostatnou lidskou implementaci, porozumění ani rozsah AI pomoci. Autorství uvádíme pouze tam, kde je dokládá existující deník nebo pozorovaná spolupráce. Historické skripty a experimentální testy při auditu deníku nebyly znovu spouštěny.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-05-12-až-2026-05-22--python-analýza-dat-a-klasické-ml"></a>

### 2026-05-12 až 2026-05-22 — Python, analýza dat a klasické ML

**Doklady projektu:** Cvičení původně zaznamenaná v historii nyní uchované větví `master`, následně převzatá do `main` a přesunutá pod `archive/`.

- Vstup v Pythonu, podmínky, cykly, funkce a kolekce; později analýza CSV v Pandas, filtrování/seskupování, chybějící hodnoty a grafy Matplotlib.
- Lineární regrese, klasifikace, křížová validace/přeučení, RandomForest, tvorba příznaků a úplné ML cvičení.
- Pojmy k upevnění: oddělení train/test, reprodukovatelné rozdělení, předzpracování a interpretace metrik místo pouhého fitování modelu.
- Důkazy: [počáteční dny 1–4, 8daf3fa](https://github.com/jyenten/AI_roadmap/commit/8daf3fa), [Pandas, 909b475](https://github.com/jyenten/AI_roadmap/commit/909b475), [úplné ML cvičení, 1c852a6](https://github.com/jyenten/AI_roadmap/commit/1c852a6).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-05-23-až-2026-06-09--pytorch-nlp-počáteční-rag-a-kontejnery"></a>

### 2026-05-23 až 2026-06-09 — PyTorch, NLP, počáteční RAG a kontejnery

**Doklady projektu:** Archivovaná učební cvičení, již zahrnutá v `main`.

- Sítě PyTorch, CNN/klasifikace obrázků, transfer learning a ResNet18.
- Klasifikace sentimentu v NLP, embeddingy, BERT/tokenizéry, attention a experimenty Hugging Face pipeline/QA.
- Počáteční RAG experimenty následované cvičeními aplikací FastAPI a Docker.
- Pojmy k upevnění: rozhraní tensor/model, tokenizace, retrieval oproti generování, kompatibilita balíčků a hranice běhu kontejnerů.
- Důkazy: [PyTorch, 1c05b12](https://github.com/jyenten/AI_roadmap/commit/1c05b12), [BERT, 4097483](https://github.com/jyenten/AI_roadmap/commit/4097483), [Hugging Face QA, 1441c8a](https://github.com/jyenten/AI_roadmap/commit/1441c8a), [Docker/RAG API, f57517e](https://github.com/jyenten/AI_roadmap/commit/f57517e).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-07-27-až-2026-08-21--základ-rag-api-diagnostika-a-ci"></a>

### 2026-07-27 až 2026-08-21 — Základ RAG API, diagnostika a CI

**Milník projektu:** Historický základ `master`; zahrnutý v `main`.

- Lepší čištění/chunkování PDF, získaný kontext a přiřazení zdrojů k vybranému kontextu; metadata zdrojů přidaná do API odpovědí.
- Endpointy health/stats/readiness, validace prázdných otázek a ošetření nedostupnosti RAG služeb; Docker a Compose konfigurace.
- Kontroly API, testovací Chroma, smoke testy a GitHub Actions CI.
- Zahrnuté pojmy: připravenost služby oproti životnosti, dohledatelné odpovědi, typované hranice API, izolace testů a opakovatelné vývojové kontroly.
- Důkazy: [metadata zdrojů, 581d6f6](https://github.com/jyenten/AI_roadmap/commit/581d6f6), [readiness, 6950495](https://github.com/jyenten/AI_roadmap/commit/6950495), [CI/smoke testy, 702c0ab](https://github.com/jyenten/AI_roadmap/commit/702c0ab), [vrchol `master`, 3c0bfdd](https://github.com/jyenten/AI_roadmap/commit/3c0bfdd).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-09-01-až-2026-09-16--diagnostika-retrievalu-a-základ-evaluace"></a>

### 2026-09-01 až 2026-09-16 — Diagnostika retrievalu a základ evaluace

**Milník projektu:** Zahrnutý v `main`; `retrieval-eval-refactor` uchovává raný stav tohoto vývoje, nikoli konečnou implementaci evaluace.

- Diagnostika retrievalu, upravené předzpracování/chunkování s regresními testy, počáteční DEV evaluace a nástroje historie evaluace.
- Zaznamenaná architektura, roadmapa a vývojová pravidla.
- Zahrnuté pojmy: diagnostika retrievalu odděleně od generování, hranice/překryv chunků, evaluace podložená evidencí a ohraničený rozsah vývoje.
- Důkazy: [regrese chunkování, 26b39e6](https://github.com/jyenten/AI_roadmap/commit/26b39e6), [počáteční evaluace, 2fafcae](https://github.com/jyenten/AI_roadmap/commit/2fafcae), [vrchol `retrieval-eval-refactor`, 010d8d1](https://github.com/jyenten/AI_roadmap/commit/010d8d1).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-09-16-až-2026-09-17--nezávislý-průzkumník-pdf-stránek"></a>

### 2026-09-16 až 2026-09-17 — Nezávislý průzkumník PDF stránek

**Milník projektu:** Implementovaný a zahrnutý v `main`.

- Modely stránek/vyhledávání, normalizace/tokenizace, načítání PDF, validace cest/PDF/vstupů, BM25 indexování/vyhledávání a interaktivní CLI.
- Syntetické testy, vývojové kontroly a automatické sledování změn pro testy.
- Zahrnuté pojmy: neměnné modely, identita zdroje/stránky, limity prostředků, lexikální řazení a oddělení stránkového průzkumu od chunkového retrievalu.
- Důkazy: [bezpečné načítání PDF, f05e080](https://github.com/jyenten/AI_roadmap/commit/f05e080), [BM25 vyhledávání, 4a0fa06](https://github.com/jyenten/AI_roadmap/commit/4a0fa06), [CLI průzkumníku stránek, 1f3fad5](https://github.com/jyenten/AI_roadmap/commit/1f3fad5).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-09-22-až-2026-10-08--párování-evidence-a-řízená-evaluace"></a>

### 2026-09-22 až 2026-10-08 — Párování evidence a řízená evaluace

**Milník projektu:** Implementovaný a zahrnutý v `main`.

- Evaluace rozdělená na modely, načítání datasetů, párování evidence, metriky, runner a JSONL historii; reprodukovatelný náhodný výběr.
- Oddělení DEV/RANDOM/závěrečného TEST, validace/povýšení kandidátů, kurátorská pravidla, CODEOWNERS a CI Eval Governance.
- Zahrnuté pojmy: fyzická čísla PDF stránek, normalizované doslovné fragmenty, MRR/Hit@K, náhodné seedy, únik dat mezi datasety a hranice lidského schválení.
- Důkazy: [modely datasetů, f0b30b8](https://github.com/jyenten/AI_roadmap/commit/f0b30b8), [párování evidence, 8e93ce5](https://github.com/jyenten/AI_roadmap/commit/8e93ce5), [runner/metriky, ed6bf73](https://github.com/jyenten/AI_roadmap/commit/ed6bf73), [náhodný výběr, 3247ab4](https://github.com/jyenten/AI_roadmap/commit/3247ab4), [governance, 8aae380](https://github.com/jyenten/AI_roadmap/commit/8aae380).
- Pozdější revize našla vady ve starším `scripts.evaluate_random`; historická implementace neznamená, že je každé starší CLI nyní správné. Podporovaný postup porovnání je v [EVALUATION.md](rag_api_project/docs/EVALUATION.md#cz).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-11-až-2026-10-12--vektorový-baseline-latence-a-pravidla-agentů"></a>

### 2026-10-11 až 2026-10-12 — Vektorový baseline, latence a pravidla agentů

**Milník projektu:** Implementovaný a zahrnutý v `main`.

- Samostatný baseline VectorRetriever, výběr retrieveru v evaluaci, latence samotného retrievalu mean/p50/p95 a přísnější validace běhů/historie.
- Testy výběru v CLI, latence, modelů/historie a Git původu.
- Globální pravidla LEARN/IMPLEMENT/REVIEW a tento deník učení.
- Zahrnuté pojmy: stabilní rozhraní retrieverů, hranice měření, reprodukovatelná metadata běhu a oddělení dokončení projektu od zvládnutí dovedností.
- Důkazy: [vector/observabilita, 9ed9985](https://github.com/jyenten/AI_roadmap/commit/9ed9985), [pravidla agentů/deník, 50797d4](https://github.com/jyenten/AI_roadmap/commit/50797d4).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-13--fáze-33-bm25-retriever"></a>

### 2026-10-13 — Fáze 3.3: BM25 Retriever

**Milník projektu:** Dokončeno

- Implementován `BM25Retriever` nad existujícími Chroma chunky s výukovým vedením.
- Implementováno načítání korpusu, validace, tokenizace, lexikální párování, řazení a výběr top-k.
- Codex samostatně připravil regresní testy.
- Testy prošly revizí kódu a byly integrovány.
- Úplná regrese: 210 úspěšných testů, 1 přeskočený, 2 varování.
- Commit: `c101680` (push do origin/document-search-bm25).

**Doklady učení:**

- Procvičovány Python kolekce, list comprehensions, `enumerate()`, `sorted()`, `lambda` a validace dat.
- Procvičováno rozlišování indexů dokumentů od skóre relevance.
- Pochopen účel deterministického rozhodování při shodě skóre a lexikálního filtrování.
- Během implementace bylo potřebné vedení a opravy.

**Hodnocení dovednosti:** GUIDED

**Další samostatné cvičení:** Vysvětlit a změnit řazení retrievalu bez vedení krok za krokem.

**Další projektový milník:** Evaluace BM25 oproti Vector na DEV a poté RANDOM.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-14--historie-portfolia-původ-práce-agentů-a-bezpečnostní-automatizace"></a>

### 2026-10-14 — Historie portfolia, původ práce agentů a bezpečnostní automatizace

**Milník projektu:** Zahrnutý v `main`.

- Starší cvičení přesunuta pod `archive/` bez přepisování obsahu; aktualizovány README portfolia/projektu a uvedena pomoc AI při vývoji.
- Zdokumentována vnořená pravidla agentů, lokální worktree BM25 testů a ručně synchronizované soukromé zrcadlo. Existující BM25 záznam připisuje přípravu regresních testů Codexu; širší samostatné autorství se nevyvozuje.
- Přidány Gitleaks, Dependabot, Dependency Review a plánovaný/PR audit závislostí.
- Zahrnuté pojmy: přesný staging, zachování dokladů učení, izolovaná práce agentů, kontrola tajných údajů a odlišení úspěšných testů od bezpečnosti závislostí.
- Důkazy: [přesun archivu, d157023](https://github.com/jyenten/AI_roadmap/commit/d157023), [původ agentů, 646525d](https://github.com/jyenten/AI_roadmap/commit/646525d), [kontrola tajných údajů, b032e9a](https://github.com/jyenten/AI_roadmap/commit/b032e9a), [audit závislostí, 6a20b25](https://github.com/jyenten/AI_roadmap/commit/6a20b25).


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-15-až-2026-10-17--návrh-reprodukovatelných-linux-závislostí"></a>

### 2026-10-15 až 2026-10-17 — Návrh reprodukovatelných Linux závislostí

**Milník projektu:** Implementováno na `chore/linux-lock-ci`, **nesloučeno** do `main`; [PR #1](https://github.com/jyenten/AI_roadmap/pull/1) zůstává otevřený.

- Snapshot závislostí Linux/Python 3.11, ověření čisté instalace Ubuntu, kontroly souladu přímých závislostí/locku a instalace podle locku v CI.
- Na této větvi přidán samostatný dokument posouzení rizik ChromaDB.
- Zahrnuté pojmy: přímé a tranzitivní závislosti, locky specifické pro OS, `pip check`, validace čistého prostředí a sledování bezpečnostních rizik.
- Důkazy: [snapshot workflow, 4b26db1](https://github.com/jyenten/AI_roadmap/commit/4b26db1), [kontrola locku, 8e2e7ec](https://github.com/jyenten/AI_roadmap/commit/8e2e7ec), [vrchol větve, a258e85](https://github.com/jyenten/AI_roadmap/commit/a258e85).
- [Historické PR CI](https://github.com/jyenten/AI_roadmap/actions/runs/39022965393) na tomto vrcholu prošlo, bezpečnostní kontroly závislostí selhaly. Nejde o schválení verzí závislostí ani důkaz, že `main` tento lock používá.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-20--fáze-34-evaluace-retrievalu"></a>

### 2026-10-20 — Fáze 3.4: Evaluace retrievalu

**Milník projektu:** Dokončeno

- BM25 integrováno do evaluačního CLI přes registr retrieverů.
- Rozšířeny parametrizované CLI testy pro legacy, vector a BM25.
- Úplná regresní sada prošla.
- BM25 a Vector vyhodnoceny na DEV (20 otázek) a RANDOM (25 otázek).
- Oddělený TEST dataset zachován.

**Baseline MRR:**

- DEV: BM25 0.7171, Vector 0.8321
- RANDOM: BM25 0.8133, Vector 0.6050

**Doklady učení:**

- Procvičováno vyhledávání ve slovníku a vzor registru.
- Procvičováno řetězení výjimek pomocí `raise ... from exc`.
- Procvičovány `getattr()`, parametrizované pytest testy a diagnostika `KeyError` a `ImportError`.
- Během implementace bylo potřebné vedení.

**Hodnocení dovednosti:** GUIDED

**Další projektový milník:** Hybridní retrieval pomocí RRF.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-26--experiment-úložiště-dokumentů-a-ověřeného-faiss-balíčku"></a>

### 2026-10-26 — Experiment úložiště dokumentů a ověřeného FAISS balíčku

**Milník projektu:** Commit pouze na lokální `experiment/vector-backend` v `14159ce`; **není ve veřejné větvi `main`**.

- Přidán `DocumentStore` s načítáním JSON, validací ID/textu/zdroje/stránky a odmítáním duplicitních ID.
- Přidány kontroly počtu FAISS/indexových záznamů a loader ověřeného balíčku, který před načtením porovnává SHA-256 hodnoty s manifestem.
- Commitnuty regresní testy úložiště pro platné/neplatné záznamy, balíčky a kontrolní součty. Byla zkontrolována jejich přítomnost; audit je nespouštěl ani neurčil počet úspěšných testů.
- Zahrnuté pojmy: stabilní ID dokumentů, oddělení vektorového indexu a metadat, integrita oproti autenticitě, validace před načtením a regrese.
- Větev navazuje na **nesloučený návrh Linux locku**, a proto ji nelze považovat za izolovanou revidovanou změnu již integrovanou v `main`.
- Dodatečný test FAISS retrieveru není ve worktree sledovaný Gitem. Tento storage commit nedokládá hotový FAISS retriever ani náhradu Chroma.
- Z dostupných důkazů nebylo určeno rozdělení implementace člověk/AI ani samostatné vysvětlení; nové hodnocení dovednosti se nepřiděluje.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-26--automatizovaný-návrh-závislosti-github-actions"></a>

### 2026-10-26 — Automatizovaný návrh závislosti GitHub Actions

**Milník projektu:** Návrh vytvořený botem, **nesloučený**.

- `dependabot/github_actions/actions/setup-python-7.1.0` v `21a5733` navrhuje `actions/setup-python` 7.0.0 → 7.1.0 ve třech workflow.
- [PR #2](https://github.com/jyenten/AI_roadmap/pull/2) je otevřený. Jeho historický [běh CI](https://github.com/jyenten/AI_roadmap/actions/runs/40291737972) prošel; neprošly všechny bezpečnostní/governance kontroly.
- Jde o záznam aktivity automatizace a příležitosti k revizi, nikoli lidské implementace nebo prokázané nové dovednosti.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-28--dvojjazyčné-návody-regrese-validátoru-a-výchozí-main"></a>

### 2026-10-28 — Dvojjazyčné návody, regrese validátoru a výchozí main

**Milník projektu:** Dokončeno a integrováno přes [PR #3](https://github.com/jyenten/AI_roadmap/pull/3), merge commit `cbb2928`.

- Codex na základě výslovného zadání IMPLEMENT + REVIEW zkontroloval a upravil české/anglické README, pravidla AGENTS, provozní dokumentaci, stav architektury/vývoje a postupy golden evidence.
- Opravena validace každé stránky evidence a duplicitních normalizovaných otázek; syntetické pokrytí validátoru rozšířeno na 10 případů. Proti původnímu validátoru tři případy reprodukovaly vady.
- Ověřeno pořadí destruktivního ingestu s falešným klientem, průzkum zdrojových stránek a validace na syntetických datech, relativní odkazy a konfigurace Compose. Nebyl tvrzen benchmark skutečného korpusu, revize evidence ze skutečných PDF ani běhový test Dockeru.
- Po výslovném schválení vlastníkem prošla Eval Governance včetně strukturálních kontrol všech sedmi kandidátních dávek. Vlastník samostatně schválil merge; nálezy auditu závislostí zůstaly otevřené a kontrola zapnutá.
- Původní nezávislá `main` zachována jako `archive/main-initial-20261028`, aktivní výchozí větev přejmenována na `main` a CI/návody sladěny v `bfb1d85`. Cíle existujících otevřených PR byly aktualizovány; historie a datasety zachovány.
- Důkazy: [oprava validátoru, 5dffd5b](https://github.com/jyenten/AI_roadmap/commit/5dffd5b), [regrese, aefaa40](https://github.com/jyenten/AI_roadmap/commit/aefaa40), [navazující změna výchozí větve, bfb1d85](https://github.com/jyenten/AI_roadmap/commit/bfb1d85).
- Ověření: Windows **222 úspěšných testů, 1 přeskočený** (oprávnění symlinků), dvě varování závislostí; GitHub CI na `main` **223 úspěšných testů**. Tyto výsledky se vztahují k integrovanému projektu, nikoli k odděleným FAISS/lock experimentům.
- Zahrnuté pojmy: dokumentace podložená důkazy, smysluplné regrese, schvalovací hranice, testy závislé na prostředí a zachování Git historie.
- Pozorovaná implementace/audit využívaly agenta; nedokládají samostatné lidské zvládnutí těchto témat.


[↑ Obsah / Contents](#obsah)

<a id="cz-2026-10-28--odpovědnosti-dokumentace-a-česká-navigace"></a>

### 2026-10-28 — Odpovědnosti dokumentace a česká navigace

**Doklady projektu:** `da6b382` odděluje vývojový postup od schváleného plánu fází.
DEVELOPMENT_GUIDE.md popisuje implementaci a revizi; ROADMAP.md určuje cíle a stav
fází. Původní specifikace fází zůstaly zachovány.

- Následná revize dokumentace přidává úplné české protějšky, přepínání jazyků,
  sbalitelné obsahy a návraty z kapitol ve všech verzovaných Markdown souborech.
- Identifikátory API, příklady, historická měření, existující hodnocení dovedností
  a schvalovací hranice zůstávají zachované. Překlad nedokládá nový implementační
  milník ani samostatnou úroveň dovednosti.
- Důkaz: [oddělení dokumentace, da6b382](https://github.com/jyenten/AI_roadmap/commit/da6b382).


[↑ Obsah / Contents](#obsah)

<a id="cz-necommitnutá-práce-pozorovaná-28-10-2026"></a>

## Necommitnutá práce pozorovaná 28. 10. 2026

Jde o pozorování worktrees, nikoli datované dokončené milníky. Z pouhé přítomnosti souborů se nevyvozuje datum vytvoření ani správnost.

- Bývalý worktree `document-search-bm25`: lokální prototyp `rrf_contribution`/`fuse_rankings` s deterministickým rozhodováním podle ID; změny rozhraní BM25/Vector `search_with_ids`; upravené requirements a nesledovaný Windows lock soubor. Tato práce nedokládá commitnutou/vydanou integraci HybridRetrieveru ani ověřený výsledek hybridní evaluace. Přítomnost závislostí/locku neznamená jejich schválení. Další nesledované experimenty agentů nebyly připsány verzovanému milníku.
- `agent/phase3-model-hardening`: vrchol větve je starší `8aae380` s necommitnutými změnami historie/modelů/CLI/latence/retrieverů/testů. Několik oblastí se překrývá s později integrovaným vektorovým baseline; změněný worktree není důkazem další hotové či sloučené funkce.
- `experiment/vector-backend`: výše je odlišena commitnutá práce na úložišti od nesledovaného testu FAISS retrieveru. Úspěch experimentálních testů se netvrdí.

Původní worktrees a necommitnuté změny byly pouze čteny a zachovány. Dalším učebním zaměřením zůstává hybridní RRF s měřením DEV/RANDOM bez ladění na TEST; experiment úložiště/backendu zůstává samostatným předmětem revize.


[↑ Obsah / Contents](#obsah)

<a id="cz-pokrytí-auditu-větví--2026-10-28"></a>

## Pokrytí auditu větví — 2026-10-28

Bylo staženo a zkontrolováno sedm tehdejších veřejných GitHub větví. Předkové se v historii počítají jednou, nikoli jako samostatné úspěchy. Soupis je časový snímek, nikoli živá stavová stránka.

| Veřejná větev | Zkontrolovaný vrchol | Stav vůči zkontrolované `main` |
| --- | --- | --- |
| `main` | `bfb1d85` | Integrovaný projekt a současná výchozí větev |
| `master` | `3c0bfdd` | Historický základ API/CI; předek `main` |
| `retrieval-eval-refactor` | `010d8d1` | Raný stav roadmapy/evaluace; předek `main` |
| `docs/bilingual-rag-runbooks-20261028` | `9504b1e` | Sloučeno přes PR #3 |
| `chore/linux-lock-ci` | `a258e85` | Nesloučený PR #1; pouze návrh locku |
| `dependabot/github_actions/actions/setup-python-7.1.0` | `21a5733` | Nesloučený návrh bota, PR #2 |
| `archive/main-initial-20261028` | `0cb285c` | Zachovaná nezávislá původní historie README |

Zkontrolováno bylo také osm lokálních větví v původním klonu projektu a všech pět registrovaných worktrees. `main` a dokumentační větev nynějšího dokumentačního checkoutu jsou již zastoupené ve veřejné tabulce.

| Původní lokální větev | Zkontrolovaný vrchol | Důkazy/stav |
| --- | --- | --- |
| `agent/bm25-tests` | `646525d` | Čistý worktree; vrchol již v `main`; původ BM25 testů zdokumentován |
| `agent/phase3-model-hardening` | `8aae380` | Vrchol v `main`; změněný auditní worktree ponechán odděleně |
| `chore/linux-lock-ci` | `a258e85` | Čistý worktree; stejný nesloučený návrh jako veřejná větev |
| `document-search-bm25` | `f9cc7e2` | Bývalý výchozí název; změněný hybridní/závislostní worktree, audit jej nesynchronizoval |
| `experiment/vector-backend` | `14159ce` | Pouze lokální storage/FAISS commit a nesledovaný test retrieveru |
| `master` | `3c0bfdd` | Stejný historický stav jako veřejná větev |
| `retrieval-eval-refactor` | `010d8d1` | Stejný historický stav jako veřejná větev |
| `retrieval-eval-refactor¨` | `3c0bfdd` | Lokální alias stavu `master`; bez samostatného milníku |

Uložené reference soukromého zrcadla `codex-private/main` a `codex-private/agent/bm25-tests` obě ukazovaly na `646525d`, již zahrnutý ve veřejné historii. Kontrolovaly se pouze tyto lokální reference; živý soukromý remote nebyl stahován. Zastaralá uložená `origin/document-search-bm25` v dokumentačním checkoutu je reference před přejmenováním, nikoli osmá současná veřejná větev. Audit deníku učení nezměnil větve, zdrojový kód, datasety ani soubory závislostí.

[↑ Nahoru / Back to top](#top) · [Obsah / Contents](#obsah)
