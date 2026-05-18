---
name: stage-4-theory-grounding
description: Test "why should this work" — beyond "benchmark goes up"
load-trigger: Step 3 of SKILL.md, after Stage 3
persona: theorist
---

# Stage 4: Theory Grounding

**Persona**: Theorist — see [../personas/theorist.md](../personas/theorist.md). Declare on entry:
> "Adopting persona: Theorist. Stance: empirics are noise — show me a mechanism."

**Goal**: Verify the idea has ≥ 1 mechanism explanation. Bonus if ≥ 2 views give consistent explanation (strong ideas usually do).

**Time budget**: 2-4 min (reasoning-heavy).

## The 7 theoretical views

1. **Inductive bias** — what bias does the method impose?
2. **Optimization** — what does it do to the loss landscape / training dynamics?
3. **Probabilistic** — Bayesian / MAP / MLE interpretation?
4. **Information-theoretic** — mutual info, compression, channel capacity?
5. **Geometry** — manifold structure, distances, projections?
6. **Dynamical systems** — fixed points, attractors, stability?
7. **Capacity argument** — does this need more or less model capacity?

## Procedure

**Before executing**: load [../question-banks/stage-4-questions.md](../question-banks/stage-4-questions.md). The Q-bank defines M1-M5 (mechanism + falsifiability), V6-V12 (the 7 views), and C13-C15 (consistency tests). In `--climb-mode`, the Q-bank's climb-mode shortcut applies. Record coverage IDs in the per-stage output.

1. Answer M1-M5 — get a 1-2 sentence mechanism, name the baseline failure mode it fixes, predict optimization behavior, state a falsification observation, and name a counterexample regime.
2. For each of V6-V12, attempt an argument. Mark applicable (✅) / weak (⚠️) / N/A (❌).
3. Identify the **strongest view** + why.
4. Run C13-C15 consistency checks.
5. Determine verdict.

## Climb-mode adjustment

If user passed `--climb-mode`:
- Skip probabilistic / information-theoretic / dynamical views (too formal for engineering goals).
- Require only inductive bias OR optimization OR an empirical-justification argument.
- Verdict may PASS even if formal theory is absent — intuition + correlation evidence is acceptable.

## Rebuttal loop

The Theorist's attacks here are typically: "what's the inductive bias?", "no convergence argument", "view A contradicts view B", "counterexample regime X breaks the mechanism" (M5). For each attack issued (≥ 1), run the rebuttal loop per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's formal-ish defense. Cite a paper / equation / known result; do not handwave.
2. Theorist persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. WEAKENED → Round 2 (refined), then stop.
4. Max 3 attacks get full rebuttal; additional listed.
5. User-input rebuttal supported (`Source: user`).
6. Cycles use [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade per [../rules/decision-logic.md](../rules/decision-logic.md).

In `--climb-mode`, the Theorist is muted — issue exactly 1 attack with rebuttal (the "where does the mechanism break?" counterexample) and move on.

## Output

Write a `Stage 4` block using `../templates/per-stage-output.md`. Include the 7-view table, the strongest-view paragraph, open questions, and the `Rebuttal-cycle summary`.

## Verdict criteria

- ✅ **PASS** — mechanism articulated; ≥ 1 view supports it consistently.
- ⚠️ **WARN** — intuition exists but not formalized; multi-view check inconsistent.
- ❌ **FAIL** — only "benchmark goes up", no mechanism explanation.

## Stage 4 importance varies by idea type

- Theoretical idea → Stage 4 is critical, formal explanation expected.
- Engineering trick → Stage 4 lighter (intuition + empirical correlation OK).
- Empirical-scaling idea → Stage 4 = "scaling explanation" (e.g., "compute-optimal frontier shifts because …").
