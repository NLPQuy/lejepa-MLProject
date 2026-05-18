# Idea 1 Vetting — Spherical t-design deterministic slice quadrature
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P3 (Replace — slice sampler) · Tier: 3 (numerical analysis / discrete geometry on sphere)
- Proposed gain: +0.1 / +0.5 / +1.2 pp
- Effort: S · Feasibility: 4/5
- Composite (batch-5): 2.4

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor. Stance: is deterministic exact-poly integration the bottleneck on ImageNet-10?*

**Attack A1.1**: "The SIGReg MC variance at M=1024 in d=384 is already small; on a 10-class 13k-image dataset the binding constraint is signal-per-epoch, not estimator variance. t-design improves the wrong dial."
**Steel-manned rebuttal**: Lower estimator variance translates to lower gradient noise → faster early-epoch convergence on small data. Batch-3 SRHT and batch-4 Repulsive both bet on the same dial; this idea is the deterministic-corner of that bet. On 100-ep budgets, early-epoch noise *does* bind.
**Persona response**: ⚠️ WEAKENED — the "deterministic corner" framing is defensible, but the bet is now 4-deep in the same family. Marginal value of a fourth VR mechanism is low unless the prior three failed.

**Verdict**: WARN. Framing OK; family-saturation is a real concern.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter. Stance: has anyone applied spherical t-designs to sliced-Wasserstein-like estimators?*

**Attack A2.1**: "QSW (arXiv:2309.11713) already uses QMC point sets on S^(d−1) for sliced-Wasserstein; t-designs are a special case of low-discrepancy constructions. Likely duplicate."
**Steel-manned rebuttal**: QSW is restricted to 3D in published form and uses Sobol-on-sphere / spiral points — not actual t-designs. t-designs give *exact* polynomial integration, which is qualitatively distinct from "low discrepancy". No published SSL application of t-designs to slice sampling.
**Persona response**: ✅ DEFLECTED. EXTENDS QSW + Tropp SRHT, not a duplicate.

**Verdict**: PASS. Novelty: NOVEL within SIGReg context.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer. Stance: novel = (t-designs) + (SIGReg slicing) — engineering or research?*

**Attack A3.1**: "Drop-in slice sampler swap. Engineering."
**Steel-manned rebuttal**: Empirical claim is the 4-way head-to-head of slice-generation strategies in SSL — first such comparison. The cross-domain transfer (Annals of Math discrete geometry → SSL slicing) has educational value even if the mechanism is "swap the sampler".
**Persona response**: ⚠️ WEAKENED — climb-mode admits engineering-and-measurement; paper-mode would not.

**Verdict**: WARN. Novelty: EXTENDS (composition).

## Stage 4 — Theory Grounding (lite, --climb-mode)
*Adopting persona: Theorist. Stance: is the Cramér-Wold claim preserved?*

**Attack A4.1**: "A *fixed* deterministic t-design is a set of M directions; uniform-over-sphere is achieved only in the population-marginal sense after random rotation. Without rotation, the per-step Cramér-Wold guarantee is lost."
**Steel-manned rebuttal**: Idea explicitly mitigates with random rotation per epoch. Random R ∈ SO(d) of a t-design is still a t-design (rotation invariance of polynomial integration on S^(d-1)), AND the rotation distribution averages directional bias to zero in the population limit. So CW preserved.
**Persona response**: ✅ DEFLECTED. The mitigation is correct and is in the idea text.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM. Stance: t-design table generation cost?*

**Attack A5.1**: "Generating a *true* spherical t-design at (d=384, t≥4, M=1024) is non-trivial; the asymptotic Bondarenko bound `M ≥ c·t^(d−1)` is meaningless at d=384. Womersley's constructions are tabulated for d=3, d=4, occasionally d=5. There may not exist a usable construction at d=384."
**Steel-manned rebuttal**: For *low t* (t=2 or t=4), explicit constructions via SDP-relaxation of the spherical-harmonic moments are tractable up to moderate d. Alternatively, use a "weighted t-design" — relax equal-weight to optimised-weight, much easier numerically. Fall-back position: t=2 (exact integration of 2nd-order moments) is trivial via orthonormal frames.
**Persona response**: ⚠️ WEAKENED — t=2 exact integration is achieved by ANY orthonormal frame with M=d points; the "spherical t-design" framing is overkill for t=2. The interesting case (t=4+) is genuinely uncertain in feasibility at d=384.

**Verdict**: WARN. Cost = unknown for t≥4; for t=2 it's a trivial orthonormal frame (which is just batch-3's SRHT in disguise — partial duplication risk).

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist. Stance: SRHT / Repulsive / Antithetic+SH-CV already cover this dial; what does t-design add?*

**Attack A6.1**: "Cumulative variance-reduction stack is SRHT (batch-3, FULL SEND) + Antithetic+SH-CV (batch-4, TOY) + Repulsive (batch-4, REFRAME). Three independent VR mechanisms. If SRHT (the FULL SEND) achieves the published 20-40% variance reduction on SIGReg, the marginal value of t-design is ~0. Dominated."
**Steel-manned rebuttal**: SRHT and Antithetic are *stochastic* VR with asymptotic variance bounds; t-design is *deterministic* with zero variance up to polynomial degree t. The mechanisms are not strictly nested. The 4-way A/B/C/D experiment is the right resolution — but only if SRHT has not already saturated the achievable variance reduction.
**Persona response**: ❌ UNREBUTTED in spirit — the marginal-utility argument bites. If SRHT lands, t-design's ceiling is what SRHT didn't capture. Recommended sequencing: t-design becomes an SRHT-contingency, mirroring batch-4 Idea 5 (Repulsive) reframe.

**Refinement (Round 2)**: Reframe as **SRHT-contingent**: do not pre-allocate. If SRHT achieves ≥ 30% variance reduction → archive t-design (SRHT dominates the corner). If SRHT achieves 10-30% → 4-way A/B/C/D at TOY priority 6 (below all batch-3/4 survivors). If SRHT < 10% → t-design fires as a TOY at priority 4.

**Verdict**: FAIL (unconditional commitment) → PASS (with SRHT-contingency reframe).

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 WARN · 2 PASS · 3 WARN · 4 PASS · 5 WARN · 6 FAIL→PASS-w-reframe · UNREBUTTED count = 1.

**Verdict**: 🔁 **REFRAME** 🟡

**Confidence**: 🟡 — the cross-domain T3 source is bona-fide; the mechanism is real; but variance-reduction-family saturation is real. The reframe (SRHT-contingent) is the honest disposition.

**Reframe direction**: Do not allocate an experiment slot pre-emptively. Decision rule depends on SRHT's variance-reduction number. If SRHT ≥ 30 %: archive. If 10–30 %: 4-arm A/B/C/D at TOY priority 6. If < 10 %: TOY priority 4 with synthetic-variance Phase A.

**Composite × confidence**: 2.4 × 0.7 = 1.68. Dominated by Ideas 5, 6 in this batch.

**Ship-now action**: hold; depends on SRHT outcome.
