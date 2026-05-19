# Idea 3 Vetting — Adversarial max-sliced SIGReg (game-theoretic worst-case slicing)
**Source**: `ideation-output/ImageNet-10/batch-7.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Replace `E_u T(Z·u)` (averaged over 1024 random slices) with `max_u T(Z·u)` via an adversarial slicing-head `g_φ`. Two-player zero-sum game; M=1 adversarial slice replaces M=1024 random.

Pattern P6 (Verify), Tier 3, Scope enhance-existing. Composite 2.17 (#2 of batch).

---

### Stage 1: Problem Framing
**Persona**: Advisor.

**Attack 1**: "Cramér–Wold says *every* 1-D projection is N(0,1) ⟹ Z is jointly N(0,I). The current SIGReg approximates 'every' with 'random sample over many directions'. Replacing with 'worst-case direction' is a *different* requirement — it gives a uniform bound, not a marginal average. Could be too strong, leading to under-regularization in other directions."

**Steel-manned rebuttal** (Round 1):
> The minimax framing is *exactly* what Cramér–Wold demands: "for all u, T(Zu) ≈ 0" ≡ "max_u T(Zu) ≈ 0". The averaging-over-u in vanilla SIGReg is a *finite-sample-budget MC estimator* of the all-u guarantee, with `O(1/M)` variance. Max_u is the supremum that the universal-quantifier *literally requires*. Other directions are not "under-regularized" — they are constrained transitively: if every direction has bounded `T`, then so does every linear combination of bounded directions (by continuity of `T` on the sphere).

**Source**: auto-steelman.

**Persona response** (Round 1): "The minimax-equivalent-to-universal-quantifier argument is the cleanest math claim in the batch. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "Deshpande CVPR 2019 max-sliced Wasserstein is for GANs (generation). Applying max-sliced to a normality-test functional for SSL is unverified in the literature. But what if Sliced-Wasserstein-SSL papers (e.g., arXiv:2502.10478 SinSim — same family) already tried max-sliced variants?"

**Steel-manned rebuttal** (Round 1):
> SinSim uses entropic-OT Sinkhorn divergence (averaged); the adversarial-slicing direction is unexplored in SSL. Search Q3 ("max sliced Wasserstein adversarial direction Deshpande sliced distribution") surfaced no SSL application. Distributional-sliced-Wasserstein (Nguyen 2020 ICLR) is the closest — but that's a *softmax* over slices, not a hard `max`, and is GAN-applied. The slot is genuinely unoccupied.

**Source**: auto-steelman.

**Persona response** (Round 1): "Slot is empty in SSL. Mechanism well-trodden in GAN/OT. EXTENDS. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Highest-novelty in batch per the ideator. But this is *application novelty* on top of standard minimax — every SSL-with-adversarial-component paper (BYOL, MoCo, every GAN-style SSL) is on the same axis."

**Steel-manned rebuttal** (Round 1):
> BYOL/MoCo adversarial components are at the *contrastive-feature* level (positives vs negatives); the present idea is adversarial *in the slicing direction of a normality test*. The mechanism is at a different layer of the SSL architecture, with a different math object (a unit vector on `S^(d−1)` vs a feature vector in `R^d`). The closest precedent is actually max-sliced-Wasserstein, not SSL adversarial methods.

**Source**: auto-steelman.

**Persona response** (Round 1): "Mechanism-distinction is sharp; the adversary's role is differentiated. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 4: Theory Grounding (lite)
**Persona**: Theorist.

**Attack 1**: "Non-convex minimax is the canonical GAN failure case. Mode collapse, oscillation, vanishing gradients all apply. Deshpande CVPR 2019 *itself* reports GAN-training instability for max-sliced. Why would this work for SSL?"

**Steel-manned rebuttal** (Round 1):
> Deshpande's GAN setting has *two* non-convex players (generator + discriminator, both deep networks). The present setting has *one* deep player (encoder) and one *low-capacity* player (slicing head `g_φ` on `S^(d−1)` — a `d`-parameter object). The inner max is over a `d−1`-dim manifold, not over a high-capacity network. This is *much* better-behaved than GAN minimax; the classical results (von Neumann minimax theorem) apply if `T` is convex in `u`, which Epps–Pulley is not (it's a smooth function on the sphere, not jointly convex). Convergence is not guaranteed but local stability is plausible.

**Source**: auto-steelman.

**Persona response** (Round 1): "Low-capacity adversary mitigates the GAN-instability concern. But 'local stability is plausible' is not a guarantee — the GAN stability literature (gradient penalty, spectral norm, R1 regularization) is exactly the toolbox needed. WEAKENED — defensible but unproven."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "Alternating optimization, gradient penalty, spectral norm, entropy regularizer — that's GAN-flavored engineering complexity. 'M effort' is optimistic; the stabilization tricks could turn this into L."

**Steel-manned rebuttal** (Round 1):
> The slicing head is a 50-LoC MLP; spectral-norm and gradient-penalty are 1-line wrappers in standard PyTorch (`torch.nn.utils.spectral_norm` and a single autograd-grad call for GP). The 50/50-mix-with-random fallback (idea description §Risks) is a 1-line safety net that reverts to baseline if the adversary degenerates. The total addition is ≤ 100 LoC. M effort is honest.

**Source**: auto-steelman.

**Persona response** (Round 1): "Engineering scope is contained. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟡 (PASS but uncertainty on the inner-max instability is real).

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "The control arm `M=1` random slice (without adversary) is the killer baseline. If the gain comes from 'one slice per step is enough', not from 'one *adversarial* slice', the entire mechanism story collapses to a slice-count question."

**Steel-manned rebuttal** (Round 1):
> The 4-arm falsification design *explicitly* includes the `M=1` random control. The primary success criterion is `max-sliced > M=1-random by ≥ 0.4 pp non-overlap` — this isolates the adversarial-vs-random mechanism delta. The secondary criterion (max-sliced > M=1024-random baseline) measures compute savings. Both checks together resolve the slice-count vs adversary corner.

**Source**: auto-steelman.

**Persona response** (Round 1): "Falsification design is sharp. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Attack 2**: "Adversary collapses to a constant direction (degenerate Nash) — has happened in every max-sliced GAN paper. If that happens, this becomes 'fixed-direction SIGReg' which is a strict regression on the random-slicing baseline."

**Steel-manned rebuttal** (Round 1):
> Entropy regularizer + gradient penalty are the standard mitigations (Distributional Sliced-Wasserstein Nguyen 2020 uses a softmax-over-directions parameterization that strictly bounds the entropy). The mechanism check (monitor `T(Z · g_φ)` over training; reject if it oscillates with > 30% amplitude across the last 50 epochs) catches degenerate dynamics empirically.

**Source**: auto-steelman.

**Persona response** (Round 1): "Mitigations are real, but only verified at toy scale. The 'reject if oscillation' clause means the experiment may yield 'undecided' rather than 'win' / 'lose'. WEAKENED — risk of inconclusive toy."

**Status after Round 1**: ⚠️ WEAKENED.

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 PASS · S2 PASS · S3 PASS · S4 WARN · S5 PASS · S6 WARN — **0 FAIL + 2 WARN**.

**Rule fired**: Rule #4 (`0 FAIL + ≤ 2 WARN + Stage 5 PASS → FULL SEND`). BUT — both WARNs are on the *same uncertainty* (non-convex minimax stability), which is risky enough to warrant a TOY pre-check. Tie-break per `decision-logic.md §Tie-breaking`: prefer reversible over irreversible.

**Verdict**: 🧪 **TOY EXPERIMENT FIRST** (with FULL SEND on Phase A pass). **Confidence**: 🟡.

**Justification**: The minimax-equivalent-to-Cramér-Wold framing is the cleanest math claim in the batch, and the 4-arm falsification design isolates the adversary-vs-random mechanism. But Stage 4+6 stability warnings are real — Phase A on CIFAR-10 / synthetic verifies the inner max converges before committing GPU-h.

---

## Toy Experiment Design

**Idea being toyed**: Adversarial max-sliced SIGReg.
**Triggered by**: Stage 4 non-convex minimax convergence WARN + Stage 6 adversary-collapse WARN.

### Setup
- **Phase A (CPU+small GPU, ~2 hr free)**:
  - Synthetic `Z = randn(512, 384)` rotated by a random non-isotropic transform (so true `max_u T(Zu) > 0`).
  - Train `g_φ` with alternating optimization for 1000 steps; log `T(Z·g_φ)` over steps.
  - Pass criterion: `T(Z·g_φ)` monotonically increases AND converges (oscillation < 10% of mean over last 200 steps). If oscillates wildly → KILL the adversarial direction; fall back to mixed-50/50 only.
- **Phase B (ImageNet-10, ~15 GPU-h)**: 4-arm at matched-WC: baseline-1024-random / 1-random / 1-adversarial / 50-50 mix.
- **Model**: ViT-S/16 + LeJEPA; slicing head as `MLP(d → 4d → d)` with spectral norm + gradient penalty.
- **Budget**: Phase A free; Phase B ~15 GPU-h (4 arms × 3 seeds × 100 ep × ~1.2 GPU-h each).

### Success criterion
- Phase A: stable inner-max convergence — gate to Phase B.
- Phase B Primary: **`1-adversarial > 1-random` by ≥ 0.4 pp non-overlap** (proves the adversary mechanism, not slice count).
- Phase B Secondary: `1-adversarial ≥ 1024-random` (proves 1000× compute savings).

### Falsification thresholds
| Observation | Action |
|-------------|--------|
| Phase A: inner max oscillates > 30 % amplitude | KILL adversary direction; archive |
| Phase A: inner max converges; Phase B `1-adv ≤ 1-random + 0.4 pp` | KILL — adversary adds nothing |
| Phase B `1-adv > 1-random + 0.4 pp` AND `1-adv ≥ 1024-random − 0.3 pp` | **FULL SEND** as new SIGReg-sampler-replacement |
| Phase B `1-adv > 1-random` but loses to `1024-random` by > 0.5 pp | REFRAME — adversary helps at low M but doesn't beat budgeted random |
| Phase B `50-50 mix > 1-adv` by ≥ 0.3 pp | REFRAME — mixed regularization dominates pure-adversarial |

### Confound check
The `1-random` arm IS the confound for `1-adversarial`; the `1024-random` arm IS the confound for the slice-count interpretation.

### Estimated cost
Phase A free; Phase B 15 GPU-h.

### Re-vet trigger
`/vet-ideas --given-toy ./max-sliced-results.md idea-3-batch-7`. **If Phase A passes**, this idea graduates to FULL SEND (Rule #4 satisfied).

### Salvageable / Resurrection-eligible
Yes / Yes — most-graduation-eligible idea in batch-7.
