# Idea 6 Vetting — Persistent-homology H₀ topological regularizer
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P1 (Combine) · **Tier**: 3 · **Source**: ideation batch-6 Idea 6

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`.

**Attack 1.1**: "The proposal claims PH₀ catches a 'Cramér-Wold blind spot' in SIGReg's finite-sample regime. But the example would be 'two distributions with identical marginals on every 1-D slice but different cluster structure' — this requires a *fixed slice set*. SIGReg uses 1024 fresh random slices per step (DDP-synced). Over training, the slice set covers the sphere; the blind spot vanishes in the population limit. **There is no finite-N blind spot at M=1024 random slices per step.**"
- Steel-manned rebuttal: True at the population limit. But within a single SGD step (the unit of gradient), only 1024 slices are sampled — the per-step gradient signal *does* have a blind spot at any finite M. PH₀ catches it within-step. The question is whether the blind spot is large enough to affect end-of-training quality.
- Persona verdict: ⚠️ WEAKENED — defensible-in-principle, magnitude unknown. PH₀ gradient may add zero useful signal over the population-limit-equivalent SIGReg at large training horizons (600 ep).

**Attack 1.2**: "Imagenette has 10 classes — natural 'cluster count' = 10. SIGReg pulls toward 1 cluster (single isotropic Gaussian). The two are in mechanistic *tension*, not complement. PH₀ wants to detect cluster structure; SIGReg wants to erase it."
- Steel-manned rebuttal: SIGReg pulls the *marginal* toward N(0, I), not the joint cluster structure. Embeddings can be marginally Gaussian per slice AND have 10 well-separated cluster centroids (the centroids just need to be near-zero-mean over the batch). PH₀ would *reject* over-collapse (when SIGReg+invariance over-pulls), supplementing.
- Persona verdict: ⚠️ WEAKENED — possible-in-principle, but the loss landscape may be inconsistent (SIGReg pulling toward unimodal Gaussian PH₀ signature; PH₀ pulling toward 10-modal mixture PH₀ signature → fights).

**Verdict**: WARN. 0 DEFLECTED / 2 WEAKENED.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`.

**Attack 2.1**: "Moor et al. *Topological Autoencoders* ICML 2020 (arXiv:1906.00722) applies PH to autoencoder embeddings. Trofimov et al. *RTD* ICML 2023 (arXiv:2302.03836) applies it specifically to SSL representations. Hofer et al. *Connectivity-Optimized Representation Learning via Persistent Homology* ICML 2019. **PH-as-SSL-regularizer is not novel**; you cited none of these."
- Steel-manned rebuttal: The ideation's citations were the *cross-domain roots* (Edelsbrunner-Letscher-Zomorodian DCG 2002) + differentiability layer (Hofer NeurIPS 2017) + gradient correctness (Carriere ICML 2021) — not the direct prior art on PH-as-SSL-regularizer. **This is a citation gap** that should have been caught at ideation. The relevant prior is Moor 2020 + Trofimov 2023. Net novelty after correction: PH₀-against-Gaussian-reference is specific (Moor/Trofimov use different PH variants), but the family is well-explored.
- Persona verdict: ❌ UNREBUTTED — uncited direct prior art existed and was not surfaced. The novelty claim ("highest in batch") is overstated.

**Verdict**: SOFT-FAIL on novelty inflation; not a hard duplicate but a missed citation.

## Stage 3 — Novelty Decomposition
EXTENDS (Moor 2020 / Trofimov 2023 family; PH₀-vs-Gaussian-reference is the only novel piece). Re-rated novelty: low.

## Stage 4 — Theory Grounding (lite)
**Attack 4.1**: "PH₀ of an N(0, I_d) sample at batch=128, d=384: the diagram is dominated by O(N) low-persistence components that merge into one connected component at ε ~ sqrt(d). The signal-to-noise of the PH₀ diagram is poor in high-d. **The gradient of W₁(D_PH(Z), D_PH(R)) may be near-zero almost-everywhere because both diagrams are dominated by random merge events.**"
- Steel-manned rebuttal: Sliced-Wasserstein on PH diagrams (Carriere 2021) is the recommended robust variant for high-d. But high-d concentration is real: in d=384, all pairwise distances are concentrated near sqrt(2d), so PH₀ has very narrow persistence range. **Gradient is small-but-nonzero**; whether it is *useful* is empirically untested.
- Persona verdict: ❌ UNREBUTTED — high-d concentration-of-measure is a known killer of PH-on-raw-features. Trofimov 2023 specifically applies PH on a *low-d projection* to avoid this. The proposal applies PH on d=384 directly.

**Verdict**: FAIL on theoretical grounding.

## Stage 5 — Feasibility
> Adopting persona: `Pragmatic PM`.

`torch_topological` exists. O(N³) Vietoris-Rips on N=128 is OK (~50 ms per call at K=200 steps → ~0.1 % overhead). **PASS on cost**; **WARN on the d=384 gradient-signal concern from Stage 4**.

## Stage 6 — Killer Baseline
**Attack 6.1**: "Per the redundancy pre-check rule (W-MSE batch-4 reframe; MMCR batch-5 reframe): 3-arm matched-WC: SIGReg-only / PH-only / SIGReg+PH. PH-only must produce a non-trivial embedding (RankMe meaningfully lower than SIGReg-only — proves PH does its own work); combo must beat both singletons by ≥ 0.4 pp non-overlap. Given the Stage 4 finding (high-d PH gradient near-zero), PH-only is likely to collapse — failing the pre-check immediately."
- Steel-manned rebuttal: Mitigation: project to a smaller subspace before PH (e.g., 32-d random projection on top of the 384-d embedding). But this is a real architectural change, not just an aux loss.
- Persona verdict: ❌ UNREBUTTED — the projection mitigation is a *different* idea (PH-on-projected-space), not the proposed one.

**Verdict**: FAIL.

## Stage 8 — Decision Gate
Stages: 1 WARN / 2 SOFT-FAIL (citation gap + novelty inflation) / 3 WARN (downgraded EXTENDS) / 4 **FAIL** (high-d concentration) / 5 WARN / 6 **FAIL** (redundancy pre-check + gradient signal). **2 FAIL + 3 WARN** → per decision-logic.md priority 8: **REFRAME or KILL**.

**Verdict**: 🔁 **REFRAME** · Confidence 🟢

### Reframe direction
**KILL the d=384 direct-PH version. Salvageable as a different idea:**
1. *Salvage 1*: "PH on a 32-d random / learnable projection" — substantively different idea; defer to batch-7 if anyone cares.
2. *Salvage 2*: "PH₁ (loops) instead of PH₀" — different topological feature; PH₁ is sometimes informative at high-d where PH₀ is degenerate. Defer.
3. **Recommend ARCHIVING the topological-regularizer direction** until a low-d-projection or PH₁-based formulation is proposed AND the high-d concentration concern is empirically tested on a small sanity script (~1 hr CPU: compute PH₀ gradient norm on N(0, I_384) — if < 1e-5 across 100 trials, KILL definitively).

### Resurrection-eligible
Only if user proposes the 32-d-projection or PH₁ variant AND the gradient-norm sanity passes.
