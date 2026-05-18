---
name: killed-ideas
type: append-only
---
# Killed ideas — ImageNet-10
<!-- entries appended below -->

## 2026-05-18

### Batch 1 — ImageNet-10

#### Idea 5: Kernelize SIGReg projections (RKHS slicing)
- Killed-at: Stage 4 (Theory) + Stage 6 (Killer Baseline) — both UNREBUTTED
- Killing-attack: (a) Applying nonlinear φ to Z makes SIGReg target Gaussianity of φ(Z), not Z itself → LeJEPA's Cramér-Wold + isotropic-optimality theorems no longer apply. (b) Stacking two linear univariate tests (Anderson-Darling + Epps-Pulley) preserves the guarantee and dominates RFF-SIGReg both theoretically and computationally.
- Evidence: LeJEPA paper §3 (theorem on N(0,I) downstream optimality requires Z, not φ(Z)); `lejepa.univariate` already exposes Anderson-Darling.
- Salvageable: YES — propose *combine-multiple-univariate-tests* as a new idea in the next batch.
- Confidence: 🟡 (theory argument strong; empirical disproof not run).
- Source: ideation batch-1, primary citation Kernel-VICReg arXiv:2509.07289.
- Resurrection-eligible: only if user demonstrates a specific non-Gaussian failure mode that no linear univariate test catches.

## 2026-05-18 — Batch 6 — ImageNet-10
*No KILL verdicts this batch.* Idea 6 (PH H₀ regularizer) is REFRAMED to near-KILL (archive; resurrection-eligible only with 32-d projection or PH₁ variant + gradient-norm sanity pass at d=384 — see batch-6/idea-6-vetting.md §Resurrection-eligible).
