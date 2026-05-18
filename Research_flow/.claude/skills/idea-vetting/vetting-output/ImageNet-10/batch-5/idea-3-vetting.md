# Idea 3 Vetting — MMCR auxiliary (manifold-capacity volume loss)
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P1 (Combine — auxiliary loss) · Tier: 3 (theoretical neuroscience — Chung-Sompolinsky)
- Proposed gain: +0.4 / +1.0 / +2.2 pp
- Effort: M · Feasibility: 4/5
- Composite (batch-5): 2.5

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor. Stance: does MMCR target a real bottleneck of SIGReg-only training?*

**Attack A1.1**: "SIGReg already constrains the embedding *distributionally*; manifold-volume is an indirect consequence. Adding MMCR may be redundant."
**Steel-manned rebuttal**: SIGReg constrains marginal Gaussianity per slice; the per-image augmentation-manifold compactness is a *higher-order* property not captured by 1-D marginals. MMCR's two-term `−tr(σ_+) + β·tr(σ_−)` is on the spectrum of the per-image SVD, which has zero overlap with per-slice goodness-of-fit.
**Persona response**: ⚠️ WEAKENED — the "zero overlap" claim is too strong. Both objectives bias toward `Cov(Z) ≈ I` indirectly (SIGReg via marginal isotropy, MMCR via batch-wide nuclear norm). The redundancy is plausible.

**Verdict**: WARN. Reframe needed.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter.*

**Attack A2.1**: "MMCR (arXiv:2303.03307) was *already proposed* as an SSL objective. Adding it on top of LeJEPA isn't novel — it's stacking two known SSL methods."
**Steel-manned rebuttal**: arXiv:2303.03307 uses MMCR *alone* and compares to SimCLR/BYOL. No published instance of MMCR + JEPA-style loss. The combination is novel; the constituents are not.
**Persona response**: ✅ DEFLECTED. EXTENDS, not DUPLICATE.

**Verdict**: PASS. Novelty: EXTENDS.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "Combining two known losses with a new α weight. Engineering plus HP tune."
**Steel-manned rebuttal**: The mechanistic claim — that MMCR's manifold-geometric signal is *orthogonal* to SIGReg's distributional signal — is a measurable empirical question that has not been answered. The α=0 ablation is a real mechanism test.
**Persona response**: ⚠️ WEAKENED — climb-mode admits this; paper venue would push back on novelty.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1**: "Manifold-capacity theory is asymptotic-d / replica-symmetric — does it transfer cleanly to d=384, ViT-S, 13k-image dataset?"
**Steel-manned rebuttal**: Yerxa et al. 2023 explicitly applies MMCR at ResNet-50 / d=128 / IN1K and shows it matches SimCLR. The d=384 case is *more* favourable for the asymptotic theory. Empirical transfer is demonstrated.
**Persona response**: ✅ DEFLECTED.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "MMCR needs ≥ 4 augmented views per anchor. Current pipeline has 2 global + 6 local. The local views are smaller resolution (98×98 vs 224×224); using them in the same per-image-SVD is dimensionally awkward."
**Steel-manned rebuttal**: All views share the encoder; their embeddings are all in R^d. The SVD is on embeddings, not pixels — resolution mismatch doesn't matter. Just use the 6 local views as the per-image manifold.
**Persona response**: ✅ DEFLECTED. Cleanly resolved.

**Verdict**: PASS.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Per batch-4 W-MSE reframe: redundancy-with-SIGReg is the recurring skill-drift symptom. MMCR's batch-nuclear-norm pull and SIGReg's marginal-Gaussianity pull *both* implicitly push `Cov(Z) → I`. Theory ablation mandatory: 3-arm (SIGReg-only / MMCR-only / SIGReg+MMCR). Combo must beat **both** singletons by ≥ 0.4 pp non-overlap."
**Steel-manned rebuttal**: The redundancy is at the second-order moment level only; MMCR additionally regulates the per-image *spectrum* (singular values), which SIGReg ignores. The 3-arm ablation will measure exactly this — if combo > both singletons, the orthogonality claim is validated; if not, drop MMCR.
**Persona response**: ⚠️ WEAKENED but procedurally addressed. The 3-arm ablation is the right answer; the question is just whether it's a pre-flight or a final-experiment design.

**Refinement (Round 2)**: 3-arm ablation is *mandatory pre-commitment* — same disposition as batch-4 W-MSE reframe. Combo arm must beat *both* singletons or MMCR is dropped (or switched to the winning singleton).

**Verdict**: FAIL (pre-flight required) → PASS (with mandatory 3-arm reframe).

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 WARN · 2 PASS · 3 WARN · 4 PASS · 5 PASS · 6 FAIL→PASS-w-reframe · UNREBUTTED = 0.

**Verdict**: 🔁 **REFRAME** 🟡

**Confidence**: 🟡 — strong T3 cross-domain source (Chung-Sompolinsky); MMCR alone has published evidence; combination with SIGReg has plausible orthogonality but is the same skill-drift symptom that caught W-MSE in batch-4.

**Reframe direction**: **Mandatory 3-arm theory ablation before any FULL SEND**: (i) SIGReg-only baseline; (ii) MMCR-only (no SIGReg) at matched compute; (iii) SIGReg + MMCR at best α. Combo must beat **both singletons** by ≥ 0.4 pp non-overlap. If only beats one, adopt that singleton and drop the combo. Add an α=0 mechanism arm. Reframed cost: 4 arms × 3 seeds × 100 ep ≈ 60 GPU-h — same shape as batch-4 W-MSE reframe.

**Composite × confidence**: 2.5 × 0.7 = 1.75.

**Ship-now action**: queue after batch-2 ASHA + batch-3 SRHT lands; share the W-MSE-reframe experimental slot.
