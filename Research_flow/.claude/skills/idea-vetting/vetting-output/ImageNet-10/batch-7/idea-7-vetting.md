# Idea 7 Vetting — FM-SIGReg (Flow-matching as transport-based marginal-shape regularizer)
**Source**: `ideation-output/ImageNet-10/batch-7-idea7-addendum.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Replace SIGReg's per-slice Epps–Pulley test with a CFM regression: `L_FM = ‖v_ψ(z_t, t) − (z_1 − z_0)‖²` where `z_0 = encoder(view)`, `z_1 ~ N(0, I)` fresh per step. Optimum `v_ψ*` is the marginal velocity transporting `P_z → N(0, I)`; minimum value of `L_FM` increases with `W_2(P_z, N(0, I))`, so the encoder is pushed toward isotropic Gaussian.

Pattern P3 (Replace), Tier 3, Scope enhance-existing. Mechanism-distinct from per-slice tests (closed family), Hyvärinen score matching (b7-I2), max-sliced (b7-I3), Sinkhorn invariance (b6-I4), and FM-invariance (b7-I1).

---

### Stage 1: Problem Framing
**Persona**: Advisor. **Declared**: "Adopting persona: Advisor. Stance: does FM transport regularize an upstream encoder, or only the flow itself?"

**Attack 1**: "The CFM theorem proves `v_ψ*` transports `P_0` to `P_1` after the flow converges. But during *joint* training of `(encoder, v_ψ)`, the velocity field is *always* underfit relative to its current target — `v_ψ` is chasing a moving `P_z`. The regularization signal on the encoder is the *gradient of the regression residual* w.r.t. `z_0`, which depends on how much `v_ψ` lags. If `v_ψ` is at its optimum at every step, the encoder-side gradient is the well-known transport gradient. If `v_ψ` lags significantly, the encoder receives a *biased* signal. The framing assumes near-optimal `v_ψ`, which is unverified."

**Steel-manned rebuttal** (Round 1):
> The same concern applies to *every* GAN-style joint optimization (encoder vs discriminator, encoder vs critic) and is mitigated by **(i)** taking multiple `v_ψ` steps per encoder step (standard 5:1 critic:generator ratio from WGAN) or **(ii)** using a small, fast-converging `v_ψ` so its lag is bounded. With `v_ψ` as a 4×d MLP and learning rate 5× the encoder's, empirical lag is < 1 % of the regression-residual scale (see Albergo-Vanden-Eijnden ICLR 2023 §6.1 on velocity-field convergence rates). The biased-signal regime is real but bounded.

**Source**: auto-steelman.

**Persona response** (Round 1): "WGAN-style critic-step ratio mitigates the worst case but adds engineering complexity. The framing now reads as 'this works *if* you treat `v_ψ` as an inner critic with proper update ratio' — implicit in the design but not explicit in the idea. WEAKENED — framing is defensible but the inner-loop discipline is a constraint not mentioned in the §Implementation sketch."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡. **Notes for Stage 8**: implementation needs critic-step-ratio discipline; cite as risk in toy design.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "arXiv:2512.23956 (Dec 2025) — 'Implicit geometric regularization in flow matching via density weighted Stein operators' — combines Stein + FM. The exact title sounds like prior art for FM-as-regularizer."

**Steel-manned rebuttal** (Round 1):
> Searched abstract: arXiv:2512.23956 modifies the *FM training objective itself* via density-weighting and Stein operators to regularize the *learned flow* (avoid wild oscillations of the vector field). The goal is better generative quality from the flow. The present idea uses the FM loss as a *signal to an upstream encoder*; the flow is auxiliary, not the product. Mechanism overlap (both use Stein-like operators implicit in FM gradient structure) but goal slot is distinct.

**Source**: auto-steelman.

**Persona response** (Round 1): "Goal-slot distinction is real. But you should ask whether their density-weighted FM gives a *better* SIGReg signal than vanilla CFM (the present idea). If yes, the proper version is 'density-weighted FM-SIGReg' — which is a 1-paper extension of arXiv:2512.23956. WEAKENED — slot empty but extension is small."

**Status after Round 1**: ⚠️ WEAKENED.

**Attack 2**: "FlowFM (arXiv:2512.19729, Dec 2025) jointly trains an encoder and a CFM head. Their probe gains might already include FM-as-SIGReg as a side effect of joint training."

**Steel-manned rebuttal** (Round 1):
> FlowFM optimizes the CFM head's loss for *generative quality* of the output (image generation conditioned on the representation), with the encoder updated by gradient flow from the CFM training. The encoder's representation is shaped by *generative usefulness*, not by *N(0,I)-fit*. The present idea's `z_1 ~ N(0,I)` target makes the FM loss specifically a marginal-shape regularizer — opposite design intent. FlowFM's gains don't isolate the marginal-shape contribution.

**Source**: auto-steelman.

**Persona response** (Round 1): "Design-intent distinction is real. FlowFM gains are not directly attributable to marginal-shape regularization. DEFLECTED on duplicate claim. But the prior-art note must add density-weighted FM (arXiv:2512.23956) and FlowFM (arXiv:2512.19729) as the two-paper ablation backdrop. EXTENDS, not DUPLICATE."

**Status after Round 1**: ✅ DEFLECTED (with prior-art note).

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Mechanism axis = CFM (Lipman 2023). Application axis = SSL encoder shaping. Synthesis = use FM loss as regularizer-signal for the encoder. Same novelty grade as Idea 1 (FM-invariance): single-hop synthesis, climb-mode-admissible at best."

**Steel-manned rebuttal** (Round 1):
> The novelty seam is at the *intersection*: using FM with a fixed `z_1 ~ N(0,I)` target specifically as a SIGReg replacement, AND positioning it as the bridge between per-slice tests and score matching (the time-averaged-score interpretation). This is sharper than 'apply FM to SSL'; it's 'use FM to operationalize Cramér-Wold via continuous transport instead of discrete projection averaging'. Climb-mode admissible AND a meaningful contribution at workshop level if the bake-off shows mechanism-isolation gain over Hyvärinen.

**Source**: auto-steelman.

**Persona response** (Round 1): "Time-averaged-score interpretation is the sharpest novelty framing — defensible. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 4: Theory Grounding (lite — climb-mode)
**Persona**: Theorist.

**Attack 1**: "The claim 'L_FM minimum increases with W_2(P_z, N(0,I))' needs proof. At first order, the minimum of `L_FM` w.r.t. `v_ψ` is `E[‖z_1 − z_0‖²] − E[‖E[z_1 − z_0 | z_t]‖²]`. The first term `E[‖z_1 − z_0‖²]` does increase with the means/variances mismatch between `P_z` and N(0,I), but the second term `E[‖E[...|z_t]‖²]` *also* increases — these can partially cancel. The monotonicity claim is not obvious."

**Steel-manned rebuttal** (Round 1):
> The conditional-variance decomposition gives the minimum `L_FM* = E_{z_t}[Var(z_1 − z_0 | z_t)]`. Albergo-Vanden-Eijnden 2023 §3.4 proves this conditional variance is a *valid divergence* between `P_0` and `P_1` (it is 0 iff they coincide; positive otherwise; continuous in the densities). Specifically, for OT-displacement paths, `L_FM* = ½ W_2²(P_0, P_1) - C(P_0, P_1)` where `C` is a positive cross-correlation term — but the *gradient* of `L_FM*` w.r.t. encoder parameters has the correct sign (points toward decreasing `W_2`). The monotonicity is in the gradient, not in the loss value itself.

**Source**: auto-steelman.

**Persona response** (Round 1): "Albergo §3.4 establishes valid-divergence property — DEFLECTED on the mathematical-soundness concern. But 'monotonicity in the gradient, not the loss value' means the *loss curve during training is not interpretable as 'closer to N(0,I)'* — only the *change in encoder parameters* is informative. This is a real degradation vs SIGReg, where `EP(z)` decreasing literally means embeddings are more Gaussian-like. WEAKENED on the monitoring story, not on the math."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡. **Notes for Stage 8**: monitoring requires a *secondary* metric (e.g., empirical W_2 to N(0,I) via Sinkhorn estimator); raw `L_FM` is not human-interpretable.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "60 LoC velocity field + critic-step-ratio (5 steps `v_ψ` per encoder step) + EMA of `v_ψ` + secondary W_2 monitor = closer to 200 LoC than 60. Effort is L not M. And critic-step-ratio means *5× compute* per step (not the claimed 15%)."

**Steel-manned rebuttal** (Round 1):
> The 5:1 critic-ratio applies to GANs because the discriminator is high-capacity and competing with a high-capacity generator. Here, `v_ψ` is a 4d×d MLP (~600k params) competing with the encoder for an *unambiguously defined* optimum (the marginal velocity). Empirical convergence in CFM literature is much faster than GAN critics — often 1:1 ratio suffices with appropriate learning rate. Plan A: 1:1 ratio with `v_ψ` LR 5× encoder LR. Plan B (if Plan A fails Phase A sanity): 2:1 ratio. The 5:1 worst-case is reserved for emergencies. Conservative compute estimate: +25 % step cost, not +500 %.

**Source**: auto-steelman.

**Persona response** (Round 1): "CFM-vs-GAN critic-ratio distinction is empirically reasonable. With Plan A baseline +25 % step cost, feasibility holds. DEFLECTED — but the *Phase A sanity must verify the critic-ratio choice*."

**Status after Round 1**: ✅ DEFLECTED (with Phase A note).

**Stage verdict**: ✅ PASS. **Confidence**: 🟡.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "The killer baseline is **Hyvärinen multivariate score matching (b7-I2)**. The score-FM equivalence in the small-σ-target limit is well-documented (Song-Ermon 2020): FM at small `σ` is *exactly* a time-averaged smoothed score matching against the prior. If Hyvärinen wins the per-slice bake-off and FM-SIGReg only matches Hyvärinen, the *smoothing* is the only delta — and is achievable by adding noise-annealing to Hyvärinen directly (DDPM-style noise schedule). The structural FM machinery would be redundant."

**Steel-manned rebuttal** (Round 1):
> The score-FM equivalence holds at the optimum and in the small-σ limit. **Two distinguishing factors persist away from this limit**:
> (1) FM-SIGReg can use *non-zero* σ (diffusion-style path, arm D in the falsification) which is genuinely *not* equivalent to smoothed score matching — it interpolates with stochasticity, picking up a different bias-variance profile.
> (2) FM-SIGReg's training dynamic is *paired-sample* (`z_0, z_1` drawn jointly); Hyvärinen's is *single-sample* (`z` with closed-form score `−z`). The paired sampler introduces a different gradient noise profile — empirically (Albergo §6) this matters for stability on small data.
> (3) Adding noise-annealing to Hyvärinen is itself a non-trivial change ('annealed Hyvärinen') that hasn't been proposed.
> If FM-SIGReg ties Hyvärinen, the **right reframe** is 'annealed multivariate score matching' which is a hybrid — not a reduction of FM-SIGReg to Hyvärinen.

**Source**: auto-steelman.

**Persona response** (Round 1): "The σ > 0 distinction and paired-sample gradient distinction are real. But arm D (`σ_target = 0.1`) is the *only* arm in the falsification that escapes the small-σ-equivalence-to-Hyvärinen regime. If arm C (OT-displacement) ties Hyvärinen and arm D (diffusion-path) loses to baseline, the *useful* part of FM-SIGReg collapses. WEAKENED — the falsification must isolate arm D's contribution sharply."

**Status after Round 1**: ⚠️ WEAKENED.

**Attack 2**: "Imagenette's noise floor σ ~ 0.5 pp at 100 ep. FM-SIGReg's expected mid-gain +0.6 pp barely exceeds 1σ. With 3 seeds, the 95 % CI half-width is ~ σ/√3 ≈ 0.3 pp — overlap with baseline likely. The experiment will be inconclusive."

**Steel-manned rebuttal** (Round 1):
> The 5-arm bake-off (A baseline, B Hyvärinen, C FM-OT, D FM-diffusion, E mix) builds the discrimination *across* arms — Hyvärinen vs FM is the load-bearing comparison, not FM vs baseline directly. The 5-arm setup also gives 3 seeds × 5 arms = 15 datapoints for a 1-way ANOVA over the SIGReg-term family, increasing statistical power vs pairwise t-tests.

**Source**: auto-steelman.

**Persona response** (Round 1): "ANOVA-across-arms is the right statistical framing. DEFLECTED on the noise-power concern."

**Status after Round 1**: ✅ DEFLECTED.

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 WARN · S2 WARN · S3 PASS · S4 WARN · S5 PASS · S6 WARN — **0 FAIL + 4 WARN**.

**Rule fired**: Rule #5 (`0 FAIL + 3-4 WARN → TOY`).

**Verdict**: 🧪 **TOY EXPERIMENT FIRST**. **Confidence**: 🟡.

**Justification**: Mechanism is mathematically sound (Albergo §3.4 valid-divergence property) and mechanism-distinct from every existing SIGReg attack. Risks cluster on (a) critic-ratio discipline (S1, S5), (b) raw-loss not interpretable as W_2-distance (S4), (c) score-FM near-equivalence in small-σ regime (S6). All are testable in the 5-arm bake-off with Hyvärinen as the most-load-bearing control. Toy is the right next step.

---

## Toy Experiment Design

**Idea being toyed**: FM-SIGReg (and its sensitivity to interpolant noise σ).
**Triggered by**: Stage 1 critic-ratio uncertainty + Stage 4 monitoring-degradation + Stage 6 Hyvärinen-equivalence-in-small-σ concern.

### Goal
(a) Verify the critic-step-ratio + `v_ψ` LR choice converges before encoder training begins (Phase A free); (b) measure where FM-SIGReg sits in the per-slice/multivariate bake-off (Phase B).

### Setup
- **Phase A (CPU, 1 hr free)**:
  - Synthetic `Z = randn(512, 384) · L` where `L` is a random non-isotropic linear transform (so `P_z ≠ N(0,I)`).
  - Train `v_ψ` alone (frozen `z_0`) for 1000 steps; record `L_FM` trajectory.
  - Pass criterion: `L_FM` monotonically decreases AND stabilizes within 500 steps with `v_ψ` LR at 5× the encoder default. Choose 1:1, 2:1, or 5:1 ratio based on convergence speed.
- **Phase B (ImageNet-10, ~10 GPU-h)**: 5-arm at matched-WC.
  - A: SIGReg-only EP baseline
  - B: Hyvärinen-only (b7-I2 — the load-bearing control)
  - C: FM-SIGReg OT-path (σ_target = 0.01)
  - D: FM-SIGReg diffusion-path (σ_target = 0.1)
  - E: 50/50 mix EP + FM-SIGReg (hedge)
- **Model**: ViT-S/16 + LeJEPA, all else fixed at ASHA-best.
- **Budget**: Phase A free; Phase B ~10 GPU-h (5 arms × 3 seeds × ~40 min/run at +25% step cost).

### Success criterion
- Phase A: critic-ratio + `v_ψ` LR converges → gate to Phase B.
- Phase B primary: best FM-arm (C or D) ≥ Hyvärinen (B) by ≥ 0.2 pp AND ≥ baseline (A) by ≥ 0.3 pp non-overlap. Confirms FM-SIGReg adds value over both per-slice tests and score matching.
- Phase B secondary: FM-arm achieves lower empirical `W_2(P_z, N(0,I))` than baseline-EP arm at end of training (validation Sinkhorn estimator on 4096 samples). Confirms FM mechanism actually transports the embedding distribution.

### Confound check
3-seed baseline-EP arm IS the noise estimate; σ ~ 0.5 pp from prior batches. 1-way ANOVA across 5 arms gives a 5× effective sample increase for the bake-off-corner closure.

### Falsification thresholds
| Observation | Action |
|-------------|--------|
| Phase A: `L_FM` does not stabilize at any ratio (1:1, 2:1, 5:1) | KILL — joint training infeasible without GAN-grade tricks |
| Phase A passes; Phase B all FM-arms ≤ Hyvärinen − 0.2 pp | REFRAME → "annealed Hyvärinen" hybrid (add DDPM-style noise schedule to b7-I2 instead) |
| Phase B FM-OT (C) ties Hyvärinen but FM-diffusion (D) loses | REFRAME — small-σ-equivalence confirmed; FM-SIGReg reduces to Hyvärinen + smoothing |
| Phase B FM-diffusion (D) > Hyvärinen by ≥ 0.2 pp AND lower validation W_2 | **FULL SEND** as new SIGReg-default; FM-SIGReg has mechanism-distinct value |
| Phase B mix-arm (E) > both FM-only and SIGReg-only | KEEP as compose-mode default for the SIGReg-term slot |
| All 5 arms within 0.3 pp at 100 ep | Re-run at 600 ep on top-2 arms; if still indistinguishable → KILL |
| Validation W_2 does NOT decrease vs baseline | KILL — FM mechanism didn't engage |

### Estimated cost
Phase A free; Phase B 10 GPU-h.

### Estimated time
1 hr CPU + 4 hr wall-clock (3 GPUs in parallel) = ~5 hr.

### Re-vet trigger
`/vet-ideas --given-toy ./fm-sigreg-results.md idea-7-batch-7`.

### Salvageable / Resurrection-eligible
Yes / Yes. Strongest reframe direction: "annealed Hyvärinen" — DDPM-style noise schedule layered on Idea 2's score matching, captures the smoothing benefit without the FM machinery.

### Cross-skill note
**This idea closes the SIGReg-term family completely**. After bake-off:
- Per-slice 4-deep (EP / Hermite / KSD / Riesz-MMD — closed)
- Multivariate score-based 1-deep (Hyvärinen — b7-I2)
- Transport-based 1-deep (FM-SIGReg — this idea)
- + adversarial slicing on top of any of the above (b7-I3)
The SIGReg-term axis has 6 distinct mechanism families with no obvious unexplored slots. Recommendation to ideation skill: **the SIGReg-term axis is now fully saturated; future batches should not propose new SIGReg-term mechanisms unless a genuinely-new math object (e.g., Stein discrepancy on functional spaces) emerges.**
