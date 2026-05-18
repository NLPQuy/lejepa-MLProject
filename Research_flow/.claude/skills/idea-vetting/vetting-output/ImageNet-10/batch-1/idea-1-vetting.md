# Idea 1 Vetting — Orthogonal / QMC slicing for SIGReg
**Source**: batch-1.md · Pattern P3 · Tier 2 · Scope enhance-existing
**Claim**: +0.3 / +1.0 / +2.0 pp, Feas 5/5, Effort S.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.

**Attack**: "Is the metric you care about (variance of SIGReg estimate) the metric that moves linear probe? You're asserting a chain: low MC variance → low gradient noise → better embedding → better probe."
- *Steel-man rebuttal*: SIGReg at M=1024 is already low-variance — the gradient signal is dominated by mini-batch noise on N=512, not slice noise. Sliced-Wasserstein literature consistently shows variance reduction matters most at *small M*; at M=1024 the gain often vanishes.
- *Response*: ❌ **UNREBUTTED**. The rebuttal *concedes* the attack: at M=1024 the gain is near zero. The only path to value is *reducing M* (compute saving), not *boosting accuracy*.

**Rebuttal-cycle summary**: 0 DEFLECTED · 0 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL** (downgraded from WARN by UNREBUTTED). Reframing recommended: not "boost accuracy", but "halve M at equal probe".

---

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

**Attack 1**: "Nguyen et al. 'Quasi-Monte Carlo Sliced Wasserstein' (NeurIPS 2024, arXiv:2309.11713) already showed orthogonal+QMC slicing for SW. You're transferring it to SIGReg/Epps-Pulley — that's a 1-line change, not a contribution."
- *Steel-man rebuttal*: Correct on prior work. As a climb lever this is fine; as a paper claim it's not. Frame: "apply QMC-SW slicing to SIGReg in LeJEPA".
- *Response*: ✅ **DEFLECTED** for climb-mode.

**Attack 2**: "Even simpler: Householder-orthogonal slicing has been in Lin et al. 'Distributional Sliced Wasserstein' (ICLR 2021)."
- *Rebuttal*: Yes. Same response — climb-only.
- *Response*: ✅ **DEFLECTED**.

**Rebuttal-cycle summary**: 2 DEFLECTED · 0 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ✅ **PASS** (climb-mode).

---

## Stage 3 — Novelty
- Trivial: orthogonalised iid Gaussians (rng + QR). Novelty in --climb-mode = N/A. ✅ PASS.

---

## Stage 4 — Theory (lite)
> Persona: **Theorist**.

**Attack**: "Orthogonal slices break the *unbiasedness* of `(1/M) Σ T(Z u^(m))` as an estimator of E_u[T(Z u)] — orthogonal vectors are not iid uniform on S^(d−1)."
- *Steel-man rebuttal*: For rotation-invariant T (Epps-Pulley *is* rotation-invariant in u for centred Z), the orthogonal-slice estimator remains unbiased and has provably lower variance (Rowland et al. 'Orthogonal Estimation of Wasserstein Distances', AISTATS 2019). The conditions are satisfied here.
- *Response*: ✅ **DEFLECTED**.

**Stage verdict**: ✅ **PASS**.

---

## Stage 5 — Feasibility
- Effort S, 1-file change, no schedule disruption. ✅ **PASS**.

---

## Stage 6 — Killer Baseline ⚔️
> Persona: **Skeptical Empiricist**.

**Attack**: "The killer baseline is: keep iid sampling, halve M from 1024 to 512. If QMC@M=512 ties iid@M=1024, you've saved compute but not accuracy. If QMC@M=512 > iid@M=512, you've shown variance reduction, but iid@M=1024 (current default) is already there — no accuracy win for the current recipe."
- *Steel-man rebuttal*: Right. The realistic value proposition is **compute saving** at iso-accuracy, not accuracy gain. Reframe expected gain to +0.0–0.5 pp accuracy, 1.5–2× compute reduction on the SIGReg term.
- *Response*: ❌ **UNREBUTTED** as accuracy-climb. ✅ **DEFLECTED** as compute-saving. The idea survives but its purpose changes.

**Rebuttal-cycle summary**: 0 DEFLECTED · 0 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL** as stated. Reframing the goal to compute-saving moves it to ⚠️ WARN.

---

## Stage 8 — Decision Gate

Tally: 2 FAIL (Stage 1, Stage 6) · 1 WARN (Stage 4) · rest PASS. 2 FAILs both reframeable.

Per `decision-logic.md` rule 8 (2 FAIL → REFRAME or KILL).

**Verdict**: 🔁 **REFRAME** 🟢

**Reframe**: Position this as a **SIGReg compute-efficiency** lever, not an accuracy lever.
- New claim: "QMC slicing matches iid SIGReg at half the M; reclaim 5–10 % step-time for more crops / longer training."
- New falsification: at M=512 QMC, training-loss curves overlap iid M=1024 within 1 σ over 100 epochs.
- This unlocks **idea 6's V=14 budget** — the two ideas chain.

If user insists on accuracy framing → **KILL**.

---

## Cycle audit
Total cycles: 6. 4 DEFLECTED · 0 WEAKENED · 2 UNREBUTTED.
