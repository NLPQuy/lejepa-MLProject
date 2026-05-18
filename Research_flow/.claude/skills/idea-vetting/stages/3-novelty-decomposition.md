---
name: stage-3-novelty-decomposition
description: Pinpoint exactly where the novelty lives; strip away non-novel scaffolding
load-trigger: Step 3 of SKILL.md, after Stage 2 (skip if Stage 2 = FAIL)
persona: critical-reviewer
---

# Stage 3: Novelty Decomposition

**Persona**: Critical Reviewer — see [../personas/critical-reviewer.md](../personas/critical-reviewer.md). Declare on entry:
> "Adopting persona: Critical Reviewer. Stance: default reject — convince me where the contribution actually is."

**Goal**: Identify which of 8 novelty axes the idea touches, strip away "implementation detail" scaffolding, and detect rebranding patterns.

**Time budget**: 1-2 min.

## The 8 novelty axes

1. **Novel objective** (new loss / training criterion)
2. **Novel architecture** (new module / layer / connectivity)
3. **Novel optimization** (optimizer / scheduler / training trick)
4. **Novel theoretical framing** (new analysis / bound / principle)
5. **Novel empirical finding** (X works where unknown, new scaling law)
6. **Novel application** (technique-domain pairing)
7. **Novel evaluation** (new metric / protocol)
8. **Novel synthesis** (combination not previously explored)

## Procedure

**Before executing**: load [../question-banks/stage-3-questions.md](../question-banks/stage-3-questions.md). The Q-bank defines M1-M8 (axis applicability), R9-R12 (rebranding test), S13 (strip test), D14-D17 (defensibility). Record coverage IDs in the per-stage output.

1. Mark applicability of each of the 8 axes — answer M1-M8 with citations.
2. For each applicable axis, write a 1-2 sentence contribution statement.
3. Run the **strip test** (S13).
4. Run the **rebranding check** (R9-R12).
5. Defensibility test: D14-D17 (A* venue? workshop? engineering note? citation-worthy in 3y?).

## Strip test

Remove the claimed novel parts. Does the remainder give the same result?
- "No, synergy exists" → axis is genuine.
- "Maybe, partial" → axis is incremental.
- "Yes, same result" → axis is illusory; novelty is cosmetic.

## Rebranding patterns to detect

- Renaming an existing method.
- Swapping module placement only.
- Changing notation only.
- Swapping activation / kernel / norm.
- Pure hyperparameter sweep.

## Rebuttal loop

The 4 rebranding-check questions (R9-R12) and the strip test (S13) double as **attacks** in this stage. For each that fires (i.e., the rebranding/strip test surfaces a concern), run the rebuttal loop per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's argument that the apparent rebrand is genuinely a new contribution. Must cite the differentiating mechanism / argument, not vague "ours is novel because we say so".
2. Critical Reviewer persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. WEAKENED → Round 2 (refined), then stop. No Round 3.
4. Max 3 rebrand/strip concerns get full rebuttal; additional concerns listed.
5. User-input rebuttal supported (`Source: user`).
6. Cycles use [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade rule from [../rules/decision-logic.md](../rules/decision-logic.md).

## Output

Write a `Stage 3` block using `../templates/per-stage-output.md`. Include the axis-applicability table, strip-test result, rebranding-check result, defensibility verdict, AND the `Rebuttal-cycle summary`.

## Verdict criteria

- ✅ **PASS** — ≥ 1 axis clearly novel and defensible.
- ⚠️ **WARN** — contribution exists but is incremental — OK for workshop or engineering report, weak for A*.
- ❌ **FAIL** — cosmetic novelty only (renaming / notation / pure rebranding).

## Early-exit

No early-exit. Stage 3 result always feeds Stage 8 synthesis.
