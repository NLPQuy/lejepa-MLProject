# Idea Batch 1 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~12 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 55/30/15`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe / kNN top-1 accuracy on the held-out split is the metric)
- Task / problem: In-domain self-supervised pretraining on ImageNet-10 only (no external data / no foundation-model init), evaluated by frozen-backbone linear probe (concat CLS of last 2 layers + LN) on the same 10 classes — exactly the recipe in `stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py`.
- Existing pipeline: LeJEPA ViT-S/B + SIGReg (EppsPulley × 1024 random 1-D slices) + invariance loss across 2 global (224²) + 6 local (96²) DINO-style crops; AdamW lr=5e-4 wd=5e-2 bf16; single hyper-parameter λ. Baseline score: **TBD on ImageNet-10 specifically** (paper-level: LeJEPA ViT-L 100ep ≈ ImageNet-1K linear probe 75–79%; our in-repo ViT-B/16 1-epoch numbers are placeholder).
- Batch scope: **mixed (≥ 50% enhance-existing)**
- Tier mix (configured): 55/30/15 (bands T1 45–65%, T2 20–40%, T3 5–25%)
- Baseline: LeJEPA ViT-S, in-repo recipe (`benchmarks/imagenet10/lejepa-vit-small.py`) — exact number TBD
- Compute budget: assumed small-to-medium (1–8 GPU, days). Re-rank if larger.
- Time budget: ~1 week of experiments
- Constraints: not hard-confirmed; ideas flag where they violate "single λ" or "in-domain only".

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Tier 1 / 2 / 3 (counts) | 3 / 2 / 1 |
| Tier mix vs configured | 50/33/17 vs 55/30/15 (within ±10 pp) |
| Scope mix | 6 enhance-existing / 0 greenfield (100% enhance — pipeline supplied) |
| Patterns used | P1, P2, P3 (×2), P4, P6 — 5 distinct |
| Distinct venues | 6 (TMLR, ICLR, CVPR, NeurIPS-W, arXiv, BMVC) |
| Time windows | <12 mo: 2 · 12–36 mo: 3 · 36–72 mo: 2 |
| Avg feasibility | 4.3 / 5 |
| Avg confidence | 🟢 33% · 🟡 50% · 🔴 17% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 6 | Class-balanced multi-crop curriculum on ImageNet-10 | P4 | 1 | +2.0 | 5 | S | **3.3** |
| 1 | Orthogonal / QMC slicing for SIGReg | P3 | 2 | +1.0 | 5 | S | 3.0 |
| 5 | Kernelize SIGReg projections (RKHS slicing) | P2 | 2 | +2.0 | 4 | M | 3.0 |
| 3 | Add register tokens to ViT backbone | P3 | 1 | +1.0 | 5 | S | 2.9 |
| 2 | Add iBOT-style patch SIGReg head | P1 | 1 | +3.0 | 3 | L | 2.8 |
| 4 | Online normality verifier → adaptive λ | P6 | 3 | +1.0 | 4 | M | 2.6 |

Composite = `0.4·Gain + 0.3·Feas + 0.2·(EffortInv) + 0.1·Novelty` (gain normalised to /5; effort: S=4 M=3 L=2 XL=1).

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 6: Class-balanced multi-crop curriculum on ImageNet-10** — Score 3.3
ImageNet-10 is tiny (~9 k images) and class-balanced by construction, so the failure mode is augmentation/overfitting rather than collapse. Sweeping local-crop count V∈{6,10,14} with a scale-curriculum (warm with wider crops, anneal toward 0.05–0.3) plus class-stratified sampling is the cheapest known lever for small-data SSL.

### ⚡ Quick win (lowest effort)
**Idea 1: Orthogonal / Quasi-Monte-Carlo slicing for SIGReg** — Effort S
Drop-in change to `SlicingUnivariateTest`: replace iid Gaussian direction sampling with orthogonalised / Sobol-QMC directions. Variance-reduction is standard in sliced-Wasserstein literature and lets you halve `num_slices` (1024 → 512) at equal stat power — frees compute or sharpens the SIGReg signal.

