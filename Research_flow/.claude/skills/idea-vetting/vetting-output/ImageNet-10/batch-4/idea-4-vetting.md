# Idea 4 Vetting — Antithetic + spherical-harmonics control-variate SIGReg estimator
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P2 (Transfer) · Tier: 3
- Proposed gain: +0.1 / +0.5 / +1.2 pp
- Effort: S · Feasibility: 4/5

## Stage 1 — Problem Framing
*Persona: Advisor.* **Attack**: "Variance reduction is *not* the bottleneck of in-domain SSL on ImageNet-10 — the bottleneck is data scarcity. Reducing SIGReg-MC variance by 25 % moves a metric that wasn't blocking anything." **Rebuttal**: Variance reduction → faster early convergence → better fit in fixed epoch budget. On small data, every gradient step matters more. **Persona**: ⚠️ WEAKENED — concession that gain mid (+0.5 pp) is honestly small. **Verdict**: WARN.

## Stage 2 — Prior Work Attack
*Persona: Prior-Work Hunter.* **Attack**: "arXiv:2402.01493 (Spherical-Harmonics CV for SW) already published the recipe. You're porting; nothing new." **Rebuttal**: Port to SIGReg is the novelty — they target sliced-Wasserstein, not slice-CF goodness-of-fit. The integrand is different (the SH coefficients matter). EXTENDS verdict honest. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 3 — Novelty Decomposition
*Persona: Critical Reviewer.* **Attack**: "Antithetic on the sphere with EppsPulley evaluates to **zero gain** when the embedding distribution is symmetric (which N(0,I) target is, by construction). The antithetic trick is *most powerful when the integrand is anti-symmetric*; EppsPulley is even. So expected gain from the antithetic half is ~0." **Rebuttal**: EppsPulley is even in *t* (the CF integration variable), not even in *u* (the slice direction). The u-antithetic pairs reduce variance when the *embedding* distribution has any asymmetry, which it does early in training (before SIGReg has fully Gaussianised). **Persona**: ✅ DEFLECTED (technically), but: the asymmetry shrinks as training progresses → the gain shrinks over epochs. Late-epoch gain is ~0.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Persona: Theorist.* **Attack**: "SH control variate variance bound depends on the smoothness of the integrand on S^(d−1). EppsPulley's per-slice statistic is smooth in the embedding but its gradient through the encoder can be highly non-smooth (multi-crop discontinuities). CV gain may not materialise." **Rebuttal**: The CV operates on the *test statistic*, not on its gradient; the gradient inherits the variance reduction proportionally. The 2024 paper's published 2–3× reduction is on the integrand, which is what we measure. **Persona**: ✅ DEFLECTED. **Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Persona: Pragmatic PM.* **Attack**: "SH up to L=2 in d=384 means O(d²) = 1.5e5 coefficient operations per slice batch. Cheap. But: implementing real spherical harmonics correctly in PyTorch is fiddly — closed-form formulas exist only up to small L." **Rebuttal**: scipy.special has full SH; cache the basis at init. Standard implementation. **Persona**: ✅ DEFLECTED. **Verdict**: PASS.

## Stage 6 — Killer Baseline
*Persona: Skeptical Empiricist.* **Attack**: "**SRHT (batch-3 Idea 2) is the killer baseline.** SRHT is *already* a variance-reduction scheme on the same slice-MC estimator, with simpler implementation and equally-cited bound. If SRHT achieves ≥ 20 % variance reduction (the SRHT target), and this idea achieves ≥ 25 % (the CV target), the *additional* gain from stacking is ambiguous — the variance-reduction headroom is bounded." **Rebuttal**: The 25 % target is *vs Gaussian baseline*, not vs SRHT. The honest claim is: this idea is a competitor *and* potentially a complement to SRHT. The falsification's synthetic-data sanity check is the pre-flight gate. **Persona**: ⚠️ WEAKENED → ❌ UNREBUTTED on the *experimental priority* question: if SRHT is already on the FULL SEND queue (Step 2 of batch-3 recommendation), running this idea before SRHT-vs-Gaussian numbers are in is wasteful. Idea must sequence *after* SRHT.

**Verdict**: WARN.

## Stage 7 — Reviewer Simulation
SKIPPED.

## Stage 8 — Decision Gate
**Stage tally**: 1-3 WARN · 4 PASS · 5 PASS · 6 WARN (UNREBUTTED sequencing). UNREBUTTED count = 1.

**Verdict**: 🧪 **TOY** 🟡

**Toy design**:
- **Phase A (synthetic, pre-flight, ~1 hour CPU)**: simulate `Z ~ N(0,I) + 5% Laplace mixture`, M=256, d=384; measure SIGReg estimator variance with: (i) Gaussian baseline, (ii) Antithetic-only, (iii) Antithetic+CV. If (iii) variance ≥ 1.5× lower than (i), graduate to Phase B. Else KILL.
- **Phase B (gated on Phase A pass AND SRHT shipped)**: 100 ep ImageNet-10, 3-arm: SRHT (baseline) vs SRHT+Antithetic+CV vs Gaussian+Antithetic+CV. 3 seeds. The SRHT+Antithetic+CV arm must beat SRHT-alone by ≥ 15 % more variance reduction. Linear probe parity ±0.3 pp acceptable.

**Toy cost**: Phase A free. Phase B = 3 arms × 3 seeds × 100 ep × 5 GPU-h ≈ 45 GPU-h.

**Sequencing dependency**: blocked on SRHT (batch-3 Idea 2) shipping first.

**Confidence**: 🟡.
