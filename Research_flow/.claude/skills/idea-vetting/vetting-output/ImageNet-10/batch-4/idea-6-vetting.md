# Idea 6 Vetting — MAE pixel-reconstruction auxiliary head alongside SIGReg
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P1 (Combine) · Tier: 1
- Proposed gain: +0.4 / +1.0 / +2.5 pp
- Effort: L · Feasibility: 3/5

## Stage 1 — Problem Framing
*Persona: Advisor.* **Attack**: "MAE famously *under-performs* on ImageNet *linear probe* (He 2022 §5.1: MAE 68.0 % vs MoCo v3 76.7 %). Adding a head that is *bad at the metric you care about* is a strange way to climb the metric." **Rebuttal**: MAE-alone under-performs on linear probe; MAE-as-auxiliary is the proposal. The pixel-recon gradient adds shape/content signal that complements SIGReg's distributional signal — published SupMAE (arXiv:2205.14540) showed MAE+supervised-head dominates MAE-alone on linear probe by ≥ 5 pp, so the auxiliary framing has empirical support. **Persona**: ⚠️ WEAKENED — SupMAE adds a *classification* head (with labels), not an *SSL* objective. The cross-evidence is suggestive, not conclusive. **Verdict**: WARN.

## Stage 2 — Prior Work Attack
*Persona: Prior-Work Hunter.* **Attack**: "C-JEPA (NeurIPS 2024) already does JEPA + auxiliary regulariser (VICReg). The category is occupied. What does MAE add over VICReg-aux?" **Rebuttal**: VICReg-aux constrains the *embedding* (more isotropy); MAE-aux constrains *pixel reconstruction* (content fidelity). Mechanistically distinct loss families. C-JEPA does not test MAE-aux. **Persona**: ⚠️ WEAKENED. EXTENDS. **Verdict**: WARN.

## Stage 3 — Novelty Decomposition
*Persona: Critical Reviewer.* **Attack**: "Decomposition: JEPA (known) + MAE (known) + linear combination with hyperparameter α (textbook). All ingredients exist; combination is engineering." **Rebuttal**: First measured JEPA+MAE-aux on ImageNet at LeJEPA scale — empirical novelty. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Persona: Theorist.* **Attack**: "MAE's pixel-MSE encourages high-frequency reconstruction; SIGReg's Gaussianity encourages low-frequency structure. The two losses pull the encoder in opposite directions — composite may be *worse* than either alone." **Rebuttal**: The α weighting handles this; at α small, MAE is a *regulariser* not a *driver*, and the published JEPA-vs-MAE comparison shows JEPA dominates on probe — so SIGReg should dominate the loss landscape with MAE as a small auxiliary. **Persona**: ⚠️ WEAKENED — the steel-man assumes α is tunable to a sweet spot; if no α exists where MAE *helps without hurting*, the combo fails. **Verdict**: WARN.

## Stage 5 — Feasibility Analysis
*Persona: Pragmatic PM.* **Attack**: "L effort + 2× wall-clock + new α HP + masking pipeline + decoder = >> 2 weeks engineering. This is not a small bet." **Rebuttal**: HuggingFace `vit_mae` reference impl exists; lifting it into stable-pretraining is 2-3 days. α sweep is 3 values × 3 seeds × 100 ep = 9 arms × 5 GPU-h = 45 GPU-h. Matched-compute control (200 ep LeJEPA-only @ 3 seeds = 15 GPU-h × 3 = 45 GPU-h). Total ~90 GPU-h is L, not XL. **Persona**: ✅ DEFLECTED — but the 2-3 days engineering is *real*, not optional. **Verdict**: PASS-with-cost-acknowledgement.

## Stage 6 — Killer Baseline
*Persona: Skeptical Empiricist.* **Attack**: "**The matched-compute baseline is the killer.** 200 ep LeJEPA-only is 2× the standard training budget; if it beats 100 ep LeJEPA+MAE, the MAE addition is dominated by 'just train longer'. Most published combination-loss SSL gains *vanish* under matched-compute. (E.g., the iBOT-vs-DINO gap shrinks substantially when DINO is trained 2× longer.)" **Rebuttal**: The published JEPA-vs-MAE gap is ~5 pp at matched epochs; if MAE-aux closes even 20 % of that gap (+1 pp), it survives matched-compute. The +1.0 pp mid claim is calibrated to this bar. **Persona**: ⚠️ WEAKENED but: prior shows combo-loss gains often vanish. The α-ablation (α=0 at 100 ep must under-perform α>0 at 100 ep by ≥ 0.4 pp) is the mechanism check; without it, the falsification is not strong enough. **Verdict**: WARN.

## Stage 7 — Reviewer Simulation
SKIPPED.

## Stage 8 — Decision Gate
**Stage tally**: 1-4 WARN · 5 PASS · 6 WARN. UNREBUTTED = 0. 5 WARN total → REFRAME per `decision-logic.md §7` (0 FAIL + ≥ 5 WARN).

But: matched-compute falsification is sharp + cited prior (SupMAE) supports the direction. With UNREBUTTED = 0, the verdict can be TOY if the engineering cost is acceptable.

**Verdict**: 🧪 **TOY** 🟡

**Toy design**:
- **Phase A (pre-flight, 1 day eng + 0 GPU-h)**: integrate HuggingFace `vit_mae` decoder into stable-pretraining; unit-test on 1 batch.
- **Phase B**: 4 arms × 3 seeds × 100 ep: (i) baseline LeJEPA, (ii) LeJEPA + MAE α=0.1, (iii) LeJEPA + MAE α=0.5, (iv) LeJEPA + MAE α=1.0. Plus 1 matched-WC arm: LeJEPA-only 200 ep × 3 seeds. Total: 15 seed-arms × 5 GPU-h ≈ 75 GPU-h.
- **Decision rules**:
  - Best α arm beats matched-WC baseline by ≥ 0.6 pp non-overlap → graduate to FULL SEND.
  - Best α arm beats *equal-epoch* (100 ep) baseline but loses to matched-WC → KILL ("compute won, not MAE").
  - Best α arm doesn't beat equal-epoch baseline → KILL outright.

**Toy cost**: 75 GPU-h + ~2 days eng. **The most expensive TOY in the cumulative queue** — only fire after batch-3 TOYs (Hermite, rank-curriculum, co-distillation) settle.

**Confidence**: 🟡.

**Composite × confidence**: 1.9 × 0.7 = 1.33.
