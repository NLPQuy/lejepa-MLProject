# Idea 1 Vetting — Stacked univariate tests in SIGReg
**Batch**: 2 · **Benchmark**: ImageNet-10 · **Task**: LeJEPA in-domain SSL embedding
**Mode**: --climb-mode (Stage 7 skipped) · **Pattern**: P1 (Combine)
**One-liner**: Per slice, sum EppsPulley + AndersonDarling + Watson — three independent normality tests already in `lejepa.univariate`, no new HP at unit weights.

---

## Stage 1 — Problem Framing
> Adopting persona: **Advisor**. Stance: does this make a real dent on the named task?

**Attack A1.1**: The task is "linear-probe top-1 on ImageNet-10". The stacked test improves *training-time SIGReg power*, not directly *probe accuracy*. The chain `more powerful normality test → more isotropic embedding → better linear probe` has two hops, each loosey.
**Steel-manned rebuttal**: LeJEPA's whole theorem says isotropic-Gaussian = optimal-downstream-linear-risk. Any improvement to the SIGReg power tightens that exact bound. The chain is one hop, not two — the theorem is the second hop.
**Persona response**: ⚠️ **WEAKENED** — theorem is asymptotic; finite-n + linear-probe variance (~0.3 pp seed) easily eats sub-1 pp signal. Plausible, not decisive.

**Verdict**: PASS (1 WARN). Framing is honest — measurable, falsifiable, on-task. Rebuttal-cycle: 0 DEFLECTED / 1 WEAKENED / 0 UNREBUTTED.

## Stage 2 — Prior Work Attack
> Adopting persona: **Prior-Work Hunter**. Stance: someone already did this.

**Attack A2.1**: "Combining goodness-of-fit tests" is statistically textbook — D'Agostino & Stephens *Goodness-of-Fit Techniques* (1986) is an entire monograph on combining/selecting tests; nothing here is statistically novel.
**Steel-manned rebuttal**: The novelty is *application to SSL loss*, not to statistics. LeJEPA paper uses one test (EppsPulley); no SSL paper has applied the *sum of complementary normality tests* in this exact slot. Combining-test-as-loss-term ≠ combining-test-for-hypothesis-decision.
**Persona response**: ✅ **DEFLECTED** — application-novel is acceptable when extending a brand-new objective. EXTENDS, not DUPLICATE.

**Attack A2.2**: Could not find direct prior art for "Anderson-Darling + Watson sum as SSL regulariser". Closest: VICReg (Bardes 2022) uses *three different terms* (variance, invariance, covariance) — same flavour, different objective. Not a duplicate.
**Steel-manned rebuttal**: VICReg's three terms are mean / variance / decorrelation, not three Gaussian-fit tests on one slice. Mechanism disjoint.
**Persona response**: ✅ **DEFLECTED**.

**Verdict**: PASS (0 FAIL). EXTENDS LeJEPA. Rebuttal-cycle: 2 DEFLECTED / 0 WEAKENED / 0 UNREBUTTED.

## Stage 3 — Novelty Decomposition
> Adopting persona: **Critical Reviewer**.

Novelty axes: (a) **mechanism** — combining > 1 univariate test in `SlicingUnivariateTest` (NEW use, EXTENDS); (b) **theory** — Cramér–Wold still applies (NOT NEW; preserved); (c) **architecture** — none.

**Attack A3.1**: Net novelty is "1 line of code (sum) + 0 theory + 0 architecture". A reviewer would call this 'engineering tweak', not 'contribution'.
**Steel-manned rebuttal**: For a *climb-mode* (benchmark-improvement) deliverable, a 1-line theory-preserving free lift IS the contribution. Not aimed at NeurIPS; aimed at the ImageNet-10 number.
**Persona response**: ✅ **DEFLECTED** in climb-mode (per `--climb-mode` flag).

**Verdict**: PASS — net novelty is application-level, acceptable in climb-mode. Rebuttal-cycle: 1 DEFLECTED / 0 WEAKENED / 0 UNREBUTTED.

## Stage 4 — Theory Grounding (lite, --climb-mode)
> Adopting persona: **Theorist**.

**Attack A4.1**: Three tests' statistics are *not independent* on n ≤ 256 (D'Agostino & Stephens 1986 power tables show AD vs CvM Pearson correlation > 0.85 at n=200). The "near-orthogonal power profile" claim is overstated.
**Steel-manned rebuttal**: Correlation across samples doesn't kill orthogonality of *power directions*: AD weights tails, EP weights all frequencies, Watson is multi-modality. Even if their statistic values correlate marginally, their gradients point at different deviation patterns. The sum has the same null (vanishes iff Gaussian) and strictly more power against any single alternative.
**Persona response**: ⚠️ **WEAKENED** — gradient-direction-orthogonality is the right concept but **not measured** in the proposal. Plausible, untested.

