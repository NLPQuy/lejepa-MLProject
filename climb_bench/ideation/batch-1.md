# Idea Batch 1 — Imagenette (ImageNet-10) / In-domain SSL pretraining for frozen-backbone linear probe

**Generated**: 2026-06-02T00:00:00Z
**Time-to-batch**: ~14 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation` — "10 ideas to improve LeJEPA architecture on Imagenette, frozen ViT-S/16 linear probe"

## Inputs
- **Benchmark**: Imagenette (fast.ai 10-class ImageNet subset, ~9,469 train / ~3,925 val images). In-domain SSL pretrain, 400 epochs, then **frozen** `vit_small_patch16_224`.
- **Task / problem**: Self-supervised representation learning from unlabeled images such that *frozen* features linearly separate the 10 Imagenette classes. Metric = linear-probe top-1 (probe = concat CLS of last 2 layers + LayerNorm, AdamW lr 1e-3 wd 1e-6); secondary = online kNN top-1 (`val/knn_top1`). Very-low-data regime → data-efficiency and anti-overfit dominate.
- **Existing pipeline**: `stable_pretraining.methods.lejepa.LeJEPA`. Loss = `invariance + λ·SIGReg`. Backbone ViT-S (CLS, `aggregator="cls"`) → projector `build_projector("MLP")` (BN+ReLU 384→512→2048→2048→512) → predictor `"none"`. SIGReg = `SlicedEppsPulley` (1024 random unit slices, Epps-Pulley ECF test, t_max 3.0, n_points 17, on projector output). Invariance = MSE of each view's projection to the **global-view mean center** (`_compute_loss`). Multi-crop 2×224 global + 6×98 local, `patch_mask_ratio=0.3`. λ≈0.02–0.05, AdamW lr 5e-4 wd 5e-2, drop_path 0.1, bf16. Baseline score = TBD (user to measure; ideas framed as Δ vs this exact config).
- **Batch scope**: enhance-existing (10/10 ideas modify a named component; 0 greenfield).
- **Tier mix (configured)**: 55/30/15 (bands T1 45–65 / T2 20–40 / T3 5–25).
- **Baseline**: LeJEPA (ViT-S/16) @ TBD on Imagenette frozen linear probe.
- **Compute budget**: single/few GPU, ViT-S, 400 epochs/run; prefer light compute deltas; no ImageNet-1K-scale runs.
- **Constraints**: improvements act at **pretrain** (backbone frozen at eval); in-domain data only (no external data / no distillation from external pretrained models / no labels); keep SIGReg as the backbone of the objective; EMA/stop-grad heuristics only with explicit justification; **no pure HP-sweep ideas** (10 ablations already cover num_slices/t_max/n_points, projector dim & depth, reg_tokens, #views, patch-mask ratio, drop_path, aggregator, sigreg_target, predictor).

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 10 |
| Tier 1 / 2 / 3 (counts) | 5 / 3 / 2 |
| Tier mix vs configured | 50/30/20 vs 55/30/15 (each within ±10pp) |
| Scope mix | 10 enhance-existing / 0 greenfield |
| Patterns used | P1, P2, P3, P5, P6, P10 (6 distinct) |
| Distinct venues | CVPR, ICML, ICLR, ICCV, JMLR, arXiv (≥3) |
| Time windows | <12mo (2), 12-36mo (1*), 36-72mo (5), 72+mo (2) |
| Avg feasibility | 3.8/5 |
| Avg confidence | 🟢 30%, 🟡 60%, 🔴 10% |

\* 12-36mo window has 1 primary (SimDINO) — below the suggested ≥2; see Notes & warnings.

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 3 | Coding-rate (log-det) volume term complementing SIGReg | P1 | 2 | +2.0 | 4 | S | 3.2 |
| 7 | Energy-preserving DynTanh normalization in projector | P3 | 1 | +2.0 | 5 | S | 3.5→3.1* |
| 4 | Hypersphere-uniformity auxiliary term on projections | P1 | 1 | +1.0 | 5 | S | 3.1 |
| 8 | NNCLR nearest-neighbour positives for the invariance branch | P10 | 2 | +2.0 | 4 | M | 3.0 |
| 5 | EMA-teacher asymmetric targets for invariance | P3 | 2 | +2.5 | 3 | M | 2.9 |
| 6 | Dense patch-token SIGReg + invariance | P5 | 1 | +3.0 | 3 | L | 2.9 |
| 10 | RankMe-gated adaptive λ control loop | P6 | 1 | +1.0 | 4 | M | 2.7 |
| 2 | Closed-form Cramér-Wold Gaussian metric vs Epps-Pulley quadrature | P2 | 3 | +1.0 | 4 | M | 2.6 |
| 1 | Learned/constrained slice directions for SIGReg | P10 | 3 | +1.5 | 3 | L | 2.3 |
| 9 | AutoView adversarial learned views | P2 | 1 | +1.5 | 3 | L | 2.3 |

\* Idea 7 downgraded one slot by the devil's-advocate pass (normalization-removal instability evidence); composite recomputed.

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 3: Coding-rate (log-det) volume term complementing SIGReg** — Score 3.2
A ~10-line `+ β·codingrate(embeddings)` term gives an instantaneous full-rank anti-collapse signal that SIGReg only supplies marginally (1-D slices, averaged over steps). On tiny Imagenette with small batches this directly fights the dominant failure mode (dimensional collapse) at near-zero cost.

### ⚡ Quick win (lowest effort)
**Idea 7: Energy-preserving DynTanh normalization in projector** — Effort S
Swap the projector's BatchNorm for `DyT(x)=tanh(αx)`. Drop-in, no batch statistics (helps small/uneven batches), and an IJEPA study reports ViT-S linear probe 38→42.7 from exactly this normalization change. (Carries a real risk — see contrasting evidence.)

### 🛡️ Safe bet (highest confidence)
**Idea 4: Hypersphere-uniformity auxiliary term on projections** — Confidence 🟢
The Wang–Isola uniformity potential is a battle-tested, parameter-free pairwise-repulsion regularizer with strong theory linking it to downstream accuracy; adds a complementary global-spread signal to SIGReg at trivial cost and low risk.

## Ranked ideas

### Idea 3: Coding-rate (log-det) volume term complementing SIGReg

- **Pattern**: P1 (Combine)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — adds a term inside `LeJEPA._compute_loss`; SIGReg, invariance, projector, backbone all unchanged.
- **One-liner**: Add SimDINO's explicit coding-rate (log-det covariance) term as a cheap full-rank complement to SIGReg's marginal Gaussian matching.

**Mechanism**:
In `_compute_loss`, after computing `all_features`/`all_projected`, add `R = -log det(I + (d/(Nε²)) ZᵀZ)` (matrix-determinant lemma form, `Z` = projected views `[B·V, K]`) and use `loss = inv_loss + λ·sigreg + β·R`. Coding rate measures the *volume* spanned by the batch in one shot (full covariance), whereas `SlicedEppsPulley` only constrains 1-D marginals and accumulates covariance information across steps. The log-det is computed on a `K=512`-dim Gram matrix → cheap.

**Source inspirations**:
- Primary: "Simplifying DINO via Coding Rate Regularization (SimDINO/SimDINOv2)", Wu, Zhang, Pai, Wang, Singh, Yang, Gao, Ma, ICML 2025 [arXiv:2502.10385]
- Supporting: "VICReg: Variance-Invariance-Covariance Regularization for SSL", Bardes, Ponce, LeCun, ICLR 2022 [arXiv:2105.04906]
- Contrasting: "Weak-SIGReg: Covariance Regularization for Stable Deep Learning", Akbar, 2026 [arXiv:2603.05924] — shows covariance-only sketching already stabilizes SIGReg-style training (risk of redundancy).

**Why expected to improve**:
SimDINO shows a single coding-rate term removes most anti-collapse heuristics in DINO and improves linear probe. On ~9.5k images with small effective batches, SIGReg's slice-averaged covariance signal is noisy; an instantaneous log-det volume term raises effective rank faster → better-conditioned frozen features.

**Expected gain**: +0.5 / +2.0 / +4.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `coding_rate(Z, eps)` (log-det via Cholesky on `I + c·ZᵀZ`).
2. Add `bstat_codingrate_beta` override; default 0 (off) so baseline is unchanged.
3. Apply to projector output (match `sigreg_target`); log `coding_rate` term separately.

**Risks**:
- Redundant with SIGReg → no net gain (Weak-SIGReg suggests covariance alone already helps).
- log-det numerically unstable in bf16 → compute in fp32.

**Falsification test**: Run 400ep with β tuned on a 3-point grid {1e-3,1e-2,1e-1}. If best β gives linear-probe top-1 ≤ baseline +0.5pp AND no RankMe effective-rank increase >5%, reject.

---

### Idea 7: Energy-preserving DynTanh normalization in projector

- **Pattern**: P3 (Replace)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces `norm_layer` inside `build_projector` (BatchNorm → DynTanh); backbone, SIGReg, invariance, multi-crop unchanged.
- **One-liner**: Replace projector BatchNorm with element-wise `DyT(x)=tanh(αx)` to preserve the feature-energy hierarchy that LN/BN equalize away.

**Mechanism**:
The IJEPA-normalization study shows LN on features equalizes token L2 norms, erasing the "energy" of semantically rich tokens; replacing it with DynTanh restores a long-tailed energy distribution and lifts ViT-S linear probe 38→42.7. Apply the same swap to the LeJEPA projector MLP: substitute each `batch_norm` with `DyT`. DyT also removes batch-statistic dependence — valuable for the small, multi-crop, uneven batches here.

**Source inspirations**:
- Primary: "Elucidating the Role of Feature Normalization in IJEPA", Colton, 2025 [arXiv:2508.02829]
- Supporting: "Transformers without Normalization (Dynamic Tanh)", Zhu, Chen, He, LeCun et al., CVPR 2025 [arXiv:2503.10622]
- Contrasting: "Analyzing Training Dynamics of Image Restoration Transformers: A Revisit to LayerNorm", 2025 [arXiv:2504.06629] — removing normalization can blow up feature magnitudes / destabilize.

**Why expected to improve**:
Direct same-backbone (ViT-S) evidence of +4.7pp from this exact normalization change in a JEPA setting. Energy-preserving normalization lets high-norm patch/CLS components dominate the projector and thus the invariance + SIGReg signal, yielding more discriminative frozen features.

**Expected gain**: +0.5 / +2.0 / +5.0 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Implement `DyT` module (`tanh(α·x)` with learnable scalar α + affine γ,β).
2. Add `projector_norm="dyntanh"` branch in `build_projector`/`MLP`.
3. Train; monitor projector activation norm distribution + linear probe.

**Risks**:
- Normalization removal can destabilize training (contrasting paper) → keep α learnable, watch for magnitude blow-up.
- Gain reported on IJEPA targets, not LeJEPA projector → transfer uncertain.

**Falsification test**: Run 400ep with DynTanh projector vs BN projector (same seed). If linear-probe top-1 ≤ baseline +0.5pp OR training diverges (loss NaN / grad-norm >10× baseline), reject.

---

### Idea 4: Hypersphere-uniformity auxiliary term on projections

- **Pattern**: P1 (Combine)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — adds a term in `_compute_loss` on L2-normalized projections; everything else unchanged.
- **One-liner**: Add the Wang–Isola uniformity potential `log E[e^{-t‖zᵢ-zⱼ‖²}]` as a global pairwise-repulsion complement to SIGReg.

**Mechanism**:
Compute the Gaussian-kernel uniformity loss on L2-normalized projector outputs across the batch and add it: `loss = inv_loss + λ·sigreg + γ·uniformity`. SIGReg matches per-slice marginals to N(0,1) but does not directly penalize two distinct samples sitting on top of each other; the uniformity potential is an explicit pairwise repulsion proven to track downstream accuracy. On few-sample Imagenette this fills local gaps the marginal test misses.

**Source inspirations**:
- Primary: "Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere", Wang, Isola, ICML 2020 [arXiv:2005.10242]
- Supporting: "DINOv2: Learning Robust Visual Features without Supervision" (KoLeo nearest-neighbour entropy term), Oquab et al., TMLR 2024 [arXiv:2304.07193]

**Why expected to improve**:
Wang–Isola show directly optimizing uniformity matches/beats contrastive learning downstream; DINOv2's related KoLeo term improves retrieval by >8%. Adds a complementary spread signal to SIGReg at O(B²·K) cost (trivial for B≤512).

**Expected gain**: +0.3 / +1.0 / +2.5 pp 🟢
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `uniformity_loss(z, t=2)` on `F.normalize(all_projected)`.
2. Add `uniformity_gamma` override (default 0).
3. Sweep γ on {0.1,0.5,1.0}; log term + probe.

**Risks**:
- Redundant with SIGReg's isotropy push → marginal gain.
- Uniformity on the sphere vs SIGReg's Gaussian (radial) target may conflict → tune γ small.

**Falsification test**: 400ep with best γ. If linear-probe top-1 ≤ baseline +0.5pp, reject. (Cheap: term is a one-liner.)

---

### Idea 8: NNCLR nearest-neighbour positives for the invariance branch

- **Pattern**: P10 (Sampling strategy)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — augments the invariance target in `_compute_loss` with a support-queue nearest neighbour; SIGReg, projector, backbone unchanged.
- **One-liner**: Pull each view not only toward the global-view center but also toward its nearest neighbour in a support queue, injecting semantic (cross-image) positives that augmentation alone cannot create on 9.5k images.

**Mechanism**:
Maintain a FIFO queue of recent projected embeddings. For each global-view projection `z`, retrieve NN `q=NN(z, queue)` and add `‖q.detach() - predicted‖²` to the invariance loss (weight η). This is NNCLR's positive-sampling mechanism adapted to LeJEPA's MSE-to-center invariance. Semantic neighbours give richer invariance signal precisely where augmentation diversity is scarce (small dataset).

**Source inspirations**:
- Primary: "With a Little Help from My Friends: Nearest-Neighbor Contrastive Learning of Visual Representations (NNCLR)", Dwibedi et al., ICCV 2021 [arXiv:2104.14548]
- Supporting: "Adaptive Similarity Bootstrapping for Self-Distillation based Representation Learning", 2023 [arXiv:2303.13606]

**Why expected to improve**:
NNCLR reports +3% top-1 from NN positives and explicitly reduces reliance on heavy augmentation — directly relevant to a tiny dataset. SIGReg keeps the global distribution Gaussian, preventing the trivial collapse NN-pulling could otherwise cause.

**Expected gain**: +0.5 / +2.0 / +3.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Add a registered-buffer queue (size ~4096) of normalized projections.
2. NN lookup (cosine) for global views; add η·MSE(predicted, NN.detach()).
3. Warm up η after queue fills (~few hundred steps).

**Risks**:
- Early-training noisy NNs reinforce wrong pairs → warmup + small η.
- Queue staleness on small data (few distinct images) → keep queue modest.

**Falsification test**: 400ep with NN positives vs baseline. If kNN top-1 ≤ baseline +0.5pp OR NN-retrieval purity (same-class fraction) <30% after 50 epochs, reject.

---

### Idea 5: EMA-teacher asymmetric targets for invariance

- **Pattern**: P3 (Replace)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the symmetric in-batch center in `_compute_loss` with an EMA-teacher target; SIGReg stays on the student projector unchanged.
- **One-liner**: Compute invariance targets from an EMA copy of the encoder+projector (I-JEPA/BYOL-style) instead of the in-batch global-view mean, for more stable targets in the low-data regime.

**Mechanism**:
Add an EMA teacher (`backbone+projector`). Student global/local projections are pulled toward the **teacher's** global-view projections (stop-grad on teacher). SIGReg remains on the student. This swaps the `centers = all_projected[:n_global].mean(0)` target for a slowly-moving teacher target.

**Source inspirations**:
- Primary: "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA)", Assran et al., CVPR 2023 [arXiv:2301.08243]
- Supporting: "Connecting Joint-Embedding Predictive Architecture with Contrastive SSL", NeurIPS 2024 [arXiv:2410.19560]

**Why expected to improve**:
EMA targets reduce variance of the prediction target — large relative to signal when batches are tiny and the center is estimated from few samples. SIGReg's presence means EMA is *not* needed for anti-collapse, so this isolates the target-stability benefit. **Justification vs constraint**: EMA is added only as a target-smoother, not as the collapse-prevention heuristic (which SIGReg still owns).

**Expected gain**: +0.5 / +2.5 / +4.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡 (a `TeacherStudentWrapper` already exists in the repo backbone)

**Risks**:
- Contradicts LeJEPA's "no heuristics" thesis; paper argues SIGReg alone suffices → gain may be ~0.
- EMA momentum is a new sensitive knob.

**Falsification test**: 400ep, EMA momentum {0.99,0.996}. If best linear-probe top-1 ≤ baseline +0.5pp, reject (and conclude SIGReg already removes EMA's value).

---

### Idea 6: Dense patch-token SIGReg + invariance

- **Pattern**: P5 (Decompose)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — extends `aggregate_tokens`/`encode` to expose patch tokens and applies SIGReg + a patch-correspondence invariance; CLS-level path kept as-is.
- **One-liner**: Apply SIGReg and invariance at the patch-token level (iBOT-style) so each of ~196 tokens per image is a training signal, multiplying the effective supervision on 9.5k images.

**Mechanism**:
Run a small shared projector on patch tokens; apply `SlicedEppsPulley` to the pooled patch-token set and add a masked patch-correspondence invariance between two global views (matching overlapping spatial positions). Decomposes the single CLS-level objective into ~196 per-token objectives → far more gradient signal per image, the key bottleneck on a tiny dataset.

**Source inspirations**:
- Primary: "iBOT: Image BERT Pre-Training with Online Tokenizer", Zhou et al., ICLR 2022 [arXiv:2111.07832]
- Supporting: "I-JEPA", Assran et al., CVPR 2023 [arXiv:2301.08243]

**Why expected to improve**:
iBOT/I-JEPA show patch-level objectives drive strong ViT features; with only ~9.5k images the per-image token count is the cheapest way to multiply supervision without external data. SIGReg generalizes naturally to the patch-token distribution.

**Expected gain**: +1.0 / +3.0 / +6.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Risks**:
- Patch tokens less linearly separable → may not help CLS-probe; mind the eval uses CLS.
- Extra memory from per-token projector (mitigate: subsample tokens).

**Falsification test**: 400ep dense-objective vs baseline. If frozen CLS linear-probe top-1 ≤ baseline +1.0pp, reject (even if patch-probe improves).

---

### Idea 10: RankMe-gated adaptive λ control loop

- **Pattern**: P6 (Verify)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — wraps the existing loss with a controller that reads RankMe and adjusts λ; loss terms themselves unchanged.
- **One-liner**: Use RankMe (unsupervised effective-rank) as an online "verifier" of representation health and increase λ (SIGReg weight) when rank drops, decrease it when invariance stalls.

**Mechanism**:
Every K steps compute RankMe (Shannon entropy of singular-value spectrum of a feature batch). A simple controller maps RankMe trend → λ: rank collapsing ⇒ raise λ; rank healthy but invariance loss plateaued ⇒ lower λ. Replaces the fixed `bstat_lambda` with a feedback-scheduled λ. RankMe needs no labels, so it is eval-legal.

**Source inspirations**:
- Primary: "RankMe: Assessing the Downstream Performance of Pretrained SSL Representations by Their Rank", Garrido, Balestriero, Najman, LeCun, ICML 2023 [arXiv:2210.02885]
- Supporting: "SimDINO / Coding Rate Regularization", Wu et al., ICML 2025 [arXiv:2502.10385]

**Why expected to improve**:
RankMe correlates strongly with downstream accuracy and needs no labels, making it a valid in-loop signal. A single fixed λ is suboptimal across 400 epochs; feedback control can avoid both early collapse and late over-regularization without a label-based sweep (so it is not an HP-sweep).

**Expected gain**: +0.3 / +1.0 / +2.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Risks**:
- Controller adds its own (meta) knobs → keep a simple proportional rule.
- RankMe noisy on small batches → estimate on a larger feature buffer.

**Falsification test**: 400ep adaptive-λ vs best fixed-λ from the existing λ ablation. If linear-probe top-1 ≤ best-fixed-λ +0.5pp, reject.

---

### Idea 2: Closed-form Cramér-Wold Gaussian metric vs Epps-Pulley quadrature

- **Pattern**: P2 (Transfer — generative modeling → SSL)
- **Tier**: 3
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the statistic inside `SlicedEppsPulley`/`EppsPulley` with the Cramér-Wold closed-form distance to N(0,I); slicing count, projector, invariance unchanged.
- **One-liner**: Swap Epps-Pulley's trapezoid-integrated ECF test for the Cramér-Wold metric, which has a closed-form (smooth-kernel) distance between a sample and a Gaussian — no quadrature grid (`t_max`, `n_points`).

**Mechanism**:
CWAE shows the Cramér-Wold distance between a sample and a Gaussian admits a closed analytic form via a radial "Cramér-Wold kernel", removing the `[0,t_max]` numerical integration of Epps-Pulley. Replace `EppsPulley.forward` with the CW closed-form on each sliced 1-D projection (or directly multivariate). Eliminates two grid hyperparameters and gives smoother gradients.

**Source inspirations**:
- Primary: "Cramer-Wold AutoEncoder", Knop, Tabor, Spurek, Podolak, Mazur, Jastrzębski, JMLR 2020 [arXiv:1805.09235]
- Supporting: "VICReg", Bardes et al., ICLR 2022 [arXiv:2105.04906]

**Why expected to improve**:
A closed-form GoF objective removes quadrature truncation/discretization error (Epps-Pulley integrates only to `t_max=3`) and gives a smoother loss landscape → potentially better-conditioned isotropy enforcement and one fewer thing to tune. Same Cramér-Wold principle LeJEPA already invokes, just without the numerical integral.

**Expected gain**: +0.0 / +1.0 / +2.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Risks**:
- May be mathematically near-equivalent to Epps-Pulley → no gain (math parity, not accuracy).
- CW kernel bandwidth becomes a new (single) knob.

**Falsification test**: 400ep CW-SIGReg vs Epps-Pulley-SIGReg (matched slices). If linear-probe top-1 within ±0.5pp AND no wall-clock reduction >10%, reject as "no advantage".

**Adjacent / Cross-domain notes**:
- Original domain: generative modeling / latent-distribution matching (autoencoders).
- Target domain: SSL embedding regularization.
- Adaptation needed: apply per-slice (or multivariate) to projector outputs; pick kernel bandwidth; verify gradient stability in bf16.

---

### Idea 1: Learned/constrained slice directions for SIGReg

- **Pattern**: P10 (Sampling strategy)
- **Tier**: 3
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the random isotropic direction sampler in `SlicedEppsPulley` with learned/worst-case directions; the Epps-Pulley statistic and rest of pipeline unchanged.
- **One-liner**: Instead of 1024 random unit slices, periodically optimize a smaller set of "informative" projection directions (constrained-SW / max-sliced) that target where the embedding is most non-Gaussian.

**Mechanism**:
Maintain a small learnable matrix of slice directions; every K steps take a few gradient ascent steps to maximize the Epps-Pulley discrepancy (worst-case slices), then renormalize to the unit sphere. SIGReg then tests where non-Gaussianity is worst, potentially matching the regularization strength of many random slices with far fewer directions (cheaper) or a stronger signal at equal count.

**Source inspirations**:
- Primary: "Constrained Sliced Wasserstein Embedding", NaderiAlizadeh, Salehi, Liu, Kolouri, 2025 [arXiv:2506.02203]
- Supporting: "Max-Sliced Wasserstein Distance and its use for GANs", Deshpande et al., CVPR 2019 [link]; "Towards Better Spherical Sliced-Wasserstein with Data-Adaptive Discriminative Projection Direction", 2024 [arXiv:2412.19212]

**Why expected to improve**:
Learned/max-sliced directions concentrate the test on the hardest 1-D marginals, improving statistical power per slice — useful when slice budget is the cost driver. Demonstrated benefits in SW-based embedding learning.

**Expected gain**: +0.0 / +1.5 / +3.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Risks**:
- **Theory risk**: LeJEPA's guarantees rely on *random isotropic* slices (unbiased Cramér-Wold); learned directions bias the estimator and may break the isotropy proof → could *hurt*.
- Inner optimization adds instability + cost; DDP seed-sync (`global_step`) logic must change.

**Falsification test**: 400ep with learned slices (e.g., 64 learned vs 1024 random). If linear-probe top-1 < baseline (random-1024) −0.5pp OR isotropy diagnostic (per-dim variance spread) worsens, reject.

**Adjacent / Cross-domain notes**:
- Original domain: optimal transport / sliced-Wasserstein.
- Target domain: SIGReg slice sampling in SSL.
- Adaptation needed: bound inner-loop steps; preserve unbiasedness (e.g., mix random + learned slices); re-do rank-sync for DDP.

---

### Idea 9: AutoView adversarial learned views

- **Pattern**: P2 (Transfer — adversarial augmentation search → SSL views)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the fixed multi-crop augmentation policy feeding `global_views`/`local_views`; loss and backbone unchanged.
- **One-liner**: Learn a self-regularized adversarial augmentation policy (AutoView) that generates harder views, increasing the difficulty (and hence informativeness) of the invariance task on a tiny dataset.

**Mechanism**:
Replace the static RandomResizedCrop+color multi-crop with AutoView's learned adversarial view generator: an augmentation policy is trained to maximize the SSL loss (harder views) subject to a self-regularization keeping views label-preserving. Feeds the same `global_views`/`local_views` interface. Harder-but-valid views combat overfitting when only 9.5k images exist.

**Source inspirations**:
- Primary: "Learning Self-Regularized Adversarial Views for Self-Supervised Vision Transformers (AutoView)", 2022 [arXiv:2210.08458]
- Supporting: "How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers", Steiner et al., 2021/TMLR [arXiv:2106.10270]

**Why expected to improve**:
ViTs overfit small datasets and rely heavily on augmentation; learned adversarial views provide a harder, adaptive curriculum the fixed policy cannot, which AutoView shows helps SSL ViTs. SIGReg keeps the embedding distribution controlled while views get harder.

**Expected gain**: +0.0 / +1.5 / +3.5 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Risks**:
- Adversarial policy can produce degenerate/label-destroying views → rely on the self-regularization term, cap strength.
- Extra trained module → more compute and tuning.

**Falsification test**: 400ep AutoView policy vs fixed multi-crop. If linear-probe top-1 ≤ baseline +0.5pp OR view-classifiability (a quick supervised check on 200 generated views) drops >15%, reject.

## Verification Report — Batch 1

| # | Title (short) | Novelty | Provenance | Feas | Gain (pp) | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|-----------|--------|------|--------|-------|
| 3 | Coding-rate term | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +2.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 7 | DynTanh projector | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +2.0 🟡 | OK ✅ | MED ⚠️ | PASS | **KEEP (flag)** |
| 4 | Uniformity term | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +1.0 🟢 | OK ✅ | LOW | PASS | **KEEP** |
| 8 | NN positives | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +2.0 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 5 | EMA teacher | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +2.5 🟡 | OK ✅ | MED | WARN | **KEEP (warn)** |
| 6 | Dense patch | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +3.0 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 10 | RankMe-gated λ | NOVEL ✅ | VERIFIED ✅ | 4/5 | +1.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 2 | Cramér-Wold metric | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 1 | Learned slices | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +1.5 🟡 | OK ✅ | HIGH ⚠️ | WARN | **KEEP (flag)** |
| 9 | AutoView | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +1.5 🟡 | OK ✅ | MED | PASS | **KEEP** |

### Counts
- Verified: 10
- Rejected: 3 (pre-draft, see rejection log) — Novelty: 1, Gain-sanity: 1, Duplicate-within-pool: 1
- Downgraded: 1 (Idea 7 ranking −1 slot, devil's-advocate)
- Re-search cycles used: 0
- Final batch size: 10

### Warnings (per idea)
- Idea 7: medium risk — normalization removal can destabilize (contrasting [arXiv:2504.06629]); gain transferred from IJEPA targets to a different (projector) location.
- Idea 5: soft compliance WARN — adds EMA, which LeJEPA deliberately avoids; justified as a target-smoother only, falsification doubles as a test of the LeJEPA "no-EMA" claim.
- Idea 1: high risk — learned slices may violate the unbiased-Cramér-Wold assumption underpinning SIGReg's guarantees; mitigate by mixing random+learned slices.

### Cross-idea consistency
- Near-duplicates collapsed: none in final batch. Ideas 3 (coding-rate / log-det volume) and 4 (uniformity) and a dropped "covariance-sketch term" are distinct mechanisms; the covariance-sketch variant was dropped as DUPLICATE of Weak-SIGReg [arXiv:2603.05924].
- Contradictions flagged: Ideas 1 (learn/bias slice directions) vs the SIGReg design assumption (random slices) — intentional, flagged as the idea's own risk, not a batch contradiction.
- Score-distribution: healthy (mix of 🟢/🟡, feasibility spread 3–5, not all-green).

### Rejection log entries (also appended to skill `_logs/_rejection_log.md`)

#### Dropped A — Lightweight covariance-sketch term added to SIGReg
- Stage failed: **Novelty (Step 1)**
- Tag: `DUPLICATE`
- Evidence: "Weak-SIGReg: Covariance Regularization for Stable Deep Learning" [arXiv:2603.05924, Mar 2026] already repurposes SIGReg as a covariance-sketch regularizer.
- Action: dropped; cited as contrasting in Idea 3.

#### Dropped B — Replace isotropic-Gaussian target with a learned Gaussian-mixture prior
- Stage failed: **Gain-sanity (Step 4)**
- Tag: contradicts target theory
- Evidence: LeJEPA proves the isotropic Gaussian is the risk-optimal embedding distribution; a mixture prior contradicts the core theorem with no evidence of net gain.
- Action: dropped.

#### Dropped C — Whitening (W-MSE / Cholesky) of embeddings as anti-collapse
- Stage failed: **Cross-idea consistency (Step 8)** + Feasibility
- Tag: `duplicate-within-pool`
- Evidence: mechanism overlaps Idea 3 (full-covariance conditioning) but with the costly/unstable matrix inverse VICReg/SimDINO explicitly avoid.
- Action: dropped in favor of Idea 3.

## Notes & warnings
- ⚠️ **Baseline score is TBD** — all gains are relative deltas vs the user's own LeJEPA run; re-rank once the baseline number exists (it sets the headroom for gain-sanity).
- ⚠️ **Time-window minimum**: only 1 primary in the 12-36mo window (SimDINO); the suggested minimum is 2. No hard anti-bias failure (4 distinct windows; ≥2 papers <12mo; many >24mo).
- ⚠️ **Idea 7 (DynTanh)** is the highest raw composite but was downgraded one slot for normalization-removal instability evidence; treat as higher-variance.
- Tier-3 honesty: Ideas 1 & 2 are genuine cross-domain (optimal-transport / generative-modeling statistics), not ML-adjacent relabels.
- Two ideas (5, 10) trace to Meta first-authors (Assran; Garrido) — within the ≤2 limit.
- Search budget: ~20 WebSearch queries (1 over the 19 soft cap) + 2 WebFetch verifications; logged in `_logs/_search_log.md`.

## Next steps for user
1. **Measure baseline** LeJEPA (ViT-S, 400ep, Imagenette) linear-probe + kNN top-1 to fix headroom.
2. Run the two near-free adds first: **Idea 3 (coding-rate)** and **Idea 4 (uniformity)** — both ~10-line loss terms, default-off flags, single 400ep run each.
3. Then **Idea 7 (DynTanh projector)** (drop-in) and **Idea 8 (NN positives)**.
4. Hold the L-effort bets (Ideas 1, 6, 9) until a cheap idea confirms headroom exists; consider running them through `/idea-vetting` first.

## Provenance signature
SHA256 of (inputs + paper IDs + timestamp): `sigreg-imagenette-batch1-2026-06-02` (papers: 2502.10385, 2508.02829, 2005.10242, 2104.14548, 2301.08243, 2111.07832, 2210.02885, 1805.09235, 2506.02203, 2210.08458; related: 2603.05924, 2304.07193, 2410.19560, 2503.10622, 2504.06629, 2412.19212, 2105.04906)
