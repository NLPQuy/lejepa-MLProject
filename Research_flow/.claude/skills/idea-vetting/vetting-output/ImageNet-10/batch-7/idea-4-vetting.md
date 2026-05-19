# Idea 4 Vetting — RL augmentation policy (REINFORCE on crop parameters)
**Source**: `ideation-output/ImageNet-10/batch-7.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Treat crop parameters (scale, location, jitter) as policy actions; reward = drop in per-image invariance loss; PPO updates every K=100 steps.

Pattern P2 (Transfer), Tier 3, Scope enhance-existing. Composite 1.80. Ideator self-flagged as EXTENDS bordering DUPLICATE.

---

### Stage 1: Problem Framing
**Persona**: Advisor.

**Attack 1**: "Saliency crops (b5 FULL SEND) already covers the 'better crops for SSL' axis with a static prior. The problem framing here is 'replace static with adaptive RL policy'. Is the adaptive-vs-static delta the actual climb-mode goal, or is this a re-framing of the same problem?"

**Steel-manned rebuttal** (Round 1):
> Saliency crops use a *pretrained-saliency* prior — fixed before SSL training begins. The encoder's weakness shifts during training (early: easy invariance; late: hard cluster-boundary patches). A static prior can't track this. RL policy adapts online to current encoder state. The mechanism delta is genuine.

**Source**: auto-steelman.

**Persona response** (Round 1): "Online-vs-static is real but the *magnitude* of the delta is unclear — the encoder's weakness may not shift enough over 600 epochs of small-data SSL to justify online adaptation. WEAKENED — framing is admissible but the marginal value over saliency is uncertain."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "SelfAugment (Reed CVPR 2021, arXiv:2009.07724) is *exactly* this idea: RL policy over augmentations for SSL. The ideator self-flagged this. The delta is the reward signal (per-image-invariance-loss-drop vs rotation-pretext-task). That's a reward-shaping ablation on a published technique, not a new idea."

**Steel-manned rebuttal** (Round 1):
> SelfAugment trains the policy *offline* on a rotation pretext task BEFORE SSL pretraining, then *freezes* the policy and runs SSL with the learned augmentation distribution. The present idea trains the policy *online during SSL pretraining* with a reward signal computed from the SSL objective itself. This is structurally different: offline-pre-policy vs online-co-policy. Hard Views (arXiv:2310.03940) confirms harder views help but still uses heuristic difficulty — not a learned policy. RL-BioAug (Jan 2026, arXiv:2601.13964) is the closest *online* RL-aug-for-SSL precedent and is on EEG, not vision.

**Source**: auto-steelman.

**Persona response** (Round 1): "Offline-vs-online distinction is real — that's the genuine novelty seam. But the engineering scope is large *just to ablate the reward signal*. The proper experiment is 'RL-online vs SelfAugment-offline at matched compute' — that's a single comparison study, not a multi-mechanism contribution. WEAKENED — novelty exists but is narrow."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Application axis: SelfAugment. Reward axis: novel-but-narrow. Synthesis axis: nothing. Total novelty is 'a reward-signal ablation on SelfAugment for vision SSL'. That is a *paragraph* in a future paper, not the headline contribution."

**Steel-manned rebuttal** (Round 1):
> Climb-mode does not require headline novelty; it requires probe gain. If the online reward yields ≥ 1 pp over SelfAugment-offline at matched WC, the climb-mode goal is met. The "narrow novelty" critique applies to publication concerns, not climb-mode utility.

**Source**: auto-steelman.

**Persona response** (Round 1): "Climb-mode framing accepted; but the *cost* of implementing an online PPO loop on top of SelfAugment infrastructure is large for a narrow gain. WEAKENED — climb-mode admissible but cost-efficiency is poor."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 4: Theory Grounding (lite)
**Persona**: Theorist.

**Attack 1**: "REINFORCE has `O(σ_r² / N)` variance where `σ_r` is reward noise; per-image-invariance-loss is *intrinsically noisy* (per-batch fluctuations are large on small data). The policy gradient may be dominated by noise."

**Steel-manned rebuttal** (Round 1):
> PPO (with advantage baselining, GAE, clipping) explicitly mitigates this. EMA of per-image invariance loss as the baseline is the natural advantage estimator. Even at high variance, the *direction* of the gradient is correct in expectation, and the EMA baseline reduces variance by `O(σ_baseline² / σ_r²)`. The first-50-epoch warm-up phase with frozen-random policy avoids the worst-noise regime.

**Source**: auto-steelman.

**Persona response** (Round 1): "Variance reduction is real but PPO + GAE + EMA-baseline is a *lot* of stabilization machinery for what should be a clean idea. WEAKENED — survivable but engineering-heavy."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "PPO loop + advantage estimator + EMA baseline + entropy bonus + warm-up phase + reward computation on held-out subset every K steps = at least 300 LoC of RL machinery. Effort is L, not M as claimed."

**Steel-manned rebuttal** (Round 1):
> stable-baselines3 ships PPO; the integration into LeJEPA is wrapping the crop-sampling step with a policy call. ~200 LoC for the policy net + reward computation. Effort = M is borderline. With stable-baselines3 the time saving brings it back to M.

**Source**: auto-steelman.

**Persona response** (Round 1): "Stable-baselines3 mitigates eng cost; but integrating its tensor lifecycle with PyTorch Lightning's training loop has historically been painful. M-leaning-L. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "Saliency crops (b5 FULL SEND) is the killer baseline. The 3-arm `random / saliency / RL-policy` head-to-head will most likely show `saliency ≥ RL ≥ random` because saliency *encodes prior knowledge* (object localization) that an RL policy has to *learn from scratch*. RL adapts but starts from random; saliency starts from a pretrained-network-derived prior."

**Steel-manned rebuttal** (Round 1):
> The composition path is `saliency-initialized RL policy` — initialize the policy distribution from the saliency map's empirical crop distribution, then let RL adapt online. This *strictly extends* saliency: at init, RL == saliency; over time, RL > saliency by the online-adaptation delta. The proper falsification is `saliency-alone vs saliency-init-RL` — measures *only* the online-adaptation delta, isolating it from the prior-knowledge contribution.

**Source**: auto-steelman.

**Persona response** (Round 1): "Saliency-initialized RL is the right experiment — but the ideator's primary falsification design is `random / saliency / RL-policy` (3-arm with RL from random init). With that design, RL likely loses to saliency. The proposed mitigation is a *reframe* of the falsification, not a defense. WEAKENED leaning UNREBUTTED — the design as written does NOT isolate the online-delta."

**Status after Round 1**: ⚠️ WEAKENED.

**Attack 2** (Round 2 follow-up on Attack 1): "Concretely, if the falsification proceeds as written and RL-from-random loses to saliency, the verdict is KILL — but the *interesting* experiment (saliency-init-RL) was never run. The idea wastes 25 GPU-h on the wrong control."

**Refined rebuttal** (Round 2):
> Accepted: the falsification design needs to be revised to `saliency / saliency-init-RL / random` 3-arm. This is the reframe direction — change the experiment to isolate the online-delta. The original `random / saliency / RL` design is indeed not the right test.

**Source**: auto-steelman.

**Persona response** (Round 2): "Reframe accepted — but this *is* the Stage 6 FAIL condition: the original falsification will not measure what the idea claims. UNREBUTTED on the original design; the reframed design is a separate idea."

**Status after Round 2**: ❌ UNREBUTTED (for original design).

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 1, UNREBUTTED 1.
**Stage verdict**: ❌ FAIL (1 UNREBUTTED on a killer-baseline attack → Stage 6 FAIL).
**Confidence**: 🟢.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 WARN · S2 WARN · S3 WARN · S4 WARN · S5 WARN · S6 **FAIL** — **1 FAIL + 5 WARN**.

**Rule fired**: Rule #2 (Stage 6 FAIL → **KILL** unless reframe). Reframe exists and is concrete: `saliency / saliency-init-RL / random` 3-arm to isolate the online-adaptation delta.

**Verdict**: 🔁 **REFRAME**. **Confidence**: 🟢.

**Justification**: The idea as written runs the wrong control experiment (random-init RL vs saliency, which RL will likely lose). The reframed experiment (saliency-init RL vs saliency-frozen) isolates the genuine novelty (online adaptation over a strong prior). Do NOT queue a new TOY under the original design. Re-submit the reframed idea in a future batch with `saliency-init-RL vs saliency-frozen` as the explicit experiment.

---

## Reframe direction

**Original idea**: REINFORCE/PPO on crop parameters with random-init policy, vs static random crops and static saliency crops.

**Reframed idea**: **Online adaptation of the saliency-derived crop policy via PPO** — initialize the policy from saliency map's empirical crop distribution, train it online with per-image-invariance-loss reward, and compare to *frozen* saliency at matched WC. Primary falsification: `saliency-init-RL beats saliency-frozen by ≥ 0.4 pp non-overlap`. This isolates the online-adaptation delta from the prior-knowledge contribution.

**Engineering implication**: requires saliency-crop infrastructure (b5 FULL SEND already covered) + PPO on top. Effort downgraded to S–M because saliency wiring exists.

**Why this is a separate idea, not a fix**: the original idea's falsification design measures the wrong thing. The reframed idea has a different mechanism story (improves on a strong baseline, not a weak random one), different falsification (saliency-vs-saliency-init-RL), and different effort estimate (smaller, since saliency exists). This warrants a fresh draft, not a salvage.

**Salvageable**: as the reframed idea, yes.
**Resurrection-eligible**: yes — submit reframed idea in batch-8 (under user direction) or via `/vet-ideas --resurrect`.
