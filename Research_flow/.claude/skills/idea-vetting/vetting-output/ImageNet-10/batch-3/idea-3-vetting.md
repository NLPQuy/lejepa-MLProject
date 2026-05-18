# Vetting — Batch 3 Idea 3: PIT-uniformity held-out monitor
**Pattern**: P6 · **Tier**: 3 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
- **Attack 1**: idea-or-engineering — "add a callback" is plumbing. **Rebuttal**: the *research claim* is that PIT-AD on held-out val correlates with linear-probe rank-order at ρ ≥ 0.7, enabling cheaper ASHA-rung evaluation. That's a measurement-with-hypothesis, not pure logging. ⚠️ **WEAKENED** — borderline between "tool" and "idea"; the correlation claim is what makes it pass.
- **Verdict**: PASS w/ flag

## Stage 2 — Prior Work Attack
- **Attack 1**: RankMe (Garrido et al., ICML 2023) and LiDAR already do label-free model selection for SSL. PIT is just another such proxy. **Rebuttal**: RankMe measures *effective rank*; LiDAR measures *informativeness*. PIT measures **distributional match to N(0,I)** on held-out — directly aligned with LeJEPA's SIGReg target. The probes are orthogonal signals. **DEFLECTED**.
- **Attack 2**: PITOS (arXiv:2510.22854) does PIT GoF in stats — applied to SSL is not their domain. **Rebuttal**: that's the point of Tier-3 transfer; the cross-domain application is the novelty. **DEFLECTED**.
- **Verdict**: PASS

## Stage 3 — Novelty Decomposition
- Novel piece: PIT-AD as SSL model-selection proxy *specifically aligned with SIGReg objective*.
- Already published: RankMe, LiDAR (label-free SSL proxies); PIT GoF (stats classic).
- Net novelty: NOVEL composition (cross-domain transfer with clear alignment story).
- **Verdict**: PASS

## Stage 4 — Theory Grounding
- Φ is monotone, PIT is exact under H₀ → ✅ U(0,1) under perfect SIGReg.
- AD-on-U(0,1) is closed-form and consistent.
- **Attack**: held-out val with a *fixed* slice ensemble — fixed slices may live in low-variance directions of the trained model, biasing the test. **Rebuttal**: fix M=512 random slices at init; over M directions on S^(d−1) the probability that all hit low-variance directions is exponentially small. Resample slices once per checkpoint family if concerned. **DEFLECTED**.
- **Verdict**: PASS

## Stage 5 — Feasibility
- Read-only callback, no training impact. Trivial.
- **Verdict**: PASS

## Stage 6 — Killer Baseline
- Killer baseline: existing `OnlineProbe` callback as model-selection signal.
- **Attack**: if PIT-AD's Spearman ρ with linear probe is < 0.5, the monitor is useless for selection. Proposal admits this and provides a graceful degradation (collapse detector). **Rebuttal**: deliverable is well-bracketed — three regimes (ρ < 0.5 reject, 0.5–0.7 collapse-detector, ≥ 0.7 ASHA rung). Honest. **DEFLECTED**.
- **Attack 2**: gain mid is +0.5 pp — that's *not* a direct lift, it's a "more ASHA arms in same budget" interpretation. Is this gain real? **Rebuttal**: the gain only materialises if (a) PIT-AD ρ ≥ 0.7 AND (b) the recovered compute is reinvested into more ASHA arms. Two conditional steps. ⚠️ **WEAKENED** — gain claim is contingent.
- **Verdict**: PASS w/ flag (contingent gain)

## Stage 8 — Decision Gate
- FAIL: 0 · WARN: 2 (idea-vs-tool flag, contingent gain)
- Per `decision-logic.md`: 0 FAIL + ≤ 2 WARN + Stage 5 PASS → **FULL SEND**
- Confidence: 🟢 (low risk, read-only, clean falsification)

## Final verdict: ✅ **FULL SEND** 🟢
- Priority: HIGH — zero-risk, runs in parallel with any other experiment, produces a correlation dataset that has its own value regardless of pp lift.
- Composite × confidence: 2.7 × 1.0 = 2.7
- Ship-as: PR that adds `PITMonitor` callback to the recipe; first deliverable is the ρ measurement across ≥ 1 full training trajectory.
- Mandatory refinement: also log per-epoch ρ vs RankMe and ρ vs LiDAR — establishes the *relative* signal quality, not just absolute.
