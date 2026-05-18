---
name: stage-7-questions
description: Question bank for Stage 7 — Reviewer Simulation (R1/R2/R3 sub-personas)
load-trigger: Loaded at start of Stage 7 execution (skip if --climb-mode --no-publish)
---

# Stage 7 Question Bank — Reviewer Simulation

Three reviewers; each must produce a score (1-5), a comment, and a decision (Strong Accept / Accept / Borderline / Reject / Strong Reject).

## R1 — Theoretician (must answer all 5)

1. **T1.** Is the theoretical contribution clear? Name the specific theoretical claim.
2. **T2.** Soundness: are the claims correctly stated and not over-reaching the evidence?
3. **T3.** Open theoretical concerns: list ≥ 2 (proofs missing, assumptions unstated, generalization to non-stated regimes).
4. **T4.** R1 score: 1 (worst) to 5 (best) on theoretical contribution.
5. **T5.** R1 decision: Strong Accept / Accept / Borderline / Reject / Strong Reject.

## R2 — Empirical (must answer all 6)

6. **E6.** Experimental design adequate? Comment on dataset, splits, sample size.
7. **E7.** Baselines fair? Tuned for the same compute? Adequate range?
8. **E8.** Statistical significance: number of seeds, reported variance, significance test used?
9. **E9.** Reproducibility: code released? hyperparameters fully specified? hardware noted?
10. **E10.** R2 score: 1-5.
11. **E11.** R2 decision.

## R3 — Novelty (must answer all 5)

12. **N12.** Novelty score: 1-5 across the 8 axes from Stage 3.
13. **N13.** Related-work coverage: are the most-relevant 5-10 prior papers cited and contextualized?
14. **N14.** Incremental flag: is this an incremental improvement (workshop-tier) or a substantive contribution (main-track)?
15. **N15.** R3 score: 1-5.
16. **N16.** R3 decision.

## Aggregate (must answer both)

17. **A17.** Combined decision using the rule below:
    - 3 Accept → ✅ PASS
    - 2 Accept + 1 Borderline → ⚠️ WARN
    - 1 Accept + 2 Borderline → ⚠️ WARN
    - ≥ 2 Reject → ❌ FAIL
18. **A18.** Critical fixes before resubmission: list 2-4 concrete changes that would flip any Borderline → Accept (e.g., "add convergence proof for the inner loop", "run 5 seeds and report std").

## Climb-mode (--climb-mode without --no-publish)

Run only R2 (Empirical). Skip R1 and R3. Map R2's decision directly to the Stage 7 verdict. If `--climb-mode --no-publish`, the whole stage is skipped per `SKILL.md`.

## Coverage record

`Questions covered: T1..T5, E6..E11, N12..N16, A17, A18 (18/18)`. Full mode requires all 18; climb-mode requires E6-E11 + A17 + A18.
