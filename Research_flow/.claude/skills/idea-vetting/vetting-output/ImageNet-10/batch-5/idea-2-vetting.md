# Idea 2 Vetting — Kernelized Stein Discrepancy per-slice statistic
**Source**: batch-5 · **Vetted**: 2026-05-18 · **Mode**: --climb-mode

## Summary
- Pattern: P2 (Transfer — Stein's method from probability theory) · Tier: 3
- Proposed gain: +0.2 / +0.7 / +1.5 pp
- Effort: M · Feasibility: 3/5
- Composite (batch-5): 2.2

---

## Stage 1 — Problem Framing
*Adopting persona: Advisor. Stance: is EppsPulley's CF integration grid actually the bottleneck?*

**Attack A1.1**: "EppsPulley at n_points=17 is a fast, well-conditioned statistic with strong CF-distance asymptotics. Calling its integration grid 'bias' is overstated; the trapezoid error at 17 points for a Gaussian CF on [0, t_max] is tiny."
**Steel-manned rebuttal**: The fixed t_max truncates the CF tail. KSD has no truncation — fully data-driven. On non-Gaussian alternatives with heavy tails (a known failure mode of collapse), KSD's tail sensitivity > EP's. Liu-Lee-Jordan 2016 measure 30-50 % higher AUC on tail-deviation alternatives.
**Persona response**: ⚠️ WEAKENED — the tail sensitivity is real but on the SSL trajectory, heavy tails are not the dominant failure mode. SSL collapse looks like *low variance* (compaction), not heavy tails. KSD's edge is targeted at the wrong failure mode.

**Verdict**: WARN.

## Stage 2 — Prior Work Attack
*Adopting persona: Prior-Work Hunter. Stance: has KSD been applied as an SSL regulariser?*

**Attack A2.1**: "Score-matching for SSL exists (e.g., score-SSL line, denoising-score-matching). KSD is closely related. Hard duplicate risk."
**Steel-manned rebuttal**: Score-SSL fits a score *network* to data; KSD-as-SSL-regulariser uses the *known* score of N(0,1) on the embedding. The mechanisms are reversed (score-SSL: learn score of data; KSD-SIGReg: enforce embedding has known score). No published instance of the second.
**Persona response**: ✅ DEFLECTED. Distinct mechanism.

**Verdict**: PASS.

## Stage 3 — Novelty Decomposition
*Adopting persona: Critical Reviewer.*

**Attack A3.1**: "It's a statistic swap — change `T(h)` from EppsPulley to KSD. Bonus that KSD is more famous? Engineering."
**Steel-manned rebuttal**: The novelty is the *first time* a Stein-discrepancy statistic is applied to the slice-projected embedding in an SSL pipeline; the slicing geometry preserves Cramér-Wold, and Stein-kernel choice + RFF approximation are non-trivial design choices.
**Persona response**: ⚠️ WEAKENED — climb-mode allows engineering-and-measurement; paper venue would push back.

**Verdict**: WARN.

## Stage 4 — Theory Grounding (lite)
*Adopting persona: Theorist.*

**Attack A4.1**: "KSD with isotropic RBF kernel has known *low power in high dimension* (curse of dimensionality on the kernel scale). Per-slice (d=1) avoids this, but then the per-slice KSD power is bounded by the kernel bandwidth, which is a new HP."
**Steel-manned rebuttal**: median-heuristic bandwidth has decades of empirical track record on KSD; it absorbs the HP. And per-slice (d=1) is exactly where KSD's curse-of-dim issue *doesn't* apply. The composition with slicing is intentional.
**Persona response**: ✅ DEFLECTED. The CoD critique applies to full-multivariate KSD; sliced is fine.

**Verdict**: PASS.

## Stage 5 — Feasibility Analysis
*Adopting persona: Pragmatic PM.*

**Attack A5.1**: "O(N²) per slice × 1024 slices = 250M ops per SIGReg call vs EppsPulley's 9k. Even with mini-block KSD (subsample 64 of 512), 64² × 1024 = 4M ops — still 400× slower than EP at full M. Cost claim 'M effort' understates."
**Steel-manned rebuttal**: At B=512, d=384, the encoder forward is ~50 G FLOPs/step; SIGReg's 250M ops are <0.5 % of step cost. Cost is wall-clock-negligible even at O(N²). RFF approximation drops to O(N · D_features) at marginal accuracy cost.
**Persona response**: ⚠️ WEAKENED — the absolute cost argument is correct (encoder dominates), but the implementation complexity (sorted-block KSD or RFF-KSD) is real M-effort eng, not S. Also the kernel-bandwidth HP per layer is more annoying than median-heuristic suggests.

**Verdict**: WARN. Cost wall-clock OK; eng-effort actually L not M.

## Stage 6 — Killer Baseline
*Adopting persona: Skeptical Empiricist.*

**Attack A6.1**: "Per-slice statistic alternatives are stacking up: EP (baseline), Hermite (batch-3 TOY), Riesz-MMD (Idea 4 this batch). KSD is the *most expensive* of the four and the only one with a kernel-bandwidth HP. Dominated by Idea 4 on the cost axis."
**Steel-manned rebuttal**: KSD's score-awareness gives it a *power* advantage over the CF-based EP and EP-adjacent Riesz-MMD. Liu-Lee-Jordan show 1.5-2× power on tail-deviation alternatives. If embedding collapses heavy-tailed (e.g., from rank curriculum), KSD detects it first.
**Persona response**: ⚠️ WEAKENED — the power-advantage claim has not been measured on SSL embeddings; supervised KSD numbers don't transfer cleanly. And the 4-way A/B/C/D experiment of per-slice statistics is the right resolution, not pre-committing to KSD.

**Verdict**: WARN with refinement. **Phase A pre-flight mandatory**: synthetic-power test of KSD vs EP vs Riesz-MMD vs Hermite on N(0,1) + 5% shifted mixture. If KSD does not show ≥ 1.5× power at α=0.05, drop it from the 4-way bake-off and keep only the cheaper three.

## Stage 7 — Reviewer Simulation
SKIPPED (--climb-mode).

## Stage 8 — Decision Gate
*Adopting persona: Advisor (PI mode).*

**Stage tally**: 1 WARN · 2 PASS · 3 WARN · 4 PASS · 5 WARN · 6 WARN-w-refinement · UNREBUTTED = 0, 4 WARN.

**Verdict**: 🧪 **TOY** 🟡

**Confidence**: 🟡 — Stein's method is bona-fide T3; the implementation has real complexity; the killer-baseline argument bites (4-way statistic A/B/C/D is the right framing, not pre-commit to KSD).

**Toy design**: Phase A — synthetic power test of {EP, KSD, Riesz-MMD, Hermite} at α=0.05 on N(0,1)+5%mixture, 0 GPU-h CPU. Phase B (only if KSD passes Phase A and beats Riesz-MMD on power): 100-ep ImageNet-10 head-to-head with EP baseline at fixed (λ, lr, wd); 30 GPU-h. Decision rule: Phase B linear probe ≥ 0.4 pp non-overlap.

**Composite × confidence**: 2.2 × 0.7 = 1.54.

**Ship-now action**: queue Phase A together with Idea 4's Phase A — single synthetic-test pass covers both statistic-swap candidates.
