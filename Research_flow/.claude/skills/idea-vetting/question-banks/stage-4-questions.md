---
name: stage-4-questions
description: Question bank for Stage 4 — Theory Grounding (Theorist persona)
load-trigger: Loaded at start of Stage 4 execution
---

# Stage 4 Question Bank — Theory Grounding

Test "why should this work" beyond "benchmark goes up". Strong ideas pass ≥ 2 views consistently.

## Mandatory: mechanism (must answer all 5)

1. **M1.** Why should this work? Give a 1-2 sentence mechanism in plain words.
2. **M2.** What specific failure mode of the baseline is the mechanism fixing? Cite the failure.
3. **M3.** What is the predicted optimization behavior? (Faster convergence? Smoother loss? Lower variance?)
4. **M4.** Is the mechanism falsifiable? Name an observation that would disprove it.
5. **M5.** Counterexample: name a regime where the mechanism would predict failure. (If the mechanism predicts the idea always works, it is unfalsifiable → WARN.)

## Views (attempt each — mark ✅ applies / ⚠️ weak / ❌ N/A)

6. **V6. Inductive bias view**: what bias does the method impose on the function class?
7. **V7. Optimization view**: what does it do to the loss landscape / training dynamics?
8. **V8. Probabilistic view**: Bayesian / MAP / MLE interpretation?
9. **V9. Information-theoretic view**: mutual information, compression, channel capacity?
10. **V10. Geometric view**: manifold, distance, projection?
11. **V11. Dynamical-systems view**: fixed point, attractor, stability?
12. **V12. Capacity view**: does the method need more or less effective capacity?

## Consistency tests

13. **C13.** Are the applicable views internally consistent? (If view V6 predicts behavior X and view V8 predicts ¬X, the mechanism is incoherent.)
14. **C14.** Multi-view check: does the idea pass ≥ 2 views? Single view → MODERATE; multi-view consistent → STRONG.
15. **C15.** Empirical-only acceptable? If user goal is engineering / climb-mode AND ≥ 1 view holds, an absence of formal theory is OK. If user goal is paper publication AND only 1 view holds → Stage 4 = WARN.

## Climb-mode shortcut

If `--climb-mode`: only **M1**, **M2**, **M3**, **V6** OR **V7**, and **C14** are required. Skip V8-V11 and the formal-theory threshold.

## Coverage record

`Questions covered: M1..M5, V6, V7, V12, C13, C14 (10/15)`. Stage 4 cannot pass with fewer than M1, M2, M4, and ≥ 1 view.