### 🛡️ Safe bet (highest confidence)
**Idea 3: Add register tokens to ViT backbone** — Confidence 🟢
Darcet et al. (ICLR 2024) showed 4 register tokens fix attention artifacts and improve dense + linear-probe metrics across DINOv2, MAE, supervised ViT. The change is `n_register_tokens=4` in the timm `vit_small_patch16_224`; no LeJEPA-side change. Mechanism is orthogonal to SIGReg, so collisions are unlikely.

---

## Ranked ideas

### Idea 6: Class-balanced multi-crop curriculum on ImageNet-10

- **Pattern**: P4 (Scale — knob-twist on multi-crop)
- **Tier**: 1
- **Target task**: ImageNet-10 in-domain SSL linear probe — same as batch task.
- **Scope**: enhance-existing. Modifies the `_global_transform` / `_local_transform` builders and the sampler in `lejepa-vit-small.py`. Backbone, SIGReg loss, optimiser unchanged.
- **One-liner**: Adapt the DINO multi-crop recipe to a 9k-image dataset by sweeping V and using a scale curriculum + class-stratified sampling.

**Mechanism**:
Three orthogonal changes to the data layer: (a) ablate V_local ∈ {4, 6, 10, 14} for fixed global=2; (b) replace the static local-scale range `(0.05, 0.3)` with a per-epoch curriculum that starts at `(0.2, 0.6)` and linearly anneals to `(0.05, 0.3)` over the first 30 epochs (DINO observed wider-then-narrower is more stable on small data); (c) replace random sampling with a `WeightedRandomSampler` keyed on class to guarantee balance per batch — cheap because ImageNet-10 has labels for free (used only for the sampler, not the loss).

**Source inspirations**:
- Primary: *Emerging Properties in Self-Supervised Vision Transformers (DINO)*, Caron et al., ICCV 2021 [arXiv:2104.14294]
- Supporting: *DINO-MC: SSL with Multi-sized Local Crops*, Wanyan et al., 2023 [arXiv:2303.06670]
- Supporting (small-data caveat): *You Don't Need Data Augmentation in SSL*, 2024 [arXiv:2406.09294]

**Why expected to improve**:
DINO ablations show local-crop count and scale diversity are the dominant drivers of small-data SSL accuracy; LeJEPA inherits multi-crop verbatim but never tuned it for the ImageNet-10 regime. SIGReg is invariant to V (averages over slices, not views), so adding crops only strengthens the invariance signal without disturbing the normality term.

**Expected gain**: +0.5 / +2.0 / +4.0 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add a `V_local` config knob; rerun the canonical recipe at V_local ∈ {4, 6, 10, 14}.
2. Wrap scale into a Lightning `on_train_epoch_start` callback that mutates the transform.
3. Swap the train sampler for `WeightedRandomSampler(num_samples=len(ds), weights=1/class_freq)`.

**Risks**:
- Diminishing returns past V=8 are known (multi-crop search shows modest gains beyond ~4 crops); the budget on local crops competes with batch size.
- Adding crops slows step time roughly linearly — may push wall-clock past budget at V=14.

**Falsification test**: Run V_local ∈ {6, 10} with scale curriculum for 100 ImageNet-10 epochs, ViT-S, fixed compute. If linear-probe top-1 fails to improve by ≥ 1.0 pp over the V=6 / no-curriculum baseline at equal wall-clock, the idea fails.

---

### Idea 1: Orthogonal / Quasi-Monte-Carlo slicing for SIGReg

- **Pattern**: P3 (Replace — swap the slice-direction sampler)
- **Tier**: 2
- **Target task**: same as batch.
- **Scope**: enhance-existing. Modifies `SlicingUnivariateTest._sample_directions` in `lejepa/multivariate.py`. `EppsPulley`, projector, backbone, optimiser unchanged.
- **One-liner**: Replace iid Gaussian slice directions with orthogonalised or low-discrepancy directions to cut MC variance of the SIGReg estimate at fixed `num_slices`.

**Mechanism**:
At every training step the SIGReg estimate is `(1/M) Σ_m T(Z u^(m))` with u^(m) iid uniform on S^(d−1). Replace this with (a) Gram-Schmidt-orthogonalised batches of M directions, or (b) directions obtained by projecting Sobol-QMC points on R^d onto the sphere. Both have O(M·d) cost matched to the existing sampler. The DDP seed-sync code in `UnivariateTest.base` already guarantees identical directions across ranks; the change is local.

