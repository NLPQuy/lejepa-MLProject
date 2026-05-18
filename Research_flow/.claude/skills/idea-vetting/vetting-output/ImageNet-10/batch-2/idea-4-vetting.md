# Idea 4 Vetting — LARS / LAMB optimizer for small-batch SSL
**Batch**: 2 · **Pattern**: P3 (Replace)
**One-liner**: Swap AdamW for LARS/LAMB in `configure_optimizers`.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.
On-task; framing fine. Cycle: 0/0/0. PASS.

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

**Attack A2.1**: LARS was designed for **large**-batch SGD on ResNets (You 2017). SimCLR adopted it precisely because they trained at batch 4096+. ImageNet-10 effective batch is 512. Citing "SimCLR/BYOL/SwAV all use LARS" misframes the regime — those are *large*-batch papers; LARS is the *large*-batch optimizer.
**Steel-manned rebuttal**: BYOL ablates batch 256–4096 (Grill 2020 Tab. 11) and reports LARS-on-BYOL stable at batch 256. SwAV runs at batch 256 with LARS. So LARS works at small batch too — it's a per-layer-trust-ratio fix, not exclusively a large-batch fix.
**Persona response**: ⚠️ **WEAKENED** — LARS works at small batch but the **expected gain there is much smaller**. Most ViT-SSL methods (DINO, DINOv2, iBOT, MAE) chose **AdamW** for ViT specifically. The "SimCLR pedigree" is for ResNets.

**Attack A2.2**: For ViT backbones specifically: DINO (Caron 2021) uses AdamW. DINOv2 uses AdamW. MAE uses AdamW. iBOT uses AdamW. The convergent evidence on **ViT-SSL = AdamW** is much stronger than "SimCLR uses LARS".
**Steel-manned rebuttal**: Those papers tuned at much larger batch and longer schedules. The proposal targets a *low-data, small-model* niche where standard wisdom may not transfer. Plus LAMB (You 2019) was explicitly designed for transformers and is the right variant if going this route.
**Persona response**: ⚠️ **WEAKENED** — the rebuttal pivots from LARS to LAMB. Proposal should narrow to LAMB-only; the LARS framing is weak for ViT.

**Verdict**: WARN — prior art mostly contradicts the proposal as stated. Cycle: 0/2/0. EXTENDS (with corrections).

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.
Net novelty: **zero**. Optimizer swap is engineering. In climb-mode, ok if the gain is real.
**Verdict**: PASS-with-caveat. Cycle: 0/0/0.

## Stage 4 — Theory Grounding (lite)
> Persona: **Theorist**.
No theory claim beyond "trust ratio decouples lr from gradient norm" — textbook. PASS. Cycle: 0/0/0.

## Stage 5 — Feasibility Analysis
> Persona: **Pragmatic PM**.
One-line swap if using `torch_optimizer.Lamb`. LR re-sweep is needed (LARS/LAMB tolerate higher lr). 4-point lr sweep × 2 seeds × 1.5 GPU-h = 12 GPU-h.
**Verdict**: PASS. Effort S. Cycle: 0/0/0.

## Stage 6 — Killer Baseline
> Persona: **Skeptical Empiricist**.

**Attack A6.1**: Killer baseline = **AdamW with lr re-swept** (matched effort). If LAMB's "gain" disappears under matched lr-sweep on AdamW, it was lr-tuning, not optimizer.
**Steel-manned rebuttal**: Absolutely fair — and the proposal should be co-run with **AdamW + lr-sweep** as the control. This is the same critique batch-1 ideas faced and the right discipline.
**Persona response**: ⚠️ **WEAKENED** — must include AdamW lr-sweep control.

**Attack A6.2**: The expected gain in the proposal (mid +0.8 pp) is **larger than published ViT-SSL optimizer-swap gains** (BYOL/SwAV LARS vs AdamW deltas were < 0.5 pp on linear probe). The proposal over-claims.
**Steel-manned rebuttal**: Published comparisons were at large batch / large model. Small-data regime *could* be more sensitive — but no evidence proposal can cite for that being upward. Proposal should down-revise mid-gain to ~0.4 pp.
**Persona response**: ❌ **UNREBUTTED** — the expected-gain magnitude is not supported by cited evidence.

**Verdict**: WARN — gain over-claimed; AdamW lr-sweep control mandatory. Cycle: 0/1/1.

## Stage 8 — Decision
Tally: PASS / WARN / PASS / PASS / PASS / WARN — 0 FAIL, 2 WARN, **1 UNREBUTTED**. Per UNREBUTTED-downgrade rule: 1 UNREBUTTED downgrades the verdict tier by 1 (FULL→TOY, or TOY→REFRAME).
Pre-downgrade: TOY. Post-downgrade: **REFRAME**.

**Verdict**: 🔁 **REFRAME** · 🟡 confidence

### Reframe direction
1. Switch the proposal from "LARS or LAMB" to **LAMB only** — LAMB is the transformer-appropriate variant; LARS-on-ViT-SSL has no precedent.
2. Down-revise expected gain to mid **+0.3 pp** (worst +0.0, best +0.8 pp) — match published optimizer-swap deltas.
3. Co-run **AdamW with the same lr-sweep** as a control. If AdamW@best-lr matches LAMB@best-lr within 0.2 pp, the optimizer was a red herring; keep AdamW + the better lr.
4. Fold this experiment **into Idea 5's ASHA sweep** — add optimizer ∈ {AdamW, LAMB} as a 4th search axis at marginal cost.

If after reframe the LAMB@best beats AdamW@best by ≥ 0.3 pp non-overlap → graduate to FULL SEND. Otherwise kill.

Cycle totals: 0 DEFLECTED / 3 WEAKENED / 1 UNREBUTTED.
