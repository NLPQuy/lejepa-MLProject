---
name: vetting-log
type: append-only
---
# Vetting log — ImageNet-10
<!-- entries appended below -->

## 2026-05-18 — Batch 1 vetting
- Benchmark: ImageNet-10
- Source: ideation-output/ImageNet-10/batch-1.md
- Ideas vetted: 6
- Verdicts: 0 FULL · 2 TOY · 3 REFRAME · 1 KILL
- Time: ~30 min · Mode: --climb-mode
- Survival: 33% (within 30–80 band, no spot-audit)
- Top pick: Idea 3 (Registers) — cheapest toy, 🟢 confidence
- Notable: 0 FULL SEND is a measurement gap, not an ideation gap. Baseline ImageNet-10 number must be fixed first.
- Re-vet trigger: when user reports toy results for Idea 3 or Idea 6, or when LeJEPA-vs-DINOv2 baseline measurement lands (re-vet Idea 2).

## 2026-05-18 — Batch 2 vetting
- Benchmark: ImageNet-10
- Source: ideation-output/ImageNet-10/batch-2.md
- Ideas vetted: 6
- Verdicts: 1 FULL · 2 TOY · 3 REFRAME · 0 KILL
- Time: ~25 min · Mode: --climb-mode
- Survival: 50% (in 30–80 band)
- Top pick: Idea 5 (ASHA HP sweep) — first FULL SEND across both batches; gates ranking of every other open idea
- Notable: 3 REFRAMEs share one failure mode — over-claimed gain magnitude where cited prior art was on a different regime (CNN/large-batch/larger-teacher). Surface to ideation skill as a calibration correction.
- Re-vet trigger: (a) when Idea-5 ASHA returns measured ImageNet-10 baseline, re-rank everything else against the real number; (b) when 150-ep vanilla baseline lands, re-vet Idea 6; (c) when Idea-1 stacked-tests toy returns, re-vet Idea 2.

## 2026-05-18 — Batch 3 vetting
- Benchmark: ImageNet-10 (Imagenette, linear probe top-1)
- Source: ideation-output/ImageNet-10/batch-3.md (--tier-mix 40/20/40, --given-vetting batch-2)
- Ideas vetted: 6 (P12 / P2 / P6 / P3 / P4 / P5)
- Verdicts: 2 FULL SEND (Ideas 2 SRHT, 3 PIT), 3 TOY (Ideas 1 co-distill, 4 Hermite, 6 rank-curriculum), 1 REFRAME (Idea 5 DDP-disjoint as engineering default), 0 KILL
- Time: ~30 min · Mode: --climb-mode
- Survival: 5/6 = 83 % (just above healthy band — audit done, structural not drift)
- Top pick: Idea 3 PIT-monitor (FULL SEND 🟢) — zero-risk, ship in parallel with batch-2 Idea 5 ASHA
- Notable: first batch with 2 FULL SENDs; first batch with 0 KILLs; both FULL SENDs are Tier-3 cross-domain (SRHT + PIT) validating the Tier-3 strategy
- Re-vet trigger: after batch-2 Idea 1 (stacked-tests toy) returns — re-evaluate Idea 4 (Hermite) priority based on whether orthogonal-basis still adds beyond stacked-correlated tests

## 2026-05-18 — Batch 4 vetting
- Benchmark: ImageNet-10
- Task: in-domain SSL embedding (LeJEPA, lejepa-vit-small.py)
- Source: ideation-output/ImageNet-10/batch-4.md
- Ideas vetted: 6
- Verdicts: 1 FULL SEND · 3 TOY · 2 REFRAME · 0 KILLED
- Time: ~35 min
- Survival: 67 % (healthy band, calibration improved from 83 % in batch-3)
- Top pick: Idea 1 (SAM / Friendly-SAM optimizer wrap) — 🟢 ship as ASHA 4th axis
- Notable: 2 REFRAMEs surface ideation skill-drift signals — redundancy-with-pipeline (Idea 2 vs SIGReg covariance pull) and experimental-economy collision (Idea 5 vs SRHT). Idea 3 Phase A is 0-GPU-h pre-flight probe-alignment check — run immediately on any baseline checkpoint.
- Re-vet trigger: after SRHT (batch-3 FULL SEND) ships, re-vet Ideas 4 & 5 with measured SRHT variance numbers.

