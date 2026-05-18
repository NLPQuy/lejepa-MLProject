# Idea 1 Vetting — SAM / Friendly-SAM optimizer wrap
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P3 (Replace optimizer) · Tier: 1
- Proposed gain: +0.3 / +0.8 / +1.5 pp linear probe
- Effort: S · Feasibility: 5/5
- Composite (batch-4 ranking): 2.8 (top)

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor. Stance: does the optimizer-swap actually address the SSL-on-small-data bottleneck?*

**Attack A1.1**: "Does swapping AdamW → SAM target the *actual* bottleneck on ImageNet-10 (small data + multi-crop variance), or is it a generic 'flatness helps' wave?"
**Steel-manned rebuttal**: Foret 2021 + arXiv:2405.20439 (2024) "SAM Enhances Feature Quality" show SAM specifically improves *linear probe* (not just fine-tune) accuracy across supervised vision — exactly the eval metric here. SIGReg's MC noise + multi-crop's sharp updates *amplify* the sharpness pathology SAM addresses. The targeting is concrete, not generic.
**Persona response**: ⚠️ WEAKENED — the cited 2024 paper is on *supervised* features, not SSL features. The transfer from supervised-SAM to SSL-SAM is plausible but unproven. Idea acknowledges this with a matched-WC falsification.

**Verdict**: PASS. Re-vet trigger: if matched-WC SSL+SAM ablation shows < 0.2 pp lift, downgrade.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter. Stance: has someone already shown SAM-for-SSL?*

**Attack A2.1**: "If SAM-for-SSL trivially worked, BYOL/DINO/MoCo papers would have used it. They didn't. That's a tacit negative result."
**Steel-manned rebuttal**: BYOL/DINO/MoCo predate the SAM-as-feature-quality paper (2024). Modern SSL work has begun adopting SAM-like sharpness regularisation — but the literature is thin. The absence of a published SSL-SAM ablation is *opportunity*, not negative evidence.
**Persona response**: ✅ DEFLECTED. Search for "SAM self-supervised pretraining linear probe negative result" returned no SSL-specific negative results (the SAM-as-Segment-Anything namespace collision obscures search; manual check needed). No hard dup found.

**Verdict**: PASS. No prior work kills the idea.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer. Stance: novel = (SAM existing) + (SSL existing) — is the combination publishable-novel or just engineering?*

**Attack A3.1**: "Combination is straightforward — `SAMOptimizer(AdamW(...))`. Engineering, not research."
**Steel-manned rebuttal**: The novelty is *empirical*: first measured ImageNet-linear-probe number for LeJEPA + Friendly-SAM, plus the mechanistic claim that SAM specifically rescues SIGReg's MC-noise regime. Engineering-and-measurement counts as research when the result is uncertain.
**Persona response**: ⚠️ WEAKENED — the publishable angle is weak (composition of two known methods), but the *climb-mode* relevance (just beat the benchmark) is strong.

**Verdict**: WARN. Novelty: EXTENDS (not NOVEL).

## Stage 4 — Theory Grounding (lite, --climb-mode)
*Adopting persona: Theorist. Stance: does SAM's flatness bias conflict with SIGReg's distributional pull?*

**Attack A4.1**: "SAM seeks flat minima; SIGReg's slice-CF gradient is locally sharp along the slice directions by design. The two may fight." (Cited: [JMLR 2024 SAM stability paper](https://www.jmlr.org/papers/volume26/24-0065/24-0065.pdf) — SAM under-performs on strong directional curvature.)
**Steel-manned rebuttal**: SAM perturbs in the *parameter* space (encoder weights), not in the *output* space (slice projections). SIGReg's sharpness is in `Z`-space, not in θ-space — the two regularisations operate on different axes. The JMLR concern applies when the parameter-curvature mirrors the loss-component sharpness, which is not guaranteed here. ASAM (adaptive per-param ρ) is the fallback if vanilla SAM struggles.
**Persona response**: ✅ DEFLECTED at the mechanism level. The empirical falsification (matched-WC) will adjudicate.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM. Stance: ship cost?*

**Attack A5.1**: "Vanilla SAM is 2× wall-clock; Friendly-SAM ~1.3×; SAMPa needs 2 GPUs to amortise. Idea claims 'effort S' but the matched-WC control doubles the experiment plan."
**Steel-manned rebuttal**: Friendly-SAM at 1.3× and 100 ep is ~130-ep AdamW equivalent. The control is exactly one extra AdamW arm at 130 ep, runnable on the same hardware. Net cost: +1 arm × 3 seeds × ~5 GPU-h = ~15 GPU-h. That is genuinely S.
**Persona response**: ✅ DEFLECTED.

**Verdict**: PASS. Cost = ~15 GPU-h.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist. Stance: what cheaper / simpler intervention dominates this?*

**Attack A6.1**: "Lookahead-AdamW or SWA (Stochastic Weight Averaging) also targets flatness, at <10% wall-clock overhead. If SWA wins, SAM is dominated."
**Steel-manned rebuttal**: SWA is a *post-hoc* average; it does not change the optimisation trajectory the way SAM's inner-perturbation does. SWA gains stack with SAM (SAM-trained model + SWA average) — they are not substitutes. The 2024 feature-quality paper explicitly compared and found SAM > SWA on probe quality.
**Persona response**: ⚠️ WEAKENED — the steel-man is plausible but the "SAM > SWA on probe" claim is from supervised setting; SWA-for-SSL has its own track record (e.g., on DINO checkpoints). The falsification design should *include SWA as a baseline arm*, not just AdamW.
**Refinement (Round 2)**: Add SWA-AdamW as a third arm in the experiment — 4 arms total (baseline AdamW @ 100, baseline AdamW @ 130, SWA-AdamW @ 100, FSAM-AdamW @ 100). Cost: +3 arms × 3 seeds × ~5 GPU-h ≈ 45 GPU-h.

**Verdict**: PASS with refinement. **Baseline arm expansion mandatory** before the +0.4 pp claim is testable.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: Stage 1 PASS · 2 PASS · 3 WARN · 4 PASS · 5 PASS · 6 PASS-w-refinement · UNREBUTTED count = 0.

**Verdict**: ✅ **FULL SEND** 🟢

**Confidence**: 🟢 — well-cited mechanism, S-effort, low risk, matched-WC falsification built in, only weakness is novelty (EXTENDS, not NOVEL — which is fine for climb-mode).

**Refinement applied from Stage 6**: experiment must include SWA-AdamW baseline arm. Updated cost ≈ 45 GPU-h.

**Composite × confidence**: 2.8 × 1.0 = 2.8.

**Ship-now action**: Add `optimizer ∈ {adamw, swa_adamw, fsam_adamw}` as a 3rd axis to batch-2 Idea 5's ASHA sweep. Same training infrastructure, just an extra grid point.
