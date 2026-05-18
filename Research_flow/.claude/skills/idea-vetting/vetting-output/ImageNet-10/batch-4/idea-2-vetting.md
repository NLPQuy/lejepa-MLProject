# Idea 2 Vetting — W-MSE Cholesky whitening pre-step before SIGReg
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P5 (Decompose) · Tier: 1
- Proposed gain: +0.5 / +1.2 / +2.5 pp
- Effort: S · Feasibility: 4/5
- Composite: 2.8 (tied top)

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor.*

**Attack A1.1**: "If SIGReg already pulls `Cov(Z) → I` (via Cramér–Wold: every 1-D slice is N(0,1) ⇒ joint is isotropic Gaussian), what does pre-whitening *add*? You're solving the same problem twice."
**Steel-manned rebuttal**: SIGReg's covariance pull is *implicit and MC-noisy*. Whitening makes it *explicit and deterministic*. The decomposition lets SIGReg focus its MC budget on the harder problem (marginal Gaussianity per direction) instead of splitting between covariance flattening + marginal shape.
**Persona response**: ⚠️ WEAKENED — the decomposition story is coherent but the mechanism overlap is real. UNREBUTTED concern: if SIGReg already does (a) covariance and (b) marginals in a single coupled gradient, splitting them off via whitening may *hurt* by removing the variance signal SIGReg needs to learn the projector. **This is a Stage 4 theory issue, not just framing.**

**Verdict**: WARN. **Carry UNREBUTTED concern forward to Stage 4.**

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter.*

**Attack A2.1**: "Whitening Consistently Improves SSL (arXiv:2408.07519, 2024) tested BYOL / SimCLR / SwAV. Crucially, *not JEPA-family*. JEPA without EMA + SIGReg is a different beast — the published deltas don't transfer cleanly."
**Steel-manned rebuttal**: Correct that JEPA wasn't tested in the cited paper, but the mechanism (decorrelate the embedding to ease the downstream linear probe) is method-agnostic. The published deltas (1–5 pp) probably bound the upper end; conservative +1.2 pp mid is honest.
**Persona response**: ⚠️ WEAKENED — the mechanism is method-agnostic *for the linear probe gain*, but JEPA's loss already encodes a covariance constraint (SIGReg) that the SimCLR/BYOL family does not. So the *headroom* whitening provides on JEPA is likely smaller than on those baselines.

**Verdict**: WARN.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "Pre-whitening + JEPA = W-MSE + JEPA composition. C-JEPA (NeurIPS 2024) already combined JEPA with VICReg, which includes a covariance-decorrelation term. Mechanically same family."
**Steel-manned rebuttal**: VICReg's covariance term is a *penalty*; Cholesky-whitening is a *deterministic linear projection*. The two are not equivalent: the penalty trades off with other losses (multi-HP problem LeJEPA was designed to remove); the projection is parameter-free. The novelty is specifically the *projection* (not penalty) for SIGReg.
**Persona response**: ⚠️ WEAKENED. EXTENDS verdict.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1** (carrying forward from Stage 1): "Whitening + SIGReg may be a *double regulariser* on the same axis. Concretely: after `Z_w = L^{-1} Z`, `Cov(Z_w) = I` deterministically. SIGReg's gradient on `Z_w` then has *no covariance signal* to drive — only marginal Gaussianity. But the marginals of `Z_w` are linear combinations of `Z`'s components, weighted by `L^{-1}`'s rows. The *encoder* receives gradient through `L^{-1}` which depends on `Cov(Z)`. The chain `∂L/∂Z = ∂L/∂Z_w · L^{-1}` introduces a coupling that may *destabilise* training when `Cov(Z)` becomes near-singular early on."
**Steel-manned rebuttal**: The `eps` ridge term + EMA on `Cov(Z)` (proposed in the impl sketch) addresses near-singularity. The coupling is well-studied in W-MSE; Ermolov 2021 showed it converges. The added stability of SIGReg-on-prewhitened-Z dominates the chain-rule complexity.
**Persona response**: ❌ **UNREBUTTED** at the deeper concern: even with `eps` + EMA, the *informativeness* of SIGReg's gradient on `Z_w` is reduced — the signal SIGReg uses to *shape the encoder* now has to fight through `L^{-1}`'s dependence on the encoder. W-MSE works *because* it is the *only* regulariser; adding it *on top* of an already-effective regulariser (SIGReg) is theoretically ambiguous. Needs ablation: SIGReg-alone vs W-MSE-alone vs both — and the "both" arm must beat the *max* of the two singletons, not just one.

**Verdict**: FAIL. Theory concern UNREBUTTED. **Stage 4 downgrades the idea's verdict by one level per `rules/decision-logic.md §UNREBUTTED downgrade rule`.**

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "Cholesky on a 384×384 batch covariance is O(d³) = 6e7 ops per step. Negligible. But: batch covariance from B=256 samples in d=384 is *rank-deficient* (rank ≤ 256). Cholesky fails unless ridged generously."
**Steel-manned rebuttal**: The impl sketch already includes `eps = 1e-4` ridge, sufficient for rank-256 covariance in d=384. Alternative: rank-deficient Cholesky via pivoted Cholesky.
**Persona response**: ✅ DEFLECTED.

**Verdict**: PASS.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Two cheaper baselines must run first: (a) SIGReg with **higher M** (1024 → 4096 slices) — same MC-variance reduction story, no whitening required; (b) SIGReg with **larger projector dim** (LeJEPA paper shows projector dim matters more than M). If either dominates, whitening is redundant."
**Steel-manned rebuttal**: Both are good controls but neither addresses the *probe-alignment* angle. The published 1–5 pp gain in arXiv:2408.07519 (2024) was measured *with* methods that already do MC variance reduction. So whitening's gain is *additional* to those controls.
**Persona response**: ⚠️ WEAKENED — the empirical evidence for "additional gain on top of high-M SIGReg" is *not* in the cited paper (those baselines don't do MC slicing). The killer-baseline arms (high-M, large-projector) are mandatory.

**Verdict**: WARN. Falsification must include the high-M SIGReg and large-projector arms.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 WARN · 2 WARN · 3 WARN · 4 **FAIL (UNREBUTTED theory)** · 5 PASS · 6 WARN. UNREBUTTED count = 1 (Stage 4).

**Downgrade rule**: 1 UNREBUTTED → one verdict level down from TOY (the default for 4 WARN + 1 FAIL).

**Verdict**: 🔁 **REFRAME** 🟡

**Reframe direction**: Do **not** ship whitening as a pre-step blindly. First run the **3-arm theory ablation**: (i) SIGReg-only (current baseline), (ii) Whitening-only (no SIGReg — just use Cholesky-whitened embeddings + invariance), (iii) Whitening + SIGReg (proposed). The proposed arm must beat **both singletons** by ≥ 0.4 pp non-overlap. If only beats one singleton, the gain is from that singleton alone — and the reframe is "switch to that singleton, not the combo".

Additionally, the high-M SIGReg control from Stage 6 must rule out "more slices would have given the same lift".

**Confidence**: 🟡 — mechanism is sound but redundancy with SIGReg's existing covariance pull is unresolved by published evidence.

**Composite × confidence**: 2.8 × 0.5 = 1.4 (downgraded — REFRAME, not direct ship).

**Action**: Add the 3-arm theory ablation to the TOY queue at priority 4 (below the surviving TOYs from batch-3). Cost: 3 arms × 3 seeds × 100 ep × 5 GPU-h ≈ 45 GPU-h.