## 2026-05-18 — Batch 5 vetting
- Benchmark: ImageNet-10
- Task: in-domain SSL embedding (LeJEPA, lejepa-vit-small.py)
- Source: ideation-output/ImageNet-10/batch-5.md (--tier-mix 30/20/50, --given-vetting batch-4)
- Ideas vetted: 6 (P3 / P2 / P1 / P3 / P5 / P8)
- Verdicts: 2 FULL SEND (Ideas 5 SIE-split, 6 saliency-crops), 2 TOY (Ideas 2 KSD, 4 Riesz-MMD), 2 REFRAME (Idea 1 t-design, 3 MMCR), 0 KILL
- Time: ~30 min · Mode: --climb-mode
- Survival: 67 % (matches batch-4 exactly — calibration steady in healthy band)
- Top pick: Idea 6 (saliency crops) — composite 2.7, lowest-risk highest-confidence; Idea 5 (SIE-split) is top expected-value with direct LeCun-lab evidence
- Notable: BOTH REFRAMEs are the recurring skill-drift symptoms identified in batch-4 vetting and *flagged in batch-5 ideation's own notes* — (a) MMCR's redundancy-with-SIGReg covariance pull = batch-4 W-MSE pattern; (b) t-design's variance-reduction family saturation = batch-4 Repulsive pattern. Skill discipline is working. The joint Phase-A synthetic-power test (Ideas 2 + 4) is 0 GPU-h and resolves the 4-way per-slice-statistic bake-off in 1 hr CPU.
- Re-vet trigger: (a) after Phase A (Ideas 2 + 4) returns power numbers, re-vet KSD priority; (b) after SRHT (batch-3 FULL SEND) lands with measured variance reduction, decide Idea 1 t-design disposition (archive / TOY-pri-6 / TOY-pri-4); (c) after Idea 3 MMCR 3-arm singleton-vs-combo ablation returns, decide combo vs singleton.
- Cross-skill signal: cumulative pattern coverage unchanged 9/12; 6 concrete composable survivors (PIT, SRHT, SAM, ASHA-ext, Saliency, SIE) — batch-6 should invoke --compose-mode formally instead of new patterns.

## 2026-05-18 — Batch 6 vetting
- Benchmark: ImageNet-10
- Task: in-domain SSL embedding (LeJEPA, lejepa-vit-small.py)
- Source: ideation-output/ImageNet-10/batch-6.md (--tier-mix 30/20/50, --given-vetting batch-5)
- Ideas vetted: 6 (P6 / P3 / P1 / P3 / P2 / P1)
- Verdicts: 0 FULL SEND, 4 TOY (Ideas 1 RankMe-ctrl, 3 iBOT-SIGReg, 4 Sinkhorn→FULL on Phase A, 5 Poincaré), 2 REFRAME (Idea 2 registers = duplicate-of-batch-1 TOY, Idea 6 PH = near-KILL on Stage 4+6 fail), 0 KILL
- Time: ~25 min · Mode: --climb-mode
- Survival: 67 % (3rd batch in a row matching 67 % — calibration steady)
- Top pick: Idea 4 Sinkhorn (only graduation-eligible candidate; Phase A 15 GPU-h decisive); fastest = joint Idea 1-A + Idea 5-A (0 GPU-h, 1 hr CPU each)
- Notable: BOTH REFRAMEs are *ideation skill process failures* (not idea failures):
  (a) Idea 2 = ideation skill did not consult `_toy_queue.md` — proposed an active TOY as a new idea.
  (b) Idea 6 = ideation skill missed Moor 2020 / Trofimov 2023 PH-as-SSL prior art; novelty inflated; high-d concentration of measure caught at Stage 4.
  Cross-skill feedback to ideation: add duplicate-check-against-active-TOY pre-flight; require in-field-SSL search query when T3 ideas are drafted (not just cross-domain root).
