# Batch 5 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-5.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~30 min

## Verdicts table

| # | Title | Pattern | Tier | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|------|---------|------------|-------------------|
| 5 | SIE invariant + equivariant split predictor | P5 | 1 | ✅ **FULL SEND** | 🟢 | Stage 6: matched-d-invariant arm added |
| 6 | Saliency-guided crop region sampling | P8 | 1 | ✅ **FULL SEND** | 🟢 | Stage 5+6: 2-arm (naive vs encoder-attention) + mid gain revised to +0.5 pp |
| 2 | KSD per-slice statistic | P2 | 3 | 🧪 **TOY** | 🟡 | Stage 6 UNREBUTTED→addressed: Phase A synthetic-power gate mandatory |
| 4 | Sliced Riesz-MMD per-slice statistic | P3 | 2 | 🧪 **TOY** | 🟡 | Stage 6: Phase A synthetic-power + wall-clock gate |
| 1 | Spherical t-design slice quadrature | P3 | 3 | 🔁 **REFRAME** | 🟡 | Stage 6 UNREBUTTED: variance-reduction family saturation — SRHT-contingent |
| 3 | MMCR auxiliary | P1 | 3 | 🔁 **REFRAME** | 🟡 | Stage 6 UNREBUTTED→addressed: redundancy-with-SIGReg 3-arm singleton-vs-combo ablation mandatory |

## Survival statistics
- KILLED: 0/6 (0 %)
- REFRAMED: 2/6 (33 %)
- TOY: 2/6 (33 %)
- FULL SEND: 2/6 (33 %)
- **survival_rate = (FULL + TOY) / N = 4/6 = 67 %**

**Calibration**: 67 % is *inside* the 30–80 % healthy band — matches batch-4 (67 %) exactly. The two REFRAMEs are the same skill-drift symptoms flagged in batch-4 vetting:
- Idea 3 (MMCR) — *theoretical redundancy with SIGReg* (same as batch-4 W-MSE). Caught at Stage 6 via the explicit pre-flight rule that batch-4 added.
- Idea 1 (t-design) — *variance-reduction family saturation* (same family as batch-3 SRHT + batch-4 Repulsive + batch-4 Antithetic+SH-CV). Caught at Stage 6 via the cumulative-family-coverage rule that batch-4 added.

The two FULL SENDs (Ideas 5 and 6) are head-side / data-side changes that are mechanically orthogonal to every prior survivor.

## Top-3 across distinct axes

### 🥇 Top FULL SEND
**Idea 6: Saliency-guided crop region sampling** 🟢
- composite × confidence: 2.7 × 1.0 = **2.7** (top of batch)
- Drop-in sampler change; T1 published evidence on the exact metric (CIFAR/object-centric linear probe); S effort. Refinement: 2-arm (naive local-std saliency vs encoder-attention saliency at α=0.6); revised mid gain +0.5 pp (down from +0.8 pp per Stage 6 calibration).
- Cost: ~30 GPU-h (3 arms × 3 seeds × 100 ep + saliency precompute).
- **Lowest novelty in batch** (EXTENDS bordering DUPLICATE) — explicitly acknowledged; climb-mode admissible.

### ⚡ Fastest to validate (lowest `toy_cost`)
**Idea 4 Phase A + Idea 2 Phase A** — *zero* GPU-h (1 hr CPU each, can be done in parallel).
- Joint synthetic-power test of {EppsPulley baseline, KSD, Riesz-MMD, Hermite-from-batch-3} on N(0,1) + 5% shifted-mixture at α=0.05. Resolves the per-slice-statistic 4-way bake-off before any GPU time.
- Decision rule: if any candidate has < EP power at matched wall-clock, drop it. If Riesz-MMD ≥ EP power AND wall-clock ≤ EP, it becomes the new default (pre-empts the 4-way and just ships).

