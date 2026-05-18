# Idea 6 Vetting — Saliency-guided crop region sampling
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P8 (Augment — data-side sampler change) · Tier: 1
- Proposed gain: +0.3 / +0.8 / +1.5 pp
- Effort: S · Feasibility: 5/5
- Composite (batch-5): 2.7 (top of batch)

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor.*

**Attack A1.1**: "DINO-style multi-crop was *designed* assuming random cropping; biasing it to saliency may reduce the diversity that makes multi-crop work."
**Steel-manned rebuttal**: The idea only biases the 2 *global* views (which currently waste ~20-30% on background); the 6 local views keep uniform sampling and provide the diversity. Saliency-bias on globals + uniform locals is exactly the ContrastiveCrop recipe (CVPR 2022) shown to lift linear probe.
**Persona response**: ✅ DEFLECTED. The split-treatment is correct.

**Verdict**: PASS.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter.*

**Attack A2.1**: "ContrastiveCrop (CVPR 2022) and arXiv:2210.16776 (2022) already did saliency-guided cropping for contrastive SSL. Hard duplicate."
**Steel-manned rebuttal**: Method exists; never applied to LeJEPA / SIGReg / Imagenette specifically. Engineering-and-measurement counts as a climb-mode idea when the result is uncertain.
**Persona response**: ⚠️ WEAKENED — clear EXTENDS. Climb-mode admissible; paper venue would push back hard.

**Verdict**: PASS. Novelty: EXTENDS (almost DUPLICATE of method).

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "Lowest novelty in the batch. Almost a pure transfer."
**Steel-manned rebuttal**: True in publication-novelty terms; high value in benchmark-climb terms (S effort, T1 evidence, ~1 pp ceiling that compounds with everything).
**Persona response**: ⚠️ WEAKENED.

**Verdict**: WARN. Lowest novelty in batch — explicitly acknowledged.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1**: "Saliency biases the *crop-content* distribution, which interacts with SIGReg's marginal-Gaussianity claim. If crops are object-only, the embedding becomes systematically biased toward object-coding, breaking Cramér-Wold's isotropy claim on natural-image embeddings."
**Steel-manned rebuttal**: SIGReg enforces isotropy on the embedding *conditional on the training distribution*, whatever that distribution is. Biasing crops toward objects shifts the data distribution but does not break the Gaussianity-of-embedding-marginals claim (which holds for any training distribution).
**Persona response**: ✅ DEFLECTED. Distribution shift is fine.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "Per-image saliency = `local_std(image_gray, kernel=5)` is naive; on Imagenette's 'tench' class (mostly water) it'll concentrate on splashes, not the fish. ContrastiveCrop uses the *encoder's attention map*, which requires a warm-up phase."
**Steel-manned rebuttal**: The idea proposes a mixture `(1-α)·Uniform + α·Saliency` to mitigate exactly this; ablate α ∈ {0.3, 0.6, 1.0}. The encoder-attention bootstrap is a stretch improvement.
**Persona response**: ⚠️ WEAKENED — local-std saliency is genuinely weak; the encoder-attention version is what the published gains use. Naive local-std may show only +0.2 pp.

**Refinement (Round 2)**: Two-arm design: (a) local-std saliency at α=0.6; (b) encoder-attention saliency (bootstrap after epoch 50) at α=0.6. The bootstrap version is the right comparison to the published ~1 pp gain.

**Verdict**: PASS with refinement.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Imagenette is *already* object-centric (10 specific ImageNet classes, each curated). The gap between random-crop and saliency-crop is smaller than on raw ImageNet because there's less non-object area to discard."
**Steel-manned rebuttal**: 224×224 crop at scale=0.3 keeps ~30% area; with random center, on a 500×400 image that's ~half-object/half-background. Even on a curated subset, ~30% of global crops are non-object. The 2025 paper (arXiv:2504.19824) measures CIFAR-10 (more object-centric than Imagenette) and reports ~1 pp lift.
**Persona response**: ⚠️ WEAKENED — the published CIFAR-10 lift is the strongest analog; Imagenette is in between CIFAR-10 and ImageNet on object-centricity. Expected gain on Imagenette is plausibly 0.3-0.8 pp (lower band of the idea's claim).

**Refinement (Round 2)**: Down-revise mid gain to +0.5 pp (from +0.8 pp); high band to +1.2 pp.

**Verdict**: PASS with refinement.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 PASS · 2 PASS · 3 WARN · 4 PASS · 5 PASS-w-refinement · 6 PASS-w-refinement · UNREBUTTED = 0, 1 WARN.

**Verdict**: ✅ **FULL SEND** 🟢

**Confidence**: 🟢 — drop-in, S effort, T1 evidence, very low risk. Lowest novelty in batch is a feature in climb-mode, not a bug.

**Refinement applied**: 2-arm design (local-std saliency vs encoder-attention saliency at α=0.6); mid gain revised to +0.5 pp.

**Composite × confidence**: 2.7 × 1.0 = 2.7. **Top of batch-5.**

**Ship-now action**: Run alongside batch-2 ASHA — the saliency precompute is per-image and one-time; the crop sampler is a 10-line change.