- Re-vet trigger: (a) Phase A results for Ideas 1 + 5 (free, this week); (b) Sinkhorn 3-arm result → re-vet for SIE-split + saliency-crops interactions; (c) iBOT-SIGReg vs MAE-aux head-to-head (consolidates batch-4 MAE-aux TOY).
- Cross-skill signal: compose-mode recommendation now 4 batches in a row. Cumulative survivor stack 6–8 concrete components. Batch-7 should formally enumerate compositions; stop proposing new patterns.

## 2026-05-19 — Batch 7 vetting
- Benchmark: ImageNet-10 (Imagenette linear probe)
- Source: ideation-output/ImageNet-10/batch-7.md
- Ideas vetted: 5 (all Tier 3, user-directed 100 % T3 override)
- Verdicts: 0 KILL / 2 REFRAME / 3 TOY / 0 FULL SEND
- Time: ~22 min
- Survival: 60 % (first time below 67 % since b2 — attributable to T3-heavy mix)
- Top pick: Idea 3 Adversarial max-sliced SIGReg → FULL SEND on Phase A pass (free 2-hr sanity); potentially supersedes variance-reduction sampler family
- Notable:
  - Idea 4 REFRAMED for *original-design measures-wrong-control* (Stage 6 FAIL); reframe = saliency-init RL vs saliency-frozen — should ship in batch-8
  - Idea 5 REFRAMED for *0-cost prerequisites deferred to vetting* (Cramér-Wold↔ETF redundancy check); run pre-checks before any compute
  - Process gaps: (a) self-flagged EXTENDS-bordering-DUPLICATE ideas should auto-trigger in-batch reframe (Idea 4); (b) identified `0-cost` prerequisites should run at draft-time, not be deferred (Idea 5)
- Re-vet trigger: Idea 2-A + Idea 3-A Phase A results (free, ~3 hr total wall-clock); Idea 1 after b6 Sinkhorn Phase B settles
- Cross-skill: compose-mode recommendation now 5 batches in a row; user should formally choose between T3-novel-axis continuation vs compose-mode enumeration for batch-8

