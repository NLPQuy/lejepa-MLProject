# Idea 2 Vetting — Multivariate score matching vs N(0,I) (Hyvärinen + Hutchinson)
**Source**: `ideation-output/ImageNet-10/batch-7.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Replace SIGReg's per-slice Epps–Pulley with full-d Hyvärinen score matching: `L_sm = ½‖s_θ(z)+z‖² + v^T ∇(s_θ(z) v)` (Hutchinson). Drop-in `~10 LoC` alternative to SIGReg with closed-form target score `−z`.

Pattern P3 (Replace), Tier 3, Scope enhance-existing. Composite 2.27 (top of batch).

---

### Stage 1: Problem Framing
**Persona**: Advisor. **Declared**: "Adopting persona: Advisor. Stance: in-domain SSL probe gain — does the swap improve probe?"

**Attack 1**: "Hyvärinen 2005 score matching is for fitting *parametric models* to data. Here, the situation is inverted — the encoder produces the data, and the target N(0,I) is fixed. Is the Hyvärinen objective even well-defined when the 'model' is fixed and the 'data' is what we vary?"

**Steel-manned rebuttal** (Round 1):
> The Fisher divergence `F(p_data || p_target) = E_{p_data}[‖∇log p_data(z) − ∇log p_target(z)‖²]` is symmetric in role: the *integrand* uses the data-side score and the target-side score; the *expectation* is over the data. We use it in "reverse direction": optimize the encoder so that the empirical distribution of `z` has score matching `∇log N(0,I)(z) = −z`. This is exactly the setup of *score-based generative models that match a prior* (Song-Ermon 2020 NeurIPS §3.2 "annealed score matching") — the prior side is fixed (Gaussian), the data side is what we shape. Well-defined.

**Source**: auto-steelman.

**Persona response** (Round 1): "Inverted-direction usage is principled and matches score-based generative model literature. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 0, UNREBUTTED 0.
**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "Vincent 2011 *Neural Computation* (Denoising Score Matching) and Song-Ermon 2019 (Sliced Score Matching) are direct prior art using score matching as a deep-learning regularizer. The 'as SIGReg replacement' framing is a 1-line substitution."

**Steel-manned rebuttal** (Round 1):
> Vincent 2011 fits denoising autoencoders; Song-Ermon 2019 trains score-based generative models. Neither applies score matching as an SSL embedding-shape regularizer with a fixed N(0,I) target. The closest published precedent is the LeJEPA paper itself (which uses Epps–Pulley, an ECF-based test). The score-matching-as-SIGReg-alternative slot is unoccupied in the SSL literature based on the live-search log (search Q2: "score matching Hyvarinen self-supervised representation learning embedding density" returned no direct hit).

**Source**: auto-steelman.

**Persona response** (Round 1): "Application slot is empty — verified by search. The mechanism is well-trodden (Hyvärinen 2005 + Hutchinson 1990) but the slot-application is novel. EXTENDS, not DUPLICATE. WEAKENED (mechanism is not novel, only the slot is)."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Novelty is purely on the *application* axis (Stage 3 axis check). Mechanism = Hyvärinen 2005, computation = Hutchinson 1990. Climb-mode admissible, but the contribution is narrow."

**Steel-manned rebuttal** (Round 1):
> Climb-mode goal is *probe gain*, not novelty grandeur. The cost is `~10 LoC` and 5% step-cost overhead; the benefit is a closed-form-gradient alternative to the per-slice ECF test that completes the per-slice-statistic 5-way bake-off (EP / Hermite / KSD / Riesz-MMD / Hyvärinen). Even if it underperforms, the bake-off result is informative for closing the SIGReg-statistic corner permanently.

**Source**: auto-steelman.

**Persona response** (Round 1): "Bake-off-completion framing is a legitimate climb-mode contribution. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 4: Theory Grounding (lite)
**Persona**: Theorist.

**Attack 1**: "The convex-decoy failure mode: `s_θ(z) = −z` makes `L_sm ≡ 0` identically. The mitigation (backprop through `z`) is heuristic, not theoretically guaranteed to escape this minimum."

**Steel-manned rebuttal** (Round 1):
> The Hutchinson trace term `v^T ∇(s_θ(z) v) = v^T ∇s_θ(z) v` is `−‖v‖²` only when `s_θ(z) = −z` — but reaching that solution requires the *encoder* to produce embeddings that satisfy `z + s_θ(z) = 0` *sample-wise*. The gradient flowing through `z` to the encoder is `∂L/∂z = s_θ(z) + z + ∇·s_θ`. At the decoy `s_θ = −z`, this gradient is `0 + (−∂z/∂z) = -I` — non-zero w.r.t. encoder parameters. The encoder is therefore *pushed* to make `z` match the score model's predictions, not the other way around. The decoy is a saddle, not a minimum, for the *joint* (encoder, s_θ) system. Vincent 2011 §4 has a similar argument for DSM. The 1-hr CPU sanity check verifies this at init.

**Source**: auto-steelman.

**Persona response** (Round 1): "Joint-saddle argument is reasonable but the CPU sanity test is *mandatory* before committing to the full run — the joint-non-convex optimization could still get trapped in approximate decoy in practice. WEAKENED — theoretically defensible, empirically unverified at init."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "Hutchinson trace requires `create_graph=True` for the second-derivative Jacobian-vector product. That's 2x memory at minimum, and at d=384 with batch=512 on a single A100, that may OOM."

**Steel-manned rebuttal** (Round 1):
> The `s_θ` is a small head (`d → d`, e.g. one linear layer or 2-layer MLP), not the encoder. The Jacobian is `d × d = 384 × 384 ≈ 150k params`; the JVP `v^T ∇s_θ v` is one extra forward+backward through the head only, not through the encoder. Memory overhead is ~ size of one extra `(B, d)` tensor (`~1 MB`), trivial.

**Source**: auto-steelman.

**Persona response** (Round 1): "Confirmed — the JVP is local to `s_θ`. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "Killer baseline = whichever of {EP, Hermite, KSD, Riesz-MMD} wins the per-slice bake-off currently in active TOY queue. If KSD beats EP and Hyvärinen ties KSD, the 'add Hyvärinen as 5th arm' value is zero — KSD already covers the per-slice corner with a Stein-discrepancy mechanism."

**Steel-manned rebuttal** (Round 1):
> KSD is per-slice (1-D RKHS Stein); Hyvärinen-Hutchinson is multivariate full-d. Even if KSD wins per-slice, Hyvärinen could win on *multivariate-cluster-shape failures* that per-slice tests miss (the Cramér-Wold finite-sample blind spot identified in batch-6 Idea 6 reasoning, before that idea was reframed for d=384 concentration). The 5-way bake-off is informative regardless of which wins because Hyvärinen + KSD together resolve "per-slice vs multivariate" as a corner.

**Source**: auto-steelman.

**Persona response** (Round 1): "Per-slice vs multivariate distinction is mechanism-level real. But if KSD wins clearly by ≥ 0.4 pp on the per-slice bake-off, the multivariate alternative needs to *outperform* KSD by enough margin to justify the structural change — bake-off needs paired controls. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 PASS · S2 WARN · S3 PASS · S4 WARN · S5 PASS · S6 WARN — **0 FAIL + 3 WARN**.

**Rule fired**: Rule #5 (`0 FAIL + 3-4 WARN → TOY`).

**Verdict**: 🧪 **TOY EXPERIMENT FIRST**. **Confidence**: 🟢.

**Justification**: Cheapest addition in batch — slots into the existing per-slice bake-off as 5th arm. Convex-decoy sanity is mandatory pre-flight (1-hr CPU, free). High confidence because feasibility is trivial and the bake-off resolves the per-slice/multivariate corner regardless of outcome.

---

## Toy Experiment Design

**Idea being toyed**: Hyvärinen+Hutchinson as 5th arm of per-slice statistic bake-off.
**Triggered by**: Stage 4 convex-decoy WARN + Stage 6 KSD-might-already-cover WARN.

### Goal
(a) Verify Hyvärinen escapes convex decoy at init (CPU sanity). (b) Measure probe lift / parity against the EP / Hermite / KSD / Riesz-MMD per-slice family at matched WC.

### Setup
- **Phase A (CPU sanity, 1 hr free)**: 1000 SGD steps on synthetic `Z = randn(512, 384)`, fixed encoder, learn `s_θ`; measure `‖s_θ(z) + z‖_F` and `‖Cov(z) − I‖_F`. Expectation: `s_θ` converges toward `−z` while `‖Cov − I‖_F` stays at its random-init value — confirms `s_θ` alone cannot escape but is not trapping the joint optimization.
- **Phase B (ImageNet-10, ~6 GPU-h)**: Hyvärinen-only arm at ASHA-best (lr, wd, λ), 3 seeds, 100 ep. Add to the existing 4-way bake-off as 5th arm (incremental cost is the Hyvärinen arm).
- **Model**: ViT-S/16 + LeJEPA, SIGReg term replaced with `L_sm`.
- **Budget**: Phase A free; Phase B ~6 GPU-h (3 seeds × 100 ep × 2 GPU-h/run = 6 GPU-h).

### Success criterion
- Phase A: `‖s_θ + z‖_F` decreases AND `‖Cov(z)−I‖_F` does NOT decrease (proves decoy is reachable in isolation; needs joint training to actually shape `z`).
- Phase B: Hyvärinen-arm linear probe ≥ baseline-EP − 0.3 pp (parity floor) AND wall-clock ≤ EP × 1.10. If Hyvärinen *beats* the bake-off winner by ≥ 0.4 pp non-overlap → graduate as new SIGReg-term default.

### Confound check
3-seed EP-baseline within the same bake-off; noise estimate σ ~ 0.5 pp from prior batches.

### Falsification thresholds
| Observation | Action |
|-------------|--------|
| Phase A: `s_θ + z` doesn't decrease | KILL — score model can't even regress its target |
| Phase A passes; Phase B Hyvärinen < EP − 0.3 pp | REFRAME — per-slice EP is sufficient, multivariate adds nothing |
| Phase A passes; Phase B Hyvärinen ties bake-off winner ±0.3 pp | KEEP as compose-mode option |
| Phase A passes; Phase B Hyvärinen beats winner by ≥ 0.4 pp non-overlap | FULL SEND as new SIGReg-term default |
| Wall-clock > EP × 1.20 | REFRAME — efficiency loss negates the gain |

### Estimated cost
Phase A: free. Phase B: 6 GPU-h.

### Estimated time
1 hr CPU + 2 hr wall-clock (3-GPU parallel) = ~3 hr.

### Re-vet trigger
`/vet-ideas --given-toy ./hyvarinen-bakeoff-results.md idea-2-batch-7`.

### Salvageable / Resurrection-eligible
Yes / Yes.
