# Idea 3 Vetting — Layer-wise SIGReg with deep supervision
**Source**: batch-4 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P5 (Decompose) · Tier: 2
- Proposed gain: +0.3 / +0.8 / +1.8 pp
- Effort: S · Feasibility: 4/5

## Stage 1 — Problem Framing
*Persona: Advisor.* **Attack**: "The probe-alignment story is appealing but the gap between final-CLS-only training and last-2-CLS-probing has never been *measured* on LeJEPA. Speculative bottleneck." **Rebuttal**: True, but the LeJEPA paper's own choice to probe with concat-last-2 suggests they observed the second-to-last layer matters; training-eval mismatch is *prima facie* a real gap. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 2 — Prior Work Attack
*Persona: Prior-Work Hunter.* **Attack**: "SDSSL (intermediate-layer SSL distillation, arXiv:2408.17059 survey) and DINOv3's multi-loss recipe (LDINO + LIBOT + LKoleo + LGram) already do multi-layer SSL losses. Not novel." **Rebuttal**: Those apply *different* losses at different layers; the proposal applies the *same* SIGReg statistic at multiple depths. The mechanism (same regulariser, multi-depth) is distinct. **Persona**: ⚠️ WEAKENED. EXTENDS. **Verdict**: WARN.

## Stage 3 — Novelty Decomposition
*Persona: Critical Reviewer.* **Attack**: "Same as Stage 2 — deep supervision is 2014, multi-layer SSL losses are 2023+. Engineering-novel, not research-novel." **Rebuttal**: Climb-mode prioritises measured lift, not publishability. **Persona**: ⚠️ WEAKENED. **Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Persona: Theorist.* **Attack**: "Constraining intermediate layers to be Gaussian *interferes* with the encoder's natural hierarchical representation. Early ViT blocks should carry low-level texture statistics that are *not* Gaussian. Forcing Gaussianity there may *destroy* useful structure." **Rebuttal**: The intermediate-layer SIGReg fires only on the CLS token, not on patch tokens — CLS is the global summary, where Gaussianity is mechanistically justified (it's the variable the probe uses). Patch tokens are untouched. **Persona**: ✅ DEFLECTED. **Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Persona: Pragmatic PM.* **Attack**: "3 SIGReg calls per step instead of 1 → 3× slicing cost." **Rebuttal**: Slicing is ~5 % of step time per CLAUDE.md (augmentation dominates); 3× of 5 % = 15 % → ~10 % wall-clock total. Negligible. Depth weights HP is the real cost (mitigated by fixed default). **Persona**: ✅ DEFLECTED. **Verdict**: PASS.

## Stage 6 — Killer Baseline
*Persona: Skeptical Empiricist.* **Attack**: "Probe-alignment can be tested cheaper: switch the *probe* to use only the final layer (no concat), at *baseline* LeJEPA. If probe-only-last-layer ≥ probe-concat-2-layer, the alignment story is wrong from the start." **Rebuttal**: That's a valid pre-flight cheap check — adds zero compute and may *eliminate the need* for this idea. **Persona**: ❌ UNREBUTTED — and this is the *killer*. The cheap pre-flight check must run first.

**Verdict**: FAIL → downgrade.

## Stage 7 — Reviewer Simulation
SKIPPED.

## Stage 8 — Decision Gate
**Stage tally**: 1-3 WARN · 4 PASS · 5 PASS · 6 **FAIL (UNREBUTTED)**. UNREBUTTED count = 1.

**Verdict**: 🧪 **TOY** 🟡 (downgraded from FULL by 1 level due to Stage 6 UNREBUTTED).

**Toy design**: Two phases.
- **Phase A (free)**: At an existing baseline LeJEPA checkpoint, evaluate both `probe(last)` and `probe(concat-last-2)` on ImageNet-10 val. If `gap < 0.3 pp`, **KILL** the idea — the probe-alignment premise is wrong.
- **Phase B (conditional on Phase A gap ≥ 0.3 pp)**: Train 3-layer SIGReg with weights (0.25, 0.25, 1.0), 100 ep, 3 seeds, fixed (λ, lr, wd). Decision rule: ≥ 0.5 pp non-overlap vs baseline, AND last-2-layer probe gap *widens* (the mechanism check).

**Toy cost**: Phase A = 0 GPU-h (uses existing checkpoint). Phase B = 3 seeds × 100 ep × ~5 GPU-h = 15 GPU-h.

**Confidence**: 🟡.
