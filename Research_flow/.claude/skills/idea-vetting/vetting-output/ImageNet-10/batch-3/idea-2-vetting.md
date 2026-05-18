# Vetting — Batch 3 Idea 2: SRHT structured slices
**Pattern**: P2 · **Tier**: 3 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
- **Attack 1**: idea-or-engineering gate — "swap RNG for FWHT" is borderline engineering. **Rebuttal**: the *mechanism* is variance-reduction on the SIGReg MC estimator via structured projections; that's a named principle (SRHT, Tropp 2011) with a research claim (lower estimator variance ⇒ better gradient quality ⇒ better representations). Not pure plumbing. **DEFLECTED**.
- **Verdict**: PASS

## Stage 2 — Prior Work Attack (Prior-Work Hunter)
- **Attack 1**: SRHT-in-DL is decade-old (random features, sketching SGD). Why is this novel? **Rebuttal**: novelty is the *target* — applying SRHT to the slice generator of a normality-test SSL loss, not to feature compression. **DEFLECTED**.
- **Attack 2**: Random Feature SSL (e.g., the OpenReview paper) already plays in this space. **Rebuttal**: that paper *reconstructs* random projections of data; this *replaces* the projection ensemble inside an existing loss. Orthogonal use. **DEFLECTED**.
- **Verdict**: PASS

## Stage 3 — Novelty Decomposition (Critical Reviewer)
- Novel piece: applying SRHT specifically to `SlicingUnivariateTest`.
- Already published: SRHT itself (Tropp 2011), random-projection SSL.
- Net novelty: EXTENDS.
- **Verdict**: PASS

## Stage 4 — Theory Grounding (Theorist)
- SRHT preserves isotropy on S^(d−1) up to log factors per Tropp 2011 — ✅ Cramér–Wold lifts.
- **Attack**: at M close to d, structured-row correlations may violate marginal-independence assumed by per-slice tests. **Rebuttal**: with d=384 pad-to-512, M=1024, oversampling ratio M/d ≈ 2.6 — Tropp's bound holds with constant slack; per-slice statistics treat each row independently, structured correlation across rows is irrelevant to the test value. **DEFLECTED**.
- **Verdict**: PASS

## Stage 5 — Feasibility (Pragmatic PM)
- 1-line code change + cached Hadamard matrix. Trivial.
- Zero-padding 384→512 wastes 25 % of FWHT compute — negligible (slicing is not bottleneck).
- **Verdict**: PASS

## Stage 6 — Killer Baseline (Skeptical Empiricist)
- Killer baseline: Gaussian slices at same M, same (λ, lr, wd).
- **Attack**: gain mid is only +0.6 pp — within seed variance (~0.3–0.5 pp on Imagenette). Could be noise. **Rebuttal**: the proposal correctly anchors the *primary* falsification on SIGReg-loss variance reduction (≥ 20 %), not on linear probe. Variance is a measurable mechanism check independent of probe noise. **DEFLECTED**.
- **Attack 2**: at M=1024 the MC estimator is already saturated; the variance-reduction story does not cash. **Rebuttal**: proposal explicitly hedges this by including M ∈ {128, 256} ablation where SRHT's edge is largest. **DEFLECTED**.
- **Falsification sharpness**: ✅ dual criterion (variance + parity).
- **Verdict**: PASS

## Stage 8 — Decision Gate
- FAIL: 0 · WARN: 0 · falsification sharp · low cost
- Per `decision-logic.md`: 0 FAIL + 0 WARN + Stage 5 PASS → **FULL SEND**
- But: small gain claim (+0.6 mid) + parity-acceptable falsification means the **expected lift is small**. Promote with the explicit understanding that this is a variance/wall-clock win, not a pp lift.
- Confidence: 🟢

## Final verdict: ✅ **FULL SEND** 🟢
- Priority: medium (low cost, low pp lift, real stability/speed benefit).
- Ship after batch-2 Idea 5 (ASHA) returns (λ, lr, wd). Run at fixed best HP, 3 seeds, with M ∈ {128, 256, 1024} ablation for the variance-reduction claim.
- Composite × confidence: 2.8 × 1.0 = 2.8