## 2026-05-19 — Batch 7 ADDENDUM vetting (Idea 6 quantum-themed)
- Benchmark: ImageNet-10 (Imagenette linear probe)
- Source: ideation-output/ImageNet-10/batch-7-idea6-addendum.md (added mid-session per user request)
- Idea vetted: 1 (Idea 6 — SU(d)-structured-orthogonal projector, quantum-circuit-inspired classical analog)
- Verdict: 1 TOY (Rule #5: 0 FAIL + 4 WARN)
- Time: ~8 min
- Top pick (incremental): adds to batch-7 TOY queue at 12 GPU-h
- Notable:
  - Quantum framing is decorative (Stage 1 WEAKENED) — the empirical question (structured-orthogonal vs MLP projector with strong wd) is well-shaped regardless.
  - VNE-as-SSL direction (arXiv:2304.01434) is direct prior art that closes the von-Neumann-entropy-regularizer angle — flagged for future ideation.
  - Mutually exclusive with b6 Poincaré TOY (same projector axis).
  - Compose-mode tie-in with Idea 3 (max-sliced): "lean SIGReg + lean projector" frees ~30% effective epochs at same budget.
- Updated batch-7 survival: 4/6 = 67 % (back into b4/b5/b6 calibration band).

## 2026-05-19 — Batch 7 SECOND ADDENDUM vetting (Idea 7 FM-SIGReg)
- Benchmark: ImageNet-10 (Imagenette linear probe)
- Source: ideation-output/ImageNet-10/batch-7-idea7-addendum.md (added mid-session per user request "improve SIGReg with flow matching")
- Idea vetted: 1 (Idea 7 — FM-SIGReg: transport-based marginal-shape regularizer via CFM toward N(0,I))
- Verdict: 1 TOY (Rule #5: 0 FAIL + 4 WARN)
- Time: ~8 min
- Top pick (incremental): adds to batch-7 TOY queue at 10 GPU-h (Phase B), 0 GPU-h Phase A
- Notable:
  - **Closes the SIGReg-term axis** when combined with b7-I2 Hyvärinen and the closed per-slice family. Recommendation to ideation: stop proposing new SIGReg-term mechanisms.
  - **Mechanism-distinct from every existing SIGReg attack**: per-slice tests (test-based), Hyvärinen (score-based), max-sliced (worst-case test), FM-SIGReg (transport-based).
  - **Strongest reframe target**: "annealed Hyvärinen" — DDPM-style noise schedule on b7-I2 score matching captures the smoothing benefit without FM machinery. Falls out naturally if FM-OT arm (C) ties Hyvärinen and FM-diffusion (D) loses.
  - **Killer baseline** is b7-I2 Hyvärinen, not the EP baseline. Score-FM equivalence in small-σ regime (Song-Ermon 2020) means FM-OT may reduce to smoothed Hyvärinen; arm D (σ=0.1) is the load-bearing distinctness test.
  - Closest prior art: arXiv:2512.23956 "Implicit geometric regularization in FM via Stein operators" (Dec 2025) — regularizes the flow itself, not an upstream encoder. Goal slot empty.
- Updated batch-7 survival: 5/7 = 71 % (just inside upper edge of 30–70 % healthy band)
- Re-vet trigger: Idea 7-A Phase A results (free, 1 hr CPU); then 7-B 10-GPU-h bake-off

## 2026-05-19 — Batch 7 Idea 7 RE-VET (v2 after targeted research)
- Source: idea-7-vetting-v2.md supersedes idea-7-vetting.md
- Trigger: user request "research lại idea trên để vượt vetting"
- Live searches performed (4 queries): closed-form FM velocity / FM KL Wasserstein bounds / FM gradient variance vs score / FM vs score multimodal
- Critical finds:
  - arXiv:2511.05480 (Nov 2025) — `KL(P_z || N(0,I)) ≤ C(d,T)·L_FM`; explicit constant C=T=1 for OT-displacement → fixes S4 monitoring WARN
  - Explicit Flow Matching (ExFM) — closed-form denoised regression target → fixes S1 critic-ratio WARN
  - Multisample FM (arXiv:2304.14772, ICML 2023) — Hungarian-matching coupling → zero gradient variance at convergence → reduces S6 score-FM-equivalence concern
  - Non-Gaussian target capability (Albergo §3.3, arXiv:2303.08797) — Hyvärinen *cannot* use non-Gaussian targets (no closed-form score) → load-bearing differentiator → fully fixes S6
- v2 verdict: 🚀 FULL SEND 🟢 (Rule #4: 0 FAIL + 0 WARN + S5 PASS)
- v2 upgrades:
  - Upgrade A — ExFM regression target (variance ↓)
  - Upgrade B — certified KL upper bound from L_FM (interpretability ↑)
  - Upgrade C — Multisample OT batch-level Hungarian coupling (gradient variance ↓)
  - Upgrade D — non-Gaussian target Σ* inherits RankMe 0.6·d setpoint (no new HP)
- 6-arm v2 falsification: baseline-EP / Hyvärinen / FM-v1 / FM-v2-N(0,I) / mix / FM-v2-anisotropic
- Cost: ~12 GPU-h (1 extra arm vs v1)
- Updated batch-7 stats: 0 KILL / 2 REFRAME / 4 TOY / 1 FULL SEND; survival 5/7 = 71 %
