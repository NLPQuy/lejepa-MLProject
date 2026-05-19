---
name: toy-queue
type: append-only
sort: cost-ascending under Active
---
# Toy queue — ImageNet-10
<!-- entries appended below -->

## Active

### Idea 3 — Register tokens (batch 1)
- Toy-cost: 8 GPU-h (4 runs × ViT-S/100ep)
- Decision rule: Δ_probe ≥ 0.5 pp + non-overlapping seed range → graduate to FULL SEND; −0.3 < Δ < 0.5 pp → keep (free); Δ < −0.3 pp → KILL.
- Falsification trigger: LeJEPA CLS-concat probe is structurally insulated from patch-token artifacts (Darcet ICLR 2024 §5).
- Status: queued.

### Idea 6 — Multi-crop curriculum + class-balanced sampler (batch 1)
- Toy-cost: 12 GPU-h (6 runs × ViT-S/100ep, V∈{6,10} × curr∈{on,off} × 3 seeds, two cells dropped for budget)
- Decision rule: V=10+curr > V=6+baseline by ≥ 1.0 pp at equal wall-clock with non-overlapping CIs → graduate to V∈{10,14} sweep; overlap → KILL.
- Falsification trigger: small-data SSL seed variance (σ ~0.5 pp) is close to the expected gain.
- Status: queued.

