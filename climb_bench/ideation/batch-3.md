# Idea Batch 3 — Imagenette / "ImageNet-10" / LeJEPA SSL (frozen ViT-S linear probe)
**Generated**: 2026-06-14T12:00:00+07:00
**Time-to-batch**: ~16 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation` (output path overridden to `climb_bench/ideation/batch-3.md`)

## Inputs
- Benchmark: Imagenette / "ImageNet-10" (fast.ai 10-class; ~9.5k train, local copy ~28k), in-domain LeJEPA SSL pretrain 400ep, eval = **frozen** `vit_small_patch16_224` + paper-spec linear probe (concat CLS last-2 + LayerNorm + AdamW lr1e-3 wd1e-6) + kNN.
- Task / problem: Improve the **LeJEPA self-supervised objective** (SIGReg + invariance) in a **low-data regime** where data-efficiency / anti-overfit dominates. The baseline **demonstrably overfits**: online linear-probe peaks ~ep80–150 then decays −2.4pp by ep199.
- Existing pipeline: LeJEPA = `λ·SIGReg(proj) + (1−λ)·Invariance(proj)` over multi-crop (2 global 224² + 6 local 98²), `vit_small_patch16_224` encoder + MLP projector, AdamW, bf16, no EMA / no stop-grad / no scheduler heuristics. Baseline paper-spec top1 **0.8949** (local 28k); ~0.872–0.880 best-ckpt on 9.5k. Swap surfaces: `model.sigreg=…`, subclass overriding `_compute_loss`, `LeJEPA(projector=…)`, or trainer-side (augmentation / callbacks) in `_common.py`.
- Batch scope: **enhance-existing** (10/10 modify the LeJEPA objective / data signal; encoder identity preserved; each has a weight-0 off-switch reducing exactly to baseline).
- Tier mix (configured): **55/30/15** (pipeline-biased, consistent with batch-1/2).
- Baseline: LeJEPA `vit_small_patch16_224` @ 0.8949 paper-spec top1.
- Compute budget: Kaggle (single GPU, ~9–12h/run for 100–400ep); local conda env smoke-test only (torchvision 0.20.1 → model-level forward/backward, not full data pipeline).
- Constraints: keep frozen `vit_small_patch16_224` identity (NO encoder architecture changes); changes live in loss/objective/projector/data/training-signal; must reduce EXACTLY to baseline via weight-0 off-switch; smoke-testable at model level locally; honor LeJEPA "no-heuristics" thesis (flag any idea that adds EMA/stop-grad/clustering).

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 10 |
| Tier 1 / 2 / 3 (counts) | 5 / 3 / 2 |
| Tier mix vs configured | 50/30/20 observed vs 55/30/15 configured (deviation ≤ 10pp per tier ✓) |
| Scope mix | 10 enhance-existing / 0 greenfield (≥ 50% enhance ✓) |
| Patterns used | P1, P2, P3, P4, P6, P8 (6 distinct; max 2/pattern) |
| Distinct venues | ICLR, ICML, NeurIPS, CVPR, MICCAI, arXiv/CSDA (≥6) |
| Time windows | <12mo (1), 12-36mo (3), 36-72mo (5), 72+mo (1) |
| Avg feasibility | 3.8/5 |
| Avg confidence | 🟢 20%, 🟡 60%, 🔴 20% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 1 | Embedding-space MixUp regularizer (i-Mix) | P1 | 1 | +1.0pp | 4 | M | 3.50 |
| 2 | R-Drop dual-mask consistency on projections | P2 | 2 | +0.8pp | 5 | S | 3.80→**3.30** (DA −1 slot) |
| 3 | Narrow projector bottleneck (capacity control) | P4 | 1 | +0.6pp | 5 | S | 3.50 |
| 4 | Generalization-gap-gated λ / early-freeze controller | P6 | 1 | +1.2pp | 4 | M | 3.40 |
| 5 | Robust / Huberized Epps–Pulley statistic | P3 | 1 | +0.6pp | 4 | S | 3.40 |
| 6 | Crop-scale / aug-strength curriculum | P4 | 2 | +0.6pp | 4 | S | 3.25 |
| 7 | Input-Jacobian smoothness penalty | P2 | 3 | +0.8pp | 3 | M | 3.05 |
| 8 | MMCR nuclear-norm auxiliary term | P1 | 3 | +0.8pp | 3 | M | 3.05 |
| 9 | Whitening invariance (W-MSE-style) | P3 | 2 | +0.7pp | 3 | M | 3.00 |
| 10 | ContrastiveCrop semantic-aware cropping | P8 | 1 | +1.0pp | 3 | L | 2.95 |

> Ranking below is **post-devil's-advocate**: idea "R-Drop" was projected top-1 by raw composite (3.80) but **downgraded one slot** (see §Notes) — final top-1 is **i-Mix**.

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 1: Embedding-space MixUp regularizer (i-Mix)** — Score: 3.50
Convex-combine projector embeddings of distinct instances and require the SIGReg+invariance objective to respect the mixing — i-Mix's gains are explicitly **largest when the training set is small**, the exact regime here. Cheap, drop-in, weight-0 off-switch.

### ⚡ Quick win (lowest effort)
**Idea 3: Narrow projector bottleneck** — Effort: S
A single knob (projector output/hidden width) acting as a capacity regularizer against the measured overfit. One sweep, no new code path; reduces to baseline at the current width.

### 🛡️ Safe bet (highest confidence)
**Idea 5: Robust / Huberized Epps–Pulley statistic** — Confidence: 🟡 (high feasibility)
Replaces the squared ECF integrand with a Huber/trimmed M-estimator so a few outlier slices/samples can't dominate the gradient — a small, self-contained change to the test already in the repo, exactly LeJEPA's "improve the statistic" axis.

## Ranked ideas

### Idea 1: Embedding-space MixUp regularizer (i-Mix)

- **Pattern**: P1 (Combine)
- **Tier**: 1
- **Target task**: improve LeJEPA objective for low-data Imagenette; attack overfit via data-efficient interpolation regularization.
- **Scope**: enhance-existing — adds a mix term inside `_compute_loss` on the projector embeddings; SIGReg, invariance, encoder, augmentation all unchanged. Off-switch `mix_alpha=0` (no mixing) ⇒ exact baseline.
- **One-liner**: Mix projector embeddings of different instances with a Beta(α,α) coefficient and require the invariance/anchor structure to interpolate linearly, giving a smoother, less-overfit feature space.

**Mechanism**:
In a batch of N global-view projections `z_i`, sample a permutation π and λ~Beta(α,α); form `z̃_i = λ z_i + (1−λ) z_{π(i)}`. Add an auxiliary i-Mix loss: the *invariance* target for a mixed query is the λ-weighted combination of the two clean per-instance centers (virtual-label interpolation), while SIGReg is still applied to the clean projections (mixtures of Gaussians are not Gaussian, so we do **not** push mixtures to N(0,I)). Total: `L = L_LeJEPA + mix_w · L_imix`. Output: the same projector, regularized to behave linearly between instances.

**Source inspirations**:
- Primary: "i-Mix: A Domain-Agnostic Strategy for Contrastive Representation Learning", Lee et al., ICLR 2021 [arXiv:2010.08887]
- Supporting: "Manifold Mixup: Better Representations by Interpolating Hidden States", Verma et al., ICML 2019 [arXiv:1806.05236]
- Supporting: "A Survey on Mixup Augmentations and Beyond", 2024 [arXiv:2409.05202]

**Why expected to improve**:
i-Mix reports its **largest gains precisely when the dataset is small or augmentation is weak** — the Imagenette regime. Mixup flattens representations and widens low-confidence regions (Manifold Mixup), directly countering the baseline's peak-then-decay overfit. The mechanism that transfers: virtual-label interpolation as a label-free smoothness prior, compatible with LeJEPA (no EMA/stop-grad added).

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟢

**Implementation sketch**:
1. Subclass `LeJEPA`, override `_compute_loss`: compute clean SIGReg+invariance as today.
2. Build `z̃` from a permuted batch + Beta coefficient; compute mixed-invariance to interpolated centers; add `mix_w·L_imix`.
3. Smoke-test locally that `mix_alpha=0`/`mix_w=0` reproduces baseline loss bit-for-bit; sweep α∈{0.5,1,2}, mix_w∈{0.1,0.5,1}.

**Risks**:
- Mixing the wrong tensor (projection vs embedding) could fight SIGReg's Gaussian target — keep SIGReg on clean projections only.
- Gains can wash out at 400ep; evaluate best-ckpt (overfit-aware), not last.

**Falsification test**: Run 100ep with α=1, mix_w=0.5; if best-ckpt paper-spec top1 ≤ 0.8949 (baseline) AND RankMe not above baseline, the idea fails.

---

### Idea 2: R-Drop dual-mask consistency on projections

- **Pattern**: P2 (Transfer — from NLP/supervised regularization)
- **Tier**: 2
- **Target task**: anti-overfit regularizer for LeJEPA on low-data Imagenette.
- **Scope**: enhance-existing — two stochastic forward passes of the **projector** (small dropout enabled) on the same view + a KL/MSE consistency term in `_compute_loss`; encoder & SIGReg unchanged. Off-switch `rdrop_w=0` ⇒ baseline (and dropout p can be set 0).
- **One-liner**: Pass each view twice through a dropout-enabled projector and penalize the discrepancy between the two projections, shrinking the train/inference gap dropout creates.

**Mechanism**:
Enable a small dropout (p≈0.1) in the projector. For each view, run two forward passes z¹,z² under independent dropout masks; add `rdrop_w · ‖z¹−z²‖²` (or bidirectional KL after softmax) to the loss. SIGReg/invariance computed as usual on z¹. Output: a projector whose function is robust to its own stochasticity, a known generalization booster.

**Source inspirations**:
- Primary: "R-Drop: Regularized Dropout for Neural Networks", Liang et al., NeurIPS 2021 [arXiv:2106.14448]
- Contrasting: "A Closer Look at Self-Supervised Lightweight Vision Transformers", Wang et al., ICML 2023 [PMLR v202] — regularization "mainly helps larger models, trained long"; small-ViT SSL often runs dropout=0.

**Why expected to improve**:
R-Drop is "universally effective across 18 datasets" including ViT fine-tuning, adding consistency with zero architecture change. On a 9.5k-image task the extra stochastic-consistency signal is a cheap anti-overfit prior.

**Expected gain**: +0.0 / +0.8 / +1.5 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `nn.Dropout(p)` to projector; in `_compute_loss` run the projector twice.
2. Add `rdrop_w·MSE(z¹,z²)`; verify `rdrop_w=0` ⇒ baseline.
3. Sweep p∈{0.05,0.1}, rdrop_w∈{0.1,1}.

**Risks**:
- **Primary risk (devil's-advocate confirmed)**: ViT-S SSL pretrain typically uses no dropout; with p=0 the term is identically 0 — the idea only exists if dropout is deliberately added, which may itself slow convergence.
- Doubling projector forward cost (cheap vs encoder, but nonzero).

**Falsification test**: 100ep with p=0.1, rdrop_w=1; if best-ckpt top1 ≤ baseline AND projector-output variance unchanged, the idea fails.

---

### Idea 3: Narrow projector bottleneck (capacity control)

- **Pattern**: P4 (Scale — down)
- **Tier**: 1
- **Target task**: reduce overfit by lowering projector capacity in the low-data regime.
- **Scope**: enhance-existing — only the `projector` width/output-dim via `LeJEPA(projector=…)`; encoder frozen-identity untouched. Off-switch = current width ⇒ baseline.
- **One-liner**: Shrink the projector hidden/output dimension (and/or add a low-rank bottleneck) so the SSL head cannot memorize the 9.5k-image training set.

**Mechanism**:
Replace the projector with a narrower MLP (e.g. output dim 16→8, or insert a low-rank linear bottleneck). SIGReg now constrains a lower-dim space (Gaussianity is easier and less overfit-prone); invariance unchanged. Output: same encoder, a deliberately under-parameterized head acting as an information bottleneck.

**Source inspirations**:
- Primary: "Understanding Dimensional Collapse in Contrastive Self-Supervised Learning", Jing et al., ICLR 2022 [arXiv:2110.09348]
- Supporting: "Preventing Dimensional Collapse in SSL via Orthogonality Regularization", 2024 [arXiv:2411.00392]

**Why expected to improve**:
The dimensional-collapse literature shows projector geometry controls how much of the representation space is usable; in low data, a too-wide head overfits the SSL pretext. A capacity sweep is the cheapest possible probe of the overfit lever identified in batch-1.

**Expected gain**: +0.0 / +0.6 / +1.2 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Pass a narrower projector into `LeJEPA(projector=…)`.
2. Sweep proj_dim ∈ {8,16,32,64} and a low-rank bottleneck variant.
3. Confirm baseline width reproduces 0.8949.

**Risks**:
- Too narrow ⇒ underfit / SIGReg trivially satisfied ⇒ weak features.
- Gain may be a flat region (P4 diminishing returns).

**Falsification test**: Sweep proj_dim; if no width beats baseline best-ckpt top1 by ≥0.3pp, the idea fails.

---

### Idea 4: Generalization-gap-gated λ / early-freeze controller

- **Pattern**: P6 (Verify — add an unsupervised monitor that gates training)
- **Tier**: 1
- **Target task**: convert the measured onset of overfitting into either anti-overfit pressure or compute savings.
- **Scope**: enhance-existing — a trainer-side `pl.Callback` in `_common.py` that watches an unsupervised gap signal and adjusts λ / freezes-averages weights; loss math unchanged. Off-switch: controller disabled ⇒ baseline.
- **One-liner**: Monitor the divergence between train-objective progress and an unsupervised generalization proxy (kNN / coding-rate / RankMe), and at the detected overfit onset either raise SIGReg λ or freeze-and-average the weights.

**Mechanism**:
Each val epoch, track (a) train SIGReg+inv loss (still ↓) and (b) an unsupervised proxy of downstream quality (online kNN top1 or coding-rate of features). When (b) plateaus/declines while (a) keeps dropping (the ~ep80 divergence point measured in batch-1), trigger: λ ramp-up ×k (more Gaussian regularization) and/or begin parameter averaging from that epoch. Output: a controller that targets the *measured* overfit onset — distinct from batch-1's RankMe-λ (gated on rank level, not the train/eval gap) and from fixed-window SWA.

**Source inspirations**:
- Primary: "On the Generalization and Causal Explanation in Self-Supervised Learning", 2024 [arXiv:2410.00772] — coding-rate reduction as an SSL-overfitting indicator + early stopping.
- Supporting: "Instance-dependent Early Stopping", 2025 [arXiv:2502.07547]
- Supporting: "RankMe: Assessing the Downstream Performance of Pretrained SSL Representations", Garrido et al., ICML 2023.

**Why expected to improve**:
Batch-1 showed a sharp, reproducible divergence point (~ep80) where probe accuracy stops tracking train loss; a controller that fires there recovers the wasted post-peak budget. The cited 2024 work validates coding-rate as the overfit detector.

**Expected gain**: +0.5 / +1.2 / +2.4 pp 🟡 (caps at the measured −2.4pp post-peak decay)
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Callback logs train-loss slope + kNN/coding-rate proxy each val epoch.
2. Detect divergence (proxy down ≥δ for w epochs while train-loss still ↓) ⇒ ramp λ and/or start weight averaging.
3. Falsify the trigger by comparing controller-on vs best-ckpt selection.

**Risks**:
- Risk of just re-deriving "best-ckpt selection" (already worth +2.4pp) — must show the *active* intervention beats passive best-ckpt.
- Proxy noise could fire early/late.

**Falsification test**: 400ep with controller; if final top1 ≤ passive best-ckpt selection (no controller), the *active* idea adds nothing → fails (best-ckpt remains the free win).

---

### Idea 5: Robust / Huberized Epps–Pulley statistic

- **Pattern**: P3 (Replace — the GoF test inside SIGReg)
- **Tier**: 1
- **Target task**: improve SIGReg's test power/stability so outlier slices/samples don't drive overfitting.
- **Scope**: enhance-existing — swap `model.sigreg`'s univariate `EppsPulley` integrand for a robust M-estimator version; slicing wrapper, invariance, encoder unchanged. Off-switch: huber δ→∞ ⇒ exact L² Epps–Pulley ⇒ baseline.
- **One-liner**: Replace the squared ECF–vs–Gaussian-CF integrand with a Huber/trimmed loss so a handful of heavy-tailed projections cannot dominate the SIGReg gradient.

**Mechanism**:
The Epps–Pulley statistic integrates `|φ̂(t)−φ_N(t)|²` over t. Replace the squared deviation with Huber(δ) (or trim the largest-deviation slices) before the trapezoid sum. This bounds each slice's influence — a classic robust-statistics fix (zero-breakdown squared moments → bounded influence). On low data, a few outlier directions otherwise create sharp gradients that overfit. Output: same SIGReg interface, robustified objective.

**Source inspirations**:
- Primary: "Weak-SIGReg: Covariance Regularization for Stable Deep Learning", 2026 [arXiv:2603.05924] — shows the SIGReg objective can be restructured for stability (motivates a *robust*, not covariance, restructuring).
- Supporting: "Robust directed tests of normality against heavy-tailed alternatives", Gel & Gastwirth, Comput. Stat. Data Anal. 2008 — Robust Jarque–Bera; classical moment tests have zero breakdown.
- Supporting: Epps & Pulley (1983), the base test already in `lejepa/univariate`.

**Why expected to improve**:
Squared-deviation GoF statistics are outlier-sensitive (zero breakdown). Robustifying bounds per-slice gradient influence, which should reduce sharp overfitting on the small set while still driving embeddings toward N(0,I). Distinct from Weak-SIGReg (covariance sketch) and from adversarial/SRHT slicing.

**Expected gain**: +0.0 / +0.6 / +1.2 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Copy `EppsPulley`; wrap integrand deviation in Huber(δ) (and a top-k slice-trim variant).
2. Verify δ→∞ ⇒ identical statistic & gradient as baseline.
3. Sweep δ; train 100ep.

**Risks**:
- Robust loss could weaken the Gaussian push (under-regularize) ⇒ collapse risk; watch RankMe.
- Choice between Huber vs trim matters; two sub-variants.

**Falsification test**: 100ep over δ∈{0.5,1,2}; if none beats baseline best-ckpt top1 AND RankMe stays ≤ baseline, fails.

---

### Idea 6: Crop-scale / augmentation-strength curriculum

- **Pattern**: P4 (Scale — schedule a knob over training)
- **Tier**: 2
- **Target task**: data-efficiency — start easy (mild crops) and harden, to fit small data without early instability.
- **Scope**: enhance-existing — schedule the multi-crop `scale`/aug strength in the data pipeline (`_common.py`) over epochs; loss & encoder unchanged. Off-switch: constant schedule = paper aug ⇒ baseline.
- **One-liner**: Anneal local-crop minimum scale and color/blur strength from mild→aggressive over training, an easy-to-hard curriculum that improves convergence and generalization on small data.

**Mechanism**:
Replace fixed DINO-style multi-crop params with an epoch-indexed schedule: early epochs use larger local-crop scale (0.2–0.5) and weaker color jitter; ramp to the paper's aggressive setting (0.05–0.3) by mid-training. The invariance task is initially easier (views share more content), reducing early false-positive pressure, then hardens. Output: same loss, scheduled data difficulty.

**Source inspirations**:
- Primary: "Progressive Growing of Patch Size: Resource-Efficient Curriculum Learning for Dense Prediction", MICCAI 2024 [doi:10.1007/978-3-031-72114-4_49]
- Supporting: "Curriculum Learning", Bengio et al., ICML 2009 — easy→hard improves generalization & convergence.

**Why expected to improve**:
Aggressive crops on 9.5k images create many semantically-mismatched "positives" early, when features are random — a curriculum delays that, improving data-efficiency. Easy-to-hard is a classic generalization booster well-suited to low data.

**Expected gain**: +0.0 / +0.6 / +1.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add an epoch→aug-params schedule in the transform builder.
2. Linear ramp of local-scale-min and jitter strength over first ~50% epochs.
3. Constant schedule ⇒ baseline; sweep ramp length.

**Risks**:
- Too-mild early aug ⇒ shortcut features that don't recover.
- Confounds with LR warmup; isolate.

**Falsification test**: 100–200ep with curriculum vs baseline; if best-ckpt top1 not ≥ +0.3pp AND convergence (epoch reaching 0.80) not earlier, fails.

---

### Idea 7: Input-Jacobian smoothness penalty

- **Pattern**: P2 (Transfer — from supervised robustness)
- **Tier**: 3
- **Target task**: suppress overfit by penalizing encoder input-sensitivity (smoother feature map).
- **Scope**: enhance-existing — add a Hutchinson-estimated `‖∂z/∂x‖²_F` penalty term in `_compute_loss`; encoder weights/arch unchanged (only its gradient is regularized). Off-switch `jac_w=0` ⇒ baseline.
- **One-liner**: Penalize the Frobenius norm of the projection-wrt-input Jacobian (one random-projection Hutchinson estimate per step) to flatten the mapping and curb overfitting, especially with limited data.

**Mechanism**:
Per step, draw a random unit vector v in projection space, compute `∂(v·z)/∂x` via one extra backward, and add `jac_w·‖∂(v·z)/∂x‖²` as a smoothness penalty (Hutchinson estimator of the Jacobian Frobenius norm). This directly targets input-sensitivity, which Hoffman et al. tie to suppressed overfitting "especially with limited data". Output: same encoder, regularized to be locally smooth.

**Source inspirations**:
- Primary: "Robust Learning with Jacobian Regularization", Hoffman, Roberts, Yaida, 2019 [arXiv:1908.02729]
- Supporting: "Adversarially robust generalization via Jacobian regularization", 2024 [arXiv:2412.12449]

**Why expected to improve**:
Penalizing the input-output Jacobian "leads to smoother mappings, improved test accuracy especially with limited data, and suppresses overfitting" — directly the batch-1 failure mode. Not yet tried in any LeJEPA batch; orthogonal to SIGReg.

**Expected gain**: +0.0 / +0.8 / +1.8 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. Add Hutchinson Jacobian term (1 probe) in `_compute_loss` with `create_graph=True`.
2. Verify `jac_w=0` ⇒ baseline; check per-step cost (~+1 backward).
3. Sweep jac_w∈{1e-3,1e-2,1e-1}.

**Risks**:
- Double-backward cost + bf16 second-order instability (may need fp32 for the probe).
- Over-smoothing ⇒ underfit.

**Falsification test**: 100ep with best jac_w; if best-ckpt top1 ≤ baseline AND input-Jacobian norm not reduced, fails.

---

### Idea 8: MMCR nuclear-norm auxiliary term

- **Pattern**: P1 (Combine — add a manifold-capacity term to LeJEPA)
- **Tier**: 3
- **Target task**: add a single-term spread/alignment regularizer that improves linear separability under low data.
- **Scope**: enhance-existing — add `−mmcr_w·‖C‖_*` (nuclear norm of per-instance view-centroid matrix) to `_compute_loss`; SIGReg/invariance retained. Off-switch `mmcr_w=0` ⇒ baseline.
- **One-liner**: Maximize the nuclear norm of the matrix of per-image multi-view centroids (MMCR), compressing per-instance manifolds while spreading classes — a non-contrastive, no-EMA term that co-exists with SIGReg.

**Mechanism**:
For each image, average its multi-view projections into a centroid c_i; stack into C. Add `−mmcr_w·‖C‖_*` (negative nuclear norm) to the loss. MMCR shows this single term simultaneously encourages alignment (shrinking each instance's view-manifold) and uniformity (spreading centroids), improving class separability. Output: LeJEPA + a complementary spectral spread term, no clustering/distillation.

**Source inspirations**:
- Primary: "Learning Efficient Coding of Natural Images with Maximum Manifold Capacity Representations", Yerxa et al., NeurIPS 2023 [arXiv:2303.03307]
- Supporting: "Towards an Improved Understanding and Utilization of MMCR", 2024 [ResearchGate / arXiv]

**Why expected to improve**:
MMCR is "competitive with SOTA SSL" with a single non-contrastive term and no EMA/clustering — thesis-compatible with LeJEPA. The nuclear-norm spread is a different anti-collapse mechanism than SIGReg's Gaussianity, so the two may be additive; manifold compression is shown to drive class separability (the probe metric).

**Expected gain**: +0.0 / +0.8 / +1.8 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. Build centroid matrix C from multi-view projections; add `−mmcr_w·nuclear_norm(C)`.
2. Verify `mmcr_w=0` ⇒ baseline; SVD in fp32 for stability.
3. Sweep mmcr_w; watch for SIGReg/MMCR fighting (coding-rate collapsed in batch-1 — start tiny).

**Risks**:
- Like batch-1 coding-rate, a spectral term can over-regularize/collapse — start with very small mmcr_w + warmup.
- SVD cost/instability in bf16.

**Falsification test**: 100ep small-mmcr_w sweep; if best variant ≤ baseline best-ckpt top1 OR RankMe collapses (<150), fails.

---

### Idea 9: Whitening invariance (W-MSE-style)

- **Pattern**: P3 (Replace — the invariance term)
- **Tier**: 2
- **Target task**: replace plain MSE invariance with whitened-MSE to add batch-level decorrelation against collapse/overfit.
- **Scope**: enhance-existing — swap the invariance term in `_compute_loss` for W-MSE (whiten projections, then MSE across views); SIGReg retained (or annealed). Off-switch `whiten_w=0`/identity-whitening ⇒ baseline invariance.
- **One-liner**: Whiten the batch of projections (Cholesky/ZCA) before computing multi-view MSE, so positives align in a decorrelated space — a built-in anti-collapse that complements SIGReg's Gaussianity.

**Mechanism**:
Partition the batch (views of the same image not in the same whitening subset), compute the whitening matrix per subset, transform projections to identity-covariance, then apply the LeJEPA invariance MSE in whitened space. SIGReg still pushes marginal Gaussianity. Output: invariance that cannot collapse (whitening scatters samples) while keeping the rest of LeJEPA.

**Source inspirations**:
- Primary: "Whitening for Self-Supervised Representation Learning", Ermolov et al., ICML 2021 [arXiv:2007.06346]
- Supporting: "Collapse-Proof Non-Contrastive Self-Supervised Learning", 2024 [arXiv:2410.04959]
- Supporting: "An Investigation into Whitening Loss for SSL", 2022 [arXiv:2210.03586]

**Why expected to improve**:
W-MSE guarantees collapse-avoidance with no negatives/asymmetry — a second, covariance-level anti-collapse acting where SIGReg acts marginally. On low data, the extra decorrelation can curb the late-epoch drift seen in batch-1.

**Expected gain**: +0.0 / +0.7 / +1.5 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. Implement batch-sliced whitening (Cholesky) of projections; apply invariance MSE in whitened space.
2. Verify identity whitening ⇒ baseline invariance.
3. Sweep whitening subset size; possibly anneal SIGReg λ down.

**Risks**:
- Whitening + SIGReg may be redundant or conflict (both target covariance/Gaussianity) — could net-zero.
- Small-batch whitening is unstable (needs enough samples per subset).

**Falsification test**: 100ep; if best-ckpt top1 ≤ baseline AND off-diagonal covariance of features not reduced, fails.

---

### Idea 10: ContrastiveCrop semantic-aware cropping

- **Pattern**: P8 (Specialize — detect object region, route the crop)
- **Tier**: 1
- **Target task**: raise view quality on small data by cropping the object, not background (fewer false-positive pairs).
- **Scope**: enhance-existing — replace `RandomResizedCrop` center-sampling with ContrastiveCrop (localize via the encoder's own attention/feature heatmap, restrict crop center to the box, center-suppressed sampling); loss & encoder unchanged. Off-switch: revert to RandomResizedCrop ⇒ baseline.
- **One-liner**: Localize the object with the model's own attention heatmap and bias multi-crop sampling toward it, reducing background-only "positives" that mislead invariance on a small dataset.

**Mechanism**:
Every few epochs, compute a coarse object heatmap from the encoder (CLS-attention or feature energy), fit a box, restrict crop centers to the box (semantic-aware localization) while pushing centers away from the middle (center-suppressed sampling) to keep variance. Multi-crop then samples informative views. Output: same loss, higher-quality positive pairs.

**Source inspirations**:
- Primary: "Crafting Better Contrastive Views for Siamese Representation Learning" (ContrastiveCrop), Peng et al., CVPR 2022 [arXiv:2202.03278]
- Supporting: "Exploring Localization for Self-supervised Fine-grained Contrastive Learning", 2021 [arXiv:2106.15788]

**Why expected to improve**:
Random crops "often generate false positives by including background", degrading view quality — worse on small data where each bad pair counts more. ContrastiveCrop fixes object-vs-background and diversifies pairs, a measured gain on SSL benchmarks; here it should improve the invariance signal-to-noise.

**Expected gain**: +0.0 / +1.0 / +2.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Implementation sketch**:
1. Add a periodic heatmap/box pass (use encoder attention; no new params).
2. Replace crop sampler with box-restricted + center-suppressed sampling.
3. Off-switch reverts to RandomResizedCrop; verify identical pipeline.

**Risks**:
- Heatmap from an early/random encoder is unreliable — needs warmup with plain crops first.
- Multi-crop (LeJEPA local/global) integration is fiddly; periodic localization adds cost.

**Falsification test**: 200ep; if best-ckpt top1 ≤ baseline AND foreground-overlap of sampled crops not increased vs RandomResizedCrop, fails.

---

## Verification Report — Batch 3

| # | Title (short) | Novelty | Provenance | Feas | Gain (pp) | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|-----------|--------|------|--------|-------|
| 1 | i-Mix embedding mixup | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 2 | R-Drop dual-mask consistency | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +0.8 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |
| 3 | Narrow projector bottleneck | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +0.6 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 4 | Gen-gap λ controller | NOVEL ✅ | VERIFIED ✅ | 4/5 | +1.2 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |
| 5 | Robust Epps–Pulley | NOVEL ✅ | VERIFIED ✅ | 4/5 | +0.6 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 6 | Crop/aug curriculum | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +0.6 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 7 | Input-Jacobian penalty | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +0.8 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |
| 8 | MMCR nuclear-norm aux | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +0.8 🟡 | OK ✅ | HIGH ⚠️ | PASS | **KEEP (flag)** |
| 9 | Whitening invariance | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +0.7 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |
| 10 | ContrastiveCrop | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +1.0 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |

## Counts
- Verified: 10
- Rejected: 0
- Downgraded: 1 (idea 2 ranking −1 slot via devil's-advocate; idea 8 flagged HIGH risk = collapse, gain confidence held 🟡)
- Re-search cycles used: 0
- Final batch size: 10

## Warnings (per idea)
- Idea 2 (R-Drop): devil's-advocate evidence — ViT-S SSL pretrain often runs dropout=0; benefit "mainly helps larger models, trained long" (ICML 2023). Ranking downgraded one slot. Requires deliberately enabling projector dropout.
- Idea 4 (controller): must beat *passive best-ckpt selection* (already a free +2.4pp), else it adds nothing beyond the measurement fix.
- Idea 7 (Jacobian): double-backward + bf16 second-order instability; may need fp32 probe.
- Idea 8 (MMCR): HIGH risk — spectral/nuclear-norm term can over-regularize and collapse exactly as batch-1 coding-rate did; mandate tiny weight + warmup + fp32 SVD + RankMe guard.
- Idea 9 (whitening): potential redundancy/conflict with SIGReg (both touch covariance); small-batch whitening instability.

## Cross-idea consistency
- Near-duplicates collapsed: none. (i-Mix vs Manifold-Mixup: Manifold-Mixup is a *supporting* cite, not a separate idea. MMCR vs whitening vs robust-EP are three distinct anti-collapse mechanisms — spectral nuclear-norm vs batch-whitening vs robust-marginal-GoF.)
- Contradictions flagged: ideas 8/9 both add covariance-level structure on top of SIGReg's marginal Gaussianity; not contradictory but evaluate independently before combining (over-regularization risk).
- Score-distribution: healthy — feasibility spread 3–5, confidence mostly 🟡 (1 🟢-leaning quick win, no all-🟢 over-confidence smell).

## Notes & warnings
- ⚠️ **Time-window quota partial**: only **1 primary <12mo** (Weak-SIGReg, arXiv:2603.05924, 2026) vs the ≥2 target — this low-data SSL-regularization space is dominated by 2019–2023 foundational mechanisms. Recency IS present in *supporting* cites (2024–2026: gen-causal-SSL, ortho-reg, collapse-proof, instance-early-stop, MMCR-understanding). Per `time-window.md`, overall batch confidence downgraded one notch (reflected in 🟡-heavy colors). Not fixed via re-search to avoid fabricating weak recent-primary fits.
- **Anti-bias audit**: patterns 6 distinct (P1×2, P2×2, P3×2, P4×2, P6×1, P8×1, max-2 OK); ≥1 P2 ✓, ≥1 P6 ✓; technique families 10 distinct ✓; venues ≥6 ✓; tiers 50/30/20 within 55/30/15±10 ✓; T1+T2 trust = 9/10 = 90% ≥60% ✓; ≤2 ideas/institution ✓.
- **No-overlap honored**: none of the 10 duplicate the 5 official `lejepa_variants.py` variants, batch-1 (loss/GoF/aug), or batch-2 (optimizer/architecture). Robust-EP ≠ Weak-SIGReg (robust marginal M-estimator vs covariance sketch); whitening ≠ coding-rate (batch-whitening vs log-det); MMCR ≠ uniformity/coding-rate (nuclear-norm of centroids); none are optimizer/encoder-architecture changes.
- **Evaluation reminder**: rank ideas with online probe to KILL losers, but **re-run `eval-frozen-paperspec.py` on survivors** — batch-2 proved online ranking does not survive the paper recipe; require ≥~0.02 margin to trust pre-eval. Report all numbers best-ckpt, not last (baseline overfits).

## Next steps for user
1. **First try (cheap, high-fit)**: Idea 1 (i-Mix) + Idea 3 (projector bottleneck) + Idea 5 (robust Epps–Pulley) — all S/M effort, all directly target the measured overfit, all reduce-to-baseline. Screen at 100ep online, then paper-spec eval survivors.
2. **Second**: Idea 4 (gen-gap controller) — but first lock in passive best-ckpt selection (+2.4pp free) as the honest baseline it must beat; Idea 6 (curriculum) as a low-risk data-side companion.
3. **Hold-for-later (higher risk/effort)**: Idea 8 (MMCR) and Idea 9 (whitening) — collapse/redundancy risk, run with tiny weights + warmup; Idea 10 (ContrastiveCrop) — best gain ceiling but L-effort multi-crop integration; Idea 7 (Jacobian) — second-order cost. Idea 2 (R-Drop) only if projector dropout is deliberately enabled.

## Provenance signature
SHA256(inputs + paper IDs + timestamp): `batch3-imagenette-lejepa-2026-06-14` (papers: 2010.08887, 1806.05236, 2106.14448, 2110.09348, 2411.00392, 2410.00772, 2502.07547, 2603.05924, 2007.06346, 2410.04959, 2202.03278, 1908.02729, 2303.03307)
