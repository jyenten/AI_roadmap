# AI RAG Project Development Guide

## 1. Purpose

This document defines how the AI RAG project is developed.

It establishes rules for:

- development workflow
- scope control
- module design
- Python style
- testing
- evaluation
- Git usage
- branching
- documentation
- security
- collaboration and learning workflow

The purpose is not to introduce unnecessary process.

The purpose is to keep development:

```text
predictable
testable
measurable
reproducible
understandable
```

---

## 2. Core Development Strategy

The project follows:

```text
Complete
   ↓
Measure
   ↓
Improve
```

The preferred approach is to build a complete vertical system to a
sufficient quality level before deeply optimizing individual components.

The project should avoid two extremes.

### Extreme 1 — premature perfection

```text
perfect component A
↓
perfect component B
↓
perfect component C
```

Problem:

The project may spend large amounts of time optimizing a subsystem before
knowing whether that subsystem is actually the main bottleneck.

---

### Extreme 2 — uncontrolled prototype growth

```text
feature
↓
another feature
↓
temporary workaround
↓
another workaround
↓
large refactor
```

Problem:

The system becomes difficult to understand, test, and reproduce.

---

### Preferred model

```text
working vertical slice
        ↓
measurement
        ↓
identify weakness
        ↓
improve one subsystem
        ↓
test
        ↓
measure again
```

---

## 3. Phase-Based Development

Development follows the phases defined in:

```text
docs/ROADMAP.md
```

Each phase contains:

- a clear goal
- planned modules
- important concepts
- an estimated time
- a Definition of Done

A phase should not be expanded indefinitely.

When the Definition of Done is satisfied, the phase is considered frozen.

---

## 4. Scope Control

Scope control is a major project rule.

During a phase, implement only functionality required to complete that
phase.

Example:

PHASE 2A requires:

```text
PDF loading
text normalization
tokenization
BM25 indexing
search
CLI
tests
basic security
```

PHASE 2A does not require:

```text
fuzzy search
semantic search
LLM reranking
query rewriting
synonym dictionaries
hybrid retrieval
advanced UI
```

Those ideas may be useful later, but they do not block PHASE 2A.

---

## 5. Backlog Rule

A useful idea discovered during implementation does not automatically
become part of the current task.

The preferred flow is:

```text
new idea
   ↓
does current Definition of Done require it?
   │
   ├── YES → implement
   │
   └── NO  → backlog / future phase
```

This rule exists specifically to prevent development loops.

---

## 6. Architecture Before Large Refactors

Before a major architectural change:

```text
identify the problem
↓
understand current behavior
↓
define target architecture
↓
define interfaces
↓
implement
```

Do not repeatedly change interfaces while implementing dependent modules
unless a concrete technical problem requires it.

For significant changes, update:

```text
docs/ARCHITECTURE.md
```

before or together with the implementation.

---

## 7. Module Design

Each Python module should have one clear primary responsibility.

Examples:

```text
normalize.py
→ text normalization

tokenize.py
→ tokenization

load_pages.py
→ PDF page loading

build_index.py
→ BM25 index creation

search.py
→ search execution
```

A file should not become a collection of unrelated functions.

---

## 8. Major Functions and Files

Major pipeline responsibilities should usually have their own module.

However:

```text
one function
≠
automatically one file
```

Small helper functions should remain with the module that owns their
responsibility unless they are:

- reused by multiple modules
- independently testable domain concepts
- large enough to deserve a separate abstraction

Avoid excessive file fragmentation.

The goal is:

```text
high cohesion
+
low coupling
```

---

## 9. High Cohesion

A module has high cohesion when its functions belong to the same
responsibility.

Good example:

```text
pdf_validation.py

validate_pdf_extension()
validate_pdf_signature()
validate_pdf_limits()
```

All functions belong to PDF validation.

---

## 10. Low Coupling

Modules should depend on as few implementation details of other modules
as possible.

Preferred:

```python
results = search_pages(
    index,
    query,
)
```

Not preferred:

```text
caller manually:
- reads BM25 internals
- accesses page arrays
- calculates scores
- sorts results
```

The implementation should be hidden behind a stable interface.

---

## 11. Public Interfaces

A subsystem should expose a small public API.

Examples:

```python
load_pdf_pages(...)
build_bm25_index(...)
search_pages(...)
```

or later:

```python
retrieve(...)
answer_question(...)
evaluate_dataset(...)
```

Internal helper functions may change more freely.

Callers should rely primarily on public interfaces.

---

## 12. Data Models

Structured data should use explicit data models instead of anonymous
tuples where the meaning is important.

Avoid:

```python
result = (
    source,
    page,
    score,
    text,
)
```

Prefer:

```python
SearchResult(
    document=document,
    score=score,
)
```

Benefits:

```text
readability
type safety
clear semantics
less index-based code
easier refactoring
```

