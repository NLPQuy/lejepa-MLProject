# Idea Batch 2 — CultureCommittee 5-bench / P* fusion-operator paradigm survey
**Generated**: 2026-05-31 (panel-fusion batch-2)
**Skill invocation**: `/benchmark-climb-ideation` (RACECAR project; ideation lens = full estimation/optimization-paradigm space for P*)
**Relation to batch-1**: COMPLEMENT, not replacement. Batch-1 carried the in-field accuracy/de-sycophancy operators (reliability-weighted median, per-view calibration, CAD/DoLa axes, dispersion-temperature, neutral-routing) plus 3 fusion transfers (log-pool, depth-trim, ordinal W-bary). Batch-2 is the **estimation-paradigm map**: each idea is a distinct *solver* for the optimal fused distribution P* over the answer simplex, prioritizing the spread-preserving operators that fix the R1/R2 finding that the geometric median **over-collapses spread** on the four distribution-match benches.

## Inputs
- Benchmarks: NormAd-ETI (acc) + DICES-350/990 (base-2 JSD ↓) + GlobalOpinionQA (1−JSdist ↑) + VITAL (JS dist ↓) + Scruples (base-2 JSD ↓ + acc).
- Task: training-free, label-free fusion of K single-model panel views (ONE frozen Qwen2.5-7B-Instruct called K times under persona×paraphrase×order perturbations) into P* over the answer simplex. Post-forward logit math only; never generate.
- Existing pipeline: `exps/exp003_single_model_panel.py` — `[1]` multi-axis panel → `[2]` geometric-median barycenter (Weiszfeld) → `[3]` decode/metric. **Every batch-2 idea swaps fusion `[2]`** (panel `[1]`, decode `[3]` unchanged) ⇒ all `enhance-existing`.
- Pain point (R1/R2): the geometric median is a robust *point estimate* → ideal for NormAd argmax but it **collapses the spread** that DICES/GOQA/VITAL/Scruples reward (they score the *shape* of P* against a human distribution). Need operators that keep robustness **without** crushing legitimate pluralism.
- Constraints: single model only (K calls = the agents; fusing distinct models FORBIDDEN); no trainable params; no generation; no test-set tuning / magic thresholds.
- Budget: Kaggle T4 / RTX Pro 6000, offline, K cheap forwards/item.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 8 indexed ideas (+ 5-paradigm appendix map) |
| Tier 1 / 2 / 3 (counts) | 2 / 3 / 3 |
| Tier mix vs configured 45/35/20 | 25/37/37 — ⚠ T1 below band, T3 above (intentional; see Notes) |
| Scope mix | 8 enhance-existing / 0 greenfield (≥50% ✓) |
| Patterns used | P3×2, P2×2, P1, P5×2, P7 (5 distinct ✓; ≥1 P2 ✓) |
| Distinct venues | J.ACM, Math of OR, JRSS-B, IEEE T-IT, ICLR, Found.Comp.Math, J.Math.Sociology, MDPI Algorithms (≥8) |
| Time windows | <12mo (2), 12-36mo (2), 36-72mo (2), 72+mo (2) |
| Avg feasibility | 4.0/5 |

## Summary table (composite = 0.4·Gain + 0.3·Feas + 0.2·(XL−Effort) + 0.1·Novelty; all 1–5)
| # | Title | Paradigm | Pattern | Tier | Feas | Effort | Score |
|---|-------|----------|---------|------|------|--------|-------|
| 1 | α-divergence (Rényi/quasi-arithmetic) centroid | Information geometry | P3 | 1 | 4 | M | 4.20 |
| 2 | MaxEnt moment-matching I-projection barycenter | Information projection | P2 | 3 | 4 | M | 3.95 |
| 3 | Beta-recalibrated linear opinion pool (flexible dispersion) | Opinion pooling | P1 | 3 | 5 | S | 4.25 |
| 4 | DRO minimax barycenter over a φ-divergence ball | Distributionally-robust opt | P2 | 2 | 3 | L | 3.15 |
| 5 | Robust-PCA consensus / sparse-outlier decomposition | Robust subspace | P5 | 2 | 3 | M | 3.25 |
| 6 | Median-of-Means block barycenter | Robust M-estimator | P3 | 2 | 5 | S | 4.25 |
| 7 | Plackett-Luce / spectral rank-aggregation (order axis) | Rank aggregation | P5 | 1 | 4 | M | 3.45 |
| 8 | Friedkin-Johnsen stubborn-agent fixed point | Consensus dynamics | P7 | 3 | 4 | M | 3.50 |

## Top-3 recommendations
### 🏆 Top-1 by composite — and ⚡ Quick win
**Idea 3: Beta-recalibrated linear opinion pool** — 4.25, Effort S.
Ranjan–Gneiting (JRSS-B 2010) prove that *any* non-trivial linear pool of calibrated forecasts is **under-dispersive** — i.e. the plain mean (your `mean_panel`) is already too sharp before the median makes it worse. A two-parameter beta-CDF reshape of the pooled CDF restores *flexible* dispersion in closed form. Cheapest possible fix for the exact R1/R2 failure, and it is a fusion operator (combines the views), not just a temperature readout.