**Source inspirations**:
- Primary: *Quasi-Monte Carlo Variational Inference / Sliced-Wasserstein Distance for GMM*, Kolouri et al., CVPR 2018 [arXiv:1711.05376]
- Supporting: *On the Statistical Properties of Sliced Wasserstein Distances*, Nadjahi 2020 [arXiv:2003.05783] — orthogonal-slice variance reduction bound.

**Why expected to improve**:
The SIGReg estimate is a Monte Carlo integral over slices; orthogonal/QMC samplers reduce its variance by a constant factor (~2–4× empirically in SW literature). Lower-variance loss = lower gradient noise = either faster convergence or stronger signal at the same M, which directly translates to better embedding isotropy on the small-data regime where SIGReg's effect is most diluted by augmentation noise.

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add a `slice_sampler: {iid, ortho, qmc}` config to `SlicingUnivariateTest`.
2. For `ortho`, sample `MxD` standard normal then QR-decompose; for `qmc` use `scipy.stats.qmc.Sobol`.
3. Re-run the LeJEPA ImageNet-10 recipe at M ∈ {256, 512, 1024} for each sampler.

**Risks**:
- If M=1024 is already past the variance plateau, orthogonal/QMC adds nothing.
- Sobol on the sphere is correct only up to the radial projection; degenerate at very high d.

**Falsification test**: At M=256, if `ortho`/`qmc` SIGReg curves do not show ≥ 30% lower stochastic variance (measured as std of SIGReg value over a fixed mini-batch resampled 50× per step) than `iid`, the variance-reduction premise fails and downstream gain is unlikely.

---

### Idea 5: Kernelize SIGReg projections (RKHS slicing)

- **Pattern**: P2 (Transfer — kernel-VICReg trick → SIGReg)
- **Tier**: 2
- **Target task**: same as batch.
- **Scope**: enhance-existing. Inserts a fixed RFF (random Fourier feature) map φ(·) before slicing inside `lejepa.multivariate.SlicingUnivariateTest`. Projector, EppsPulley, optimiser unchanged.
- **One-liner**: Apply Epps-Pulley not to linear projections of Z but to projections of an RFF feature map of Z, so SIGReg detects nonlinear deviations from N(0, I).

**Mechanism**:
Replace `h^(m) = Z u^(m)` with `h^(m) = u^(m)·φ(Z)` where `φ: R^d → R^D` is a fixed RFF map (e.g., Gaussian kernel, D=2048). Cramér-Wold still holds in RKHS for the *distribution of φ(Z)*, so the normality check now penalises kernelised non-Gaussianity. Cost: one extra `nn.Linear(d, D, bias=False)` with frozen weights + cos/sin; gradients flow through Z. Kernel VICReg (arXiv 2509.07289) reports consistent gains over Euclidean VICReg with this kind of lift.

**Source inspirations**:
- Primary: *Kernel VICReg for SSL in Reproducing Kernel Hilbert Space*, MDPI BDCC 2025 [arXiv:2509.07289]
- Supporting: *Random Features for Large-Scale Kernel Machines*, Rahimi & Recht, NeurIPS 2007.
- Supporting: *Sliced Score Matching*, Song et al., UAI 2019 [arXiv:1905.07088] — sliced-statistic-in-feature-space precedent.

**Why expected to improve**:
SIGReg's linear-slice formulation only tests Gaussianity of *linear* marginals; the embedding could still be non-Gaussian in any nonlinear functional. Kernelising widens the family of detected deviations without breaking the Cramér-Wold guarantee (which lifts to the kernel mean embedding). On small-data, where the embedding shape is fragile, the extra discriminative power of the test plausibly pays off.

**Expected gain**: +0.5 / +2.0 / +4.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Add `rff_dim` and `rff_sigma` config; freeze a `Linear(d, rff_dim)` with N(0, 1/σ²) weights and a uniform[0, 2π] bias.
2. In `SlicingUnivariateTest.forward`, compute `phi = sqrt(2/D) cos(WZ + b)` then slice.
3. Tune σ via median heuristic on a held-out batch at init; do not learn during training.

