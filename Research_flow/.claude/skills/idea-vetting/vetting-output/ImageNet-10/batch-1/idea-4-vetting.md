# Idea 4 Vetting — Online normality verifier → adaptive λ
**Source**: batch-1.md · Pattern P6 · Tier 3 · Scope enhance-existing
**Claim**: +0.2 / +1.0 / +2.5 pp, Feas 4/5, Effort M.

---

## Stage 1 — Framing
**Attack**: "Replace 1 hyperparameter (λ) with 2 (β, s_target) — net complexity loss. LeJEPA's whole selling point is the *single-knob*."
- *Steel-man rebuttal*: s_target is computable from theory (SIGReg value of an exact N(0,I_d) sample at the same N, d, M — closed-form Monte Carlo estimate). β = 1.0 is a defensible default. So in practice you have 0 new knobs to tune.
- *Response*: ⚠️ **WEAKENED**. Works if defaults transfer; one ablation per dataset would still be needed.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 2 — Prior Work
**Attack**: "GradNorm (Chen ICML 2018), DWA (Liu CVPR 2019), uncertainty-weighted multi-task (Kendall CVPR 2018) — adaptive loss weighting is a settled, mature literature. You're transferring it. Fine for climb."
- *Rebuttal*: Acknowledged.
- *Response*: ✅ **DEFLECTED**.

**Stage verdict**: ✅ **PASS**.

---

## Stage 3 — Novelty (climb): N/A · ✅ PASS.

## Stage 4 — Theory
**Attack**: "If the loss naturally drives SIGReg → 0, a controller that *also* drives λ → 0 creates a positive-feedback runaway: SIGReg small → λ small → SIGReg gets even smaller (no regularizer) → λ → 0 → collapse."
- *Steel-man rebuttal*: λ_min and the clip in `λ_{t+1} = clip(λ_t · (s_t/s_target)^β, λ_min, λ_max)` prevent runaway. As long as λ_min > 0 and s_target is the SIGReg value of *true* N(0,I_d) (not 0), the system has a fixed point at s_t = s_target.
- *Response*: ✅ **DEFLECTED**.

**Stage verdict**: ✅ **PASS**.

---

## Stage 5 — Feasibility
- Lightning callback, ~30 lines. ✅ **PASS**.

---

## Stage 6 — Killer Baseline ⚔️
**Attack 1**: "The killer baseline is the LeJEPA paper's own recommendation: **bisection search over λ ∈ {0.005, 0.02, 0.1}** (3 runs). That's exactly your closed-form-default scenario, and probably finds a strictly better single-λ than the controller's trajectory-averaged λ."
- *Steel-man rebuttal*: A *trajectory* of λ is strictly more expressive than the best fixed λ — assuming the controller is correctly calibrated. The optimal λ early (when embedding far from Gaussian) and late (when embedding is near Gaussian) are different.
- *Response*: ⚠️ **WEAKENED**. The argument is plausible but not demonstrated. Risk: in practice the gain over fixed-λ is < 0.3 pp, which is the noise floor.

**Attack 2**: "Cosine schedule on λ (start λ=0.1, anneal to λ=0.005) achieves the same time-varying trajectory with **zero** new machinery. That's the real killer baseline."
- *Steel-man rebuttal*: ❌ Strong attack. A fixed cosine on λ is the simplest expressive-over-time schedule. The adaptive controller only wins if it learns *better* schedules than the cosine — which is the same kind of claim NAS makes vs hand-designed.
- *Response*: ❌ **UNREBUTTED**. The cosine-λ baseline is genuinely the right control.

**Rebuttal-cycle summary**: 0 DEFLECTED · 1 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL**.

---

## Stage 8 — Decision Gate

Tally: 1 FAIL (Stage 6) · 2 WARN · rest PASS.

Per `decision-logic.md` rule 7 (1 FAIL + others PASS/WARN → REFRAME or TOY).

**Verdict**: 🔁 **REFRAME** 🟡

**Reframe**: Before building the controller, run a **λ-schedule sweep** (constant, linear, cosine annealing on λ) at fixed compute. If any schedule beats the best fixed λ by ≥ 0.5 pp, *then* the controller is worth building because it could adapt the schedule per-dataset. If no schedule beats fixed λ, the controller is dead.

This is cheaper than the controller itself (3 runs vs implementation + tuning) and is a strictly stronger baseline.

---

## Cycle audit
Total cycles: 5. 2 DEFLECTED · 2 WEAKENED · 1 UNREBUTTED.
