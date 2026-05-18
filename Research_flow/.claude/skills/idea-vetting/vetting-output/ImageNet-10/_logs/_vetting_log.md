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