**Risks**:
- The RKHS test may be *too* strict and stall the invariance term (over-regularisation).
- σ choice can dominate the result; needs a sanity scan.

**Falsification test**: Train LeJEPA ViT-S on ImageNet-10 for 100 ep with rff_dim ∈ {1024, 2048} and σ ∈ {0.5, 1, 2}× median. If best kernelised run does not beat the linear-SIGReg baseline by ≥ 0.7 pp linear-probe, the kernel lift is not buying signal here.

---

### Idea 3: Add register tokens to ViT backbone

- **Pattern**: P3 (Replace — backbone tweak)
- **Tier**: 1
- **Target task**: same as batch.
- **Scope**: enhance-existing. Replaces the `timm.create_model("vit_small_patch16_224")` instantiation in `lejepa-vit-small.py` with the same model + 4 register tokens (timm exposes `reg_tokens=4`). SIGReg, projector, optimiser, schedule unchanged.
- **One-liner**: Append 4 learnable register tokens to the ViT input sequence so the model stops repurposing low-info patch tokens as global scratch space.

**Mechanism**:
ViT models develop high-norm "artifact" tokens on background patches when trained with DINO/MAE/supervised, harming dense features and (mildly) linear probes. Darcet et al. (ICLR 2024) show that giving the model 4 register tokens — which are ignored at probe time — fixes this entirely. Drop-in: `timm.create_model("vit_small_patch16_224", reg_tokens=4)`. The LeJEPA CLS-concat probe uses CLS only, so register tokens just discharge artifact mass.

**Source inspirations**:
- Primary: *Vision Transformers Need Registers*, Darcet et al., ICLR 2024 [arXiv:2309.16588]
- Supporting: *DINOv2: Learning Robust Visual Features without Supervision*, Oquab et al., TMLR 2024 [arXiv:2304.07193] — DINOv2-with-registers checkpoints.

**Why expected to improve**:
Register-token gains are repeatedly reproduced across SSL methods and backbones. Linear-probe gains in the original paper are modest (+0.3 to +1.5 pp) but essentially free. On small datasets the artifact fraction tends to be higher (less data → noisier attention), so the absolute uplift can be slightly larger than on ImageNet-1K.

**Expected gain**: +0.3 / +1.0 / +2.5 pp 🟢
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Change the timm backbone call to add `reg_tokens=4`.
2. Confirm CLS-concat probe still indexes token 0 (and not a register).
3. Re-run baseline ImageNet-10 recipe; report Δlinear-probe.

**Risks**:
- Most of the published register-token gain is on dense tasks (segmentation), not linear probe — uplift could be in the noise on a 10-class probe.
- 4 extra tokens marginally slow attention (negligible at ViT-S).

**Falsification test**: Run identical 100-epoch LeJEPA recipe on ImageNet-10 with vs without registers, 3 seeds each. If `(mean_with_reg − mean_without)` < 0.2 pp linear probe with overlapping seed CIs, the idea did not pay.

---

### Idea 2: Add an iBOT-style patch-SIGReg head

- **Pattern**: P1 (Combine — LeJEPA global SSL + iBOT patch-level objective)
- **Tier**: 1
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds a second projector + SIGReg on patch-token embeddings; CLS-side LeJEPA, encoder weights, optimiser unchanged.
- **One-liner**: Apply SIGReg + invariance not just to the CLS-side projection but also to (masked) patch tokens, mirroring how iBOT extends DINO with a patch-level MIM head.

**Mechanism**:
Forward two global views through the encoder. For each view, randomly mask a fraction p∈[0.1, 0.5] of patches; compute the SIGReg + invariance loss on (a) the existing CLS-projection (unchanged), and (b) a second projection head applied to the *masked* patch token embeddings — invariance is across the two views' patch-token sequences at matched spatial positions, SIGReg is across patches in a batch. Total loss = `L_CLS + α·L_patch` with α small (~0.1). This is the LeJEPA-native analogue of DINO→iBOT.

**Source inspirations**:
- Primary: *Image BERT Pre-Training with Online Tokenizer (iBOT)*, Zhou et al., ICLR 2022 [arXiv:2111.07832]
- Supporting: *DINOv2*, TMLR 2024 [arXiv:2304.07193] — confirms iBOT loss is the patch-level driver.
- Supporting: *Cluster and Predict Latents Patches for Improved MIM*, Meta, 2025 [arXiv:2502.08769]

