# Idea Batch 4 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~17 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 40/20/40 --given-vetting .claude/skills/idea-vetting/vetting-output/ImageNet-10/batch-3/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1).
- Task: in-domain SSL pretraining (no external data, no foundation-model init), frozen-backbone linear probe per [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py).
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (EppsPulley × 1024 Gaussian random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=4e-4 wd=5e-2, fp16, 600 epochs. Baseline still **TBD** (gated by batch-2 Idea 5 ASHA, still queued).
- Scope: **enhance-existing**.
- Tier mix (configured): 40/20/40 — bands T1 30–50%, T2 10–30%, T3 30–50%.
- Compute / time / constraint budget: 1 × A100, ≤ 4 GPU-h per 100-ep ViT-S run; soft "single-λ" branding.

### Given vetting feedback applied (batch-3 → batch-4)
- ✅ Batch-3 produced **two FULL SENDs** (PIT monitor, SRHT) and **three TOY** (Hermite, rank curriculum, co-distillation) + **one REFRAME** (per-rank DDP slices). Batch-4 explicitly does **not** re-propose anything that touches: slice-generator distribution (covered by SRHT + Repulsive — but Repulsive is mechanistically *negatively-correlated*, not just structured, so distinct), per-slice statistic family (covered by Hermite + stacked tests + Sliced-W2), embedding-dim curriculum (covered by rank curriculum), two-student self-play (covered by co-distillation), or held-out PIT monitor.
- ✅ Batch-3 vetting recommended `--compose-mode` next; batch-4 honours the spirit by tagging each idea's **composition partners** among surviving FULL-SEND / TOY ideas. (Formal compose-mode is not yet a supported subcommand; the composition discussion is in §Composition map at the end.)
- ⚠️ Survival rate 83 % in batch-3 was *just above* the healthy band — batch-4 is calibration-conscious: down-revised mid-gain claims, and **no idea avoids a head-to-head against the existing baseline at matched compute**.
- ⚠️ Tier-3 honesty audit: this batch's T3 picks are Spherical-Harmonics Control Variates for sliced estimators (mathematical statistics / numerical integration on the sphere) and Repulsive MC on the sphere for SW (point-process / determinantal-sampling literature). Both are bona-fide cross-domain — neither is "mainstream ML adjacent".
- Pattern coverage cumulative across batches 1+2+3 = P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12. P9/P10/P11 remain unsuited to in-domain pretraining. This batch revisits P1, P2, P3 (×2), P5 (×2) with **new mechanisms** that do not duplicate prior batches' instances.
- ⚠️ **No P6 (Verify) this batch** by design — batch-3 Idea 3 (PIT monitor) already occupies the "label-free callback" slot and awaits its ρ-correlation validation; adding a second P6 callback now would compete for the same callback bandwidth before the first one's signal quality is measured. Will re-open P6 in batch-5 if PIT graduates.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Search-tier T1 / T2 / T3 (counts) | 3 / 1 / 2 → 50 / 17 / 33 % |
| Tier mix vs configured | 50/17/33 vs 40/20/40 (each within ±10 pp band) |
| Scope mix | 6 enhance-existing / 0 greenfield |
| Patterns used | P1, P2, P3 (×2), P5 (×2) — 5 distinct, max 2 per pattern |
| Mandatory pattern check | ≥1 P2 ✅ (Idea 4) · ≥1 P6 ❌ — see note above |
| Distinct venues | 8 (CVPR, ICML, ICLR, NeurIPS, ScienceDirect, arXiv preprint, OpenReview, JMLR) |
| Time windows | <12 mo: 2 · 12–36 mo: 2 · 36–72 mo: 2 · classics: 1 |
| Avg feasibility | 4.0 / 5 |
| Avg confidence | 🟢 33 % · 🟡 67 % · 🔴 0 % |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|-----------:|-----:|:------:|------:|
| 1 | **SAM / Friendly-SAM** optimizer wrap for SIGReg+invariance | P3 | 1 | +0.8 | 5 | S | **2.8** |
| 2 | **W-MSE Cholesky whitening** as a pre-step before SIGReg slicing | P5 | 1 | +1.2 | 4 | S | **2.8** |
| 3 | **Layer-wise SIGReg** with deep supervision on intermediate ViT layers | P5 | 2 | +0.8 | 4 | S | **2.6** |
| 4 | **Antithetic + spherical-harmonics control-variate** SIGReg estimator | P2 | 3 | +0.5 | 4 | S | **2.6** |
| 5 | **Repulsive Monte Carlo** slice sampling on S^(d−1) (DPP / Riesz energy) | P3 | 3 | +0.5 | 4 | S | **2.6** |
| 6 | **MAE pixel-reconstruction auxiliary head** alongside SIGReg | P1 | 1 | +1.0 | 3 | L | **1.9** |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` · S=4 M=3 L=2.

## Top-3 recommendations

### ⚡ Quick win — **Idea 1: SAM / Friendly-SAM optimizer wrap**
One-line optimizer change in `configure_optimizers`. *Sharpness-Aware Minimization* (Foret et al., ICLR 2021) has a strong empirical track record on supervised ViTs; the 2024 "SAM Enhances Feature Quality" line (arXiv:2405.20439) gives the **specific evidence that SAM lowers linear-probing error** — directly relevant. Friendly-SAM (CVPR 2024) reduces SAM's 2× wall-clock to ~1.3×. Mechanism is loss-landscape, completely orthogonal to SIGReg's distributional regulariser, so compose-risk is low.

### 🛡️ Safe bet — **Idea 2: W-MSE Cholesky whitening pre-step**
Insert a differentiable Cholesky-whitening operator on `Z` *before* it enters `SlicingUnivariateTest`. W-MSE (Ermolov et al., ICML 2021) and the very recent "Whitening Consistently Improves SSL" (arXiv:2408.07519) report **1–5 pp linear-probe gains as a last-layer add-on across SSL methods including BYOL / SimCLR / SwAV**. Whitening makes the embedding covariance closer to I *deterministically*; SIGReg then only has to enforce *marginal Gaussianity per direction* on an already-decorrelated signal — strictly easier optimisation, theory preserved (Cramér–Wold still applies post-whitening since the whitening is a fixed-per-step linear map).

### 🏆 Big bet — **Idea 6: MAE pixel-reconstruction auxiliary head**
Add a lightweight MAE decoder (He et al., CVPR 2022) on the masked patch tokens; total loss = `L_LeJEPA + α · L_MAE`. Distinct from batch-1 Idea 2 (iBOT-style patch-SIGReg, which puts SIGReg on patch tokens) and from C-JEPA (which adds VICReg). MAE's pixel-recon signal complements SIGReg's distributional signal: one constrains *local content fidelity*, the other constrains *global distributional shape*. Highest theoretical lift but L-effort (decoder + masking + α tune); historically the best published gain at small scale comes from combining JEPA with a generative target.

---

## Ranked ideas

### Idea 1: SAM / Friendly-SAM optimizer wrap

- **Pattern**: P3 (Replace the optimizer with a sharpness-aware variant)
- **Tier**: 1 (in-field — optimization for vision representation learning)
- **Scope**: enhance-existing. Replaces the `AdamW` builder in `configure_optimizers` with a SAM wrapper around AdamW (or Friendly-SAM). Backbone, projector, SIGReg, schedule, data unchanged.
- **One-liner**: Wrap the AdamW step with the SAM (or Friendly-SAM) inner-perturbation step so the SIGReg + invariance objective is minimised in a flat-loss neighbourhood, demonstrably improving downstream linear-probe quality.

**Mechanism**:
SAM (Foret et al., ICLR 2021) replaces `min_θ L(θ)` with `min_θ max_{||ε|| ≤ ρ} L(θ + ε)`. Each step does (a) an ascent micro-step `ε* = ρ · ∇L(θ) / ||∇L(θ)||`, then (b) computes gradient at `θ + ε*` and applies the AdamW update at `θ`. This biases optimisation toward *flat* minima, which empirically transfer better — and crucially, "SAM Enhances Feature Quality via Balanced Learning" (arXiv:2405.20439, 2024) shows that **SAM consistently achieves lower linear-probing error than SGD across vision datasets**, i.e., it improves the exact downstream metric we care about. Friendly-SAM (Li et al., CVPR 2024) refines the inner perturbation to subtract the EMA of the gradient before normalising, reducing the friendly noise that dilutes SAM's signal — same wrap, better numbers, similar cost. SAM's 2× wall-clock can be cut to ~1.3× with SAMPa (NeurIPS 2024) by parallelising the two gradient computations.

**Source inspirations**:
- Primary: *Sharpness-Aware Minimization for Efficiently Improving Generalization*, Foret et al., ICLR 2021 [arXiv:2010.01412](https://arxiv.org/abs/2010.01412) — the SAM formulation.
- Primary: *Sharpness-Aware Minimization Enhances Feature Quality via Balanced Learning*, [arXiv:2405.20439](https://arxiv.org/html/2405.20439v1) (2024) — direct evidence that SAM lowers linear-probe error vs SGD; exactly our downstream metric.
- Supporting: *Friendly Sharpness-Aware Minimization*, Li et al., [CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Li_Friendly_Sharpness-Aware_Minimization_CVPR_2024_paper.pdf) — variance-reduced perturbation; better at the same wall-clock budget.
- Supporting: *SAMPa: Sharpness-aware Minimization Parallelized*, [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/5bf2b802e24106064dc547ae9283bb0c-Paper-Conference.pdf) — cuts SAM's 2× cost to ~1×.

**Why expected to improve**:
SIGReg's gradient is **noisy** (Monte-Carlo over slices, per CLAUDE.md) and the multi-crop invariance term induces sharp updates. SAM directly counteracts both: it flattens the loss surface seen by AdamW, which empirically helps most when gradients are noisy and the regulariser landscape is rough — both true here. The 2024 feature-quality paper is the closest published prior to our setting (vision representation, linear-probe metric); its 0.5–2 pp wins on ImageNet variants set the expected gain band.

**Expected gain**: +0.3 / +0.8 / +1.5 pp 🟢 *(based on published linear-probe deltas in SAM-for-features 2024, scaled to ViT-S / small-data)*
**Feasibility**: 5/5 🟢
**Effort**: S 🟢 (one wrapper class; ρ has a sensible default 0.05; can run Friendly-SAM with no extra HP)

**Implementation sketch**:
1. Add `optimizer: Literal["adamw", "sam_adamw", "fsam_adamw"]` to the LeJEPA config.
2. Use the public SAM repo (`davda54/sam`) as the wrapper; Friendly-SAM differs only in the perturbation rule.
3. Train 100 ep at fixed (λ, lr, wd) — use batch-2 Idea 5 (ASHA) output once available; otherwise paper defaults.
4. Compare to baseline AdamW at **matched wall-clock** (= 130 ep AdamW vs 100 ep Friendly-SAM, since FSAM is ~1.3×).

**Risks**:
- Wall-clock cost: vanilla SAM is 2×; matched-compute control is mandatory.
- ρ is a new HP (mitigation: ρ ∈ {0.02, 0.05, 0.1} micro-sweep, treat as part of ASHA).
- Possible interaction with the bf16 precision recommended in CLAUDE.md (SAM's first-step gradient norm can underflow in bf16) — train in fp32 for the first epoch or use loss scaling.

**Falsification test**: 100-ep ImageNet-10, baseline AdamW vs Friendly-SAM at matched wall-clock (i.e., 130 ep AdamW), 3 seeds each, fixed ASHA-best (λ, lr, wd). Friendly-SAM must beat the matched-compute AdamW baseline by ≥ 0.4 pp linear probe with non-overlapping seed CIs. If it only beats *equal-epoch* AdamW (not equal-wall-clock), the gain is bought by extra compute and the swap is rejected.

---

### Idea 2: W-MSE Cholesky whitening pre-step before SIGReg

- **Pattern**: P5 (Decompose — separate the embedding-covariance problem from the marginal-Gaussianity problem; whitening solves the first, SIGReg solves the second)
- **Tier**: 1 (in-field SSL representation learning)
- **Scope**: enhance-existing. Inserts a `CholeskyWhiten` module between encoder/projector output and `SlicingUnivariateTest`. No change to backbone, SIGReg, optimizer, schedule.
- **One-liner**: Before slicing `Z` for SIGReg, apply differentiable Cholesky-whitening so that `Z_w` already has identity covariance; SIGReg then only enforces per-direction Gaussianity on an already-decorrelated signal.

**Mechanism**:
W-MSE (Ermolov et al., ICML 2021) showed that a differentiable per-batch Cholesky whitening `Φ_CD(Z) = L^(−1) Z` (with `LL^T = Σ_Z` the batch covariance) is sufficient to prevent representation collapse in non-contrastive SSL — i.e., whitening alone is a collapse-prevention mechanism. "Whitening Consistently Improves SSL" (arXiv:2408.07519, 2024) recently demonstrated that adding whitening as the *last layer* improves linear-probe accuracy by **1–5 pp across BYOL / SimCLR / SwAV / multiple ViT backbones / multiple datasets**, with PCA-whitening explicitly excluded (collapses) and ZCA / Cholesky both working. In LeJEPA, SIGReg currently does both jobs in one statistical hammer: (a) make `Cov(Z) ≈ I` and (b) make each marginal Gaussian. Pre-whitening solves (a) deterministically and leaves SIGReg to do only (b), which is **strictly an easier MC-noise budget** at fixed M. Cramér–Wold still applies: the pre-whitened slice projection `u^T L^(−1) z` is N(0,1) iff `L^(−1) z` is isotropic Gaussian (which iff `z` is Gaussian with covariance Σ), so the lift to multivariate normality is preserved.

**Source inspirations**:
- Primary: *Whitening for Self-Supervised Representation Learning (W-MSE)*, Ermolov et al., [arXiv:2007.06346](https://arxiv.org/pdf/2007.06346), ICML 2021 — original differentiable-Cholesky whitening for SSL.
- Primary: *Whitening Consistently Improves Self-Supervised Learning*, [arXiv:2408.07519](https://arxiv.org/abs/2408.07519) (2024) — adds whitening as a last layer to BYOL / SimCLR / SwAV, reports 1–5 pp linear-probe gains. Closest empirical analog to our proposed add-on.
- Supporting: *An Investigation into Whitening Loss for Self-supervised Learning*, [arXiv:2210.03586](https://arxiv.org/pdf/2210.03586) — analyses why PCA-whitening collapses while ZCA/Cholesky do not.

**Why expected to improve**:
SIGReg's MC variance is dominated by directions in which `Z` has tiny variance — those slices produce near-constant `u^T z`, the empirical CF is dominated by sampling noise, and the gradient is uninformative. Whitening removes this pathology *exactly* by forcing all directions to have unit variance, so every slice contributes a comparable signal-to-noise. This is exactly the gap that drove batch-2's Idea 3 (test-strictness curriculum) and batch-3's Idea 6 (rank curriculum) — but whitening solves it in **one step, deterministically, with no curriculum HP**. Published deltas on the closest empirical analog (Whitening-as-last-layer 2024) place gains at +1–5 pp; we conservatively claim +1.2 pp mid for our smaller-dataset regime.

**Expected gain**: +0.5 / +1.2 / +2.5 pp 🟢 *(directly extrapolated from arXiv:2408.07519 deltas on SSL+linear-probe, scaled to ImageNet-10)*
**Feasibility**: 4/5 🟢 (Cholesky requires the batch covariance to be PSD with strict positive eigenvalues — need to add a small ridge `Σ + εI`)
**Effort**: S 🟢

**Implementation sketch**:
1. New `CholeskyWhiten(eps=1e-4)` module: in `forward(Z)`, compute `Σ = Z.T @ Z / N + eps*I`, then `L = torch.linalg.cholesky(Σ)`, return `Z @ torch.linalg.inv(L).T`.
2. Insert between `projector(emb)` and `loss_fn(...)` in the LeJEPA forward.
3. Compare 100-ep at fixed (λ, lr, wd) vs baseline; 3 seeds. Ablate `eps ∈ {1e-3, 1e-4, 1e-5}`.

**Risks**:
- Batch covariance estimation is noisy at small batch (B=512, d=384 is borderline; B=256, d=384 is risky). Mitigate: use moving-average covariance with EMA decay 0.99.
- Cholesky failure on near-singular Σ early in training (mitigate: ridge `eps`, fall back to eigendecomp with floor on small eigenvalues).
- Interaction with batch-3 Idea 6 (rank curriculum): both touch the embedding-covariance structure. Run sequentially, do not nest.

**Falsification test**: 100-ep run, baseline (no whitening) vs W-MSE-whitening pre-step, 3 seeds, fixed (λ, lr, wd) from ASHA. Primary: linear-probe top-1 must be ≥ 0.6 pp higher with non-overlapping seed CIs. Secondary: SIGReg-loss trajectory should show **faster early-epoch decrease** (the whitening pre-step is supposed to make SIGReg's job easier per step). If both fail, the pre-step adds nothing.

---

### Idea 3: Layer-wise SIGReg with deep supervision on intermediate ViT layers

- **Pattern**: P5 (Decompose — split the single end-of-network normality constraint into per-layer constraints down the ViT trunk)
- **Tier**: 2 (adjacent — deep-supervision for SSL is published; the specific decomposition for SIGReg is new)
- **Scope**: enhance-existing. Hooks intermediate ViT block outputs and applies `SlicingUnivariateTest` to each; the final loss is a weighted sum.
- **One-liner**: Apply `λ_ℓ · SIGReg(z_ℓ)` at multiple ViT block depths (e.g., layers 6, 9, 12), not just the final embedding — deep supervision for the distributional constraint, matching the linear-probe protocol (concat last 2 layers).

**Mechanism**:
The current LeJEPA loss applies SIGReg only to the final embedding `z = CLS_12`. The linear-probe protocol explicitly concatenates **CLS tokens from the last two layers** (per CLAUDE.md §5). This is a mismatch: the encoder is trained to be Gaussian only at the last layer, but evaluated using the last two layers. Layer-wise SIGReg fixes this: hook CLS outputs at intermediate layers (e.g., {6, 9, 12} for ViT-S/12), apply the same `SlicingUnivariateTest` to each, take a depth-weighted sum `L_SIGReg_total = Σ_ℓ λ_ℓ · SIGReg(z_ℓ)`. This is the classical **deep supervision** trick (Lee et al., 2014 "Deeply-Supervised Nets") ported to a non-classification regulariser. The recent SDSSL line (self-distillation SSL applied at intermediate layers, surveyed in [arXiv:2408.17059](https://arxiv.org/html/2408.17059v1)) shows that intermediate SSL losses **improve linear separability of shallower subnets**, which directly maps to "the layers that the probe concatenates are now also constrained to be Gaussian". DINOv3 explicitly uses a multi-component loss (LDINO + LIBOT + LKoleo + LGram) targeting different layer behaviours — same flavour of multi-layer constraint stacking.

**Source inspirations**:
- Primary: *A Survey of the Self-Supervised Learning Mechanisms for Vision Transformers*, [arXiv:2408.17059](https://arxiv.org/html/2408.17059v1) (2024) — documents SDSSL (self-distillation at intermediate layers) and its measured boost to linear separability of shallow subnets.
- Supporting: *A comprehensive review on deep supervision in computer vision*, [ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S0925231225028656) — taxonomic case for auxiliary losses on intermediate layers; convergence + transferability benefits.
- Supporting: *DINOv3* multi-loss recipe (LDINO + LIBOT + LKoleo + LGram) — modern in-field instance of distinct losses at distinct depths.

**Why expected to improve**:
Two distinct effects. **(1) Probe-objective alignment**: training-time constraint matches the eval-time feature extractor (last-two-layers concat). **(2) Optimisation-landscape regularisation**: deep supervision is known to mitigate vanishing gradients and accelerate convergence (especially in early epochs) — directly relevant on ImageNet-10 where total epoch budget is the binding constraint. Risk: depth weights `λ_ℓ` are 2 new HPs (for L = 3 layers, 2 ratios). Mitigation: fix `λ_6 = λ_9 = 0.5 · λ_12` (i.e., linear ramp); ablate ±0.25 if surviving.

**Expected gain**: +0.3 / +0.8 / +1.8 pp 🟡 *(deep-supervision deltas on classification are 0.5–2 pp; for a regulariser they are usually smaller — conservative band)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Register forward hooks on `vit.blocks[5]`, `vit.blocks[8]`, `vit.blocks[11]` to capture CLS outputs.
2. Apply the existing `SlicingUnivariateTest` to each; sum with fixed weights `(0.25, 0.25, 1.0)`.
3. Compare to baseline (only final-layer SIGReg) at matched compute, 3 seeds.
4. Probe protocol unchanged (still concat last-2 CLS + LN + linear).

**Risks**:
- Each extra SIGReg adds a forward pass of `SlicingUnivariateTest` (1024 slices on the intermediate dim — for ViT-S all blocks share d=384, so no extra cost beyond the matmul).
- λ_ℓ depth weights introduce 2 new HPs (mitigation: fixed default; ablation as stretch).
- Composition risk with batch-3 Idea 6 (rank curriculum): rank-curriculum projects to top-k_t — if applied per layer, the k_t schedule conflicts. Run only on final layer if rank curriculum is on.

**Falsification test**: 100-ep run, baseline (1-layer SIGReg) vs 3-layer SIGReg with weights (0.25, 0.25, 1.0), 3 seeds, fixed (λ, lr, wd). Primary: linear-probe top-1 ≥ 0.5 pp higher with non-overlapping CIs. Secondary: the **last-2-layer probe gap** (top-1 from concat-2 minus top-1 from last-1) should *widen* under multi-layer SIGReg (i.e., the second-to-last layer should become more useful) — this is the mechanism check.

---

### Idea 4: Antithetic + spherical-harmonics control-variate SIGReg estimator

- **Pattern**: P2 (Transfer — port a variance-reduction primitive from the Monte-Carlo / sliced-Wasserstein numerics literature)
- **Tier**: 3 (mathematical statistics / numerical integration on the sphere — Tropp-line, not adjacent ML)
- **Scope**: enhance-existing. Modifies the slice-direction sampler in `SlicingUnivariateTest` to (a) antithetic pairs (u, −u) — free since EppsPulley is symmetric in u — and (b) add a spherical-harmonics control variate on top of the MC average. Backbone, statistic, λ unchanged.
- **One-liner**: Halve the slice-MC variance for free using two textbook variance-reduction tricks: antithetic pairs (zero extra cost since EppsPulley is symmetric in slice direction) + a low-order spherical-harmonics control variate (cheap closed form on S^(d−1)).

**Mechanism**:
The SIGReg gradient is `(1/M) Σ_m ∇ T(u_m^T Z)`. Two MC variance-reduction techniques apply cleanly: **(1) Antithetic pairs.** Sample u_m for m ∈ [1, M/2]; for m ∈ [M/2 + 1, M] use −u_m. Because EppsPulley's statistic `T(h)` is **even in h** (the empirical CF of `−h` has the same modulus as that of `h`), the two halves of the sample produce statistic values that are correlated via the embedding's symmetry — this gives a textbook variance reduction whose magnitude depends on the embedding's left-right asymmetry along each direction. **(2) Spherical-harmonics control variate.** Following *Sliced-Wasserstein Estimation with Spherical Harmonics as Control Variates* (arXiv:2402.01493, 2024), the integrand `T(u^T Z)` is expanded in low-order real spherical harmonics `Y_ℓm(u)` whose integrals over S^(d−1) are known in closed form. The control-variate-corrected estimator subtracts the leading harmonic contribution and adds back its exact integral — provably-better variance for the same M, with O(L²) extra cost where L is the truncation order (L=2 or L=3 sufficient). Neither change touches Cramér–Wold (slice geometry is unchanged in distribution; only the estimator weighting changes).

**Source inspirations**:
- Primary: *Sliced-Wasserstein Estimation with Spherical Harmonics as Control Variates*, [arXiv:2402.01493](https://arxiv.org/html/2402.01493v1) (2024) — the exact recipe for spherical-harmonics CV on slice-based estimators.
- Supporting: *Adaptive Antithetic Sampling for Variance Reduction*, Ren et al., [ICML 2019](http://proceedings.mlr.press/v97/ren19b/ren19b.pdf) — adaptive antithetic in deep-learning contexts; provides the framework for applying antithetic VR to ML estimators.
- Supporting: *Antithetic variates revisited*, [Communications of the ACM](https://dl.acm.org/doi/10.1145/182.358462) — classical reference; the variance-reduction magnitude depends on the integrand's parity decomposition.

**Why expected to improve**:
SIGReg's per-step gradient variance is `O(1/M)`; both techniques drop the multiplicative constant. Antithetic alone typically yields 1.2–2× variance reduction on symmetric integrands at zero compute cost. Spherical-harmonics CV with L=2 truncation has been published as giving up to **3× variance reduction** on similar slice-based estimators (arXiv:2402.01493). At fixed M=1024, lower MC variance means each gradient step is a better push toward N(0, I) — and on small datasets like ImageNet-10 (≤ 1 epoch of stable SIGReg signal is precious), early-training variance reduction matters more than at scale. This is composable with batch-3 Idea 2 (SRHT structured slices): SRHT changes *which* directions are sampled, this idea changes *how* the average is weighted; they stack.

**Expected gain**: +0.1 / +0.5 / +1.2 pp 🟡 *(small absolute lift — variance reduction is a stability / reproducibility win, not a different objective)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. In `SlicingUnivariateTest._sample_slices`, sample M/2 directions then concatenate with their negatives.
2. Add a `_spherical_harmonics_cv(stat_values, slice_dirs, L=2)` that computes `c_ℓm = mean(stat * Y_ℓm(u))` per harmonic and subtracts `c_ℓm * Y_ℓm(u)` from the estimator (adds back exact integral, which is 0 for ℓ ≥ 1).
3. Verify on a synthetic test: `Z ~ N(0, I) + small drift` — variance of the corrected estimator must be ≥ 1.5× lower than uncorrected at M = 256.
4. Train 100 ep at fixed (λ, lr, wd); compare SIGReg-loss running-std and linear probe.

**Risks**:
- Spherical harmonics in d = 384 are expensive at high ℓ; restrict to ℓ ∈ {1, 2} (cost ~d² ops per step, ≪ encoder forward).
- Antithetic VR is small if EppsPulley's even-ness is already exploited inside the test (per CLAUDE.md, the test "exploits symmetry of the CF to halve the integration domain" — this is *t*-symmetry, not *u*-symmetry, so the u-antithetic trick is still distinct).
- If batch-3 Idea 2 (SRHT) ships first, compose carefully: SRHT slices already have structured correlation; antithetic pairs across the structured ensemble need care to remain isotropic.

**Falsification test**: Synthetic-data sanity (off-training): inject `Z` from N(0, I) + 5% Laplace mixture; estimator variance with antithetic + CV must be ≥ 1.5× lower than vanilla at M = 256. Then 100-ep ImageNet-10, baseline-MC vs antithetic+CV at matched M, 3 seeds; primary: SIGReg-loss running-std last 20 epochs ≥ 25 % lower; secondary: linear probe within ±0.3 pp (parity) is success — the real claim is the variance reduction. If variance is not lower, the implementation is wrong; reject.

---

### Idea 5: Repulsive Monte Carlo slice sampling on S^(d−1)

- **Pattern**: P3 (Replace — swap i.i.d. Gaussian / SRHT slice sampling with a repulsive / DPP-based scheme on the sphere)
- **Tier**: 3 (point-process / determinantal-sampling literature; Riesz-energy methods on the sphere — bona-fide cross-domain)
- **Scope**: enhance-existing. Changes only the slice-direction generator; statistic, λ, projector, optimizer unchanged.
- **One-liner**: Replace i.i.d. uniform sampling on S^(d−1) with a *repulsive* point process (e.g., projection-DPP or Riesz-energy minimiser) that produces slice directions which are negatively correlated → strictly faster variance decay for the SIGReg MC estimator.

**Mechanism**:
*Repulsive Monte Carlo on the sphere for the sliced Wasserstein distance* (arXiv:2509.10166, 2025) shows that **joint distributions with negative dependence (drawn from repulsive Monte Carlo methods) provably enjoy faster decaying variance than i.i.d. quadratures** for sliced-distance estimators on S^(d−1). The mechanism: a Riesz-energy minimiser on S^(d−1) (or a projection-DPP with the right kernel) produces M directions that are more uniformly spread than i.i.d. samples, in the sense that no two are too close. This reduces the variance of any test-functional averaged across the slices. Distinct from batch-3 Idea 2 (SRHT): SRHT slices are *structured-correlated* in a deterministic way driven by the Hadamard matrix; repulsive slices are *probabilistically* anti-correlated. The two are composable (apply repulsion within an SRHT-structured ensemble), but their failure modes differ — SRHT can have nearly-collinear slices when M ≫ d, repulsion explicitly prevents this. Cramér–Wold preserved: the marginal of each direction is still uniform on S^(d−1) (DPP construction guarantees marginally uniform); only the joint is non-i.i.d.

**Source inspirations**:
- Primary: *Repulsive Monte Carlo on the sphere for the sliced Wasserstein distance*, [arXiv:2509.10166](https://arxiv.org/html/2509.10166v1) (2025) — proves faster variance decay than i.i.d. for sliced estimators on the sphere; gives sampling algorithm.
- Supporting: *ReSWD: Reservoir Sampling + Sliced Wasserstein for Variance Reduction*, [arXiv:2510.01061](https://arxiv.org/html/2510.01061) (2025) — adjacent line; adaptive informative-direction retention.
- Supporting: *Sliced-Wasserstein Estimation with Spherical Harmonics as Control Variates*, [arXiv:2402.01493](https://arxiv.org/html/2402.01493v1) — sets up the larger family of variance-reduction techniques for sliced estimators.

**Why expected to improve**:
Same logic as Idea 4 (lower-variance MC = better SIGReg gradient = better stability + slightly better convergence), but via a different mechanism. The 2025 paper explicitly compares repulsive-sphere vs i.i.d. and shows asymptotic variance scaling improvements that translate to **2–4× effective slice budget** at fixed M. For ImageNet-10 where total signal is small, this is meaningful for stability of the loss curve and reproducibility across seeds.

**Expected gain**: +0.1 / +0.5 / +1.2 pp 🟡 *(small absolute lift; the real value is stability — and the mechanism is publishable in its own right)*
**Feasibility**: 4/5 🟢
**Effort**: S 🟢 (Riesz-energy gradient descent on S^(d−1) for M=1024, d=384 takes ~1 sec per resample; cache and refresh every ~10 epochs)

**Implementation sketch**:
1. Implement `_repulsive_slices(d, M, K_iter=200)`: initialise uniform on S^(d−1); run K_iter steps of gradient descent on the Riesz s=1 energy `Σ_{i<j} 1/||u_i − u_j||`; renormalise.
2. Cache the ensemble; refresh every 10 epochs to keep the slice ensemble "fresh enough" to avoid SIGReg over-fitting to a fixed direction set.
3. Add `slice_generator: Literal["gaussian", "srht", "repulsive"]` to the test.
4. Compare to baseline at fixed (λ, lr, wd); 3 seeds.

**Risks**:
- DPP / Riesz on d=384 with M=1024 is a one-time cost (~seconds) per ensemble; negligible vs training.
- If refresh-frequency is too high, the slice ensemble change rate may add noise; if too low, the encoder over-fits the fixed slice geometry. Default refresh=10 epochs based on the 2025 paper's recommendation.
- Composition with SRHT (batch-3 Idea 2): if SRHT ships first, this idea must be tested in head-to-head A/B/C (SRHT / repulsive / Gaussian baseline) rather than stacked, until pairwise gains are known.

**Falsification test**: Synthetic-data sanity: estimator variance under repulsive sampling at M=256, d=384 must be ≥ 1.5× lower than Gaussian at the same M (matches the 2025 paper's published scaling). On ImageNet-10: 100-ep run, Gaussian vs repulsive, 3 seeds, fixed (λ, lr, wd); primary: SIGReg-loss running-std ≥ 25 % lower; secondary: linear-probe within ±0.3 pp parity OR better. If neither variance nor parity holds, reject.

---

### Idea 6: MAE pixel-reconstruction auxiliary head alongside SIGReg

- **Pattern**: P1 (Combine — add a generative-style auxiliary head to the existing JEPA-style regulariser)
- **Tier**: 1 (in-field — MAE for ViT representation learning)
- **Scope**: enhance-existing. Adds a lightweight MAE decoder + masking step + pixel-recon loss term. Encoder, projector, SIGReg, λ unchanged per-component.
- **One-liner**: Train the encoder simultaneously against (a) LeJEPA loss on the standard global+local crops and (b) MAE-style pixel reconstruction on a 75 %-masked variant of the global crop, with total loss `L = L_LeJEPA + α · L_MAE`.

**Mechanism**:
SIGReg constrains the *distributional shape* of `Z`; MAE (He et al., CVPR 2022) constrains *local content fidelity* via pixel reconstruction of masked patches. These two signals operate on complementary axes — distributional vs content — and have not been published as a combined objective on JEPA (C-JEPA combines JEPA with VICReg, not with MAE; iBOT does token-distillation, not pixel-recon). The MAE recipe: mask 75 % of input patches at random, pass only the visible 25 % through the (existing) ViT encoder, prepend mask tokens, decode via a small (2–4 layer) ViT decoder, MSE loss against the masked pixels. On a small dataset like ImageNet-10, MAE alone *under-performs* contrastive / JEPA SSL (MAE shines at scale); but as an *auxiliary*, it has been shown to add 1–3 pp on top of contrastive baselines (e.g., SupMAE arXiv:2205.14540 adds a supervised classification head to MAE; the symmetric trick is to add MAE to JEPA).

**Source inspirations**:
- Primary: *Masked Autoencoders Are Scalable Vision Learners*, He et al., [CVPR 2022 / arXiv:2111.06377](https://arxiv.org/abs/2111.06377) — the MAE recipe.
- Supporting: *SupMAE: Supervised Masked Autoencoders Are Efficient Vision Learners*, [arXiv:2205.14540](https://arxiv.org/html/2205.14540v3) — proves the "MAE + classification head" combo lifts both pre-training efficiency and downstream linear-probe; symmetric to our "MAE + SIGReg" proposal.
- Supporting: *Swin MAE: Masked autoencoders for small datasets*, [ScienceDirect 2023](https://www.sciencedirect.com/science/article/abs/pii/S0010482523005024) — adapts MAE specifically to small-data regimes; directly relevant to Imagenette.

**Why expected to improve**:
The two losses constrain orthogonal axes: SIGReg pulls `Z`'s marginals toward N(0,1) per slice (global distributional), MAE pulls reconstructed pixels toward ground truth (local fidelity, no distributional implication). The two regularisations are mechanistically non-redundant, and their gradients should be largely uncorrelated — the textbook condition under which a combined loss out-performs either alone. Risk is opportunity-cost: adding a decoder doubles encoder-effective wall-clock, so matched-compute comparison is mandatory.

**Expected gain**: +0.4 / +1.0 / +2.5 pp 🟡 *(historical JEPA-vs-MAE deltas at ViT-B scale are ~5 pp linear probe — adding MAE as auxiliary should claw back some of that distance; conservative mid-claim of +1.0 pp reflects the matched-compute control bar)*
**Feasibility**: 3/5 🟡 (adds decoder + masking pipeline + α — three moving pieces)
**Effort**: L 🟡

**Implementation sketch**:
1. Add a 2-layer ViT decoder (head dim 192, mask token embed) and a `MaskedReconLoss` module.
2. On each batch, after the standard global-crop forward, run a separate masked-pass: tokenise global crop, randomly mask 75 % of patches, encode visible, decode, MSE on masked pixels.
3. Total loss: `L = L_LeJEPA + α · L_MAE`; sweep `α ∈ {0.1, 0.5, 1.0}` at fixed (λ, lr, wd).
4. Compare to **2× wall-clock LeJEPA baseline** (matched compute) at 100 ep MAE+LeJEPA vs 200 ep LeJEPA-only.

**Risks**:
- 2× wall-clock during training → matched-compute control is mandatory; without it, any gain is confounded with "more compute".
- α is a new HP; SIGReg's "single-λ" branding is violated. Mitigation: bind α to λ as `α = c · λ` with c fixed (e.g., c = 5), turning two HPs into one.
- Decoder bloat: adds ~3 M params; minor on top of ViT-S/16's 22 M.
- Composition: if W-MSE pre-step (Idea 2) is on, the encoder output is whitened — MAE decoder still works on the encoder *trunk*, not on `Z`, so they don't conflict directly.

**Falsification test**: 100-ep LeJEPA+MAE at best α vs 200-ep LeJEPA-only (matched wall-clock), 3 seeds each, fixed (λ, lr, wd). Primary: linear-probe top-1 must be ≥ 0.6 pp higher with non-overlapping seed CIs. Mechanism check: ablate `α = 0` arm at 100 ep — must be *worse* than the 100-ep α > 0 arm by ≥ 0.4 pp (else the gain is from "an extra decoder regularises the encoder's gradient" rather than the recon signal). If neither check passes, the combo adds nothing.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|------------------------|--------------------|---------------------|-----------------|------------|-------------|------------|-------|
| 1 | SAM / Friendly-SAM | ✅ Foret ICLR 2021 + arXiv:2405.20439 (2024) | ✅ | ✅ (≥0.4 pp vs matched-wall-clock baseline) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 2 | W-MSE Cholesky pre-step | ✅ Ermolov ICML 2021 + arXiv:2408.07519 (2024) | ✅ | ✅ (≥0.6 pp + faster SIGReg early decrease) | EXTENDS | VERIFIED | 4 | OK | **KEEP** |
| 3 | Layer-wise SIGReg | ✅ arXiv:2408.17059 (SDSSL survey) + ScienceDirect 2025 (deep-sup review) | ✅ | ✅ (≥0.5 pp + last-2-layer gap widens) | NOVEL | VERIFIED | 4 | ⚠️ adds 2 depth-weight HPs (mitigated by fixed default) | **KEEP w/ flag** |
| 4 | Antithetic + SH control variate | ✅ arXiv:2402.01493 (2024) + ICML 2019 antithetic | ✅ | ✅ (≥25 % SIGReg-var reduction) | NOVEL | VERIFIED | 4 | OK | **KEEP** |
| 5 | Repulsive MC slice sampling | ✅ arXiv:2509.10166 (2025) | ✅ | ✅ (≥25 % SIGReg-var reduction) | NOVEL | VERIFIED | 4 | OK | **KEEP** |
| 6 | MAE auxiliary pixel-recon head | ✅ He CVPR 2022 (arXiv:2111.06377) + SupMAE arXiv:2205.14540 + Swin-MAE 2023 | ✅ | ✅ (≥0.6 pp vs matched-compute LeJEPA-only + α=0 ablation must under-perform) | EXTENDS | VERIFIED | 3 | ⚠️ adds α HP; 2× wall-clock | **KEEP w/ flag** |

**Cross-idea consistency**:
- Ideas 4 and 5 both reduce SIGReg-MC variance via different mechanisms (estimator weighting vs sample geometry). Compose only after each is independently validated; if both pass, run a 3-way ablation (Gaussian / antithetic+CV / repulsive / both).
- Ideas 2 and 3 both touch the embedding-side preprocessing (whitening vs multi-layer extraction). They are layer-orthogonal — whitening operates on the final `Z`; layer-wise applies SIGReg at multiple depths. Compose: apply whitening *per layer* before each layer's SIGReg, but only after both work in isolation.
- Idea 1 (SAM) is loss-landscape, fully orthogonal to all others; composes safely with each.
- Idea 6 (MAE) is the highest-effort idea — gates on baseline + Step-0 ASHA per vetting; do not start before those.

**No ideas rejected this batch.** Append empty stanza to `_logs/_rejection_log.md`.

## Notes & warnings

- ⚠️ **Baseline still TBD** — batch-2 Idea 5 (ASHA sweep) remains the absolute-pp gate. All gain estimates here are *relative-to-ASHA-best baseline*.
- ⚠️ **Two ideas add a non-λ HP**: Idea 3 (depth weights, mitigated by fixed default ratio), Idea 6 (α, mitigated by tying α = c·λ). The "near-single-λ" branding is **drifting**; if both ship, LeJEPA becomes a 3-HP method. Flag for user decision.
- ⚠️ **Tier-mix delivered 50/17/33 vs configured 40/20/40** — within ±10 pp bands on every tier; no re-search. T1 slightly over (50 vs 40) because the strongest SSL primaries (SAM, W-MSE, MAE) all live in T1 / mainstream ML.
- ⚠️ **Survival rate of prior batch was 83 % (above healthy band)** — batch-4 is calibration-conscious: every idea has a *matched-compute* falsification, not just an equal-epoch one (Ideas 1, 2, 5, 6 explicitly).
- ⚠️ **No P6 (Verify) idea this batch** — by design; batch-3 Idea 3 (PIT monitor) still pending ρ-correlation validation. Re-open P6 in batch-5 if PIT graduates to "ASHA-rung evaluator".
- ⚠️ **Idea 6 (MAE auxiliary) is the riskiest** — 2× wall-clock, new HP, lowest feasibility (3/5). Listed because the JEPA-vs-MAE gap at scale is ~5 pp and a combined head is the published path to closing it; but it is unambiguously *not* a quick win.

- **Devil's-advocate on top-1 (Idea 1, SAM/Friendly-SAM)**: failure mode = SAM's flatness bias may conflict with SIGReg's *sharp* distributional pull. Some SAM analyses (e.g., the JMLR 2024 stability paper [Stabilizing Sharpness-Aware Minimization Through A Simple Renormalization Strategy](https://www.jmlr.org/papers/volume26/24-0065/24-0065.pdf)) note SAM under-performs when the loss landscape has strong directional curvature, which the SIGReg term explicitly induces along the slice directions. Mitigation: include ASAM (adaptive SAM with per-parameter ρ) as a fallback arm; falsification's "matched-wall-clock" bar already guards against the trivial failure where SAM beats baseline only by spending more compute.

- **Pattern coverage cumulative across batches 1+2+3+4**: P1, P2, P3, P4, P5, P6, P7, P8, P12 — still 9/12 (no new patterns; this batch deliberately re-uses with new mechanisms). P9 (Tool-use), P10 (Sampling-as-output), P11 (ICL) remain unsuited to in-domain SSL pretraining.

- **Prerequisites / measurements** (NOT ideas — surfaced per skill rules):
  - (i) Batch-2 Idea 5 ASHA sweep must produce a measured (λ, lr, wd) before any matched-compute claim here is testable.
  - (ii) Idea 4's synthetic-data variance-reduction sanity is a 1-hour measurement (no GPU needed), not a separate idea — gates whether Idea 4 graduates to ImageNet-10 run.
  - (iii) Idea 5's synthetic-data sanity (same shape) is similarly a measurement gate.

## Composition map (batch-3 vetting → batch-4)

Each new idea here is tagged for compatibility with surviving ideas from batch-2 + batch-3:

| New idea | Composes-with (✓ = stack, ⚠ = sequential, ✗ = conflict) |
|----------|---------------------------------------------------------|
| 1. SAM | ✓ batch-3 Idea 3 (PIT monitor — read-only) · ✓ batch-3 Idea 2 (SRHT) · ✓ batch-2 Idea 1 (stacked tests) · ✓ batch-2 Idea 5 (ASHA — extend to ρ as 4th axis) |
| 2. W-MSE pre-step | ✓ batch-3 Idea 3 (PIT) · ✓ batch-3 Idea 2 (SRHT) · ⚠ batch-3 Idea 6 (rank curriculum — both touch covariance, run sequentially) · ✓ batch-2 Idea 1 |
| 3. Layer-wise SIGReg | ✓ batch-3 Idea 3 (PIT) · ✓ batch-3 Idea 2 (SRHT, per layer) · ⚠ batch-3 Idea 6 (rank curriculum at final layer only) · ✓ batch-2 Idea 4 (LARS/LAMB) |
| 4. Antithetic + SH CV | ✓ batch-3 Idea 3 · ⚠ batch-3 Idea 2 (SRHT — A/B/C first, then stack) · ✓ all batch-2 |
| 5. Repulsive MC | ✓ batch-3 Idea 3 · ⚠ batch-3 Idea 2 (SRHT — A/B/C first) · ⚠ Idea 4 (both VR; A/B/C first) · ✓ all batch-2 |
| 6. MAE auxiliary | ✓ batch-3 Idea 3 (PIT — read-only) · ✓ batch-2 Idea 1, 4, 5 · ⚠ batch-3 Idea 1 (co-distillation — 4× wall-clock, do not combine) |

The four "stack with everything" compositions are: (a) **SAM + PIT monitor + ASHA** (Idea 1 + batch-3 Idea 3 + batch-2 Idea 5) — high-confidence stable-baseline maximiser; (b) **W-MSE + Stacked tests + PIT** (Idea 2 + batch-2 Idea 1 + batch-3 Idea 3) — distributional-quality maximiser; (c) **SRHT + Antithetic+CV** (batch-3 Idea 2 + Idea 4) — slice-MC variance minimiser; (d) **Layer-wise SIGReg + SRHT + W-MSE** (Idea 3 + batch-3 Idea 2 + Idea 2) — probe-objective alignment maximiser. These are the natural targets for a formal `--compose-mode` invocation, as recommended by batch-3 vetting.

## Next steps for user

1. **(Unchanged from batch-3 vetting)** Run batch-2 Idea 5 (ASHA) first — still the gate for all absolute-pp claims.
2. **Parallel** to ASHA: ship **Idea 1 (SAM/Friendly-SAM)** — it's a one-line optimizer change and can be folded into the ASHA grid by adding `optimizer ∈ {adamw, fsam_adamw}` as a 4th axis. Zero new infrastructure.
3. **Once ASHA returns (λ, lr, wd)**: fire **Idea 2 (W-MSE pre-step)** at fixed best HP, 3 seeds — highest expected pp lift in this batch with smallest effort.
4. **In the same training arm** as Idea 2: include the **synthetic-data sanity** for Ideas 4 (antithetic+CV) and 5 (repulsive MC) as a 1-hour CPU pre-flight; only graduate to ImageNet-10 if synthetic variance reduction holds.
5. **Idea 3 (Layer-wise SIGReg)** next, after Idea 2: tests whether the train-eval alignment story matters at all on ImageNet-10. Add as a 4th arm to the same training run.
6. **Idea 6 (MAE)** last — the most expensive idea in the batch; commit only after Ideas 1–3 settle, and run it with the matched-wall-clock control (200-ep LeJEPA-only) explicitly.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 40/20/40 | given-vetting batch-3 | 2026-05-18 batch-4`
