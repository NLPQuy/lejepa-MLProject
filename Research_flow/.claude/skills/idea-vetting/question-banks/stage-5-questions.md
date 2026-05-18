---
name: stage-5-questions
description: Question bank for Stage 5 — Feasibility Analysis (Pragmatic PM persona)
load-trigger: Loaded at start of Stage 5 execution
---

# Stage 5 Question Bank — Feasibility Analysis

Every answer must be a number or a categorical (have / don't-have / risky). Vague answers fail.

## Mandatory: cost (must answer all 4 with numbers)

1. **M1. Compute total**: total GPU-hours or API calls across implementation + tuning + ablation + final eval (not just the headline run).
2. **M2. Wallclock**: days from start to "result table done", assuming serial execution.
3. **M3. Person-hours**: solo or team-hours required.
4. **M4. Dollar cost**: total $ (API + compute rental + data fees) including the 3× factor for tuning + ablation + final.

## Mandatory: significance (must answer all 3)

5. **M5.** Baseline noise `σ`: pp standard deviation across 3 seeds. Use prior data if known; otherwise default ±0.5pp for accuracy metrics.
6. **M6.** Required runs for significance: `K = ceil((2σ / gain)²) + 1`. State the integer.
7. **M7.** Effect size in `σ` units: `gain / σ`. Below 2σ → likely indistinguishable from noise.

## Risks (answer all 4)

8. **R8.** Reproducibility concerns: closed model? non-deterministic kernels? specific hardware?
9. **R9.** Closed-model dependency: does the idea require a specific API model that may be deprecated mid-project?
10. **R10.** Hardware specificity: does the result depend on a specific GPU class (H100 vs A100)?
11. **R11.** Data license issues: is the training/eval data licensed for this use?

## Ablation matrix

12. **A12.** Knobs to sweep: list each hyperparameter that must be ablated.
13. **A13.** Total configurations: `prod(levels per knob)`. State the integer.
14. **A14.** Ablation order: which knob is swept first (the one whose value most-likely changes the conclusion)?

## Failure modes

15. **F15.** If the headline experiment fails, what is the actionable next step? (Specific: "try K=200 instead of K=100", not "iterate".)
16. **F16.** Salvageable insight even on failure? (Can the negative result be published or used to refine the next idea?)
17. **F17.** Within timeline? Compare wallclock × (1 + 0.3 slack) against the user-stated deadline.
18. **F18.** Within team capacity? Person-hours / available person-weeks ≤ 1.0?

## Coverage record

`Questions covered: M1..M7, R8, R10, A12..A14, F15, F17 (13/18)`. Stage 5 cannot pass without all of M1-M7.