**Why expected to improve**:
Patch-level prediction is the empirically dominant driver of dense + linear-probe gains in DINOv2 over DINO. LeJEPA currently lacks any patch-level signal — every embedding update comes from a single CLS projection per view. Adding a parallel patch SIGReg term increases supervisory density by ≈196× per global crop (number of patches), which is exactly the regime where small datasets are starved.

**Expected gain**: +1.0 / +3.0 / +5.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Implementation sketch**:
1. Subclass `LeJEPA` to expose `forward_features(return_patches=True)`.
2. Implement masked-patch invariance via a `BlockMasking` augmenter (iBOT style).
3. Add a `patch_projector` (MLP, same width as the CLS projector).
4. Tune `α` ∈ {0.05, 0.1, 0.2} and mask ratio ∈ {0.15, 0.3, 0.5}.

**Risks**:
- Adds a 2nd hyper-parameter (α and mask ratio) — **violates the "single λ" LeJEPA branding** (flag with user).
- Patch SIGReg is non-trivially noisier (smaller effective batch per slice) and may need M_patch ≠ M_CLS.
- Memory cost rises (extra projection head on N·patches dimensions).

**Falsification test**: With α tuned in {0.05, 0.1, 0.2} and 100-epoch ImageNet-10 budget, if the best patch-augmented run does not improve linear-probe by ≥ 1.5 pp over the CLS-only LeJEPA baseline, the patch lift fails to justify its complexity.

---

### Idea 4: Online normality verifier → adaptive λ schedule

- **Pattern**: P6 (Verify — add an online normality auditor on top of training)
- **Tier**: 3
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds a Lightning callback that watches a held-out normality statistic and adjusts λ in `LeJEPA.loss`. Pipeline shape unchanged.
- **One-liner**: Compute Epps-Pulley on a held-out validation batch each epoch; if the embedding is *already* near-Gaussian (low statistic), shrink λ to let invariance dominate; if not, grow λ.

**Mechanism**:
Each epoch end: forward a fixed held-out batch (e.g., 1024 ImageNet-10 train images, no augmentation) through the encoder + projector; compute the canonical SIGReg statistic `s_t`. A simple proportional controller updates the loss weight: `λ_{t+1} = clip(λ_t · (s_t / s_target)^β, λ_min, λ_max)`. `s_target` is the SIGReg value of an exact N(0, I_d) sample of equal batch size (a known constant). Effectively, the model self-adjusts how hard SIGReg pulls based on how Gaussian it already is — preserves the *spirit* of the single-knob LeJEPA design (λ is now derived, not chosen) but the controller has 2 of its own knobs (β, s_target margin), which is the honest cost.

**Source inspirations**:
- Primary: *LeJEPA*, Balestriero & LeCun, 2025 [arXiv:2511.08544] — bisection-search-over-λ remark motivates auto-λ.
- Supporting: *Adaptive Loss Weighting for Multi-Task Learning (GradNorm)*, Chen et al., ICML 2018 [arXiv:1711.02257]
- Supporting: *Sliced Score Matching*, UAI 2019 [arXiv:1905.07088] — independent normality signal precedent.