**Verdict**: WARN. Cramér–Wold preserved ✓. Power-additivity claim is theoretically plausible but not empirically demonstrated. Rebuttal-cycle: 0 DEFLECTED / 1 WEAKENED / 0 UNREBUTTED.

## Stage 5 — Feasibility Analysis
> Adopting persona: **Pragmatic PM**.

All three tests already implemented in `lejepa.univariate`. `SlicingUnivariateTest` takes one test → trivial extension to a list. Compute overhead: each test shares the slice projection (dominant cost) → ≤ 1.5× per-step time. 3 seeds × 3 ablations (EP, EP+AD, EP+AD+W) × 100ep × ViT-S ≈ 12 GPU-h.

**Attack A5.1**: AndersonDarling has known numerical instability at the empirical CDF tails for n < 128 per-slice. With batch=512 / V=8, per-slice n=512 — should be fine. But on the local-crop SIGReg paths (smaller effective n), tail-clamp matters.
**Steel-manned rebuttal**: All three tests in the library already clamp via `EPS`; numerical instability is a non-issue at LeJEPA's batch sizes.
**Persona response**: ✅ **DEFLECTED**.

**Verdict**: PASS. Effort S. Rebuttal-cycle: 1 DEFLECTED / 0 WEAKENED / 0 UNREBUTTED.

## Stage 6 — Killer Baseline
> Adopting persona: **Skeptical Empiricist**.

**Attack A6.1**: The killer baseline is **EppsPulley alone with M=1024 slices** (the existing default). EP at M=1024 is past the variance plateau in the LeJEPA paper Fig. 4; adding two more tests at the same M may add no probe gain because the bottleneck is invariance / data, not SIGReg power.
**Steel-manned rebuttal**: True if SIGReg is fully saturated. But on ImageNet-10 / ViT-S (small data, small model), SIGReg's regularisation is *not* saturated — that's the regime where finite-sample test power matters most. The hypothesis is testable in the falsification protocol.
**Persona response**: ⚠️ **WEAKENED** — defensible but unproven.

**Attack A6.2**: There's also a **simpler baseline**: EppsPulley at M=2048 (double the slices) costs the same as 3 tests at M=1024 and gets the same variance reduction. If the gain is from "more statistical resolution per step", just-more-slices dominates.
**Steel-manned rebuttal**: Variance reduction from more slices and from complementary-test combination are different effects. More slices reduces the *MC noise* of estimating the same statistic; stacking reduces *systematic bias* against non-Gaussian modes EP misses. They are additive, not substitutive.
**Persona response**: ⚠️ **WEAKENED** — plausible, but the experiment design must include EP@M=2048 as a control or the result is uninterpretable.

**Verdict**: WARN. Killer baseline (EP@M=2048) is mandatory in the toy. Rebuttal-cycle: 0 DEFLECTED / 2 WEAKENED / 0 UNREBUTTED.

## Stage 8 — Decision
Stage tally: PASS / PASS / PASS / WARN / PASS / WARN — 0 FAIL, 2 WARN, 0 UNREBUTTED.
Per `decision-logic.md`: 0 FAIL + ≤ 2 WARN + Stage 5 PASS → **FULL SEND** eligible, but Stage 4 power-claim is unmeasured and Stage 6 requires the EP@M=2048 control → safer route is TOY first.

**Verdict**: 🧪 **TOY** · 🟢 confidence

### Toy Experiment Design
- **Question**: Does stacking {EP, AD, Watson} beat EP-alone *and* EP@M=2048 by ≥ 0.5 pp linear probe on ImageNet-10?
- **Conditions**: 4 arms × 3 seeds, ViT-S, 100 ep, fixed λ=0.1 (or sweep λ if Idea-5 ASHA already done).
  - Arm 1: EP@M=1024 (baseline)
  - Arm 2: EP@M=2048 (variance-control)
  - Arm 3: {EP, AD}@M=1024
  - Arm 4: {EP, AD, Watson}@M=1024
- **Cost**: 4 × 3 × 1.5 GPU-h ≈ **18 GPU-h** (small).
- **Decision rule**: Arm 4 must beat both Arm 1 and Arm 2 by ≥ 0.5 pp (non-overlapping seed CIs). If only beats Arm 1 → variance-reduction, not power, was the driver → reframe to "use M=2048". If beats neither → kill the salvage.

Cycle totals: 4 DEFLECTED / 4 WEAKENED / 0 UNREBUTTED.