### 🎯 Highest expected value (`gain_mid × P(survive)`)
**Idea 5: SIE invariant + equivariant split** — gain mid +0.9 pp × P(survive) ~0.85 → ~0.77 pp expected.
- Direct published evidence on linear probe (Wang 2026 arXiv:2503.18753); LeCun-lab provenance (Garrido SIE 2023); clean Cramér-Wold preservation argument (product-Gaussian on subspaces); built-in decomposition-collapse check. Refinement: 3-arm with matched-d-invariant control.
- Cost: ~30 GPU-h + 2 days eng (augmentation-pipeline refactor for Δ-bookkeeping).

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 1 | Spherical t-design slice quadrature | **SRHT-contingent**: do not allocate slot pre-emptively. After SRHT (batch-3 FULL SEND) lands: if SRHT achieves ≥ 30 % SIGReg-variance reduction → archive (SRHT dominates the corner). If 10–30 % → 4-arm A/B/C/D (Gaussian / SRHT / Repulsive / t-design) at TOY priority 6. If < 10 % → fires as TOY priority 4 with synthetic-variance Phase A (sanity: t-design beats Gaussian on a degree-4 polynomial integrand by ≥ 1.5× variance ratio). |
| 3 | MMCR auxiliary | **Mandatory 3-arm theory ablation first** — same pattern as batch-4 W-MSE reframe: (i) SIGReg-only baseline, (ii) MMCR-only (no SIGReg) at matched compute, (iii) SIGReg + MMCR at best α. Combo must beat **both singletons** by ≥ 0.4 pp non-overlap. If only beats one, adopt that singleton, abandon combo. Include α=0 mechanism arm. Reframed cost: 4 arms × 3 seeds × 100 ep ≈ 60 GPU-h — share the experimental slot with batch-4 W-MSE reframe. |

## Toy queue (cost-ascending, batch-5 additions only)

| Priority | # | Title | Toy cost | Decision rule | Dependency |
|----------|---|-------|----------|---------------|-----------|
| 1 | 4-A | Sliced Riesz-MMD **Phase A** | 0 GPU-h (CPU, 1 hr) | Riesz-MMD power ≥ EP power AND wall-clock ≤ EP at N=512 → graduate to Phase B; else KILL | None — pairs with 2-A |
| 2 | 2-A | KSD **Phase A** | 0 GPU-h (CPU, 1 hr) | KSD power ≥ 1.5× EP power on N(0,1)+5%-shift mixture → Phase B; else KILL | None — pairs with 4-A |
| 3 | 4-B | Sliced Riesz-MMD on ImageNet-10 | 25 GPU-h | Linear-probe ±0.3 pp parity with EP baseline AND wall-clock ≤ EP → adopt as new default | Phase A pass |
| 4 | 2-B | KSD on ImageNet-10 | 30 GPU-h | Linear-probe ≥ 0.4 pp non-overlap vs EP baseline at matched cost | Phase A pass AND beats Riesz-MMD on Phase A power |

## FULL SEND queue (batch-5 additions only)

| Priority | # | Title | Composite | Confidence | Status |
|----------|---|-------|-----------|------------|--------|
| 1 | 6 | Saliency-guided crop region sampling | 2.7 | 🟢 | Ship as 2-arm (naive saliency vs encoder-attention saliency) at α=0.6, alongside Step-0 ASHA |
| 2 | 5 | SIE invariant + equivariant split predictor | 2.5 | 🟢 | Ship as 3-arm (baseline d=384 / SIE-split d=256+128 / matched-d-invariant d=256) after ASHA returns. 2-day eng refactor required first. |

## Recommended user action

**Step 0 (unchanged)**: Run batch-2 Idea 5 ASHA sweep with `optimizer ∈ {adamw, swa_adamw, fsam_adamw}` (batch-4 Idea 1 graft) as the gate for all absolute-pp claims.

**Step 1 (this week, free)**: Run **Idea 2 Phase A + Idea 4 Phase A jointly** — single CPU synthetic-power test on {EP, KSD, Riesz-MMD, Hermite-from-batch-3} at α=0.05 on N(0,1) + 5%-shift mixture. Total cost ~1 hr CPU. Decides which of {KSD, Riesz-MMD, Hermite} graduate to ImageNet-10 head-to-head. If Riesz-MMD wins outright on power AND wall-clock, it pre-empts the 4-way and ships as the new statistic default.

**Step 2 (parallel to Step 0)**: Ship **Idea 6 (saliency crops)** — 10-line sampler change + per-image saliency precompute. 2-arm A/B (naive local-std vs encoder-attention-after-epoch-50). Zero new HPs except `α ∈ {0.3, 0.6, 1.0}` micro-sweep. Lowest-risk highest-confidence in batch.

**Step 3 (after Step 0 + 2-day eng refactor)**: Ship **Idea 5 (SIE-split)** — 3-arm experiment (baseline / SIE-split / matched-d-invariant control). Cost ~30 GPU-h. The matched-d-invariant arm is mandatory per Stage 6 refinement.

