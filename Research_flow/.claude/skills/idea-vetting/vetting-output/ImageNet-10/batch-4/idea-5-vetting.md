# Idea 5 Vetting — Repulsive Monte Carlo slice sampling on S^(d−1)
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P3 (Replace slice generator) · Tier: 3
- Proposed gain: +0.1 / +0.5 / +1.2 pp
- Effort: S · Feasibility: 4/5

## Stage 1 — Problem Framing
*Persona: Advisor.* **Attack**: "Same problem as Idea 4 (variance reduction is not the binding constraint on ImageNet-10), via a different mechanism. The framing inherits Idea 4's weakness — small absolute lift, marginal value." **Rebuttal**: Different mechanism is genuinely orthogonal — DPP/repulsion vs estimator weighting; the two are *composable*, so neither makes the other redundant. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 2 — Prior Work Attack
*Persona: Prior-Work Hunter.* **Attack**: "arXiv:2509.10166 (2025) already published Repulsive MC for sliced-Wasserstein. Direct port; nothing new." **Rebuttal**: Port to SIGReg test statistic family is the novelty (SH-CV and repulsion both target SW in published form; LeJEPA inherits them). EXTENDS. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 3 — Novelty Decomposition
*Persona: Critical Reviewer.* **Attack**: "Three near-identical proposals across batches 3+4 now target slice-MC variance reduction: SRHT (batch-3), Antithetic+SH-CV (batch-4 Idea 4), Repulsive MC (this idea). Pattern duplication; one of them is enough." **Rebuttal**: Each makes a different theoretical guarantee (structured-correlation / control-variate / negative-correlation). Empirically dominant scheme is unknown a priori. **Persona**: ❌ **UNREBUTTED** on the experimental-economy front: running three competitive VR schemes simultaneously is wasteful. **Pick one** based on theoretical best-case, run head-to-head only after that ships.

**Verdict**: FAIL.

## Stage 4 — Theory Grounding (lite)
*Persona: Theorist.* **Attack**: "DPP / Riesz-energy sampling on S^(d−1) for d=384 with M=1024 produces ensembles whose *bias* (vs uniform-on-sphere) is non-zero at finite M. The 2025 paper proves variance benefit, but the bias term may dominate at d=384 / M=1024." **Rebuttal**: The 2025 paper's scaling kicks in for M ≫ d_eff (effective dimension); d=384, M=1024 is M/d ≈ 2.7, borderline. The paper's examples are at higher M/d ratios. Honest answer: scaling regime not validated for our setting. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 5 — Feasibility Analysis
*Persona: Pragmatic PM.* **Attack**: "Riesz-energy gradient descent for 200 iters at d=384, M=1024 = 200 × 1024² × 384 ops ≈ 8e10 ops per resample. Sub-second on GPU but non-trivial." **Rebuttal**: Cached, refreshed every 10 epochs as proposed; negligible vs training. **Persona**: ✅ DEFLECTED. **Verdict**: PASS.

## Stage 6 — Killer Baseline
*Persona: Skeptical Empiricist.* **Attack**: "**SRHT is the same family and ships first.** If SRHT achieves ≥ 20 % variance reduction on its own, the additional headroom for repulsion is bounded — and the implementation cost of repulsion is strictly higher (cached DPP vs in-line FWHT). Dominated unless SRHT *fails* to deliver." **Rebuttal**: True; repulsion is the *fallback* if SRHT under-delivers, not a parallel ship. **Persona**: ✅ DEFLECTED — but the rebuttal *concedes the reframe*: this is a contingency, not a primary work item.

**Verdict**: PASS-with-concession.

## Stage 7 — Reviewer Simulation
SKIPPED.

## Stage 8 — Decision Gate
**Stage tally**: 1 WARN · 2 WARN · 3 **FAIL (UNREBUTTED: experimental-economy)** · 4 WARN · 5 PASS · 6 PASS-with-concession. UNREBUTTED count = 1; one Stage 3 FAIL.

**Verdict**: 🔁 **REFRAME** 🟡

**Reframe direction**: Do not allocate an ImageNet-10 experiment slot for this idea. **Reframe as a contingency**:
- *If* SRHT (batch-3 Idea 2) ships and achieves ≥ 20 % SIGReg-loss variance reduction → repulsion is *dominated*; archive this idea.
- *If* SRHT ships and achieves < 10 % variance reduction → fire this idea as the fallback at the same fixed (λ, lr, wd).
- *If* SRHT achieves 10-20 % → run a 3-arm head-to-head (SRHT / repulsion / Antithetic+CV) at TOY priority 5 (below all other survivors).

**Confidence**: 🟡.

**Composite × confidence**: 2.6 × 0.4 = 1.04 (deep downgrade — REFRAME-as-contingency).
