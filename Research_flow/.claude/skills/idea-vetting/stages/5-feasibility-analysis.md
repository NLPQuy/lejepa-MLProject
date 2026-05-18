---
name: stage-5-feasibility-analysis
description: Stress-test feasibility beyond the basic check the ideation skill already did
load-trigger: Step 3 of SKILL.md, after Stage 4
persona: pragmatic-pm
---

# Stage 5: Feasibility Analysis (extended)

**Persona**: Pragmatic PM — see [../personas/pragmatic-pm.md](../personas/pragmatic-pm.md). Declare on entry:
> "Adopting persona: Pragmatic PM. Stance: numerical — give me exact numbers or descope."

**Goal**: Identify infeasibility BEFORE the user commits compute and person-time.

**Time budget**: 2-3 min.

## 8 feasibility dimensions

1. **Compute total** — including hyperparameter tuning, ablation, final eval (not just headline run).
2. **Data** — availability, license, preprocessing complexity.
3. **Wallclock** — time to implement + experiment + write up.
4. **Person-hours** — solo or team effort needed.
5. **Reproducibility** — closed-model dependency? hardware-specific?
6. **Statistical significance** — is the expected gain ≥ noise level?
7. **Ablation complexity** — how big is the config matrix?
8. **Failure debugging** — if it fails, is there an actionable next step?

## Procedure

**Before executing**: load [../question-banks/stage-5-questions.md](../question-banks/stage-5-questions.md). The Q-bank defines M1-M4 (cost numbers), M5-M7 (significance), R8-R11 (risks), A12-A14 (ablation matrix), F15-F18 (failure modes). Every answer must be a number or a categorical — vague answers fail. Record coverage IDs in the per-stage output.

1. Answer M1-M4 with numbers (compute, wallclock, person-hours, dollars).
2. Compare against the user's stated budget (compute, time, person-hours, deadline) — F17, F18.
3. Estimate **statistical significance** via M5-M7 (formula below).
4. Sketch the ablation matrix: A12-A14 — knobs × levels = total config count × per-config cost.
5. Run R8-R11 risk checks.
6. Issue ≥ 2 attack templates below; steel-man rebuttals.
7. Determine verdict.

## Attack templates

- "Need `<X>` GPU-hours for +`<Y>`%? Not worth."
- "Too many moving parts — reviewers will destroy this."
- "You need `<data>`, but you don't have it (or the license blocks it)."
- "Variance is ±`<σ>`pp; your gain `<g>` is within noise."
- "This depends on `<closed model>` — they might deprecate it mid-project."
- "Ablation matrix is `<K>×<L>×<M>` = 30-day sweep."

## Statistical-significance formula

- Baseline noise `σ` ≈ seed-variance of baseline (estimate from 3-seed baseline if known; otherwise assume ±0.5pp on accuracy metrics).
- Gain `g` must be ≥ 2σ to be detectable in a single run.
- Required runs `K ≈ (2σ / g)²` (round up; add 1-run margin).

## Rebuttal loop

For each of the ≥ 2 numeric attacks issued (cost overrun / variance / closed-model dep / ablation matrix size), run the loop per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's plan to descope or recover. Must include **numbers** (e.g., "running just 3 of the 9 ablation configs cuts cost to $100 and still resolves the K-vs-N question"), not "we can probably make it work".
2. PM persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. WEAKENED → Round 2 (refined descope plan), then stop.
4. Max 3 attacks get full rebuttal.
5. User-input rebuttal supported (`Source: user`); the user often has access to cost details the PM does not.
6. Cycles use [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade per [../rules/decision-logic.md](../rules/decision-logic.md).

## Output

Write a `Stage 5` block using `../templates/per-stage-output.md`. Include the resource-estimate table, the significance row, the ablation matrix, and the `Rebuttal-cycle summary`.

## Verdict criteria

- ✅ **PASS** — feasible within budget; statistical significance achievable in K ≤ planned runs.
- ⚠️ **WARN** — feasible but tight; recommend descope.
- ❌ **FAIL** — cost > budget × 2, OR gain < noise × 2, OR wallclock > deadline × 1.5.
