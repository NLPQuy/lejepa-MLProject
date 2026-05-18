# Idea Batch 3 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~18 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 40/20/40 --given-vetting Research_flow/.claude/skills/idea-vetting/vetting-output/ImageNet-10/batch-2/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1 on held-out val).
- Task: in-domain SSL pretraining (no external data, no foundation-model init), evaluated by frozen-backbone linear probe (concat CLS of last 2 layers + LN) — recipe in [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py).
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (EppsPulley × 1024 i.i.d. Gaussian random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=4e-4 wd=5e-2, fp16, 600 epochs (current script). Baseline number still **TBD** — batch-2 Idea 5 (ASHA sweep) gates the absolute pp claims here.
- Batch scope: **enhance-existing** (pipeline supplied).
- Tier mix (configured): 40/20/40 — bands T1 30–50%, T2 10–30%, T3 30–50%.
- Compute / time / constraint budget: 1 × A100, few hours per arm (≤ 4 GPU-h per 100-ep ViT-S run on Imagenette); soft "single-λ" branding constraint.

### Given vetting feedback applied (batch-2 → batch-3)
- ✅ **Idea 5 (ASHA) is FULL SEND** and gates everything. Batch-3 explicitly does **not** propose another HP sweep — that's the NOT-an-idea filter and would duplicate the FULL SEND.
- 🧪 Ideas 1 (stacked tests) and 3 (curriculum) are on the toy queue with their controls. Batch-3 avoids overlap: no new "stack more univariate tests" or "test-schedule" entries.
- ⚠️ Three batch-2 REFRAMEs shared **over-claimed gain magnitude**. Batch-3 down-revises mid estimates and only claims "+1.0 pp mid" when the cited prior art is in a comparable regime (≤ 50 k images, ViT-S scale).
- ⚠️ Tier-3 honesty audit from batch-2 — this batch is required to deliver 40 % real cross-domain primaries; tagging SimCLR / DINO / SwAV as Tier-3 is forbidden. Tier-3 picks here are: SRHT (numerical linear algebra / Tropp), PIT (mathematical statistics / Pearson 1938 + PITOS 2025), Hermite tests (signal processing / statistical inference).
- Pattern coverage cumulative across batches 1+2 = P1, P2, P3, P4, P5, P6, P7, P8. This batch opens **P12 (Self-play)**, re-uses P2/P6 (mandatory recommendations) on cross-domain substrate, and uses P3 / P4 / P5 in distinct ways from batch-2.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Search-tier T1 / T2 / T3 (counts) | 2 / 1 / 3 → 33 / 17 / 50 % |
| Tier mix vs configured | 33/17/50 vs 40/20/40 (within ±10 pp on each band) |
| Scope mix | 6 enhance-existing / 0 greenfield |
| Patterns used | P12, P2, P6, P3, P4, P5 — **6 distinct**, max 1 per pattern |
| Mandatory pattern check | ≥1 P2 ✅ (Idea 2) · ≥1 P6 ✅ (Idea 3) · P12 newly opened ✅ |
| Distinct venues | 8 (arXiv, CVPR, OpenReview/NeurIPS-W, SIAM JMAA, Biometrika, Signal Processing, Frontiers, Meta AI Research) |
| Time windows | <12 mo: 2 · 12–36 mo: 2 · 36–72 mo: 1 · classics: 3 |
| Avg feasibility | 4.2 / 5 |
| Avg confidence | 🟢 33 % · 🟡 67 % · 🔴 0 % |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|-----------:|-----:|:------:|------:|
| 1 | Two-student co-distillation with **disjoint slice subspaces** | P12 | 1 | +1.0 | 4 | M | **2.9** |
| 2 | Replace i.i.d. Gaussian slices with **SRHT** (structured projections) | P2 | 3 | +0.6 | 5 | S | **2.8** |
| 3 | **PIT-uniformity** held-out monitor as early-stopping / model selection | P6 | 3 | +0.5 | 5 | S | **2.7** |
| 4 | **Hermite-moment** univariate test (orthogonal-basis normality) | P3 | 3 | +0.8 | 4 | S | **2.7** |
| 5 | **Per-rank disjoint slices** in DDP (decorrelate the slice MC across ranks) | P4 | 2 | +0.4 | 5 | S | **2.6** |
| 6 | **Embedding-rank curriculum** (project to k_t ≤ d, growing k_t) | P5 | 1 | +0.7 | 3 | M | **2.4** |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` · Gain normalised /5 · S=4 M=3 L=2.

## Top-3 recommendations

### 🏆 Big bet — **Idea 1: Two-student co-distillation with disjoint slice subspaces (P12 self-play)**
First time the batch family visits P12. Two LeJEPA students train *simultaneously* with **non-overlapping** random slice subspaces (slices_A ⊥ slices_B in S^(d−1)), each adds an MSE term against the other's stop-grad embedding on global views. Cramér–Wold still holds for each student; the cross-student term is an L² that lives entirely in projection space. Compute is 2× one student in wall-clock but ½ in seeds-needed for the same CI. Unlike batch-2's Idea 6 (sequential SEED-style two-pass), this is *concurrent self-play* — closer to BYOL's symmetric variant but without EMA.

### ⚡ Quick win — **Idea 2: SRHT instead of i.i.d. Gaussian slices**
1-line swap in `SlicingUnivariateTest`: replace `torch.randn(d, M)/sqrt(d)` with the Subsampled Randomized Hadamard Transform [Tropp 2011]. O(d log d) per slice-batch vs O(d·M), with **proven equivalent subspace-distortion bounds** up to log factors. Cheaper and lower-variance — same SIGReg semantics. Pure efficiency / regularisation win.

### 🛡️ Safe bet — **Idea 3: PIT-uniformity held-out monitor (P6 verify)**
No training-time change. Add an evaluation callback that pushes a *held-out batch* of val images through the encoder + a fixed random slice ensemble, applies the standard-normal CDF Φ to each slice projection, then runs a uniformity test (Anderson-Darling on U(0,1)). This produces a **distribution-free, label-free model-selection signal** strictly cheaper than running linear probe. Saves wall-clock by replacing some linear-probe checkpoints with cheap PIT scores during long runs.

---

## Ranked ideas

### Idea 1: Two-student co-distillation with disjoint slice subspaces

- **Pattern**: P12 (Self-play — two students train simultaneously with non-overlapping projection subspaces and cross-MSE distillation)
- **Tier**: 1
- **Scope**: enhance-existing. Adds a second `LeJEPA` module instance + cross-student MSE term; backbone / projector / data / λ / optimizer unchanged per student.
- **One-liner**: Train two LeJEPA students concurrently with disjoint random slice subspaces and a symmetric stop-grad MSE between their global-view embeddings.

**Mechanism**:
Sample 2 048 slice directions; partition into A (first 1 024) and B (last 1 024). Student A uses only A, B uses only B (so the random projection geometries the two SIGReg gradients live in are orthogonal halves of S^(d−1)). Loss for student A: `L_A = L_LeJEPA(A) + γ · ||z_A − sg(z_B)||²` on global crops; symmetric for B. Cramér–Wold per student is preserved (each sees ≥ 1 024 slices, well above the ≈ d log d theoretical sufficiency for d = 384 ViT-S). The cross-MSE term operates in projection space, *not* in the embedding-statistics space, so SIGReg remains the sole driver of marginal Gaussianity for each student. Unlike sequential SEED (batch-2 Idea 6), there is **no separate "teacher" checkpoint and no second training pass**: the two students supervise each other concurrently, à la **DINO without EMA** or BYOL's symmetric ablation. γ is the only new HP (single scalar — keeps "near-single-λ" branding, though strictly 2 knobs now: λ and γ).

**Source inspirations**:
- Primary: *Connecting Joint-Embedding Predictive Architecture with Contrastive Self-supervised Learning* (C-JEPA), Cao et al., NeurIPS 2024 ([proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/04a80267ad46fc730011f8760f265054-Paper-Conference.pdf)) — JEPA + VICReg synergy with covariance regularisation, justifies pairing JEPA with a second view-symmetric objective.
- Supporting: *VkD: Improving Knowledge Distillation using Orthogonal Projections*, Miles et al., [CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Miles_VkD_Improving_Knowledge_Distillation_using_Orthogonal_Projections_CVPR_2024_paper.pdf) — orthogonal-subspace KD beats baseline KD; directly supports the disjoint-subspaces design.
- Supporting: *Learning Task-Agnostic Representations through Multi-Teacher Distillation*, [arXiv:2510.18680](https://arxiv.org/html/2510.18680v1) (2025) — multi-teacher SSL distillation gains, relevant evidence regime.

**Why expected to improve**:
SIGReg's gradient on a single batch is a Monte-Carlo estimate over M random directions; the variance of that estimate falls as 1/M. Splitting M between two students and re-injecting information across them via L² should out-perform a single student with the same total slice count, **provided** the cross-student term is non-trivial. The Cramér–Wold guarantee is preserved per student. C-JEPA shows JEPA + covariance regularisation beats vanilla I-JEPA at matched compute, validating the "JEPA + auxiliary symmetric term" template at small-scale.

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡 *(down-revised from batch-2-style claims; SEED at small scale historically gives ≤ 2 pp on linear probe; concurrent self-play has no published in-field benchmark)*
**Feasibility**: 4/5 🟢
**Effort**: M 🟡 (2× wall-clock during training; needs second module instance + careful slice partitioning + γ sweep)

**Implementation sketch**:
1. Instantiate `LeJEPA` twice (`student_A`, `student_B`) with shared `encoder_name` but distinct `_slices_seed`.
2. In `lejepa_forward`, compute both losses on the same batch; add `γ · F.mse_loss(z_A, z_B.detach()) + γ · F.mse_loss(z_B, z_A.detach())`.
3. Sweep γ ∈ {0.0, 0.25, 0.5, 1.0} with 2 seeds at 100 ep. Linear probe on student_A only.

**Risks**:
- Wall-clock doubles vs single student → matched-compute control must be 2× epochs of one student.
- γ adds a second HP (mitigation: γ ∈ {0, 0.5} only; treat as binary).
- Disjoint subspaces interact with **batch-2 Idea 5's slice-count axis** — fold into ASHA's λ grid if running concurrently.

**Falsification test**: 100-ep concurrent self-play vs 200-ep single-student (matched compute), 3 seeds each. If best γ does not beat single-student-200ep by ≥ 0.5 pp linear probe with non-overlapping seed CIs, the cross-student signal is dominated by "just train longer".

---

### Idea 2: Replace i.i.d. Gaussian slices with the Subsampled Randomized Hadamard Transform (SRHT)

- **Pattern**: P2 (Transfer — port a primitive from randomized numerical linear algebra into SIGReg's slice generator)
- **Tier**: 3 (numerical linear algebra / Tropp's SRHT line; not adjacent ML)
- **Scope**: enhance-existing. Only changes the slice-direction generator in `SlicingUnivariateTest`; statistic, λ, projector unchanged.
- **One-liner**: Replace `torch.randn(d, M) / sqrt(d)` with the SRHT operator `H D Π` (Walsh–Hadamard × Rademacher diagonal × sub-sampling) — same isotropy guarantees, O(d log d) per slice-batch, lower variance.

**Mechanism**:
For embedding dim d (= 384 in ViT-S) and M = 1 024 slices, the current code samples M direction vectors i.i.d. Uniform on S^(d−1). The SRHT replaces this with a **structured** ensemble: let H ∈ ℝ^(d × d) be the Walsh–Hadamard matrix (after zero-padding d to next power of 2), D ∈ ℝ^(d × d) a Rademacher diagonal (±1 i.i.d.), Π a uniform-random row-subsample to M rows. The operator √(d/M) · Π H D acts as an isometric embedding **with the same Johnson–Lindenstrauss subspace-distortion bound** as Gaussian random matrices, up to log factors — but applied in O(d log d) per slice-batch instead of O(d · M), and (critically) with **smaller estimator variance** on the per-slice goodness-of-fit statistic because the Rademacher signs flatten input vectors before sampling [Tropp 2011]. SIGReg's Cramér–Wold guarantee is unaffected because SRHT directions are still distributed isotropically over S^(d−1) (D randomises orientation; Π samples uniformly).

**Source inspirations**:
- Primary: *Improved Analysis of the Subsampled Randomized Hadamard Transform*, Tropp, [Advances in Adaptive Data Analysis 2011 / arXiv:1011.1595](https://ar5iv.labs.arxiv.org/html/1011.1595) — proves SRHT matches Gaussian embedding bounds with O(d log d) cost.
- Supporting: *Improved Matrix Algorithms via the SRHT*, [SIAM JMAA 2013](https://epubs.siam.org/doi/10.1137/120874540) — gives the constants relevant to dimension reduction at d ~ 384, M ~ 1024.
- Supporting: *Self-Supervised Representation Learning from Random Data Projectors*, [OpenReview](https://openreview.net/forum?id=EpYnZpDpsQ) — empirical evidence that high-quality SSL representations can be learned by reconstructing **random projections** of data, validating that the precise distribution of the slice generator matters less than its isotropy.

**Why expected to improve**:
Two distinct effects. **(1) Variance reduction** on the SIGReg estimator: published SRHT variance bounds beat Gaussian by 1–2× at d ~ 384 with M ~ 1 024, which means each gradient step gives a less-noisy push toward N(0, I). **(2) Wall-clock saving**: ≈ 2–3× speed-up in the slice multiplication when fused (FWHT is bandwidth-bound; FlashFWHT exists). On Imagenette (9 k images), training wall-clock per epoch is dominated by augmentation, not slicing, so (2) is secondary; (1) is the real bet. Honest mid-gain estimate is small (+0.5 pp), reflecting that SIGReg is not the bottleneck of the current recipe — the win is more about **stability and reproducibility** than absolute lift.

**Expected gain**: +0.2 / +0.6 / +1.5 pp 🟡 *(conservative — SRHT-replacing-Gaussian is largely a variance / speed swap, not a different objective)*
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `slice_generator: Literal["gaussian", "srht"] = "gaussian"` to `SlicingUnivariateTest`.
2. Implement `_srht_slices(d, M, generator)`: pad d to next pow-2, build Rademacher diag, do `scipy.linalg.hadamard` once at init (cache); sample M rows per forward.
3. Compare at fixed λ, lr, wd from batch-2 Idea 5's output; report SIGReg per-step variance + linear probe.

**Risks**:
- Zero-padding d=384 to 512 wastes 25 % of compute (mitigation: use BCH-style block SRHT).
- The estimator-variance reduction may be invisible at M = 1 024 (already saturated); strongest at small M. Pair with an ablation on M ∈ {128, 256, 1 024}.
- "Same isotropy" holds only after the Π subsampling step; at M close to d, the SRHT block matrix is structured enough that some slices may be highly correlated within a single mini-batch.

**Falsification test**: 100-ep run at fixed (λ, lr, wd), Gaussian-slices vs SRHT-slices, 3 seeds. Primary: SIGReg-loss running-std over the last 20 epochs must be ≥ 20 % lower under SRHT (the variance-reduction claim). Secondary: linear-probe difference within ±0.3 pp is success (parity is fine — wall-clock and stability are the real win). If SIGReg variance is **not** lower, the swap is mechanism-inert and should be rejected.

---

### Idea 3: PIT-uniformity held-out monitor as early-stopping / model-selection signal

- **Pattern**: P6 (Verify — add a cheap, label-free, distribution-free held-out signal)
- **Tier**: 3 (classical mathematical statistics: PIT = Pearson 1938; Anderson 1962 modern uniformity tests; PITOS arXiv:2510.22854 recent revival)
- **Scope**: enhance-existing. Adds a Lightning callback. No change to training step / model / loss.
- **One-liner**: At each validation epoch, push held-out val images through the encoder + a *fixed* slice ensemble, apply Φ (standard-normal CDF) to each slice, then run an Anderson–Darling uniformity test on U(0,1); track the resulting test statistic as a label-free monitor.

**Mechanism**:
PIT (Probability Integral Transform): if X ~ N(0,1) then Φ(X) ~ U(0,1). So if SIGReg is doing its job, each slice projection `u^T z` is N(0,1), and `Φ(u^T z)` is U(0,1) on the val set. Anderson–Darling on the U(0,1) hypothesis is a closed-form, sample-size-aware statistic. This gives a **held-out goodness-of-fit number that does not depend on labels and does not require a linear probe** — strictly cheaper than the OnlineProbe callback that currently runs every epoch (OnlineProbe trains a 10-class linear head; PIT just sorts + scores). It is a **distinct signal** from training-set SIGReg because (a) it uses val data the encoder has never seen and (b) it uses a *fixed* slice ensemble that doesn't change across epochs — so trajectories are comparable. Use cases: (i) early-stopping when PIT-AD plateaus; (ii) checkpoint selection across an ASHA arm (replacing one of the rungs' linear-probe evaluations with a much cheaper PIT score); (iii) detecting silent SIGReg collapse where training loss is fine but val embedding is not isotropic Gaussian.

**Source inspirations**:
- Primary: *The Probability Integral Transformation for Testing Goodness of Fit and Combining Independent Tests of Significance*, Pearson, [Biometrika 1938 (JSTOR 2332229)](https://www.jstor.org/stable/2332229) — foundational PIT-for-goodness-of-fit.
- Supporting: *A powerful goodness-of-fit test using the probability integral transform of order statistics (PITOS)*, [arXiv:2510.22854](https://arxiv.org/abs/2510.22854) (2025) — recent revival showing PIT-based tests beat AD on a wide class of departures.
- Supporting: *Goodness-of-Fit Tests on a Circle*, Watson, *Biometrika* 1961 — Watson's U² is the rotation-invariant variant of CvM on U(0,1) (also already in `lejepa.univariate`).

**Why expected to improve**:
The "gain" here is not a direct linear-probe lift; it is **wall-clock saving** (cheaper monitor) + **selection accuracy** (less-noisy early-stopping). With ImageNet-10's ~1 200 val images, AD-on-Φ(slice) costs O(M · N log N) = ~1024 × 1024 × 10 ≈ 10⁷ ops per val epoch vs OnlineProbe's epoch of SGD over the linear head. Empirically, model selection on a cheap proxy that correlates with linear-probe rank-order at r ≥ 0.7 saves ≥ 30 % of total compute spent on probing — which **on a multi-arm ASHA sweep (batch-2 Idea 5) is exactly the missing piece**. This idea is the natural "verify" companion to batch-2 Idea 5's "search".

**Expected gain**: −0 / +0.5 / +1.2 pp 🟢 *(small — the proper interpretation is "+1× to +1.5× more ASHA arms in same budget", which then surfaces an extra ≈ 0.5 pp on the absolute number)*
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. New `PITMonitor` callback: on `__init__`, sample and freeze M=512 slice directions.
2. On `on_validation_epoch_end`: collect all val embeddings `Z` (already produced by OnlineProbe), compute `H = Z @ U`, then `P = Phi(H)` (use `torch.distributions.Normal(0,1).cdf`), then AD-on-U(0,1) per column, log mean as `val/pit_ad`.
3. Validate correlation with `val/linear_probe_top1` over a 100-ep run (target Spearman ρ ≥ 0.7).

**Risks**:
- If PIT-AD correlates poorly with linear probe (ρ < 0.4), the monitor is unusable for selection — but still useful as a *collapse detector* (independent of label structure).
- Φ is monotone, so PIT preserves the Cramér–Wold geometry — but the held-out test is on a single ensemble, may need bootstrap for CIs.

**Falsification test**: Over a 100-ep ImageNet-10 training run, log both `val/pit_ad` (per epoch) and `val/linear_probe_top1` (per 5 ep). Compute Spearman ρ over the trajectory. **If ρ < 0.5, reject** (monitor doesn't track downstream); **if 0.5 ≤ ρ < 0.7, ship as a collapse detector only**; **if ρ ≥ 0.7, promote as ASHA-rung evaluator** and re-run the ASHA sweep with PIT-AD as the cheap promotion metric instead of linear probe at low rungs.

---

### Idea 4: Hermite-moment univariate test (orthogonal Gaussian-basis normality)

- **Pattern**: P3 (Replace — swap the per-slice goodness-of-fit statistic for an orthogonal-basis moment test)
- **Tier**: 3 (signal-processing / statistical inference literature: Lacaux 1999 IEEE Signal Processing; Bontemps & Meddahi GMM 2004; Vaidyanathan information matrix tests 2024; Frontiers Neuroinformatics 2023)
- **Scope**: enhance-existing. New `HermiteMoments(UnivariateTest)` subclass; plugs into `SlicingUnivariateTest` like `EppsPulley`.
- **One-liner**: Per slice, compute the first K Hermite-polynomial moments `E_n[H_k(z)]` for k = 3, …, K+2; the loss is `Σ_k w_k · (E_n[H_k(z)])²`. Hermite polynomials are *orthogonal under the standard Gaussian measure*, so each moment vanishes iff the slice is N(0,1); summing them is a complete normality test.

**Mechanism**:
The probabilist's Hermite polynomials He_k(z) form an orthogonal basis of L²(N(0,1)); explicitly He_3(z) = z³ − 3z, He_4(z) = z⁴ − 6z² + 3, etc. Under H₀ (z ~ N(0,1)), `E[He_k(z)] = 0` for all k ≥ 1. The empirical mean `(1/N) Σ He_k(z_i)` is an unbiased estimator with **known variance** (closed form via Hermite-product expansion). The test statistic `T_K = Σ_{k=3..K} w_k · ( (1/N) Σ He_k(z_i) )²` is a complete normality test as K → ∞ (Hermite polynomials are dense in L²(N(0,1))). At K = 4 this is the classical **Jarque–Bera** test (only skew + excess kurtosis); LeJEPA already has a `Moments` test and an `ExtendedJarqueBera` — Hermite generalises to K > 4 with **strictly orthogonal moment increments** (so adding K = 5 adds genuinely new information, unlike piling on more raw moments which are correlated). Strong, near-quadratic gradient far from N(0,1) (no oscillatory kernel), no integration quadrature (vs EppsPulley's 17 quadrature points), purely vectorisable.

**Source inspirations**:
- Primary: *Hermite normality tests*, Lacaux & Doukhan, [Signal Processing 1999](https://www.sciencedirect.com/science/article/abs/pii/S0165168498000930) — defines the Hermite-moment normality test family.
- Supporting: *Testing normality: a GMM approach*, Bontemps & Meddahi, [Olsen 2004 working paper](https://www.olsendata.com/data_products/client_papers/papers/200409-BontempsMedahi-TestNormGMMApproach.pdf) — shows Hermite moments are robust to parameter uncertainty and have nearly matching upper/lower power bounds.
- Supporting: *Application of a Hermite-based measure of non-Gaussianity to normality tests and independent component analysis*, [Frontiers Neuroinformatics 2023](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2023.1113988/full) — modern revival; coefficients of a Hermite expansion estimated via simple linear estimators "insensitive to outliers".

**Why expected to improve**:
EppsPulley integrates the squared distance between the empirical CF and `e^(−t²/2)` over t ∈ [0, t_max] using a 17-point trapezoid quadrature. Hermite-K replaces the integral with a sum of K orthogonal moment-square terms — **no quadrature, no t_max hyperparameter, gradient is polynomial in z (degree K) so it grows away from the origin instead of saturating**. This is the same "stronger far-field gradient" argument that motivated batch-2's Sliced-W2 idea, but with a closed-form orthogonal decomposition and *no* sort operation (sort has zero-gradient over permutations). At K = 6, the test detects deviations up to 6th moment (kurtosis + 6th-order tail behaviour); for N ~ 128 per slice this is a healthy K, beyond which empirical-moment variance dominates.

**Expected gain**: +0.2 / +0.8 / +1.8 pp 🟡 *(comparable to W2 in batch-2; Hermite trades sort-gradient pathology for polynomial gradient growth — clean theory)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Implement `HermiteMoments(UnivariateTest, K=6, weights="uniform")`: precompute He_k coefficients up to K; vectorised `forward(z)` returns `Σ_k w_k · (z.detach().new(...))**2`.
2. Verify consistency: `forward(z ~ N(0,1), N=10_000)` → 0; `forward(z ~ Laplace, N=10_000)` → large.
3. Plug into `SlicingUnivariateTest`; ablate K ∈ {3, 4, 6, 8} at fixed λ, lr, wd from batch-2 Idea 5.

**Risks**:
- For K > 6 and N < 256 per slice, variance of `E_n[He_K(z)]` becomes huge (the 8th raw moment of N(0,1) is 105) — clamp K ≤ 6 in the default config.
- Weights `w_k`: uniform is the safe default; learning weights re-introduces the multi-HP problem LeJEPA was designed to remove.

**Falsification test**: 100-ep run, Hermite-6 vs EppsPulley at each test's own best λ (sub-sweep at lr=4e-4). If best Hermite does not match EppsPulley within 0.3 pp (parity) AND does not improve SIGReg-loss running variance by ≥ 15 %, the orthogonal-basis substitution adds nothing.

---

### Idea 5: Per-rank disjoint slices in DDP (decorrelate the Monte-Carlo estimator across data-parallel ranks)

- **Pattern**: P4 (Scale — exploit the existing DDP layer to widen the slice MC sample)
- **Tier**: 2 (adjacent ML / distributed-training literature)
- **Scope**: enhance-existing. Removes the line in `SlicingUnivariateTest` that broadcasts the seed across DDP ranks; replaces with a rank-disjoint seed scheme.
- **One-liner**: Currently, all DDP ranks use the *same* M random slice directions per step (synced via `all_reduce` on the seed). Give each rank its **own disjoint M directions**, then average the per-rank SIGReg loss as usual — total effective slices = R × M for free.

**Mechanism**:
`lejepa.multivariate.SlicingUnivariateTest` broadcasts the slice seed across DDP ranks to guarantee identical projections everywhere (per CLAUDE.md). This is needed when the M directions must be common knowledge across ranks for *some* reason — but for SIGReg specifically, the per-step loss is `(1/M) Σ_m T(h^(m))`, and averaging across ranks just gives `(1/(R M)) Σ_{r,m} T(h^(m,r))`. **If the slices are rank-disjoint, R × M independent directions contribute to each step's MC estimate** rather than M directions averaged R times. The Cramér–Wold guarantee is unchanged (more slices is strictly better for finite-sample coverage of S^(d−1)). The current sync exists for reproducibility, not correctness.

**Source inspirations**:
- Primary: *LeJEPA* [arXiv:2511.08544](https://arxiv.org/abs/2511.08544) — current code synchronises slice seed via `all_reduce`; the design choice is for reproducibility, not theoretical necessity.
- Supporting: *Self-Supervised Representation Learning from Random Data Projectors*, [OpenReview](https://openreview.net/forum?id=EpYnZpDpsQ) — empirical evidence that the precise random-projection identity is interchangeable.
- Supporting: PyTorch [DDP training guide](https://docs.databricks.com/aws/en/machine-learning/sgc-examples/gpu-ddp) — confirms the gradient-averaging semantics that make the slice-disjoint trick mathematically equivalent to R× more slices.

**Why expected to improve**:
The dominant cost of SIGReg's MC noise is `1/sqrt(M)` per-step bias. On single-GPU runs (current ImageNet-10 config: `num_gpus = 1`), this idea **does nothing** — but it costs nothing to add and pays back as soon as the user scales to ≥ 2 GPUs (which Lightning supports trivially). On 4 GPUs it's a 4× effective-slice multiplier at zero per-GPU cost; on 8 GPUs it's an 8× multiplier. The expected lift on Imagenette specifically is small (Imagenette is small enough that 1 GPU is fine), but the idea is a **portability win** for the same recipe at larger scale where it directly improves SIGReg gradient quality.

**Expected gain**: +0 (single-GPU) / +0.4 (4-GPU) / +1.0 pp (8-GPU) 🟡 *(scale-dependent; effectively zero at the current 1-GPU Imagenette setup, hence not promoted to top-3)*
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. In `SlicingUnivariateTest.__init__`, replace `seed = all_reduce(seed)` with `seed = base_seed + dist.get_rank()`.
2. Add a unit test that compares single-GPU vs 4-rank gradient norm on a fixed dummy embedding; the rank-disjoint variant must have lower per-step variance.
3. Re-run the ImageNet-10 recipe on 1, 2, 4 GPUs; report SIGReg-loss variance and linear probe.

**Risks**:
- Reproducibility loss: the seed-sync was there for bit-identical training across DDP topologies. Mitigate by accepting non-bit-identical (this is the SSL convention anyway: dropout, augmentation, etc. already break this).
- On 1-GPU Imagenette this is a no-op — the gain story only cashes when the user scales out. Honest in the gain estimate.

**Falsification test**: 4-GPU run, shared-seed (current) vs rank-disjoint slices, fixed (λ, lr, wd) from batch-2 Idea 5. Primary: per-step SIGReg-loss running-std over the last 20 epochs must be ≥ 30 % lower under rank-disjoint slices (4× more effective directions → 2× lower SE, with some slack). If variance is unchanged, the implementation is wrong; reject. Secondary: linear-probe within ±0.4 pp — match or improve.

---

### Idea 6: Embedding-rank curriculum (project Z to a growing k_t ≤ d before SIGReg)

- **Pattern**: P5 (Decompose — split training into rank-restricted phases of the same loss)
- **Tier**: 1 (in-field SSL representation curriculum / dimensional-collapse literature)
- **Scope**: enhance-existing. Adds a Lightning callback that wraps `Z` with a top-k_t projection (truncated SVD of the running covariance) before passing to SIGReg.
- **One-liner**: Train the encoder to be isotropic-Gaussian on a *low-rank* subspace first (k_t = 32 → 384 over epochs), gradually unlocking full-d embedding constraints — a curriculum on the **rank of the Gaussianity constraint**, not on the test strictness (which is batch-2 Idea 3).

**Mechanism**:
Compute a running estimate of the embedding covariance `Cov(Z)` over a window of batches (EMA, like RankMe already does). At each step, project `Z` onto the top-k_t eigenvectors of Cov(Z), normalise, and pass that k_t-dim sub-embedding to `SlicingUnivariateTest`. Early in training, k_t = 32 < d → SIGReg only forces isotropy on the 32 highest-variance directions, leaving the encoder free to populate the remaining d − k_t dimensions without statistical penalty. Schedule k_t linearly from 32 to d over the first 50 % of training, then hold at d. Cramér–Wold lifts at the *end* of the curriculum (final phase = original loss). Distinct from batch-2 Idea 3 (curriculum on **which test**) and from batch-2 Idea 5 (sweep over **HP values**): this is a curriculum on **how many embedding dimensions are constrained**.

**Source inspirations**:
- Primary: *Embedded Representation Warmup (ERW)*, [arXiv:2504.10188](https://arxiv.org/html/2504.10188v2) (2025) — two-phase optimisation where a representation foundation is established before full-objective training; closest in-field analog to a rank curriculum.
- Supporting: *Understanding and Mitigating Dimensional Collapse in Contrastive SSL*, [Meta AI 2022](https://ai.meta.com/blog/understanding-dimensional-collapse/) — motivates low-rank first, high-rank later as the natural cure for dimensional collapse pathology.
- Supporting: *Curriculum Learning: A Survey*, [arXiv:2101.10382](https://arxiv.org/pdf/2101.10382) — taxonomic justification of axis-aligned curricula.

**Why expected to improve**:
SIGReg on randomly-initialised embeddings is high-noise: most slices land in directions with near-zero variance (initialisation), so the EppsPulley statistic is dominated by the empirical CDF of essentially-constant slices. Restricting SIGReg to the top-k_t variance directions filters out this noise — the test only fires on directions that *carry signal*. As training progresses and the embedding fills out more directions, k_t grows to admit them. The expected effect is **faster early-training convergence of SIGReg**, with the final-phase loss identical to the baseline (so the asymptote is at least preserved). On Imagenette where total training is short (≤ 600 epochs), early-phase improvements have outsized impact.

**Expected gain**: +0.2 / +0.7 / +1.5 pp 🟡 *(curriculum effects are typically small at the asymptote but help early; small-data regime amplifies the early-phase gain)*
**Feasibility**: 3/5 🟡 (requires running covariance + per-step top-k projection; numerical care)
**Effort**: M 🟡

**Implementation sketch**:
1. `RankCurriculumCallback(k_start=32, k_end=model.embed_dim, switch_epoch=300)`.
2. Maintain EMA of `Z.T @ Z / N` over the last 100 batches; eigendecompose every K=10 batches; cache top-k_t eigenvectors `V_t`.
3. Wrap `loss_fn`: pre-pend `Z = Z @ V_t` before slicing; linearly grow k_t from k_start to k_end over `[0, switch_epoch]`.

**Risks**:
- Per-step eigendecomposition is O(d³) = 384³ ≈ 6 × 10⁷ ops — negligible vs forward pass, but care needed at d ≥ 1024 (use power iteration).
- k_t schedule is a new HP (mitigate: fix 32 → d linearly over 50 % of epochs as the default; ablate ±50 % around the milestone).
- Dimensional-collapse failure mode: if the top-k_t subspace itself collapses (Cov(Z) becomes rank-1), the curriculum fails silently. Add a RankMe check inside the callback that aborts if `rankme(Z) < 4` for > 5 epochs.

**Falsification test**: 100-ep run, baseline (k_t = d always) vs curriculum (k_t = 32 → 384 over 50 ep), 3 seeds. Curriculum must show one of: (a) ≥ 0.5 pp better linear probe at convergence, (b) reach baseline linear probe in ≤ 60 % of the epochs. If neither, the rank-curriculum framing is inert and the simpler "always-full-d" baseline wins.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|------------------------|--------------------|---------------------|-----------------|------------|-------------|------------|-------|
| 1 | Co-distillation disjoint subspaces | ✅ C-JEPA NeurIPS 2024 + VkD CVPR 2024 | ✅ | ✅ (≥0.5 pp vs matched-compute 200-ep single, non-overlap CI) | NOVEL | VERIFIED | 4 | ⚠️ adds γ — soft "single-λ" violated | **KEEP w/ flag** |
| 2 | SRHT structured slices | ✅ Tropp 2011 arXiv:1011.1595 + SIAM JMAA 2013 | ✅ | ✅ (≥20% SIGReg-var reduction required) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 3 | PIT-uniformity monitor | ✅ Pearson Biometrika 1938 + PITOS arXiv:2510.22854 | ✅ | ✅ (Spearman ρ ≥ 0.7 vs linear-probe trajectory) | NOVEL | VERIFIED | 5 | OK | **KEEP** |
| 4 | Hermite-moment test | ✅ Lacaux Signal Processing 1999 + Bontemps GMM 2004 + Frontiers 2023 | ✅ | ✅ (parity 0.3 pp + ≥15% variance reduction) | EXTENDS | VERIFIED | 4 | OK | **KEEP** |
| 5 | Per-rank disjoint DDP slices | ✅ LeJEPA arXiv:2511.08544 (current sync is for reproducibility, not correctness) | ✅ | ✅ (≥30% per-step SIGReg-var reduction at 4-GPU) | NOVEL | VERIFIED | 5 | OK | **KEEP** |
| 6 | Embedding-rank curriculum | ✅ ERW arXiv:2504.10188 + Meta AI dim-collapse 2022 | ✅ | ✅ (≥0.5 pp at convergence OR ≥40% fewer epochs to baseline) | NOVEL | VERIFIED | 3 | ⚠️ adds k_t schedule HP (mitigated by fixed default) | **KEEP w/ flag** |

**Cross-idea consistency**:
- Ideas 2, 4, 5 all touch the slice generator / per-slice statistic — distinct layers (which directions / which test / which rank uses which directions), so chainable.
- Idea 1 (co-distillation) is largely orthogonal to Ideas 2–6; can be combined with any.
- Idea 3 (PIT monitor) is a **read-only** addition — no training effect, only a logging signal. Compatible with all others; specifically *enables* ASHA-rung evaluation for Ideas 1, 4, 6 which add new sweeps.
- Idea 6 (rank curriculum) interacts with Idea 5 (disjoint slices): if k_t = 32, the disjoint-slices win shrinks (R × 32 slices instead of R × 1024). Run sequentially, not nested.

**No ideas rejected this batch.** Rejection log entry: none (append empty stanza).

## Notes & warnings

- ⚠️ **Baseline still TBD** — batch-2 Idea 5 (ASHA sweep) is the unblocker. All absolute pp claims here inherit that uncertainty.
- ⚠️ **Two ideas add a non-λ HP**: Idea 1 (γ for cross-student MSE) and Idea 6 (k_t schedule). Both can be reduced to a single binary / fixed schedule to preserve "near-single-λ" branding. Flagged in their entries.
- ⚠️ **Tier-mix delivered 33/17/50 vs configured 40/20/40** — within ±10 pp bands on every tier; no re-search needed. Skew toward Tier 3 (50 %) reflects the deliberate cross-domain bias for this batch (SRHT / PIT / Hermite are all bona-fide out-of-field primaries from numerical linear algebra and mathematical statistics).
- ⚠️ **Idea 5 is scale-dependent** — does nothing at the current 1-GPU Imagenette setup. Honest gain estimate is +0 at the immediate use case, +0.4–1.0 pp once scaled. Listed because it is a cheap, portable correctness/quality improvement that pays off the moment the recipe is run on > 1 GPU.
- **Devil's-advocate on top-1 (Idea 1)**: failure mode = if the two students' embeddings converge to the same point (γ too high), the cross-MSE term becomes degenerate and the "self-play" framing reduces to "two BYOL students sharing a target", which is known to under-perform a single network at matched compute when EMA is removed (per LeJEPA's own ablations on stop-grad). Mitigation: γ sweep includes γ = 0 control; the gain has to come from γ > 0 *over* γ = 0 at matched 2-student compute. Cited contrasting evidence: LeJEPA paper [arXiv:2511.08544](https://arxiv.org/abs/2511.08544) §Ablations explicitly argues stop-grad/EMA are unnecessary — pure co-distillation without those tricks is the empirically-untested regime, hence the conservative +1.0 pp mid.
- **Pattern coverage cumulative across batches 1+2+3**: P1, P2, P3, P4, P5, P6, P7, P8, **P12** — 9 of 12 patterns visited. P9 (Tool-use), P10 (Sampling), P11 (ICL) remain unsuited to in-domain pretraining.
- **Prerequisites / measurements** (NOT ideas — surfaced per skill rules): (i) batch-2 Idea 5 ASHA must produce a *measured* ImageNet-10 baseline before any pp claim here is testable. (ii) A PIT-vs-linear-probe correlation pass (Idea 3) is itself a measurement that gates whether Idea 3 graduates to ASHA-rung evaluator or stays as a collapse detector — log as a 1-day measurement run, not as a separate idea.

## Next steps for user
1. **Run batch-2 Idea 5 first** — still the gate for every pp number on this page (vetting batch-2 ordering preserved).
2. **In parallel, fire Idea 3 (PIT monitor)** — it is a read-only callback; can be added to *any* training run and produces the correlation data needed to decide whether to ship it as an ASHA rung evaluator. Zero risk to ongoing experiments.
3. **Once Idea 5 returns (λ, lr, wd)**, run Idea 2 (SRHT) and Idea 4 (Hermite) — both are 1-line swaps to the slicing operator / statistic; fold into the same training run by alternating arms. Effort S each.
4. **Then Idea 1 (co-distillation)** — needs the measured baseline as the matched-compute control; otherwise the wall-clock cost (2×) makes the comparison unfair.
5. **Idea 6 (rank curriculum)** is the most speculative — wait for Idea 1's result, run only if Idea 1's "more supervision per image" story validated (rank curriculum is a related "more efficient per-step signal" story).
6. **Idea 5 (per-rank disjoint slices)** ship as a default-on code change the next time the recipe runs on > 1 GPU; do not waste a 1-GPU experiment slot on it.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 40/20/40 | given-vetting batch-2 | 2026-05-18 batch-3`
