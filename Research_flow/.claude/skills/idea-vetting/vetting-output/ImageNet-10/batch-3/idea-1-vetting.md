# Vetting — Batch 3 Idea 1: Two-student co-distillation with disjoint slice subspaces
**Pattern**: P12 · **Tier**: 1 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
> Adopting persona: `Advisor`. Stance: idea-or-engineering gate first; framing second.
- **Attack 1**: Is this an idea or two students glued together? **Rebuttal** (steel-man): the mechanism is *symmetric concurrent co-training with disjoint slice subspaces* — that's a defined inductive bias, not gluing. **DEFLECTED**.
- **Attack 2**: Task drift — claim is "more supervision per image", but the actual change is "more MC slices via two students". The two are not the same. **Rebuttal**: paper frames it as supervision-per-image and the disjoint subspaces are the supervision channel; valid framing. ⚠️ **WEAKENED** (gain story conflates two effects).
- Cycles: 2 (DEFLECTED 1, WEAKENED 1, UNREBUTTED 0)
- **Verdict**: PASS (with framing flag)

## Stage 2 — Prior Work Attack (Prior-Work Hunter)
- **Attack 1**: This is BYOL-symmetric without EMA, which LeJEPA paper explicitly ablated as inferior to LeJEPA-without-EMA. **Rebuttal**: LeJEPA's ablation removed EMA *and* kept a single student; this proposal restores 2 students but trades EMA for disjoint slice subspaces — the disjointness is the new lever. ⚠️ **WEAKENED** — close to BYOL-symmetric but the inductive bias is different.
- **Attack 2**: C-JEPA NeurIPS 2024 already proposed JEPA + VICReg with multi-objective; this is just rebranding. **Rebuttal**: C-JEPA uses VICReg covariance reg as the auxiliary — not a second JEPA student with cross-MSE. Different topology. **DEFLECTED**.
- **Attack 3**: VkD CVPR 2024 "orthogonal projections in KD" — this is the disjoint-subspace trick. **Rebuttal**: VkD does sequential teacher→student KD; this is concurrent symmetric two-student. Different setting (KD vs SSL pretraining). **DEFLECTED**.
- Cycles: 3 (DEFLECTED 2, WEAKENED 1, UNREBUTTED 0)
- **Verdict**: PASS (extension, not duplicate)

## Stage 3 — Novelty Decomposition (Critical Reviewer)
- Novel piece: **disjoint random slice subspaces** as the diversification mechanism between students. Not previously published in SSL.
- Already-published pieces: symmetric two-network SSL (BYOL/DINO), L²-distillation (SEED), co-training (Blum & Mitchell 1998).
- Net novelty: EXTENDS — single new ingredient on a known scaffold.
- **Verdict**: PASS

## Stage 4 — Theory Grounding (Theorist) [lite, --climb-mode]
- Cramér–Wold per student: ✅ each sees 1024 slices ≥ d log d sufficiency.
- Cross-MSE term in projection space: ✅ does not alter SIGReg's isotropy target for each student.
- **Attack**: if γ → ∞, both students collapse to a common point — SIGReg pulls toward N(0,I), MSE pulls toward identical, the equilibrium is non-trivial. **Rebuttal**: stop-grad on both sides keeps the system from a degenerate fixed point; γ ≤ 1.0 in the sweep keeps the MSE term bounded by SIGReg. ⚠️ **WEAKENED** — equilibrium analysis is hand-wavy; γ-sweep is the empirical safeguard.
- **Verdict**: PASS w/ warning (equilibrium not proved)

## Stage 5 — Feasibility (Pragmatic PM)
- 2× wall-clock vs single student → matched-compute control = 200-ep single student. Honest.
- γ adds a 2nd HP — soft "single-λ" violated (flagged in proposal).
- ImageNet-10 + ViT-S: 1 student = ~1.5 GPU-h/100ep → 2 students = ~3 GPU-h. γ sweep (4 values × 2 seeds) = 24 GPU-h. Within budget.
- **Verdict**: PASS w/ warning (2nd HP)

## Stage 6 — Killer Baseline (Skeptical Empiricist)
- The killer baseline is **single-student LeJEPA at 200 ep (matched compute)**. This is the *only* fair comparison; without it, "more wall-clock = better" is the trivial explanation.
- **Attack**: published evidence that *any* concurrent two-network SSL without EMA matches matched-compute single-network is weak. SEED (sequential) shows +2–5 pp on *small students*, but the LeJEPA student is not bandwidth-limited at ViT-S. **Rebuttal**: ImageNet-10 is signal-per-image-bottlenecked (9 k images), not parameter-bottlenecked — SEED's regime applies. ⚠️ **WEAKENED** — argument credible but no direct evidence.
- **Falsification sharpness**: ✅ ≥ 0.5 pp non-overlap CI vs 200-ep single student.
- **Verdict**: PASS w/ warning (gain bar is real and tight)

## Stage 8 — Decision Gate (Advisor PI)
- FAIL count: 0 · WARN count: 4 (framing flag, prior-work proximity, equilibrium unproved, gain-bar tight)
- Per `decision-logic.md`: 0 FAIL + 3–4 WARN → **TOY EXPERIMENT FIRST**
- Confidence: 🟡 (clean mechanism but proximity to known negative results)

## Final verdict: 🧪 **TOY** 🟡
- Toy: 24 GPU-h (γ ∈ {0, 0.5, 1.0} × 2 seeds × 100 ep + 200-ep single-student control × 2 seeds).
- Decision rule: best γ > 0 arm beats 200-ep single-student by ≥ 0.5 pp non-overlap → graduate to FULL SEND. Beats single-student-100ep but not 200ep → "extra wall-clock did it" → KILL. Worse than 200-ep → KILL outright.
- Falsification trigger: cross-student MSE with stop-grad and no EMA is the BYOL-symmetric-no-EMA ablation, which the LeJEPA paper presents as inferior.