### 🎲 Big bet
**Idea 1: α-divergence centroid** — Score 4.20, Novelty 5.
One continuous knob α that **subsumes** `mean_panel` (linear pool), batch-1's log-pool, and a mode-seeking limit as special cases; α tunes exactly how much spread to keep. The principled, theorem-friendly headline operator — pick α from panel dispersion, not the eval set.

### 🛡️ Safe bet
**Idea 6: Median-of-Means block barycenter** — Feas 5, classic sub-Gaussian theory.
Partition the K views into m blocks, average within each block (this **retains** within-block spread), then take the geometric median of the m block-means. High-breakdown like the median but far less spread-collapse, with a clean concentration theorem. No-op → `mean_panel` at m=1. Distinct from batch-1's depth-trim (that *discards* views; this *averages in blocks*).

---

## Ranked ideas

### Idea 1: α-divergence (Rényi / quasi-arithmetic) centroid
- **Paradigm**: Information geometry (α-divergence centroid on the statistical manifold).
- **Pattern**: P3 (Replace). **Tier**: 1. **Scope**: enhance-existing — replaces fusion `[2]`.
- **One-liner**: Fuse the K views as the **α-centroid** `P* = argmin_P Σ_v D_α(P, P_v)`; the single α slides continuously from the spread-preserving arithmetic mean (α→1, mass-covering) through the geometric/log-pool mean to a mode-seeking limit, so you *dial in* exactly how much pluralism to keep instead of always collapsing it.

