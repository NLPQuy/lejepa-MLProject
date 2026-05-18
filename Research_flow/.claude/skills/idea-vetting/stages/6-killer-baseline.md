---
name: stage-6-killer-baseline
description: Find a simple baseline that could match or beat the idea
load-trigger: Step 3 of SKILL.md, after Stage 5
persona: skeptical-empiricist
---

# Stage 6: Killer Baseline Check

**Persona**: Skeptical Empiricist — see [../personas/skeptical-empiricist.md](../personas/skeptical-empiricist.md). Declare on entry:
> "Adopting persona: Skeptical Empiricist. Stance: baseline wins until proven otherwise — did you actually tune the baseline?"

**Goal**: Identify ≥ 3 simple baselines that could match or beat the idea. This is the most-painful stage (kills favorite ideas) and the highest-value (saves compute).

**Time budget**: 2-3 min.

## Standard baseline catalog (consider each — pick relevant ones)

- **Self-consistency K=N** (for LLM ideas)
- **Best-of-K** with simple verifier
- **Standard CoT** without proposed tricks
- **Larger backbone** (next size up)
- **Longer training** (epochs × 2)
- **EMA / SWA** weight averaging
- **Better hyperparameter sweep** (proper grid, not the paper's defaults)
- **More data / synthetic data**
- **Stronger augmentation** (mixup / cutout / RandAug)
- **Tool-use** (calculator, code-exec) — for reasoning ideas
- **Retrieval baseline** — for tasks with a knowledge dimension
- **Ensemble of cheap models**

## Procedure

**Before executing**: load [../question-banks/stage-6-questions.md](../question-banks/stage-6-questions.md). The Q-bank defines B1-B12 (the 12-baseline catalog), C13-C15 (per-baseline comparison: cost ratio, gain delta, KILLER flag), K16-K18 (killer-baseline action). Every baseline must have an estimated pp gain AND a cost-vs-idea estimate. Record coverage IDs in the per-stage output.

1. From the B1-B12 catalog, mark applicability (✅/❌). Pick the 3-5 most relevant ✅ baselines for this idea.
2. For each ✅ baseline, answer C13 (cost ratio) and C14 (gain delta) with numbers.
3. Apply C15 to flag KILLER baselines.
4. Apply K16-K18 to decide PASS / WARN / FAIL.
5. Issue specific attacks (templates below).
6. Determine verdict.

## Specific attack templates

- "Did you compare to SC K=100? On adjacent benchmarks it gets `<X>`pp."
- "Did you tune the baseline for the same compute as the idea?"
- "What about Tool-use (e.g., Python exec for math)? It is cheaper and often beats reasoning tricks."
- "What about just `<simpler baseline>` — has anyone shown it loses?"
- "Just scale the baseline 2× — does the idea still win?"

## Rebuttal loop

For each ≥ 1 KILLER baseline flagged (and for the 2-3 close-call baselines if no KILLER), run the loop per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md):
1. **Steel-manned rebuttal** — the idea author's argument why the idea wins over (or super-adds with) the baseline. Must include estimated pp numbers, not vague "ours captures something extra".
2. Empiricist persona evaluates: ✅ DEFLECTED / ⚠️ WEAKENED / ❌ UNREBUTTED.
3. WEAKENED → Round 2 (refined: e.g., "combined version of idea + baseline shows super-additivity in toy"), then stop.
4. Max 3 baselines get the full rebuttal; the rest are listed in the table without a cycle.
5. User-input rebuttal supported (`Source: user`).
6. Cycles use [../templates/rebuttal-format.md](../templates/rebuttal-format.md).
7. Apply UNREBUTTED-downgrade per [../rules/decision-logic.md](../rules/decision-logic.md).

A KILLER baseline that stays UNREBUTTED across both rounds → Stage 6 = FAIL → early-exit to Stage 8 KILL or REFRAME.

## Output

Write a `Stage 6` block using `../templates/per-stage-output.md`. Include the baselines table (Baseline / Cost vs idea / Expected gain / Status), the KILLER count, and the `Rebuttal-cycle summary`.

## Verdict criteria

- ✅ **PASS** — no simple baseline matches/beats the idea.
- ⚠️ **WARN** — a close baseline exists; the idea must show a clear delta in ablation.
- ❌ **FAIL** — a simple baseline beats the idea → KILL or reframe as "X combined with idea" (only if combined version provably > each alone).

## Early-exit

If Stage 6 = FAIL → skip Stage 7; go to Stage 8 with verdict `KILL` (or `REFRAME` if a combined version is plausible). Log the killing baseline.
