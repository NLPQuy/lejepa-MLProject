# Idea 6 Vetting — Class-balanced multi-crop curriculum on ImageNet-10
**Source**: `ideation-output/ImageNet-10/batch-1.md` · Pattern P4 · Tier 1 · Scope enhance-existing
**Claim**: +0.5 / +2.0 / +4.0 pp linear probe, Feas 5/5, Effort S.
**Mode**: --climb-mode (Stage 7 skipped)

---

## Stage 1 — Problem Framing
> Persona: **Advisor**. Stance: is the problem framed sharply enough to optimise against?

**Attack 1**: "Multi-crop curriculum + balanced sampler is *three* changes in a trench-coat (V, scale schedule, class balance). You can't attribute a gain to anything if all three move together."
- *Steel-man rebuttal*: The ablation plan in the Implementation sketch sweeps V independently and turns the curriculum and sampler on/off; the falsification test specifies V∈{6,10} at fixed scale-schedule + sampler. That isolates V. Class balance is a no-op on Imagenette (already balanced ~950 imgs/class), so really only V + scale curriculum are live.
- *Response*: ⚠️ **WEAKENED**. The "class balance is a no-op on Imagenette" admission means one of the three knobs is *cosmetic*, which the idea card should have called out. The expected-gain stays anchored on V + curriculum only — lower it.

**Rebuttal-cycle summary**: 0 DEFLECTED · 1 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ⚠️ **WARN** — framing OK but the headline expected gain is mildly inflated; recalibrate `gain_mid` from +2.0 to ~+1.2.

---

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**. Stance: has this been done?

**Attack 1**: "DINO (Caron 2021) ran exactly this ablation (V ∈ {2, 4, 6, 8, 10}, scale ranges). DINOv2 picked V=8 globally + 8 local. You're re-running a 4-year-old ablation on a different dataset."
- *Steel-man rebuttal*: DINO ran the ablation on ImageNet-1K (1.28 M images), where the optimum collapsed to 2 + 8. On a 9 k-image dataset the optimum can be very different — small-data SSL is empirically separate (see DINO-MC arXiv:2303.06670; ViTs-for-small-scale BMVC 2022). The "scale curriculum" knob is also not in DINO's grid.
- *Response*: ⚠️ **WEAKENED**. Reframe accepted: this is "re-run DINO's ablation on the small-data regime + add a curriculum." That is a legitimate but narrow contribution — and the curriculum is the only genuinely new piece.

**Attack 2**: "The curriculum (wide → narrow scales) is also old: SimCLR's strong-aug schedule and the entire 'curriculum learning for augmentations' line (e.g., AutoAugment + curriculum, Wang 2021). You're not first."
- *Steel-man rebuttal*: Curriculum-on-crop-scale specifically for multi-crop SSL on small data is not a documented combo. The closest is DINO-MC (multi-sized) but that uses fixed sizes per epoch, not a schedule.
- *Response*: ⚠️ **WEAKENED**. Novel enough as an empirical combo; not a publishable contribution but defensible as a climb lever.

**Rebuttal-cycle summary**: 0 DEFLECTED · 2 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ⚠️ **WARN** — adjacent prior work is dense; expect skepticism from any reviewer but acceptable for a climb.

---

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.

**Attack**: "Decompose: (V sweep = trivial), (scale curriculum = mildly novel), (class-balanced sampler = no-op). The 'novel' fraction is ~25 %."
- *Steel-man rebuttal*: Accepted. This is a climb idea, not a paper.
- *Response*: ✅ **DEFLECTED** *in --climb-mode* — novelty is not the gating axis. Would be UNREBUTTED in paper-mode.

**Rebuttal-cycle summary**: 1 DEFLECTED · 0 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ✅ **PASS** (climb-mode only).

---

## Stage 4 — Theory Grounding (lite, climb-mode)
> Persona: **Theorist**.

**Attack**: "Why does wider-then-narrower help? Intuition not theory."
- *Rebuttal*: Wider initial crops preserve global structure → invariance term gets a clean signal early; narrowing later forces fine-grained features. No formal proof, but consistent with the 'optimization landscape' literature.
- *Response*: ⚠️ **WEAKENED** — informal but plausible.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 5 — Feasibility
> Persona: **Pragmatic PM**.

