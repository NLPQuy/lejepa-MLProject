# Idea 3 Vetting — Add register tokens to ViT backbone
**Source**: batch-1.md · Pattern P3 · Tier 1 · Scope enhance-existing
**Claim**: +0.3 / +1.0 / +2.5 pp, Feas 5/5, Effort S, Confidence 🟢.

---

## Stage 1 — Framing
> Persona: **Advisor**.

**Attack**: "Registers fix *attention artifacts* — the published linear-probe gain on ImageNet-1K is only +0.5 pp (DINOv2-r ViT-L). On a 10-class probe with class-balanced data you have almost no headroom to detect even that."
- *Steel-man rebuttal*: The artifact phenomenon is *amplified* on smaller backbones (ViT-S/B has fewer 'spare' high-norm tokens to discharge into). And the linear-probe gain may be larger relative to baseline on a poorly-saturated 9 k-image regime.
- *Response*: ⚠️ **WEAKENED**. The "amplified on small backbones" is hand-wavey — Darcet's ablation showed the artifact appears in ViT-L/H, less in ViT-S.

**Stage verdict**: ⚠️ **WARN** — gain is probably real but inside noise on 10-class probe.

---

## Stage 2 — Prior Work
**Attack**: "Already in `timm` as `reg_tokens=4`. Done by Meta. Nothing to do here except flip a flag."
- *Rebuttal*: Yes — and that's the whole point of P3 (Replace) in --climb-mode. Free win.
- *Response*: ✅ **DEFLECTED**.

**Stage verdict**: ✅ **PASS**.

---

## Stage 3 — Novelty (climb-mode): N/A · ✅ PASS.

## Stage 4 — Theory: registers absorb high-norm artifact tokens (Darcet §4). ✅ PASS.

## Stage 5 — Feasibility: one timm kwarg. ✅ PASS, Effort S confirmed.

---

## Stage 6 — Killer Baseline ⚔️
> Persona: **Skeptical Empiricist**.

**Attack 1**: "Without registers, the LeJEPA CLS-concat probe already pools last-2 layers' CLS tokens. The 'artifact tokens' Darcet identifies are *patch* tokens, not CLS — so the linear probe is structurally insulated from the artifact phenomenon."
- *Steel-man rebuttal*: ⚠️ Strong attack. The DINOv2 register paper's linear-probe gain came mostly from k-NN retrieval, less from CLS linear probe. For the LeJEPA recipe (which uses CLS-concat), the gain may genuinely be ~0.
- *Response*: ❌ **UNREBUTTED**. This is the right way to think about it.

**Attack 2**: "Killer baseline: spend the same 5 minutes of engineering on a different cheap knob (e.g., larger projector — DINOv2 shows projector width matters more than backbone tweaks)."
- *Rebuttal*: Both are cheap. Run both, see.
- *Response*: ⚠️ **WEAKENED**.

**Rebuttal-cycle summary**: 0 DEFLECTED · 1 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL** — the CLS-probe insulation argument is unrebutted.

---

## Stage 8 — Decision Gate

Tally: 1 FAIL (Stage 6) · 2 WARN (Stage 1, Stage 6 attack 2) · rest PASS.

Per `decision-logic.md` rule 7 (1 FAIL + others PASS/WARN → REFRAME or TOY).

**Verdict**: 🧪 **TOY** 🟢

**Rationale**: The cost is trivially low (S effort, one kwarg) and the failure mode (no gain on CLS-probe) is checkable in a single short run. Confirm with one 100-epoch run before committing it to the official recipe.

### Toy Experiment Design
- **Goal**: detect ≥ 0.3 pp linear-probe lift, with vs without registers, 2 seeds each.
- **Budget**: 4 × ViT-S/100ep ImageNet-10 ≈ 8 GPU-h.
- **Decision rule**:
  - Δ ≥ 0.5 pp + non-overlapping seed range → FULL SEND.
  - −0.3 < Δ < 0.5 pp → keep registers (free, no harm) but don't count as a "win".
  - Δ < −0.3 pp → KILL (something is interacting badly with LeJEPA's CLS pooling).

---

## Cycle audit
Total cycles: 4. 2 DEFLECTED · 1 WEAKENED · 1 UNREBUTTED.