---

## 13. Immutability

Objects representing facts should be immutable whenever practical.

Preferred example:

```python
@dataclass(frozen=True)
class PageDocument:
    source: str
    page: int
    text: str
```

Examples of data that should normally remain immutable:

```text
document identity
page number
gold evidence
evaluation question
completed search result
```

Mutable state should exist only when the problem genuinely requires it.

---

## 14. Getters and Setters

Python-style properties should be used only when access or mutation needs
controlled behavior.

Do not automatically create Java-style:

```python
get_page()
set_page()
```

for every field.

Prefer:

```python
document.page
```

for simple immutable data.

Use:

```python
@property
```

when controlled read access is useful.

Use a setter only when runtime mutation is intentionally supported and
must be validated.

Security should not depend on getters and setters.

---

## 15. Python Style

The project should use idiomatic Python.

Preferred:

```text
clear
compact
typed
readable
production-like
```

Avoid artificially verbose code written only for teaching purposes.

Also avoid code golf that sacrifices readability.

---

## 16. Compact Code

Compact Python constructs are encouraged when they remain readable.

Examples:

```python
return " ".join(text.lower().split())
```

```python
return [
    item
    for item in items
    if condition(item)
]
```

```python
sorted(
    results,
    key=lambda result: result.score,
    reverse=True,
)
```

These constructs should be learned because they are common in real
Python code.

---

## 17. Avoid Clever Code

Compact code becomes undesirable when understanding it requires
unnecessary mental work.

Avoid:

```text
deeply nested ternary expressions
nested lambdas
obscure one-liners
unnecessary metaprogramming
complex comprehensions with multiple responsibilities
```

Readability has priority over minimum line count.

---

## 18. Type Hints

New project code should normally use type hints.

Example:

```python
def tokenize(
    text: str,
) -> list[str]:
```

Type hints improve:

```text
readability
IDE assistance
static analysis
refactoring safety
interface clarity
```

They do not replace runtime validation.

---

## 19. Function Design

Functions should ideally have:

```text
clear purpose
clear input
clear output
limited side effects
predictable behavior
```

Prefer small functions with one responsibility.

However, functions should not be split merely to reduce line count.

---

## 20. Pure Functions

Where practical, prefer pure functions.

A pure function:

```text
same input
→
same output
```

and does not unexpectedly modify external state.

Example:

```python
normalize_text(text)
```

Pure functions are easier to:

```text
test
reason about
reuse
debug
```

---

## 21. Side Effects

Functions performing side effects should make that responsibility clear.

Examples:

```text
reading PDF files
writing evaluation history
logging
database access
HTTP requests
```

Do not hide significant side effects inside apparently simple utility
functions.

---

## 22. Error Handling

Errors should be explicit.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

because it hides failures.

Prefer controlled exceptions with meaningful messages.

Example:

```python
raise ValueError(
    "top_k must be greater than zero."
)
```

---

## 23. Fail Explicitly

Silent data loss is especially dangerous in RAG systems.

For example, if a PDF cannot be completely processed, do not silently
pretend that ingestion succeeded.

Preferred:

```text
document rejected
+
reason recorded
```

rather than:

```text
document partially processed
+
no warning
```

Data integrity has priority over silently continuing.

---

## 24. Logging vs Printing

Reusable application modules should eventually use logging rather than
`print()`.

Example:

```text
app/
document_search/
evaluation/
```

Command-line scripts may use `print()` for user-facing output.

Example:

```text
scripts/search_pdf.py
```

This distinction keeps application diagnostics separate from CLI
presentation.

---

## 25. Testing Strategy

Testing has multiple layers.

They serve different purposes.

```text
UNIT TEST
→ one function or module

INTEGRATION TEST
→ multiple components together

SMOKE TEST
→ basic end-to-end functionality

EVALUATION
→ model/retrieval quality
```

One type does not replace another.

---

## 26. Unit Tests

A new reusable module should normally receive corresponding unit tests.

Example:

```text
document_search/tokenize.py
        ↕
tests/document_search/test_tokenize.py
```

Tests should focus on behavior rather than internal implementation when
possible.

---

## 27. Synthetic Test Data

Unit tests should prefer small synthetic data.

Example:

```text
Document A:
"OSPF uses a designated router."

Document B:
"Database replication uses transactions."
```

This is preferable to requiring a 500-page production PDF for every
unit test.

Benefits:

```text
fast
deterministic
easy to understand
easy to debug
```

---

## 28. Real Corpus Testing

Real PDFs are still important.

They belong primarily in:

```text
integration testing
manual validation
evaluation
```

Unit tests and real-corpus validation serve different purposes.

---

## 29. Regression Tests

When a real bug is discovered and fixed, add a regression test when
practical.

The test should demonstrate that the same bug does not return later.

Example:

