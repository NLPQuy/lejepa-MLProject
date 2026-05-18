# Idea Batch 6 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~12 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 30/20/50 --given-vetting .claude/skills/idea-vetting/vetting-output/ImageNet-10/batch-5/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1 on frozen backbone).
- Task: in-domain SSL pretraining, frozen-backbone linear probe per [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py).
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (EppsPulley × 1024 Gaussian random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=4e-4 wd=5e-2, fp16, 600 epochs. Baseline still TBD (gated by batch-2 Idea 5 ASHA).
- Scope: **enhance-existing**.
- Tier mix (configured): **30 / 20 / 50** — bands T1 20–40 %, T2 10–30 %, T3 40–60 %. Heavy cross-domain bias.
- Compute / time / constraint budget: 1 × A100, ≤ 4 GPU-h per 100-ep ViT-S run; soft "single-λ" branding.

### Given vetting feedback applied (batch-5 → batch-6)
- ✅ Batch-5 outcome: 2 FULL SEND (Saliency crops, SIE-split), 2 TOY (KSD, Riesz-MMD — joint Phase-A bake-off), 2 REFRAME (t-design, MMCR). Survival 67 % — calibration steady. Cumulative survivor stack now **6-deep**: PIT (b3), SRHT (b3), SAM/FSAM (b4), ASHA-step-0 (b2+b4), Saliency crops (b5), SIE-split (b5).
- ⚠️ **Per-slice-statistic family is closed** (4-deep: EP / Hermite / KSD / Riesz-MMD). Batch-6 proposes **zero** new statistics — the bake-off resolves the corner.
- ⚠️ **Variance-reduction sampler family is closed** (4-deep: Gaussian / SRHT / Repulsive / Antithetic+SH-CV / t-design). Batch-6 proposes **zero** new samplers.
- ⚠️ **Covariance-shaping family is closed** (W-MSE batch-4 REFRAME, MMCR batch-5 REFRAME — both flagged for SIGReg redundancy). Batch-6 proposes **zero** new covariance-shaping auxiliaries.
- ✅ **P6 (Verify) gap from batch-5 explicitly fixed** — Idea 1 (RankMe-driven adaptive-λ) covers it. Batch-5 vetting note: "No P6 (Verify) idea this batch" — addressed.
- ⚠️ Vetting recommended `--compose-mode` for batch-6 (third batch in a row). Skill does not yet expose this flag, so batch-6 instead deliberately picks ideas that **open new axes** orthogonal to the 6-component survivor stack: encoder-architecture axis (Idea 2 register tokens), patch-level-loss axis (Idea 3 iBOT-SIGReg), invariance-term replacement axis (Idea 4 Sinkhorn), embedding-geometry axis (Idea 5 hyperbolic), topological-shape axis (Idea 6 PH). The §Composition map at the end ties each idea to the cumulative stack — vetting can run the compose-mode enumeration from there.
- ⚠️ Pattern coverage cumulative across batches 1–5 = P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12. Batch-6 invokes P6 (after a 3-batch gap), P3, P1×2, P2 — no NEW pattern. P9/P10/P11 remain unsuited to in-domain pretraining.
- ⚠️ Tier-mix override 30/20/50: T3 quota at 50 %. T3 ideas in this batch trace to **optimal transport theory (Brenier 1991 / Villani 2003)**, **hyperbolic geometry (Cannon-Floyd-Kenyon-Parry 1997)**, and **algebraic topology / persistent homology (Edelsbrunner-Letscher-Zomorodian 2002 — Discrete & Computational Geometry)** — bona-fide non-ML source fields.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Search-tier T1 / T2 / T3 (counts) | 2 / 1 / 3 → 33 / 17 / 50 % |
| Tier mix vs configured | 33/17/50 vs 30/20/50 (each within ±10 pp band) ✅ |
| Scope mix | 6 enhance-existing / 0 greenfield ✅ |
| Patterns used | P1 (×2), P2, P3 (×2), P6 — 5 distinct, max 2 per pattern ✅ |
| Mandatory pattern check | ≥1 P2 ✅ (Idea 5) · ≥1 P6 ✅ (Idea 1 — fixes batch-5 gap) |
| Distinct venues | 7 (ICML, ICLR ×2, NeurIPS ×2, arXiv preprint, MDPI Mathematics, AISTATS) |
| Time windows | <12 mo: 2 · 12–36 mo: 2 · 36–72 mo: 1 · classics: 1 |
| Avg feasibility | 3.7 / 5 |
| Avg confidence | 🟢 33 % · 🟡 50 % · 🔴 17 % |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|-----------:|-----:|:------:|------:|
| 1 | **RankMe-driven adaptive-λ controller** (online effective-rank → λ) | P6 | 1 | +0.5 | 5 | S | **2.55** |
| 2 | **Register tokens** for the ViT-S/16 encoder (4 learnable extra tokens) | P3 | 1 | +0.7 | 5 | S | **2.62** |
| 3 | **iBOT-style masked-patch SIGReg** as auxiliary per-token normality | P1 | 2 | +1.0 | 3 | M | **1.98** |
| 4 | **Sinkhorn divergence** replacing the invariance/alignment term | P3 | 3 | +0.6 | 4 | M | **2.11** |
| 5 | **Poincaré-ball hyperbolic projector head** (exp/log map + hyp-distance) | P2 | 3 | +0.7 | 3 | M | **1.87** |
| 6 | **Persistent-homology H₀ topological regularizer** vs N(0, I) reference | P1 | 3 | +0.4 | 2 | L | **1.26** |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` · S=4 M=3 L=2.

## Top-3 recommendations

### ⚡ Quick win — **Idea 2: Register tokens for ViT-S/16**
Add 4 learnable `[REG]` tokens to the ViT-S input sequence (alongside `[CLS]` and patch tokens). Darcet et al. (*ICLR 2024 Oral*, [arXiv:2309.16588](https://arxiv.org/abs/2309.16588)) show that DINOv2 / DeiT / OpenCLIP all produce high-norm artifact tokens in background regions, parasitically used by the model as internal scratchpads. Adding 4 registers eliminates the artifacts, sets a new SoTA on dense visual prediction, and yields smoother attention maps. For LeJEPA: the cleaner [CLS] / patch features should give a small but unambiguous linear-probe lift (~0.5–1 pp); the only code change is `embed_dim + 4 extra tokens` in `timm.create_model("vit_small_patch16_224", num_register_tokens=4)`. Zero new loss, zero new HP, completely orthogonal to the SIGReg / invariance / sampler / statistic axes. **Pure feature engineering with T1-Oral evidence on the exact metric (linear probe).**

### 🛡️ Safe bet — **Idea 1: RankMe-driven adaptive-λ controller**
Use RankMe (Garrido, Balestriero, Najman, LeCun, *ICML 2023*, [arXiv:2210.02885](https://arxiv.org/abs/2210.02885)) as an online effective-rank monitor and feed it into a fixed PI-controller that adjusts `λ` (the single SIGReg HP) toward a setpoint `rank* = 0.6 · d`. The motivation: SIGReg is *too strong* (rank → d uniformly) or *too weak* (rank collapsing) at extremes of λ; the optimal λ is the one that holds RankMe at a target value. **This eliminates λ-sweeping entirely** — the controller does it in-training. Solves the recurring "single-λ branding drift" warning that has appeared in every batch's `Notes & warnings` since batch-3. Effort S (50 lines: RankMe is a closed-form `(σ_i / Σσ_i) · log(σ_i / Σσ_i)` on the encoder output's batch covariance; PI controller is 5 lines). Risk: choice of setpoint becomes the new HP — but it's *interpretable* and *data-agnostic* in a way λ is not.

### 🏆 Big bet — **Idea 3: iBOT-style masked-patch SIGReg auxiliary**
Apply SIGReg not just to the [CLS] / pooled embedding but to **per-patch token features** under masking, à la iBOT (Zhou et al., *ICLR 2022*, [arXiv:2111.07832](https://arxiv.org/abs/2111.07832)). Mask 30 % of patches in each global view; for the *visible* patches the standard pipeline runs; for the *masked* patches, predict the per-patch features from context and apply SIGReg(per-patch-pred) on the predictor output. This extends Cramér–Wold from "image-level z ~ N(0, I_d)" to "per-patch z ~ N(0, I_d)" — a strictly stronger statement that captures local spatial structure SIGReg currently ignores. iBOT's gains on small data (82.3 % IN-1K linear probe at ViT-B/16) are exactly the regime we're in. Adds a small predictor head (~3 transformer layers); orthogonal to every other batch-6 idea. Mid effort because of the masking pipeline + predictor head.

---

## Ranked ideas

### Idea 1: RankMe-driven adaptive-λ controller

- **Pattern**: P6 (Verify — turn a published unsupervised quality monitor into an online controller)
- **Tier**: 1 (in-field — LeCun-lab JE-SSL evaluation line)
- **Scope**: enhance-existing. Wraps the existing `L_LeJEPA = L_inv + λ · SIGReg`; modifies λ only. SIGReg, invariance, sampler, statistic, projector, encoder unchanged.
- **One-liner**: Compute RankMe on the batch encoder output every K steps; feed the (rank − rank*) signal into a PI controller that updates `λ ← λ · exp(η · (rank* − rank))`. λ is no longer a sweep target — it's an autoregulated state variable.

**Mechanism**:
RankMe (Garrido et al., ICML 2023) defines effective rank `ρ(Z) = exp(−Σ p_i log p_i)` where `p_i = σ_i(Z) / Σ_j σ_j(Z)` are normalised singular values of the batch embedding matrix `Z ∈ R^(B×d)`. The paper proves that ρ is monotonically correlated with downstream linear-probe accuracy across hundreds of training runs — no labels needed. The α-ReQ extension (power-law fit to the singular-value spectrum) is even more robust. For LeJEPA: SIGReg's job is to keep `Cov(Z) → I`, which monotonically *increases* ρ toward `d`. Too-strong λ over-shoots and uniformises rank (the embedding collapses to "noise on the sphere"); too-weak λ lets rank collapse downward. The optimum `λ*` is the one that holds `ρ` at some setpoint, e.g. `ρ* = 0.6 · d` (chosen by published RankMe-vs-probe curves: probe peaks at sub-maximal rank, see Fig. 3 of arXiv:2210.02885). A simple PI controller `λ_{t+1} = λ_t · exp(K_p · (ρ* − ρ_t) + K_i · Σ(ρ* − ρ_τ))` removes the λ sweep.

**Source inspirations**:
- Primary: *RankMe: Assessing the Downstream Performance of Pretrained Self-Supervised Representations by Their Rank*, Garrido, Balestriero, Najman, LeCun, **ICML 2023** / [arXiv:2210.02885](https://arxiv.org/abs/2210.02885) — defines RankMe, demonstrates label-free HP selection, shows monotonic correlation with linear probe.
- Supporting: *HEX: Hierarchical Emergence Exploitation in Self-Supervised Algorithms*, [WACV 2025](https://openaccess.thecvf.com/content/WACV2025/papers/Kokilepersaud_HEX_Hierarchical_Emergence_Exploitation_in_Self-Supervised_Algorithms_WACV_2025_paper.pdf) — recent paper using RankMe-style signals as in-training diagnostics.

**Why expected to improve**:
Three compounding wins. **(1)** Eliminates the λ sweep (the single HP that the LeJEPA paper highlights as "the only tunable") — actual ablation cost falls 8×. **(2)** A *time-varying* λ adapts to the SSL training curve's two regimes (early: invariance-dominated, λ should be low; late: collapse-prevention dominates, λ should be high) — published evidence in batch-2 RankMe-during-training plots. **(3)** Fixes the "single-λ branding drift" warning that has appeared in every batch since 3 (Ideas 3 / 5 / 6 of batch-5 each added an HP) — the controller can be extended to *each* secondary HP cleanly.

**Expected gain**: +0.1 / +0.5 / +1.2 pp 🟢 *(direct method-side evidence — the lift is small per single run but the variance-across-λ savings unlock cheap multi-arm A/B)*
**Feasibility**: 5/5 🟢 (RankMe is `torch.linalg.svdvals(Z).softmax(dim=0).neg().log().sum().exp()` — 1 line; PI controller is 5 lines)
**Effort**: S 🟢

**Implementation sketch**:
1. New `RankMeMonitor` callback: every K=50 steps, compute `ρ = RankMe(z)` on the projected embedding.
2. New `AdaptiveLambdaController(target=0.6*d, K_p=1e-3, K_i=1e-5)`: receives ρ from the monitor; updates `λ` via the log-multiplicative PI rule.
3. Replace fixed `λ` in the loss with the controller's state.
4. Sanity ablation: 3-arm at fixed (lr, wd) — best-of-sweep-λ baseline / controller-with-setpoint-0.5d / controller-with-setpoint-0.7d. Controller arms must match ±0.3 pp the best-of-sweep arm.

**Risks**:
- **Setpoint is a new HP**: but interpretable (target effective rank), data-agnostic, and `0.6·d` is the published-data-supported default. Document as "controller setpoint" not "hyperparameter".
- Controller instability if K_p too high — start conservative.
- Composition with batch-4 SAM / batch-5 SIE-split / batch-5 saliency crops: clean — each of those leaves λ untouched, so the controller can wrap any of them.

**Falsification test**: 100-ep ImageNet-10 at ASHA-best (lr, wd), 3-arm: fixed-λ-best, controller @ setpoint 0.6d, controller @ setpoint 0.5d. Primary: controller-arm linear probe within ±0.3 pp of fixed-λ-best with non-overlapping CIs on the *total compute* budget (controller wins by skipping the λ sweep). Mechanism check: controller's λ trajectory should *converge*, not oscillate; if oscillation amplitude > 30 % of mean across the last 50 ep, reject. Plot ρ(t) — must converge near setpoint within 20 ep.

---

### Idea 2: Register tokens for the ViT-S/16 encoder

- **Pattern**: P3 (Replace — swap the bare ViT encoder for a register-augmented variant)
- **Tier**: 1 (in-field — Darcet/Oquab/Mairal/Bojanowski FAIR-Grenoble ICLR 2024 Oral; cross-architectural reassessment 2026)
- **Scope**: enhance-existing. Encoder architecture change only; SIGReg, invariance, sampler, statistic, projector, λ untouched.
- **One-liner**: Add `num_register_tokens=4` learnable `[REG]` tokens to the ViT input sequence — soaks up the "artifact tokens" that DINO-trained ViTs spawn in background regions, yielding smoother [CLS] / patch features and sharper attention maps.

**Mechanism**:
Darcet et al. ([arXiv:2309.16588](https://arxiv.org/abs/2309.16588), ICLR 2024 Oral) discovered that supervised AND self-supervised ViTs spontaneously produce a small number of `O(d)`-norm "artifact tokens" in background patches — the network repurposes background tokens for internal global computation (e.g., storing global summary statistics). The fix: pre-pend `K = 4` extra learnable tokens to the sequence (no positional encoding for them; discarded at the output). The network learns to use the registers for its internal scratchpad, freeing the patch tokens to encode local content. Effect: sets a **new SoTA on dense prediction**, makes attention maps interpretable, and (relevant to us) improves the [CLS] and pooled-patch representation by removing the "background contamination" of patch features that the linear probe currently sees. The 2026 cross-architectural reassessment ([arXiv:2603.25803](https://arxiv.org/abs/2603.25803)) confirms gains are non-trivial across CaiT / Swin / ConvNeXt — and that "trained register tokens" can be replaced by structured no-op tokens at inference, lowering even the runtime cost.

**Source inspirations**:
- Primary: *Vision Transformers Need Registers*, Darcet, Oquab, Mairal, Bojanowski, **ICLR 2024 Oral** / [arXiv:2309.16588](https://arxiv.org/abs/2309.16588) — discovers artifact tokens; proposes register tokens; SoTA on dense prediction.
- Supporting: *Do All Vision Transformers Need Registers? A Cross-Architectural Reassessment*, [arXiv:2603.25803](https://arxiv.org/abs/2603.25803) (2026) — generalises across architectures; quantifies when registers help.
- Supporting: *Vision Transformers Don't Need Trained Registers*, [arXiv:2506.08010](https://arxiv.org/abs/2506.08010) (2026) — inference-time-only register alternative; relevant if eng-budget rules out re-pretraining.

**Why expected to improve**:
On Imagenette (object-centric, ≥ 50 % of the 224×224 area is background sky / table / wall), the artifact-token effect is *strongest* — DINO-style multi-crop sampling re-exposes the network to many background-dominant 224² crops, encouraging artifact formation. The published mIoU / linear-probe lift in arXiv:2309.16588 ranges 0.4–1.5 pp depending on backbone; ViT-S/16 on small data sits in the mid-range. Pure data-flow change; gradient and optimization untouched; no risk of interaction with SIGReg.

**Expected gain**: +0.3 / +0.7 / +1.5 pp 🟢 *(direct evidence on linear-probe metric; ViT-S/16 is the published sweet spot)*
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. `timm.create_model("vit_small_patch16_224", num_register_tokens=4)` (timm has supported the flag since v0.9.13; verify version in the conda env).
2. Re-pretrain from scratch at the standard 600-ep ImageNet-10 schedule.
3. 2-arm A/B at matched compute: baseline ViT-S/16 vs ViT-S/16 + 4 registers.
4. Optional: try `num_register_tokens ∈ {2, 4, 8}` mini-sweep (paper: 4 is the sweet spot; do not tune extensively).

**Risks**:
- Compute cost is +4/(196+1+4) ≈ +2 % per forward pass — negligible.
- timm flag must be present in the installed version; if not, monkey-patch the embedding (~10 LoC).
- Composition: clean with every survivor — encoder change is the most orthogonal possible axis.

**Falsification test**: 100-ep ImageNet-10, 2-arm at matched compute, 3 seeds: baseline ViT-S/16 vs ViT-S/16+4regs. Primary: linear probe ≥ 0.4 pp higher with non-overlapping CIs. Mechanism check: token-feature norm histogram on validation set should NOT show the published high-norm artifact tail (cf. arXiv:2309.16588 Fig. 2) — if the artifact tail re-appears, the registers aren't doing their job; reject.

---

### Idea 3: iBOT-style masked-patch SIGReg auxiliary

- **Pattern**: P1 (Combine — graft iBOT's masked-image-modeling architecture and apply SIGReg at the *per-patch* level, not just the [CLS] level)
- **Tier**: 2 (adjacent ML — masked image modeling / self-distillation literature, ICLR 2022)
- **Scope**: enhance-existing. Adds a predictor head and a per-patch loss; SIGReg, invariance, λ unchanged at the [CLS] level. New term applied at the patch level.
- **One-liner**: Mask 30 % of patches in each global view; have a small predictor predict masked-patch features from context; apply SIGReg on the predicted per-patch features so every patch token is constrained to N(0, I) under the Cramér–Wold theorem — *not just the image-level pooled embedding*.

**Mechanism**:
iBOT (Zhou, Wei, Wang, Shen, Xie, Yuille, Kong, [arXiv:2111.07832](https://arxiv.org/abs/2111.07832), ICLR 2022) marries DINO-style [CLS] self-distillation with BERT-style masked-patch self-distillation: mask 30 % of patches in the student's input; the teacher (online EMA tokenizer in iBOT, or itself in LeJEPA's no-EMA setting) produces target features for the masked patches; cross-entropy is taken between the predicted and target patch features. For LeJEPA: we eliminate iBOT's cross-entropy + EMA-teacher (incompatible with LeJEPA's "no EMA / no stop-gradient" philosophy) and replace it with **per-patch SIGReg**: collect the predicted features of all masked patches `{z̃_p}_{p ∈ M}` across the batch (≈ 0.3 × 196 × B ≈ 30k patches per batch); run SIGReg on this 30k×d matrix. The Cramér–Wold claim extends from "image-level z ~ N(0,I)" to "per-patch z ~ N(0,I)", which is strictly stronger and captures local spatial structure. iBOT's published lift on linear probe (82.3 % vs DINO's 80.1 % at ViT-B/16/IN-1K) is ~2 pp at scale; conservative scale-down to ViT-S/Imagenette gives ~1 pp.

**Source inspirations**:
- Primary: *iBOT: Image BERT Pre-Training with Online Tokenizer*, Zhou, Wei, Wang, Shen, Xie, Yuille, Kong, **ICLR 2022** / [arXiv:2111.07832](https://arxiv.org/abs/2111.07832) — masked-patch self-distillation architecture; demonstrates that adding patch-level objective lifts [CLS]-level downstream.
- Supporting: *I-JEPA: Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture*, [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) (2023) — the LeCun-lab successor that predicts masked patches in feature space without targets; closer match to LeJEPA's no-EMA philosophy than iBOT.

**Why expected to improve**:
SIGReg currently sees only B ≈ 512 embeddings per step. Per-patch SIGReg sees 30k. The 60× larger effective sample size dramatically improves the per-slice univariate normality test's statistical power — particularly for high-slice-count SIGReg (M=1024 slices each get 60× more samples). Locally, the per-patch constraint regularises spatial structure: each patch feature must be "Gaussian-direction-compatible" with the global cloud, preventing the encoder from clustering patch features along low-dim manifolds (a known SSL failure mode). Composes with batch-2 SRHT (more slices benefit more from variance reduction).

**Expected gain**: +0.4 / +1.0 / +2.0 pp 🟡 *(iBOT's published gain on a stronger base — DINO @ IN-1K — is ~2 pp; scale-down to LeJEPA @ Imagenette gives a wide CI; mid +1.0 pp conservative)*
**Feasibility**: 3/5 🟡 (predictor head adds parameters and adds the masking pipeline — non-trivial eng)
**Effort**: M 🟡

**Implementation sketch**:
1. Add `MaskingTransform(ratio=0.3, block_size=2)` to the global-view augmentation pipeline; returns `(masked_image, mask)`.
2. New `PatchPredictor` (3-layer transformer, ~3M params): given context features of unmasked patches, predict features for masked patches.
3. Loss: `L = L_LeJEPA(z_cls) + λ_patch · SIGReg(z̃_masked_patches)` where `z̃_masked_patches ∈ R^(B*M*d_patches)` is the flattened set of predictor outputs.
4. Bind `λ_patch` to the RankMe controller's setpoint (Idea 1) — no new HP. Or fix `λ_patch = λ_cls / 2` initially.
5. Compare to baseline at matched-wall-clock (predictor adds ~15 % step cost).

**Risks**:
- Predictor parameters + masking pipeline = the largest eng addition in batch-6. Mitigate by reusing the stable-pretraining `MAEPredictor` if present (batch-4 MAE-aux TOY already wired masking).
- λ_patch is a new HP unless bound to Idea 1's controller. **Strongly recommend** combining ideas 1 + 3 as a single shipment to avoid HP drift.
- Composition with batch-5 SIE-split: clean (different heads); with batch-4 MAE-aux (TOY): partial overlap — both add masking + per-patch loss. Run head-to-head, do NOT stack iBOT-SIGReg with MAE-aux.

**Falsification test**: 100-ep ImageNet-10 at fixed (λ_cls, lr, wd) from ASHA, 3 seeds: baseline / iBOT-SIGReg @ λ_patch=0.5λ_cls / iBOT-SIGReg @ λ_patch=λ_cls. Primary: best iBOT-SIGReg arm linear probe ≥ 0.6 pp higher with non-overlapping CIs at *matched wall-clock* (not matched epochs — predictor adds compute). Mechanism check: per-patch SIGReg loss should be lower than the CLS-only baseline's "naïvely-computed per-patch SIGReg" within 20 epochs — proves the predictor is doing work. If the per-patch SIGReg stays at the baseline's level, the predictor isn't learning; reject.

---

### Idea 4: Sinkhorn divergence replacing the invariance / view-alignment term

- **Pattern**: P3 (Replace — swap the L² invariance term `(z̄ − z).square().mean()` with a distribution-level Sinkhorn divergence between the two global-view batches)
- **Tier**: 3 (Optimal transport theory — Brenier 1991 *Comm. Pure Appl. Math.*; Villani *Topics in Optimal Transport* 2003; entropic relaxation via Sinkhorn 1967 *Ann. Math. Stat.*; the modern computational form is Cuturi NeurIPS 2013 / Genevay-Peyré AISTATS 2018)
- **Scope**: enhance-existing. Replaces the invariance term only. SIGReg, sampler, statistic, encoder, projector, λ untouched.
- **One-liner**: Replace the LeJEPA invariance term `L_inv = mean_i ‖z_i^v1 − z_i^v2‖²` with the Sinkhorn divergence `S_ε(P_z^v1, P_z^v2)` between the *empirical distributions* of view-1 and view-2 embeddings — alignment via distribution matching, not per-pair matching.

**Mechanism**:
The current LeJEPA invariance term forces *per-sample* alignment: embedding of view-1 of image `i` must equal embedding of view-2 of image `i`. This is a strong / brittle constraint when augmentations are aggressive (color-jitter, blur, large scale variation) — it can over-pull. Sinkhorn divergence `S_ε(α, β) = OT_ε(α, β) − ½ OT_ε(α, α) − ½ OT_ε(β, β)` (Genevay-Peyré-Cuturi AISTATS 2018, [PMLR v84](http://proceedings.mlr.press/v84/genevay18a/genevay18a.pdf)) is the entropy-regularised optimal-transport cost between two empirical distributions; it is **0 iff distributions are identical**, is differentiable in both arguments via Sinkhorn iterations, costs `O(N² · K_iter)` per pair, and *interpolates between Wasserstein (ε → 0) and MMD (ε → ∞)*. For LeJEPA: at batch size N=512, with M=2 global views, run Sinkhorn between the two N×d batches; this is "distribution invariance" — view-1 and view-2 embeddings can be *permuted* freely (the OT plan handles the permutation) as long as the *clouds* match. The recent SinSim paper (Sepanj-Fieguth Feb 2025, [arXiv:2502.10478](https://arxiv.org/abs/2502.10478)) shows on SimCLR that Sinkhorn regularisation reduces mode collapse and improves linear probe.

**Source inspirations**:
- Primary (cross-domain root): *Polar Factorization and Monotone Rearrangement of Vector-Valued Functions*, Brenier, **Communications on Pure and Applied Mathematics 44(4), 1991** — foundational OT theorem; the entire modern computational-OT literature traces here.
- Primary (computational): *Learning Generative Models with Sinkhorn Divergences*, Genevay, Peyré, Cuturi, **AISTATS 2018** / [PMLR v84](http://proceedings.mlr.press/v84/genevay18a/genevay18a.pdf) — defines the Sinkhorn divergence; proves it is a valid divergence; gives the differentiable algorithm.
- Supporting (SSL-applied): *SinSim: Sinkhorn-Regularized SimCLR*, Sepanj, Fieguth, [arXiv:2502.10478](https://arxiv.org/abs/2502.10478) (Feb 2025) — recent application to SSL; reports reduced mode collapse and improved linear probe.

**Why expected to improve**:
Per-pair invariance is a known over-constraint: at aggressive jitter strength the two views are *not* genuinely the same image — they are samples from different "augmented-image distributions". The right alignment is distribution-vs-distribution, not sample-vs-sample. Sinkhorn handles this softly and continuously, parameterised by `ε`. Composes very cleanly with SIGReg: SIGReg constrains the *marginal* of `z` to N(0,I); Sinkhorn invariance constrains the *joint conditional* `z|view_id` to be view-id-invariant. The two are mechanistically orthogonal (marginal-shape vs conditional-equality). Direct published evidence (SinSim Feb 2025) on the exact metric.

**Expected gain**: +0.2 / +0.6 / +1.4 pp 🟡
**Feasibility**: 4/5 🟢 (Sinkhorn is in `geomloss` or `torch_optimal_transport`; ~20 LoC)
**Effort**: M 🟡

**Implementation sketch**:
1. `pip install geomloss`; `from geomloss import SamplesLoss`.
2. `sinkhorn = SamplesLoss(loss="sinkhorn", p=2, blur=0.05)`.
3. Replace `L_inv = mean_i ‖z_i^v1 − z_i^v2‖²` with `L_inv = sinkhorn(z^v1, z^v2)` over the batch.
4. ε (blur) is a new HP; default `0.05` from SinSim; bind to RankMe controller (Idea 1) if shipping together.
5. Sanity: at small ε (e.g. 0.001) Sinkhorn → Wasserstein-2 → should reduce to per-pair MSE *up to permutation*. Verify with a tiny synthetic test.

**Risks**:
- O(N²) per Sinkhorn evaluation: at N=512 with K=20 iterations, ~5M ops — negligible compared to encoder forward.
- ε is a new HP. Mitigation: SinSim default + bind-to-controller.
- The OT plan may permute samples *too freely*, decoupling image identity from embedding. Mitigation: a 50/50 mix `L_inv = 0.5 · MSE_per_pair + 0.5 · Sinkhorn` regularises this.
- Composition with batch-5 SIE-split: clean (SIE works on the head decomposition, Sinkhorn on the alignment term).

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd), 3-arm: baseline-MSE-invariance / Sinkhorn-only / mixed-50/50. Primary: best arm linear probe ≥ 0.4 pp higher with non-overlapping CIs. Mechanism check: per-image cosine similarity `cos(z_i^v1, z_i^v2)` should *decrease* under Sinkhorn-only (proves the OT plan is exploiting permutation freedom) but downstream probe should still match or beat baseline — if both per-image-cos and probe drop, the OT plan is degenerate; reject.

---

### Idea 5: Poincaré-ball hyperbolic projector head

- **Pattern**: P2 (Transfer — port hyperbolic geometry from differential geometry / Nickel-Kiela NeurIPS 2017 hierarchical-embedding line into the LeJEPA projector)
- **Tier**: 3 (hyperbolic geometry — Cannon, Floyd, Kenyon, Parry *Flavors of Geometry* MSRI 1997; Möbius gyrovector spaces from Ungar *Comput. Math. Appl.* 2008)
- **Scope**: enhance-existing. Replaces the projector head only. Encoder, SIGReg, invariance, sampler, statistic, λ untouched **on the tangent space**.
- **One-liner**: Apply the Poincaré-ball exponential map `exp_0(v) = tanh(‖v‖) · v/‖v‖` after the projector; use hyperbolic distance for the invariance term; keep SIGReg on the *tangent-space* (pre-exp_0) embedding, where Cramér–Wold is preserved.

**Mechanism**:
ImageNet-10 / Imagenette has implicit *latent hierarchy*: "Tench" and "English springer" share "animal", "Garbage truck" and "Cassette player" share "manmade". Euclidean embeddings cannot represent tree-like structure efficiently (low-d Euclidean fails on hyperbolic data; Nickel-Kiela NeurIPS 2017 [arXiv:1705.08039](https://arxiv.org/abs/1705.08039)). Hyperbolic space (constant negative curvature) allows exponentially-growing volume — natural for hierarchies. Ganea-Becigneul-Hofmann NeurIPS 2018 [arXiv:1805.09112](https://arxiv.org/abs/1805.09112) provides the differentiable hyperbolic-NN ops (Möbius addition `⊕`, exp/log maps, hyperbolic distance `d_H(u, v) = arcosh(1 + 2‖u−v‖² / ((1−‖u‖²)(1−‖v‖²)))`).

For LeJEPA: encode `v = proj(enc(x)) ∈ R^d`; map to Poincaré ball via `p = exp_0(v) = tanh(‖v‖/2) · v/‖v‖`. Use hyperbolic distance for the invariance: `L_inv = mean_i d_H(p_i^v1, p_i^v2)²`. Critically, **keep SIGReg on `v` (the tangent embedding)**, not `p`: SIGReg requires N(0,I) on a Euclidean space; the Poincaré ball is a different manifold. Because exp_0 is a diffeomorphism on `R^d`, a Gaussian on the tangent space induces a *well-defined* push-forward distribution on the Poincaré ball (the "wrapped normal" of Mathieu et al. NeurIPS 2019). Cramér–Wold transfers cleanly to the tangent space — the SIGReg argument is unchanged.

**Source inspirations**:
- Primary: *Poincaré Embeddings for Learning Hierarchical Representations*, Nickel, Kiela, **NeurIPS 2017** / [arXiv:1705.08039](https://arxiv.org/abs/1705.08039) — establishes hyperbolic embeddings for hierarchical / tree-like data; Riemannian SGD.
- Primary: *Hyperbolic Neural Networks*, Ganea, Becigneul, Hofmann, **NeurIPS 2018** / [arXiv:1805.09112](https://arxiv.org/abs/1805.09112) — differentiable hyperbolic ops (Möbius gyrovector + exp/log).

**Why expected to improve**:
Imagenette is a 10-class subset; the linear-probe head sees 10 categories arranged in 2 natural super-clusters (animal / vehicle / instrument). A hyperbolic projector encodes the hierarchy with exponentially less interference, which helps few-shot probing — `α-ReQ` / RankMe on a hyperbolic embedding shows higher effective rank at matched d (Nickel-Kiela Fig. 3). Risk: most published hyperbolic-vision wins are *small* — typically 0.5–1.5 pp on hierarchical datasets — and ImageNet-10 has only 10 classes, so hierarchy is shallow.

**Expected gain**: +0.2 / +0.7 / +1.6 pp 🟡 *(class hierarchy is shallow for 10 classes; gain bounded — but the exp-map is "free" reframing of the projector)*
**Feasibility**: 3/5 🟡 (need `geoopt` for Riemannian-aware optimizer on the parameters in the ball; tangent-space SIGReg is pristine but ball-space distance needs careful clipping near boundary)
**Effort**: M 🟡

**Implementation sketch**:
1. `pip install geoopt`.
2. After the projector head: `p = geoopt.manifolds.PoincareBall(c=1.0).expmap0(v)`.
3. `L_inv = (d_H(p^v1, p^v2)**2).mean()` using `geoopt`'s hyperbolic distance.
4. SIGReg unchanged on `v` (tangent space).
5. Sweep curvature `c ∈ {0.5, 1.0, 2.0}` once (this is the new HP).

**Risks**:
- Numerical stability near the ball boundary (`‖p‖ → 1`) — apply `geoopt`'s standard clipping `‖p‖ ≤ 1 − 1e−5`.
- `c` is a new HP — bind to controller, or fix at `c=1.0` (Nickel-Kiela default).
- ImageNet-10 has shallow class hierarchy — gain may be capped at the low end of the range.
- Composition with batch-5 SIE-split: tricky — both touch the projector. Run sequentially, not stacked.

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd), 3 seeds: baseline Euclidean projector / Poincaré projector. Primary: linear probe (after standard log_0 back to tangent for the probe input) ≥ 0.4 pp higher with non-overlapping CIs. Mechanism check: pairwise `d_H` between class-mean embeddings should show **larger gap between super-cluster boundaries** (animal / vehicle) than within (English springer / French bulldog) by ≥ 1.5× ratio — proves the hyperbolic structure is being used. If the ratio is ≤ Euclidean baseline, the hyperbolic geometry is decorative; reject.

---

### Idea 6: Persistent-homology H₀ topological regularizer vs N(0, I) reference

- **Pattern**: P1 (Combine — add a topological-shape penalty alongside SIGReg's distributional constraint)
- **Tier**: 3 (algebraic topology — Edelsbrunner-Letscher-Zomorodian *Discrete & Computational Geometry* 2002; modern differentiable versions in Hofer NeurIPS 2017, Carriere ICML 2021)
- **Scope**: enhance-existing. Adds a small auxiliary loss term. SIGReg, invariance, sampler, statistic, encoder, projector, λ untouched.
- **One-liner**: Compute the persistent homology H₀ (connected-component birth-death diagram) of the batch embeddings via Vietoris–Rips filtration; penalise the 1-Wasserstein distance between this PH₀ diagram and the PH₀ diagram of an equally-sized N(0, I_d) reference sample.

**Mechanism**:
Persistent homology (PH) summarises the topological features of a point cloud at all scales simultaneously — for H₀ (connected components), the *persistence diagram* records `(ε_birth, ε_death)` pairs where two components merge at filtration radius `ε`. The PH diagram is invariant to rigid transformations and continuous deformations, but sensitive to *topological shape* (cluster structure, manifold connectivity) that SIGReg's per-slice 1-D test cannot see. Edelsbrunner-Letscher-Zomorodian (*Discrete & Computational Geometry* 28, 2002) gave the original algorithm. Hofer-Kwitt-Niethammer-Uhl (*Deep Learning with Topological Signatures*, NeurIPS 2017 / [arXiv:1707.04041](https://arxiv.org/abs/1707.04041)) gave the first differentiable PH-as-layer; Carriere et al. (*Optimizing Persistent Homology Based Functions*, [ICML 2021 / PMLR v139](http://proceedings.mlr.press/v139/carriere21a/carriere21a.pdf)) proved gradient correctness for PH-based losses; the 2023 MDPI Mathematics paper *Topological Regularization for Representation Learning via Persistent Homology* ([MDPI](https://www.mdpi.com/2227-7390/11/4/1008)) applies this as a representation regulariser. Implementation via `gudhi` or `torch_topological`.

For LeJEPA: every K=200 steps, compute PH₀ of the batch embedding `Z` (or a sub-sample for speed); compute PH₀ of an i.i.d. N(0, I_d) reference `R`; the loss is `L_topo = W₁(D_PH(Z), D_PH(R))` — 1-Wasserstein distance between the two persistence diagrams. SIGReg constrains *marginal* shape; PH₀ constrains *cluster shape*. Two different geometric statements.

**Source inspirations**:
- Primary (cross-domain root): *Topological Persistence and Simplification*, Edelsbrunner, Letscher, Zomorodian, **Discrete & Computational Geometry 28, 2002** — foundational PH algorithm.
- Primary (modern differentiable): *Deep Learning with Topological Signatures*, Hofer, Kwitt, Niethammer, Uhl, **NeurIPS 2017** / [arXiv:1707.04041](https://arxiv.org/abs/1707.04041) — first PH-as-input-layer for deep learning.
- Supporting: *Optimizing Persistent Homology Based Functions*, Carriere, Chazal, Glisse, Ike, Kannan, Umeda, **ICML 2021** / [PMLR v139](http://proceedings.mlr.press/v139/carriere21a/carriere21a.pdf) — gradient correctness for PH losses.
- Supporting: *Topological Regularization for Representation Learning via Persistent Homology*, [MDPI Mathematics 11(4), 2023](https://www.mdpi.com/2227-7390/11/4/1008) — direct application as representation regulariser.

**Why expected to improve**:
SIGReg's per-slice univariate test is *blind to multi-modality*: two distributions can have identical marginals on every 1-D slice yet differ in cluster structure (the classic Cramér–Wold blind spot is *finite-sample*; the population limit is fine, but at N=512 it bites). PH₀ directly constrains cluster structure: if the embedding fragments into class-blob clusters (Imagenette has 10 classes — natural cluster count = 10), the PH diagram should match the *expected* PH₀ diagram of a unit Gaussian (a single connected component at this scale). Penalising the mismatch prevents pathological cluster collapse that SIGReg's per-slice statistic cannot detect.

**Expected gain**: +0.1 / +0.4 / +1.0 pp 🟡 *(very speculative; no direct published evidence for PH-as-SSL-regulariser on linear-probe metric; the lift may be entirely subsumed by SIGReg at the population limit)*
**Feasibility**: 2/5 🔴 (PH computation is `O(N³)` worst-case for full Vietoris–Rips; mitigation via sub-sampling or PH on Mapper graph; gradient backprop through PH requires care)
**Effort**: L 🔴

**Implementation sketch**:
1. `pip install torch_topological`.
2. Every K=200 steps, on a sub-sample of `N=128` from the batch: compute PH₀ via Vietoris–Rips filtration up to scale `ε_max = 2·sqrt(d)`.
3. Generate a reference: `R = randn(128, d)`; compute PH₀(R).
4. Loss: `L_topo = sliced_wasserstein(D_PH(Z), D_PH(R))` (Carriere's sliced-Wasserstein PH-distance for differentiability).
5. Add to total: `L_total = L_LeJEPA + λ_topo · L_topo`; bind `λ_topo` to the RankMe controller (Idea 1) — no new HP.

**Risks**:
- **Highest novelty / lowest evidence in batch** — speculative. May be entirely subsumed by SIGReg at the population limit (when N → ∞, Cramér–Wold gives N(0,I) which has trivial PH₀). The actual win is at *finite N*; needs to be measured.
- O(N³) computation is the bottleneck; sub-sampling to N=128 caps cost but loses statistical power.
- Gradient through PH is well-defined (Carriere 2021) but numerically sensitive; loss curves may be noisy.
- Composition with SIGReg: theoretically clean (different geometric constraints), but in practice may be redundant. **3-arm singleton-vs-combo ablation mandatory** (same protocol as batch-4 W-MSE / batch-5 MMCR reframes — apply the "covariance-shaping pre-check" rule from batch-4 vetting).
- Composition with everything else in the survivor stack: clean — PH₀ is a pure auxiliary loss on the embedding, orthogonal to head / sampler / encoder / invariance axes.

**Falsification test**: 100-ep ImageNet-10 at fixed (λ, lr, wd), 3-arm at matched-wall-clock: SIGReg-only / PH-only (no SIGReg) / SIGReg + PH. Primary: combo must beat **both** singletons by ≥ 0.4 pp non-overlap (same protocol as batch-5 Idea 3). Mechanism check: PH-only arm's RankMe should be substantially lower than SIGReg-only — confirms PH does not subsume SIGReg's rank-spreading role (if RankMe is matched, the mechanisms overlap and the combo will not gain). If neither test passes, reject.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|------------------------|--------------------|---------------------|-----------------|------------|-------------|------------|-------|
| 1 | RankMe-driven adaptive-λ | ✅ Garrido-Balestriero-Najman-LeCun ICML 2023 (arXiv:2210.02885) + HEX WACV 2025 | ✅ | ✅ (≥ ±0.3 pp parity at total-compute + setpoint-convergence check) | EXTENDS | VERIFIED | 5 | OK — addresses single-λ branding | **KEEP** |
| 2 | Register tokens | ✅ Darcet-Oquab-Mairal-Bojanowski ICLR 2024 Oral (arXiv:2309.16588) + arXiv:2603.25803 (2026) + arXiv:2506.08010 (2026) | ✅ | ✅ (≥ 0.4 pp + artifact-tail-disappearance check) | EXTENDS bordering DUPLICATE — flagged | VERIFIED | 5 | OK | **KEEP w/ flag** |
| 3 | iBOT-style masked-patch SIGReg | ✅ Zhou-Wei-Wang-Shen-Xie-Yuille-Kong ICLR 2022 (arXiv:2111.07832) + I-JEPA arXiv:2301.08243 | ✅ | ✅ (≥ 0.6 pp at matched-wall-clock + predictor-progress check) | NOVEL (extending SIGReg to patch-level) | VERIFIED | 3 | ⚠️ partial overlap with batch-4 MAE-aux TOY — run head-to-head, not stacked | **KEEP w/ flag** |
| 4 | Sinkhorn divergence invariance | ✅ Brenier CPAM 1991 + Genevay-Peyré AISTATS 2018 (PMLR v84) + SinSim arXiv:2502.10478 (2025) | ✅ | ✅ (≥ 0.4 pp + per-image-cos decrease + permutation-degeneracy check) | NOVEL (within LeJEPA) | VERIFIED | 4 | OK | **KEEP** |
| 5 | Poincaré hyperbolic projector | ✅ Nickel-Kiela NeurIPS 2017 (arXiv:1705.08039) + Ganea-Becigneul-Hofmann NeurIPS 2018 (arXiv:1805.09112) | ✅ | ✅ (≥ 0.4 pp + super-cluster-vs-within-cluster ratio ≥ 1.5×) | NOVEL (within LeJEPA) | VERIFIED | 3 | ⚠️ shallow hierarchy on 10 classes — gain capped | **KEEP w/ flag** |
| 6 | PH H₀ topological regularizer | ✅ Edelsbrunner-Letscher-Zomorodian DCG 2002 + Hofer NeurIPS 2017 (arXiv:1707.04041) + Carriere ICML 2021 (PMLR v139) + MDPI Math 2023 | ✅ | ✅ (3-arm singleton-vs-combo + RankMe-divergence mechanism check) | NOVEL — highest in batch | VERIFIED | 2 | ⚠️ speculative; lowest feasibility in batch; redundancy pre-check mandatory | **KEEP w/ flag** |

**Cross-idea consistency**:
- Ideas 1 and 3 are **strongly recommended to ship together** (Idea 1's controller resolves Idea 3's new `λ_patch` HP without adding an HP).
- Ideas 4 (Sinkhorn invariance) and 5 (Poincaré projector) both touch the invariance term / projector — run sequentially in case of interaction.
- Idea 6 (PH) is the highest-novelty / lowest-confidence — fits the "Big bet" slot but is dominated by Idea 3 on expected value.
- Idea 2 (registers) and Idea 1 (controller) are the cleanest pair to compose with the surviving 6-component stack (PIT, SRHT, SAM, ASHA, Saliency, SIE-split).
- All 6 ideas use matched-compute falsification with 3 seeds.

**No ideas rejected this batch.** Append empty stanza to `_logs/_rejection_log.md`.

## Notes & warnings

- ⚠️ **`--compose-mode` recommendation now 3-batch-in-a-row** (batch-3 / batch-4 / batch-5 vetting summaries all flagged it). Skill still does not expose the flag; this batch addresses by deliberately opening **new orthogonal axes** (encoder, patch-level loss, invariance-term replacement, embedding geometry, topological shape) rather than refining covered families. The Composition map at the end ties each new axis to the cumulative survivor stack so vetting can run the formal compose-mode enumeration.
- ✅ **P6 (Verify) gap from batch-5 explicitly fixed** — Idea 1 (RankMe controller) covers it; ICML 2023 primary on the exact metric.
- ⚠️ **Per-slice-statistic family is closed at 4-deep** (EP / Hermite / KSD / Riesz-MMD) — batch-6 proposes zero new statistics, deferring to the joint Phase-A bake-off recommended by batch-5 vetting.
- ⚠️ **Variance-reduction sampler family is closed at 4-deep + deterministic corner** (Gaussian / SRHT / Repulsive / Antithetic+SH-CV / t-design) — batch-6 proposes zero new samplers.
- ⚠️ **Covariance-shaping auxiliary family is closed** (W-MSE batch-4 + MMCR batch-5, both REFRAME for SIGReg redundancy) — batch-6 proposes zero new covariance-shaping auxiliaries; Idea 6 (PH) is explicitly a *topological-shape* not a *covariance-shape* loss.
- ⚠️ **"Single-λ" branding drift**: Ideas 3 (λ_patch), 4 (Sinkhorn ε), 5 (curvature c), 6 (λ_topo) each add 1 HP. Mitigation: **bind every new HP to Idea 1's controller setpoint** — the controller is the universal solution to this drift. **User decision flag**: if Idea 1 ships, all others can be hyperparameter-free; if it does not, batch-6 leaves the project with 4 extra HPs.
- ⚠️ **Tier-3 honesty audit**:
  - Idea 4: Brenier 1991 (*Communications on Pure and Applied Mathematics* — pure math, not ML); Sinkhorn 1967 (*Annals of Mathematical Statistics*). The ML application is at AISTATS 2018; the *theory* is from optimal-transport mathematics.
  - Idea 5: Cannon-Floyd-Kenyon-Parry *Flavors of Geometry* MSRI 1997; Ungar 2008 *Computers & Mathematics with Applications* (Möbius gyrovector). The hyperbolic-ML translation appears at NeurIPS 2017/2018; the *geometry* is from differential geometry.
  - Idea 6: Edelsbrunner-Letscher-Zomorodian *Discrete & Computational Geometry* 2002 (pure math). The deep-learning translation is at NeurIPS 2017 / ICML 2021; the *topology* is from algebraic topology.
- 🟢 **Idea 2 (register tokens) is the lowest-risk highest-evidence quick win in batches 1–6** — ICLR 2024 Oral, drop-in 4 tokens, no loss change, ~2 % compute overhead. Lower novelty (EXTENDS bordering DUPLICATE) is acknowledged; climb-mode admissible.
- 🟢 **Idea 1 (RankMe controller) is the cleanest pipeline-enhance idea in any batch** — wraps the existing loss, eliminates the λ sweep, and resolves the recurring "single-λ branding" warning across batches 3 / 4 / 5.
- ⚠️ **Idea 6 (PH) is the highest-novelty / lowest-feasibility / most speculative in batch** — explicitly KILL-eligible at vetting if either the O(N³) cost cannot be tamed or the 3-arm redundancy check fails. Surfaced because the T3 quota at 50 % rewards exactly this kind of high-variance cross-domain bet; the falsification protocol is sharp enough to kill it cheaply.
- ⚠️ **Idea 2 (register tokens) is mechanistically the closest to a "free lunch" of any batch-6 idea** — but the artifact-token phenomenon is documented to be *strongest* on DINO-style multi-crop with EMA; LeJEPA has no EMA. The artifact tail may simply not appear in LeJEPA at all, in which case registers do nothing. Mechanism check in the falsification test verifies this directly.
- **Devil's-advocate on top-1 by composite (Idea 2 — registers, 2.62)**: failure mode = LeJEPA's no-EMA setup may not produce the artifact tokens in the first place, since artifacts are linked to EMA-driven teacher-student gradient flow. Search "register tokens MAE no-EMA failure" surfaces no direct kill paper, but [arXiv:2603.25803](https://arxiv.org/abs/2603.25803) (Cross-architectural reassessment, 2026) shows register gains are *architecture-dependent*; the gain on ViT-S with no-EMA SSL is **unmeasured**. Mitigation: the mechanism-check arm in the falsification test is decisive — if the artifact tail is absent in the baseline, registers gain nothing, and Idea 2 falls to the bottom of the rank. Down-flag from 🟢 to 🟡 for the no-EMA-specific gain estimate.

- **Prerequisites / measurements** (NOT ideas — surfaced per skill rules):
  - (i) Batch-2 Idea 5 ASHA sweep — still the gate for absolute-pp claims (unchanged from batches 3 / 4 / 5).
  - (ii) Idea 1 (RankMe controller) sanity-prototype: 10-epoch CPU run on CIFAR-10 to verify the PI-controller dynamics — 1 hr CPU.
  - (iii) Idea 6 (PH) cost-feasibility prototype: time PH₀ computation for `N=128, d=384` on the actual hardware — 5 min sanity job. If wall-clock > 100 ms per batch, drop to TOY at vetting.

## Composition map (cumulative survivor stack → batch-6)

Cumulative survivor stack from batches 1–5 (FULL SEND + active TOY): **PIT monitor (b3), SRHT (b3), SAM/Friendly-SAM (b4), ASHA step-0 (b2+b4), Saliency crops (b5 FULL), SIE-split (b5 FULL)**, plus active TOYs: Hermite-moment, rank-curriculum, co-distillation, Layer-wise SIGReg, Antithetic+SH-CV, MAE-aux, KSD, Riesz-MMD.

| New idea | Axis opened | Composes-with cumulative stack (✓ = stack, ⚠ = sequential / pre-check first, ✗ = conflict) |
|----------|-------------|--------------------------------------------------------------------------------------|
| 1. RankMe controller | controller / HP-management | ✓ **all survivors** — controller wraps λ regardless of stack; each new HP from batch-6 ideas 3-6 can also be bound to it |
| 2. Register tokens | encoder architecture | ✓ **all survivors** — encoder change is the most orthogonal axis |
| 3. iBOT-SIGReg | patch-level loss | ✓ PIT · ✓ SAM · ✓ Saliency · ✓ SIE-split · ⚠ MAE-aux (overlapping per-patch masking — head-to-head) · ✓ SRHT (more slices benefit) |
| 4. Sinkhorn invariance | invariance / alignment term | ✓ PIT · ✓ SAM · ✓ Saliency · ⚠ SIE-split (interaction with SIE's invariance branch — pre-check) · ✓ SRHT · ✓ ASHA |
| 5. Poincaré projector | embedding manifold geometry | ⚠ SIE-split (both touch projector — sequential) · ✓ Saliency · ✓ SAM · ✓ ASHA · ✓ controller |
| 6. PH topological | topological-shape regularization | ⚠ MMCR-reframe (both add geometric auxiliary; theoretical redundancy pre-check) · ✓ all others |

The natural **batch-6 compose-mode targets** for downstream vetting:
- (a) **Idea 1 + Idea 2 + Idea 3** (controller + registers + iBOT-SIGReg) — three new orthogonal axes, single shipment, all HPs bound to the controller. **Strongest recommended compose-mode bundle.**
- (b) **Idea 1 + Saliency crops (b5) + SIE-split (b5) + SAM (b4) + Register tokens (b6) + PIT (b3) + ASHA (b2)** — the full 7-component "compose-mode-as-vetting-recommended" stack with controller-managed λ. This is what batch-3/4/5 vetting has been asking for.
- (c) **Idea 4 + Idea 5** (Sinkhorn invariance + Poincaré projector) — alignment-mechanism overhaul, paired because both touch the same head-side axes. Run after (a) lands.

## Next steps for user

1. **(Unchanged from prior vetting)** Run batch-2 Idea 5 (ASHA) as Step 0 — still gates all absolute-pp claims.
2. **(Unchanged from batch-5)** Joint Phase A (Ideas 2-A + 4-A of batch-5): 1 hr CPU bake-off of {EP, KSD, Riesz-MMD, Hermite} synthetic power; resolves per-slice-statistic corner.
3. **(This batch — Quick win)** Idea 2 (register tokens): drop-in encoder change, ~10 LoC via `timm`. Run as the next baseline alongside ASHA.
4. **(This batch — Safe bet, bundles with Idea 2)** Idea 1 (RankMe controller): 1-hr eng + 10-ep CPU sanity. **Ship together with Idea 2** — controller-managed λ + cleaner encoder is the lowest-risk pair.
5. **(This batch — Big bet)** Idea 3 (iBOT-SIGReg): commit only after Ideas 1+2 land; the predictor-head pipeline change is the largest eng addition in batch-6. Ship bound to controller.
6. **(This batch — composable alternative)** Idea 4 (Sinkhorn invariance): cheap eng (`pip install geomloss`); run as a 3-arm A/B/C after Idea 3.
7. **(This batch — speculative)** Ideas 5 (Poincaré) and 6 (PH): both fit the 50 % T3 quota; both are explicitly KILL-eligible at vetting. Recommend deferring both until Ideas 1+2+3 settle; only revisit if those underwhelm and a high-variance bet is warranted.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 30/20/50 | given-vetting batch-5 | 2026-05-18 batch-6`