### Idea 1 — Stacked univariate tests in SIGReg (batch 2)
- Toy-cost: 18 GPU-h (4 arms × 3 seeds × ViT-S/100ep). Arms: EP@M=1024, EP@M=2048, {EP,AD}@M=1024, {EP,AD,W}@M=1024.
- Decision rule: triple-test arm beats both EP-only AND EP@M=2048 (variance-reduction control) by ≥ 0.5 pp non-overlap CI → graduate to FULL SEND. Beats only EP-only but not EP@M=2048 → reframe to "use M=2048" (variance, not power, was the driver). Beats neither → KILL the salvage.
- Falsification trigger: AD ↔ EP statistic-value correlation > 0.85 at n ≤ 256 (D'Agostino & Stephens 1986) suggests gradient directions may not be as orthogonal as proposal claims.
- Status: queued. Run after or alongside Idea-5 ASHA; not gated on its output (uses fixed λ=0.1 or ASHA-found λ if available).

### Idea 3 — Test-strictness curriculum (Moments → Epps–Pulley) (batch 2)
- Toy-cost: 18 GPU-h (4 arms × 3 seeds × ViT-S/100ep). Arms: always-EP, cosine-λ on EP, curriculum-Moments(0–30ep)→EP, curriculum-Moments(0–50ep)→EP.
- Decision rule: best curriculum arm beats both always-EP and cosine-λ-on-EP by ≥ 0.5 pp non-overlap. Sanity: SIGReg(EP) at switch ≤ 2× the always-EP value at the same epoch.
- Falsification trigger: `Moments` test has infinitely many minimisers (any zero-mean unit-variance distribution); switch discontinuity may catastrophically increase EP loss at transition.
- Status: queued. Run after stacked-EP and cosine-λ-on-EP are both measured (uses them as controls).

## Completed
*(none yet)*

### Idea 4 — Hermite-moment univariate test (batch 3)
- Toy-cost: 12 GPU-h (4 arms × 3 seeds × ViT-S/100ep). Arms: EP@M=1024, ExtendedJB, Hermite-4, Hermite-6.
- Decision rule: Hermite-6 beats **both** EP **and** ExtendedJB by ≥ 0.5 pp non-overlap → graduate. Beats EP but not ExtendedJB → reframe as "Hermite ≡ JB" → KILL. Beats neither → KILL.
- Falsification trigger: D'Agostino & Stephens 1986 power tables — higher-moment tests rarely beat AD/EP at n ≤ 256 on light-tailed alternatives.
- Status: queued. Run after or alongside batch-2 Idea 1 (stacked-tests) toy — shares `UnivariateTest` plumbing; can fold into a single 7-arm job-array (3 stacked + 4 Hermite).

### Idea 6 — Embedding-rank curriculum (batch 3)
- Toy-cost: 18 GPU-h (3 arms × 3 seeds × ViT-S/100ep). Arms: always-d=384, curriculum 32→384 over 50ep, curriculum 32→384 over 30ep. Log RankMe per epoch.
- Decision rule: best curriculum ≥ 0.5 pp at endpoint **OR** reaches baseline pp in ≤ 60 % epochs. Sanity: RankMe at end-of-curriculum ≥ baseline (no slow-drift collapse).
- Falsification trigger: equilibrium risk (top-k_t isotropic + (d−k_t) drift) detectable via RankMe gap > 30 % at end-of-curriculum phase.
- Status: queued. Needs measured baseline (batch-2 Idea 5 ASHA output) before running.

### Idea 1 — Two-student co-distillation, disjoint slice subspaces (batch 3)
- Toy-cost: 24 GPU-h (γ ∈ {0, 0.5, 1.0} × 2 seeds × 100ep + 200-ep single-student matched-compute control × 2 seeds).
- Decision rule: best γ > 0 beats 200-ep single-student by ≥ 0.5 pp non-overlap → graduate. Beats single-100ep but not single-200ep → KILL ("more wall-clock did it"). Worse than 200-ep single → KILL.
- Falsification trigger: BYOL-symmetric-no-EMA is presented as inferior in LeJEPA paper ablations; concurrent co-distillation without EMA is the empirically-untested regime.
- Status: queued. Needs measured baseline; run last in toy sequence (most expensive, tightest control bar).

## Active (batch-4 additions, cost-ascending)

### Idea 3-A (batch-4): Layer-wise SIGReg — Phase A (probe-alignment check)
- Toy cost: 0 GPU-h
- Dependency: any baseline LeJEPA checkpoint
- Decision rule: if gap(probe-concat-2, probe-last) ≥ 0.3 pp → Phase B fires; else KILL idea 3 and archive layer-wise SIGReg family
- Status: active

### Idea 4-A (batch-4): Antithetic+CV — Phase A synthetic-variance sanity
- Toy cost: 0 GPU-h (CPU)
- Dependency: none
- Decision rule: at M=256, d=384, synthetic Z: variance ratio (vanilla / antithetic+CV) ≥ 1.5 → Phase B fires; else KILL idea 4
- Status: active

### Idea 3-B (batch-4): Layer-wise SIGReg — Phase B
- Toy cost: 15 GPU-h
- Dependency: Phase A pass
- Decision rule: ≥ 0.5 pp non-overlap vs baseline AND last-2-layer probe gap widens
- Status: active (gated)

### Idea 4-B (batch-4): Antithetic+CV on ImageNet-10
- Toy cost: 45 GPU-h
- Dependency: Phase A pass + SRHT (batch-3 Idea 2) shipped
- Decision rule: SIGReg-loss running-std ≥ 25 % lower vs SRHT-alone; linear-probe parity ±0.3 pp
- Status: active (gated)

### Idea 6 (batch-4): MAE pixel-recon auxiliary head
- Toy cost: 75 GPU-h + ~2 days eng
- Dependency: after batch-3 TOYs (Hermite, rank-curriculum, co-distillation) settle
- Decision rule: best α arm beats matched-WC baseline by ≥ 0.6 pp non-overlap → FULL; beats equal-epoch but loses to matched-WC → KILL; loses to equal-epoch → KILL outright
- Status: active (deferred)

<!-- Batch-5 additions, appended 2026-05-18, cost-ascending order -->

### Batch 5 — Active TOYs

- **Idea 4-A** (Sliced Riesz-MMD Phase A — synthetic power test)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: Riesz-MMD power ≥ EP power AND wall-clock ≤ EP on N(0,1)+5%-shift mixture at α=0.05 → graduate to Phase B; else KILL
  - Dependency: pairs with Idea 2-A (same synthetic test, joint run)
  - Status: pending — run immediately, free

- **Idea 2-A** (KSD Phase A — synthetic power test)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: KSD power ≥ 1.5× EP power on N(0,1)+5%-shift mixture (must justify O(N²) cost) → Phase B; else KILL
  - Dependency: pairs with Idea 4-A
  - Status: pending — run immediately, free

- **Idea 4-B** (Sliced Riesz-MMD on ImageNet-10)
  - Cost: 25 GPU-h
  - Decision rule: linear-probe ±0.3 pp parity with EP baseline AND wall-clock ≤ EP → adopt as new default statistic
  - Dependency: Phase A pass
  - Status: blocked on Phase A

- **Idea 2-B** (KSD on ImageNet-10)
  - Cost: 30 GPU-h
  - Decision rule: linear-probe ≥ 0.4 pp non-overlap vs EP baseline at matched cost
  - Dependency: Phase A pass AND beats Riesz-MMD on Phase A power
  - Status: blocked on Phase A

<!-- Batch-6 additions, appended 2026-05-18, cost-ascending order -->

### Batch 6 — Active TOYs

- **Idea 1-A** (RankMe controller Phase A — CIFAR-10 PI-controller dynamics)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: λ trajectory converges within 5 ep, oscillation < 30 % of mean → Phase B fires; else retune or KILL
  - Dependency: pairs with Idea 5-A
  - Status: pending — run immediately, free

- **Idea 5-A** (Poincaré pre-flight — super-cluster/within-cluster ratio on saved baseline)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: ratio ≥ 1.5 → Phase B fires; 1.3–1.5 → defer; < 1.3 → KILL idea (Imagenette hierarchy too shallow)
  - Dependency: any saved LeJEPA checkpoint
  - Status: pending — run immediately, free

- **Idea 3-A** (iBOT-SIGReg Phase A — synthetic predictor-output normality on position-correlated patches)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: predictor-output per-slice normality value approaches iid baseline within 200 SGD steps → Phase B fires; else KILL
  - Dependency: none
  - Status: pending — run with 1-A and 5-A

- **Idea 1-B** (RankMe controller Phase B — 3-arm ImageNet-10)
  - Cost: 12 GPU-h
  - Decision rule: best controller arm matches fixed-λ-best within ±0.3 pp at total compute ≤ fixed-λ-best → FULL SEND; matches probe but uses more compute → REFRAME (compose-mode binder); loses on probe → KILL
  - Dependency: ASHA Step-0 + Phase A pass
  - Status: blocked on Phase A

- **Idea 4** (Sinkhorn invariance 3-arm A/B/C on ImageNet-10) — cheapest path to a batch-6 FULL SEND
  - Cost: 15 GPU-h
  - Decision rule: best arm ≥ 0.4 pp non-overlap vs baseline-MSE; mixed wins → FULL SEND as new invariance default; Sinkhorn-only wins + per-image cos < 0.5 → REFRAME (OT-collapse); baseline wins → KILL
  - Dependency: ASHA Step-0
  - Status: pending — run after ASHA

- **Idea 3-B** (iBOT-SIGReg vs MAE-aux 3-arm head-to-head on ImageNet-10)
  - Cost: 25 GPU-h — consolidates batch-4 MAE-aux TOY (saves ~50 GPU-h on the deferred 75-GPU-h MAE-aux)
  - Decision rule: best aux arm ≥ 0.5 pp non-overlap vs baseline; iBOT ≥ MAE by ≥ 0.3 pp → graduate iBOT, KILL MAE-aux; else drop both or graduate winner
  - Dependency: ASHA Step-0 + Phase A pass; bind λ_patch to Idea 1 controller if it ships
  - Status: blocked on Phase A

- **Idea 5-B** (Poincaré hyperbolic 2-arm Euclidean vs Poincaré on ImageNet-10)
  - Cost: 25 GPU-h
  - Decision rule: hyperbolic ≥ 0.4 pp non-overlap + super-cluster ratio in hyp ≥ 1.5× Euclidean → FULL SEND; else KILL
  - Dependency: Phase A pass + ASHA Step-0
  - Status: blocked on Phase A

### Batch 6 — Reframed (NOT new TOYs)

- **Idea 2 (register tokens)** — REFRAMED to "promote batch-1 Idea 3 TOY to Priority 1 + augment decision rule with artifact-tail mechanism-check". Do NOT queue as a new TOY; do NOT spend new compute. See batch-6/idea-2-vetting.md §Reframe direction.

- **Idea 6 (PH H₀ regularizer)** — REFRAMED to "ARCHIVE direction; salvageable only with 32-d projection or PH₁ variant + 1-hr-CPU gradient-norm sanity at d=384". Do NOT queue as a TOY.

<!-- Batch-7 additions, appended 2026-05-19, cost-ascending order -->

### Batch 7 — Active TOYs

- **Idea 2-A (batch 7)** (Hyvärinen Phase A — synthetic convex-decoy sanity)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: `‖s_θ + z‖_F` decreases AND `‖Cov(z) − I‖_F` does NOT decrease in isolation → Phase B fires; else KILL
  - Dependency: none — run immediately
  - Status: pending

- **Idea 3-A (batch 7)** (Max-sliced Phase A — alternating-opt stability on rotated synthetic)
  - Cost: 0 GPU-h (CPU + small-GPU, ~2 hr)
  - Decision rule: `T(Z·g_φ)` monotonic increase AND converges (oscillation < 10 % over last 200 steps) → Phase B fires; else KILL adversary direction (keep 50/50-mix fallback)
  - Dependency: none — run immediately
  - Status: pending

- **Idea 2-B (batch 7)** (Hyvärinen 5th arm of per-slice bake-off on ImageNet-10)
  - Cost: 6 GPU-h
  - Decision rule: Hyvärinen ≥ EP − 0.3 pp at matched WC × 1.10 → KEEP; ≥ winner + 0.4 pp non-overlap → FULL SEND new SIGReg default; loses by > 0.3 pp → KILL
  - Dependency: Phase A pass + ASHA Step-0
  - Status: blocked on Phase A

- **Idea 1 (batch 7)** (Flow-matching invariance 3rd arm in alignment bake-off)
  - Cost: 12 GPU-h (~5 GPU-h incremental over Sinkhorn b6 TOY)
  - Decision rule: FM ≥ baseline-MSE + 0.4 pp AND within ±0.3 pp of Sinkhorn → FULL SEND as alignment 2nd-option; FM > MSE but < Sinkhorn − 0.3 pp → REFRAME; FM ≤ MSE → KILL; flow divergence > 0.5 on val → KILL
  - Dependency: b6 Sinkhorn Phase B settled (sequencing); ASHA Step-0
  - Status: pending — sequenced after b6 Sinkhorn

- **Idea 3-B (batch 7)** (Max-sliced 4-arm on ImageNet-10)
  - Cost: 15 GPU-h
  - Decision rule: `1-adv > 1-random + 0.4 pp` AND `1-adv ≥ 1024-random − 0.3 pp` → FULL SEND (supersedes sampler family); `1-adv ≤ 1-random + 0.4 pp` → KILL; `50-50 mix > 1-adv + 0.3 pp` → REFRAME
  - Dependency: Phase A pass + ASHA Step-0
  - Status: blocked on Phase A

### Batch 7 — Reframed (NOT new TOYs)

- **Idea 4 (RL augmentation policy)** — REFRAMED. Original `random / saliency / RL-from-random` design measures the wrong control. Re-submit as **saliency-init RL vs saliency-frozen** in batch-8 (isolates online-adaptation delta). Do NOT spend new compute on the original design.

- **Idea 5 (Neural-collapse ETF prototypes)** — REFRAMED. **0-cost prerequisite passes** mandatory: (a) literature search "Cramér–Wold neural collapse simplex ETF"; (b) empirical k-means cluster-mean pairwise-cosine check on saved LeJEPA checkpoint vs ETF target `−1/19`. If either pre-check shows redundancy → KILL definitively. If both pass → re-submit with SwAV-style baseline + K-sweep.

### Batch 7 — Addendum TOY (quantum-themed Idea 6, added mid-session per user request)

- **Idea 6 (batch 7 addendum)** (SU(d)-structured-orthogonal projector — quantum-circuit-inspired)
  - Cost: 12 GPU-h (4 arms: baseline-MLP / MLP-strong-wd / structured-L=2d / structured-L=2d log d, × 3 seeds × 100 ep)
  - Decision rule: best structured arm ≥ baseline + 0.4 pp AND > MLP-strong-wd by ≥ 0.3 pp → FULL SEND (new projector default); ≈ MLP-strong-wd → REFRAME (use weight decay, structure decorative); ≤ baseline − 0.3 pp → KILL; all within ±0.3 pp → re-run at 600 ep, else KILL.
  - Falsification trigger: LeJEPA paper §5.2 reports projector contribution ~1 pp → signal may be in seed-variance noise (σ ~0.5 pp).
  - Implementation requirement: vectorized butterfly pattern, NOT naive Python loop (per Stage 5 note).
  - Dependency: ASHA Step-0; pairs naturally with Idea 3 (max-sliced) compose-mode bundle ("lean SIGReg + lean projector").
  - Mutually exclusive with: b6 Idea 5 Poincaré (same projector axis — head-to-head only).
  - Status: pending — slots into batch-7 TOY queue priority 5 (between Idea 1 alignment-bake-off and Idea 3-B max-sliced).

### Batch 7 — Second Addendum TOY (FM-SIGReg Idea 7, added mid-session per user request)

- **Idea 7-A (batch 7 addendum)** (FM-SIGReg Phase A — critic-step-ratio sanity on synthetic non-isotropic Z)
  - Cost: 0 GPU-h (CPU, ~1 hr)
  - Decision rule: `L_FM` monotonically decreases AND stabilizes within 500 steps at 1:1 critic-ratio with `v_ψ` LR = 5× encoder LR → Phase B fires at 1:1; if needs 2:1 → flag higher compute cost; if 5:1 fails → KILL (joint training infeasible)
  - Dependency: none — run immediately
  - Status: pending

- **Idea 7-B (batch 7 addendum)** (FM-SIGReg 5-arm bake-off on ImageNet-10)
  - Cost: 10 GPU-h (5 arms × 3 seeds × 100 ep × ~40 min/run at +25% step cost)
  - Arms: A baseline-EP / B Hyvärinen-only / C FM-SIGReg OT-path (σ=0.01) / D FM-SIGReg diffusion-path (σ=0.1) / E 50/50 mix EP+FM
  - Decision rule: best FM-arm ≥ Hyvärinen + 0.2 pp AND ≥ baseline + 0.3 pp non-overlap AND lower validation W_2 to N(0,I) → FULL SEND (new SIGReg-default); FM-OT (C) ties Hyvärinen + FM-diffusion (D) loses → REFRAME ("annealed Hyvärinen" hybrid); all FM ≤ Hyvärinen − 0.2 pp → KILL; validation W_2 not lower → KILL (mechanism didn't engage)
  - Falsification trigger: score-FM near-equivalence in small-σ limit (Song-Ermon 2020) → arm D (σ=0.1) is the load-bearing test of mechanism-distinctness
  - Implementation: paired sampling (`z_0 from encoder, z_1 from N(0,I) fresh`) + 4×d MLP velocity field + critic-ratio per Phase A result
  - Dependency: Phase A pass + ASHA Step-0
  - Status: blocked on Phase A
  - Note: this idea closes the SIGReg-term axis after bake-off. Per-slice 4-deep (closed) + multivariate score 1-deep (Hyvärinen) + transport-based 1-deep (FM-SIGReg) + adversarial-on-top (max-sliced) = 6 mechanism families; no obvious un-covered slots remain.

### Batch 7 — Idea 7 STATUS UPDATE (2026-05-19)
- **Idea 7-A status**: unchanged — still pending Phase A sanity (free CPU, 1 hr)
- **Idea 7-B status update**: TOY (v1) → FULL SEND (v2 after research-driven upgrades) — see idea-7-vetting-v2.md
  - Cost updated: 10 GPU-h → 12 GPU-h (added anisotropic-target arm F)
  - 6-arm bake-off replaces 5-arm: A baseline-EP / B Hyvärinen / C FM-v1 / D FM-v2-N(0,I) / E 50/50 mix / F FM-v2-anisotropic (Σ* = RankMe-0.6d setpoint, Hyvärinen N/A)
  - The original 7-B TOY queue entry above stays for audit; this entry supersedes its status.
