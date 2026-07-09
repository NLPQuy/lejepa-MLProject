# Idea Batch 5 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~25 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 30/20/50 --given-vetting .claude/skills/idea-vetting/vetting-output/ImageNet-10/batch-4/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1).
- Task: in-domain SSL pretraining, frozen-backbone linear probe per [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py).
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (EppsPulley × 1024 Gaussian random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=4e-4 wd=5e-2, fp16, 600 epochs. Baseline still TBD (gated by batch-2 Idea 5 ASHA).
- Scope: **enhance-existing**.
- Tier mix (configured): **30 / 20 / 50** — bands T1 20–40 %, T2 10–30 %, T3 40–60 %. Heavy cross-domain bias.
- Compute / time / constraint budget: 1 × A100, ≤ 4 GPU-h per 100-ep ViT-S run; soft "single-λ" branding.

### Given vetting feedback applied (batch-4 → batch-5)
- ✅ Batch-4 outcome: 1 FULL SEND (SAM/Friendly-SAM), 3 TOY (Layer-wise SIGReg, Antithetic+SH CV, MAE aux), 2 REFRAME (W-MSE pre-step, Repulsive MC). Survival 67 % — inside healthy band.
- ⚠️ **Two REFRAME signals flagged skill-drift**: (a) redundancy-with-SIGReg theoretical pre-check (W-MSE was caught), (b) variance-reduction *family* coverage across batches (Repulsive vs SRHT collision was caught). Batch-5 applies both pre-checks: every idea is audited against the cumulative survivor stack (PIT monitor, SRHT, SAM, ASHA, FSAM, W-MSE, layer-wise SIGReg, antithetic+CV, MAE-aux) for either kind of redundancy before drafting. See `Notes & warnings` for explicit annotations on Ideas 1 (variance-reduction-family overlap) and 3 (covariance-shaping overlap).
- ⚠️ Pattern coverage cumulative across batches 1+2+3+4 = P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12. Batch-5 deliberately covers a *new pattern instance* in P8 (Augment) at the data-side — only batch-1 visited P8 previously; new mechanism. P9 / P10 / P11 remain unsuited to in-domain pretraining.
- ⚠️ Vetting recommended `--compose-mode` for batch-5. Skill does not yet expose this flag, but every idea is tagged for *compose-with-survivor-stack* compatibility at the end (§Composition map), so the next vetting cycle can run combinations.
- ⚠️ Tier-mix override 30/20/50: T3 quota at 50 % is aggressive. T3 ideas in this batch trace to **discrete geometry on the sphere (Annals of Mathematics)**, **Stein's method (probability theory / mathematical statistics)**, and **theoretical neuroscience (manifold capacity / Chung-Sompolinsky)** — all bona-fide non-ML source fields, not "mainstream ML adjacent".

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Search-tier T1 / T2 / T3 (counts) | 2 / 1 / 3 → 33 / 17 / 50 % |
| Tier mix vs configured | 33/17/50 vs 30/20/50 (each within ±10 pp band) ✅ |
| Scope mix | 6 enhance-existing / 0 greenfield ✅ |
| Patterns used | P1, P2, P3 (×2), P5, P8 — 5 distinct, max 2 per pattern ✅ |
| Mandatory pattern check | ≥1 P2 ✅ (Idea 2) · ≥1 P6 ❌ — see note |
| Distinct venues | 7 (Annals of Mathematics, ICML, NeurIPS, JMLR, OpenReview/ICLR, arXiv preprint, ICCV) |
| Time windows | <12 mo: 2 · 12–36 mo: 2 · 36–72 mo: 1 · classics: 1 |
| Avg feasibility | 3.8 / 5 |
| Avg confidence | 🟢 17 % · 🟡 67 % · 🔴 17 % |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|-----------:|-----:|:------:|------:|
| 1 | **Spherical t-design** deterministic slice quadrature on S^(d−1) | P3 | 3 | +0.5 | 4 | S | **2.4** |
| 2 | **Kernelized Stein Discrepancy** as per-slice normality statistic | P2 | 3 | +0.7 | 3 | M | **2.2** |
| 3 | **MMCR auxiliary** (manifold-capacity volume loss) alongside SIGReg | P1 | 3 | +1.0 | 4 | M | **2.5** |
| 4 | **Sliced MMD with Riesz kernels** replacing EppsPulley statistic | P3 | 2 | +0.6 | 4 | S | **2.4** |
| 5 | **SIE-style invariant + equivariant split head** (predict augmentation) | P5 | 1 | +0.9 | 4 | M | **2.5** |
| 6 | **Saliency-guided / ContrastiveCrop** region sampling for the 2 global crops | P8 | 1 | +0.8 | 5 | S | **2.7** |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` · S=4 M=3 L=2.

## Top-3 recommendations

### ⚡ Quick win — **Idea 6: Saliency-guided crop region sampling**
Drop-in change to the global-crop sampler: replace `RandomResizedCrop(scale=0.3–1.0)` with a *saliency-weighted* sampler (ContrastiveCrop / saliency-as-prior). Zero new HPs, S effort, T1 publication evidence. The standard DINO multi-crop wastes a non-trivial fraction of "global" views on background sky / fur texture — on ImageNet-10 (Imagenette: object-centric 10-class), object-aware cropping is published to add **~1 pp** linear probe with no architectural change.

### 🛡️ Safe bet — **Idea 5: SIE-style invariant + equivariant split predictor**
Add a 2-layer MLP head that predicts the augmentation parameters (rotation angle, color-jitter strengths, blur σ) from `(z_view1, z_view2)`. The encoder is then constrained to retain *equivariant* information about the transformation, decomposing the embedding into an invariant subspace (used by the linear probe) and a transformation-coding subspace. Garrido / Najman / LeCun's SIE paper (arXiv:2302.10283) shows this *improves* downstream linear probe vs invariance-only on 3DIEBench; the 2026 follow-up (arXiv:2503.18753) confirms with equivariance-coherence on standard SSL. Composes cleanly with SIGReg (invariance term gets a new partner — equivariance term — but SIGReg stays on the full `z`).

### 🏆 Big bet — **Idea 3: MMCR auxiliary (manifold-capacity volume loss)**
Add Yerxa / Kuang / Simoncelli / Chung's **Maximum Manifold Capacity Representation** objective `−tr(Σ_⨁) + β·tr(Σ_⊖)` (sum over augmented-view manifolds of intra-class compactness minus inter-class spread, derived from Chung–Sompolinsky manifold-capacity theory in theoretical neuroscience) as a small auxiliary term. MMCR is a *direct neural-coding-theoretic* objective — distinct mechanism from SIGReg's distributional pull. arXiv:2303.03307 shows MMCR alone matches SimCLR/BYOL at ResNet-50/IN1K. As an auxiliary on top of SIGReg, the expected lift is bounded by the published MMCR-vs-VICReg deltas (~1 pp at small scale). Mid-effort because the manifold construction needs ≥ 4 views per anchor.

---

## Ranked ideas

### Idea 1: Spherical t-design deterministic slice quadrature

- **Pattern**: P3 (Replace — swap i.i.d. Gaussian / SRHT / repulsive sampling with a *deterministic* spherical t-design point set)
- **Tier**: 3 (numerical analysis / discrete geometry on the sphere — Annals of Mathematics line; not ML)
- **Scope**: enhance-existing. Replaces only `SlicingUnivariateTest._sample_slices`. Statistic, λ, projector, optimizer untouched.
- **Cross-domain transfer**: discrete geometry on S^(d−1) → SIGReg slice sampler.
- **One-liner**: Use Bondarenko–Radchenko–Viazovska's existence theorem and Womersley's numerical constructions to place M slice directions as a spherical t-design — equal-weight quadrature that integrates *every polynomial up to degree t exactly* — instead of i.i.d. Monte Carlo.

**Mechanism**:
A spherical t-design is a finite set `{u_1, …, u_M}` on S^(d−1) such that the equal-weight average of any polynomial of degree ≤ t over the set equals its exact integral over the sphere. Bondarenko–Radchenko–Viazovska (*Optimal asymptotic bounds for spherical designs*, Annals of Mathematics 2013) proved the existence of spherical t-designs with `M ≥ c·t^(d−1)` points for all dimensions, settling the Korevaar–Meyers conjecture. Womersley (*Efficient Spherical Designs with Good Geometric Properties*, [SIAM J. Numer. Anal. 2017 / arXiv:1709.01624](https://ar5iv.labs.arxiv.org/html/1709.01624)) gives numerical constructions for d=3 with `M ≈ (t+1)²/2`; high-d constructions are available via the same line ([numerical integration over unit sphere with t-designs, arXiv:1611.02785](https://arxiv.org/abs/1611.02785)). For SIGReg, the test functional `T(u^T Z)` can be Taylor-expanded around 0 in the slice direction; a t-design exactly integrates the first `t` polynomial terms — equivalent to "free MC variance reduction" of the leading harmonic components without any random sampling at all. This is the **deterministic corner** of the slice-VR design space (stochastic alternatives: SRHT — batch-3 Idea 2; Repulsive MC — batch-4 Idea 5; Antithetic + SH-CV — batch-4 Idea 4). Cramér–Wold is preserved: equal-weight average over a t-design with `t ≥ 2L` exactly integrates the order-L spherical-harmonics expansion of `E[T(u^T Z)]`, so the population SIGReg loss is reproduced with zero bias for low-order behaviour.

**Source inspirations**:
- Primary: *Optimal asymptotic bounds for spherical designs*, Bondarenko, Radchenko, Viazovska, **Annals of Mathematics 178 (2013)** — proves spherical t-designs exist with M ≥ c·t^(d−1); foundational existence theorem.
- Primary: *Efficient Spherical Designs with Good Geometric Properties*, Womersley, [arXiv:1709.01624](https://ar5iv.labs.arxiv.org/html/1709.01624) — numerical constructions usable as drop-in tables. Pair with [arXiv:1611.02785](https://arxiv.org/abs/1611.02785) (*Numerical integration over the unit sphere by using spherical t-design*).
- Supporting: *A Survey on Spherical Designs: Existence, Numerical Constructions, and Applications*, [arXiv:2601.11963](https://arxiv.org/html/2601.11963v1) (2026 survey) — gathers high-d constructions and computational pipelines.

**Why expected to improve**:
At fixed M, deterministic exact-polynomial integration is strictly better (zero MC variance for any test functional of polynomial degree ≤ t) than stochastic schemes — including SRHT and repulsion. For SIGReg's EppsPulley statistic, the leading terms in the slice expansion are exactly the moments of `u^T Z`; t-design with `t ≥ 4` exactly integrates the 4th-moment term that drives kurtosis-sensitivity in EppsPulley. The 2025 repulsive-MC paper (batch-4 Idea 5) already places the stochastic ceiling; t-designs improve over that by replacing "asymptotic variance decay" with "zero variance up to degree t". Mid-gain claim conservative because the random-slicing approach already converges fast for d=384 at M=1024; the win is *stability + reproducibility* and a sharper finite-M bias.

**Expected gain**: +0.1 / +0.5 / +1.2 pp 🟡 *(stability + reproducibility win; similar mid to batch-4 Idea 4/5 because the same dimensional family is being optimised)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢 (precompute the t-design table once for (d=384, M=1024); cache as constant tensor)

**Implementation sketch**:
1. Generate / load a spherical t-design for `(d, M, t = 6)` using Womersley's construction or a SDP relaxation on the harmonic moments (one-time CPU job, ≤ 1 hr per (d, M)).
2. Add `slice_generator: Literal["gaussian", "srht", "repulsive", "t_design"]` to `SlicingUnivariateTest`.
3. Train 100 ep at fixed ASHA-best (λ, lr, wd); compare to baseline Gaussian and to SRHT (if shipped) on same compute.
4. The cached t-design *cannot be re-sampled per step*; this is its defining property. Schedule a small random rotation `R ∈ SO(d)` applied to the t-design every epoch to retain Cramér–Wold-style coverage without losing the exact-integration property (uniform R averages any directional bias to zero).

**Risks**:
- **Variance-reduction-family overlap** with batch-3 SRHT, batch-4 Repulsive, batch-4 Antithetic+SH-CV (⚠️ explicitly flagged per batch-4 vetting). Position: t-design is the *deterministic corner*; the experiment value is a 4-way A/B/C/D head-to-head, **not** stacking with the other three.
- t-design table generation in d=384 with t ≥ 6 is non-trivial (`M ≥ c·6^383` lower bound is meaningless in practice — usable constructions use `t ≤ d / log d` heuristically). Fall back to small-t (t=4): exact for 4-moment EppsPulley contribution, MC for higher.
- The fixed (per-epoch) ensemble risks SIGReg "memorising" the slice geometry. Mitigation: random rotation per epoch (step 4 above).

**Falsification test**: 100-ep ImageNet-10, 4-arm head-to-head: Gaussian / SRHT / repulsive / t-design at matched M = 1024, 3 seeds each, fixed (λ, lr, wd). Primary: SIGReg-loss running-std over last 20 epochs must be ≥ 20 % lower than Gaussian *and* ≥ 10 % lower than the best of SRHT/repulsive. Secondary: linear probe within ±0.3 pp parity OR better. If t-design loses on both axes, it is dominated by stochastic VR — reject.

---

### Idea 2: Kernelized Stein Discrepancy as per-slice normality statistic

- **Pattern**: P2 (Transfer — port Stein's method from probability theory / mathematical statistics)
- **Tier**: 3 (Stein's method: Charles Stein (1972) Annals of Math Stat; KSD originally Liu-Lee-Jordan ICML 2016 — but the *method* and the target use of "goodness-of-fit for an unnormalised density" are from mathematical statistics; recent KSD theory papers are in *Statistics & Computing*, *Annals of Statistics*, *J. Mach. Learn. Res.*)
- **Scope**: enhance-existing. Replaces the per-slice statistic `T` inside `SlicingUnivariateTest`. Slicing geometry, λ, projector, optimizer untouched. Distinct from batch-3 Idea 5 (Hermite moments) — KSD uses the score of N(0,1) directly, not a polynomial expansion.
- **Cross-domain transfer**: Stein's method (probability theory) → SIGReg per-slice goodness-of-fit.
- **One-liner**: Replace EppsPulley's empirical-CF distance with the Kernelized Stein Discrepancy `KSD²(h_m, N(0,1))` per slice — a Stein-operator-based goodness-of-fit statistic whose squared form has a closed-form double-sum estimator that is *zero in expectation iff the slice is exactly Gaussian*.

**Mechanism**:
Stein's identity for N(0, 1): for any sufficiently smooth `f`, `E_{X∼N(0,1)} [f'(X) − X·f(X)] = 0`. The Kernelized Stein Discrepancy of a sample `{h_i}_{i=1}^N` against N(0,1) is
`KSD²(h, N(0,1)) = (1/N²) Σ_{i,j} k_p(h_i, h_j)`
where `k_p(x, y) = (∂_x ∂_y + ∂_x s_p(y) + ∂_y s_p(x) + s_p(x) s_p(y)) k(x, y)` is the Stein-kernel built from a base kernel `k` (e.g. RBF) and the score `s_p(x) = ∂_x log p(x) = −x` of N(0,1). This is the textbook KSD of Liu-Lee-Jordan ([arXiv:1602.03253](https://arxiv.org/abs/1602.03253), ICML 2016). For SIGReg, replace EppsPulley(`h_m`) with `KSD²(h_m, N(0,1))`. Properties: (i) closed-form, fully differentiable, no integration grid `t_max`; (ii) `= 0` iff `h_m ∼ N(0,1)` (under standard regularity); (iii) the only HP is the kernel bandwidth `σ` (heuristic: median-distance); (iv) cost per slice is `O(N² · K_eval)` where K_eval is the kernel evaluation cost — same order as EppsPulley's `O(N · n_points)` for typical (N, n_points). Cramér–Wold preserved: KSD per slice is a valid univariate normality test, applied independently to each direction.

**Source inspirations**:
- Primary: *A Kernelized Stein Discrepancy for Goodness-of-fit Tests*, Liu, Lee, Jordan, ICML 2016 / [arXiv:1602.03253](https://arxiv.org/abs/1602.03253) — foundational KSD construction; the Stein-kernel formula and the unbiased U-statistic estimator.
- Primary: *Using Perturbation to Improve Goodness-of-Fit Tests based on Kernelized Stein Discrepancy*, Liu, Duncan, Gandy, [arXiv:2304.14762](https://hf.co/papers/2304.14762) (2023) — addresses KSD's known low-power failure mode (similar modes / different mixing) via Markov perturbations; relevant fix if vanilla KSD under-performs.
- Supporting: *A kernel Stein test of goodness of fit for sequential models*, Baum, Kanagawa, Gretton, [arXiv:2210.10741](https://hf.co/papers/2210.10741) (2022) — variable-dimension Stein test; helpful framing for the multi-slice combination.

**Why expected to improve**:
Two distinct edges over EppsPulley. **(1) No integration grid.** EppsPulley uses a fixed `n_points=17` trapezoid grid over `[0, t_max]`; KSD has no such grid and is a pure pairwise statistic. The fixed grid is a known approximation source ([CLAUDE.md] notes "must be odd" — there is no reason an oddness condition should matter except that it indexes a trapezoid quadrature). **(2) Score-aware.** EppsPulley measures the CF-distance; KSD measures Stein-discrepancy and is *directly* sensitive to the score function of N(0,1), which is exactly what we want the embedding to match. Power against tail mis-specification is higher than CF-based tests (per Liu-Lee-Jordan, KSD beats Anderson–Darling / Cramér–Von Mises on a battery of non-Gaussian alternatives). Risk: KSD's known low-power failure case is "same modes, wrong mixing" — but the SSL embedding under SIGReg should not look like that during normal training; if it does, the 2023 perturbation-KSD fix applies.

**Expected gain**: +0.2 / +0.7 / +1.5 pp 🟡 *(replacing the *statistic* has a higher ceiling than replacing the *sampler* — but most published KSD-vs-EP comparisons are on synthetic data; small-data SSL transfer is unmeasured)*
**Feasibility**: 3/5 🟡 (O(N²) double sum may be expensive at batch=512; mitigate via random-Fourier-features KSD or down-sampling per slice)
**Effort**: M 🟡

**Implementation sketch**:
1. New `KSDNormality(kernel="rbf", sigma="median")` univariate test inheriting `UnivariateTest`.
2. `forward(h)`: compute median-heuristic bandwidth on `h` (or fix `σ = 1.0`); evaluate the Stein-RBF kernel matrix; return the U-statistic.
3. Swap in via `SlicingUnivariateTest(univariate_test=KSDNormality(), num_slices=1024)`.
4. Ablate `σ ∈ {0.5, 1.0, 2.0}` and the median heuristic.

**Risks**:
- O(N²) cost: at N=512, that's 262k kernel evals per slice × 1024 slices ≈ 250M ops/step, vs EppsPulley's ~9k ops/step. ~10× slower at the SIGReg call. Mitigation: stochastic mini-block KSD (subsample 64 of 512 per slice) drops cost 8×; or random-Fourier KSD.
- Kernel bandwidth is a *new HP* — violates the "near-single-λ" branding. Mitigation: median-heuristic fully removes it.
- Composition with Hermite-moment statistic (batch-3 Idea 5 TOY): these are alternative statistics on the same slice; head-to-head, do not stack.

**Falsification test**: Synthetic-data sanity (off-training, 1 hour CPU): inject `h ∼ N(0,1) + 5 % skew`; KSD power at α=0.05 must be ≥ 1.5× higher than EppsPulley at matched N. Then 100-ep ImageNet-10, baseline EppsPulley vs KSDNormality at fixed (λ, lr, wd), 3 seeds; primary: linear probe ≥ 0.4 pp higher with non-overlapping CIs; secondary: SIGReg loss converges in ≤ 80 % of baseline epochs (lower-bias statistic should converge faster). If synthetic-power test fails the implementation is wrong; reject.

---

### Idea 3: MMCR auxiliary — manifold-capacity volume loss alongside SIGReg

- **Pattern**: P1 (Combine — add a *neural-coding-theoretic* auxiliary objective with distinct mechanism)
- **Tier**: 3 (theoretical neuroscience — Chung-Sompolinsky manifold-capacity theory, *Physical Review X 2018*; ventral-stream / Simoncelli lab line. Not adjacent ML.)
- **Scope**: enhance-existing. Adds a small auxiliary term `α · L_MMCR` to the existing `L_LeJEPA`; encoder, SIGReg, λ unchanged per-component. Distinct from batch-4 Idea 6 (MAE-aux) which adds *pixel*-recon; MMCR is a *capacity-theoretic geometric* term.
- **Cross-domain transfer**: theoretical neuroscience (linear-classification capacity of manifolds in high-d cortex models) → SSL embedding shape objective.
- **One-liner**: Add the Maximum Manifold Capacity Representations objective `L_MMCR = −tr(σ_+) + β · tr(σ_−)` over the per-image augmented-view manifold, complementing SIGReg's distributional pull with an explicit manifold-volume / capacity term.

**Mechanism**:
Chung & Sompolinsky (*Phys. Rev. X 2018*) defined the *manifold capacity* of a set of class manifolds in a representation space as the maximum number of binary dichotomies linearly separable per ambient unit — a quantity from theoretical neuroscience that directly predicts downstream linear-probe accuracy. MMCR (Yerxa, Kuang, Simoncelli, Chung, [arXiv:2303.03307](https://hf.co/papers/2303.03307), 2023) operationalises this for SSL: for each image, form an *augmented-view manifold* by collecting K augmented features `Z_i ∈ R^d`; its nuclear-norm `‖Z_i‖_*` is a proxy for the manifold's effective volume. The MMCR loss maximises the *batch-wide* nuclear norm of stacked-augmentation tensors `‖concat_i (Z_i)‖_*` (spreading manifolds apart) while minimising each per-image `‖Z_i‖_*` (compactifying each manifold). The two-term objective `−tr(σ_+) + β · tr(σ_−)` is conceptually orthogonal to SIGReg: SIGReg makes the *marginal* of `Z` Gaussian per slice; MMCR makes the *per-image augmentation manifold* small and the *between-image cloud* large — a manifold-geometric statement, not a distributional one. arXiv:2303.03307 shows MMCR alone matches SimCLR/BYOL at ResNet-50/ImageNet-1K *without* a distributional regulariser; as an auxiliary on top of SIGReg, the upside is set by the MMCR-vs-VICReg gap on small-data linear probe.

**Source inspirations**:
- Primary: *Learning Efficient Coding of Natural Images with Maximum Manifold Capacity Representations*, Yerxa, Kuang, Simoncelli, Chung, [arXiv:2303.03307](https://hf.co/papers/2303.03307) (2023) — the SSL operationalisation of manifold-capacity theory; loss formula, experimental setup.
- Supporting: Chung, Lee, Sompolinsky, *Phys. Rev. X 8, 031003* (2018) — manifold-capacity theory; cross-domain root.
- Supporting: *Improve Representation for Imbalanced Regression through Geometric Constraints*, [arXiv:2503.00876](https://hf.co/papers/2503.00876) (2025) — uniformity-on-hypersphere constraints with explicit geometric losses; the modern "geometric SSL" line that MMCR sits within.

**Why expected to improve**:
SIGReg constrains the *batch* distributional shape but is *blind* to the per-image augmentation-view spread — two embeddings can both be marginally Gaussian per slice while having very different intra-image vs inter-image variance ratios. MMCR's two-term objective directly maximises this ratio. The two losses use different first principles (Cramér–Wold theorem for SIGReg, manifold-capacity theory for MMCR) and have low gradient correlation in published analyses. Risk: MMCR's batch-nuclear-norm computation needs ≥ 4 views per image; the current pipeline uses 2 global + 6 local. Mitigation: restrict MMCR to the 6 local views (already K ≥ 4).

**Expected gain**: +0.4 / +1.0 / +2.2 pp 🟡 *(MMCR alone reaches SimCLR levels at scale; as an auxiliary on top of a stronger SIGReg base, the marginal lift should be smaller — published MMCR-vs-VICReg gap is ~1.5 pp on linear probe at ResNet-50, conservative scale-down to ViT-S/Imagenette gives ~1 pp mid)*
**Feasibility**: 4/5 🟢 (nuclear-norm differentiation is `O(d²)` per image; cheap at d=384)
**Effort**: M 🟡 (auxiliary head + α HP + need to wire ≥ 4 views together per image)

**Implementation sketch**:
1. New `MMCRLoss(beta=1.0)` module: from per-image `K` augmented embeddings (K=6 from local views), compute `‖Z_i‖_*` (sum of singular values via `torch.linalg.svdvals`); average over batch; build the batch-nuclear-norm term over `[Z_1, …, Z_B]` flattened.
2. Add `L_total = L_LeJEPA + α · L_MMCR`. Sweep `α ∈ {0.05, 0.1, 0.3}` at fixed best (λ, lr, wd).
3. Compare to **matched-wall-clock** baseline (MMCR adds 1 SVD per image per step — moderate cost; expect ~1.1× wall-clock).

**Risks**:
- **Redundancy-with-SIGReg pre-check** (⚠️ per batch-4 vetting Idea 2 reframe lesson): MMCR's "spread the batch nuclear norm" pull *could* overlap with SIGReg's `Cov(Z) → I` implicit pull. Required ablation: 3-arm (SIGReg only / MMCR only / SIGReg + MMCR). The combo must beat **both singletons** by ≥ 0.4 pp non-overlap; if it only beats one, the gain is from that singleton — adopt it, drop the combo.
- α is a new HP; "single-λ" branding violated unless bound to λ as `α = c · λ`. Apply same trick as batch-4 Idea 6.
- SVD cost: `O(K · d²) = 6 · 384² ≈ 0.9 M ops per image`; total at B=512 is 0.46 G ops/step — negligible vs encoder forward.

**Falsification test**: 3-arm matched-wall-clock at 100 ep: SIGReg / MMCR-only / SIGReg+MMCR (best α), 3 seeds each, fixed (λ, lr, wd) from ASHA. Combo must beat *both* singletons by ≥ 0.4 pp non-overlap. Mechanism check: ablate `α = 0` — must be *worse* than `α > 0` by ≥ 0.3 pp (else MMCR's extra compute is the win, not the objective). If neither passes, reject.

---

### Idea 4: Sliced MMD with Riesz kernels as the SIGReg slice statistic

- **Pattern**: P3 (Replace — swap EppsPulley with sliced-MMD against an N(0,1) reference sample)
- **Tier**: 2 (adjacent ML — generative-modelling MMD-flow line, with the Riesz-kernel theory drawn from harmonic analysis / potential theory)
- **Scope**: enhance-existing. Replaces only the per-slice statistic. Slice sampler, λ, projector, optimizer untouched.
- **One-liner**: Replace EppsPulley's CF-based statistic with **sliced MMD using Riesz kernels** `k(x, y) = −‖x − y‖^s` (s ∈ (0, 2)) against a stored N(0, 1) reference sample — closed-form via sorting (Hertrich et al. 2023), no integration grid, ties to the *energy distance*.

**Mechanism**:
Hertrich, Wald, Altekrüger, Hagemann ([arXiv:2305.11463](https://hf.co/papers/2305.11463), 2023) show that the sliced MMD with a *Riesz kernel* `k_s(x, y) = −‖x − y‖^s` reduces to an O(N log N) computation via sorting on each slice — making it a *cheaper* drop-in than even EppsPulley's trapezoid integration. For SIGReg, store a fixed reference sample `r_1, …, r_R ∼ N(0, 1)` (R = 2048, fixed); per slice compute MMD²(h, r) = (1/N²) Σ_{i,j} k_s(h_i, h_j) − 2/(N R) Σ_{i,k} k_s(h_i, r_k) + (1/R²) Σ_{k,l} k_s(r_k, r_l), all via sorted-difference shortcuts at O((N+R) log(N+R)) per slice. For `s = 1` this is the energy distance, with very strong characteristic properties (zero iff distributions identical). The statistic is differentiable in `h` and the gradient is also computable in O((N+R) log(N+R)).

**Source inspirations**:
- Primary: *Generative Sliced MMD Flows with Riesz Kernels*, Hertrich, Wald, Altekrüger, Hagemann, [arXiv:2305.11463](https://hf.co/papers/2305.11463) (2023) — sorted O(N log N) computation; theoretical equivalence to energy distance for `s = 1`; gradient formula.
- Supporting: *Demystifying MMD GANs*, Bińkowski, Sutherland, Arbel, Gretton, [arXiv:1801.01401](https://hf.co/papers/1801.01401) (ICLR 2018) — establishes MMD with Cramér / energy-distance kernels as a stable training signal; unbiased gradient estimator.
- Supporting: *Optimally-Weighted Estimators of the MMD for Likelihood-Free Inference*, [arXiv:2301.11674](https://hf.co/papers/2301.11674) (2023) — sample-complexity improvements; relevant for the small-N regime.

**Why expected to improve**:
EppsPulley uses a *fixed* trapezoid grid `[0, t_max]` over the CF integrand (per CLAUDE.md `n_points=17`); this is a known bias source — the grid choice trades off between testing the body vs the tails of the distribution. Sliced MMD with energy kernel `s=1` has *no integration grid*: the statistic is a closed-form sorted-difference computation. It is also a strict integral-probability-metric (universal characteristic), so zero iff exact match — stronger than EP's "L²-distance between CFs over `[0, t_max]`". Practically: O(N log N) per slice is *cheaper* than EP's `O(N · n_points)`; the cost goes *down*, not up. Risk: the choice of `s ∈ (0, 2)` is a new HP; `s = 1` is the canonical default. The reference sample size R is also a HP; R=2048 is paper-default.

**Expected gain**: +0.2 / +0.6 / +1.3 pp 🟡 *(another statistic swap — same family as Idea 2, KSD; expected mid lower than Idea 2 because Riesz-MMD is "EP-adjacent" while KSD is mechanistically distinct)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. New `SlicedRieszMMD(s=1.0, ref_size=2048)` univariate test inheriting `UnivariateTest`.
2. On init, draw and cache `r ∼ N(0, 1)^R`.
3. `forward(h)`: sort `h` and `r`; compute the cross-sample term and self-sample term via O(N log N) sorted-difference recurrences (per arXiv:2305.11463 §3).
4. Swap in via `SlicingUnivariateTest(univariate_test=SlicedRieszMMD(), num_slices=1024)`.
5. Ablate `s ∈ {0.5, 1.0, 1.5}` once; expect `s = 1` to dominate.

**Risks**:
- s-choice HP. Mitigation: fix `s = 1` as the default (energy distance, characteristic kernel) — published as the canonical choice.
- The reference sample R is fixed per training run — if R is too small there is bias toward the particular `r`. Mitigation: refresh R every 50 epochs; or use the exact-N(0,1) closed-form integrals from Hertrich §3.2 (no reference sample needed).
- Head-to-head against KSD (Idea 2) and Hermite (batch-3 TOY) — three alternative statistics on the same slice. Run A/B/C — do not stack.

**Falsification test**: Synthetic sanity (1 hr CPU): mixture of N(0,1) + 5 % shifted N(0.5, 1); SlicedRieszMMD power must be ≥ EppsPulley power at α=0.05. Then 100-ep ImageNet-10, baseline EppsPulley vs SlicedRieszMMD at matched (λ, lr, wd) and matched M, 3 seeds; primary: linear probe ≥ 0.3 pp higher with non-overlapping CIs; secondary: SIGReg-call wall-clock should be ≤ EppsPulley by 10–20 % (sorting is cheaper than trapezoid). If wall-clock is higher, implementation is wrong; reject.

---

### Idea 5: SIE-style invariant + equivariant split predictor head

- **Pattern**: P5 (Decompose — split the embedding into invariant and equivariant subspaces under augmentation, train each with its own objective)
- **Tier**: 1 (in-field — SSL representation learning, Garrido / LeCun line)
- **Scope**: enhance-existing. Adds a small head and an equivariance loss term; encoder, SIGReg, λ_inv unchanged.
- **One-liner**: Add a 2-layer MLP `g_ψ` that, given `(z_view1, z_view2)`, predicts the augmentation parameters `Δ` (rotation angle, jitter strengths, blur σ, crop offset) — forcing the encoder to retain *equivariant* information about the transformation as a decomposed subspace, complementing SIGReg's invariance pull.

**Mechanism**:
Garrido, Najman, LeCun ([arXiv:2302.10283](https://hf.co/papers/2302.10283), 2023) introduced **SIE (Split-Invariant-Equivariant)** representations: rather than discarding augmentation information (the standard SSL trick), explicitly split the embedding into `z = (z_inv, z_eq)` and require `z_inv(view1) = z_inv(view2)` (existing invariance term) AND `g_ψ(z_eq(view1), z_eq(view2)) ≈ Δ` (augmentation prediction). The 2026 follow-up (*SSL based on Transformed Image Reconstruction for Equivariance-Coherent Feature Representation*, [arXiv:2503.18753](https://hf.co/papers/2503.18753), 2026) confirms that on standard SSL benchmarks the equivariance-coherence term *improves invariant-task linear probe* (the prediction head pulls signal out of the embedding that would otherwise leak into the invariant subspace as noise). For LeJEPA: keep `L_inv` unchanged; add `L_eq = MSE(g_ψ(z(view1), z(view2)), Δ_true)` and decompose `z = (z_inv, z_eq)` (e.g. split the projector head into two parallel branches with disjoint output dimensions, `d = d_inv + d_eq`). SIGReg is applied to *both* branches independently — the per-direction Gaussianity claim still holds; Cramér–Wold transfers to each subspace separately.

**Source inspirations**:
- Primary: *Self-supervised learning of Split Invariant Equivariant representations*, Garrido, Najman, LeCun, [arXiv:2302.10283](https://hf.co/papers/2302.10283) (2023) — SIE method; 3DIEBench dataset; loss design.
- Primary: *Self-Supervised Learning Based on Transformed Image Reconstruction for Equivariance-Coherent Feature Representation*, Wang, Quercia, Bruns, Morrison, Scharr, Krajsek, [arXiv:2503.18753](https://hf.co/papers/2503.18753) (2026) — direct evidence that adding equivariance-coherence to standard SSL improves downstream invariant-linear-probe.
- Supporting: *EquiCaps: Predictor-Free Pose-Aware Pre-Trained Capsule Networks*, [arXiv:2506.09895](https://hf.co/papers/2506.09895) (2025) — predictor-free variant; relevant ablation if equivariance head adds cost.

**Why expected to improve**:
The existing invariance loss `(z̄ − z).square().mean()` forces both views to map to the same point — discarding all variation due to augmentation. But augmentation-variation is *structured signal*: rotation angle, colour shift, scale. A linear probe on a fully-invariant representation has *fewer informative axes*; adding an equivariant branch enriches the feature space. Wang et al. (2026) shows this explicitly on standard SSL pipelines — equivariance-coherence improves downstream invariant-classification linear probe by ~1 pp (their Table 2). On the small ImageNet-10 / object-centric setting, the equivariance signal is strongest for color-jitter / blur (where the parameter `Δ` is a meaningful scalar). Risk: predicting `Δ` requires storing the true augmentation parameters per sample — easy in our pipeline since augmentations are applied in-loop.

**Expected gain**: +0.3 / +0.9 / +1.8 pp 🟢 *(direct published evidence for the in-domain linear-probe metric)*
**Feasibility**: 4/5 🟢
**Effort**: M 🟡 (2-layer MLP head + Δ-bookkeeping + d-split)

**Implementation sketch**:
1. Split projector output: `d = 256 + 128` (invariant + equivariant); SIGReg applied to both halves with same λ.
2. New `EquivarianceHead(d_eq=128, num_params=K)` — predicts a flat vector of augmentation parameters from `concat(z_eq^1, z_eq^2)`.
3. Bookkeep `Δ` from the augmentation pipeline (rotation degrees, jitter triplet, blur σ, crop bbox).
4. `L_total = L_LeJEPA(z_inv) + λ · SIGReg(z_eq) + γ · MSE(g_ψ(z_eq), Δ)`. Fix `γ = 1.0` initially (or `γ = c · λ`); ablate.

**Risks**:
- Doubles SIGReg compute slightly (2 branches × 1024 slices). Mitigate: 512 slices on each (M unchanged in total).
- Bookkeeping of `Δ` requires augmentation refactor (`Compose` returns transformed image + params). Mid-sized eng change.
- Composition with batch-1 / batch-3 augmentation-side ideas: clean — the equivariance head is on the head side, not the augmentation side.

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd), 3 seeds: baseline vs SIE-split. Primary: linear probe (on `z_inv` only) must be ≥ 0.5 pp higher with non-overlapping CIs. Mechanism check: linear probe on the *full* `z = (z_inv, z_eq)` should be **lower** than `z_inv` only — that proves `z_eq` is encoding augmentation noise, not class signal (the intended decomposition). If `z_full ≥ z_inv` the decomposition collapsed; reject.

---

### Idea 6: Saliency-guided crop region sampling for the global views

- **Pattern**: P8 (Augment — data-side change to the crop sampler)
- **Tier**: 1 (in-field — SSL data augmentation literature; ContrastiveCrop / saliency-guided SSL)
- **Scope**: enhance-existing. Replaces the global-crop region sampler (currently `RandomResizedCrop(scale=0.3–1.0)`). Encoder, projector, SIGReg, λ untouched.
- **One-liner**: Replace uniform `RandomResizedCrop` for the 2 global views with a *saliency-weighted* crop sampler (low-cost saliency: image gradient magnitude or off-the-shelf U²-Net teacher) so global crops are object-centric rather than background-biased — particularly relevant on Imagenette where each image has a single dominant object.

**Mechanism**:
Standard `RandomResizedCrop(scale=0.3–1.0)` on Imagenette routinely produces global views that contain mostly background sky / wood / texture (≈ 20–30 % of crops by inspection on the 10-class subset). These "background-global views" still anchor the invariance loss but their feature should match the object-centric local-view features — a known source of noisy gradients. Saliency-guided cropping ([Saliency Can Be All You Need in Contrastive SSL, arXiv:2210.16776](https://hf.co/papers/2210.16776), 2022) and ContrastiveCrop ([arXiv:2202.03278, CVPR 2022](https://arxiv.org/abs/2202.03278)) propose: compute a per-image saliency map once (gradient magnitude or off-the-shelf segmentation), then sample crop centers from the saliency-weighted distribution. The 2025 paper *Taming the Randomness: Towards Label-Preserving Cropping in Contrastive Learning* ([arXiv:2504.19824](https://hf.co/papers/2504.19824), 2025) shows ~1 pp linear-probe lift on CIFAR-10 / object-centric subsets with parameterised crop samplers, exactly the regime we are in. Mechanism is data-side (does not touch the loss); composes with everything.

**Source inspirations**:
- Primary: *Saliency Can Be All You Need in Contrastive Self-Supervised Learning*, Kocaman, Shir, Bäck, Belbachir, [arXiv:2210.16776](https://hf.co/papers/2210.16776) (2022) — saliency-as-prior for contrastive SSL crop sampling.
- Primary: *Taming the Randomness: Towards Label-Preserving Cropping in Contrastive Learning*, Hassan, Wasil, Houben, [arXiv:2504.19824](https://hf.co/papers/2504.19824) (2025) — parameterised crops; quantitative gains on small-object-centric datasets matching our setting.
- Supporting: *ContrastiveCrop*, Peng et al., [CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/papers/Peng_Crafting_Better_Contrastive_Views_for_Siamese_Representation_Learning_CVPR_2022_paper.pdf) — semantic-aware cropping; bootstrap with current encoder's attention map.

**Why expected to improve**:
Imagenette is **maximally object-centric** by construction (10 specific ImageNet classes, each a single dominant object). The DINO-style crop sampler treats it like ImageNet-1K. A saliency-aware sampler that biases global crops toward the object reduces the "global view that contains no object" failure mode — the invariance term then anchors object-vs-object, not background-vs-object. Published gains on object-centric subsets (CIFAR-10, fine-grained) are ~1 pp. On in-domain SSL with 600 epochs, this small bias compounds.

**Expected gain**: +0.3 / +0.8 / +1.5 pp 🟢
**Feasibility**: 5/5 🟢 (saliency map = `image.float().std(dim=channel)` + box-blur; no extra model; 1 ms per image)
**Effort**: S 🟢

**Implementation sketch**:
1. Add `crop_saliency: bool` flag to the data transform.
2. Per-image saliency: simplest `S(x, y) = local_std(image_gray, kernel=5)`, normalise to a 2D probability map.
3. Crop center is sampled from `S`; crop scale stays `~Uniform(0.3, 1.0)`. Local crops keep uniform sampling (their job is to *find* whatever the global cropped).
4. Compare to baseline at matched compute (no extra compute; this is a sampler change).

**Risks**:
- Saliency-as-prior on background-textured classes (e.g. "tench" mostly water, "gas pump" with sky) may concentrate too aggressively; ablate `crop_center ~ (1 − α) · Uniform + α · Saliency` with `α ∈ {0.3, 0.6, 1.0}`.
- Composition with batch-2 / batch-3 augmentation ideas: clean — sampler change is mechanically separate from the augmentation set.
- Tier-1, "incremental" risk: this idea is the *least mechanistically novel* of the batch; success is bounded by the published ~1 pp ceiling.

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd), 3 seeds: baseline `RandomResizedCrop` vs saliency-weighted (best `α` from {0.3, 0.6, 1.0}). Primary: linear probe ≥ 0.5 pp higher with non-overlapping CIs. Mechanism check: a `α = 1` (full saliency) arm should *not* dominate `α = 0.6` (some uniform residual is needed for invariance regularisation) — if `α = 1` wins, the gain is from data-distribution shift, not the prior. If `α ≥ 0.3` does not beat baseline, reject.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|------------------------|--------------------|---------------------|-----------------|------------|-------------|------------|-------|
| 1 | Spherical t-design slicing | ✅ Bondarenko-Radchenko-Viazovska Annals 2013 + Womersley arXiv:1709.01624 + arXiv:1611.02785 | ✅ | ✅ (≥20 % loss-std reduction vs Gaussian AND beat best stochastic VR by ≥10 %) | NOVEL (within SIGReg) | VERIFIED | 4 | ⚠️ family overlap with batch-3/4 VR ideas — flagged | **KEEP w/ flag** |
| 2 | KSD per-slice statistic | ✅ Liu-Lee-Jordan ICML 2016 (arXiv:1602.03253) + arXiv:2304.14762 (2023) + arXiv:2210.10741 (2022) | ✅ | ✅ (≥1.5× synthetic power AND ≥0.4 pp non-overlap linear probe) | NOVEL | VERIFIED | 3 | ⚠️ O(N²) cost — mitigation provided | **KEEP w/ flag** |
| 3 | MMCR auxiliary | ✅ Yerxa-Kuang-Simoncelli-Chung arXiv:2303.03307 (2023) + Chung-Sompolinsky PRX 2018 + arXiv:2503.00876 (2025) | ✅ | ✅ (3-arm singleton-vs-combo + α=0 mechanism check) | EXTENDS | VERIFIED | 4 | ⚠️ redundancy-with-SIGReg pre-check mandatory | **KEEP w/ flag** |
| 4 | Sliced Riesz-MMD statistic | ✅ Hertrich et al arXiv:2305.11463 (2023) + Bińkowski-Sutherland-Arbel-Gretton ICLR 2018 (arXiv:1801.01401) | ✅ | ✅ (≥synth-power-parity + ≥0.3 pp non-overlap + wall-clock ≤ EP) | NOVEL (within SIGReg) | VERIFIED | 4 | OK | **KEEP** |
| 5 | SIE invariant+equivariant split | ✅ Garrido-Najman-LeCun arXiv:2302.10283 (2023) + Wang et al arXiv:2503.18753 (2026) + arXiv:2506.09895 (2025) | ✅ | ✅ (z_inv probe ≥ 0.5 pp + z_full < z_inv decomposition check) | EXTENDS | VERIFIED | 4 | OK | **KEEP** |
| 6 | Saliency-guided crops | ✅ arXiv:2210.16776 (2022) + arXiv:2504.19824 (2025) + ContrastiveCrop CVPR 2022 | ✅ | ✅ (≥0.5 pp probe + non-trivial-α dominance check) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |

**Cross-idea consistency**:
- Ideas 2 and 4 (and batch-3 TOY Hermite) are alternative *per-slice statistics*. Run A/B/C — do not stack. Pick the winner.
- Idea 1 (t-design) joins the cumulative variance-reduction family (SRHT batch-3, Repulsive batch-4, Antithetic+SH-CV batch-4). Run 4-way A/B/C/D — do not stack pairwise without singleton numbers.
- Idea 3 (MMCR) has a *potential* redundancy with SIGReg's covariance pull; the 3-arm singleton-vs-combo ablation is mandatory.
- Ideas 5 (SIE) and 6 (saliency crops) are mechanically orthogonal to every other survivor; compose with the cumulative stack freely.
- All ideas use the same falsification protocol (matched-compute baseline; 3 seeds; non-overlapping CIs at ≥ 0.3–0.6 pp).

**No ideas rejected this batch.** Append empty stanza to `_logs/_rejection_log.md`.

## Notes & warnings

- ⚠️ **Variance-reduction family is now 4-deep** (SRHT batch-3, Repulsive batch-4, Antithetic+SH-CV batch-4, t-design batch-5). Idea 1 must be evaluated head-to-head against the other three, not stacked. Vetting batch-4's lesson about "variance-reduction family coverage across batches" is explicitly applied here — Idea 1 is included BECAUSE the family deserves a deterministic corner, not in spite of the overlap. The 4-arm A/B/C/D experiment is the right resolution.
- ⚠️ **Per-slice-statistic family is now 4-deep** too (EppsPulley = baseline, Hermite-moment = batch-3 TOY, KSD = batch-5 Idea 2, Sliced Riesz-MMD = batch-5 Idea 4). These four statistics need a single round-robin head-to-head experiment, not pairwise A/B.
- ⚠️ **MMCR (Idea 3) requires redundancy pre-check** — apply the lesson from batch-4 Idea 2 (W-MSE) reframe: theoretical-redundancy-with-SIGReg pre-check is mandatory. 3-arm (SIGReg-only / MMCR-only / both) at matched compute; combo must beat both singletons.
- ⚠️ **No P6 (Verify) idea this batch** — batch-3 Idea 3 (PIT monitor) still pending ρ-correlation validation; no new callback added until PIT graduates.
- ⚠️ **Pattern coverage cumulative across batches 1–5 = P1, P2, P3, P4, P5, P6, P7, P8, P12 (9/12, unchanged)**. P9 / P10 / P11 remain unsuited to in-domain SSL pretraining.
- ⚠️ **Soft "single-λ" branding drift**: Ideas 3 (α for MMCR), 5 (γ for equivariance MSE), 6 (α for saliency mixture) each add 1 HP. Mitigation in every case: bind to λ as `HP = c · λ` with `c` fixed. If 2+ of these ship, LeJEPA becomes a 3-HP method. **User decision flag** — same as batch-4.
- ⚠️ **Idea 2 (KSD) feasibility 3/5** is the lowest in the batch — O(N²) cost is real; if the stochastic-mini-block KSD does not preserve power, this idea is the most likely to be downgraded to TOY.
- ⚠️ **Tier-3 honesty audit**: every T3 idea here traces to a primary in a *named non-ML field* —
  - Idea 1: Annals of Mathematics (Bondarenko-Radchenko-Viazovska) + SIAM J. Numer. Anal. (Womersley). Discrete geometry / numerical analysis.
  - Idea 2: Stein's method (Charles Stein 1972, *Annals of Math. Stat.*); KSD application appears at ICML but the *method* and the "goodness-of-fit for unnormalised density" frame are mathematical statistics — Anastasiou et al. *Statist. Surv.* 2023 documents the field-of-origin claim.
  - Idea 3: Chung-Sompolinsky *Phys. Rev. X* 2018 (theoretical neuroscience / statistical physics of neural representations).
- **Devil's-advocate on top-1 by composite (Idea 6 — saliency crops, 2.7)**: failure mode = saliency-as-prior fails when saliency is *wrong* (e.g. "tench" mostly water — saliency picks the splashes, not the fish). The 2025 paper (arXiv:2504.19824) explicitly notes label-preservation as the failure mode; their parameterisation reduces this to a HP. Mitigation already in falsification: the `α=1` arm must NOT dominate `α=0.6`. Search for "saliency contrastive SSL failure" surfaced no published kill case — absence-of-evidence only.

- **Prerequisites / measurements** (NOT ideas — surfaced per skill rules):
  - (i) Batch-2 Idea 5 ASHA sweep — still the gate for absolute-pp claims (unchanged from batch-3 / batch-4 notes).
  - (ii) Spherical t-design table generation for `(d=384, M=1024, t=4 or 6)` is a one-time CPU compute (≤ 1 hr). Run as a Step-0-parallel measurement.
  - (iii) Synthetic-power test for KSD vs EppsPulley (Idea 2) and Sliced Riesz-MMD vs EppsPulley (Idea 4) — 1 hr CPU each; gates whether each statistic graduates to ImageNet-10 run.

## Composition map (cumulative survivor stack → batch-5)

Cumulative survivor stack from batches 1–4: PIT monitor (b3), SRHT (b3), Hermite-moment (b3 TOY), rank-curriculum (b3 TOY), co-distillation (b3 TOY), SAM/Friendly-SAM (b4 FULL), Layer-wise SIGReg (b4 TOY), Antithetic+SH-CV (b4 TOY), Repulsive MC (b4 REFRAME), MAE-aux (b4 TOY), W-MSE pre-step (b4 REFRAME), ASHA (b2 step-0).

| New idea | Composes-with cumulative stack (✓ = stack, ⚠ = sequential / A-B-C first, ✗ = conflict) |
|----------|--------------------------------------------------------------------------------------|
| 1. Spherical t-designs | ✓ PIT · ✓ SAM · ✓ MAE-aux · ⚠ SRHT / Repulsive / Antithetic+SH-CV (4-way A/B/C/D first) · ✓ ASHA · ✓ rest |
| 2. KSD per-slice | ✓ PIT · ✓ SAM · ✓ MAE-aux · ⚠ Hermite + Riesz-MMD (4-way per-slice-statistic A/B/C/D first) · ✓ SRHT (orthogonal axis) · ✓ ASHA |
| 3. MMCR auxiliary | ✓ PIT · ✓ SAM · ⚠ W-MSE (both touch covariance — sequential redundancy check) · ⚠ MAE-aux (both are auxiliary heads — measure α-vs-α joint sensitivity) · ✓ ASHA |
| 4. Sliced Riesz-MMD | same as Idea 2 (per-slice-statistic family) |
| 5. SIE split | ✓ all survivors — head-side change, orthogonal to slicing / statistic / optimiser axes |
| 6. Saliency crops | ✓ all survivors — data-side change, orthogonal to everything |

The natural **compose-mode targets** for batch-6 are: (a) **Saliency crops + SIE split + SAM + PIT + ASHA** (data + head + optimiser + monitor + tuning — orthogonal across 5 axes); (b) **Best per-slice statistic from {EP, KSD, Riesz-MMD, Hermite} + Best slice sampler from {Gaussian, SRHT, Repulsive, t-design} + Antithetic+SH-CV estimator** — the full SIGReg numerics stack; (c) **MMCR + SIGReg + W-MSE** — the covariance-shaping stack (with the redundancy pre-check).

## Next steps for user

1. **(Unchanged from batch-4 vetting)** Run batch-2 Idea 5 (ASHA) as Step 0 — still gates all absolute-pp claims.
2. **(Unchanged)** Idea 3-A (Layer-wise probe-alignment Phase A): 0 GPU-h pre-flight from batch-4.
3. **(This batch)** Idea 6 (Saliency crops): drop-in change, S effort, T1 evidence — run as a 2-arm A/B alongside the next baseline. Likely batch-5's **quick win**.
4. **(This batch)** Idea 5 (SIE split): M effort, needs augmentation-pipeline refactor; commit only after Idea 6 settles or in parallel if eng bandwidth allows.
5. **(This batch)** Idea 4 (Sliced Riesz-MMD): cheap statistic swap; combine with the per-slice-statistic 4-way A/B/C/D experiment.
6. **(This batch)** Idea 2 (KSD): the most expensive statistic swap (O(N²)); fold into the same 4-way A/B/C/D.
7. **(This batch)** Idea 1 (t-designs): only after the t-design table is generated; run inside the 4-way slice-sampler A/B/C/D (Gaussian / SRHT / Repulsive / t-design).
8. **(This batch)** Idea 3 (MMCR): largest expected gain in this batch; requires 3-arm singleton-vs-combo redundancy check before commitment. **Big bet — run last** in this batch's queue, after baseline + ASHA + cheaper survivors lock in.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 30/20/50 | given-vetting batch-4 | 2026-05-18 batch-5`
