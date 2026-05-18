# Idea 6 Vetting — Two-pass self-distillation across LeJEPA checkpoints
**Batch**: 2 · **Pattern**: P8 (Distill)
**One-liner**: Train LeJEPA 50 ep → freeze → continue training a fresh student with `L_LeJEPA + α · MSE(z_student, z_teacher)`.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.
On-task; gain claimed +1.5 pp mid. PASS. Cycle: 0/0/0.

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

**Attack A2.1**: SEED (Fang 2021) distills from a **larger** teacher into a **smaller** student. The proposal distills **same-model → same-model**, which is closer to **self-distillation** (Furlanello 2018, *Born-Again Networks*) — and BAN's gains are notoriously inconsistent for SSL.
**Steel-manned rebuttal**: Same-model two-pass with the second pass on the same data *is* an extra signal: the teacher embedding is a non-trivial regression target that re-uses the same data. Empirical evidence: DINOv2's distillation step (TMLR 2024) uses same-architecture teachers and gains 2-3 pp.
**Persona response**: ⚠️ **WEAKENED** — DINOv2 distillation uses a *longer-trained* teacher with EMA, not a static checkpoint. The proposal's 50-ep static teacher is closer to BAN. The gain estimate is over-claimed.

**Verdict**: WARN — closer to BAN than SEED. Cycle: 0/1/0.

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.
Mechanism: existing BAN/SEED pattern, novel only in LeJEPA-specific implementation (re-using `TeacherStudentWrapper` for non-EMA frozen teacher). Net: low novelty. PASS-with-caveat. Cycle: 0/0/0.

## Stage 4 — Theory Grounding (lite)
> Persona: **Theorist**.

**Attack A4.1**: Adding `α · MSE(z, z_teacher)` is an L² regulariser pulling embeddings toward the frozen teacher's. But LeJEPA's whole theorem says the *optimal* target is N(0, I), not z_teacher. Pulling toward z_teacher actively *fights* SIGReg — they have different fixed points.
**Steel-manned rebuttal**: The teacher itself is approximately N(0, I) (it was trained with SIGReg). So MSE-to-teacher is approximately MSE-to-a-sample-from-N(0,I), which is in the basin of SIGReg's optimum. They are not orthogonal forces.
**Persona response**: ⚠️ **WEAKENED** — under-trained teacher (50 ep) is *only approximately* isotropic. The "they agree" claim is conditional on teacher quality, which is exactly what we're trying to bootstrap from.

**Verdict**: WARN — theory-conflict with SIGReg's unique fixed point is real. Cycle: 0/1/0.

## Stage 5 — Feasibility Analysis
> Persona: **Pragmatic PM**.

2× wall-clock per condition + α sweep (3 values) + teacher-epoch sweep (3 values) × 3 seeds. Naive: 18 runs × 1.5 GPU-h ≈ 27 GPU-h. Plus the prerequisite teacher checkpoints. Effort M-L.

**Attack A5.1**: Comparing distilled-student (150 GPU-eq) to baseline-50ep is unfair (more compute). Comparing to baseline-150ep is the only honest comparison.
**Steel-manned rebuttal**: Proposal already specifies "must beat 150-ep vanilla baseline" — this is the right control.
**Persona response**: ✅ **DEFLECTED**.

**Verdict**: PASS. Cycle: 1/0/0.

## Stage 6 — Killer Baseline
> Persona: **Skeptical Empiricist**.

**Attack A6.1**: The most likely outcome is **"distilled-student ≈ 150-ep vanilla"** — i.e., the 2× compute spent on distillation matches 2× compute spent on just training longer. SEED-style gains required the larger-teacher gap that this proposal lacks.
**Steel-manned rebuttal**: This is exactly the falsification protocol the proposal accepts ("must beat 150-ep baseline by ≥ 1.0 pp"). If it doesn't, it dies.
**Persona response**: ⚠️ **WEAKENED** — the 1.0 pp bar is high; the *prior probability* of clearing it given same-model BAN literature is < 30%.

**Attack A6.2**: Adds α — violates "single λ" branding (proposal flagged). If LeJEPA's main paper-level contribution is one-knob simplicity, this idea is anti-branding even if it works.
**Steel-manned rebuttal**: True; but climb-mode pursues *the benchmark number*, not branding. If gain is real, accept the second knob.
**Persona response**: ⚠️ **WEAKENED** — fair in climb-mode.

**Attack A6.3**: The *much cheaper* baseline is "just train 100 ep with same compute as the 2-pass total". Two-pass = 50+100 ep total compute. Single-pass at 150 ep is the direct match. If the proposal's falsification means it has to beat 150-ep vanilla by 1 pp, the *expected gain* should mid-shrink to **+0.5 pp**, not +1.5 pp.
**Steel-manned rebuttal**: Proposal's gain estimate is anchored to SEED-style gains, which used a stronger teacher. With the weaker (same-model) teacher, +1.5 pp is over-claimed; +0.5 pp mid is honest.
**Persona response**: ❌ **UNREBUTTED** — expected-gain magnitude was over-claimed.

**Verdict**: WARN — over-claimed gain, theoretical tension with SIGReg fixed point. Cycle: 1/2/1.

## Stage 8 — Decision
Tally: PASS / WARN / PASS / WARN / PASS / WARN — 0 FAIL, 3 WARN, **1 UNREBUTTED** → downgrade.
Pre-downgrade: TOY (3 WARN ≥ 3 → TOY per `decision-logic.md`). Post-downgrade (1 UNREBUTTED): **REFRAME**.

**Verdict**: 🔁 **REFRAME** · 🟡 confidence

### Reframe direction
1. **Down-revise gain estimate** to mid +0.5 pp (range 0.0 – +1.5 pp) — match same-model BAN expectations, not larger-teacher SEED.
2. **Run the 150-ep vanilla baseline first** (it's already a needed control for batch-2 anyway). If 150-ep already saturates the ImageNet-10 ViT-S regime (e.g., probe within 0.3 pp of 100-ep), distillation cannot win and should be killed.
3. If 150-ep shows clear improvement over 100-ep, then *and only then* run the distillation toy with **only 1 α** (α=0.5, midpoint) × 2 seeds — a single confirmation experiment, not a sweep.
4. Stretch: try a **cross-architecture in-domain** teacher (ViT-S → ViT-B trained on the same 9k images): that gets closer to SEED's "smaller-to-larger transfer" regime and is the only way this idea can plausibly clear +1.0 pp.

Cycle totals: 2 DEFLECTED / 4 WEAKENED / 1 UNREBUTTED.
