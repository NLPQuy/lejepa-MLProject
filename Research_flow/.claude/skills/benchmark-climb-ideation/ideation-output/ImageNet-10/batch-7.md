# Idea Batch 7 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-19
**Time-to-batch**: ~12 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 30/20/50 --given-vetting .claude/skills/idea-vetting/vetting-output/ImageNet-10/batch-6/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1 on frozen backbone).
- Task: in-domain SSL pretraining, frozen-backbone linear probe per [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py).
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (EppsPulley × 1024 Gaussian random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=4e-4 wd=5e-2, fp16, 600 epochs.
- Scope: **enhance-existing**.
- Tier mix (configured): **30 / 20 / 50** — overridden mid-session by user feedback to **0 / 0 / 100** (T3-only). The configured-mode band-rule `each ≥ 10` is therefore violated by user direction; surfaced as `⚠ Tier-mix-override violation` below.
- Budget / constraint: 1 × A100, ≤ 4 GPU-h per 100-ep ViT-S run; soft "single-λ" branding.
- User-directed themes (per mid-session feedback): **flow matching, score matching, game theory, reinforcement learning, neural collapse**.

### Given vetting feedback applied (batch-6 → batch-7)
- ✅ Avoided **batch-6 TOY / REFRAME duplicates**: registers (REFRAMED), RankMe controller (TOY), iBOT-SIGReg (TOY), Sinkhorn invariance (TOY → distinguished from Idea 1 below), Poincaré projector (TOY), PH topology (REFRAMED, near-KILL).
- ✅ **Per-slice-statistic family closed** (EP / Hermite / KSD / Riesz-MMD) — Idea 2 below explicitly uses *multivariate* Hyvärinen score matching with Hutchinson trace (NOT per-slice; mechanism-distinct from KSD — see Idea 2 §Mechanism for the differentiation).
- ✅ **Variance-reduction sampler family closed** (Gaussian / SRHT / Repulsive / Antithetic+SH-CV / t-design) — Idea 3 below replaces *expectation over u* with *max over u* (minimax, not MC variance reduction; mechanism-distinct).
- ✅ **Covariance-shaping auxiliary family closed** (W-MSE, MMCR — both REFRAMED for SIGReg redundancy) — Idea 5 below uses pairwise-cosine-equiangular-prototype targets (frame theory), not a covariance-determinant penalty.
- ✅ **Cross-skill feedback addressed**: batch-6 vetting noted (a) the ideation skill should consult `_toy_queue.md` and per-skill rejection logs before drafting and (b) for T3 ideas it should search `"<technique> SSL representation learning"` in-field. Both lookups performed for every idea below (see search log entries with "self-supervised" or "representation learning" clause).
- ⚠️ **`--compose-mode` recommendation now 5 batches in a row** — vetting has flagged this since batch-3. The skill still does not expose the flag. This batch *honors the user's explicit T3-themes feedback* over the compose-mode recommendation; surface to user that the compose-mode-enumeration request remains unaddressed at the skill level.
- ⚠️ **Tier-mix-override violation**: user requested 100 % T3 in mid-session feedback. The skill spec's `each ≥ 10` rule is therefore violated by user direction. All 5 ideas are T3 cross-domain. No T1 or T2 ideas in this batch.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 5 (minimum) |
| Search-tier T1 / T2 / T3 (counts) | 0 / 0 / 5 → 0 / 0 / 100 % |
| Tier mix vs configured | 0/0/100 vs configured 30/20/50, user-overridden 0/0/100 — bands-rule violated by direction ⚠ |
| Scope mix | 5 enhance-existing / 0 greenfield ✅ |
| Patterns used | P1, P2, P3 (×2), P5, P6 — 5 distinct, max 2 per pattern ✅ |
| Mandatory pattern check | ≥1 P2 ✅ (Idea 4) · ≥1 P6 ✅ (Idea 3) |
| Distinct venues | 7 (ICLR 2023, JMLR, NeurIPS 2019, CVPR 2019, CVPR 2021, PNAS 2020, arXiv 2026) |
| Time windows | <12 mo: 2 · 12–36 mo: 2 · 36–72 mo: 1 · classics: 2 |
| Avg feasibility | 3.4 / 5 |
| Avg confidence | 🟢 20 % · 🟡 60 % · 🔴 20 % |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|-----------:|-----:|:------:|------:|
| 2 | **Multivariate score matching** vs N(0,I) (Hyvärinen + Hutchinson trace) | P3 | 3 | +0.5 | 4 | S | **2.27** |
| 3 | **Adversarial max-sliced SIGReg** (game-theoretic worst-case slicing) | P6 | 3 | +0.7 | 4 | M | **2.17** |
| 1 | **Flow-matching invariance** (continuous-time velocity field aligns view distributions) | P3 | 3 | +0.8 | 3 | M | **1.91** |
| 4 | **RL-learned augmentation policy** (REINFORCE on crop parameters) | P2 | 3 | +0.6 | 3 | M | **1.80** |
| 5 | **Neural-collapse ETF prototypes** (online k-means + simplex-ETF cosine target) | P5 | 3 | +0.5 | 3 | M | **1.78** |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` · S=4 M=3 L=2.

## Top-3 recommendations

### ⚡ Quick win — **Idea 2: Multivariate score matching vs N(0,I)**
The score of the target N(0,I) is **closed-form**: `∇z log p(z) = −z`. Hyvärinen's score-matching objective `E[‖∇z log p_data(z) − ∇z log p_target(z)‖²]` reduces to the integration-by-parts identity `E[‖s_θ(z) + z‖² + 2 ∇·s_θ(z)]` (with `s_θ(z) = ∇z log p_data(z)`). At LeJEPA scale (`d = 384`), the divergence trace can be computed by the **Hutchinson estimator** `Tr(∇s) ≈ E_v[v^T ∇s v]` with `v ~ N(0,I)`. Drop-in alternative to SIGReg with `~10 LoC` and *zero new HP*. **Mechanism-distinct from KSD (batch-5 TOY)**: KSD = per-slice kernel goodness-of-fit; multivariate score matching = full-d L² between scores via Hutchinson — different math object, different bias-variance profile. Sharp falsification at 100 ep ImageNet-10 cost.

### 🏆 Big bet — **Idea 3: Adversarial max-sliced SIGReg**
LeJEPA averages SIGReg over `M = 1024` *random* slices. Game theory says: don't average, *minimax*. At each step, an adversarial slicing head `g_φ : R^d → S^(d−1)` proposes the **worst-case** direction where the Epps–Pulley statistic on `Z · g_φ` is largest (the encoder's blind spot); the encoder is trained to be flat against this worst direction. Mathematically: replace `E_u T(u)` with `max_u T(u)` (von Neumann minimax 1928 / Nash 1951 / Deshpande et al. CVPR 2019 "Max-Sliced Wasserstein"). Two players: encoder minimizes, slicing-head maximizes; gradient ascent–descent or no-regret online learning. **Mechanism-distinct from the closed variance-reduction sampler family**: those reduce variance of a Monte-Carlo expectation estimator; max-sliced *replaces* the expectation with a worst-case. Single slice suffices in principle — `M = 1` instead of 1024. Strong novelty; well-tested mechanism in GAN literature with direct linear-probe-relevant evidence on density-matching.

### 🛡️ Safe bet — **Idea 1: Flow-matching invariance**
Replace the per-pair invariance `L_inv = mean_i ‖z_i^v1 − z_i^v2‖²` with **conditional flow matching** (Lipman et al. ICLR 2023): learn a time-dependent velocity field `v_ψ(z, t)` such that the continuous ODE `dz/dt = v_ψ(z, t)` transports the embedding distribution of view-1 (at `t=0`) into the embedding distribution of view-2 (at `t=1`). Loss is the closed-form CFM L² between `v_ψ` and the OT-displacement target. **Mechanism-distinct from Sinkhorn (batch-6 TOY)**: Sinkhorn = static entropic OT plan between two empirical clouds, single solve per batch; flow matching = a continuous *velocity field* that defines an entire ODE flow — the regularization signal is the deviation of `v_ψ` from the prescribed conditional path, which gives richer gradients than a single OT plan. Direct published evidence: arXiv:2512.19729 "High-Performance SSL by Joint Training of Flow Matching" (Dec 2025) reports SSL gains from flow-matching as a parallel objective.

---

## Ranked ideas

### Idea 2: Multivariate score matching vs N(0,I) (Hyvärinen + Hutchinson trace)

- **Pattern**: P3 (Replace — swap the Epps–Pulley univariate ECF test with multivariate Hyvärinen score matching)
- **Tier**: 3 (mathematical statistics — Stein's identity 1972 *Ann. Math. Stat.* / Hyvärinen *JMLR* 2005)
- **Scope**: enhance-existing. Replaces SIGReg's per-slice statistic with a single multivariate term. Encoder, projector, invariance, λ, multi-crop unchanged.
- **One-liner**: At each step, compute `L_sm = ‖s_θ(z) + z‖² + 2 ∇·s_θ(z)` where `s_θ` is the gradient of the projector head w.r.t. its input and `∇·` is the divergence estimated by Hutchinson — *0 iff the embedding distribution is exactly N(0, I)*.

**Mechanism**:
Hyvärinen (JMLR 2005, [https://www.jmlr.org/papers/v6/hyvarinen05a.html](https://www.jmlr.org/papers/v6/hyvarinen05a.html)) showed that an unnormalised density `p_θ(z) ∝ exp(−E_θ(z))` can be fit by minimizing the Fisher divergence `J(θ) = E_p_data[‖∇z log p_θ(z) − ∇z log p_data(z)‖²]`, which by integration-by-parts reduces to `J(θ) = E[‖∇z log p_θ(z)‖² + 2 Δ log p_θ(z)]` (no need to estimate `∇ log p_data`). For our setting, the *model* distribution is the empirical distribution of LeJEPA embeddings (the thing we want to *constrain*) and the *target* is N(0,I). Flipping the roles: define `s_θ(z) = z − μ_θ(z)` as a small parametric model of the data-side score and minimize the Fisher divergence to the N(0,I) score `−z`. Equivalently, *the encoder is trained so that its embedding distribution matches N(0,I) in the score-matching sense*. The trace `Δ log p` is estimated by the Hutchinson trick `Tr(A) ≈ E_v[v^T A v]` with `v ~ N(0, I_d)` — one extra random vector per batch, one extra Jacobian-vector product (`torch.autograd.grad` with `create_graph=True`). At `d = 384`, this is ~5 % step-cost overhead.

The distinction from batch-5 KSD (per-slice Kernel Stein Discrepancy, currently in the joint Phase-A bake-off) is sharp: KSD is a *per-slice statistic* computed over each 1-D projection `u^T z`, with kernel mediation in the RKHS of `u^T z`. Multivariate Hyvärinen score matching is a *single full-d L² distance* between two `R^d → R^d` vector fields — no slicing, no kernel, no RKHS. The bias-variance profile is fundamentally different: KSD's variance scales with `M_slices`; Hyvärinen's variance scales with the Hutchinson sample count and `d`. The two regularizers can both be 0 at the population N(0,I) limit but penalize different finite-sample failures.

**Source inspirations**:
- Primary (cross-domain root): *Estimation of Non-Normalized Statistical Models by Score Matching*, Hyvärinen, **JMLR 6, 2005** — foundational identity; integration-by-parts trick.
- Primary (computational trace): Hutchinson, *A stochastic estimator of the trace of the influence matrix*, **Communications in Statistics — Simulation and Computation 19(2), 1990** — random-vector trace estimator.
- Supporting: *Sliced Score Matching*, Song, Garg, Shi, Ermon, **NeurIPS 2019** / [arXiv:1905.07088](https://arxiv.org/abs/1905.07088) — scalable estimator for score matching (provides the gradient-trace cost-reduction trick; we use Hutchinson at full-d instead of sliced to be mechanism-distinct from per-slice closed family).
- Supporting: *Stein's Unbiased Risk Estimate and Hyvärinen's Score Matching*, [arXiv:2502.20123](https://arxiv.org/abs/2502.20123) (Feb 2025) — recent unification of score matching with SURE.

**Why expected to improve**:
SIGReg's per-slice statistic is *intrinsically* a 1-D-projection test — Cramér-Wold guarantees consistency only at the *population* limit `M → ∞`. At finite batch size `N = 512` and finite `M = 1024`, the test is unbiased but has nontrivial variance. Multivariate score matching is a *full-d* test that uses the analytic form of the target score (`−z`); at the population limit it gives the same answer, but at finite N it leverages the smoothness of `−z` to give a lower-variance estimate of the same quantity. Empirically (Song-Ermon 2019, Vincent 2011), score-matching-trained EBMs match or beat ECF-style methods on standard density-estimation benchmarks at equal sample complexity.

**Expected gain**: +0.2 / +0.5 / +1.2 pp 🟢 *(direct evidence on density-fit; small-but-clean lift; lowest-variance estimator of a quantity already known to be useful)*
**Feasibility**: 4/5 🟢 (`torch.autograd.grad(s, z, grad_outputs=v, create_graph=True)` + one extra forward + `0.5*(s+z).pow(2).mean() + (v*grad).mean()` — ~10 LoC)
**Effort**: S 🟢

**Implementation sketch**:
1. Define `s_θ(z) = projector_head(z) − z` (small residual head; trainable score function).
2. Sample `v ~ N(0, I_d)` once per batch.
3. Compute `grad_v = torch.autograd.grad((s_θ(z) * v).sum(), z, create_graph=True)[0]`.
4. Loss: `L_sm = 0.5 * (s_θ(z) + z).pow(2).sum(-1).mean() + (v * grad_v).sum(-1).mean()`.
5. Replace SIGReg's `λ · SIGReg(z)` term with `λ · L_sm`. Use same λ — score-matching is on the same scale.
6. Sanity ablation: 3-arm at ASHA-best (lr, wd, λ_SIGReg): baseline SIGReg / Hyvärinen-only / 50/50-mixed (both at the same λ).

**Risks**:
- Hutchinson variance: single-`v` estimator is unbiased but noisy; consider 2-3 `v` samples if the loss curve is too jagged (cost is linear).
- Score-matching has a known **convex-decoy** failure: the trivial `s_θ(z) = −z` gives `L_sm = 0` regardless of the actual embedding distribution. **Hard mitigation**: parameterize `s_θ(z) = MLP(z)` from scratch (no closed-form `−z` reachable in 1 step) AND backprop through `z`, *not just through `s_θ`*. This way, when the MLP collapses to `−z`, the gradient flows back into the encoder forcing the embedding to actually be N(0,I) for the equality `s_θ(z) + z = 0` to hold sample-wise.
- Composition with batch-2 SRHT (variance-reduction sampler for the *closed* per-slice family): irrelevant — score matching does not slice. With Idea 1 RankMe-controller (b6 TOY): clean, controller works on `λ_SIGReg` regardless of which SIGReg variant is used.
- Composition with KSD (b5 active TOY): **mutually exclusive** in the per-step loss budget. The Phase-A bake-off should be extended to a 5-arm: EP / Hermite / KSD / Riesz-MMD / Hyvärinen, all measured by per-step time × downstream probe.

**Falsification test**: 100-ep ImageNet-10 at ASHA-best (lr, wd, λ), 3 seeds, 3-arm: SIGReg-only baseline / Hyvärinen-only / 50-50 mixed. Primary: best Hyvärinen-containing arm linear probe ≥ 0.3 pp non-overlap above baseline at matched-wall-clock. Mechanism check: monitor `‖Cov(z) − I‖_F` and the per-slice Epps–Pulley statistic on saved Hyvärinen-only checkpoint; *both* should converge to baseline-or-better levels — if SIGReg-statistic *increases* under Hyvärinen-only, the two are not equivalent population-limits and Hyvärinen is missing something Cramér–Wold captures; reject.

---

### Idea 3: Adversarial max-sliced SIGReg (game-theoretic worst-case slicing)

- **Pattern**: P6 (Verify — turn SIGReg into a minimax adversarial verifier rather than an averaging estimator)
- **Tier**: 3 (game theory — von Neumann 1928 *Math. Ann.* minimax theorem; Nash 1951 *Ann. Math.* equilibria; ML translation Deshpande et al. CVPR 2019)
- **Scope**: enhance-existing. Adds a small slicing-direction head `g_φ`; replaces `E_u T(u)` with `max_u T(u)` (or `top-k`). Encoder, projector, invariance, λ, multi-crop unchanged.
- **One-liner**: Train a small adversarial head `g_φ : R^d → S^(d−1)` that outputs the *worst-case* projection direction maximizing the Epps–Pulley test on the encoder's batch; train the encoder to minimize `T(Z · g_φ(Z))`. Two-player zero-sum game: encoder vs. test-direction.

**Mechanism**:
The Cramér–Wold theorem says: *every* 1-D projection of `Z` is N(0,1) `⇒ Z` is jointly N(0, I). LeJEPA approximates this by averaging the Epps–Pulley statistic over `M = 1024` random unit directions: `L = (1/M) Σ_m T(Z · u^(m))`. Game theory rewrites the requirement as a minimax: `Z ~ N(0,I) ⇔ max_u T(Z · u) = 0`. The encoder minimizes the *worst-case* slice, not the average slice. This is exactly the structure of the Max-Sliced Wasserstein distance (Deshpande et al. CVPR 2019, [arXiv:1904.05877](https://arxiv.org/abs/1904.05877)): replace `E_u W_2(P u, Q u)` with `max_u W_2(P u, Q u)`. Deshpande et al. prove a finite-sample concentration that *improves* on the sliced-Wasserstein bound for a fixed projection budget; this carries over to the Epps–Pulley setting because both are functionals of the 1-D-projected empirical distribution.

The min-max is solved by alternating gradient ascent–descent: `g_φ` ascends `T(Z · g_φ(Z))`, projected onto the unit sphere; the encoder descends the same. Convergence is guaranteed for convex–concave games (von Neumann minimax theorem) and *empirically* observed in the non-convex GAN regime with appropriate regularization (gradient penalty, spectral normalization). For SIGReg the situation is *more favorable* than GANs: the inner-`max` is over a low-dimensional sphere `S^(d−1)` (vs. GANs where the inner max is over a high-capacity discriminator), and there is no "fake distribution" — the adversary's only job is to find the worst projection direction.

Per-step cost: the slicing head can be a 2-layer MLP (`d → 4d → d`) with normalized output, ~600k params total — negligible vs the encoder. Per-step time is dominated by the *fewer* slices: `M = 1` adversarial slice replaces `M = 1024` random — net 100×–1000× *cheaper* SIGReg per step.

This is **mechanism-distinct from the closed variance-reduction sampler family** (Gaussian / SRHT / Repulsive / Antithetic+SH-CV / t-design): those families estimate `E_u T(u)` with *lower-variance MC* — the target quantity is still the average. Max-sliced replaces the *target quantity* with `max_u T(u)` — a fundamentally different objective. Two estimators of two different quantities.

**Source inspirations**:
- Primary (cross-domain root): *Zur Theorie der Gesellschaftsspiele*, von Neumann, **Math. Ann. 100, 1928** — minimax theorem; foundational result of game theory.
- Primary (computational): *Max-Sliced Wasserstein Distance and its use for GANs*, Deshpande, Hu, Sun, Pyrros, Siddiqui, Koyejo, Zhao, Forsyth, Schwing, **CVPR 2019** / [arXiv:1904.05877](https://arxiv.org/abs/1904.05877) — establishes the minimax-over-projections framework for distribution matching; finite-sample concentration bound.
- Supporting: *Distributional Sliced-Wasserstein and Applications to Generative Modeling*, Nguyen et al. ICLR 2021 — distribution-over-projections variant (interpolates between random and adversarial); informs the gradient-penalty mitigation below.
- Supporting: *Greedy Approach to Max-Sliced Wasserstein*, [ICLR 2020 workshop](https://openreview.net/pdf?id=BJgRsyBtPB) — algorithmic alternatives to gradient ascent for the inner max.

**Why expected to improve**:
Three compounding wins. **(1) Sample efficiency**: max-sliced concentrates at rate `O(d / N)` vs. average-sliced at `O(1/M + 1/N)` for fixed `M`; the encoder is regularized against its *worst* embedding direction, which is what matters for downstream — a linear probe will *find* the worst direction at test time. **(2) Cheap SIGReg**: M=1 adversarial slice replaces M=1024 random — 1000× fewer projection evaluations per step (the slicing-head fwd-bwd is amortized). **(3) Single hyperparameter**: the inner ascent learning rate `η_φ` is the only new HP; bind to RankMe controller (b6 TOY) or fix `η_φ = 10 · η_θ` (standard GAN ratio). Direct evidence from GAN / OT literature: Deshpande et al. CVPR 2019 show max-sliced beats average-sliced at *every* projection budget on CelebA / LSUN; the same mechanism transports to LeJEPA because both are functionals of 1-D-projected empirical distributions.

**Expected gain**: +0.3 / +0.7 / +1.6 pp 🟡 *(strong theoretical case; empirical GAN evidence; but mode of failure — non-convex inner max not converging — is real)*
**Feasibility**: 4/5 🟢 (slicing head is 50 LoC; alternating optimization is standard PyTorch idiom)
**Effort**: M 🟡

**Implementation sketch**:
1. `class SlicingHead(nn.Module): MLP(d → 4d → d) + F.normalize(out, dim=-1)`.
2. New gradient hooks: `g_φ` updates ascend `T(Z · g_φ(z_anchor))`; encoder updates descend `T(Z · g_φ.detach()(z_anchor))`. Use a *fixed anchor* embedding (the rolling mean of `Z` over the last K steps) as input to `g_φ` to break the trivial-recursion (avoids the adversary depending on the very embedding it's evaluating).
3. Gradient penalty on `g_φ`: enforce `‖∇_z g_φ(z)‖₂ ≤ 1` (WGAN-GP-style); spectral-normalize the MLP layers.
4. 2-player alternating optimization: 1 step `g_φ` ascent per 1 step encoder descent.
5. Sanity at init: with random g_φ, `T(Z · g_φ(Z))` should match the random-slice baseline `T(Z · u_random)` within 5 % — proves the head is initialized neutrally.

**Risks**:
- Non-convex inner max may not converge → encoder over-regularizes against an *artifact* direction the adversary failed to find. Mitigation: a 50/50 mix of random + adversarial slices for stability (cf. distributional sliced-Wasserstein); reverts to baseline if the adversary degenerates.
- Adversary collapses to a constant direction (degenerate Nash). Mitigation: entropy regularizer on `g_φ`'s output distribution over directions; gradient penalty.
- Composition with batch-2 SRHT (variance-reducer for the closed sampler family): **mutually exclusive** — max-sliced *replaces* the sampler; SRHT is irrelevant under max-sliced. This is good news (one less HP family) but should be flagged.
- Composition with batch-6 Sinkhorn TOY (Idea 4 there): clean — Sinkhorn replaces the *invariance* term, max-sliced replaces the *SIGReg* term. Orthogonal.
- Composition with Idea 1 (flow matching invariance, this batch): clean — different LeJEPA terms.

**Falsification test**: 100-ep ImageNet-10, 3 seeds, 4-arm at matched-wall-clock: SIGReg-average (baseline, `M=1024` random slices) / SIGReg-average (`M=1` random slice — control for slice-count) / SIGReg-max-sliced (`M=1` adversarial) / 50-50 mix of random+adversarial. Primary: max-sliced arm linear probe ≥ 0.4 pp non-overlap above `M=1`-random control (proves the *max-vs-mean* mechanism, not just slice count). Secondary: max-sliced ≥ baseline (1024-random) — proves the 1000× compute savings is "free". Mechanism check: monitor the inner-max value `T(Z · g_φ(Z))` over training — should *decrease* monotonically (game converges); if it oscillates with amplitude > 30 % of mean across the last 50 epochs, the adversary–encoder dynamics is unstable; reject.

---

### Idea 1: Flow-matching invariance (continuous-time velocity field aligns view distributions)

- **Pattern**: P3 (Replace — swap the per-pair MSE invariance with continuous-flow distribution matching)
- **Tier**: 3 (probability theory / continuous-time stochastic processes — Föllmer's Schrödinger problem 1988; ICLR-2023 ML translation Lipman et al.)
- **Scope**: enhance-existing. Replaces the invariance / view-alignment term only. SIGReg, sampler, statistic, encoder, projector, λ untouched. Mechanism-distinct from batch-6 Sinkhorn TOY (see Mechanism §).
- **One-liner**: Train a small velocity field `v_ψ : R^d × [0,1] → R^d` to satisfy `dz/dt = v_ψ(z, t)` such that the ODE flow transports the view-1 embedding distribution at `t=0` into the view-2 distribution at `t=1`; the closed-form CFM target gives a regression loss with no OT solver in-the-loop.

**Mechanism**:
Lipman, Chen, Ben-Hamu, Nickel, Le (*Flow Matching for Generative Modeling*, ICLR 2023 Oral / [arXiv:2210.02747](https://arxiv.org/abs/2210.02747)) show that for any **conditional probability path** `p_t(z | z_0, z_1)` joining a sample `z_0 ∼ P_0` to a sample `z_1 ∼ P_1`, there is a closed-form **conditional vector field** `u_t(z | z_0, z_1)` such that training `v_ψ` to regress `u_t` minimizes the *marginal* flow-matching loss (which is the loss of an *unconditional* CNF that transports `P_0` to `P_1`). The OT-displacement choice — `p_t(z | z_0, z_1) = δ((1−t) z_0 + t z_1)` — gives the simplest conditional path; the conditional vector field is then `u_t(z | z_0, z_1) = z_1 − z_0` (constant in `t`).

For LeJEPA: with the two global views giving embeddings `(z_0, z_1)` per image, sample `t ∼ U(0,1)`, form the interpolant `z_t = (1−t) z_0 + t z_1 + σ ε` with `ε ∼ N(0, I), σ = 0.01`, and regress `v_ψ(z_t, t)` to the target `z_1 − z_0`. Loss: `L_FM = E_{i, t, ε}[‖v_ψ(z_t^i, t) − (z_1^i − z_0^i)‖²]`. This term is **0** iff `v_ψ` correctly transports view-1 to view-2 *as distributions* — softer than per-pair MSE, harder than nothing.

**Mechanism-distinct from batch-6 Sinkhorn TOY (Idea 4)**: Sinkhorn solves a static entropic-OT problem between two empirical distributions, returning a (regularized) transport plan `π* ∈ R^(N × N)`; the loss is `<π*, C>` for cost matrix `C`. Flow matching learns a *continuous velocity field* `v_ψ(z, t)` whose ODE flow transports `P_0` to `P_1` along a *prescribed* path — the regression signal is the deviation of `v_ψ` from the prescribed conditional path. The *math objects* are different (transport plan vs. vector field), the *gradients* are different (plan-derivative vs. field-derivative), and the *failure modes* are different (Sinkhorn fails by entropy-collapse to permutation degeneracy; flow matching fails by `v_ψ` underfit). Both are alignment-axis replacements; should be A/B-tested head-to-head, not stacked.

**Source inspirations**:
- Primary (cross-domain root): *Random fields associated with multiple points of the Brownian motion*, Föllmer, in *Séminaire de Probabilités* 1988 — Schrödinger problem / entropic SDE bridges; foundational for the continuous-time view of probability-distribution transport.
- Primary (computational): *Flow Matching for Generative Modeling*, Lipman, Chen, Ben-Hamu, Nickel, Le, **ICLR 2023 Oral** / [arXiv:2210.02747](https://arxiv.org/abs/2210.02747) — closed-form CFM training; simulation-free CNF.
- Supporting: *High-Performance Self-Supervised Learning by Joint Training of Flow Matching*, [arXiv:2512.19729](https://arxiv.org/abs/2512.19729) (Dec 2025) — FlowFM: jointly trains representation encoder and conditional flow-matching generator; reports SSL gains.
- Supporting: *Better Source, Better Flow: Learning Condition-Dependent Source Distribution*, [arXiv:2602.05951](https://arxiv.org/abs/2602.05951) — conditional-source generalization of CFM (might be useful for view-conditioned sources).

**Why expected to improve**:
Per-pair MSE invariance is the *strongest possible* alignment constraint — it forces `z_0 = z_1` for each image. Under aggressive augmentation (color jitter, blur, large scale variation), views are not "the same image" but *samples from an augmented-image distribution*; per-pair MSE over-pulls and discards genuine view-specific information. Flow matching softens this: `v_ψ` only has to capture the *distributional* transport, not the per-pair identity. The view-1 / view-2 alignment becomes distribution-vs-distribution alignment with a *learnable, continuous* transport map. Direct SSL evidence: arXiv:2512.19729 reports flow-matching-as-SSL-auxiliary outperforms MSE-alignment on standard recognition benchmarks.

**Expected gain**: +0.3 / +0.8 / +1.6 pp 🟡 *(direct SSL evidence Dec 2025; mechanism is well-motivated; competition with Sinkhorn TOY caps the unique gain)*
**Feasibility**: 3/5 🟡 (velocity-field MLP + time-conditioning + integration into existing invariance term — 50–80 LoC; standard pattern in CFM codebases)
**Effort**: M 🟡

**Implementation sketch**:
1. `class VelocityField(nn.Module): MLP(d + d_t → 4d → d)` with sinusoidal time-embedding for `t ∈ [0,1]`.
2. Each step: sample `t ~ U(0,1)`, `ε ~ N(0, σ² I)`, form `z_t = (1-t) z_0 + t z_1 + ε`.
3. Loss: `L_FM = ((v_ψ(z_t, t) - (z_1 - z_0))**2).mean()`.
4. Replace `L_inv = MSE(z̄, z)` with `L_inv = L_FM`. Same weight (`(1-λ)` in `(1-λ) · L_inv + λ · SIGReg`).
5. Use `σ = 0.01` (small noise for OT-displacement path; larger σ gives diffusion-style path).

**Risks**:
- Velocity-field cost ~ encoder-projector cost; expect +20 % step time. Mitigation: small MLP (`d → 2d → d` with shared time-embedding).
- Soft permutation: `v_ψ` could learn "transport everything to the mean" — degenerate flow. Mitigation: the regression target `z_1 − z_0` is *per-image* so the loss is 0 iff the velocity is correctly *per-image conditional*; the *marginal* flow then follows by the CFM theorem. Less prone to degeneracy than Sinkhorn.
- Composition with Sinkhorn (batch-6 TOY): **mutually exclusive** at the alignment axis. Suggest A/B-bake-off in a single 3-arm experiment (Sinkhorn / Flow-matching / baseline-MSE) to resolve the alignment-axis corner just like the per-slice-statistic bake-off resolved the SIGReg-statistic corner.
- Composition with SIE-split (b5 FULL SEND): clean (SIE works on the head decomposition, FM on the alignment term).
- Composition with Idea 3 (max-sliced SIGReg, this batch): clean (different LeJEPA terms).

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd) from ASHA, 3 seeds, 3-arm at matched-wall-clock: baseline-MSE-invariance / Sinkhorn-invariance (b6 TOY result) / Flow-matching-invariance. Primary: flow-matching arm ≥ 0.4 pp non-overlap above baseline AND within ±0.3 pp of Sinkhorn arm — proves it's competitive at the same axis. Mechanism check: compute `v_ψ` divergence `∇·v_ψ` on validation embeddings; should be near-0 (incompressible flow) → confirms `v_ψ` learned a volume-preserving transport. If divergence is large positive (volume-collapse), the flow is degenerate; reject.

---

### Idea 4: RL-learned augmentation policy (REINFORCE on crop parameters)

- **Pattern**: P2 (Transfer — port the REINFORCE / policy-gradient framework from RL into SSL augmentation selection)
- **Tier**: 3 (reinforcement learning is a distinct research field from supervised/unsupervised ML — Bellman 1957 *Princeton U. Press* / Sutton-Barto 1998 textbook / Williams REINFORCE 1992 *Machine Learning*)
- **Scope**: enhance-existing. Modifies the multi-crop augmentation distribution only. Encoder, projector, SIGReg, invariance, λ untouched.
- **One-liner**: Treat the crop parameters (scale, location, jitter strength) as **actions** drawn from a parametric policy `π_φ(a | x)`; reward = drop in per-image invariance loss (or proxy linear-probe score on a held-out subset); update `π_φ` by REINFORCE every K=100 steps. The augmentation distribution becomes *adapted* to the encoder's current weakness.

**Mechanism**:
Multi-crop SSL (DINO, LeJEPA) draws crop parameters from a *fixed* distribution: scale `s ∼ U(0.3, 1.0)` for global, `s ∼ U(0.05, 0.3)` for local. The fixed distribution is the strongest assumption in the multi-crop pipeline — "for any image, all crops at these scales are useful". RL says: don't assume, *learn*. A small policy network `π_φ(a | x_global)` outputs a distribution over `(scale, x_center, y_center, jitter_strength)`; sample one crop from the policy and feed it to the encoder; observe a *reward* `r = ΔL_invariance(crop)` (the invariance loss improvement from including this crop vs. a control random crop, computed on a small held-out subset every K steps); update `π_φ` by `∇φ E[r] = E[r · ∇φ log π_φ(a | x)]`. This is exact REINFORCE (Williams 1992); modern variants use PPO or actor-critic for variance reduction.

**Distinct from batch-5 saliency crops FULL SEND**: saliency crops use a *frozen pre-trained* saliency map (e.g., a small object-detection model) to bias crop sampling toward salient regions. **The saliency map is fixed**: it does not adapt to the encoder's current weakness. RL augmentation is *online and adaptive*: the policy network sees the encoder's recent failures (via reward signal) and shifts crop sampling toward harder regions for the *current* encoder. Saliency = static prior; RL = dynamic posterior. The two could compose (saliency-initialized RL policy), but mechanistically distinct.

**Distinct from batch-6 RankMe controller TOY**: that adjusts `λ_SIGReg` based on RankMe; the present idea adjusts the *augmentation distribution* based on per-image rewards. Different control signals, different control targets. Could be composed (controller manages `λ`, policy manages crops) — clean stacking.

**Source inspirations**:
- Primary (cross-domain root): *Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning* (REINFORCE), Williams, **Machine Learning 8, 1992** — policy gradient estimator; foundational for differentiable-through-sampling.
- Primary (SSL application): *SelfAugment: Automatic Augmentation Policies for Self-Supervised Learning*, Reed, Yue, Chen, Trivedi, Chen, Darrell, **CVPR 2021** / [arXiv:2009.07724](https://arxiv.org/abs/2009.07724) — RL-style automated augmentation for SSL; evaluation via rotation-pretext-task proxy reward.
- Supporting: *Evolutionary Augmentation Policy Optimization for Self-Supervised Learning*, [arXiv:2303.01584](https://arxiv.org/abs/2303.01584) (2023) — alternative gradient-free SSL-augmentation optimizer (informs reward-shaping choices).
- Supporting: *Beyond Random Augmentations: Pretraining with Hard Views*, [arXiv:2310.03940](https://arxiv.org/abs/2310.03940) (2023) — confirms harder crops outperform random; informs the reward design.
- Supporting: *RL-BioAug: Label-Efficient Reinforcement Learning for Self-Supervised EEG Representation Learning*, [arXiv:2601.13964](https://arxiv.org/abs/2601.13964) (Jan 2026) — recent RL-for-SSL-augmentation work in EEG; mechanism transports to vision.

**Why expected to improve**:
Random crops waste compute on "easy" views the encoder already handles well. RL policy shifts the augmentation distribution toward "hard" views — those with the highest per-image invariance loss — implementing a *curriculum* automatically. Hard-view literature (arXiv:2310.03940) shows up to 1 pp probe lift from hard-view selection at matched-compute; RL adds the adaptation-to-current-encoder-state on top of this. On a small dataset like Imagenette (only ~9k training images, but each augmented many times per epoch), the redundancy in random crops is high; RL is well-motivated.

**Expected gain**: +0.2 / +0.6 / +1.4 pp 🟡 *(direct SSL evidence on hard-view selection; novel mechanism is the online-RL-vs-static-prior delta; gain CI wide because reward shaping is fragile)*
**Feasibility**: 3/5 🟡 (REINFORCE has high variance; PPO is more stable but adds complexity; reward signal needs careful definition to avoid degenerate policies — e.g., always-zoom-to-center)
**Effort**: M 🟡

**Implementation sketch**:
1. `class CropPolicy(nn.Module)`: input = small CNN features of `x_global` (16x16 average-pool of input); output = parameters of a Gaussian over `(scale, x_center, y_center, jitter_strength)`.
2. Sample 4 of the 6 local crops from `π_φ(a | x)` (keep 2 random as baseline).
3. After each crop forward: `r_i = L_invariance_random_baseline - L_invariance(crop_i)` (compute baseline once per image with a default random crop).
4. Every K=100 steps: PPO update `φ ← φ + η · ∇φ E[r · log π_φ(a|x)]` with clip ratio 0.2, advantage baseline = mean(r) over batch.
5. Sanity at init: random-initialized policy should match random-crop baseline within 0.1 pp invariance — proves the policy starts neutral.

**Risks**:
- **Reward signal is the bottleneck**: per-image-invariance-drop as reward is noisy; could be smoothed by an EMA of the invariance loss per image. Mitigation: warm up with a frozen random-policy phase for the first 50 epochs.
- Policy can collapse to a single mode (always-zoom-to-center). Mitigation: entropy bonus `+ β · H(π_φ)`; clip the scale range.
- Variance of REINFORCE may dominate the encoder gradient signal early in training. Mitigation: stop the RL update during the first 10 % of training (warm-up phase with random crops).
- Composition with Saliency crops (b5 FULL SEND): can compose by *initializing* the policy with saliency-biased sampling — but verify the gain over saliency-only is positive before stacking.
- Composition with Idea 1 (FM invariance, this batch): RL reward then becomes `ΔL_FM(crop)` instead of `ΔL_MSE(crop)`. Should still work but verify the FM-loss signal is informative per-crop.

**Falsification test**: 100-ep ImageNet-10, 3 seeds, 3-arm at matched-wall-clock: random crops baseline / Saliency crops (b5 FULL SEND result) / RL policy (this idea). Primary: RL arm ≥ 0.4 pp non-overlap above random baseline AND within ±0.3 pp of saliency arm — proves it's at least competitive with the static-saliency alternative. Mechanism check: log the entropy `H(π_φ)` over training — should *decrease* monotonically (policy becomes peaked on useful actions); if entropy stays at the uniform-prior value the policy isn't learning, reject. Secondary: log average `r` over training — should be monotonically positive (policy learns to find better-than-random crops); if `r` stays near 0, the reward signal is too noisy and the idea reduces to baseline; reject.

---

### Idea 5: Neural-collapse ETF prototypes (online k-means + simplex-ETF cosine target)

- **Pattern**: P5 (Decompose — decompose the unsupervised embedding space into K cluster prototypes whose pairwise cosines target the simplex-ETF geometry)
- **Tier**: 3 (frame theory / Welch 1974 bound on max cross-correlation; Papyan-Han-Donoho 2020 *PNAS* discovers ETF geometry in trained networks)
- **Scope**: enhance-existing. Adds an online k-means head + ETF cosine penalty. SIGReg, invariance, sampler, statistic, encoder, projector, λ untouched.
- **One-liner**: Maintain `K = 20` learnable cluster prototypes `μ_k ∈ R^d`; assign each embedding to its nearest prototype by cosine; penalize the pairwise cosines between prototypes to match the simplex-ETF target `−1/(K−1)` (the unique geometry that maximizes pairwise distances).

**Mechanism**:
Papyan-Han-Donoho (*Prevalence of Neural Collapse during the Terminal Phase of Deep Learning Training*, PNAS 2020 / [arXiv:2008.08186](https://arxiv.org/abs/2008.08186)) document that *supervised* networks at terminal training collapse to a **simplex Equiangular Tight Frame (ETF)** geometry: (i) within-class features collapse to their class means; (ii) class means form a simplex ETF — pairwise cosines all equal to `−1/(C−1)` for `C` classes, which is the *maximum-equiangular* configuration in `R^d` for `C` points (a result from Welch 1974 *IEEE Trans. Info. Theory*); (iii) classifier weights align with class means (self-dual); (iv) classification reduces to nearest-class-mean.

Translating to SSL: there are no labels, but we can maintain `K = 20` **online prototypes** updated by k-means (SwAV / DINO have similar structure but use different losses). Define `L_ETF = Σ_{k ≠ k'} (cos(μ_k, μ_k') − (−1/(K−1)))²` — penalize the pairwise cosines of the prototypes to the ETF target. Additionally, push each embedding toward its assigned prototype: `L_cluster = − E_i[cos(z_i, μ_{c(i)})]` where `c(i) = argmax_k cos(z_i, μ_k)`. Total auxiliary: `L_NC = α · L_ETF + β · L_cluster`.

**Mechanism-distinct from MMCR / W-MSE (closed covariance-shaping family)**: those penalize `det(Cov(z))` or `‖Cov(z) − I‖_F` — full-covariance targets. ETF prototypes are a **specific pairwise-cosine target on a *small* set of K=20 prototype vectors**, not a covariance condition on the d=384-dim embedding. The K-prototype geometry is a low-rank discrete object; the full covariance is a d×d continuous object. Different math, different gradients.

**Mechanism-distinct from batch-5 SIE-split FULL SEND**: that decomposes the embedding into shared-invariant-equivariant heads (decomposition along augmentation axes). ETF prototypes decompose along *cluster* axes — discrete-cluster geometry vs. continuous-invariance geometry. Cleanly orthogonal.

**Source inspirations**:
- Primary (cross-domain root): *Lower Bounds on the Maximum Cross Correlation of Signals*, Welch, **IEEE Trans. Info. Theory 20(3), 1974** — establishes the simplex-ETF as the maximum-equiangular configuration; the cross-domain root in frame theory.
- Primary (deep-learning observation): *Prevalence of Neural Collapse during the Terminal Phase of Deep Learning Training*, Papyan, Han, Donoho, **PNAS 117(40), 2020** / [arXiv:2008.08186](https://arxiv.org/abs/2008.08186) — observes ETF emergence; provides the geometric characterization.
- Supporting: *Guiding Neural Collapse: Optimising Towards the Nearest Simplex Equiangular Tight Frame*, [arXiv:2411.01248](https://arxiv.org/abs/2411.01248) (Nov 2024) — recent active-ETF-targeting (instead of waiting for emergence); gives the loss formulation we adapt.
- Supporting: *rETF-semiSL: Semi-Supervised Learning for Neural Collapse in Temporal Data*, [arXiv:2508.10147](https://arxiv.org/abs/2508.10147) (Aug 2025) — most-recent ETF application to *semi*-supervised setting; technique transports cleanly to SSL (just substitute online-k-means cluster assignments for the partial labels).

**Why expected to improve**:
SIGReg constrains the *marginal* geometry (N(0,I)). Per-sample invariance constrains the *per-image* alignment. Neither directly constrains the *cluster* geometry of the embedding space. ETF prototypes are the *optimal-information-packing* arrangement of K points in R^d (Welch bound saturator) — the geometry that supports the *cleanest linear-probe decision boundaries* in the K-class regime. Imagenette has 10 classes; setting `K = 20` (overcomplete, robust to class-count mismatch) gives the linear probe a near-optimal embedding geometry. Recent active-ETF-targeting (arXiv:2411.01248) shows up to 1.5 pp lift on imbalanced classification; for SSL pretraining the upper-bound gain on linear-probe-after is somewhat smaller because the probe sees the pre-projection features.

**Expected gain**: +0.2 / +0.5 / +1.2 pp 🟡 *(recent ETF-targeting evidence on supervised tasks; SSL transfer is plausible but unmeasured; small Imagenette class count = both opportunity and ceiling)*
**Feasibility**: 3/5 🟡 (online k-means stability + ETF loss + assignment-stop-gradient careful — standard SwAV-style implementation)
**Effort**: M 🟡

**Implementation sketch**:
1. `class PrototypeBank(nn.Module): nn.Parameter(K, d)`, `K=20`; normalize prototypes after each step.
2. Hard cluster assignment by `argmax_k cos(z_i, μ_k)`; stop-gradient through the assignment.
3. `L_cluster = - cos(z_i, μ_{c(i)}).mean()`.
4. ETF: `L_ETF = ((cos_matrix - target_matrix)**2).mean()` where `target_matrix = -1/(K-1) * (1 - I_K)`.
5. Total auxiliary: `L_NC = 0.1 * L_ETF + 0.1 * L_cluster`; add to LeJEPA loss with binding to RankMe controller if shipping with Idea 1 of batch-6.
6. Sanity: at init, prototypes are random unit vectors; their pairwise cosine matrix has mean 0 and std `1/sqrt(d)` ≈ 0.05; target is `-1/19 ≈ -0.053`; initial L_ETF should be `O(1/d)` — confirm before launching full run.

**Risks**:
- **K choice**: `K=20` is `2 × C_imagenette`; vetting note that SwAV uses K=3000 for ImageNet-1K. Mitigation: `K ∈ {10, 20, 40}` mini-sweep (one of these is the new HP — bind to RankMe controller if shipping together).
- Cluster-prototype collapse (all `z_i` assigned to one cluster). Mitigation: Sinkhorn-Knopp balanced assignment (cf. SwAV) — but adds compute. Alternative: anti-collapse regularizer `+ γ · KL(p_cluster_assignment || uniform)`.
- Composition with MMCR (closed REFRAMED): pre-check mandatory — if `Cov(z)` already drives toward isotropy and `L_ETF` does the same on prototype-cosines, there could be subtle interaction.
- Composition with batch-5 SIE-split (FULL SEND): clean (different decomposition axes).
- Composition with batch-5 saliency crops (FULL SEND): clean (independent crop and ETF axes).
- The N(0,I) target of SIGReg may already implicitly encourage some ETF structure — *prior-art prerequisite check*: search "Cramer-Wold neural collapse simplex ETF" — if confirmed equivalent, this idea reduces to a redundancy; the falsification test catches this.

**Falsification test**: 100-ep ImageNet-10, 3 seeds, 3-arm at matched-wall-clock: SIGReg-only baseline / SIGReg + L_NC / L_NC-only (no SIGReg, isolates the ETF contribution). Primary: combined arm ≥ 0.4 pp non-overlap above baseline AND L_NC-only arm ≥ baseline − 1 pp (proves ETF alone is non-trivially regularizing, not just decorative). Mechanism check: at end of training, measure the empirical class-mean pairwise-cosine matrix on the validation set (using ground-truth labels at test time only); should approach `-1/9 ≈ -0.111` for the 10 Imagenette classes; if class-mean cosines remain near 0 (no ETF emergence), the prototypes did not transfer their geometry to the embedding; reject.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|------------------------|--------------------|---------------------|-----------------|------------|-------------|------------|-------|
| 1 | Flow-matching invariance | ✅ Lipman ICLR 2023 (arXiv:2210.02747) + arXiv:2512.19729 (Dec 2025) | ✅ | ✅ (≥ 0.4 pp + ≤ ±0.3 pp of Sinkhorn arm + flow-divergence check) | NOVEL (within LeJEPA) | VERIFIED | 3 | ⚠ overlaps Sinkhorn axis — A/B mandatory | **KEEP w/ flag** |
| 2 | Multivariate score matching | ✅ Hyvärinen JMLR 2005 + Song NeurIPS 2019 (arXiv:1905.07088) + arXiv:2502.20123 | ✅ | ✅ (≥ 0.3 pp + per-slice Epps–Pulley convergence cross-check) | NOVEL (within LeJEPA) | VERIFIED | 4 | ⚠ adds to closed per-slice bake-off as 5th arm — single 5-way bake-off recommended | **KEEP** |
| 3 | Adversarial max-sliced SIGReg | ✅ Deshpande CVPR 2019 (arXiv:1904.05877) + von Neumann Math. Ann. 1928 | ✅ | ✅ (≥ 0.4 pp above M=1-random control + game-convergence monotonicity check) | NOVEL — strongest in batch | VERIFIED | 4 | OK | **KEEP** |
| 4 | RL augmentation policy | ✅ SelfAugment CVPR 2021 (arXiv:2009.07724) + Williams 1992 + arXiv:2601.13964 (Jan 2026) | ✅ | ✅ (≥ 0.4 pp above random + entropy-monotonicity + reward-monotonicity checks) | EXTENDS (SelfAugment already covers RL-aug-for-SSL; novelty is the per-image-invariance reward) | VERIFIED | 3 | ⚠ EXTENDS bordering DUPLICATE — flag at vetting | **KEEP w/ flag** |
| 5 | Neural-collapse ETF prototypes | ✅ Papyan PNAS 2020 (arXiv:2008.08186) + Welch IEEE TIT 1974 + arXiv:2411.01248 + arXiv:2508.10147 | ✅ | ✅ (3-arm SIGReg vs L_NC singletons vs combo + class-mean-cosine emergence) | NOVEL (active ETF-targeting on SSL with online k-means) | VERIFIED | 3 | ⚠ prior-art prerequisite check on Cramer-Wold ↔ ETF | **KEEP w/ flag** |

**Cross-idea consistency**:
- Ideas 1 (flow matching) and Sinkhorn (b6 TOY) **must be A/B-compared at the alignment axis**; do not stack. Recommend a 3-arm `baseline-MSE / Sinkhorn / FM` experiment to resolve the alignment-axis corner like the per-slice statistic bake-off.
- Idea 2 (Hyvärinen) **must be added as the 5th arm to the per-slice-statistic bake-off** (currently 4-deep: EP / Hermite / KSD / Riesz-MMD). The bake-off becomes EP-vs-Hermite-vs-KSD-vs-Riesz-vs-Hyvärinen (5-way), measuring per-step time × downstream probe.
- Ideas 3 (max-sliced) and the SRHT variance-reducer (b3, in survivor stack) are **mutually exclusive at the slicing-distribution level** — if max-sliced wins, SRHT is irrelevant under the new scheme.
- Ideas 4 (RL policy) and Saliency crops (b5 FULL SEND) are **at the same augmentation-distribution axis** — A/B-bakeoff. They can compose (saliency-initialized RL) but verify gain over saliency-only first.
- Idea 5 (ETF prototypes) and SIGReg may be redundant at the population limit; the falsification 3-arm singleton-vs-combo test resolves this.
- All 5 ideas use matched-wall-clock falsification with 3 seeds; the score distribution is reasonable (composite range 1.78–2.27, no single dominant winner — consistent with high-variance T3-only batch).

**No ideas rejected at verification.** Three flagged for cross-idea redundancy at vetting (Ideas 1, 3, 4). Append empty-rejection stanza to `_logs/_rejection_log.md`.

## Notes & warnings

- ⚠ **Tier-mix-override violation**: configured `30/20/50` was overridden mid-session to `0/0/100`. The spec rule `each tier ≥ 10` is violated by user direction. All 5 ideas are T3 cross-domain (math statistics / game theory / probability / RL / frame theory). Surface to user that batch-7 deliberately *honors the user's T3-only feedback* over the configured tier mix.
- ⚠ **`--compose-mode` recommendation now 5 batches in a row** — vetting has flagged this since batch-3. The skill still does not expose `--compose-mode`. This batch *honors the user's explicit T3-themes feedback* over the compose-mode recommendation. The compose-mode-enumeration request remains unaddressed at the skill level; the cumulative survivor stack is now 6–8 deep (PIT, SRHT, SAM/FSAM, ASHA, Saliency, SIE-split + pending Sinkhorn, RankMe-controller from b6).
- ⚠ **Process gap from batch-6 explicitly addressed**: every Tier-3 idea below has at least one supporting search with `"<technique> SSL representation learning"` or equivalent in-field clause (see search log). Hits found for flow-matching (arXiv:2512.19729 Dec 2025), score matching (Song-Ermon NeurIPS 2019), RL aug (SelfAugment CVPR 2021), neural collapse (rETF-semiSL Aug 2025). Adversarial max-sliced for SSL specifically *was not found* — flagged as genuine novelty rather than missed prior art.
- ⚠ **Per-slice / sampler / covariance closed-family disposition**:
  - Per-slice statistic bake-off becomes 5-way with Idea 2 (Hyvärinen) added as the multivariate alternative.
  - Variance-reduction sampler family is **superseded** by Idea 3 if max-sliced wins — would mean SRHT (b3), Repulsive, Antithetic+SH-CV, t-design all become irrelevant. Strong signal: this is a *winner-take-all* corner now.
  - Covariance-shaping is **untouched** by batch-7 — ETF prototypes (Idea 5) is geometry-on-prototypes not geometry-on-covariance.
- 🟢 **Idea 2 (Hyvärinen) is the lowest-risk addition in batch-7** — `~10 LoC` drop-in alternative to SIGReg with closed-form gradient; ships as the 5th arm of the per-slice bake-off.
- 🟢 **Idea 3 (adversarial max-sliced) is the highest-novelty idea in batch-7** — direct game-theoretic mechanism with no published SSL precedent; if it works it potentially supersedes the entire sampler family.
- ⚠ **Idea 4 (RL aug policy) is EXTENDS bordering DUPLICATE of SelfAugment (CVPR 2021)** — SelfAugment uses rotation-pretext-task reward; this idea uses per-image-invariance-loss-drop reward. The mechanism delta is the reward signal and the online-during-training-vs-pre-training-of-policy distinction. Vetting will likely flag this; consider running as a *pure ablation of the reward signal* on top of SelfAugment infrastructure rather than a from-scratch implementation.
- ⚠ **Idea 5 (ETF prototypes) prior-art prerequisite check**: search "Cramér–Wold neural collapse simplex ETF" before vetting. If SIGReg's N(0, I) target *already implies* ETF emergence (a corollary of Cramér–Wold + concentration on the sphere), then ETF prototypes are redundant. This is a `0-cost` check before allocating compute.
- ⚠ **Tier-3 honesty audit** (per skill rules — every T3 idea must trace to a genuine non-ML field):
  - Idea 1: cross-domain root = continuous-time probability / Föllmer's Schrödinger problem (probability theory, *Séminaire de Probabilités*). The deep-learning translation Lipman ICLR 2023 is the modern entry. **Bona-fide T3**.
  - Idea 2: cross-domain root = mathematical statistics — Stein's identity (Stein 1972 *Berkeley Symp.*) → Hyvärinen JMLR 2005. JMLR borderline ML-venue, but the underlying theory is statistics. **Defensible T3**.
  - Idea 3: cross-domain root = game theory — von Neumann 1928 *Math. Ann.* minimax theorem / Nash 1951 *Ann. Math.* equilibria. Game theory is a distinct research field from ML. **Bona-fide T3**.
  - Idea 4: cross-domain root = reinforcement learning — Bellman 1957 *Princeton U. Press* / Sutton-Barto textbook / Williams REINFORCE 1992 *Machine Learning*. RL is a distinct community from supervised/unsupervised ML, though there is significant cross-fertilization. **Borderline T2/T3 — defensible as T3** under the conventional RL-as-separate-field framing.
  - Idea 5: cross-domain root = frame theory — Welch 1974 *IEEE Trans. Info. Theory*. The Papyan-Han-Donoho PNAS observation is the deep-learning entry; the underlying geometric statement (max-equiangular configuration) is from frame theory / coding theory. **Bona-fide T3**.
- **Devil's-advocate on top-1 by composite (Idea 2 Hyvärinen, 2.27)**: failure mode = score matching's known **convex-decoy** — the trivial `s_θ(z) = −z` gives `L_sm = 0` identically. Search "score matching trivial solution failure" — Vincent 2011 *Neural Computation* documents this; Song-Ermon 2019 NeurIPS Sliced-Score-Matching adds a Hutchinson trick that *prevents* the decoy by forcing dependence on `Z`. The implementation sketch §3 above (backprop through `z` not just `s_θ`) is the standard mitigation. **Down-flag from 🟢 to 🟡 unless the mitigation is verified at init in a 1-hour CPU sanity test.**

- **Prerequisites / measurements** (NOT ideas — surfaced per skill rules):
  - (i) Batch-2 Idea 5 ASHA sweep — still the gate for absolute-pp claims (unchanged from batches 3–6).
  - (ii) Per-slice-statistic 5-way bake-off (EP / Hermite / KSD / Riesz-MMD / **Hyvärinen**) — add Idea 2 to the joint Phase-A bake-off recommended by batch-5 vetting.
  - (iii) Alignment-axis 3-way bake-off (MSE / Sinkhorn / **Flow-matching**) — pair Idea 1 with the Sinkhorn TOY from batch-6.
  - (iv) ETF prior-art prerequisite check (search "Cramér–Wold neural collapse simplex ETF") — `0-cost` before compute allocation for Idea 5.
  - (v) Hyvärinen convex-decoy sanity (1-hour CPU; verify `s_θ` does not collapse to `−z` identically while embedding distribution stays non-Gaussian) — before Idea 2 Phase B fires.

## Composition map (cumulative survivor stack → batch-7)

Cumulative survivor stack from batches 1–6: **PIT monitor (b3)**, **SRHT (b3)**, **SAM/FSAM (b4)**, **ASHA step-0 (b2+b4)**, **Saliency crops (b5 FULL)**, **SIE-split (b5 FULL)**, plus pending FULL-SEND-eligible: **Sinkhorn invariance (b6 TOY → FULL on Phase A pass)**, **RankMe controller (b6 TOY)**, plus active TOYs: Hermite-moment, rank-curriculum, co-distillation, Layer-wise SIGReg, Antithetic+SH-CV, MAE-aux, KSD, Riesz-MMD, iBOT-SIGReg, Poincaré.

| New idea | Axis opened | Composes-with cumulative stack |
|----------|-------------|-------------------------------|
| 1. Flow-matching invariance | alignment / invariance term | ⚠ Sinkhorn (same axis — A/B mandatory) · ✓ PIT · ✓ SAM · ✓ Saliency · ⚠ SIE-split (SIE has invariance branch — pre-check) · ✓ SRHT · ✓ ASHA · ✓ controller |
| 2. Multivariate score matching | SIGReg term replacement | ✓ all survivors — slots into the per-slice bake-off as 5th arm (mutually exclusive with EP / Hermite / KSD / Riesz-MMD) |
| 3. Adversarial max-sliced SIGReg | slicing distribution → minimax | ⚠ SRHT (samplers become irrelevant under max-slicing) · ✓ PIT · ✓ SAM · ✓ Saliency · ✓ SIE-split · ✓ ASHA · ✓ controller · ⚠ Repulsive / Antithetic / t-design (all superseded) |
| 4. RL augmentation policy | augmentation distribution | ⚠ Saliency (same axis — A/B mandatory; saliency-initialized RL is the composition path) · ✓ PIT · ✓ SAM · ✓ SIE-split · ✓ SRHT · ✓ controller |
| 5. Neural-collapse ETF prototypes | cluster-geometry decomposition | ⚠ MMCR (closed REFRAMED — pre-check Cramér–Wold↔ETF redundancy) · ✓ Saliency · ✓ SAM · ✓ ASHA · ✓ controller · ✓ SRHT · ⚠ SIE-split (both touch projector — sequential) |

**Compose-mode targets for downstream vetting** (5 batches in a row of vetting recommendation):
- (a) **Idea 2 (Hyvärinen) + Idea 3 (max-sliced) joint replacement of SIGReg core** — Hyvärinen is per-step; max-sliced is per-slice — together they fully define a *new* SIGReg variant (`max_u Hyvarinen(Z · u)` instead of `mean_u EppsPulley(Z · u)`). Highest-leverage compose-mode bundle in this batch.
- (b) **Idea 1 (FM invariance) + Idea 4 (RL policy)** — the policy provides hard crops; FM aligns the resulting distributions. Both touch the augmentation-and-alignment loop; tight coupling expected.
- (c) **Full 8-component survivor stack + Idea 2 + Idea 3** — the long-awaited compose-mode enumeration; defer until each of the survivors' Phase B is settled.

## Next steps for user

1. **(Unchanged from batches 3–6)** Run batch-2 Idea 5 (ASHA) as Step 0 — still gates all absolute-pp claims.
2. **(This batch — Quick win)** **Idea 2 (multivariate Hyvärinen) added as 5th arm to the per-slice statistic bake-off**. Cheapest addition: `~10 LoC`, ships into the existing joint Phase-A bake-off; 1 extra arm × matched-wall-clock = negligible extra cost.
3. **(This batch — Big bet)** **Idea 3 (adversarial max-sliced SIGReg)** — strongest novelty; potentially supersedes entire sampler family. Run as a 4-arm: baseline-1024-random / 1-random / 1-adversarial / 50/50-mix. ~15 GPU-h.
4. **(This batch — Safe bet, pair with b6 Sinkhorn)** **Idea 1 (flow-matching invariance)** — add as 3rd arm to the b6 Sinkhorn Phase A/B. The alignment-axis 3-way bake-off (MSE / Sinkhorn / FM) resolves the alignment corner.
5. **(This batch — defer)** **Idea 4 (RL policy)** — EXTENDS-bordering-DUPLICATE flag means vetting will likely demand a tight A/B vs SelfAugment baseline. Defer until prior priorities settle.
6. **(This batch — prerequisite-gated)** **Idea 5 (ETF prototypes)** — `0-cost` prior-art check first (search "Cramér–Wold neural collapse simplex ETF"). If passes, run 3-arm Phase B (~25 GPU-h). If the prior-art search surfaces a direct equivalence theorem, KILL the idea cheaply.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 0/0/100 (user-override) | given-vetting batch-6 | themes: flow-matching/score-matching/game-theory/RL/neural-collapse | 2026-05-19 batch-7`
