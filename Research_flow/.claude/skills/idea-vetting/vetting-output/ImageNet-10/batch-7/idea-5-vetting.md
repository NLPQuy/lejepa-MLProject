# Idea 5 Vetting — Neural-collapse ETF prototypes (online k-means + simplex-ETF cosine target)
**Source**: `ideation-output/ImageNet-10/batch-7.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Maintain K=20 learnable prototypes; assign embeddings by nearest-cosine; penalize pairwise prototype cosines toward simplex-ETF target `−1/(K−1)`. Push embeddings toward assigned prototype.

Pattern P5 (Decompose), Tier 3, Scope enhance-existing. Composite 1.78 (#5 of batch).

---

### Stage 1: Problem Framing
**Persona**: Advisor.

**Attack 1**: "Neural collapse (Papyan-Han-Donoho 2020) is a *supervised* phenomenon at terminal training. The simplex-ETF emerges from cross-entropy with class labels. Applying the *target* without the *driving signal* (labels) is decorative — there's no theoretical reason ETF prototypes should help unsupervised."

**Steel-manned rebuttal** (Round 1):
> rETF-semiSL (arXiv:2508.10147, Aug 2025) and 'Guiding Neural Collapse' (arXiv:2411.01248, Nov 2024) explicitly target the ETF geometry in semi-supervised and supervised settings without waiting for terminal-phase emergence. The framework transfers: replace labels with online k-means cluster assignments. Welch 1974 *IEEE TIT* proves simplex-ETF is the maximum-equiangular configuration regardless of how the prototypes are derived — the *target geometry* is well-defined for any K-prototype set, supervised or not.

**Source**: auto-steelman.

**Persona response** (Round 1): "Active-ETF-targeting is published. But k-means assignments are *much* noisier than labels — the prototype updates may not converge to a meaningful clustering on Imagenette's 10 classes with K=20 prototypes. Framing transfer is partial. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "SwAV (Caron et al. NeurIPS 2020) maintains learnable prototypes with cluster assignments AND uses Sinkhorn-Knopp balancing — *exactly* the architecture proposed here. The ETF cosine penalty is the only delta, and that's a single-line loss addition."

**Steel-manned rebuttal** (Round 1):
> SwAV uses prototypes as classifier weights and trains them via cross-prediction (view-1 predicts view-2's assignment). The present idea uses prototypes as *geometric anchors* with explicit ETF-cosine target on the prototype-to-prototype matrix. SwAV's prototypes drift to whatever helps cross-prediction; ETF-targeting *constrains* the geometry to the Welch-bound saturator. Different objective, different inductive bias. The composition `SwAV + ETF-penalty` would be a genuine extension, not a duplicate.

**Source**: auto-steelman.

**Persona response** (Round 1): "Geometric-anchor vs cross-predictor distinction is real but narrow. The killer comparison is `SwAV-frozen-prototypes vs SwAV+ETF-penalty` — and that's exactly the experiment that needs to run, not `LeJEPA+ETF` (which has different baseline). WEAKENED — the proper baseline is SwAV-style, not LeJEPA-style."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Mechanism axis = ETF-cosine penalty (rETF-semiSL Aug 2025). Application axis = SSL pretraining with online k-means (SwAV NeurIPS 2020). Synthesis = combine them. Novelty score: low — the synthesis is 1 hop in the literature graph."

**Steel-manned rebuttal** (Round 1):
> The synthesis has not been published per the search log. Climb-mode does not require novelty grandeur; it requires probe gain. If `ETF + online k-means + LeJEPA` adds ≥ 0.5 pp over baseline LeJEPA, the climb-mode goal is met regardless of novelty score.

**Source**: auto-steelman.

**Persona response** (Round 1): "Climb-mode admissible. But ETF prototypes on Imagenette with K=20 prototypes feels under-specified — Imagenette has 10 classes, and the K=20 choice is `2 × C`. The optimal K is *another* HP, undermining the 'single-λ branding' goal. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 4: Theory Grounding (lite)
**Persona**: Theorist.

**Attack 1**: "**Cramér-Wold↔ETF redundancy prerequisite** (flagged by ideator §Risks): SIGReg's N(0, I) target on a unit-norm projector output may *already* induce approximate-ETF prototype emergence — N(0, I) on the sphere is the maximum-entropy configuration, and prototype-mean cosines on a uniform sample tend to `−1/(K−1) ± O(1/√d)` at large d. If this is the case, ETF penalty is redundant."

**Steel-manned rebuttal** (Round 1):
> The argument is that *expected* cosine under uniform spherical sampling is 0, not `−1/(K−1)`. The ETF geometry is a *specific* configuration of K points (vertices of a simplex), not the mean over random spherical samples. SIGReg constrains the embedding marginal but does not pick out the simplex configuration — those K prototypes are *free parameters* that need their own loss. The redundancy concern conflates 'embeddings are N(0,I)' with 'prototypes form a simplex'.

**Source**: auto-steelman.

**Persona response** (Round 1): "Argument distinguishes marginal-shape from prototype-shape. But the prerequisite check the ideator flagged (`search 'Cramér–Wold neural collapse simplex ETF'`) is mandatory pre-flight — if a theoretical-equivalence result exists, the entire idea is killed. WEAKENED — defensible but theoretically uncertain."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "Online k-means + prototype updates + Sinkhorn-Knopp balanced assignment (to avoid cluster collapse) + ETF cosine penalty + cluster-loss + K hyperparameter — 4 new components, 2 new HPs. Effort is L, not M."

**Steel-manned rebuttal** (Round 1):
> SwAV ships exactly this infrastructure; reusing it is ~50 LoC. K = 20 is a fixed default (2× ground-truth classes per Imagenette mini-sweep recommendation in idea §Risks). ETF penalty is `~5 LoC`. Total addition ~ 100 LoC. M effort holds.

**Source**: auto-steelman.

**Persona response** (Round 1): "SwAV ships it, but integrating it cleanly with LeJEPA's no-EMA architecture is non-trivial (SwAV uses momentum encoder; LeJEPA does not). The integration cost is the unspoken complexity. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "SwAV (no ETF, no LeJEPA) at matched parameters/WC is a *direct* killer-baseline comparison. The idea is 'LeJEPA + ETF prototypes' which has *two* deltas vs SwAV (no momentum encoder + ETF penalty) — the experiment as written cannot isolate the ETF contribution."

**Steel-manned rebuttal** (Round 1):
> The falsification 3-arm `SIGReg-only / SIGReg+L_NC / L_NC-only` *does* isolate the ETF contribution within the LeJEPA setup. SwAV comparison is *cross-framework* and would be apples-to-oranges (different architectural choices). The within-LeJEPA 3-arm is the right scope.

**Source**: auto-steelman.

**Persona response** (Round 1): "Within-LeJEPA isolation is fair, but the question 'does ETF help LeJEPA specifically?' is narrower than the headline 'ETF helps SSL pretraining'. If LeJEPA + ETF beats LeJEPA-baseline but is *worse* than SwAV-baseline, the climb-mode goal is unclear. WEAKENED — falsification design measures within-framework delta but not cross-framework dominance."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 WARN · S2 WARN · S3 WARN · S4 WARN · S5 WARN · S6 WARN — **0 FAIL + 6 WARN**.

**Rule fired**: Rule #6 (`0 FAIL + ≥ 5 WARN → REFRAME`).

**Verdict**: 🔁 **REFRAME**. **Confidence**: 🟡.

**Justification**: Every stage WARNed — no single death blow, but the cumulative uncertainty (Cramér-Wold↔ETF redundancy, k-means assignment noise, K hyperparameter, SwAV-vs-LeJEPA scope, SwAV-as-killer-baseline) signals the idea is mis-shaped. The redundancy prerequisite is the cheapest disambiguation.

---

## Reframe direction

**Reframe**: do not implement as proposed. Instead:

1. **Prerequisite-only pass** (`0-cost`): Search `"Cramér–Wold neural collapse simplex ETF"` AND `"isotropic Gaussian prototype simplex ETF"` in the literature. If a direct theoretical-equivalence result exists, **KILL** the idea definitively. If no equivalence, proceed to step 2.
2. **Empirical pre-check** (`0 GPU-h`): on any saved LeJEPA baseline checkpoint, compute the K-means (K=20) cluster-mean pairwise cosine matrix; compare to the simplex-ETF target `−1/19 = −0.053`. If the empirical mean cosine is already within `±0.02` of the ETF target, ETF prototypes are *empirically redundant* — **KILL** definitively.
3. **If both pre-checks pass**, re-submit as a fresh idea with SwAV-style baseline (not LeJEPA-only) and K-sweep included in the experimental design.

**Re-vet condition**: `/vet-ideas --resurrect idea-5-batch-7 --counter-argument "<results of pre-checks>"` if both pre-checks pass.

**Salvageable**: Only with the prerequisite-pass discipline. As written, the idea is too speculative for the cost.
**Resurrection-eligible**: yes, conditional on pre-checks passing.
