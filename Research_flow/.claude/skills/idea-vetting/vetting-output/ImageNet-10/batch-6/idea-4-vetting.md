# Idea 4 Vetting — Sinkhorn divergence invariance term
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P3 (Replace) · **Tier**: 3 · **Source**: ideation batch-6 Idea 4

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`.

**Attack 1.1**: "LeJEPA's invariance term is `(z̄ − z).square().mean()` — a *centred* per-pair L². The proposal's framing as 'per-sample L²' is incorrect; the existing term is already a soft alignment. Sinkhorn replaces a per-pair-soft alignment with distribution-level alignment — a real change, but the framing in the proposal is sloppy."
- Steel-manned rebuttal: Acknowledged — the existing term pulls each `z_i^v` toward the per-image mean `z̄_i = mean_v z_i^v`, which is per-image (not per-pair) but still has 0 OT-permutation freedom across i. The Sinkhorn replacement opens that permutation freedom across-i; the framing is correct in *direction* even if the formula was loosely stated. Sharpen the proposal: "replace per-image-mean alignment with batch-level distribution alignment".
- Persona verdict: ✅ DEFLECTED (with sharpening).

**Verdict**: PASS.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`.

**Attack 2.1**: "SinSim (arXiv:2502.10478, Feb 2025) does exactly this on SimCLR. **You are not the first.** What does Imagenette / LeJEPA add that SinSim's paper didn't show?"
- Steel-manned rebuttal: SinSim is on SimCLR (contrastive); LeJEPA is non-contrastive with SIGReg as the collapse-prevention term. The interaction between Sinkhorn invariance and SIGReg is unmeasured. The proposal's mid-gain estimate (+0.6 pp) is properly conservative — SinSim reports +1.5 pp on SimCLR/CIFAR but no number for non-contrastive SSL. Novelty = "first non-contrastive Sinkhorn invariance".
- Persona verdict: ⚠️ WEAKENED — narrow novelty. Could be one paper away from being scooped.

**Attack 2.2**: "Caron's SwAV (NeurIPS 2020) already uses Sinkhorn — but for *clustering*, not invariance. Mention?"
- Steel-manned rebuttal: SwAV's Sinkhorn enforces equipartition over cluster prototypes, a different target. Citing for completeness is fair; it does not undermine novelty.
- Persona verdict: ✅ DEFLECTED.

**Verdict**: PASS. 1 DEFLECTED / 1 WEAKENED.

## Stage 3 — Novelty Decomposition
EXTENDS (SinSim mechanism + non-contrastive substitution). Modest novelty.

## Stage 4 — Theory Grounding (lite)
**Attack 4.1**: "Permutation-free OT may decouple image identity from embedding. Specifically, if the OT plan maps view-1 of image i to view-2 of image j (i ≠ j), the invariance loss is satisfied with a *random* mapping that has nothing to do with the image semantics. This is collapse via permutation."
- Steel-manned rebuttal: At low ε (e.g. 0.001), Sinkhorn → Wasserstein-2 with sparse plan; at high ε, → MMD with full-coverage plan. The 50/50 mix `L_inv = 0.5·per-pair-MSE + 0.5·Sinkhorn` (in the proposal's risk-mitigation) anchors per-pair identity. Plus SIGReg's collapse-prevention term is unchanged — global collapse to a permutation-free degenerate is blocked by SIGReg.
- Persona verdict: ⚠️ WEAKENED — defensible but needs the mechanism-check arm in falsification (per-image cos must NOT drop to ~0). Already in the proposal.

**Verdict**: WARN.

## Stage 5 — Feasibility
`geomloss` is mature; ~20 LoC swap. ε is a new HP but bindable to Idea 1 controller. **PASS**.

## Stage 6 — Killer Baseline
**Attack 6.1**: "Killer baseline = per-pair MSE invariance + SIGReg (current LeJEPA). 3-arm: baseline / Sinkhorn-only / 50/50 mixed. The 50/50 mixed arm is the most likely winner — but a sharper test is: if 50/50 beats baseline by ≥ 0.4 pp, does removing the per-pair MSE term (Sinkhorn-only at the same ε) also win? If only the mixed arm wins, the gain is the *regularization* of per-pair (not Sinkhorn's distributional alignment) — REFRAME to 'softened per-pair MSE'."
- Steel-manned rebuttal: The mechanism-check in the falsification covers this — per-image cos must drop under Sinkhorn-only relative to mixed; if it doesn't drop, OT freedom isn't being used.
- Persona verdict: ✅ DEFLECTED (mechanism check is sharp).

**Verdict**: PASS.

## Stage 8 — Decision Gate
Stages: 1 PASS / 2 PASS / 3 WARN / 4 WARN / 5 PASS / 6 PASS. **2 WARN, 0 FAIL → FULL SEND** per decision-logic.md priority 4.

But: gain mid +0.6 pp is small relative to risk; the 50/50 mix sharpening (Stage 4) is required to avoid permutation collapse. **Downgrade to TOY** for the 1st phase (cheap sanity), then FULL SEND if Phase A passes.

**Verdict**: 🧪 **TOY → FULL SEND** · Confidence 🟢

### Toy Experiment Design
- **Phase A (~15 GPU-h)**: 100-ep ImageNet-10 at fixed (λ, lr, wd) from ASHA, 3 seeds, 3-arm: baseline-MSE / Sinkhorn-only (ε=0.05) / 50/50 mixed. Decision: best arm ≥ 0.4 pp non-overlap vs baseline; mixed arm wins → graduate as new default invariance term; Sinkhorn-only wins AND per-image cos dropped < 0.5 → REFRAME (OT-permutation collapse); baseline wins → KILL.
- **Phase B (skip — Phase A is decisive)**: only fires if a second ε is worth scanning.
- **Dependency**: ASHA Step-0. Independent of all other batch-6 ideas.