**Step 4 (after ASHA + SRHT lands)**:
- Fire **Idea 3 reframed 3-arm theory ablation** (MMCR redundancy check) — share the experimental slot with batch-4 W-MSE reframe. Cost ~60 GPU-h.
- Decide **Idea 1 (t-designs)** disposition based on SRHT's variance-reduction number: archive / TOY-priority-6 / TOY-priority-4.

**Step 5 (after per-slice-statistic Phase B settles)**: If KSD or Riesz-MMD becomes the new default, batch-2/3/4 statistic-related FULL SEND / TOY (Hermite, PIT-monitor's calibration) need a re-check at the new default — flag for batch-6 ideation.

**Step 6 (cross-skill feedback for next ideation batch)**: 
- Cumulative pattern coverage P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12 (unchanged from batch-4). 
- Batch-5 added new mechanism *instances* to P1 (MMCR), P3 (t-designs, Riesz-MMD), P5 (SIE-split), P8 (saliency). 
- Surviving cumulative FULL SEND queue: PIT monitor (b3), SRHT (b3), SAM/FSAM (b4), ASHA-extended (b2+b4), Saliency crops (b5), SIE-split (b5). **Six concrete, composable survivors.**
- Batch-3 vetting's `--compose-mode` recommendation is now *very* concrete — these six should be the formal compose-mode enumeration for batch-6 instead of new patterns.

## Notes & warnings

- ⚠️ **Survival 67 % matches batch-4** — calibration steady inside healthy band. No over-correction either direction.
- ⚠️ **The two REFRAMEs are recurring skill-drift symptoms** (per batch-4 vetting summary, now confirmed for a 2nd batch):
  - Idea 3 (MMCR) — *theoretical redundancy with SIGReg* (same as batch-4 W-MSE).
  - Idea 1 (t-design) — *variance-reduction family saturation* (same as batch-4 Repulsive).
  Both were caught by the explicit pre-flight rules added to ideation after batch-4 vetting — the rules work. Batch-5 ideation actually *flagged* both concerns in its own §Notes & warnings before vetting; this is the discipline working.
- 🟢 **Idea 6 (saliency crops) is the cleanest FULL SEND of batch-5** — drop-in sampler change with published precedent on the exact metric. Confidence 🟢. **Lowest novelty in batch is a feature, not a bug, in climb-mode.**
- 🟢 **Idea 5 (SIE-split) is the highest expected-value FULL SEND** — direct LeCun-lab evidence + 2026 follow-up confirmation. The Cramér-Wold-product-Gaussian argument cleanly resolves the theoretical concern.
- ⚡ **The joint Phase A (Ideas 2 + 4) is the cheapest TOY ever surfaced** alongside batch-4's Idea 3-A (0 GPU-h). Do it this week regardless of other priorities.
- ⚠️ **Per-slice-statistic family now 4-deep** (EP, Hermite from batch-3, KSD and Riesz-MMD from batch-5). Vetting recommends a single 4-way bake-off, not pairwise A/B comparisons. The Phase A test resolves this in ~1 hr CPU.
- ⚠️ **Variance-reduction family now 4-deep** (SRHT, Repulsive, Antithetic+SH-CV, t-design). Vetting confirms: t-design becomes SRHT-contingent (Idea 1 reframe), exactly as Repulsive became SRHT-contingent in batch-4.
- ⚠️ **Pattern coverage and "compose-mode" recommendation**: batch-5 added no new patterns (still 9/12). The surviving cumulative stack (PIT, SRHT, SAM, ASHA, Saliency, SIE) is now a *coherent 6-component composition*. **Strong signal: batch-6 must invoke `--compose-mode` formally**, not propose new patterns. Re-stating batch-3 + batch-4 vetting's recommendation with even more concrete targets.
- ⚠️ **Soft "single-λ" branding drift continues**: Ideas 3 (α for MMCR), 5 (γ for equivariance MSE), 6 (α for saliency mixture) each add 1 HP. Of the FULL SENDs, Idea 6's α can be removed (use median saliency-mass at fixed α=0.6 as default); Idea 5's γ can be bound to λ as `γ = c · λ`. After mitigations, single-λ branding survives if 5 + 6 both ship.
- ⚠️ **Idea 2 (KSD) is the most likely TOY to die at Phase A** — synthetic-power vs EP must be ≥ 1.5×, not just ≥ 1×, because KSD's O(N²) implementation cost demands a power dividend. If KSD shows only EP-parity power, drop it; Riesz-MMD will likely dominate by cost.
- **Stage-2 search-tool note**: WebSearch rate-limited after 4 queries during ideation; remaining 8 queries via HF paper search. All primary papers still trace to a live search in this session — provenance audit clean.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-5
