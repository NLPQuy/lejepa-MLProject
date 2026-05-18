# Idea 3 Vetting — iBOT-style masked-patch SIGReg auxiliary
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P1 (Combine) · **Tier**: 2 · **Source**: ideation batch-6 Idea 3

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`.

**Attack 1.1**: "Why is per-patch SIGReg the right next move when batch-4 Idea 6 (MAE pixel-recon aux, 75 GPU-h TOY) is still queued and untested? Two patch-level auxiliaries competing for the same slot is wasteful."
- Steel-manned rebuttal: They are *mechanistically different*. MAE-aux is pixel-space reconstruction (rgb prediction); iBOT-SIGReg is feature-space normality on the predicted-patch features. The published evidence on small-data linear probe favors feature-space (iBOT 82.3 % vs MAE 68 % at ViT-B/IN-1K). Running iBOT-SIGReg first dominates the MAE-aux TOY priority.
- Persona verdict: ✅ DEFLECTED — supersedes MAE-aux on prior evidence.

**Verdict**: PASS.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`.

**Attack 2.1**: "iBOT's per-patch loss is *cross-entropy on the online tokenizer's soft labels*, not SIGReg. Adapting iBOT to SIGReg is novel-as-mechanism but rests on the unproven assumption that per-patch features should be marginally N(0, I_d) — which they SHOULDN'T be, since adjacent patches are spatially correlated."
- Steel-manned rebuttal: SIGReg already operates on the *batch* of image-level embeddings under the assumption that, *across the batch*, the marginal is approximately Gaussian. The per-patch extension is "across the batch × patches, the per-patch marginal is approximately Gaussian". Spatial correlation within an image biases this — but at batch=512, the within-image correlation is dwarfed by between-image variability. The claim is no stronger than the original LeJEPA assumption; just at larger N.
- Persona verdict: ⚠️ WEAKENED — defensible but unverified. Should be a synthetic-data sanity gate.

**Attack 2.2**: "I-JEPA (arXiv:2301.08243) is the LeCun-lab successor to iBOT and is *exactly* 'predict masked patches in feature space without targets'. The proposal is closer to I-JEPA than iBOT; calling it 'iBOT-style' is misleading and the relevant baseline is I-JEPA, not iBOT."
- Steel-manned rebuttal: Acknowledged in batch-6 ideation's source-inspirations (I-JEPA listed as supporting). I-JEPA without SIGReg is the de-facto baseline; the proposal is I-JEPA's predictor head + SIGReg on the predicted patch features in place of I-JEPA's self-distillation loss. The novelty is the loss substitution, not the architecture. Relabel as "I-JEPA + SIGReg-on-patches".
- Persona verdict: ⚠️ WEAKENED — relabeling required; ideation framing was loose.

**Verdict**: PASS (no hard duplicate; relabel required). 0 DEFLECTED / 2 WEAKENED.

## Stage 3 — Novelty Decomposition
**EXTENDS** (I-JEPA mechanism + SIGReg loss substitution). Net novelty: substitution of loss in published architecture. Modest.

## Stage 4 — Theory Grounding (lite)
**Attack 4.1**: "Cramér-Wold guarantees uniformity on the sphere only if the slice directions are isotropic w.r.t. the SAMPLE distribution. If per-patch features are clustered by spatial position (which they are, due to position embedding), the isotropic-slice assumption fails."
- Steel-manned rebuttal: After projection through the predictor head (3 transformer layers, learnable mixing across positions), the position-conditional correlation drops substantially. SIGReg is applied AFTER the predictor, not on raw patch tokens. The predictor can be seen as "the part of the network that makes per-patch features sample-able as i.i.d.-from-Gaussian".
- Persona verdict: ⚠️ WEAKENED — theoretically intact-but-stretched. Empirical sanity needed (RankMe on per-patch predictor output should approach RankMe on image-level z within ~20 ep).

**Verdict**: WARN.

## Stage 5 — Feasibility
> Adopting persona: `Pragmatic PM`.

3M-param predictor + masking pipeline = ~2 days eng. Stable-pretraining already has MAE-aux scaffolding from batch-4 (TOY, deferred). Reuse possible. Wall-clock overhead +15 %. **PASS** with M-effort flag.

## Stage 6 — Killer Baseline
> Adopting persona: `Skeptical Empiricist`.

**Attack 6.1**: "Matched-wall-clock baseline is the right control (predictor adds 15 % step cost). If the +15 % cost is instead spent on +15 % more epochs of baseline LeJEPA, does iBOT-SIGReg still win? Most masking-aux papers fail this test."
- Steel-manned rebuttal: The ideation's falsification test ALREADY mandates matched-wall-clock at 100 ep. iBOT @ ViT-B/IN-1K beats DINO by 2 pp at matched epochs and ~1.5 pp at matched wall-clock (iBOT Table 5). On Imagenette ViT-S scaled down conservatively, the matched-WC win should be 0.4–0.8 pp — sharp but not dominant.
- Persona verdict: ⚠️ WEAKENED — published matched-WC win exists but is small; on a small backbone + small dataset, may not survive.

**Attack 6.2**: "head-to-head with MAE-aux (batch-4 TOY) is mandatory. Two patch-aux ideas cannot both ship."
- Steel-manned rebuttal: Agreed. The TOY should be a 3-arm: baseline / MAE-aux / iBOT-SIGReg at matched WC. Whichever wins, the other is killed. This is more efficient than running them sequentially.
- Persona verdict: ✅ DEFLECTED via head-to-head framing.

**Verdict**: WARN. 1 DEFLECTED / 1 WEAKENED / 0 UNREBUTTED.

## Stage 8 — Decision Gate
Stages: 1 PASS / 2 PASS (w/ relabel) / 3 WARN / 4 WARN / 5 PASS / 6 WARN. **3 WARN, 0 FAIL → TOY** per decision-logic.md priority 5.

**Verdict**: 🧪 **TOY** · Confidence 🟡

### Toy Experiment Design
- **Phase A (free, 1 hr CPU)**: synthetic sanity — generate 5k iid patch-style features (with position-embedding-like correlations); verify predictor-head output's per-slice univariate normality test value approaches that of an iid-Gaussian baseline within 200 SGD steps on a toy regression. Decision: if NOT, position correlation defeats the Cramér-Wold argument → KILL.
- **Phase B (~25 GPU-h)**: 100-ep ImageNet-10, 3-arm at **matched wall-clock**: baseline LeJEPA / +MAE-aux (batch-4 TOY) / +iBOT-SIGReg (this idea). 3 seeds each. Decision rule: best aux arm ≥ 0.5 pp non-overlap vs baseline; iBOT-SIGReg ≥ MAE-aux by ≥ 0.3 pp → graduate iBOT-SIGReg, KILL MAE-aux. Else: drop both or graduate the winner.
- **Bind** `λ_patch` to **Idea 1's RankMe controller setpoint** (if Idea 1's Phase B passes) — avoids the extra HP. Otherwise fix `λ_patch = λ_cls / 2`.
- **Dependency**: ASHA Step-0 + (recommended) Idea 1 Phase A.
