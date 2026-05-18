---
name: stage-1-problem-framing
description: Verify the problem the idea attacks is real and worth solving
load-trigger: Step 3 of SKILL.md, first stage
persona: advisor
---

# Stage 1: Problem Framing

**Persona**: Senior Advisor — see [../personas/advisor.md](../personas/advisor.md). Declare on entry:
> "Adopting persona: Advisor. Stance: charitable but probing — convince me this problem is real."

**Goal**: Confirm the problem is real, not a benchmark artifact, not already implicitly solved, and not dissolved by simply scaling the baseline.

**Time budget**: 30-60 sec per idea.

## Procedure

**Before executing**: load [../question-banks/stage-1-questions.md](../question-banks/stage-1-questions.md). The Q-bank defines the M1-M5 mandatory questions and the R6-R10 / P11-P15 recommended/probing sets. Record coverage IDs in the per-stage output.

1. **Idea-or-engineering gate (run FIRST, before any attacks).** Strip the framing words ("measurement", "principled search", "deliverable"). What remains as the *mechanism*? If the answer is one of:
   - Hyperparameter sweep / grid search / Bayesian-opt / ASHA / Hyperband / random search
   - "Just train longer / bigger / with more seeds"
   - Re-running the existing pipeline or a public baseline for comparison
   - Code refactor / library swap with no behavioural change
   - Pure measurement / instrumentation / logging
   - Any framing that reduces to "tune X better" without naming what is being changed mechanistically
   ...then Stage 1 is an **automatic FAIL** with tag `not-an-idea`. Skip every other stage and emit Stage 8 verdict `KILL` with reframe = "move to project prerequisites / `Notes & warnings`, not a vetted idea". The `--climb-mode` flag does NOT override this gate — engineering tasks dressed up as research are still engineering tasks, regardless of mode.
2. State the problem in 1 sentence (M1).
3. Answer all mandatory Q-bank items (M1-M5). Then answer ≥ 3 of R6-R10.
4. Issue ≥ 2 of the attack templates below. Steel-man each rebuttal.
5. If the idea is borderline, escalate to P11-P15.
6. Determine verdict.

## Attack templates (try ≥ 2)

- "This is a benchmark artifact — fixing it means nothing in practice."
- "Scaling the baseline 10× (or swapping to the next model size) solves this; the idea is moot."
- "The problem is already implicitly solved by `<existing technique>` — just not on this benchmark name."
- "This problem doesn't matter for any downstream task — what real user pain does it touch?"
- "Strip the framing — what is the *mechanism* being added? If the answer is 'tune HPs better', 'train longer', or 'measure the baseline', this is engineering, not an idea." (If this attack lands UNREBUTTED, the verdict is FAIL `not-an-idea`, not WARN.)

## Rebuttal loop (applies to every attack)

For each attack issued, run the loop in [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. Generate a **steel-manned rebuttal** — the strongest argument the idea author would give. Cite papers, use logic, no handwaving.
2. Advisor persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. If WEAKENED, ONE refined follow-up (Round 2). Then stop. No Round 3.
4. Max 3 attacks get the full rebuttal cycle; additional attacks listed without a cycle.
5. User MAY interject with their own rebuttal (tag `Source: user`).
6. Each cycle emitted using [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. After all attacks, apply the UNREBUTTED-downgrade rule from [../rules/decision-logic.md](../rules/decision-logic.md) to the verdict below.

## Output

Write a `Stage 1` block using [../templates/per-stage-output.md](../templates/per-stage-output.md). Include the `Rebuttal-cycle summary` (DEFLECTED / WEAKENED / UNREBUTTED counts).

## Verdict criteria

- ✅ **PASS** — problem real, no obvious dissolution, and a mechanism contribution is present.
- ⚠️ **WARN** — problem unclear or scoped too narrowly; needs reframe before Stage 2 attack can land cleanly.
- ❌ **FAIL** — one of:
  - `benchmark-artifact` — fixing the metric does not reflect a real capability.
  - `scale-dissolves` — next model size / 10× compute makes the problem go away.
  - `already-solved` — known technique on renamed task.
  - `not-an-idea` — engineering/HP/measurement task with zero mechanism contribution (per the idea-or-engineering gate above). KILL with reframe to prerequisites, not a vetted idea.

## Early-exit

If Stage 1 = FAIL → skip Stages 2-7 entirely; go directly to Stage 8 with provisional verdict `KILL`.
