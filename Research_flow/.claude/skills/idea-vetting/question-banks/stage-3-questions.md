---
name: stage-3-questions
description: Question bank for Stage 3 — Novelty Decomposition (Critical Reviewer persona)
load-trigger: Loaded at start of Stage 3 execution
---

# Stage 3 Question Bank — Novelty Decomposition

Pinpoint exactly which of the 8 novelty axes are claimed and which survive the rebranding test.

## Mandatory: 8-axis applicability (must mark each ✅/⚠️/❌ with citation)

1. **M1. Axis 1 — Novel objective**: Is the loss / training criterion new? Cite prior work that used the same objective.
2. **M2. Axis 2 — Novel architecture**: New module, layer, or connectivity? Cite the closest existing module.
3. **M3. Axis 3 — Novel optimization**: New optimizer, scheduler, or training trick? Cite the existing optimization equivalent.
4. **M4. Axis 4 — Novel theoretical framing**: New analysis, bound, or principle? Cite prior theory in the same vicinity.
5. **M5. Axis 5 — Novel empirical finding**: Demonstrating X works where unknown, or a new scaling law? Cite the closest existing empirical claim.
6. **M6. Axis 6 — Novel application**: New technique-domain pairing (e.g., MCTS → math reasoning)? Cite both the technique's origin domain and any prior transfer attempts.
7. **M7. Axis 7 — Novel evaluation**: New metric or protocol? Cite the closest existing eval.
8. **M8. Axis 8 — Novel synthesis**: New combination not previously explored? Cite each component plus any prior combination attempts.

## Rebranding test (must run all 4)

9. **R9. Renaming check**: Is this an existing method with a new name? (Try to map idea terms back to prior-paper terms.)
10. **R10. Module-swap check**: Is the only change moving a module from position A to position B in an existing architecture?
11. **R11. Notation-change check**: Is the math identical to prior work under a change of variables?
12. **R12. Hyperparameter-tune check**: Is the "novelty" just a different hyperparameter choice that the prior paper did not sweep?

## Strip test

13. **S13. Strip test**: Remove the claimed novel parts. Does the remainder produce the same result? Answer one of:
    - "No, synergy exists" → axis is genuine
    - "Partial, weaker but non-zero" → axis is incremental
    - "Yes, same result" → axis is illusory

## Defensibility

14. **D14.** Is this publishable as a standalone contribution at an A* venue (NeurIPS / ICML / ICLR / ACL / EMNLP / CVPR)?
15. **D15.** If not A*, what venue tier IS it defensible at? Workshop? Engineering report? Tech blog only?
16. **D16.** Will this stand on its own as a citation-worthy paper in 3 years, or is it only useful as part of a larger system?
17. **D17.** Would this survive Stage 7's R3 (novelty reviewer)? If R3's likely verdict is Reject → Stage 3 cannot PASS.

## Coverage record

`Questions covered: M1..M8, R9..R12, S13, D14, D15, D17 (16/17)`. Stage 3 cannot pass with fewer than the 8 mandatory axis checks plus the strip test.
