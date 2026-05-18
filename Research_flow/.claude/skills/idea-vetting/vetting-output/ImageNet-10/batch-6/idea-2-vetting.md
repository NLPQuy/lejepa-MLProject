# Idea 2 Vetting — Register tokens for ViT-S/16
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P3 (Replace) · **Tier**: 1 · **Source**: ideation batch-6 Idea 2

## Pre-vet flag
**⚠️ HARD DUPLICATE WARNING**: batch-1 Idea 3 ("Register tokens") is currently in `_toy_queue.md` (Active) at 8 GPU-h with explicit falsification trigger:
> "LeJEPA CLS-concat probe is structurally insulated from patch-token artifacts (Darcet ICLR 2024 §5)."

The proposed idea is the *same mechanism, same paper, same backbone*. Stage 2 will fire on this.

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`. Stance: same hammer, same nail — but is there new evidence?

**Attack 1.1**: "What in batch-6's framing is different from the batch-1 proposal that is sitting in the TOY queue right now?"
- Steel-manned rebuttal: Batch-6 framing adds **two 2026 papers** that were not in the batch-1 vetting: (a) arXiv:2603.25803 (cross-architectural reassessment) confirming register gains are architecture-dependent and quantifying when they help; (b) arXiv:2506.08010 (inference-time-only registers) — neither was available 5 months ago. The batch-6 falsification test ALSO adds a mechanism-check (artifact-tail-disappearance check) absent from the batch-1 TOY decision rule.
- Persona verdict: ⚠️ WEAKENED — the new papers refine the *risk model* (architecture-dependence quantified), but the *core decision rule* of the batch-1 TOY ("Δ_probe ≥ 0.5 pp + non-overlapping seed range → graduate") is unchanged. The right action is **NOT a new vetting** — it's to **promote the existing batch-1 TOY** to higher priority and add the mechanism-check to its decision rule.

**Verdict**: PASS but with **redirect-to-existing-TOY** flag.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`. Stance: this exact idea has been killed (almost) before, in our own logs.

**Attack 2.1**: "Per `_toy_queue.md` Active, batch-1 Idea 3 IS the same idea. Per `_killed_ideas.md`, the killing falsification trigger is **LeJEPA CLS-concat probe is structurally insulated from patch-token artifacts**. Darcet ICLR 2024 §5 explicitly documents this: register-token gains accrue on **dense prediction** and **patch-feature-based** downstream (segmentation, retrieval), not on [CLS]-only / [CLS]-concat linear probe. The batch-6 ideation framing inflates the linear-probe gain from the published number."
- Steel-manned rebuttal: The standard LeJEPA linear probe uses **CLS-concat from the last 2 layers + LayerNorm + AdamW** (per CLAUDE.md §5 "Linear Probe Evaluation"). Darcet §5 indeed shows the artifact effect is most-strongly felt in *patch* tokens, not CLS — but CLS at the last layer indirectly attends to all patches (the artifact tokens included), so contaminated patches DO leak into CLS via the final attention block. Empirically Darcet Table 2 shows +0.4–1.0 pp on ImageNet linear probe across DINOv2 backbones — a real, if smaller-than-dense, effect. The published number is not inflated; it is the published linear-probe number.
- Persona verdict: ⚠️ WEAKENED — gain is real but smaller than dense-prediction gain; batch-6 ideation listed mid +0.7 pp, which is on the high end of Darcet's CLS-linear-probe range (0.4–1.0 pp). Acceptable. **BUT**: this is precisely what the batch-1 TOY was designed to measure. Running a *new* full vetting on the same idea is duplicate compute.

**Verdict**: ⚠️ SOFT-FAIL on duplicate-with-active-TOY grounds. Per skill discipline (`_killed_ideas.md` + active TOY), the correct action is **REFRAME to "promote existing batch-1 TOY"**, not a new vetting commit.

Rebuttal: 0 DEFLECTED / 2 WEAKENED / 0 UNREBUTTED. Verdict downgrade applied.

## Stage 3 — Novelty Decomposition
> Adopting persona: `Critical Reviewer`.

Mechanism identical to the published Darcet paper. **EXTENDS bordering DUPLICATE** (batch-6 ideation acknowledged this).

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
Mechanism: registers act as global-scratchpad tokens. Theoretical claim ("artifact tokens form because of no-EMA-driven gradient flow") is FAIR-team's hypothesis — Darcet did not isolate the cause. LeJEPA has no EMA, so the artifact mechanism may NOT activate. **WARN** (per Devil's-advocate already raised in batch-6 ideation).

## Stage 5 — Feasibility
`timm.create_model("vit_small_patch16_224", num_register_tokens=4)` if timm ≥ 0.9.13. **PASS**.

## Stage 6 — Killer Baseline
> Adopting persona: `Skeptical Empiricist`.

**Attack 6.1**: "Killer baseline = run the batch-1 TOY (8 GPU-h) and decide. Batch-6 has NO new evidence to short-circuit the toy. So the killer baseline IS the existing TOY."
- Steel-manned rebuttal: True. The right next action is *not* to re-vet but to run the TOY. The batch-6 proposal can be folded into the TOY by adding the artifact-tail mechanism-check to its decision rule.
- Persona verdict: ✅ DEFLECTED on the technical merit (TOY is the right next step); UNREBUTTED on "new vetting was unnecessary".

**Verdict**: WARN. Rebuttal: 1 DEFLECTED / 0 WEAKENED / 1 UNREBUTTED (process critique).

## Stage 8 — Decision Gate
> Adopting persona: `Advisor (PI mode)`.

Stages: 1 PASS / 2 SOFT-FAIL (duplicate-with-active-TOY) / 3 WARN / 4 WARN / 5 PASS / 6 WARN. **1 FAIL + 3 WARN → REFRAME** per decision-logic.md priority 7.

**Verdict**: 🔁 **REFRAME** · Confidence 🟢

### Reframe direction
**Do NOT run new vetting compute or queue a new TOY. Instead:**
1. **Promote the existing batch-1 Idea 3 TOY** (8 GPU-h, currently `queued`) to **Priority 1** in `_toy_queue.md ## Active`.
2. **Augment the batch-1 TOY's decision rule** with the batch-6 mechanism-check: "in addition to Δ_probe ≥ 0.5 pp graduating, verify the artifact-tail in token-norm histogram disappears in the registered-arm (cf. Darcet Fig. 2). If Δ_probe ≥ 0.5 pp but artifact tail did not exist in the baseline either, downgrade to 'free-lunch confirmed, no theoretical insight' and ship anyway."
3. Add the 2026 cross-architectural reassessment + inference-time-register papers to the batch-1 TOY's "Source" field for future audit.
4. **Do not re-cite this as a batch-6 idea in proposal log**. It already counts as batch-1 Idea 3.