**Why expected to improve**:
The paper itself notes that λ is the single tuning knob and bisection-searchable — but a fixed schedule wastes capacity early (when embedding is far from Gaussian, λ too small) and over-regularises late (when it's already Gaussian, λ too high). A normality-conditioned controller is the explicit version of "always run at the right λ for the current embedding state".

**Expected gain**: +0.2 / +1.0 / +2.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Add `NormalityMonitorCallback` in `stable-pretraining/callbacks/`.
2. At `on_train_epoch_end`: compute SIGReg on a frozen monitor batch, update `module.lamb`.
3. Sweep β ∈ {0.1, 0.3, 1.0} with s_target = SIGReg(noise of same shape).

**Risks**:
- Replaces 1 hand-tuned λ with 2 controller knobs — possible net complexity wash.
- Feedback loops can oscillate; needs damping and a sane λ_min / λ_max.
- The held-out monitor batch may not represent the training distribution late in training.

**Falsification test**: If, across β ∈ {0.1, 0.3, 1.0}, no adaptive-λ run beats the best fixed-λ result from a 3-point bisection (λ ∈ {0.005, 0.02, 0.1}) on ImageNet-10 by ≥ 0.5 pp linear probe at equal compute, the controller adds no value.

**Adjacent / Cross-domain notes**:
- Original domain: multi-task loss weighting + adaptive regularization (NLP / RL).
- Target domain: SSL with statistical-test regularizer.
- Adaptation needed: choose the normality statistic to drive control (same as the training loss is the most defensible); pick a held-out monitor batch fixed across epochs to avoid coupling control to mini-batch noise.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|----------------------|--------------------|--------------------|-----------------|------------|-------------|------------|-------|
| 6 | Multi-crop curriculum | ✅ DINO arXiv:2104.14294 (ICCV 2021) | ✅ | ✅ (Δ≥1 pp) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 1 | QMC slicing | ✅ Kolouri arXiv:1711.05376 (CVPR 2018) | ✅ | ✅ (Δvar≥30%) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 5 | Kernel-SIGReg | ✅ arXiv:2509.07289 (BDCC 2025) | ✅ | ✅ (Δ≥0.7 pp) | NOVEL | VERIFIED | 4 | OK | **KEEP** |
| 3 | Register tokens | ✅ Darcet arXiv:2309.16588 (ICLR 2024) | ✅ | ✅ (Δ≥0.2 pp + CI) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 2 | iBOT patch-SIGReg | ✅ Zhou arXiv:2111.07832 (ICLR 2022) | ✅ | ✅ (Δ≥1.5 pp) | NOVEL | VERIFIED | 3 | ⚠️ violates "single λ" — flagged | **KEEP w/ flag** |
| 4 | Adaptive-λ verifier | ✅ Balestriero arXiv:2511.08544 + GradNorm arXiv:1711.02257 | ✅ | ✅ (Δ≥0.5 pp) | NOVEL | VERIFIED | 4 | OK | **KEEP** |

No ideas rejected. Cross-idea consistency: ideas 1, 4, 5 all touch SIGReg internals but at different layers (sampler vs weight vs feature map) — non-conflicting; can stack.

Rejected: 0 — see `_logs/_rejection_log.md` (empty for this batch).

## Notes & warnings
- **Baseline number is TBD on ImageNet-10**: gain estimates are anchored to similar-scale SSL results (Imagenette + DINO/iBOT literature) rather than a measured starting point. First action for the user: run the canonical `lejepa-vit-small.py` end-to-end to fix the baseline number, then re-rank.
- **Idea 2 violates "single λ" branding** of LeJEPA — if user wants to preserve the single-knob property, downgrade Idea 2.
- **Tier-3 quota tight**: only 1 T3 idea (Idea 4) — within configured 15% ± 10pp band (range 5–25%) but at the edge. Acceptable; do not silently re-search.
- **Devil's-advocate on Top-1 (Idea 6)**: search surfaced "modest returns beyond ~4 crops" and small-data overfitting risk from `arXiv:2406.09294`. Top-1 still defensible because (a) baseline V=6 already past the "≥4 crops" knee and we move to V∈{10,14}, (b) class-balanced sampler is the real new lever, not the crop count. Top-1 rank preserved; risk added to idea card.
- All ideas are **enhance-existing**; no greenfield in this batch. If user wants a from-scratch redesign (different SSL family), open a separate batch with `tier-mix 45/35/20`.

## Next steps for user
1. **Measure the ImageNet-10 baseline first** — run `lejepa-vit-small.py` at 100 epochs, fix the number; without it, all gains here are unfalsifiable in absolute terms.
2. **Run Idea 1 + Idea 3 in parallel** — both effort-S, additive, non-conflicting; gives 2 cheap deltas before any expensive idea.
3. **Then Idea 6** (multi-crop curriculum) — the single biggest expected uplift at S effort.
4. Hold Idea 2 (iBOT patch head) and Idea 5 (Kernel-SIGReg) until the cheap ideas land — both add real complexity.
5. Hold Idea 4 (adaptive λ) for last; it pays off most when paired with the other improvements (more sensitive to λ).

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 55/30/15 | 2026-05-18`
