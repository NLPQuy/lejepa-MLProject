# Batch-7 Addendum — Idea 8 (CLIP-guided LeJEPA)
**Generated**: 2026-05-19 · **Added per user request**: "add CLIP guidance để add thêm semantic, hoặc align tốt hơn nhờ concept"

## Idea 8: CLIP-text-encoder semantic guidance for LeJEPA (predictive embedding alignment + SIGReg)

- **Pattern**: P1 Combine (graft CLIP-text guidance onto LeJEPA's SIGReg pipeline)
- **Tier**: 1 (in-field — vision-language pretraining literature directly addresses this)
- **Scope**: enhance-existing
- **Two sub-formulations** (the user request is open; both are surfaced for vetting):

### Sub-formulation 8A — CLIP image-encoder feature distillation
Add an auxiliary loss `L_distill = 1 − cos(LeJEPA_encoder(image), CLIP-ViT-L_encoder(image).detach())` for each global view. Frozen CLIP-ViT-L teacher; LeJEPA-ViT-S student aligns to CLIP's representation. Encoder distillation, the strongest probe-gain variant.

### Sub-formulation 8B — CLIP text-anchor predictive alignment
For each image, sample a vocabulary `V = {1000 ImageNet-class-name prompts}`; compute CLIP-text-embeddings `T_v = CLIP-text(v)`. Add an auxiliary head `g_φ` that predicts a soft-assignment over `V` from the LeJEPA encoder output; cross-entropy against a CLIP-image-derived soft target. Semantic-anchor regularization variant.

Both variants keep SIGReg + invariance + multi-crop unchanged; the CLIP-guidance is an additive auxiliary.

### Source inspirations (live-searched 2026-05-19)

- **🚨 Closest prior art (sibling-domain)**: NOVA — *Non-Contrastive Vision-Language Learning with Predictive Embedding Alignment*, Kuhn, Serra, Buettner, [arXiv:2602.00653](https://arxiv.org/abs/2602.00653) (Jan-Feb 2026) — **literally this idea applied to medical imaging**: aligns visual representations to a frozen text encoder (ClinicalBERT) via predictive embedding alignment, **using SIGReg** as the distributional regularizer. The natural-image + CLIP-text version (this idea, sub-formulation 8B) is the direct sibling-domain extension.
- **8A direct prior art**: SILC (ECCV 2024) — CLIP + local-to-global self-distillation; MaskCLIP (CVPR 2023) — masked self-distillation on CLIP; CLIP-KD (arXiv:2307.12732) — empirical study of CLIP distillation. The CLIP-distillation slot is heavily occupied.
- **8B alternative anchor**: CLIP-S⁴ (arXiv:2305.01040) — language-guided self-supervised semantic segmentation via CLIP-text consistency.

### Expected gain
- 8A: +3 to +8 pp 🟢 (CLIP-distillation reliably moves the needle by several pp on Imagenette; *because* the foundation model is much stronger).
- 8B: +0.5 to +2 pp 🟡 (semantic anchors provide weaker signal; NOVA reports moderate gains on its sibling domain).

### Feasibility
- 8A: 5/5 🟢 (10 LoC: load frozen CLIP-ViT-L from HF, add cosine-distill loss; ~2 GB extra GPU memory).
- 8B: 4/5 🟢 (30 LoC: precompute CLIP-text embeddings offline, add a soft-classifier head).

### Effort
- 8A: S. 8B: M.

### Falsification
- 8A: 3-arm baseline-LeJEPA / LeJEPA+CLIP-distill / **frozen-CLIP-direct-probe** (the killer baseline — uses CLIP directly with NO LeJEPA training, just CLIP-ViT-L features + linear probe). Primary: does LeJEPA+CLIP-distill beat frozen-CLIP-direct? Almost certainly NO at Imagenette scale.
- 8B: 3-arm baseline-LeJEPA / LeJEPA+NOVA-replica (CLIP-text version of NOVA) / NOVA-paper-published-result (cross-domain reference if reproducible). Primary: does LeJEPA+NOVA-CLIP beat baseline-LeJEPA by ≥ 1 pp?

### Risks
- **🚨 Stage 1 task-framing violation**: "in-domain SSL on Imagenette" implies no external foundation models. CLIP guidance violates this.
- **🚨 Stage 2 NOVA duplicate (sibling-domain)**: mechanism (CLIP-text + SIGReg + predictive alignment) is fully covered by NOVA's medical-domain instance.
- **🚨 Stage 6 killer baseline**: frozen-CLIP-ViT-L direct probe achieves ~97-98% on Imagenette (10-class CLIP-trained subset of ImageNet-1K). LeJEPA-ViT-S target is ~85-90%. Asymptotically dominated.
- **Information leakage**: Imagenette's 10 classes are in CLIP's training set. Any CLIP-derived signal carries implicit label information about these classes. The "unsupervised" framing is broken.
