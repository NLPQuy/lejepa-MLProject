# Idea 5 Vetting — SIE-style invariant + equivariant split predictor
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P5 (Decompose — split embedding into invariant + equivariant subspaces) · Tier: 1
- Proposed gain: +0.3 / +0.9 / +1.8 pp
- Effort: M · Feasibility: 4/5
- Composite (batch-5): 2.5

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor.*

**Attack A1.1**: "Predicting augmentation parameters wastes capacity that could go to invariant features — the *only* thing the linear probe uses."
**Steel-manned rebuttal**: Wang et al. 2026 (arXiv:2503.18753) measure that equivariance-coherence *improves* downstream invariant-linear-probe by ~1 pp — the augmentation-prediction signal *removes* augmentation-coding noise from the invariant subspace (which is otherwise where it leaks). Decomposition makes z_inv cleaner, not noisier.
**Persona response**: ✅ DEFLECTED. The 2026 paper is direct evidence.

**Verdict**: PASS.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter.*

**Attack A2.1**: "SIE (Garrido-Najman-LeCun 2023) is already the method. Idea 5 is just porting SIE to LeJEPA — that's an implementation note, not a research idea."
**Steel-manned rebuttal**: SIE was demonstrated on VICReg/SimCLR, not on JEPA-style invariance. The mechanism transfer is plausible but unmeasured — SIGReg's slicing geometry interacts non-trivially with the equivariant subspace (Cramér-Wold on the equivariant subspace is a non-trivial claim). And the 2026 follow-up adds equivariance-coherence as a separate technique.
**Persona response**: ⚠️ WEAKENED — the SIE method exists; the LeJEPA-specific composition is the novel angle, climb-mode admissible.

**Verdict**: PASS. Novelty: EXTENDS.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "Method-port from VICReg/SimCLR setting to LeJEPA setting. Engineering."
**Steel-manned rebuttal**: The empirical question — "does equivariance-coherence improve LeJEPA linear probe on Imagenette?" — has not been answered. Engineering-and-measurement is admissible in climb-mode.
**Persona response**: ⚠️ WEAKENED.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1**: "Applying SIGReg to BOTH z_inv and z_eq independently doubles the regulariser. If SIGReg's strength λ is unchanged, the effective regularisation per subspace is *halved*. Compensating by doubling λ over-regularises."
**Steel-manned rebuttal**: SIGReg on each subspace at the original λ enforces Gaussianity per subspace independently; the joint distribution is then product-Gaussian, which is *exactly* what an isotropic Gaussian is on the concatenated space (per Cramér-Wold, equivalent to enforcing it on the joint). No double-regularisation.
**Persona response**: ✅ DEFLECTED. The product-Gaussian argument is correct.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "Augmentation-parameter bookkeeping requires refactoring the Compose pipeline to return (image, Δ-dict). Across rotation/jitter/blur/crop that's 4 typed parameters with different scales. Real eng effort."
**Steel-manned rebuttal**: stable-pretraining already supports dict-data flow (per CLAUDE.md §stable-pretraining). Adding a `params` key alongside `image` is a single refactor; the augmentation classes already know their parameters internally.
**Persona response**: ⚠️ WEAKENED — the refactor is real but standard; M-effort is honest. The MSE-on-mixed-scale-parameters issue (rotation degrees vs jitter probability vs blur σ) needs scale normalisation but is easy.

**Verdict**: PASS. Cost ~30 GPU-h (1 run × 3 seeds × ~10 GPU-h each), + 2 days eng for the refactor.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Standard ablation: does the equivariance head help vs just *doubling the projector head dim* at no equivariance loss? Maybe the gain is from capacity, not from decomposition."
**Steel-manned rebuttal**: This is exactly the mechanism check in the idea's falsification: linear probe on z_full should be *lower* than on z_inv. If z_full ≥ z_inv, the decomposition collapsed and the gain is from capacity. The check is built-in.
**Persona response**: ✅ DEFLECTED — but the actual experiment design needs a "matched-d invariant-only" arm too. 3-arm: baseline / SIE-split (z_inv probe) / matched-d-invariant-only (d=256, same as z_inv). If matched-d-invariant beats baseline by similar margin, the gain is from regularisation balance, not equivariance.

**Refinement (Round 2)**: Add matched-d-invariant arm. 3-arm experiment: baseline (d=384, full invariance) / SIE-split (d=256+128, probe on d=256) / matched-d-invariant (d=256, full invariance). Cost: +1 arm.

**Verdict**: PASS with refinement.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 PASS · 2 PASS · 3 WARN · 4 PASS · 5 PASS · 6 PASS-w-refinement · UNREBUTTED = 0.

**Verdict**: ✅ **FULL SEND** 🟢

**Confidence**: 🟢 — direct published evidence on the eval metric (Wang 2026 arXiv:2503.18753); LeCun-lab provenance via SIE; clean composition with SIGReg (product-Gaussian); built-in decomposition-collapse check + matched-d-control.

**Refinement applied**: experiment includes matched-d-invariant arm (3-arm total).

**Composite × confidence**: 2.5 × 1.0 = 2.5.

**Ship-now action**: After Step-0 ASHA returns (λ, lr, wd), run SIE-split as a 3-arm experiment alongside Idea 6 (saliency crops) — both head-side / data-side changes are orthogonal to the SIGReg numerics stack.
