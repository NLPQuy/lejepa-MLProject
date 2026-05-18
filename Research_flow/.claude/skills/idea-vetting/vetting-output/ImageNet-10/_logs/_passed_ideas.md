---
name: passed-ideas
type: append-only
---
# FULL SEND ideas — ImageNet-10
<!-- entries appended below -->

## 2026-05-18 — Batch 1
*No FULL SEND verdicts this batch.* See `_toy_queue.md` for graduation candidates.

## 2026-05-18 — Batch 2

#### Idea 5: Multi-fidelity ASHA HP sweep (λ, lr, wd)
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 3.2
- Gain (mid): +1.5 pp (anchored: matches the missing measurement, not pure HP win)
- Cost: ~12 GPU-h (8-arm ASHA, 25→50→75→100ep rungs, 2 seeds at top rung)
- Priority: HIGHEST — blocks ranking of every other open idea (batch-1 toys, batch-2 reframes)
- Risk-mitigation: (a) use **kNN-on-batch top-1** as the promotion metric, not linear probe (linear probe at low rungs is non-predictive); (b) explicit fallback deliverable = measured baseline + landscape plot even if λ-landscape is flat
- Source: ideation-output/ImageNet-10/batch-2.md Idea 5
- Status: queued — recommend ship next.

## 2026-05-19 — Correction to Batch 2 Idea 5

#### Idea 5: Multi-fidelity ASHA HP sweep — RETRACTED
- Original verdict: FULL SEND (2026-05-18) — **incorrect**.
- Corrected verdict: **KILL `not-an-idea`** — pure HP sweep with zero mechanism contribution. Should never have been drafted by ideation; should have been instant-FAILed at Stage 1.
- Reframe: move to project prerequisites / `Notes & warnings` of any future batch as "measured baseline + HP-anchor needed before idea ranking is meaningful". Run it as engineering, not as a vetted research idea.
- Process bug: both skills failed.
  - Ideation: mislabeled HP sweep as P7 (Iterate) — P7 is self-refine, not search. Pattern catalog already said "if no pattern fits, skip the idea"; the right move was to drop, not relabel.
  - Vetting: let "measurement is the deliverable" pass Stage 1 + Stage 3 in `--climb-mode`. The mode was treated as a permission to admit engineering tasks; that was wrong.
- Skill fixes applied (2026-05-19):
  - `benchmark-climb-ideation/patterns/pattern-catalog.md` — added §NOT-an-idea filter listing HP sweeps / just-train-longer / re-runs / refactors / pure measurement as drops.
  - `benchmark-climb-ideation/SKILL.md` — Step 3 invokes the filter before drafting; new Anti-pattern entries.
  - `idea-vetting/stages/1-problem-framing.md` — new idea-or-engineering gate runs first; new FAIL tag `not-an-idea`; explicit note that `--climb-mode` does NOT override.
  - `idea-vetting/rules/decision-logic.md` — new Priority Rule 0 routes `not-an-idea` straight to KILL.

## 2026-05-18 — Batch 3

#### Idea 2: SRHT structured slices
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 2.8
- Gain (mid): +0.6 pp (small; real value is variance/stability/speed, not pp)
- Cost: ~4 GPU-h (3 seeds × 100ep at fixed best HP from ASHA + M ablation)
- Priority: medium — ship after batch-2 Idea 5 (ASHA) provides (λ, lr, wd)
- Risk-mitigation: primary falsification = SIGReg-loss running-std reduction ≥ 20 % (mechanism), not linear-probe pp (which is small and seed-noisy)
- Source: ideation-output/ImageNet-10/batch-3.md Idea 2
- Status: queued.

#### Idea 3: PIT-uniformity held-out monitor
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 2.7
- Gain (mid): +0.5 pp (contingent — only cashes if ρ ≥ 0.7 enables more ASHA arms)
- Cost: ~0 (read-only callback; piggybacks on any running training job)
- Priority: HIGH — ship in parallel with batch-2 Idea 5 ASHA; first deliverable = ρ(PIT-AD, linear-probe) on the first complete trajectory
- Risk-mitigation: graceful degradation across 3 ρ regimes (< 0.5 reject, 0.5–0.7 collapse detector, ≥ 0.7 ASHA evaluator). Mandatory refinement: also log ρ vs RankMe and ρ vs LiDAR for relative signal quality.
- Source: ideation-output/ImageNet-10/batch-3.md Idea 3
- Status: queued.

#### Idea 1 (batch-4): SAM / Friendly-SAM optimizer wrap
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 2.8
- Gain (mid): +0.8 pp linear probe
- Cost: ~45 GPU-h (4-arm × 3 seeds × 100 ep)
- Priority: 1 (cheapest cumulative FULL SEND that hasn't shipped; folds into ASHA as 4th axis)
- Risk mitigation: include SWA-AdamW arm (Stage 6 catch); matched-wall-clock control (not matched-epoch); ASAM fallback if Friendly-SAM under-delivers
- Source: ideation-output/ImageNet-10/batch-4.md, idea 1
- Status: queued — ship as ASHA 4th axis after Step-0 lands

## 2026-05-18 — Batch 5 — ImageNet-10

#### Idea 5: SIE invariant + equivariant split predictor
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 2.5 (× 1.0 = 2.5)
- Gain (mid): +0.9 pp linear probe
- Cost: ~30 GPU-h + ~2 days eng (augmentation-pipeline refactor for Δ-bookkeeping)
- Priority: 2 (run after Idea 6 ships; needs ASHA-best HP)
- Risk-mitigation: 3-arm experiment with matched-d-invariant control (d=256, full invariance) per Stage 6 refinement — confirms gain is from decomposition, not just capacity. Built-in decomposition-collapse check (z_full probe < z_inv probe required).
- Source: arXiv:2302.10283 (Garrido-Najman-LeCun SIE 2023) + arXiv:2503.18753 (Wang et al 2026 equivariance-coherence) — LeCun-lab provenance + direct linear-probe evidence
- Status: queued behind Idea 6 and Step-0 ASHA

#### Idea 6: Saliency-guided crop region sampling
- Verdict: FULL SEND
- Confidence: 🟢
- Composite: 2.7 (× 1.0 = 2.7) — **top of batch-5**
- Gain (mid): +0.5 pp linear probe (revised down from +0.8 pp at Stage 6 — Imagenette's higher object-centricity than raw IN1K reduces ceiling)
- Cost: ~30 GPU-h (3-arm × 3-seed × 100-ep + per-image saliency precompute)
- Priority: 1 — drop-in sampler change, run alongside Step-0 ASHA
- Risk-mitigation: 2-arm (naive local-std saliency vs encoder-attention saliency bootstrapped after epoch 50) at α=0.6 per Stage 5 refinement. α ∈ {0.3, 0.6, 1.0} micro-sweep; α=1 must NOT dominate α=0.6 (mechanism check)
- Source: arXiv:2210.16776 (Saliency in CSSL 2022) + arXiv:2504.19824 (Taming Randomness 2025) + ContrastiveCrop CVPR 2022
- Status: ship in parallel with Step-0 ASHA

## 2026-05-18 — Batch 6 — ImageNet-10
*No FULL SEND verdicts this batch.* All 4 surviving ideas are TOY (Phase A free for 3 of them). Idea 4 (Sinkhorn) is the most-likely graduation candidate via its 15-GPU-h Phase A — re-vet on results.
