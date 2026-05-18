# Idea 3 Vetting — Test-strictness curriculum (Moments → Epps–Pulley)
**Batch**: 2 · **Pattern**: P5 (Decompose)
**One-liner**: Warm up SIGReg with `Moments` (mean/var only) for first 30% of training, then switch to `EppsPulley`.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.
**Attack A1.1**: Curriculum learning's empirical track record is mixed; Wu et al. (2021, *When Do Curricula Work?*) showed gains are mostly absent on standard regimes.
**Steel-manned rebuttal**: That paper studied curricula on *examples* (easy → hard data). This is a curriculum on *objectives* (weak → strong test) — a much narrower instrument. Closer precedent: SwAV's queue-warmup, MoCo's momentum schedule — both objective-curricula and both shipped.
**Persona response**: ⚠️ **WEAKENED** — analogy holds but Wu et al.'s skepticism transfers partly.

**Verdict**: PASS. Cycle: 0 / 1 / 0.

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

**Attack A2.1**: Sliced-Score-Matching (Song 2019) literally has a "from-moments-to-score" hierarchy. Curriculum on statistical tests is implicit in any moment-matching → score-matching sequence.
**Steel-manned rebuttal**: SSM is a generative-model objective curriculum on *what is being scored*; this is an SSL-regulariser curriculum on *which Gaussianity test is being penalised*. Different family, but the principle is the same — supports the prior, not duplicates it.
**Persona response**: ✅ **DEFLECTED** — EXTENDS the principle to SSL regularisation. Not duplicate.

**Verdict**: PASS. EXTENDS. Cycle: 1 / 0 / 0.

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.
Net novelty: **mechanism-new** (curriculum across UnivariateTest plugins), **theory-clean** (both tests still null at N(0,1)). Acceptable. Cycle: 0/0/0.

**Verdict**: PASS.

## Stage 4 — Theory Grounding (lite)
> Persona: **Theorist**.

**Attack A4.1**: `Moments` test is `||μ||² + ||σ²−1||²` per slice — that's TWO degrees of freedom. It has **infinitely many minimisers**: any 1-D distribution with mean 0, variance 1 (Cauchy-truncated, bimodal, etc.). Embedding can perfectly satisfy `Moments` and be wildly non-Gaussian. Switching to EP at epoch 30 then faces a *catastrophic discontinuity*: the embedding is in a "Moments-OK / EP-bad" plateau, and EP gradients now have to undo whatever non-Gaussian shape Moments tolerated. May train worse than always-EP.
**Steel-manned rebuttal**: The 2-3 epoch linear blend at the switch (mentioned in proposal's "Risks") absorbs this. Empirically, going through "wrong shape but right scale" before "right shape" is *the standard easy-to-hard path*; the worry is symmetric to "training large LMs on data before code", which is the accepted regime.
**Persona response**: ⚠️ **WEAKENED** — linear-blend transition mitigates but does not eliminate. The "infinite minimisers" critique is real and the falsification protocol must check the SIGReg(EP) value at the switch is not catastrophic.

**Verdict**: WARN. Cycle: 0/1/0.

## Stage 5 — Feasibility Analysis
> Persona: **Pragmatic PM**.

5-point milestone sweep × 3 seeds × 1.5 GPU-h = **22 GPU-h**. Lightning callback is 20 LOC.

**Attack A5.1**: The proposal's 5-point sweep buries the cost — actually 15 runs at top fidelity = closer to 30 GPU-h.
**Steel-manned rebuttal**: True for 3 seeds × 5 points. Could halve by collapsing seed-grid to 2 seeds at the edges and 3 at the predicted-best — but this is a small ablation, not the headline result.
**Persona response**: ⚠️ **WEAKENED** — cost is real but bounded. Effort still S (≤ 30 GPU-h).

**Verdict**: PASS. Cycle: 0/1/0.

## Stage 6 — Killer Baseline
> Persona: **Skeptical Empiricist**.

**Attack A6.1**: Killer baseline = milestone 0 (always EP) = vanilla LeJEPA. If the U-shape over milestone is flat or monotone-decreasing, the curriculum is worthless and we learned only that EP works from epoch 0.
**Steel-manned rebuttal**: This is exactly the falsification protocol the proposal already specifies ("best curriculum must beat both endpoints by ≥ 0.5 pp"). Honest design.
**Persona response**: ✅ **DEFLECTED**.

**Attack A6.2**: A stronger baseline is **cosine-λ schedule** (the reframed batch-1 Idea 4) — same "ramp the regulariser" intuition but cheaper (no callback, no test swap). If cosine-λ matches or beats this curriculum, this idea is dominated.
**Steel-manned rebuttal**: Cosine-λ and curriculum-on-test are *not* equivalent: cosine-λ shrinks the *magnitude* of the same statistic; curriculum-on-test changes *which* statistic is computed. The proposal explicitly argues curriculum-on-test is the more natural place. Both should run in parallel and be compared.
**Persona response**: ⚠️ **WEAKENED** — they should be co-run; without cosine-λ as a control, this idea's result is uninterpretable.

**Verdict**: WARN — cosine-λ control is mandatory in the toy. Cycle: 1/1/0.

## Stage 8 — Decision
Tally: PASS / PASS / PASS / WARN / PASS / WARN — 0 FAIL, 2 WARN, 0 UNREBUTTED → **TOY** eligible.

**Verdict**: 🧪 **TOY** · 🟡 confidence

### Toy Experiment Design
- **Question**: Does curriculum-on-test (Moments→EP) beat always-EP and cosine-λ-on-EP by ≥ 0.5 pp linear probe?
- **Arms (3 seeds each)**:
  1. Always-EP (vanilla LeJEPA, milestone=0)
  2. Cosine-λ on EP (cosine from λ_max=0.2 to λ_min=0.02 over 100 ep)
  3. Curriculum: Moments first 30ep → 3ep linear blend → EP rest, fixed λ
  4. Curriculum (worst-case): Moments first 50ep → EP rest, fixed λ
- **Cost**: 4 × 3 × 1.5 = **18 GPU-h**.
- **Decision rule**: Best curriculum arm beats both Arm 1 and Arm 2 by ≥ 0.5 pp (non-overlapping CI). Sanity check: SIGReg(EP) at switch time ≤ 2× its always-EP value at the same epoch.

Cycle totals: 2 DEFLECTED / 4 WEAKENED / 0 UNREBUTTED.
