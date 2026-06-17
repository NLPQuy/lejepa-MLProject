# Rejection log

| Date | Batch | Stage | Idea | Tag | Evidence |
|------|-------|-------|------|-----|----------|
| 2026-05-27 | VILD batch-6 | Draft | Stiefel-barycentre BMA over {R_C, R_E, R_E_subrank} | OFF-LIMITS | User explicit OFF-LIMITS in task brief: `Stiefel barycentre across {R_C, R_E}`. Dropped before verification. |
| 2026-05-27 | VILD batch-6 | Draft | Per-bench config table router | OFF-LIMITS | User explicit OFF-LIMITS: `Bench-specific config tables`. Dropped. |
| 2026-05-27 | VILD batch-6 | Draft | SURE-stopped rounds (Deledalle-Vaiter-Peyré-Fadili) | DUPLICATE | Structurally equivalent to Idea 2 held-out CV stopping (same outer-loop signal, different bias-correction recipe). Would push P6 over its 2-idea quota. Kept Deledalle 2014 as a supporting citation under Idea 2 instead. |
| 2026-05-27 | VILD batch-6 | Draft | Hodges 1951 superefficient combo | RISK (theoretical) | Hodges' superefficiency is pointwise-only and the maximum risk is unbounded (Le Cam 1953). Not a defensible practical mechanism for a benchmark-shipping pipeline. Cited in search log; dropped from idea pool. |
| 2026-05-27 | VILD batch-6 | Draft | Information-theoretic round budget `rounds = ⌊log₂(N/D)⌋` | NOT-AN-IDEA / hand-formula | Mentioned in user's N3 priority list as a candidate, but it is a hand-coded heuristic without a theorem derivation. Would violate `no hand-tuned λ schedule` OFF-LIMITS. Dropped at draft. |
| 2026-05-30 | VILD batch-17 | Draft | SUGAR/SURE multi-parameter operator-intensity selection (Deledalle-Vaiter 2014) | DUPLICATE (vs batch-6) | SURE-based selection of a continuous parameter vector overlaps batch-6's SURE-stopped-rounds lens; kept SUGAR [arXiv:1405.1164] as a supporting citation only. Decision-theory slot filled instead by James-Stein admissible shrinkage (Idea 5, different tool) — avoids 3× P6 and batch-6 overlap. |
| 2026-05-30 | VILD batch-17 | Draft | Shapley-value operator-coalition selection (cooperative game theory) | TIER-BALANCE | Genuine T3 candidate for co-fire interaction handling, but adding it pushed T3 to 5/8 (>50% band ceiling for 30/30/40) and starved the T1 in-field count. Interaction handling covered instead by Idea 7 (PCA-basis-safe composition, T1) + Idea 1 (hysteresis anti-chatter). Not verified; dropped at draft. |
| 2026-05-30 | VILD batch-17 | Devil's-advocate | Soft MoE gate (Idea 2) — ranking | DOWNGRADE (not reject) | [arXiv:2202.09368] + routing-collapse literature: token-choice MoE suffers load imbalance; standard cures need TRAINED aux losses (banned). Idea KEPT but ranked #2 (from raw-composite #1); Expert-Choice Routing added as Contrasting. |

## CultureCommittee 5-bench — Batch 1 — 2026-05-31
- Rejected: 0 / 10. All ideas passed the 7-step pipeline.
- Downgrades (not rejections): Idea 2 (per-view contextual calibration) ranking demoted one slot — devil's-advocate arXiv:2404.08382 ("Look at the Text") shows instruction-tuned models need less option-debias; contrasting ref attached. Idea 9 (robust ordinal Wasserstein barycenter) gain-confidence -> 🔴 per gain-sanity (high-variance, distribution-match-only).

## CultureCommittee 8-bench — Batch 5 (B3 shared-bias) — 2026-05-31
- Rejected: 0 / 10. All passed the 7-step pipeline.
- Downgrades (not rejections): Idea 2 (PCA-flip shared-component) -1 slot via devil's-advocate (Raunak 2020 + Stable-Anisotropic-Regularization arXiv:2305.19358 — removing top principal components can destroy useful signal); mitigation = eigengap gate + r<=1 + LEACE surgical alternative; contrasting refs attached. Idea 7 (CCS/DLK latent-truth direction) -1 slot via devil's-advocate (Farquhar et al arXiv:2312.10029 — CCS finds the most-prominent feature, not truth); mitigation = answer-subspace restriction + probe ensemble + Cluster-Norm (2407.18712).
- Top-1 (Idea 5 PriDe) DA caveat (kept, not downgraded): debiasing harms when the prior is itself a correct prior -> alpha dispersion gate (full removal on NormAd acc, gated on distribution benches); contrasting refs arXiv:2405.02743, 2410.14248.

## batch-6 (2026-05-31, CultureCommittee 8-bench, BREAK B2 EXCHANGEABILITY)
- 0 REJECTED.
- 1 DOWNGRADED: Idea 2 (Factorial-ANOVA nuisance main-effect removal) | stage=Devil's-advocate | tag=NON-ADDITIVITY | evidence=arXiv:1911.04974 (fANOVA main/interaction effects non-identifiable; additive subtraction biased under persona x order interaction) -> demoted from raw-composite-top to quick-win; Idea 3 (anchor regression, soft gamma) promoted to Top-1 (degrades gracefully under partial invariance).
