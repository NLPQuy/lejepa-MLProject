---
name: stage-6-questions
description: Question bank for Stage 6 — Killer Baseline (Skeptical Empiricist persona)
load-trigger: Loaded at start of Stage 6 execution
---

# Stage 6 Question Bank — Killer Baseline

Every baseline must have an **estimated pp gain** and **estimated cost relative to the idea**. Vague "have you tried X" is forbidden.

## Mandatory: standard baseline catalog (consider each relevant entry)

For each baseline below, output: applicable? (✅/❌), estimated cost vs idea (cheaper / similar / more), estimated gain (pp), status (PASS / CLOSE / KILLER).

1. **B1. Self-Consistency K=N** (for LLM ideas — pick a relevant N).
2. **B2. Best-of-K** + simple verifier prompt.
3. **B3. Standard CoT** without the idea's proposed tricks.
4. **B4. Larger backbone** (next size up — e.g., gpt-4o-mini → gpt-4o).
5. **B5. Longer training / more epochs** (× 2).
6. **B6. EMA / SWA** (exponential moving average of weights).
7. **B7. Properly-tuned hyperparameter sweep** (full grid, not the paper defaults).
8. **B8. More data** (synthetic or additional human-labeled).
9. **B9. Stronger augmentation** (mixup / cutout / RandAug).
10. **B10. Tool-use** (calculator / Python exec / formal-verification tool).
11. **B11. Retrieval baseline** (kNN-retrieved exemplars or RAG).
12. **B12. Ensemble of cheap models**.

## Mandatory: per-baseline comparison (must run for each ✅-applicable baseline)

13. **C13.** Compute cost ratio: `cost(baseline) / cost(idea)`. State as fraction (e.g., `0.05` = baseline is 20× cheaper).
14. **C14.** Estimated gain delta: `gain(idea) - gain(baseline)` in pp. Negative → baseline beats idea.
15. **C15.** Killer flag: if `gain(baseline) >= gain(idea)` AND `cost(baseline) <= cost(idea)` → tag as KILLER.

## Killer-baseline action

16. **K16.** How many KILLER baselines identified?
17. **K17.** If ≥ 1 KILLER:
    - Can the idea be reframed as "KILLER + idea" with super-additivity demonstrated? If yes → REFRAME candidate.
    - If no plausible combination → Stage 6 = FAIL → likely KILL at Stage 8.
18. **K18.** If 0 KILLER but ≥ 1 baseline within 0.5pp of idea's claimed gain → Stage 6 = WARN — the idea must show a clear delta in ablation.

## Coverage record

`Questions covered: B1, B3, B4, B10, B11 (applicable subset), C13..C15, K16, K17 (9/18)`. Stage 6 cannot pass with fewer than 3 baselines actually estimated.