**(a) Objective + post-forward solver**: minimize `Σ_v D_α(P,P_v)` over the simplex. For the quasi-arithmetic (Rényi/Amari) family this is the closed-form generalized mean `P* ∝ (Σ_v w_v P_v^{α})^{1/α}` (escort/power-mean), renormalized — a few lines, no autograd. For the dual Bregman/α form, a Weiszfeld-style fixed-point with simplex projection. α and weights fixed a priori (α read off panel dispersion).
**(b) No-op reduction**: α→1 ⇒ arithmetic mean = **`mean_panel`**; α→0 ⇒ geometric mean = log-linear pool (= batch-1 Idea 6 as a *single point* of this family); α→−∞ ⇒ mode-seeking. So the operator strictly generalizes both existing baselines.
**(c) Theorem it could carry**: α-centroid is the unique minimizer of the average α-divergence (Amari/Nielsen); a **pluralism-preservation bound** — entropy H(P*) is monotone non-decreasing in α, giving a provable spread-vs-α curve (the anti-collapse certificate the project wants, dual to DISCA's contraction).
**(d) Metric family**: **distribution-match first** (α>0 mass-covering keeps spread for DICES/GOQA/VITAL/Scruples) + accuracy (α→−∞ recovers a sharp mode for NormAd) — one operator spanning both families via α.

**Source inspirations**:
- Primary (in-field): "Ensemble Learning for Heterogeneous LLMs with Deep Parallel Collaboration" (DeePEn — distribution fusion in a relative space), 2024 [arXiv:2404.12715].
- Primary (math): Nielsen, "Generalizing the Alpha-Divergences and the Oriented KL Divergences with Quasi-Arithmetic Means", MDPI Algorithms 15(11):435, 2022.
- Supporting: "Dually flat structure with escort probability … α-Voronoi diagrams", 2010 [arXiv:1010.4965].

**Why expected to improve**: the median collapses spread because it is one fixed point on the mean↔mode axis; the α-family makes that axis a tunable knob. DeePEn shows LLM next-token distributions fuse better in a transformed (relative) geometry than by naive prob-space averaging — the α-geometry is exactly such a transform with a closed-form solver.
**Expected gain**: distribution-match +1.0/+2.0/+3.5 (rel. JSD %); NormAd acc ±0.5. 🟡
**Feasibility**: 4/5 🟢 **Effort**: M 🟡 **Novelty**: NOVEL (continuous α-centroid as a panel-fusion op; subsumes batch-1 log-pool).

**Implementation sketch**: add `alpha_centroid(P_views, alpha)` (power-mean closed form + renorm); α=1 asserts byte-equality to `mean_panel` (no-op guard); sweep α∈{−4,−1,0,0.5,1} a priori; report JSD + H(P*) vs α on all 5 benches.
**Risks**: α>1 loses joint convexity (Rényi-VI literature [arXiv:1602.02311]) → restrict the *robust* solve to α∈(0,1] for a convex objective; α≤0 handled by the closed-form mean (no optimization). Near-zero P_v need an ε floor (power with negative α).
**Falsification test**: if no α∈{−4,−1,0,0.5} simultaneously (a) keeps NormAd-rot acc within 0.3pp of `panel_med` and (b) beats it on ≥2 distribution benches by ≥0.004 base-2 JSD, the α-axis buys nothing over the two existing operators — drop.

---

### Idea 2: Maximum-entropy moment-matching (I-projection) barycenter
- **Paradigm**: Information projection (Jaynes MaxEnt / min-cross-entropy I-projection, moment-matching).
- **Pattern**: P2 (Transfer: statistical physics / info theory → fusion). **Tier**: 3. **Scope**: enhance-existing.
- **One-liner**: Set P* to the **maximum-entropy** distribution whose answer-token moments equal the panel's consensus moments (mean, optionally variance) — anti-collapse *by construction*: among all distributions consistent with what the agents agree on, pick the least-committal (flattest) one, so spread is preserved rather than crushed.

**(a) Objective + solver**: `max_P H(P) s.t. E_P[φ_j] = (1/K)Σ_v E_{P_v}[φ_j]` for chosen statistics φ (label indicators ⇒ match the mean; pairwise products ⇒ match co-occurrence/variance). Solution is the exponential-family `P* ∝ exp(Σ_j λ_j φ_j)`; solve the few Lagrange multipliers λ by convex Newton/Newton-Raphson on the simplex (m−1 dims, trivial). Equivalent to the I-projection of the uniform onto the moment-constraint set.
**(b) No-op reduction**: match only the first moment (mean of label indicators) with no other constraint ⇒ P* = panel mean = **`mean_panel`**. Adding the variance moment is the only departure → controlled, single extra constraint.
**(c) Theorem it could carry**: Shore–Johnson axiomatic uniqueness — MaxEnt/min-cross-entropy is the *only* consistent inference rule satisfying system-independence & subset-independence; gives a "least-committal consensus" guarantee and an explicit lower bound H(P*) ≥ H of any moment-matching distribution (never under-disperses below the consensus moments).
**(d) Metric family**: **distribution-match** (designed to preserve spread → DICES/GOQA/VITAL/Scruples) ; accuracy neutral-to-positive (argmax tracks the matched mean).

**Source inspirations**:
- Primary: Shore & Johnson, "Axiomatic Derivation of the Principle of Maximum Entropy and the Principle of Minimum Cross-Entropy", IEEE T-IT 26(1), 1980.
- Supporting: "On the existence and characterization of the maxent distribution under general moment(-inequality) constraints", 2005 [arXiv:cs/0506013].

**Why expected to improve**: the four distribution benches penalize over-sharp P*; MaxEnt is the canonical operator that injects exactly zero information beyond the agreed moments, so it cannot manufacture false confidence the way a median does. It is the principled opposite of DISCA's variance contraction.
**Expected gain**: distribution-match +0.8/+1.8/+3.0 (rel. JSD %). 🟡
**Feasibility**: 4/5 🟢 **Effort**: M 🟡 **Novelty**: NOVEL (MaxEnt moment-matching as a panel-fusion op).

**Implementation sketch**: `maxent_match(P_views, moments={'mean'} or {'mean','var'})`; mean-only asserts equality to `mean_panel` (no-op guard); Newton solve for λ; report JSD + entropy on the 4 distribution benches.
**Risks**: with only label-indicator moments on a 2–3 label space, MaxEnt-mean ≈ mean (small benches) → the win comes from the variance/co-occurrence moment; if that moment is noisy, P* over-flattens (falsifiable). Constraint set can be infeasible if a view is degenerate → ε floor.
**Falsification test**: on DICES-350, if MaxEnt with the variance moment does not reduce mean base-2 JSD by ≥0.005 over `mean_panel`, moment-matching adds no spread information — drop.

---

### Idea 3: Beta-recalibrated linear opinion pool (flexible dispersion)
- **Paradigm**: Probabilistic opinion pooling (linear pool + nonlinear recalibration).
- **Pattern**: P1 (Combine: linear pool ⊕ beta recalibration). **Tier**: 3. **Scope**: enhance-existing.
- **One-liner**: Take the linear pool of the views, then pass its CDF (over the **ordered** label space) through a learned-free **beta CDF transform** — Ranjan–Gneiting's BLP — which is *flexibly dispersive*: it fixes the provable under-dispersion of the mean itself, the very over-sharpness R1/R2 blames on fusion.

**(a) Objective + solver**: `P* = beta_{a,b}∘CDF( Σ_v w_v P_v )` then difference back to a pmf. The beta transform reshapes mass across ordered labels; (a,b) set a priori from the panel's dispersion-vs-target relationship (a=b=1 is the identity). Pure closed-form arithmetic; one CDF + one beta evaluation.
**(b) No-op reduction**: (a,b)=(1,1) ⇒ identity beta ⇒ P* = **`mean_panel`** exactly.
**(c) Theorem it could carry**: Ranjan–Gneiting calibration theorem — any non-trivial linear pool of calibrated forecasts is uncalibrated/under-dispersive, and the BLP is the parsimonious family that **restores calibration** (a dispersion guarantee on P*).
**(d) Metric family**: **distribution-match**, especially the **ordered-label** benches (NormAd yes/neutral/no, DICES safe/unsure/unsafe, GOQA/VITAL Likert) where the CDF transform is meaningful.

**Source inspirations**:
- Primary: Ranjan & Gneiting, "Combining Probability Forecasts", JRSS-B 72(1):71–91, 2010 (beta-transformed linear pool; "flexibly dispersive").
- Supporting: "Combining Predictive Distributions", 2011 [arXiv:1106.1638] (dispersion/coherence of pooled CDFs).

**Why expected to improve**: this is the most direct hit on the documented failure — it proves the mean is under-dispersive and gives the closed-form repair. Distinct from batch-1's two spread ideas: batch-1 Idea 5 is a single-scalar *temperature* rescale (argmax-invariant); batch-1 Idea 6 is a *log*-pool that **sharpens**. BLP is the opposite — it *disperses*, can move mass asymmetrically across ordered labels, and is a fusion operator.
**Expected gain**: distribution-match +1.0/+2.2/+3.5 (rel. JSD %). 🟢
**Feasibility**: 5/5 🟢 **Effort**: S 🟢 **Novelty**: NOVEL (BLP as an LLM-panel fusion op).

**Implementation sketch**: order labels per bench; `blp(P_views, a, b)` = beta-reshape of the pooled CDF; (1,1) asserts equality to `mean_panel`; one a-priori (a,b) sensitivity curve; report base-2 JSD on the 4 distribution benches.
**Risks**: needs an ordered label space — degenerate on unordered/binary (falls back to `mean_panel`). (a,b) chosen off-eval-set: derive from panel dispersion quantiles, never from the metric.
**Falsification test**: on GlobalOpinionQA (ordered Likert), if no a-priori (a,b) on a fixed curve improves 1−JSdist by ≥0.005 over `mean_panel`, dispersion recalibration is inert — drop.

---

### Idea 4: Distributionally-robust minimax barycenter over a φ-divergence ball
- **Paradigm**: Distributionally-robust optimization (φ-divergence / Wasserstein ambiguity ball).
- **Pattern**: P2 (Transfer: operations research → fusion). **Tier**: 2. **Scope**: enhance-existing.
- **One-liner**: Treat the panel as defining an **ambiguity set** of plausible human distributions and output the minimax-robust center `P* = argmin_P sup_{Q∈ball(panel)} D(P, Q)` — a fused distribution that is *certified* against the worst plausible framing, carrying the bounded-influence theorem the project wants.

**(a) Objective + solver**: `min_P max_{Q: D_φ(Q, P̄)≤ρ} ℓ(P,Q)` where P̄ = panel mean and ρ from panel dispersion. By DRO duality the inner sup collapses to a convex regularized objective (Wasserstein-DRO ↔ norm penalty; φ-divergence ↔ variance/χ² penalty), solved by convex optimization on the simplex. The radius ρ is the robustness knob.
**(b) No-op reduction**: ρ→0 ⇒ ambiguity set = {P̄} ⇒ P* = **`mean_panel`**; large ρ ⇒ conservative (flatter) P*. (A specific ρ + Wasserstein ground cost ≈ a robust barycenter, linking to `panel_med`.)
**(c) Theorem it could carry**: **bounded-influence / breakdown certificate** — DRO gives a worst-case regret bound `ℓ(P*) ≤ inf + O(ρ)`, i.e. P* cannot be moved arbitrarily by views inside the ball (the formal anti-manipulation guarantee for exp002's corrupted-view sweep).
**(d) Metric family**: both — robust accuracy (NormAd, exp002 robustness) **and** distribution-match (the ρ-inflated center is less over-sharp than the median).

**Source inspirations**:
- Primary: "Bridging Bayesian and Minimax MSE Estimation via Wasserstein Distributionally Robust Optimization", Math of OR, 2021 [arXiv:1911.03539].
- Supporting: "Minimax Statistical Learning with Wasserstein Distances", 2017 [arXiv:1705.07815].

**Why expected to improve**: directly furnishes exp002's robustness theorem with a *tunable* certificate rather than the median's fixed breakdown 0.5, and the radius-inflated center keeps more spread than a point median.
**Expected gain**: robustness curve (primary) + distribution-match +0.5/+1.5/+2.5 (rel. JSD %). 🔴 (high variance; radius/solver sensitivity)
**Feasibility**: 3/5 🟡 **Effort**: L 🟡 **Novelty**: NOVEL (DRO barycenter for panel fusion + the certificate).

**Implementation sketch**: pick φ=χ² (variance-penalty dual, closed-ish) first; `dro_bary(P_views, rho)`; ρ=0 reproduces `mean_panel` (no-op guard); evaluate on exp002 corrupted-view sweep + the 4 distribution benches.
**Risks**: minimax solve + radius choice add complexity (feas 3); Wasserstein-DRO needs a ground cost (reuse ordinal cost) — entropic blur risk. Mostly a theorem vehicle; empirical gain uncertain.
**Falsification test**: on exp002, if the DRO center's `W₂(P*, P*_clean)` under k<K/2 corrupted views is not ≤ the median's at matched clean-accuracy, the certificate buys no empirical robustness — drop to theory-only appendix.

---

### Idea 5: Robust-PCA consensus / sparse-outlier decomposition of the K-view matrix
- **Paradigm**: Robust subspace / Robust PCA (low-rank + sparse).
- **Pattern**: P5 (Decompose). **Tier**: 2. **Scope**: enhance-existing.
- **One-liner**: Stack the K views as rows of a matrix and run **Principal Component Pursuit** to split it into a low-rank **consensus** `L` (the framing-invariant agreement shared across views) plus a **sparse** `S` (the biased/sycophantic outlier views); read P* off the consensus, explicitly separating legitimate agreement from framing artifacts.

**(a) Objective + solver**: `min ‖L‖_* + λ‖S‖_1 s.t. M = L + S` (M = K×m view matrix), solved by Inexact ALM / ADMM (standard, ~30 lines). P* = simplex-projected dominant consensus row of L (or its column-mean). λ = 1/√(max dim) (Candès default — *not* eval-tuned).
**(b) No-op reduction**: λ→∞ ⇒ S=0 ⇒ L=M ⇒ consensus = column-mean = **`mean_panel`**. As λ shrinks, more views are pushed into S (outliers removed).
**(c) Theorem it could carry**: PCP **exact-recovery** (Candès et al.) — L is recovered exactly even when a constant fraction of entries are arbitrarily corrupted, given incoherence ⇒ a breakdown guarantee phrased on the view matrix (complements the median's vector breakdown).
**(d) Metric family**: robustness (exp002) + accuracy; distribution-match *if* the consensus is read as a distribution (rank-1 L preserves the shared shape).

**Source inspirations**:
- Primary: Candès, Li, Ma, Wright, "Robust Principal Component Analysis?", J. ACM 58(3), 2011.
- Supporting: "Stable Principal Component Pursuit", 2010 [arXiv:1001.2363] (noisy case).

**Why expected to improve**: turns "down-weight outlier views" (what the median does implicitly) into an *explicit, certified* low-rank/sparse split, so the biased views are identified (interpretable for the paper) and the consensus shape — not a collapsed point — becomes P*.
**Expected gain**: robustness + acc +0.3/+1.0/+2.0pp; distribution-match modest. 🟡
**Feasibility**: 3/5 🟡 **Effort**: M 🟡 **Novelty**: NOVEL (RPCA on a panel-view matrix for fusion).

**Implementation sketch**: `rpca_consensus(P_views, lambda)` via IALM; λ→∞ asserts `mean_panel`; report which views land in S (sycophant detection) + metrics; cross-check S against exp002's injected corrupted views.
**Risks**: K is small (tens of views) → low-rank structure may be weak; consensus row→distribution mapping needs simplex projection (can distort). Best framed as robustness/interpretability evidence.
**Falsification test**: on exp002 with k injected corrupted views, if PCP's sparse support does not recover ≥70% of the injected views at the default λ, the decomposition is not isolating bias — drop.

---

### Idea 6: Median-of-Means block barycenter
- **Paradigm**: Robust M-estimators (median-of-means; geometric median is one point in this family).
- **Pattern**: P3 (Replace). **Tier**: 2. **Scope**: enhance-existing.
- **One-liner**: Randomly partition the K views into m blocks, **average within each block** (this keeps the block's internal spread), then take the **geometric median of the m block-means** — high-breakdown like the median but with far less spread-collapse, plus a sub-Gaussian concentration guarantee.

**(a) Objective + solver**: split K → m blocks; `B_j = mean(block_j)`; `P* = geometric_median({B_j})` via Weiszfeld + simplex projection. m fixed a priori from the expected corrupted-view fraction (e.g. m ≈ 2k+1 to tolerate k bad views). Cheap.
**(b) No-op reduction**: m=1 ⇒ one block = global mean ⇒ **`mean_panel`**; m=K ⇒ each block is one view ⇒ exactly today's **`panel_med`**. The operator *interpolates* between the two baselines by block count.
**(c) Theorem it could carry**: MoM **sub-Gaussian concentration** under heavy tails/contamination (Lugosi–Mendelson lineage) and breakdown ≈ (m−1)/2 blocks — robustness with an explicit, *tunable* spread (block means are not collapsed).
**(d) Metric family**: both — keeps NormAd-style robustness while the block-averaging retains more spread than the per-view median ⇒ helps the distribution benches where R1/R2 saw over-collapse.

**Source inspirations**:
- Primary: "Mean Estimation and Regression Under Heavy-Tailed Distributions: A Survey" (median-of-means), Found. Comp. Math. 19, 2019; + "Uniform Mean Estimation … via Median-of-Means", 2025 [arXiv:2506.14673].
- Supporting (in-field): "Revisiting Self-Consistency from a Dynamic Distributional Alignment Perspective", 2025 [arXiv:2502.19830] (the answer distribution's shape matters, not just the mode).

**Why expected to improve**: the median over-collapses because it ignores *within-group* agreement; MoM keeps it via block means and only medians *across* blocks. **Distinct from batch-1 Idea 8 (depth-trim)**: depth-trim *discards* the shallowest views; MoM *averages all views in blocks* and never throws data away — different estimator, different theorem.
**Expected gain**: distribution-match +0.6/+1.5/+2.8 (rel. JSD %); NormAd acc ±0.3. 🟡
**Feasibility**: 5/5 🟢 **Effort**: S 🟢 **Novelty**: NOVEL (MoM-block barycenter for panel fusion).

**Implementation sketch**: `mom_bary(P_views, m, seed)` (seed fixed for determinism); m=1 asserts `mean_panel`, m=K asserts `panel_med` (two no-op guards); sweep m∈{1,3,5,K} a priori; report JSD + H(P*) + NormAd acc.
**Risks**: random block assignment adds variance for small K — fix the seed and report mean over a few seeds; with K<6 the block count is coarse.
**Falsification test**: if no m∈{3,5} both (a) keeps NormAd-rot acc within 0.3pp of `panel_med` and (b) beats it on ≥2 distribution benches by ≥0.004 base-2 JSD, MoM blocks add nothing between the two endpoints — drop.

---

### Idea 7: Plackett-Luce / spectral rank-aggregation for the option-order axis
- **Paradigm**: Rank-aggregation / spectral (Plackett-Luce MLE, Luce Spectral Ranking).
- **Pattern**: P5 (Decompose: treat the order axis as a ranking problem). **Tier**: 1. **Scope**: enhance-existing.
- **One-liner**: For the option-order views, convert each view's answer distribution into a **ranking** of the labels and aggregate the K rankings with a **Plackett-Luce / spectral** estimator to recover an order-invariant consensus score → softmax to P*; this subsumes PriDe/CalibraEval order-debiasing as a special case and is intrinsically ordinal.

**(a) Objective + solver**: from each view get a label ranking (or use the soft scores); fit a single Plackett-Luce score vector θ by **Luce Spectral Ranking** (one eigenvector of a pairwise-transition matrix — closed-form, no iteration) or I-LSR MLE; `P* = softmax(θ)`.
**(b) No-op reduction**: a single canonical order with one view ⇒ θ = that view's logits ⇒ **`raw_single`**; uniform pairwise weights ⇒ score = mean rank ≈ `mean_panel` over the order axis.
**(c) Theorem it could carry**: spectral-ranking **consistency / top-K optimality** (sample-complexity guarantees) ⇒ the recovered order-invariant ranking provably removes the option-position bias PriDe targets, as a corollary of the order axis + PL fusion.
**(d) Metric family**: **accuracy** (NormAd order-debias) primarily; distribution-match via the PL choice probabilities for ordered labels.

**Source inspirations**:
- Primary (in-field): "Large Language Models Are Not Robust Multiple Choice Selectors" (PriDe), ICLR 2024 [arXiv:2309.03882]; "CalibraEval", ACL 2025 [arXiv:2410.15393].
- Supporting: "Top-K Ranking from Pairwise Comparisons: When Spectral Ranking is Optimal", 2016 [arXiv:1603.04153]; "Improved guarantee for rank aggregation via spectral method", 2023 [arXiv:2309.03808].

**Why expected to improve**: the order axis produces views that differ *only* by label position; aggregating them as rankings is the statistically correct fusion and recovers the order-invariant preference that PriDe estimates by permutation — but as a one-shot spectral solve over the existing views, no extra forwards.
**Expected gain**: NormAd acc +0.5/+1.5/+3.0pp (order-sensitive items). 🟡
**Feasibility**: 4/5 🟢 **Effort**: M 🟡 **Novelty**: EXTENDS (PL/spectral aggregation applied to the panel's order axis; PriDe is the binary-prior special case).

**Implementation sketch**: `pl_aggregate(order_views)` via LSR (eigenvector of the empirical transition matrix); single-order asserts `raw_single`; compare to `panel_med` on NormAd order conditioning.
**Risks**: PL assumes IIA (independence of irrelevant alternatives) — may not hold across personas; apply only on the order axis, fuse other axes separately. Tiny label spaces give thin rankings.
**Falsification test**: on NormAd-rot with the order axis active, if PL aggregation does not beat `panel_med` accuracy by ≥0.5pp on the order-sensitive subset, ranking adds nothing over the median there — drop.

---

### Idea 8: Friedkin-Johnsen stubborn-agent fixed-point consensus
- **Paradigm**: Fixed-point consensus dynamics (DeGroot / Friedkin-Johnsen).
- **Pattern**: P7 (Iterate to a fixed point). **Tier**: 3. **Scope**: enhance-existing.
- **One-liner**: Iterate the views as opinions on a similarity graph with a **stubbornness** term that anchors each view to its own initial distribution: `P_i ← (1−θ)P_i^0 + θ Σ_j w_ij P_j`; the fixed point P* is a consensus that, unlike DeGroot averaging, **provably retains persistent disagreement** — built-in anti-collapse.

**(a) Objective + solver**: build a row-stochastic similarity matrix W from inter-view 1−JSD; iterate the Friedkin-Johnsen update to its closed-form equilibrium `P* = (I − Θ̄W)^{-1}(I−Θ̄)P^0` (Θ̄ = diag of susceptibilities), then pool the equilibrium opinions. θ fixed a priori. One small linear solve.
**(b) No-op reduction**: θ=1 (no stubbornness) ⇒ pure DeGroot ⇒ converges to the consensus **mean** = `mean_panel`; θ=0 ⇒ no interaction ⇒ views unchanged → pool = `mean_panel` of originals. Intermediate θ gives the FJ disagreement-preserving consensus.
**(c) Theorem it could carry**: FJ **unique-equilibrium + persistent-disagreement** theorem — with stubbornness the dynamics do *not* collapse to a single point (unlike DeGroot), so a provable spread is retained at equilibrium (a pluralism-preservation result distinct from α/MaxEnt).
**(d) Metric family**: **distribution-match** (the retained disagreement matches human spread on DICES/GOQA/VITAL/Scruples).

**Source inspirations**:
- Primary: Friedkin & Johnsen, "Social influence and opinions", J. Mathematical Sociology 15(3-4):193–206, 1990.
- Supporting: DeGroot, "Reaching a Consensus", JASA 69(345):118–121, 1974 (the θ=1 collapse baseline).

**Why expected to improve**: the explicit "agents anchored to their own view" mechanism is a principled, *interaction-based* fusion that, by design, stops at a spread-preserving consensus instead of a collapsed point — and it is a genuinely different lever (graph dynamics) from every other operator here. Note: this is **internal distribution math on the K views, not debate** — no extra generations, no second model, so it stays within the single-model constraint and avoids the group-think the debate baseline (2505.24671) risks.
**Expected gain**: distribution-match +0.5/+1.3/+2.5 (rel. JSD %). 🟡
**Feasibility**: 4/5 🟢 **Effort**: M 🟡 **Novelty**: NOVEL (FJ opinion dynamics as single-model panel fusion).

**Implementation sketch**: `fj_consensus(P_views, theta, W)`; θ=1 asserts DeGroot→`mean_panel` (no-op guard); W from inter-view 1−JSD, row-normalized; sweep θ∈{0.2,0.5,0.8}; report JSD + H(P*).
**Risks**: must read as distribution math (not multi-agent *debate*) to stay single-model-compliant — state this explicitly in the paper. W and θ off-eval-set (θ from panel dispersion). Linear solve assumes (I−Θ̄W) invertible (holds for θ<1).
**Falsification test**: on DICES-990, if the FJ equilibrium pool does not reduce base-2 JSD by ≥0.005 over `mean_panel` at any θ∈{0.2,0.5,0.8}, the stubbornness term retains no useful spread — drop.

---

## Appendix — remaining paradigms surveyed, mapped, and why they are NOT indexed ideas
(The ideation lens asked to map *at least* these; each is mapped with the same (a)–(d), then triaged.)

- **Bayesian / supra-Bayesian pooling & Product-of-Experts.** (a) PoE `P*∝∏P_v^{w}` / supra-Bayes treats views as data and updates a posterior. (b) equal weights, log-space → log-linear pool. (c) external-Bayesianity (Genest-Zidek). (d) — **NOT indexed**: PoE/log-pool *multiplies* probabilities ⇒ **sharpens** (the wrong direction for the over-collapse problem), and the log-pool point is already covered by batch-1 Idea 6 and is the α→0 limit of **Idea 1**. Kept as the explicit "what makes collapse worse" baseline.

- **Optimal-transport (Wasserstein) barycenter on ordinal cost.** (a) `min_P Σ W₂(P,P_v)` on an ordinal ground cost. (b) 0/1 cost → ~mode; uniform → order-aware mean. (c) order-respecting mass preservation. (d) distribution-match on ordered labels. **NOT indexed here** — already shipped as **batch-1 Idea 9 (robust ordinal W-barycenter)**; per the lens, OT is "one option, do not center the batch on it." Idea 1 (α-centroid) and Idea 3 (BLP) give cheaper order-aware spread without Sinkhorn blur.

- **Max-consensus / RANSAC / mean-shift mode-seeking.** (a) find the largest agreeing coalition of views / the density mode; discard the rest. (b) bandwidth→∞ → mean. (c) max-consensus / breakdown. (d) **accuracy only** — mode-seeking *deliberately* collapses spread, so it is exactly wrong for the four distribution-match benches that R1/R2 flagged. **NOT indexed** (would worsen the headline failure); a candidate only for a NormAd-acc-only ablation, where batch-1 Idea 7 (dispersion-gated routing) already serves.

- **Convex feasibility / POCS.** (a) each view = a convex constraint set on the simplex; P* = projection onto the intersection (alternating projections). (b) single constraint → that view. (c) convergence of POCS to the intersection. (d) both. **NOT indexed**: for disagreeing views the intersection is typically **empty**, forcing an ad-hoc relaxation that reduces to a weighted mean (no new behavior) — low novelty/payoff versus Ideas 1–3.

- **Variational / free-energy (ELBO).** (a) `P* = argmin Σ KL(P‖P_v) + λ·(−H(P))` — a free-energy with an entropy/temperature term. (b) λ=0, KL-reverse → mean; entropy weight → MaxEnt. (c) ELBO/variational-free-energy bound. (d) distribution-match. **NOT indexed as separate** — it is the Lagrangian *dual view* of **Idea 2 (MaxEnt)** and **Idea 1 (α via Rényi-VI)**; folded into those rather than duplicated.

## Verification Report — Batch 2
| # | Title (short) | Novelty | Provenance | Feas | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|--------|------|--------|-------|
| 1 | α-divergence centroid | NOVEL ✅ | VERIFIED ✅ | 4/5 | OK ✅ | LOW (α>1 convexity flagged) | PASS | **KEEP** |
| 2 | MaxEnt I-projection | NOVEL ✅ | VERIFIED ✅ | 4/5 | OK ✅ | LOW | PASS | **KEEP** |
| 3 | Beta-recalibrated linear pool | NOVEL ✅ | VERIFIED ✅ | 5/5 | OK ✅ | LOW | PASS | **KEEP** |
| 4 | DRO minimax barycenter | NOVEL ✅ | VERIFIED ✅ | 3/5 | OK ✅ | MED (variance 🔴) | PASS | **KEEP (flag)** |
| 5 | Robust-PCA decomposition | NOVEL ✅ | VERIFIED ✅ | 3/5 | OK ✅ | MED (small K) | PASS | **KEEP** |
| 6 | Median-of-Means barycenter | NOVEL ✅ | VERIFIED ✅ | 5/5 | OK ✅ | LOW | PASS | **KEEP** |
| 7 | Plackett-Luce rank-agg | EXTENDS ✅ | VERIFIED ✅ | 4/5 | OK ✅ | LOW | PASS | **KEEP** |
| 8 | Friedkin-Johnsen fixed point | NOVEL ✅ | VERIFIED ✅ | 4/5 | OK ✅ | MED (debate-confusion) | PASS | **KEEP (warn)** |

### Counts
- Verified: 8 · Rejected: 0 · Downgraded: 1 (Idea 4 confidence → 🔴 per gain-sanity high variance) · Re-search cycles: 0 · Final batch size: 8.

### Cross-idea consistency
- **No within-batch near-duplicates**: Ideas 1/2/3/6 all touch "preserve spread" but via four distinct estimators (α-geometry centroid / entropy-max moment-match / beta-CDF recalibration / median-of-means blocks) with different no-op reductions and different theorems — mutually-alternative, compare don't stack.
- **Cross-BATCH dedup (vs batch-1)** — checked explicitly:
  - Idea 1 α-centroid **subsumes** batch-1 Idea 6 (log-pool = α→0 point) and `mean_panel` (α→1) — superset, not duplicate.
  - Idea 3 BLP is the **opposite direction** to batch-1 Idea 6 (disperses vs sharpens) and a fusion operator unlike batch-1 Idea 5's scalar temperature readout.
  - Idea 6 MoM **≠** batch-1 Idea 8 depth-trim: MoM averages all views in blocks (discards nothing); depth-trim discards shallow views. Different estimator + theorem.
  - OT barycenter and pure log-pool are deliberately left in the appendix because batch-1 already indexed them.
- **Contradiction check**: Idea 1 (can go mode-seeking at α<0) vs Ideas 2/3/8 (spread-preserving) — not a contradiction; they are alternative operators selected per metric family (the project's stated two-family strategy).
- **Score-distribution**: feas 3–5, confidence mix 🟢/🟡/🔴 — not over-confident.

## Notes & warnings
- **⚠ Tier-band deviation (surfaced, intentional)**: observed T1/T2/T3 = 25/37/37 vs configured 45/35/20; **T1 is below the 40–50% band and T3 above the 20–30% band**. This is by design: the ideation lens explicitly asked to import operators from the *full* estimation/optimization-paradigm space (information geometry, DRO, robust statistics, opinion pooling, consensus dynamics) — those primaries are genuinely cross-domain (JRSS-B, Math of OR, J.ACM, J.Math.Sociology, IEEE T-IT). The in-field T1 operators were already delivered in **batch-1** (calibration, PriDe, DoLa, reliability-weighting). Forcing more T1 here would mean mis-tagging cross-domain primaries — rejected in favor of an honest band deviation. To rebalance, re-run with `--tier-mix 25/40/35`.
- **Spread-first triage (the R1/R2 fix)**: Ideas 1, 2, 3, 6, 8 are the spread-preserving operators that directly target the median's over-collapse on DICES/GOQA/VITAL/Scruples. Ideas 4, 5 are robustness/certificate plays (exp002). Idea 7 is the accuracy/order-debias play (NormAd).
- **Single-model compliance ✅**: every operator is post-forward distribution math on the K views of the ONE frozen model — no second model, no fusion of distinct models, no generation. Idea 8 (Friedkin-Johnsen) is explicitly **distribution math on the views, not inter-agent debate**, to stay clear of both the single-model constraint and the debate baseline's group-think.
- **No-op guards everywhere**: each idea names the knob that reduces it to `mean_panel` (or `panel_med`/`raw_single`) — mandatory for the project's verify-before-deliver rule and for clean ablation.
- **Devil's-advocate (top candidate, Idea 1)**: Rényi-VI literature [arXiv:1602.02311] shows the α-divergence loses joint convexity for α>1 ⇒ restrict the robust solve to α∈(0,1] (convex); α≤0 uses the closed-form power-mean. No rank change. The beta-pool primary [Ranjan-Gneiting JRSS-B 2010] was re-confirmed in-session (under-dispersion of the linear pool is a theorem, not a heuristic).
- **Provenance honesty**: Friedkin-Johnsen (1990) and DeGroot (1974) are pre-arXiv classics cited by venue/DOI; all other primaries trace to in-session WebSearches logged in `_logs/_search_log.md` (panel-fusion batch-2 entry).

## Next steps for user
1. **Cheapest both-families probe on the existing cache**: run Idea 3 (BLP) and Idea 6 (MoM blocks) — both closed-form, both no-op-guarded — alongside batch-1 Idea 5 (temperature). All three attack the over-collapse from different angles; see which restores DICES/GOQA/VITAL/Scruples spread best.
2. **Headline operator**: implement Idea 1 (α-centroid) and sweep α; plot H(P*) and JSD vs α — this single figure tells the whole "tunable mean↔median↔mode" story and subsumes `mean_panel`, `panel_med`-like, and batch-1's log-pool in one axis.
3. **Theorem for the paper**: Idea 4 (DRO certificate) and Idea 5 (RPCA exact-recovery) feed exp002's robustness section; Idea 8 (FJ persistent-disagreement) and Idea 1 (entropy-monotone-in-α) feed the pluralism-preservation claim.
4. Hold Idea 7 (PL rank-agg) for the NormAd order-conditioning ablation (which axis carries the order-debias win).
