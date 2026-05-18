# Idea 2 Vetting — iBOT-style patch-SIGReg head
**Source**: batch-1.md · Pattern P1 · Tier 1 · Scope enhance-existing
**Claim**: +1.0 / +3.0 / +5.0 pp, Feas 3/5, Effort L.

---

## Stage 1 — Framing
**Attack**: "You're rebuilding DINOv2 on top of LeJEPA. If you wanted DINOv2, run DINOv2."
- *Steel-man rebuttal*: The point is to inherit LeJEPA's theoretical guarantees (Cramér-Wold + isotropic-Gaussian optimality) at *both* CLS and patch level. DINOv2 has no such guarantee on its iBOT head.
- *Response*: ⚠️ **WEAKENED**. The theoretical-guarantee story for patch tokens is murky — patch tokens are spatially correlated, so the iid-Gaussian target is actually wrong for them.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 2 — Prior Work
**Attack**: "iBOT (Zhou ICLR 2022), DINOv2 (Oquab TMLR 2024), and 'Cluster and Predict Latents' (2025) all already extend global SSL with patch-level objectives. The LeJEPA-flavour is the only twist."
- *Rebuttal*: True; positioned as 'LeJEPA + patch'.
- *Response*: ✅ **DEFLECTED** for climb-mode.

**Stage verdict**: ✅ **PASS**.

---

## Stage 3 — Novelty: combination novel; mechanism standard. ✅ PASS.

## Stage 4 — Theory
**Attack**: "Patch tokens within an image are *strongly correlated*. SIGReg targets iid N(0, I) — applying it across patches violates the iid assumption that Cramér-Wold relies on."
- *Steel-man rebuttal*: Compute SIGReg across patches *across the batch* (one slice per spatial location), not across patches within an image. That restores approximate independence.
- *Response*: ⚠️ **WEAKENED** — workable but requires careful tensor reshaping; needs a worked-out batch structure.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 5 — Feasibility
**Attack 1**: "Effort L is optimistic. You need: a second projector head, masked-patch sampling, a separate SIGReg call, a new invariance metric for spatial alignment across views (which views share patches?), α + mask-ratio tuning. That's 1–2 weeks, not L."
- *Steel-man rebuttal*: True. Bump effort estimate from L to XL.
- *Response*: ❌ **UNREBUTTED**. Effort revised: L→XL.

**Attack 2**: "Violates the *single-λ* property that is LeJEPA's headline. You're adding α + mask_ratio + patch-M. Three new knobs."
- *Steel-man rebuttal*: Set mask_ratio=0.3 by default (iBOT) and patch-M = CLS-M. Only α is genuinely new.
- *Response*: ⚠️ **WEAKENED**.

**Rebuttal-cycle summary**: 0 DEFLECTED · 1 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL** (effort UNREBUTTED → FAIL on cost).

---

## Stage 6 — Killer Baseline ⚔️
**Attack**: "The killer baseline is: train DINOv2 (already implemented in `stable-pretraining/benchmarks/imagenet10/`) and compare. If DINOv2 already > LeJEPA + patch on ImageNet-10, you've done all this work to reinvent a worse DINOv2."
- *Steel-man rebuttal*: That's the right baseline. The user *should* run vanilla DINOv2 on ImageNet-10 first; if it dominates LeJEPA, this whole idea is moot. If LeJEPA already beats DINOv2 on this small-data regime, then 'LeJEPA + patch' is a real candidate.
- *Response*: ❌ **UNREBUTTED**. The DINOv2 comparison is the prerequisite, and it's not even run yet.

**Rebuttal-cycle summary**: 0 DEFLECTED · 0 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL**.

---

## Stage 8 — Decision Gate

Tally: 2 FAIL (Stage 5 cost, Stage 6 baseline) · 3 WARN · rest PASS.

Per `decision-logic.md` rule 8 (2 FAIL → REFRAME or KILL).

**Verdict**: 🔁 **REFRAME** 🟡

**Reframe**:
1. **First** run vanilla DINOv2 on ImageNet-10 (existing benchmark file). Establish whether LeJEPA already beats it.
2. **If LeJEPA wins** → then revisit patch-SIGReg as a 2-week project.
3. **If DINOv2 wins** → just use DINOv2 and stop trying to bolt patch heads onto LeJEPA.

This reframe makes Idea 2 conditional on a 1-day measurement that may KILL it for free.

---

## Cycle audit
Total cycles: 6. 1 DEFLECTED · 3 WEAKENED · 2 UNREBUTTED.
