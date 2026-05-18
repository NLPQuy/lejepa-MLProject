---
name: stage-2-prior-work-attack
description: Attempt to kill the idea by finding existing paper that already does it
load-trigger: Step 3 of SKILL.md, after Stage 1 (skip if Stage 1 = FAIL)
persona: prior-work-hunter
---

# Stage 2: Prior Work Attack

**Persona**: Prior-Work Hunter — see [../personas/prior-work-hunter.md](../personas/prior-work-hunter.md). Declare on entry:
> "Adopting persona: Prior-Work Hunter. Stance: hostile until proven novel — assume someone already did this."

**Goal**: Find a paper that already does this idea, or its close cousin. Most weak ideas die here.

**Time budget**: 2-3 min (web search required).

## Procedure

**Before executing**: load [../question-banks/stage-2-questions.md](../question-banks/stage-2-questions.md). The Q-bank defines M1-M5 (mandatory similar-paper search), A6-A10 (aggressive attacks), and D11-D15 (differentiation when close prior work surfaces). Record coverage IDs in the per-stage output.

1. Extract unique keywords from the idea (terms NOT in the source papers it already cites).
2. Run 3-5 search queries from the templates below to cover M1-M5.
3. For each promising hit, compare to the idea — same mechanism + same benchmark = hard duplicate.
4. Issue ≥ 3 attacks from A6-A10, each citing a specific paper.
5. Steel-man each rebuttal (charitable interpretation of the idea's delta).
6. If close prior work surfaces, run D11-D15.
7. Determine verdict.

## Search queries (template)

- Exact-phrase: `"<unique mechanism keywords>"`
- Author + topic: `<first-author of idea's source paper> <topic>` (follow-ups often by same author)
- Concurrent (last 12 mo): `<topic> arXiv 2024 OR 2025`
- Implicit equivalence: `<related technique> equivalent <topic>`
- GitHub: `site:github.com <unique mechanism keywords>`

## Attack templates (issue ≥ 3 — these correspond to A6-A10 in the Q-bank)

- "Isn't this just `<method M>` with `<minor variation V>`?"
- "This smells like `<classical algo>` in modern clothing."
- "`<Author>` did this in `<year>`, see arXiv:`<id>`."
- "Concurrent work `<paper>` from `<month>` covers the same mechanism."

## Rebuttal loop (applies to every attack)

For each of the ≥ 3 "Isn't this just X?" attacks, run the loop in [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's strongest delta argument vs the cited prior paper. Must cite specific mechanism / scale / benchmark differences, not vague "ours is different".
2. Hunter persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. WEAKENED → ONE refined round (Round 2), then stop.
4. Max 3 attacks get the full rebuttal cycle; additional citations listed without a cycle.
5. User-input rebuttal supported (`Source: user`).
6. Cycles emitted using [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade rule from [../rules/decision-logic.md](../rules/decision-logic.md).

A single UNREBUTTED attack here that cites an exact-duplicate paper is a hard duplicate → Stage 2 = FAIL → early-exit to Stage 8 KILL.

## Output

Write a `Stage 2` block using `../templates/per-stage-output.md`. Include a **Search log** sub-block (queries + close-call papers) and the `Rebuttal-cycle summary`.

## Verdict criteria

- ✅ **PASS** — no exact duplicate; differences from related work are substantial.
- ⚠️ **WARN** — close cousin exists; idea needs a clear delta argument to be publication-worthy.
- ❌ **FAIL** — exact prior paper found (same mechanism + same benchmark) → idea is a duplicate.

## Early-exit

If Stage 2 = FAIL (hard duplicate) → skip Stages 3-7; go to Stage 8 with verdict `KILL`. Log the duplicating paper to `_logs/_killed_ideas.md`.