```text
bug:
page.extract_text used without ()

fix:
page.extract_text()

regression test:
verify actual extracted string is processed
```

---

## 30. Testing Before Commit

Before a meaningful code commit:

```text
stage exact intended files
↓
inspect staged diff
↓
run automated checks
↓
commit
```

Current project helper:

```cmd
python -m scripts.git_check
```

This currently performs:

```text
git diff --cached --check
+
pytest
```

A commit should not be created when these checks fail unless there is a
specific documented reason.

---

## 31. Evaluation Discipline

Retrieval quality must be measured rather than judged only by manually
selected examples.

Datasets have separate roles.

### DEV

May influence tuning.

### RANDOM

Used for robustness and discovery.

### TEST

Held out until tuning is complete.

---

## 32. Avoid Evaluation Leakage

Do not repeatedly inspect TEST failures and then modify the system to
solve them.

That effectively turns TEST into another DEV dataset.

The intended flow is:

```text
DEV
↓
design and tuning

RANDOM
↓
robustness discovery

TEST
↓
final generalization check
```

---

## 33. Gold Evidence

Gold evidence should be created independently from the retrieval system
being evaluated whenever practical.

Current approach:

```text
lexical BM25 corpus explorer
+
human validation
```

System being evaluated:

```text
embedding retrieval
+
CrossEncoder reranking
```

This separation reduces circular benchmark construction.

---

## 34. Measure Before Retrieval Changes

A major retrieval change should follow:

```text
record baseline
↓
implement change
↓
run DEV evaluation
↓
compare metrics
```

Avoid:

```text
change retrieval
↓
inspect one question
↓
declare improvement
```

---

## 35. Git Principles

Git history should represent meaningful project checkpoints.

A commit should ideally be:

```text
coherent
testable
small enough to review
large enough to represent one idea
```

---

## 36. Exact Staging

Do not use:

```cmd
git add .
```

as the normal workflow.

Prefer exact staging:

```cmd
git add document_search/models.py
git add tests/document_search/test_models.py
```

Benefits:

```text
avoids accidental files
forces awareness of commit contents
creates cleaner commits
```

---

## 37. Inspect Before Commit

Useful commands include:

```cmd
git status --short
```

```cmd
git diff
```

```cmd
git diff --cached
```

```cmd
git diff --cached --check
```

The developer should understand what is about to be committed.

---

## 38. Commit Scope

Do not unnecessarily combine unrelated work.

Prefer:

```text
commit 1:
evaluation dataset change

commit 2:
architecture documentation

commit 3:
BM25 data models
```

instead of one large commit containing unrelated modifications.

---

## 39. Commit Messages

Commit messages should describe the completed change.

Preferred examples:

```text
Add OSPF interface cost DEV question

Add project roadmap and architecture docs

Add document search data models

Add BM25 document indexing
```

Avoid vague messages such as:

```text
update
fix stuff
changes
work
```

---

## 40. Push Strategy

A local commit does not need to be pushed immediately after every tiny
change.

Push when there is a coherent checkpoint worth preserving remotely.

Before pushing:

```text
tests should pass
commit history should be understandable
working state should be known
```

---

## 41. Branch Strategy

Create a branch when work represents:

```text
a meaningful feature
a major refactor
an architectural experiment
a different development direction
```

Do not create a new branch for every minor edit.

Example of an appropriate branch:

```text
document-search-bm25
```

because it represents a separate architectural development direction.

---

## 42. Experimental Work

Experimental code does not need to become production code.

If an experiment is useful for learning but is not part of the final
architecture, it may be:

```text
stashed
kept on an experimental branch
removed after lessons are captured
```

Do not preserve complexity only because time was spent writing it.

---

## 43. Git Stash

Stash may be used for temporary work that should not enter the current
commit.

Example:

```cmd
git stash push -m "WIP heuristic PDF search prototype" -- scripts/search_pdf.py
```

Prefer stashing exact files when unrelated working-tree changes must
remain active.

---

## 44. Documentation

Project documentation lives under:

```text
docs/
```

Primary documents:

```text
ROADMAP.md
ARCHITECTURE.md
DEVELOPMENT_GUIDE.md
```

---

## 45. Documentation Responsibilities

### `ROADMAP.md`

Answers:

```text
what are we building?
in what order?
when is a phase complete?
```

---

### `ARCHITECTURE.md`

Answers:

```text
how is the system structured?
which modules exist?
how do they communicate?
what are dependency boundaries?
```

---

### `DEVELOPMENT_GUIDE.md`

Answers:

```text
how do we implement changes?
how do we test them?
how do we use Git?
how do we avoid scope creep?
```

---

## 46. Documentation Updates

Documentation should change when the actual project direction changes.

Do not update architecture documentation for every hypothetical idea.

Preferred:

```text
decision made
↓
documentation updated
↓
implementation
```

