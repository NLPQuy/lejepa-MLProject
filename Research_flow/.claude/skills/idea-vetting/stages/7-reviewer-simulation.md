---
name: stage-7-reviewer-simulation
description: Simulate peer-review attacks via three reviewer sub-personas
load-trigger: Step 3 of SKILL.md, after Stage 6 (skip if --climb-mode --no-publish)
persona: critical-reviewer (×3 — theoretician / empirical / novelty)
---

# Stage 7: Reviewer Simulation

**Personas**: three reviewers — see [../personas/critical-reviewer.md](../personas/critical-reviewer.md) §Sub-personas. Declare on entry for each:
> "Adopting persona: Reviewer R1 (Theoretician). Stance: default reject — score theory."
> (then) "Adopting persona: Reviewer R2 (Empirical). Stance: default reject — score experiments."
> (then) "Adopting persona: Reviewer R3 (Novelty). Stance: default reject — score delta from prior work."

**Goal**: Mock the peer-review process. Expose the attacks the paper will face.

**Time budget**: 3-5 min.

## Climb-mode behavior

If user passed `--climb-mode --no-publish`: **skip this stage** and proceed to Stage 8.
If user passed `--climb-mode` but NOT `--no-publish`: run a lightweight version focused on R2 (Empirical) only — reproducibility and significance are what matter for an engineering ship.

## Per-reviewer procedure

**Before executing**: load [../question-banks/stage-7-questions.md](../question-banks/stage-7-questions.md). The Q-bank defines T1-T5 (R1 Theoretician), E6-E11 (R2 Empirical), N12-N16 (R3 Novelty), A17-A18 (aggregate + critical fixes). In `--climb-mode` (without `--no-publish`), only R2 runs — answer E6-E11 + A17 + A18. Record coverage IDs in the per-stage output.

For each of R1 / R2 / R3 (or R2 only in climb-mode):
1. Adopt the sub-persona.
2. Answer the Q-bank section for that reviewer (T-, E-, or N- prefixed questions).
3. Score on the reviewer's primary axis (1-5).
4. Write 2-3 specific concerns (cite paper / metric / setting).
5. Decide: Strong Accept / Accept / Borderline / Reject / Strong Reject.
6. After all reviewers, apply A17 (aggregate rule) and A18 (critical fixes list).

## Common attacks per reviewer

### R1 — Theoretician
- "Lacks theoretical justification."
- "Mechanism unproven."
- "No convergence argument."
- "What is the inductive bias actually doing?"

### R2 — Empirical
- "Experimental section incomplete."
- "Need broader comparison."
- "Statistical significance unclear — single seed?"
- "Reproducibility concerns — closed model / no code."
- "Hyperparameters not tuned for baseline."

### R3 — Novelty
- "Weak novelty."
- "Incremental over `<paper>`."
- "Concurrent work `<paper>` overlooked."
- "Only works in narrow setting."

## Aggregated decision

| Pattern | Stage 7 verdict |
|---------|-----------------|
| 3 Accept | ✅ PASS |
| 2 Accept + 1 Borderline | ⚠️ WARN |
| 1 Accept + 2 Borderline | ⚠️ WARN |
| ≥ 2 Reject | ❌ FAIL |

## Rebuttal loop

Reviewer comments are the attacks here. For each reviewer (R1, R2, R3), pick the **single most decisive concern** the reviewer raised and run the rebuttal loop per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's response to that reviewer's concern (this is the "author rebuttal" of the real review process). Cite results, ablations, or specific text-changes the author would make.
2. The reviewer sub-persona (R1/R2/R3) evaluates: ✅ DEFLECTED (the concern is addressed; would flip Borderline → Accept) / ⚠️ WEAKENED (concern partially addressed) / ❌ UNREBUTTED (the concern stands; decision unchanged or worsens).
3. WEAKENED → Round 2, then stop.
4. Up to 3 reviewer concerns get full rebuttal (typically 1 per reviewer). Other concerns listed in the comments without a cycle.
5. User-input rebuttal supported (`Source: user`) — the user often knows how they would actually respond at rebuttal time.
6. Cycles use [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade per [../rules/decision-logic.md](../rules/decision-logic.md).

In `--climb-mode`, only R2's most-decisive concern gets a rebuttal cycle.

## Output

Write a `Stage 7` block using `../templates/per-stage-output.md`. Include three sub-sections (R1, R2, R3) each with score / comment / decision, then an **Aggregated** row, a **Critical fixes** bullet list (changes that would flip Borderline → Accept), and the `Rebuttal-cycle summary`.

## No early-exit

Stage 7 result feeds Stage 8 synthesis. Stage 7 FAIL alone does not auto-KILL; Stage 8 weighs it against the other stages per `../rules/decision-logic.md`.