**Attack**: "Step time scales ~linearly with V_local. V=14 is 2.3× over baseline V=6. Your 'equal wall-clock' falsification has fewer steps for V=14 — it can lose just because the model trained less."
- *Steel-man rebuttal*: True. Mitigation: report two curves — equal-wall-clock and equal-steps. If the equal-steps result also fails, the idea fails cleanly. If only equal-wall-clock fails, that's a separate (compute-efficiency) question.
- *Response*: ✅ **DEFLECTED**.

**Rebuttal-cycle summary**: 1 DEFLECTED · 0 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ✅ **PASS**. Effort genuinely S; feasibility 5/5 stands.

---

## Stage 6 — Killer Baseline ⚔️
> Persona: **Skeptical Empiricist**. Stance: what cheap baseline silently beats this?

**Attack 1**: "The killer baseline is: take the canonical recipe (V=6, scale 0.05–0.3), train 1.5× longer at equal compute to V=14. That's a one-line change and is almost always competitive with multi-crop expansion."
- *Steel-man rebuttal*: For SSL, "train longer" eventually saturates and adding diversity tends to win at saturation. DINO showed 8 local crops > 4 local crops + longer. But that was on ImageNet-1K — on 9 k images longer training overfits, so "train longer" is *not* an obvious win here. The longer-training baseline is *exactly* the right control to include.
- *Response*: ✅ **DEFLECTED**, but it forces the protocol: report (V_baseline, equal compute) vs (V_baseline, equal steps, longer training) vs (V_increased, equal compute). Without all three, the claim is unfalsifiable.

**Attack 2**: "Best-of-3 random seeds at V=6 might already overlap with V=10 mean. Small-data SSL has high seed variance (σ ~0.5 pp seen in Lightly benchmarks)."
- *Steel-man rebuttal*: Run 3 seeds per setting; report CI. If +1.2 pp ≪ 2σ ≈ 1.0 pp, the gain is in the noise floor.
- *Response*: ⚠️ **WEAKENED**. Seed-variance gate is binding; gain estimate of +1.2 pp is uncomfortably close to noise floor → confidence 🟡.

**Rebuttal-cycle summary**: 1 DEFLECTED · 1 WEAKENED · 0 UNREBUTTED.
**Stage verdict**: ⚠️ **WARN** — passes only if the seed-CI protocol is followed.

---

## Stage 7 — Reviewer Simulation (skipped, climb-mode)

---

## Stage 8 — Decision Gate
> Persona: **Advisor (PI mode)**.

Tally: Stages 1, 2, 4, 6 = **WARN**; Stages 3, 5 = **PASS**. 0 FAIL, 4 WARN.

Per `decision-logic.md` rule 5 (0 FAIL + 3–4 WARN → **TOY EXPERIMENT FIRST**).

**Verdict**: 🧪 **TOY** 🟢

**Rationale**: Effort is small (1–2 GPU-days), seed-variance is the main risk, and the killer-baseline protocol is well-defined. Run a 3-seed toy at V∈{6,10} with the curriculum on/off before committing to the full sweep.

### Toy Experiment Design
- **Goal**: detect ≥ +1.0 pp linear-probe lift of V=10 + curriculum vs V=6 + no-curriculum, 3 seeds each, equal wall-clock.
- **Budget**: 6 × ViT-S/100ep × ImageNet-10 ≈ 12 GPU-h on 1 × A100.
- **Decision rule**:
  - If V=10 + curr mean > V=6 baseline mean + 1.0 pp and CIs separate → graduate to FULL SEND with V∈{10,14}.
  - If overlap → KILL (not the right lever for this dataset).
  - If V=10 alone (no curr) > V=6 by ≥ 1.0 pp → graduate but drop the curriculum.
- **Risks**: longer training baseline missing — add a 4th cell (V=6 + 1.5× steps) if compute allows.

---

## Cycle audit
Total rebuttal cycles: 7 (within 16-cycle cap). 2 DEFLECTED · 5 WEAKENED · 0 UNREBUTTED.
