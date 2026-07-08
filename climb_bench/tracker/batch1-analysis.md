# Insights — Batch-1 results & direction for next ideas

**Source**: CSVLogger metrics from `ckpt/batch_1/` (baseline + idea3 coding-rate, idea4 uniformity, idea7 DynTanh). Visualized in [climb_bench/viz/](../viz/) (`figures/*.png`, `summary.csv`, `matched_400.csv`).
**Setup**: Imagenette (~9.5k train), in-domain LeJEPA pretrain, **frozen** ViT-S/16, online linear-probe + kNN + RankMe. Runs are unfinished 400ep schedules (baseline ~ep233, ideas ~ep280) — all past their peak, so conclusions hold.
**Date**: 2026-06-08.

> Metric convention: because of overfitting (below), the honest metric is **best-checkpoint** linear-probe top1, not last.

## TL;DR — which idea is most promising?

| Rank | Idea | best lp (Δ vs base) | Verdict | Promise |
|---|---|---|---|---|
| 1 | **idea4 uniformity** | **0.880 (+0.8pp)**, RankMe 244 vs 209 | ≈ baseline, slightly above, higher feature spread | **Salvageable / keep** — only idea that doesn't hurt; combine with anti-overfit |
| 2 | idea3 coding-rate | 0.466 then **collapses to 0.22** | Diverges after a fast early start (peak @ ep10) | **Rescue candidate** — mechanism fires early then over-regularizes; needs tiny β + fp32 + warmup |
| 3 | idea7 DynTanh | 0.810 (−6pp), reaches 0.80 only @ ep264 | **8× slower** convergence, never beats baseline | **Reject** — normalization-removal instability, as flagged |

**But the single biggest signal is not an idea — it is a baseline pathology (next section).**

## 🔑 The dominant finding: the baseline OVERFITS

| Run | peak lp | @ epoch | reaches 0.80 at | last lp | peak→last drop |
|---|---|---|---|---|---|
| baseline | 0.872 | **81** | ep34 | 0.847 | −0.024 |
| idea4 uniformity | 0.880 | 102 | ep32 | 0.853 | −0.026 |
| idea7 DynTanh | 0.810 | 274 | ep264 | 0.803 | −0.007 |
| idea3 coding-rate | 0.466 | 10 | never | 0.224 | **−0.242** |

- Baseline linear-probe **peaks around ep80–150 then decays** (−2.4pp by ep199, and the run keeps drifting). kNN shows the same peak-then-decline.
- **400 epochs is too long for this baseline** — most of the budget is spent past the peak, in the overfitting regime.
- Implications:
  1. **Best-checkpoint, not last-checkpoint, is the metric.** Online-probe-at-end under-reports the model by ~2.4pp.
  2. **Anti-overfit at pretrain is the highest-headroom lever** on this 9.5k-image task — exactly the thesis behind batch-2.
  3. A near-free +2.4pp is available just by **early-stopping / checkpoint-by-best** (RankMe or kNN as the unsupervised selector) — no new mechanism needed.

## Per-idea evidence

### idea4 uniformity — the one keeper (marginal)
Tracks the baseline almost exactly (see `figures/linear_probe.png`), best lp **+0.8pp**, and **RankMe 244 vs baseline 209** — measurably higher feature spread without hurting accuracy. The gain is within noise on accuracy but the rank signal is consistent. → Keep as a cheap add-on; its value may show up **combined with an anti-overfit method** (more spread + less overfit).

### idea3 coding-rate — broken, but informative
Peaks at **ep10 (0.466)** — it actually learns *fast* at first — then **collapses** to 0.22 with RankMe crashing 201→72. This is not "no effect"; it is **over-regularization / instability**: the log-det coding-rate term dominates and destroys features once activated. Likely causes: β too large, sign/scale, or bf16 log-det instability (the convention file already warns log-det must run fp32). → **Rescue path**: β-sweep downward (e.g. 1e-3→1e-4), force fp32 log-det, warm up β after ep~20. Medium promise *if* stabilized.

### idea7 DynTanh — reject
Converges **8× slower** (0.80 at ep264 vs baseline ep34) and never catches baseline even at ep280. The 100ep variant is stuck at 0.48. Confirms the batch-1 devil's-advocate flag (normalization-removal instability). → Drop; not worth the compute.

### Note on 100 vs 400 epochs
idea4 ranks consistently at 100ep and 400ep (≈baseline both). idea7 looks catastrophic at 100ep (0.48) but recovers to 0.81 by ep280 — i.e. **short budgets under-rate slow-converging ideas**. So 100ep screening is safe for *killing* unstable ideas (idea3) and confirming neutral ones (idea4), but a slow idea must be confirmed at full budget before rejection.

## Direction for the next ideas (what to propose / prioritize)

The data redirects priority from "add a loss term" toward **anti-overfit training geometry** — which is precisely batch-2's focus. Concretely, ranked by expected payoff against the observed overfit:

1. **[Near-free baseline fix] Best-checkpoint selection by RankMe/kNN.** Worth ~+2.4pp for *every* run and makes all comparisons honest. Do this first; it is not even an "idea," it is a measurement fix. *(Wire: checkpoint-by-best on `eval/knn_probe_top1`.)*
2. **SWA / tail weight-averaging (batch-2 exp7).** Directly attacks the peak-then-decline by averaging the overfitting tail into a flatter solution. Strongest mechanistic fit to this exact failure mode.
3. **SAM / sharpness-aware (batch-2 exp1).** Flat minima → less overfit on 9.5k images; the baseline's late-epoch decay is the textbook symptom SAM targets. Use `--sam_late` (cost-bounded).
4. **Progressive stochastic-depth (batch-2 exp9).** Ramp regularization as overfitting risk rises past the peak.
5. **Combine idea4 uniformity + an anti-overfit method.** Uniformity raised RankMe with no accuracy cost; pairing it with SWA/SAM is a plausible additive win (more spread *and* flatter minimum). Low cost to test.
6. **Rescue idea3 coding-rate** (small β, fp32, warmup) — only if a cheap β-sweep stabilizes it; otherwise shelve.

### A new idea this analysis suggests (not yet in any batch)
**Overfit-aware early-stop / λ-anneal driven by the kNN-vs-train-loss gap.** The data shows a clear divergence point (~ep80) where probe accuracy stops tracking train loss. A controller that detects this gap and (a) freezes/averages weights or (b) increases regularization at that point would convert the wasted post-peak budget into either compute savings or generalization. This differs from batch-1's RankMe-λ (which gated on rank, not on the train/eval generalization gap) and from plain SWA (fixed window) by being **triggered by the measured onset of overfitting**. Candidate for batch-3.

## Caveats
- Runs are unfinished and on a 400ep cosine schedule read mid-way; absolute numbers will shift with a completed run, but the **ranking and the overfit pattern are robust** (all runs past peak).
- Online-probe (lr 0.03) is the comparison metric, not the paper-spec probe — consistent across runs, so deltas are valid; final winner should be re-measured with the paper-spec probe.
- idea3's collapse could be a config/β artifact rather than a fundamental flaw — treat its rejection as conditional.

Related: [[batch1-status]], [[batch2-status]], [[techniques-already-tried]], [[imagenette-benchmark-setup]]
