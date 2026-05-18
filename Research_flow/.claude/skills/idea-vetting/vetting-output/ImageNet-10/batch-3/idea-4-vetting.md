# Vetting — Batch 3 Idea 4: Hermite-moment univariate test
**Pattern**: P3 · **Tier**: 3 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
- **Attack 1**: idea-or-engineering — implementing a new `UnivariateTest` subclass is plumbing. **Rebuttal**: the *claim* is that orthogonal-basis moment tests have stronger far-field gradient than ECF integration → better early-training convergence. That's mechanism. **DEFLECTED**.
- **Verdict**: PASS

## Stage 2 — Prior Work Attack (Prior-Work Hunter)
- **Attack 1**: ⚠️ **Hermite K=4 is exactly the Jarque–Bera test**, which `lejepa.univariate.ExtendedJarqueBera` already implements. This is a re-skin of an existing test. **Rebuttal**: Hermite *generalises* JB to K > 4 with **orthogonal moment increments** — adding K=5 in plain moments would be correlated with K=3/4, but Hermite-5 is orthogonal under N(0,1) and adds genuinely new information. JB stops at K=4 by convention; Hermite-6 is materially different. ⚠️ **WEAKENED** — distinction exists but is narrow.
- **Attack 2**: D'Agostino & Stephens 1986 showed that for n ≤ 256, higher-moment tests have huge variance and rarely beat AD or EP empirically. **Rebuttal**: proposal already clamps K ≤ 6 for this reason. Acknowledged. **DEFLECTED**.
- **Attack 3**: batch-2 Idea 1 (stacked tests on toy queue) *already* covers "more statistical power inside the linear-slice family". If stacked tests win, Hermite is dominated; if they lose, Hermite likely also loses. **Rebuttal**: Hermite is *orthogonal-basis* (no test-correlation), while stacked AD+EP have correlated power profiles. The two are not redundant. ⚠️ **WEAKENED** — true but the marginal lift over stacked-tests is unclear; idea sits in the shadow of the toy queue.
- Cycles: 3 (DEFLECTED 1, WEAKENED 2, UNREBUTTED 0)
- **Verdict**: WARN — gain story is dominated by adjacent toy

## Stage 3 — Novelty Decomposition
- Novel piece: K=6 Hermite-moment test in SSL context.
- Already published: JB (K=4), Hermite normality tests (Lacaux 1999 in signal processing), `ExtendedJarqueBera` in `lejepa.univariate`.
- Net novelty: EXTENDS (narrow — K=4 → K=6 plus orthogonal-basis framing).
- **Verdict**: WARN

## Stage 4 — Theory Grounding
- Hermite polynomials orthogonal under N(0,1) → ✅ each moment vanishes iff slice ~ N(0,1).
- Sum is complete normality test as K → ∞.
- **Attack**: at finite K, the test is *consistent* but power may be lower than EP for distributions whose deviations show up in the ECF tail beyond moment 6. **Rebuttal**: true — Hermite-K and EP test different alternatives. Neither dominates; the bet is that the polynomial-gradient story wins in *training*, not in test-power on adversarial distributions. **DEFLECTED**.
- **Verdict**: PASS

## Stage 5 — Feasibility
- ~50 lines of code. Easy.
- **Verdict**: PASS

## Stage 6 — Killer Baseline (Skeptical Empiricist)
- Killer baseline: **`ExtendedJarqueBera` (already in library)** at matched λ — NOT just EppsPulley.
- **Attack**: if Hermite-6 ≈ ExtendedJarqueBera empirically (likely on n ≤ 256), the proposal is inert. UNREBUTTED — no published evidence that Hermite-6 specifically beats JB at SSL scales. ❌ **UNREBUTTED**.
- **Falsification sharpness**: ✅ proposal requires parity (0.3 pp) + ≥ 15 % variance reduction. Reasonable but the parity bar means even success is small.
- **Verdict**: WARN (one UNREBUTTED → downgrade)

## Stage 8 — Decision Gate
- FAIL: 0 · WARN: 3 (Stage 2 prior-art proximity, Stage 3 narrow novelty, Stage 6 dominated-by-JB risk) · UNREBUTTED: 1
- Per `decision-logic.md`: 0 FAIL + 3 WARN → **TOY EXPERIMENT FIRST** (downgraded from FULL by UNREBUTTED)
- Confidence: 🟡

## Final verdict: 🧪 **TOY** 🟡
- Toy: 12 GPU-h (4 arms × 3 seeds × ViT-S/100ep). Arms: EP@M=1024, ExtendedJB, Hermite-4, Hermite-6.
- Decision rule: Hermite-6 must beat **both** EP **and** ExtendedJB by ≥ 0.5 pp non-overlap CI → graduate. Beats EP but not ExtendedJB → reframe as "Hermite-6 ≡ JB" → KILL. Beats neither → KILL.
- Falsification trigger: D'Agostino & Stephens 1986 power tables suggest higher-moment tests beat lower-moment at n ≤ 256 only on heavy-tailed alternatives; ImageNet-10 embedding distributions are unlikely to be heavy-tailed enough.
- Dependency: should run **after** batch-2 Idea 1 (stacked-tests toy) lands — if stacked-{EP, AD, W} already wins decisively, Hermite-6 becomes a low-priority follow-up; if stacked-tests fail, Hermite-6 represents a different attack vector (orthogonal basis vs correlated stacking).
