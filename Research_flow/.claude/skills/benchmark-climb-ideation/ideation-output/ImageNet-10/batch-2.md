# Idea Batch 2 — ImageNet-10 / SSL embedding (LeJEPA in-domain)
**Generated**: 2026-05-18
**Time-to-batch**: ~14 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation ImageNet-10 --task "Self-supervised learning embedding training in-domain like stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py" --pipeline baseline_lejepa.md --tier-mix 55/30/15 --given-vetting vetting-output/ImageNet-10/batch-1/batch-summary.md`

## Inputs
- Benchmark: **ImageNet-10** (Imagenette — 10-class ImageNet subset; linear-probe top-1 on held-out split).
- Task: in-domain self-supervised pretraining (no external data / no foundation-model init), evaluated by frozen-backbone linear probe (concat CLS of last 2 layers + LN) — exact recipe in `stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py`.
- Existing pipeline: LeJEPA ViT-S/16 + SIGReg (`EppsPulley` × 1024 random slices) + invariance loss over 2 global + 6 local crops; AdamW lr=5e-4 wd=5e-2 bf16; single hyper-parameter λ. Baseline number on ImageNet-10 still **TBD** (vetting batch-1 Step-0 prerequisite).
- Batch scope: **enhance-existing** (pipeline supplied).
- Tier mix (configured): 55/30/15 — bands T1 45–65%, T2 20–40%, T3 5–25%.
- Compute / time / constraint budget: same as batch-1 (1–8 GPU, ~1 week, soft "single-λ" branding constraint).

### Given vetting (batch-1) feedback applied
- ☠️ Idea 5 (Kernel-SIGReg) was killed for breaking Cramér–Wold. Vetting suggested the **combine-multiple-univariate-tests** substrate as theory-preserving salvage → **Idea 7 in this batch** (renumbered to **Idea 1**, since it leads).
- 🔁 Idea 4 (Adaptive-λ) was reframed: do **cosine-schedule on λ** before any controller. Subsumed below in **Idea 3 (curriculum-on-test-strictness)**, which is the natural superset.
- 🔁 Idea 2 (iBOT patch-SIGReg) was reframed pending **vanilla DINOv2 measurement** — not re-proposed here (waiting on Step-0).
- The vetting note "bias toward measurement-first phrasing" → **Idea 5 (multi-fidelity HP sweep)** is exactly that: the cheapest way to convert "TBD baseline" into a real ranking.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Tier 1 / 2 / 3 (counts) | 3 / 2 / 1 |
| Tier mix vs configured | 50/33/17 vs 55/30/15 (within ±10 pp) |
| Scope mix | 6 enhance-existing / 0 greenfield (100% enhance) |
| Patterns used | P1, P3 (×2), P5, P7, P8 — 5 distinct |
| Distinct venues | 8 (arXiv, ICML, NeurIPS, TMLR, ICLR, MLSys, ICCV, JASA) |
| Time windows | <12 mo: 3 · 12–36 mo: 1 · 36–72 mo: 2 · classics: 4 |
| Avg feasibility | 4.5 / 5 |
| Avg confidence | 🟢 50% · 🟡 50% · 🔴 0% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------------|------|--------|-------|
| 1 | Stacked univariate tests in SIGReg (theory-preserving) | P1 | 1 | +1.2 | 5 | S | **3.2** |
| 5 | Multi-fidelity HP sweep (ASHA over λ, lr, wd) | P7 | 3 | +1.5 | 5 | S | **3.2** |
| 3 | Test-strictness curriculum (Moments → EppsPulley) | P5 | 2 | +1.0 | 4 | S | 2.9 |
| 4 | LARS / LAMB optimizer for small-batch SSL | P3 | 1 | +0.8 | 5 | S | 2.9 |
| 2 | Sliced-Wasserstein-2 statistic instead of Epps–Pulley | P3 | 1 | +1.0 | 4 | M | 2.7 |
| 6 | Two-pass self-distillation across LeJEPA checkpoints | P8 | 2 | +1.5 | 3 | M | 2.7 |

Composite = `0.4·Gain + 0.3·Feas + 0.2·EffortInv + 0.1·Novelty` (Gain normalised /5; S=4 M=3 L=2).

## Top-3 recommendations

### 🏆 Top-1 by composite score (tie) — **Big bet**
**Idea 1: Stacked univariate tests in SIGReg.** Sum of EppsPulley + AndersonDarling + Watson on the same slice. All three already live in `lejepa.univariate`; Cramér–Wold is preserved (each test's null is N(0,1), so the sum is zero iff the projection is N(0,1)). No new hyperparameter if equally weighted. Salvaged substrate from killed Kernel-SIGReg.

### ⚡ Quick win — also Top-1 by composite
**Idea 5: Multi-fidelity HP sweep (ASHA) over (λ, lr, wd).** Direct response to vetting's "measurement is the bottleneck, not ideas". 8-arm ASHA at 25→50→100 epoch rungs over a 3×3×3 grid → final ranking in ≈ 30 GPU-h, fixing the baseline ranking *and* giving a defensible λ instead of the paper default. Effort S.

### 🛡️ Safe bet (highest confidence + lowest risk)
**Idea 4: LARS / LAMB optimizer.** SimCLR / BYOL / SwAV all switched to LARS specifically for small-batch SSL stability. One-line optimizer change in the Lightning `configure_optimizers`. Confidence 🟢, effort S.

---

## Ranked ideas

### Idea 1: Stacked univariate tests in SIGReg

- **Pattern**: P1 (Combine — sum several normality tests in the existing slice loop)
- **Tier**: 1
- **Target task**: same as batch.
- **Scope**: enhance-existing. Modifies `SlicingUnivariateTest.univariate_test` to accept a *list* of tests; everything else (backbone, slicing, projector, optimizer, schedule, λ) unchanged.
- **One-liner**: Per slice, evaluate `EppsPulley + AndersonDarling + Watson` and sum — three independent normality tests, all already in the library, no new λ.

**Mechanism**:
EppsPulley targets the empirical characteristic function (frequency-domain deviation). Anderson–Darling weights tail deviations of the CDF. Watson is rotation-invariant on the unit interval and catches multi-modal departures. The three tests have **near-orthogonal power profiles** (tails / body / multimodality), so their sum is a strictly more powerful normality test on each 1-D slice. Cramér–Wold lifts: every per-slice marginal vanishes iff every slice is N(0,1), iff Z is isotropic Gaussian. No new tunable weight needed at unit weighting; an optional learned weight is a stretch goal.

**Source inspirations**:
- Primary: *LeJEPA: Provable and Scalable SSL Without the Heuristics*, Balestriero & LeCun, 2025 [arXiv:2511.08544] — the paper that defines SIGReg and lists all three tests in `lejepa.univariate`.
- Supporting: *Asymptotic Theory of Certain "Goodness-of-Fit" Criteria Based on Stochastic Processes*, Anderson & Darling, *Annals of Math. Stat.* 1952 — power against tails.
- Supporting: *Goodness-of-Fit Tests on a Circle*, Watson, *Biometrika* 1961 — rotation-invariant variant of CvM.

**Why expected to improve**:
This is the **salvaged substrate** from killed Idea 5 (Kernel-SIGReg). Vetting analysis showed that "stacking two linear univariate tests dominates RFF-SIGReg theoretically and computationally" — i.e., adding statistical power *inside* the linear-slice family is the right move, not lifting to RKHS. Three tests cost ≤ 1.5× one test (tests share the slice projection — dominant cost). The extra power should help most where SIGReg is currently noisy: small-batch, small-dataset regimes like ImageNet-10.

**Expected gain**: +0.4 / +1.2 / +2.5 pp 🟢
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Extend `SlicingUnivariateTest` to accept `univariate_tests: list[UnivariateTest]`.
2. Forward each slice through all tests, sum outputs (already shape `(K,)`).
3. Re-run the canonical ImageNet-10 recipe at unit weights; ablate single vs pair vs triple.

**Risks**:
- Anderson–Darling has numerical instability at the tails for small batch — clamp via existing `EPS`.
- If EppsPulley alone is already saturated on this regime, triple adds nothing.

**Falsification test**: 100-epoch LeJEPA on ImageNet-10, 3 seeds, with `tests = {EP}` vs `{EP, AD}` vs `{EP, AD, W}`. If best triple does not beat best singleton by ≥ 0.5 pp linear-probe with non-overlapping seed CIs, the salvage was inert.

---

### Idea 5: Multi-fidelity HP sweep (ASHA) over (λ, lr, wd)

- **Pattern**: P7 (Search — successive halving over the existing knob set)
- **Tier**: 3
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds an Optuna/Ray Tune driver around the existing `train_lejepa_ablation.py`; no change to the model, loss, or data pipeline.
- **One-liner**: Replace the "trust the paper's λ=0.1, lr=5e-4" assumption with an 8-arm ASHA sweep at 25→50→100 epoch rungs, producing a *measured* λ for ImageNet-10 and a real baseline.

**Mechanism**:
ASHA (Asynchronous Successive Halving) trains many configurations in parallel, kills the bottom-η at each rung, and promotes the rest with more compute. For LeJEPA's three real continuous knobs (λ, lr, wd), an 8-arm × 3-rung sweep visits 8 → 4 → 2 → 1 configurations at 25 / 50 / 75 / 100 epochs, total compute ≈ 4× a single 100-ep run rather than 8×. ImageNet-10 is small enough that 100 epochs ViT-S is ~1.5 GPU-h, so a full sweep is ~6–8 GPU-h. Output: the **measured baseline number** the vetting pass said was missing, *plus* a defensible λ for every later ablation.

**Source inspirations**:
- Primary: *LeJEPA*, Balestriero & LeCun, 2025 [arXiv:2511.08544] — explicitly says λ is the only knob and is "bisection searchable", motivating an explicit, principled sweep instead of bisection-by-hand.
- Supporting: *A System for Massively Parallel Hyperparameter Tuning (ASHA)*, Li et al., MLSys 2020 [arXiv:1810.05934].
- Supporting: *Hyperband: A Novel Bandit-Based Approach to HP Optimization*, Li et al., JMLR 2017 [arXiv:1603.06560].

**Why expected to improve**:
The vetting summary diagnosed `0 FULL SEND` ⇒ "the bottleneck is measurement, not ideas". This idea is literally that bottleneck dissolved into compute. Paper-default λ=0.1 was tuned for ImageNet-1K ViT-L; the ImageNet-10 / ViT-S regime is 30× smaller data, ~4× smaller model, and the effective batch / slice-noise ratio differs — there is a real prior that the optimal λ is *not* 0.1 here. A 0.5–2 pp gap between "default λ" and "best λ" is the standard observation in small-data SSL.

**Expected gain**: +0.5 / +1.5 / +3.0 pp 🟢
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Wrap `train_lejepa_ablation.py` in a thin Optuna study with `MedianPruner` (≈ ASHA).
2. Search space: λ ∈ logspace(-3, -0.5, 8), lr ∈ {2e-4, 5e-4, 1e-3}, wd ∈ {1e-2, 5e-2, 1e-1}.
3. Promote top-2 to full 100 epochs; report all three rungs to wandb.

**Risks**:
- Linear-probe variance across seeds (~0.3–0.5 pp on Imagenette) can mask small λ deltas; ASHA needs ≥ 2 seeds per arm at the top rung.
- If λ landscape is flat, the win collapses to "now you have a measured number" — still worthwhile per vetting Step-0.

**Falsification test**: After the sweep, fit a 1-D landscape over λ at fixed best (lr, wd). If best-λ is within ±0.2 pp of paper-default λ=0.1, the sweep returned no new λ signal — but the measured baseline is still the deliverable.

---

### Idea 3: Test-strictness curriculum (Moments → Epps–Pulley)

- **Pattern**: P5 (Decompose — split pretraining into 2 phases with different statistical tests)
- **Tier**: 2
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds a Lightning callback that swaps `module.loss_fn.univariate_test` at a milestone epoch. SIGReg, slicing, λ, projector, optimizer unchanged.
- **One-liner**: Warm up SIGReg with the cheap `Moments` test (mean + variance to 0 / 1) for the first 30 % of epochs, then switch to the full `EppsPulley` — curriculum on test strictness.

**Mechanism**:
The Epps–Pulley statistic is non-convex in the embedding and has weaker gradients far from N(0,1) (the ECF is bounded by 1, deviations saturate). The `Moments` test penalises `||μ||² + ||σ²−1||²` of the slice — strong, almost-linear gradient and unique global minimum at standardised marginals. Training the encoder to first reach unit variance / zero mean per slice is the *easy half* of being isotropic Gaussian; only after that does the higher-moment (kurtosis, multimodality) signal of Epps–Pulley dominate. The curriculum subsumes the **reframed Idea 4 (cosine λ-schedule)**: cosine-on-λ shrinks the same statistic uniformly; this shrinks the *complexity* of the statistic. Two phases, single switch milestone — no continuous controller, no extra continuous HP.

**Source inspirations**:
- Primary: *Curriculum Learning*, Bengio et al., ICML 2009 — easy-to-hard objectives.
- Supporting: *SwAV*, Caron et al., NeurIPS 2020 [arXiv:2006.09882] — empirically uses a curriculum of warmup / queue / sinkhorn steps in SSL.
- Supporting: *LeJEPA* [arXiv:2511.08544] — `Moments` and `EppsPulley` already implemented as drop-in `UnivariateTest`s.

**Why expected to improve**:
Vetting flagged that a *fixed-schedule on λ* (the Idea-4 reframe) should be tried before any adaptive controller. This idea is the corresponding fixed-schedule on the **test itself**, which is the more natural place to put the curriculum: it changes *what* SIGReg measures, not *how hard* it pulls. Two distinct knobs collapse to one milestone epoch, which has a discrete prior (30 % of training).

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `CurriculumTestCallback(milestone_epoch=30, easy=Moments, hard=EppsPulley)`.
2. At `on_train_epoch_start`, if epoch == milestone, mutate `module.loss_fn.univariate_test`.
3. Ablate milestone ∈ {0 (baseline = always-hard), 20, 30, 50, 100 (always-easy)}.

**Risks**:
- Discontinuity at the switch may spike the loss; warmup the new test over 2–3 epochs by mixing the two with linear weighting.
- `Moments` alone may collapse spread (it has no shape constraint) — verify by checking SIGReg(EppsPulley) at switch time stays bounded.

**Falsification test**: 5-point milestone sweep at 100 ep. If the U-shape over milestone is monotone or flat (best milestone ∈ {0, 100}), the curriculum is inert. Specifically: best curriculum run must beat both endpoints by ≥ 0.5 pp linear probe.

---

### Idea 4: LARS / LAMB optimizer for small-batch SSL

- **Pattern**: P3 (Replace — swap AdamW for LARS in `configure_optimizers`)
- **Tier**: 1
- **Target task**: same as batch.
- **Scope**: enhance-existing. Changes only the optimizer class in the Lightning recipe.
- **One-liner**: Replace AdamW with LARS (or LAMB if grouping by layer matters), which SimCLR/BYOL/SwAV all settled on for small-batch SSL stability.

**Mechanism**:
LARS applies a per-layer trust-ratio rescaling `lr_eff = lr · ||w|| / (||∇w|| + wd·||w||)`, which decouples the effective LR from the gradient norm and is what the SimCLR family found essential at small effective batch (≤ 1024). LeJEPA inherits the AdamW default from the paper because ViT-L / IN-1K large-batch tolerated it, but on ImageNet-10 the effective batch is much smaller, the SIGReg gradient is high-norm in early training (slice variance is large until embedding centres), and the per-layer rescaling is exactly the missing piece.

**Source inspirations**:
- Primary: *A Simple Framework for Contrastive Learning of Visual Representations (SimCLR)*, Chen et al., ICML 2020 [arXiv:2002.05709] — adopts LARS, ablates against AdamW.
- Supporting: *Large Batch Training of Convolutional Networks (LARS)*, You et al., arXiv 2017 [arXiv:1708.03888].
- Supporting: *Reducing the Need for Batch Size in SSL with LARS-style trust ratios*, multi-reference in BYOL (Grill 2020 [arXiv:2006.07733]) and SwAV (Caron 2020 [arXiv:2006.09882]).

**Why expected to improve**:
This is a category-of-result, not a single-paper claim: virtually every modern SSL recipe at small effective batch uses LARS or LAMB. LeJEPA keeping AdamW is a paper-faithfulness choice, not an evidence-backed one for the ImageNet-10 regime. Adding LARS at the same lr=5e-4 gives the per-layer rescaling for free; effort cost is one Lightning import.

**Expected gain**: +0.2 / +0.8 / +1.8 pp 🟢
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Replace `torch.optim.AdamW` with `lightning.fabric.optim.LARS` (or `torch_optimizer.Lamb`).
2. Sweep `lr ∈ {3e-4, 5e-4, 1e-3, 3e-3}` because LARS tolerates higher LR.
3. Keep wd, schedule, λ identical to the AdamW baseline for clean comparison.

**Risks**:
- LARS on transformer-norm layers can over-rescale — exclude `norm` and `bias` from trust ratio (standard convention).
- If wandb diff shows a 2–3× higher gradient norm under LARS, the trust ratio is doing the right thing but downstream may need lr re-tuned. Folds naturally into **Idea 5's sweep**.

**Falsification test**: 100-epoch LeJEPA ViT-S, LARS vs AdamW, matched lr per the LARS sweep. If best-LARS does not beat best-AdamW by ≥ 0.3 pp linear-probe with overlapping seeds, the per-layer rescaling didn't add at this scale.

---

### Idea 2: Sliced-Wasserstein-2 statistic instead of Epps–Pulley

- **Pattern**: P3 (Replace — swap the per-slice test)
- **Tier**: 1
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds a `SlicedW2Test(UnivariateTest)` subclass, plug into `SlicingUnivariateTest` exactly like `EppsPulley`. Slicing, λ, projector, optimizer unchanged.
- **One-liner**: Replace the empirical-characteristic-function test with the closed-form 1-D Wasserstein-2 distance between the slice's empirical CDF and N(0,1).

**Mechanism**:
For 1-D distributions the Wasserstein-2 distance has a closed-form integral against the inverse CDF: `W2²(p, N(0,1)) = ∫₀¹ (F_p⁻¹(u) − Φ⁻¹(u))² du`. With N batch samples per slice, this is just `sort(z) − Φ⁻¹((rank − 0.5)/N)`, squared, mean. Cost O(N log N) per slice — same order as Epps–Pulley's quadrature. The gradient through `sort` is well-defined (it's a permutation, identity on the sorted values), and W2 is **smoother** than the ECF integral in the sense of having no oscillatory kernel — closer to a quadratic, with stronger gradients far from the target. Drop-in replacement for any `UnivariateTest`.

**Source inspirations**:
- Primary: *LeJEPA*, Balestriero & LeCun, 2025 [arXiv:2511.08544] — `UnivariateTest` interface defines exactly this drop-in point.
- Supporting: *Generalized Sliced Wasserstein Distances*, Kolouri et al., NeurIPS 2019 [arXiv:1902.00434] — sliced-W variants and gradient properties.
- Supporting: *Sliced and Radon Wasserstein Barycenters*, Bonneel et al., JMIV 2015 — closed-form 1-D W2 and its differentiability.

**Why expected to improve**:
Epps–Pulley integrates `|φ_p(t) − e^(−t²/2)|²` over `t ∈ [0, t_max]`; far from N(0,1), the characteristic function still has bounded magnitude ≤ 1, so the gradient saturates. W2 grows quadratically with distance and never saturates, giving a stronger early-training signal — directly relevant to the small-data regime where the embedding starts far from isotropic. Same Cramér–Wold guarantee: W2 per slice = 0 iff the slice is N(0,1).

**Expected gain**: +0.3 / +1.0 / +2.0 pp 🟡
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Implement `SlicedW2Test(UnivariateTest)` using `torch.sort` + a cached `Φ⁻¹((rank − 0.5)/N)`.
2. Verify `forward(N(0,1) sample)` → 0 at large N (consistency check).
3. Plug into `SlicingUnivariateTest`, run at fixed λ.

**Risks**:
- `torch.sort` has zero-gradient over the permutation itself; only sorted values get gradient. This is fine mathematically (W2 is the right derivative) but loses no-op of the rank loss — verify.
- W2 has different units / scale than Epps–Pulley → optimal λ will move. Couple to **Idea 5's sweep** to find the new λ.

**Falsification test**: 100-epoch ImageNet-10, W2-SIGReg vs EP-SIGReg, each with its own best λ (sub-sweep at lr=5e-4). If best W2 run does not match EP within 0.3 pp (let alone beat by 0.5 pp), the smoother gradient story did not cash.

---

### Idea 6: Two-pass self-distillation across LeJEPA checkpoints

- **Pattern**: P8 (Distill — use the model's own pretrained checkpoint as a teacher)
- **Tier**: 2
- **Target task**: same as batch.
- **Scope**: enhance-existing. Adds a frozen teacher (a previous LeJEPA checkpoint of the same architecture) and a single auxiliary loss term. Backbone architecture, multi-crop, projector unchanged; one new α weight.
- **One-liner**: First train LeJEPA normally for 50 ep → freeze that model → continue training a **new** student LeJEPA where the loss adds `α · ||z_student − stop_grad(z_teacher)||²` on the global view embeddings.

**Mechanism**:
SEED (Fang et al., ICLR 2021) showed that small SSL models gain substantially from a frozen-teacher distillation signal even when the teacher is just a longer-trained version of itself. Unlike DINO/BYOL EMA — which couples teacher to student *online* and was explicitly removed by LeJEPA — this is **offline two-pass**: no EMA, no stop-gradient inside the optimisation loop, no architectural change. The first pass establishes a "good enough" representation; the second pass uses it as a regression target on top of the normal LeJEPA loss. Compute cost is exactly 2× (two passes), nothing more. The Cramér–Wold guarantee on the student is unaffected (the distillation term is an L² penalty in the projection space; the SIGReg term remains the unique driver of marginals being N(0,1)).

**Source inspirations**:
- Primary: *SEED: Self-supervised Distillation for Visual Representation*, Fang et al., ICLR 2021 [arXiv:2101.04731] — offline frozen-teacher SSL distillation, +2–5 pp on small students.
- Supporting: *DINOv2: Learning Robust Visual Features without Supervision*, Oquab et al., TMLR 2024 [arXiv:2304.07193] — confirms distilled SSL students outperform raw-trained ones at matched compute.
- Supporting: *LeJEPA* [arXiv:2511.08544] — teacher / student wrapper exists in `stable-pretraining.backbone.TeacherStudentWrapper` but is currently *unused* by the LeJEPA recipe (the wrapper is there for EMA setups). Reusing it for an offline frozen-teacher is a 5-line config change.

**Why expected to improve**:
On a 9 k-image dataset, the bottleneck is signal-per-image, not compute. A second pass over the same data with an extra (frozen-teacher) target effectively doubles supervision per image without needing fresh data — exactly the regime where two-pass distillation pays in SEED's ablations (+3 pp on CIFAR-scale targets). The α weight is one new continuous knob — **this violates the "single-λ" branding** like batch-1's Idea 2; flagged.

**Expected gain**: +0.5 / +1.5 / +3.0 pp 🟡
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. Run the canonical recipe for 50 ep → save checkpoint as `teacher.ckpt`.
2. Add `DistillationLoss(teacher_ckpt=teacher.ckpt, alpha=0.5)` returning `α · MSE(z_student, z_teacher.detach())`.
3. Train a fresh student for 100 ep with `L = L_LeJEPA + α · L_distill`; sweep α ∈ {0.1, 0.5, 1.0}.

**Risks**:
- α introduces a second knob → violates single-λ branding; if it pays, accept; if marginal, reject.
- Teacher feature space may be "wrong" at 50 ep — try teachers from {50, 80, 100} ep.
- Twice the wall-clock to compare against single-pass baseline at matched-budget.

**Falsification test**: 100-ep student with α ∈ {0.1, 0.5, 1.0}, teacher = 50-ep checkpoint. If best distilled student does not beat the **150-ep** vanilla LeJEPA baseline (matched compute, since 50+100 = 150) by ≥ 1.0 pp, the distillation signal is dominated by just training longer.

---

## Verification report

| # | Title | Primary paper VERIFIED | Mechanism concrete | Falsification sharp | Novelty verdict | Provenance | Feasibility | Compliance | Final |
|---|-------|----------------------|--------------------|--------------------|-----------------|------------|-------------|------------|-------|
| 1 | Stacked univariate tests | ✅ LeJEPA arXiv:2511.08544 + AD 1952 + Watson 1961 | ✅ | ✅ (Δ≥0.5 pp, non-overlapping CI) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 5 | ASHA HP sweep | ✅ Li MLSys 2020 arXiv:1810.05934 + LeJEPA bisection remark | ✅ | ✅ (measured-λ check; falls back to baseline-fixing) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 3 | Test-strictness curriculum | ✅ Bengio ICML 2009 + LeJEPA (Moments + EppsPulley both implemented) | ✅ | ✅ (5-point milestone sweep, U-shape required) | NOVEL | VERIFIED | 4 | OK | **KEEP** |
| 4 | LARS / LAMB | ✅ SimCLR ICML 2020 arXiv:2002.05709 + You arXiv:1708.03888 | ✅ | ✅ (Δ≥0.3 pp non-overlap) | EXTENDS | VERIFIED | 5 | OK | **KEEP** |
| 2 | Sliced-W2 statistic | ✅ Kolouri NeurIPS 2019 arXiv:1902.00434 + Bonneel JMIV 2015 + LeJEPA | ✅ | ✅ (W2 must match EP within 0.3 pp at own best λ) | NOVEL | VERIFIED | 4 | OK | **KEEP** |
| 6 | Two-pass self-distillation | ✅ SEED ICLR 2021 arXiv:2101.04731 + DINOv2 TMLR 2024 + LeJEPA wrapper | ✅ | ✅ (must beat 150-ep matched-compute baseline by ≥1.0 pp) | EXTENDS | VERIFIED | 3 | ⚠️ adds α — violates "single λ"; flagged | **KEEP w/ flag** |

**Cross-idea consistency**: Ideas 1, 2, 3 all touch the per-slice statistic but at different layers (combine / replace / schedule) — non-conflicting; can chain (e.g., curriculum from Moments → stacked-{EP, AD, W} in idea 1; or curriculum from Moments → W2 in idea 2). Idea 4 is orthogonal (optimizer). Idea 5 (HP sweep) is meta and applies to any other idea's tuning step. Idea 6 (distillation) is independent of everything but the optimizer.

No ideas rejected. Rejection log entry: see `_logs/_rejection_log.md` (empty for this batch).

## Notes & warnings
- ⚠️ **Baseline still TBD** — Idea 5 is the explicit fix. Until baseline is measured, every absolute gain estimate inherits the same uncertainty as batch-1.
- ⚠️ **Idea 6 introduces α** — second hyper-parameter; if user wants to preserve the single-λ property strictly, downgrade Idea 6 or fold α into Idea 5's sweep.
- ⚠️ **Tier-2 quota near floor** — T2 = 33 % (within 20–40 % band). Time-window <12 mo count is 3 primaries (LeJEPA × 3 — same paper counted multiple times). If reviewer wants distinct-source <12 mo papers, swap one LeJEPA citation for *DINOv2-with-Registers* checkpoint paper (12-36 mo) and surface as warning rather than re-search.
- **Devil's-advocate on top-1 tied pair** (Idea 1 + Idea 5):
  - Idea 1: failure mode = three near-orthogonal tests still cover only *linear-marginal* deviations; if the residual non-Gaussianity is fully captured by EppsPulley already (Imagenette is small enough that the empirical CDF is well-resolved), stacking is inert. Citation supporting risk: power studies show AD and EP are highly correlated on n<2048 samples (D'Agostino & Stephens, *Goodness-of-Fit Techniques*, 1986).
  - Idea 5: failure mode = if the linear-probe landscape over λ is flat between 0.02 and 0.1 (which is what LeJEPA paper Fig. 4 hints), the sweep returns no λ signal — but the measured baseline is still the deliverable. Rank preserved.
- **Pattern coverage cumulative across batches 1+2**: P1, P2, P3, P4, P5, P6, P7, P8 — 8 of 12 patterns visited. P9, P10, P11, P12 unused (most don't fit pretraining naturally; P12 self-play possible for a future greenfield batch).

## Next steps for user
1. **Run Idea 5 (ASHA sweep) first** — this gives the measured ImageNet-10 baseline that the vetting pass said is the bottleneck of everything else.
2. **In parallel, run Idea 4 (LARS) and Idea 1 (stacked tests)** — both effort-S, orthogonal, non-conflicting. Two more cheap deltas before ASHA finishes.
3. **Then Idea 3 (curriculum)** at the milestone the sweep recommends.
4. **Hold Idea 2 (W2)** until Idea 5 returns the new λ — λ will shift under a different statistic, don't compare at frozen λ.
5. **Hold Idea 6 (distillation)** until everything cheap has landed; it costs 2× wall-clock and adds an HP.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 55/30/15 | given-vetting batch-1 | 2026-05-18 batch-2`