---

## 47. Security During Development

Security is not only a final PHASE 6 concern.

Basic security principles should be followed throughout development.

Examples:

```text
validate external input
avoid unsafe filesystem access
avoid exposing secrets
limit resource usage
pin important boundaries
fail explicitly
```

PHASE 6 performs deeper security hardening and threat modeling.

---

## 48. Security and Data Processing

Security validation and text preprocessing are separate concerns.

Security may decide:

```text
is this file allowed?
is this path safe?
is this request too large?
```

Preprocessing may decide:

```text
how should valid text be normalized?
```

Security code should not silently alter document meaning.

---

## 49. Resource Limits

External input should eventually have explicit limits.

Examples:

```text
maximum file size
maximum PDF pages
maximum query length
maximum top_k
maximum request size
```

Limits protect:

```text
memory
CPU
latency
service availability
```

---

## 50. Dependency Management

External libraries are part of the system's attack surface and
reproducibility model.

Dependencies should be:

```text
intentional
documented
reviewed
updated deliberately
```

Future production phases may add:

```text
dependency vulnerability scanning
version pinning strategy
automated update tooling
```

---

## 51. Learning and Implementation Workflow

Project implementation is also used as a learning process.

The code is manually typed rather than blindly copied whenever practical.

For each implementation subphase, the preferred explanation format is:

```text
1. what is being built
2. why it exists
3. complete file or logical code block
4. explanation of new logic
5. what is intentionally out of scope
6. one clear test step
7. expected result
```

---

## 52. Code Delivery Granularity

Do not split implementation into unnecessarily tiny conversational
steps.

Avoid:

```text
add one import
↓
run
↓
add three lines
↓
run
↓
rename variable
```

Prefer complete logical units.

Examples:

```text
models.py
```

or:

```text
normalize.py
+
tokenize.py
+
their tests
```

when both are small and closely related.

---

## 53. Large Modules

Larger or riskier components should receive their own implementation
block.

Examples:

```text
PDF loading
filesystem security
retrieval service
API lifecycle
```

because they contain more edge cases and deserve focused testing.

---

## 54. Explanation Style

Code explanations should focus primarily on concepts not previously used
in the project.

Previously learned fundamentals do not need full repetition unless their
use in the new context is important.

New concepts should be explained in enough depth to understand:

```text
syntax
purpose
data flow
design reason
failure modes
future use
```

---

## 55. Idiomatic Learning

The project should teach real Python patterns.

Useful constructs may include:

```text
dataclasses
properties
type hints
list comprehensions
dictionary comprehensions
generator expressions
sorted(..., key=...)
enumerate()
any()
all()
Path
context managers
custom exceptions
dependency injection
```

They should be introduced when they naturally solve a project problem.

---

## 56. No Artificial Simplification

Do not intentionally avoid a useful Python feature only because it is
new.

Instead:

```text
use appropriate feature
+
explain it
```

The goal is to gradually move toward production-quality Python.

---

## 57. No Premature Complexity

The opposite rule also applies.

Do not introduce:

```text
abstract base classes
complex inheritance
design patterns
async code
metaprogramming
advanced frameworks
```

unless they solve a real current problem.

The architecture should remain as simple as requirements allow.

---

## 58. Definition of Done for a Module

A reusable module is normally considered complete when:

```text
its responsibility is clear
its interface is defined
its implementation works
important inputs are validated
relevant unit tests pass
full project tests still pass
```

Not every module requires every possible edge case before progress can
continue.

---

## 59. Definition of Done for a Subphase

A development subphase is complete when:

```text
planned files exist
planned behavior works
tests pass
known intentional limitations are documented
no critical unresolved bug remains
```

Then development moves to the next subphase.

---

## 60. Freeze Rule

After a subphase or phase is complete:

```text
do not reopen it merely because an improvement is imaginable
```

Reopen it only when:

```text
evaluation exposes a problem
integration exposes a problem
security exposes a problem
requirements materially change
```

This is a central project rule.

---

## 61. Current Workflow

Current project phase:

```text
PHASE 2 — Evaluation Foundation
```

Current subphase:

```text
PHASE 2A — Universal Document Explorer
```

Current implementation sequence:

```text
2A.0
architecture freeze

2A.1
data models

2A.2
normalization + tokenization

2A.3
security foundations

2A.4
PDF loading + validation

2A.5
BM25 index

2A.6
search engine

2A.7
CLI

2A.8
integration
```

The main RAG retrieval implementation should remain unchanged until the
evaluation foundation is sufficiently complete.

---

## 62. Final Development Rule

When uncertain whether to add another feature, ask:

```text
Does this feature help complete the current Definition of Done?
```

If yes:

```text
implement it
```

If no:

```text
record it for later
and continue the current phase
```

The project should optimize for completed, measured, understandable
systems rather than endless local refinement.