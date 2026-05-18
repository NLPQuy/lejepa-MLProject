# Idea 4 Vetting — Sliced MMD with Riesz kernels as SIGReg statistic
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P3 (Replace per-slice statistic) · Tier: 2
- Proposed gain: +0.2 / +0.6 / +1.3 pp
- Effort: S · Feasibility: 4/5
- Composite (batch-5): 2.4

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor.*

**Attack A1.1**: "Riesz-MMD vs EppsPulley is fundamentally the same family — both are integral-probability-metric tests against N(0,1). The mechanistic distance is small."
**Steel-manned rebuttal**: Riesz-MMD with s=1 is the *energy distance*, a characteristic kernel — strictly stronger than EP's L²-CF distance (which has finite-grid bias). And the O(N log N) sorted computation is mechanically simpler than EP's trapezoid integration. Mechanism: closed-form via sorting, no t_max HP, no n_points HP.
**Persona response**: ✅ DEFLECTED. Framing OK.

**Verdict**: PASS.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter.*

**Attack A2.1**: "Sliced energy distance / sliced MMD is widely used in generative modelling (MMD GANs, MMD flows). Applying to SSL slice statistics is a small step from there."
**Steel-manned rebuttal**: All cited applications are *generator-vs-data* MMD; using Riesz-MMD as a *normality* statistic against an N(0,1) reference is a different objective. The reference-sample-vs-closed-form-N(0,1)-integral split is a design choice not present in the GAN literature.
**Persona response**: ⚠️ WEAKENED — the design choice is real, but the "novel" claim is thin. EXTENDS more than NOVEL.

**Verdict**: PASS. Novelty: EXTENDS.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "Statistic swap with cheaper implementation. Same family as EP."
**Steel-manned rebuttal**: Cheaper-and-strictly-stronger (characteristic kernel) is publishable engineering in climb-mode.
**Persona response**: ⚠️ WEAKENED.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1**: "For s ∈ (0, 2), Riesz-MMD is a valid IPM. But the sorted O(N log N) computation depends on the *unbiased U-statistic* form; the V-statistic form (which is what auto-grad gives by default) introduces a non-zero bias that does not vanish at finite N."
**Steel-manned rebuttal**: Hertrich et al. 2023 §3 give explicit unbiased estimators with the same O(N log N) cost. Implementation must use the U-statistic form, not the naive double-sum.
**Persona response**: ✅ DEFLECTED — implementation note, addressed.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "Sort-and-cumsum gradient through torch.argsort is differentiable but not GPU-friendly at d=384 × M=1024 slices in batched form."
**Steel-manned rebuttal**: `torch.sort` returns a differentiable view; gradients flow through the sorted indices via the standard PyTorch path. At (N=512, M=1024), the cost is 512·log(512)·1024 ≈ 4.7M ops/step — cheaper than EP's 17·512·1024 ≈ 9M.
**Persona response**: ✅ DEFLECTED. Wall-clock should be ≤ EP.

**Verdict**: PASS.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Per-slice-statistic family now 4-deep (EP, Hermite, KSD, Riesz-MMD). What does Riesz-MMD add over the 3 existing?"
**Steel-manned rebuttal**: Cheapest (O(N log N) vs O(N²) KSD vs O(N·n_pts) EP), characteristic kernel (stronger than EP), no HP (no kernel-bandwidth like KSD). Among the four, Riesz-MMD has the best cost-mechanism trade-off; KSD has the highest power but worst cost; EP is the baseline. 4-way A/B/C/D experiment resolves.
**Persona response**: ⚠️ WEAKENED — the "best cost-mechanism trade-off" claim is conditional on synthetic-power being non-worse than EP. Phase A is the right gate.

**Refinement (Round 2)**: Phase A (synthetic-power vs EP/Hermite/KSD at α=0.05): if Riesz-MMD ≥ EP power and wall-clock ≤ EP, it's the new default; pre-empts the 4-way and just ships.

**Verdict**: PASS with refinement.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 PASS · 2 PASS · 3 WARN · 4 PASS · 5 PASS · 6 PASS-w-refinement · UNREBUTTED = 0.

**Verdict**: 🧪 **TOY** 🟡 (with strong upside to graduate after Phase A)

**Confidence**: 🟡 — clean implementation, S effort, T2 evidence; the 4-way bake-off frames the experiment well. Phase A is essentially free.

**Toy design**: Phase A (CPU, 1 hr): synthetic power on N(0,1)+5%shift mixture for {EP, KSD, Riesz-MMD, Hermite}. Phase B (ImageNet, ~25 GPU-h): if Phase A shows Riesz-MMD ≥ EP-power AND wall-clock ≤ EP, ship as new default and run 100-ep head-to-head with EP baseline. If both probe ±0.3 pp parity AND wall-clock lower, adopt Riesz-MMD as the new default statistic.

**Composite × confidence**: 2.4 × 0.7 = 1.68.

**Ship-now action**: Phase A pairs with Idea 2 Phase A — single synthetic-test pass.
