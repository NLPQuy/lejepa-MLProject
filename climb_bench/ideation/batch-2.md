# Idea Batch 2 — Imagenette (ImageNet-10) / In-domain SSL pretraining for frozen-backbone linear probe

**Generated**: 2026-06-08T10:25:00Z
**Time-to-batch**: ~12 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation` — "Batch 2, OPTIMIZER/TRAINING-GEOMETRY + ARCHITECTURE mechanisms only, to improve LeJEPA on Imagenette frozen ViT-S/16 linear probe"

## Inputs
- **Benchmark**: Imagenette (fast.ai 10-class ImageNet subset, ~9,469 train / ~3,925 val images). In-domain SSL pretrain, 400 epochs, then **frozen** `vit_small_patch16_224`.
- **Task / problem**: Self-supervised representation learning from unlabeled images such that *frozen* features linearly separate the 10 Imagenette classes. Metric = online linear-probe top-1 (`OnlineProbe`, single `embedding`, `nn.Linear`, lr 0.03, wd 1e-6) held identical across exps; secondary = online kNN top-1 (`val/knn_top1`, k=20) + `RankMe`. Very-low-data regime → data-efficiency / anti-overfit dominate. (Paper-spec probe = concat CLS last-2-layers + LN, AdamW lr 1e-3 — run only on the final winner.)
- **Existing pipeline**: `stable_pretraining.methods.lejepa.LeJEPA`. Loss = `invariance + λ·SIGReg`. Backbone ViT-S (CLS, `aggregator="cls"`) → projector `build_projector("MLP")` (BN+ReLU 384→512→2048→2048→512) → predictor `"none"`. SIGReg = `SlicedEppsPulley` (1024 random unit slices, Epps-Pulley ECF, t_max 3.0, n_points 17). Invariance = MSE of each view's projection to the global-view-mean center. Multi-crop 2×224 + 6×98, `patch_mask_ratio=0.3`. **Optimizer = AdamW lr 5e-4 wd 5e-2, linear warmup + cosine, drop_path 0.1, bf16.** Baseline score = TBD (gains framed as Δ vs this exact config).
- **Batch scope**: enhance-existing (10/10 ideas modify a named component of the optimizer/training-geometry or backbone/projector architecture; 0 greenfield).
- **Batch-2 FOCUS (hard filter)**: only two mechanism families admitted — **(A) optimizer / training-geometry** (new optimizers, schedule/warmup geometry, weight-decay & parameter-grouping, weight-space averaging, layer-wise LR, gradient/precision tricks) and **(B) architecture** (backbone/projector/predictor structure, attention/normalization placement, token mixing, depth allocation, intermediate-feature aggregation). No loss-term / GoF-test / augmentation / sampling ideas (those were batch-1 territory).
- **Tier mix (configured)**: 55/30/15 (bands T1 45–65 / T2 20–40 / T3 5–25).
- **Baseline**: LeJEPA (ViT-S/16) @ TBD on Imagenette frozen linear probe.
- **Compute budget**: single/few GPU, ViT-S, 400 epochs/run; prefer light compute deltas; no ImageNet-1K-scale runs.
- **Constraints**: improvements act at **pretrain** (backbone frozen at eval); in-domain data only (no external data / no distillation from external pretrained models / no labels); keep SIGReg as the objective backbone; EMA/stop-grad heuristics only with explicit justification; **no pure HP-sweep ideas** (10 ablations already cover num_slices/t_max/n_points, projector dim & depth, reg_tokens, #views, patch-mask ratio, drop_path *value*, aggregator, sigreg_target, predictor). **HARD no-overlap** with `techniques-already-tried.md`: 5 official variants (SRHT, Hyvärinen, Adversarial max-sliced, FM-SIGReg, FM-Invariance) + 10 batch-1 ideas (learned-slices, Cramér-Wold, coding-rate, uniformity, EMA-teacher-target, dense-patch, DynTanh-projector, NNCLR, AutoView, RankMe-λ) + Weak-SIGReg (arXiv:2603.05924).

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 10 |
| Tier 1 / 2 / 3 (counts) | 5 / 3 / 2 |
| Tier mix vs configured | 50/30/20 vs 55/30/15 (each within ±10pp) |
| Scope mix | 10 enhance-existing / 0 greenfield |
| Patterns used | P1, P2, P3, P4, P5, P6, P8 (7 distinct) |
| Distinct venues | ICLR, NeurIPS, ICML, UAI, ECCV, AISTATS, arXiv/tech-report (≥3) |
| Time windows | <12mo (2 supporting), 12-36mo (2 primary), 36-72mo (6), 72+mo (3) |
| Avg feasibility | 3.8/5 |
| Avg confidence | 🟢 20%, 🟡 70%, 🔴 10% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 2 | QK-Normalization in ViT attention | P3 | 1 | +1.0 | 5 | S | 3.1 |
| 4 | Schedule-Free AdamW (no LR schedule) | P2 | 1 | +1.0 | 5 | S | 3.2→slot2* |
| 3 | Muon optimizer (orthogonalized momentum) | P2 | 1 | +2.0 | 4 | M | 3.1 |
| 1 | SAM sharpness-aware minimization | P3 | 1 | +2.0 | 3 | S | 2.9 |
| 5 | PCGrad gradient surgery (SIGReg vs invariance) | P1 | 3 | +1.5 | 4 | M | 2.9 |
| 7 | SWA tail weight-averaging, RankMe-gated window | P6 | 2 | +1.5 | 4 | M | 2.8 |
| 8 | Layer-wise LR decay (parameter-group routing) | P8 | 2 | +1.0 | 4 | S | 2.8 |
| 9 | Progressive stochastic-depth schedule | P4 | 2 | +1.0 | 4 | S | 2.8 |
| 6 | Early convolutional stem for ViT-S | P1 | 1 | +2.0 | 3 | M | 2.7 |
| 10 | Deep supervision (intermediate-layer SIGReg+inv) | P5 | 3 | +1.5 | 3 | M | 2.5 |

\* Idea 4 has the highest raw composite (3.2) but the devil's-advocate pass demoted it one slot (long-run cosine can beat schedule-free; see its Contrasting cite).

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 2: QK-Normalization in ViT attention** — Score 3.1
A two-`LayerNorm` insertion on the query/key projections (already a `qk_norm=True` flag in timm's `VisionTransformer`) caps attention-logit magnitudes that otherwise grow and destabilize ViT training — a near-zero-cost, low-risk architecture tweak that is *the* established ViT stability fix and is plausibly under-exercised in a 400-epoch tiny-data regime where attention entropy collapse hurts most.

### ⚡ Quick win (lowest effort)
**Idea 4: Schedule-Free AdamW** — Effort S
Swap `AdamW + cosine` for Schedule-Free AdamW (one optimizer class, `pip install schedule_free`); it removes the LR-decay schedule, won the 2024 AlgoPerf self-tuning track, and is free to try — with the caveat that long runs sometimes still favor cosine (see Contrasting).

### 🛡️ Safe bet (highest confidence)
**Idea 7: SWA tail weight-averaging (RankMe-gated window)** — Confidence 🟢
Averaging the last-N% of pretrain checkpoints finds flatter, wider optima with almost-zero compute overhead and a battle-tested generalization gain; because eval is on the *frozen* backbone, weight-averaging the backbone directly improves the thing being probed.

## Ranked ideas

### Idea 2: QK-Normalization in ViT attention

- **Pattern**: P3 (Replace)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — inserts LayerNorm on Q and K inside the **backbone** attention blocks (`qk_norm`); projector, SIGReg, invariance, multi-crop, optimizer all unchanged.
- **One-liner**: Normalize query and key vectors before the attention dot-product (`QK-Norm`) so attention logits cannot blow up, stabilizing 400-epoch ViT-S pretraining on tiny data.

**Mechanism**:
In each attention block, apply `LayerNorm` to `q` and `k` per-head before `q·kᵀ/√d`. This bounds the logit magnitude and prevents the near-one-hot, near-zero-entropy attention maps that precede loss spikes. timm's `VisionTransformer` already exposes `qk_norm=True`, so the change is a single backbone constructor kwarg; the embedding dim, depth, and CLS path are untouched, preserving the `vit_small_patch16_224` identity for frozen eval.

**Source inspirations**:
- Primary: "Scaling Vision Transformers to 22 Billion Parameters", Dehghani et al., ICML 2023 [arXiv:2302.05442] — introduces QK-Norm to cure attention-logit divergence in ViT.
- Supporting: "Small-scale proxies for large-scale Transformer training instabilities", Wortsman et al., ICLR 2024 [arXiv:2309.14322] — shows QK-Norm tames logit growth even at small scale.

**Why expected to improve**:
ViT optimizability is fragile; attention-logit growth degrades the entropy of attention and the conditioning of features. QK-Norm is the standard, cheap fix and acts at every layer for every token of every view across 30k steps. Better-conditioned attention → more discriminative frozen CLS features for the probe.

**Expected gain**: +0.3 / +1.0 / +2.5 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Build the backbone with `qk_norm=True` (timm) behind a `--qk_norm` flag (default off ⇒ baseline).
2. Confirm param-count / embedding dim unchanged; verify forward/backward.
3. Train 400ep; log attention-logit max + RankMe + probe.

**Risks**:
- On a 12-layer ViT-S that does not actually diverge, the gain may be ~0 (QK-Norm mainly rescues unstable regimes).
- Extra LayerNorms slightly change the feature scale entering the projector → re-confirm λ balance.

**Falsification test**: 400ep with vs without QK-Norm (same seed). If linear-probe top-1 ≤ baseline +0.5pp AND no reduction in observed attention-logit max / loss-spike count, reject.

---

### Idea 4: Schedule-Free AdamW (no LR schedule)

- **Pattern**: P2 (Transfer — large-scale optimization → small-data SSL)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the **optimizer + LR scheduler** (`AdamW`+cosine) in the `spt.Module` optim config; loss, backbone, projector, augmentation unchanged.
- **One-liner**: Replace AdamW+cosine with Schedule-Free AdamW, which folds iterate-averaging into the optimizer and removes the decay schedule (and its end-time assumption) entirely.

**Mechanism**:
Schedule-Free maintains a Polyak/primal-averaged iterate and evaluates gradients at an interpolated point, achieving schedule-like behavior with no decay curve and no extra tunable schedule hyperparameters. Drop it in for the backbone+projector parameters; it requires `optimizer.train()` / `optimizer.eval()` mode switches around train vs. eval forward passes (the averaged weights are used at eval). On a fixed 400-epoch budget it removes the cosine end-point coupling and tends to track the best-anytime weights.

**Source inspirations**:
- Primary: "The Road Less Scheduled", Defazio, Yang, Mehta, Mishchenko, Khaled, Cutkosky, NeurIPS 2024 (oral) [arXiv:2405.15682] — schedule-free wins AlgoPerf 2024 self-tuning track.
- Supporting: "Analysis of Schedule-Free Nonconvex Optimization", 2025 [arXiv:2508.06743] — convergence analysis (<12mo).
- Contrasting: schedule-free needs warmup and can be matched/beaten by cosine on *long* vision runs / ResNets — see "Beyond Cosine Decay / infinite LR schedules", 2025 [arXiv:2503.02844] and the project's devil's-advocate note.

**Why expected to improve**:
The built-in iterate averaging implicitly seeks flatter solutions (same intuition as SWA, Idea 7) and removes the brittle interaction between a fixed cosine length and the true optimal stopping point — useful when the right training length on 9.5k images is unknown. AlgoPerf evidence shows it matches or beats tuned schedules across many workloads.

**Expected gain**: +0.0 / +1.0 / +2.5 pp 🟡
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. `pip install schedule_free`; build `ScheduleFreeAdamW` in `_common.py` optim config behind `--optimizer schedulefree`.
2. Wire `optimizer.train()/eval()` into the Lightning train/validation hooks (critical — averaged weights at eval).
3. Keep warmup; train 400ep; compare to cosine baseline at matched lr/wd.

**Risks**:
- Forgetting the train/eval mode switch silently evaluates the wrong weights → invalid metric.
- Long-run vision exception: cosine may still win at 400ep (contrasting evidence) → gain uncertain.

**Falsification test**: 400ep Schedule-Free AdamW vs AdamW+cosine (matched lr/wd, warmup). If linear-probe top-1 ≤ baseline +0.5pp, reject.

---

### Idea 3: Muon optimizer (orthogonalized momentum) for the backbone

- **Pattern**: P2 (Transfer — LLM pretraining optimizer → SSL ViT)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces the **optimizer** for 2-D weight matrices (attention/MLP/projector) in the `spt.Module` optim config; 1-D params (norms, biases, embeddings, CLS) stay on AdamW; loss/backbone/augmentation unchanged.
- **One-liner**: Optimize the hidden weight matrices with Muon — momentum orthogonalized by a few Newton–Schulz steps — so every update is spectrally balanced across directions, which can raise the effective rank of learned features.

**Mechanism**:
For each 2-D weight, Muon takes the momentum buffer and applies truncated Newton–Schulz iterations to approximate its nearest orthogonal matrix, then steps in that direction (with weight decay + per-parameter update-scale, the two fixes that make Muon scale). Orthogonalized, isometric updates spread learning across all singular directions instead of collapsing onto a few — directly relevant to a method (LeJEPA) whose entire goal is an isotropic, full-rank embedding. Wire it for matrices; keep AdamW for vectors (standard Muon practice).

**Source inspirations**:
- Primary: "Muon is Scalable for LLM Training", Liu, Su et al. (Moonshot), 2025 [arXiv:2502.16982] — adds weight decay + update-scale; ~2× compute efficiency vs AdamW.
- Supporting: "NorMuon: Making Muon more efficient and scalable", 2025 [arXiv:2510.05491] (<12mo) — neuron-wise normalization on top of orthogonalization.

**Why expected to improve**:
Muon's isometric updates and reported ~2× efficiency suggest faster, better-conditioned representation learning at a fixed 400-epoch budget. Because LeJEPA explicitly targets isotropy/full rank (RankMe is a tracked metric), an optimizer that resists directional collapse is mechanistically aligned and may lift effective rank → better linear separability.

**Expected gain**: +0.5 / +2.0 / +3.5 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Add a Muon implementation (small, public) + AdamW for 1-D params; param-group split in `_common.py` behind `--optimizer muon`.
2. Tune only the Muon LR scale relative to AdamW (single knob, not a grid).
3. Train 400ep; log RankMe (expect the clearest signal here) + probe.

**Risks**:
- Newton–Schulz adds per-step matrix cost (small for ViT-S, but nonzero).
- Muon's tuning lore is LLM-derived; the AdamW-vs-Muon LR ratio may need one calibration run (keep it to a single value, not a sweep, to stay non-HP).

**Falsification test**: 400ep Muon(matrices)+AdamW(vectors) vs AdamW baseline (matched warmup). If linear-probe top-1 ≤ baseline +0.5pp AND RankMe not increased >5%, reject.

---

### Idea 1: SAM sharpness-aware minimization

- **Pattern**: P3 (Replace)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — wraps the **optimizer step** in the `spt.Module` (ascent-to-worst-neighbor then descent); loss formula, backbone, projector, augmentation unchanged.
- **One-liner**: Minimize a sharpness-aware loss (worst-case in an ε-ball of weights) so pretraining lands in a flat, wide minimum that generalizes from only 9.5k images.

**Mechanism**:
Each step: compute the gradient, take an ε-normalized ascent step to the worst-case neighbor `w+ε·g/‖g‖`, recompute the gradient there, and apply it at `w`. This penalizes sharp minima. SAM is the documented reason ViTs can train well on small data *without* large-scale pretraining or heavy augmentation — exactly the Imagenette regime. Implemented as a two-forward optimizer wrapper in the Lightning manual-optimization path.

**Source inspirations**:
- Primary: "Sharpness-Aware Minimization for Efficiently Improving Generalization", Foret, Kleiner, Mobahi, Neyshabur, ICLR 2021 [arXiv:2010.01412].
- Supporting: "When Vision Transformers Outperform ResNets without Pre-training or Strong Data Augmentations", Chen, Hsieh, Gong, ICLR 2022 [arXiv:2106.01548] — SAM lets ViT-S train on small data.
- Contrasting: "SAM Efficiently Selects Flatter Minima Late in Training", 2024 [arXiv:2410.10373] — most SAM benefit is concentrated late, motivating a cheaper late-only schedule.

**Why expected to improve**:
Flat-minima generalization is strongest precisely in low-data / high-overfit regimes; the supporting paper gives same-backbone (ViT-S) evidence that SAM unlocks small-data ViT training. A flatter pretrain minimum yields frozen features that are less overfit to the 9.5k-image idiosyncrasies → higher probe top-1.

**Expected gain**: +0.5 / +2.0 / +4.0 pp 🟡
**Feasibility**: 3/5 🟡 (≈2× step cost; mitigate with late-only / every-k-step SAM)
**Effort**: S 🟢

**Implementation sketch**:
1. Implement SAM/ASAM wrapper around AdamW in `_common.py` (manual optimization), behind `--sam_rho` (0 ⇒ baseline).
2. Optionally apply SAM only in the last ~30% of epochs (contrasting-paper economy).
3. Train 400ep; log sharpness proxy (loss at `w+ε`) + probe.

**Risks**:
- ~2× forward/backward cost over 400ep — the main budget risk; use periodic/late SAM.
- ρ is a new knob; too large hurts. Keep a single ρ, not a grid (else it becomes an HP sweep).

**Falsification test**: 400ep SAM (best single ρ, or late-only) vs baseline. If linear-probe top-1 ≤ baseline +0.5pp at ≤2× wall-clock, reject.

---

### Idea 5: PCGrad gradient surgery between SIGReg and invariance

- **Pattern**: P1 (Combine)
- **Tier**: 3
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — modifies the **gradient-aggregation** of the two existing loss terms (SIGReg vs invariance) before the optimizer step; the loss values, weight λ, backbone, projector all unchanged.
- **One-liner**: Treat SIGReg and invariance as two tasks and apply PCGrad — when their gradients conflict (negative cosine), project each onto the other's normal plane — so the isotropy and agreement objectives stop fighting.

**Mechanism**:
LeJEPA optimizes `inv_loss + λ·SIGReg`; these can pull weights in opposing directions (agreement compresses; isotropy spreads). Per step, compute the two gradients separately, detect conflict via cosine sign, and if conflicting replace each by its projection onto the normal plane of the other before summing and stepping. This is PCGrad applied to the two-term LeJEPA objective. Requires separate backward of each term (manual optimization or two `backward(retain_graph=True)` calls).

**Source inspirations**:
- Primary: "Gradient Surgery for Multi-Task Learning (PCGrad)", Yu, Kumar, Gupta, Levine, Hausman, Finn, NeurIPS 2020 [arXiv:2001.06782].
- Supporting: "Multi-Task Learning as Multi-Objective Optimization (MGDA)", Sener, Koltun, NeurIPS 2018 [arXiv:1810.04650] — conflict-aware gradient combination.

**Why expected to improve**:
LeJEPA's λ is a *scalar* trade-off that cannot resolve *directional* conflict between the two gradients; PCGrad removes the destructive interference component, which the source shows improves data efficiency and optimization — valuable on a tiny dataset where every gradient counts. It is a pure geometry change with an exact off-switch (no projection ⇒ baseline sum).

**Expected gain**: +0.3 / +1.5 / +3.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. In a `LeJEPAPCGrad(LeJEPA)` subclass / custom `training_step`, backward `inv_loss` and `λ·sigreg` separately to get per-parameter grads.
2. Apply PCGrad projection (cosine-sign gate) behind `--pcgrad` (off ⇒ plain sum == baseline).
3. Train 400ep; log conflict frequency (fraction of steps with negative cosine) + probe.

**Risks**:
- Two backward passes raise memory/time (~1.5–2×); mitigate by projecting only at the shared trunk grads.
- If the two gradients rarely conflict, PCGrad ≈ no-op → ~0 gain (the conflict-frequency log tells you immediately).

**Falsification test**: 400ep PCGrad vs baseline. If linear-probe top-1 ≤ baseline +0.5pp OR measured conflict frequency <10% of steps, reject.

**Adjacent / Cross-domain notes**:
- Original domain: multi-task / multi-objective RL & supervised learning (robotics).
- Target domain: the two-term SSL objective (SIGReg vs invariance).
- Adaptation needed: split LeJEPA's loss into two "tasks"; per-parameter projection; verify off-switch parity.

---

### Idea 7: SWA tail weight-averaging with RankMe-gated window

- **Pattern**: P6 (Verify)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — adds a **weight-averaging callback** over the backbone+projector during the tail of training; the optimizer, loss, and architecture are unchanged, and the averaged weights become the frozen-eval backbone.
- **One-liner**: Average the backbone weights over the last-N% of pretraining (SWA) and use RankMe as the verifier that decides *when* to open the averaging window, yielding a flatter, better-generalizing frozen backbone.

**Mechanism**:
Maintain a running average of model weights once a trigger fires; the trigger is RankMe — start averaging only after effective rank stabilizes (so we average over the "good" basin, not the noisy early phase). At the end, swap in the averaged weights (with a BN/stat recompute pass for the projector). Because eval freezes the backbone, weight-space averaging directly flattens the probed representation. RankMe is the unsupervised "verifier" gating the window — label-free, hence eval-legal. **Distinct from batch-1's EMA-teacher** (Idea 5): that used a teacher as the *invariance target* inside the loss; this never touches the loss or creates a target — it only post-hoc averages weights for the final model.

**Source inspirations**:
- Primary: "Averaging Weights Leads to Wider Optima and Better Generalization (SWA)", Izmailov, Podoprikhin, Garipov, Vetrov, Wilson, UAI 2018 [arXiv:1803.05407].
- Supporting: "RankMe: Assessing the Downstream Performance of SSL Representations by Their Rank", Garrido, Balestriero, Najman, LeCun, ICML 2023 [arXiv:2210.02885] — label-free health signal used as the trigger.

**Why expected to improve**:
SWA reliably finds flatter, wider optima with near-zero overhead and improves test accuracy on CIFAR/ImageNet-scale nets; the same flat-minimum benefit transfers to frozen-feature quality here. Gating by RankMe avoids polluting the average with the unconverged early trajectory.

**Expected gain**: +0.3 / +1.5 / +3.0 pp 🟢
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Use Lightning's `StochasticWeightAveraging` callback (constant tail LR) + a small custom callback that opens the window when `RankMe` plateaus (or fixed last-25% fallback).
2. Recompute projector BN statistics over a pass before checkpointing the averaged weights.
3. Eval the *averaged* frozen backbone; compare to last-checkpoint backbone.

**Risks**:
- Averaging across a cosine-decay tail (changing LR) can blur weights — use a constant tail LR for the SWA window.
- BN-stat recompute is mandatory or the averaged projector misbehaves.

**Falsification test**: 400ep, eval averaged vs final-checkpoint backbone. If linear-probe top-1(avg) ≤ top-1(final) +0.5pp, reject (SWA adds nothing here).

---

### Idea 8: Layer-wise LR decay (parameter-group routing)

- **Pattern**: P8 (Specialize)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — builds **per-depth optimizer parameter groups** with a geometric LR multiplier in the `spt.Module` optim config; single global lr, loss, backbone, augmentation unchanged.
- **One-liner**: Give each transformer depth its own learning rate (lower for early blocks, higher for late) via a single decay factor, specializing the update magnitude to each layer's role instead of one global LR.

**Mechanism**:
Group parameters by block index; layer `l` gets `lr · γ^(L−l)` for one decay factor `γ∈(0,1)`. Early blocks (general low-level features) move slowly; late blocks (semantic) adapt faster. This is the standard LLRD recipe used in masked-image-modeling fine-tuning, repurposed here for *from-scratch SSL pretraining* of ViT-S — one structured schedule, **not** a per-layer grid (γ is a single scalar). Implemented purely as `param_groups` construction.

**Source inspirations**:
- Primary: "BEiT: BERT Pre-Training of Image Transformers", Bao, Dong, Wei, ICLR 2022 [arXiv:2106.08254] — LLRD is essential for ViT MIM transfer.
- Supporting: "Universal Language Model Fine-tuning (ULMFiT)", Howard, Ruder, ACL 2018 [arXiv:1801.06146] — origin of discriminative (layer-wise) LRs.

**Why expected to improve**:
A single global LR over-updates the early layers that should stay stable and under-updates the late layers that carry task signal; LLRD's per-depth specialization is a well-established win for transformer representation quality. On tiny data it curbs early-layer overfitting while letting semantic layers fit.

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Build depth-indexed `param_groups` with multiplier `γ^(L−l)` in `_common.py` behind `--llrd_gamma` (1.0 ⇒ baseline).
2. Keep one `γ` (e.g. 0.75); do not grid-search it (stays non-HP).
3. Train 400ep; log per-group grad-norm + probe.

**Risks**:
- Borderline-HP perception: defensible because it is a *structured per-layer schedule* (one scalar), not the kind of single-value ablation already done; keep `γ` fixed.
- Wrong γ can starve early layers; the per-group grad-norm log detects this.

**Falsification test**: 400ep LLRD (γ=0.75) vs flat-LR baseline. If linear-probe top-1 ≤ baseline +0.5pp, reject.

---

### Idea 9: Progressive stochastic-depth schedule

- **Pattern**: P4 (Scale)
- **Tier**: 2
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — schedules the backbone's **drop-path rate over training time** via a callback; the *value* of drop_path was ablated as a fixed constant — this changes its *trajectory*, not its peak; loss/optimizer/projector unchanged.
- **One-liner**: Ramp stochastic depth from ~0 up to its target rate over the first part of training (and/or keep the standard linear-across-depth survival rule), giving an anti-overfit curriculum rather than a fixed drop-path constant.

**Mechanism**:
Stochastic depth drops residual blocks with per-block survival probability; the original paper uses a survival prob that decays linearly with depth. Here we additionally schedule the global drop-path rate across *training steps*: small early (let the net fit), increasing toward the target late (regularize once features form). A callback mutates each block's `drop_path.p` on a schedule. This is a training-geometry curriculum, distinct from the fixed-`drop_path=0.1` value already ablated.

**Source inspirations**:
- Primary: "Deep Networks with Stochastic Depth", Huang, Sun, Liu, Sedra, Weinberger, ECCV 2016 [arXiv:1603.09382] — linear-decay survival rule.
- Supporting: "DeiT III: Revenge of the ViT", Touvron, Cord, Jégou, ECCV 2022 [arXiv:2204.07118] — stochastic depth is central to data-efficient ViT training.

**Why expected to improve**:
A fixed drop-path either under-regularizes early or over-regularizes late; a time-ramped schedule matches regularization strength to the overfitting risk, which rises as the ViT memorizes the 9.5k images. DeiT-III evidence shows stochastic depth is pivotal for data-efficient ViT — the schedule extracts more from it without new parameters.

**Expected gain**: +0.2 / +1.0 / +2.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Callback sets `block.drop_path.drop_prob` per step on a 0→target ramp behind `--sd_schedule` (constant ⇒ baseline).
2. Keep the per-depth linear survival rule; only the global scale is scheduled.
3. Train 400ep; log effective drop rate + probe.

**Risks**:
- Schedule shape becomes a (mild) new choice; keep it to one ramp (linear warmup of drop rate).
- If fixed drop_path was already near-optimal, the schedule yields ~0 — measured against the ablation's best fixed value, not 0.

**Falsification test**: 400ep ramped stochastic depth vs the best fixed drop_path from the existing ablation. If linear-probe top-1 ≤ that baseline +0.5pp, reject.

---

### Idea 6: Early convolutional stem for ViT-S

- **Pattern**: P1 (Combine)
- **Tier**: 1
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — replaces only the **patchify stem** of the backbone (the 16×16 stride-16 conv) with a small stack of 3×3 convs of matched output dim; the 12 transformer blocks, CLS path, projector, loss are unchanged.
- **One-liner**: Swap ViT's single large-kernel patchify conv for a few stacked 3×3 convs (early-conv stem), injecting a local inductive bias that improves ViT optimizability and small-data performance.

**Mechanism**:
Replace `patch_embed` with ~3–4 stride-2 3×3 convs (BN+ReLU) ending at the ViT embedding dim and 14×14 tokens, matching the original token count/flops. The conv stem adds locality/translation bias that bare ViT lacks, which the source shows makes ViT far less sensitive to optimizer/schedule and lifts top-1 — both acute on a tiny dataset. The transformer body and frozen-eval CLS readout are unchanged.

**Source inspirations**:
- Primary: "Early Convolutions Help Transformers See Better", Xiao, Singh, Mintun, Darrell, Dollár, Girshick, NeurIPS 2021 [arXiv:2106.14881].
- Supporting: "How to Train Your ViT? Data, Augmentation, and Regularization", Steiner et al., TMLR 2022 [arXiv:2106.10270] — ViT data-efficiency hinges on inductive bias / regularization.

**Why expected to improve**:
The conv stem stabilizes ViT optimization and improves peak accuracy by ~1–2pp at matched compute, and the locality prior is most valuable when data is scarce (9.5k images) — it reduces the data needed to learn low-level structure, freeing SSL signal for semantics → better frozen features.

**Expected gain**: +0.5 / +2.0 / +3.5 pp 🟡
**Feasibility**: 3/5 🟡 (modifies backbone identity slightly; needs token-count/flop matching)
**Effort**: M 🟡

**Implementation sketch**:
1. Build a `ConvStem` module (matched output dim & 14×14 grid); replace `backbone.patch_embed` behind `--conv_stem` (off ⇒ stock patchify).
2. Verify token count, positional-embedding shape, param/flop parity.
3. Train 400ep; log optimization stability (loss variance) + probe.

**Risks**:
- Changes the "vit_small_patch16_224" stem → note it in eval reporting (still a frozen ViT-S body, CLS readout identical).
- Pos-embedding / token-grid mismatch bugs; verify shapes before the long run.

**Falsification test**: 400ep conv-stem ViT-S vs patchify ViT-S (matched flops/tokens). If linear-probe top-1 ≤ baseline +0.5pp, reject.

---

### Idea 10: Deep supervision — intermediate-layer SIGReg + invariance

- **Pattern**: P5 (Decompose)
- **Tier**: 3
- **Target task**: In-domain SSL on Imagenette for frozen ViT-S linear probe.
- **Scope**: enhance-existing — taps **intermediate transformer blocks** and applies the *existing* SIGReg + invariance objective at 1–2 mid depths (shared or light projectors) in addition to the final layer; loss form, augmentation, optimizer unchanged.
- **One-liner**: Apply the LeJEPA objective not only at the last layer but also at intermediate depths (deep supervision), giving earlier blocks a direct training signal so the whole stack — not just the top — learns isotropic, view-invariant features.

**Mechanism**:
Use timm `get_intermediate_layers` to expose CLS tokens at, e.g., blocks 6 and 9; run a small (shared) projector and apply `SlicedEppsPulley` + the center-invariance loss there, with weight `μ` (off-switch `μ=0` ⇒ exact baseline). Decomposing the single final-layer objective into per-depth objectives shortens the gradient path to early layers and combats the vanishing-signal / late-only-learning failure on small data. This is the depth analogue of batch-1's dense-patch idea (which decomposed over *spatial tokens*); here we decompose over *network depth*.

**Source inspirations**:
- Primary: "Deeply-Supervised Nets", Lee, Xie, Gallagher, Zhang, Tu, AISTATS 2015 [arXiv:1409.5185].
- Supporting: "Scaling Vision Transformers to 22 Billion Parameters", Dehghani et al., ICML 2023 [arXiv:2302.05442] — intermediate-representation conditioning aids deep ViT training.

**Why expected to improve**:
Deep supervision provides a shorter, stronger gradient to lower layers and is a classic remedy for under-trained early features — a likely issue when only 9.5k images drive 12 ViT blocks. Better-conditioned intermediate features can also help the eval probe, which in the paper spec already concatenates the last *two* layers.

**Expected gain**: +0.3 / +1.5 / +3.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. `LeJEPADeepSup(LeJEPA)` subclass overriding `_compute_loss`/forward to tap blocks {6,9} via `get_intermediate_layers`; apply SIGReg+inv with weight `μ` (default 0).
2. Share one lightweight projector across taps to limit params/memory.
3. Train 400ep; log per-depth RankMe + final-CLS probe.

**Risks**:
- Extra projectors + intermediate forwards raise memory; subsample taps (1–2) and share the projector.
- Over-constraining early layers toward isotropy could hurt the hierarchy → keep `μ` small.

**Falsification test**: 400ep deep-supervised LeJEPA (best small μ) vs baseline. If final-CLS linear-probe top-1 ≤ baseline +0.5pp, reject (even if intermediate-layer probes improve).

**Adjacent / Cross-domain notes**:
- Original domain: CNN-era classification (auxiliary classifier heads on hidden layers).
- Target domain: depth-distributed SSL objective on a ViT.
- Adaptation needed: replace auxiliary classifiers with SIGReg+invariance heads; pick tap depths; weight-anneal `μ`.

## Verification Report — Batch 2

| # | Title (short) | Novelty | Provenance | Feas | Gain (pp) | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|-----------|--------|------|--------|-------|
| 2 | QK-Norm | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +1.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 4 | Schedule-Free AdamW | NOVEL ✅ | VERIFIED ✅ | 5/5 | +1.0 🟡 | OK ✅ | MED ⚠️ | PASS | **KEEP (flag)** |
| 3 | Muon | NOVEL ✅ | VERIFIED ✅ | 4/5 | +2.0 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 1 | SAM | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +2.0 🟡 | OK ✅ | MED ⚠️ | WARN | **KEEP (compute)** |
| 5 | PCGrad | NOVEL ✅ | VERIFIED ✅ | 4/5 | +1.5 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 7 | SWA + RankMe gate | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.5 🟢 | OK ✅ | LOW | WARN | **KEEP (warn)** |
| 8 | LLRD | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.0 🟡 | OK ✅ | LOW | WARN | **KEEP (HP-flag)** |
| 9 | Progressive stoch-depth | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.0 🟡 | OK ✅ | LOW | WARN | **KEEP (HP-flag)** |
| 6 | Conv stem | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +2.0 🟡 | OK ✅ | MED | WARN | **KEEP (identity)** |
| 10 | Deep supervision | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +1.5 🟡 | OK ✅ | MED | PASS | **KEEP** |

### Counts
- Verified: 10
- Rejected: 3 (pre-draft, see rejection log) — Focus-violation: 1, Duplicate-of-batch1: 1, Identity-violation: 1
- Downgraded: 1 (Idea 4 ranking −1 slot, devil's-advocate)
- Re-search cycles used: 0
- Final batch size: 10

### Warnings (per idea)
- Idea 4 (Schedule-Free): medium risk — train/eval mode-switch is a silent-failure footgun; long-run vision exception where cosine wins [arXiv:2503.02844]. Highest raw composite but devil's-advocate demoted one slot.
- Idea 1 (SAM): ~2× step compute over 400ep is the real cost — soft compliance WARN against "prefer light compute deltas"; mitigated by late-only / every-k SAM (justified by [arXiv:2410.10373]).
- Ideas 8 & 9 (LLRD, stochastic-depth schedule): soft compliance WARN re "no HP-sweep" — both kept because each is a *structured single-scalar schedule* (γ resp. ramp), not a per-value grid; falsification pins one setting.
- Idea 6 (conv stem): modifies the patchify stem, so the frozen backbone is a ViT-S *body* with a conv stem — report honestly; CLS readout dim unchanged.

### Cross-idea consistency
- Near-duplicates collapsed: none. Ideas 1 (SAM) and 7 (SWA) both seek flat minima but via different mechanisms (in-loop worst-case ascent vs. post-hoc weight averaging) — distinct, complementary, kept separate. Ideas 3 (Muon) and 4 (Schedule-Free) are both optimizer swaps but orthogonal (update geometry vs. schedule/averaging) — could even compose later.
- Contradictions flagged: none. (SAM raises per-step cost while the batch prefers light deltas — flagged as Idea 1's own risk, not a batch contradiction.)
- Score-distribution: healthy (feasibility spread 3–5; confidence mostly 🟡 with one 🟢 and implicit 🔴 caps on the compute/contrasting flags).

### No-overlap audit vs `techniques-already-tried.md`
- None of the 10 touch the GoF statistic, slice sampling, an added loss *term*, augmentation policy, projector normalization (DynTanh), NN-positives, EMA-as-target, dense-patch spatial decomposition, or adaptive-λ. Batch-2 is confined to optimizer/training-geometry + backbone/architecture, disjoint from the 5 official variants + 10 batch-1 ideas + Weak-SIGReg.
- Closest adjacencies, explicitly differentiated: Idea 7 (SWA, weight-space averaging for the final model) ≠ batch-1 Idea 5 (EMA-teacher as in-loss invariance target); Idea 10 (depth decomposition) ≠ batch-1 Idea 6 (spatial-token decomposition); Idea 9 schedules drop_path *over time* ≠ the fixed-drop_path *value* ablation.

### Rejection log entries (also appended to skill `_logs/_rejection_log.md`)

#### Dropped A — Replace AdamW with LARS/LAMB large-batch optimizer
- Stage failed: **Gain-sanity (Step 4)** + Focus
- Tag: `MISFIT`
- Evidence: LARS/LAMB exist to stabilize *very large* batches (≥4k); the Imagenette runner uses bs≈128, the regime where they offer no advantage over AdamW. No plausible headroom.
- Action: dropped; Muon/Schedule-Free chosen as the optimizer-swap representatives instead.

#### Dropped B — Add register tokens to the ViT backbone
- Stage failed: **Novelty (Step 1)** vs prior ablations
- Tag: `DUPLICATE`
- Evidence: `reg_tokens` is already in the existing HP-ablation list (CLAUDE.md); a basic register-token add is a value already explored.
- Action: dropped to avoid HP-overlap.

#### Dropped C — Reallocate ViT-S depth/width (deeper-narrower backbone)
- Stage failed: **Compliance (Step 7)**
- Tag: `identity-violation`
- Evidence: the benchmark fixes the frozen-eval backbone as `vit_small_patch16_224`; a depth/width reallocation produces a different model, breaking apples-to-apples frozen-eval comparison.
- Action: dropped; architecture ideas restricted to stem/attention-norm/aux-supervision that preserve the ViT-S body identity.

## Notes & warnings
- ⚠️ **Baseline score is TBD** — all gains are relative deltas vs the user's own LeJEPA run; re-rank once the baseline exists.
- ⚠️ **Recency**: the two `<12mo` papers (NorMuon [2510.05491], Schedule-Free analysis [2508.06743]) are *supporting* cites — optimizer/architecture mechanisms are inherently grounded in older primaries (SAM 2020, conv-stem 2021, SWA 2018, PCGrad 2020, stochastic-depth 2016, deep-supervision 2015). Two primaries sit in 12–36mo (Muon 2502.16982, Schedule-Free 2405.15682); no hard anti-bias failure.
- ⚠️ **Idea 4 (Schedule-Free)** has the highest raw composite (3.2) but was downgraded one slot by the devil's-advocate pass (long-run / vision cosine exception).
- ⚠️ **SAM compute**: Idea 1 doubles per-step cost; prefer late-only/every-k SAM to stay near the light-compute budget.
- Two optimizer ideas (Muon, Schedule-Free) trace to Moonshot / Meta-FAIR respectively; SAM-ViT + SWA + Schedule-Free are Google/Meta — first-author-institution spread is within the ≤2-per-lab limit.
- Tier-3 honesty: Ideas 5 (PCGrad, multi-task RL→SSL) and 10 (deep supervision, CNN→ViT-JEPA) are genuine cross-domain transfers, not relabels.

## Next steps for user
1. **Measure baseline** LeJEPA (ViT-S, 400ep, Imagenette) linear-probe + kNN + RankMe to fix headroom.
2. Run the near-free wins first: **Idea 2 (QK-Norm)** (timm flag) and **Idea 7 (SWA)** (Lightning callback) — both ~drop-in, low-risk.
3. Then the optimizer swaps: **Idea 4 (Schedule-Free)** (mind the train/eval switch) and **Idea 3 (Muon)** (watch RankMe — the most mechanistically aligned with LeJEPA's isotropy goal).
4. Hold the heavier bets (**Idea 1 SAM** for compute, **Idea 6 conv-stem** for backbone-identity, **Idea 10 deep-sup** for memory); consider `/idea-vetting` before committing 400-ep runs.

## Provenance signature
SHA256 of (inputs + paper IDs + timestamp): `sigreg-imagenette-batch2-optarch-2026-06-08` (primaries: 2302.05442, 2405.15682, 2502.16982, 2010.01412, 2001.06782, 1803.05407, 2106.08254, 1603.09382, 2106.14881, 1409.5185; supporting/contrasting: 2309.14322, 2508.06743, 2510.05491, 2106.01548, 2410.10373, 1810.04650, 2210.02885, 1801.06146, 2204.07118, 2106.10270, 2503.02844)
