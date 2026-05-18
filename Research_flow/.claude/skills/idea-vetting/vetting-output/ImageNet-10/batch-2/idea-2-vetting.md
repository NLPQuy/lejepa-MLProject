# Idea 2 Vetting — Sliced-Wasserstein-2 statistic instead of Epps–Pulley
**Batch**: 2 · **Pattern**: P3 (Replace)
**One-liner**: Replace per-slice Epps–Pulley with closed-form 1-D W2 distance to N(0,1).

---

## Stage 1 — Problem Framing
> Persona: **Advisor**. On-task. PASS. Cycle: 0/0/0.

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

**Attack A2.1**: Sliced-Wasserstein-as-loss is huge: GSW (Kolouri 2019), SWAE (Kolouri 2018 autoencoder), Sliced-Wasserstein Flows (Liutkus 2019), and especially **PSW VICReg variants**. The "novelty" of using W2 in a SIGReg slot is thin — it's just substituting one widely-known statistic for another.
**Steel-manned rebuttal**: The novelty is precisely *substitution in the LeJEPA slot* + comparison head-to-head against EP at matched λ. No paper has compared EP-based SIGReg vs W2-based SIGReg as the SSL regulariser. Knowing which 1-D normality test is empirically best in the LeJEPA slot is a useful contribution.
**Persona response**: ⚠️ **WEAKENED** — application-novel, but the contribution is "one ablation row" not a method. Borderline.

**Verdict**: PASS-with-caveat. EXTENDS. Cycle: 0/1/0.

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.
Mechanism-novel for SIGReg slot. Theory unchanged. Net: ablation-tier contribution. PASS. Cycle: 0/0/0.

## Stage 4 — Theory Grounding (lite)
> Persona: **Theorist**.

**Attack A4.1**: W2 between empirical and N(0,1) **does not saturate at large deviations** — proposal cites this as a feature. But under cosine-LR + bf16, "stronger gradient far from target" is also "exploding gradient when embedding is bad" — early training could be unstable.
**Steel-manned rebuttal**: 1-D W2 against a fixed standard Gaussian is bounded above by `||sort(z)||² + const` per slice. With `BatchNorm` or unit-norm pre-slice (which LeJEPA does not have but trivially could add), gradients are well-conditioned. Empirical SW losses in GANs / VAEs train stably without exotic tricks.
**Persona response**: ✅ **DEFLECTED** — stability risk is real but well-precedented as manageable.

**Attack A4.2**: The "sort(z) − Φ⁻¹(ranks)" gradient is *zero* on most of the parameters — only the inverse-sort permutation carries gradient back to each sample. Effective gradient per sample is **shared with neighbours by rank**, which means W2's gradient signal-per-sample is *weaker* than EP's per-sample gradient.
**Steel-manned rebuttal**: That's not how `torch.sort` autograd works in practice — the sort backward is the inverse permutation; each sorted z still gets its full gradient w.r.t. the rank-matched quantile. The per-sample gradient *magnitude* is the same.
**Persona response**: ⚠️ **WEAKENED** — partially correct rebuttal; per-sample magnitudes match, but the *correlation structure* of gradients across batch samples is different (rank-ordered). Could affect mini-batch optimisation dynamics.

**Verdict**: WARN. Cycle: 1/1/0.

## Stage 5 — Feasibility Analysis
> Persona: **Pragmatic PM**.
30 LOC implementation. Need λ re-sweep because W2 has different units. Effort M (because λ-coupling adds runs).
**Attack A5.1**: λ for W2 ≠ λ for EP — comparison at frozen λ is meaningless.
**Steel-manned rebuttal**: Proposal explicitly says to couple this with Idea-5's ASHA sweep. PASS if Idea-5 runs first.
**Persona response**: ✅ **DEFLECTED**.

**Verdict**: PASS (conditional on Idea-5 done first). Cycle: 1/0/0.

## Stage 6 — Killer Baseline
> Persona: **Skeptical Empiricist**.

**Attack A6.1**: The proposal's falsification bar is "must match EP within 0.3 pp" — that's a **parity bar**, not an improvement bar. A method that *matches* EP is not worth shipping; replacing the default is bad practice without a real gain.
**Steel-manned rebuttal**: Parity at lower compute / better stability is itself a win — and W2 has known nicer gradient properties. But "nicer" is unmeasured here, so the parity-only result is dead weight unless paired with a compute or stability metric.
**Persona response**: ❌ **UNREBUTTED** — without an explicit *secondary* improvement metric (stability, compute, or +0.5 pp gain), this idea ships a tie at best.

**Attack A6.2**: Killer baseline is Idea-1 (stacked tests). If stacking 3 tests inside EP's framework beats EP-alone, switching the *base test* from EP to W2 may be dominated.
**Steel-manned rebuttal**: Orthogonal axes — could stack {EP, W2, AD} as a future move. But for *this* batch the head-to-head must beat the easier-and-cheaper stacked-EP win.
**Persona response**: ⚠️ **WEAKENED** — fair; downgrade priority below Idea 1.

**Verdict**: WARN — bar is parity, not gain; dominated-by-Idea-1 risk. Cycle: 0/1/1.

## Stage 8 — Decision
Tally: PASS / PASS / PASS / WARN / PASS / WARN — 0 FAIL, 2 WARN, **1 UNREBUTTED** → downgrade.
Pre-downgrade: TOY. Post-downgrade: **REFRAME**.

**Verdict**: 🔁 **REFRAME** · 🟡 confidence

### Reframe direction
1. Replace the parity bar with a **gain bar**: best W2 run must beat EP by ≥ 0.5 pp linear probe at each side's best λ, **or** demonstrate ≥ 30 % lower SIGReg-loss-variance at the same probe.
2. Sequence: run **after Idea 1 (stacked tests)** — if stacking already beats EP by ≥ 0.5 pp, W2 must beat the stacked result, not the singleton.
3. If neither bar met, kill — W2 is then just an "alternative spelling" of the same effect.

Cycle totals: 2 DEFLECTED / 3 WEAKENED / 1 UNREBUTTED.
