# Batch 4 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-4.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~35 min

## Verdicts table

| # | Title | Pattern | Tier | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|------|---------|------------|-------------------|
| 1 | SAM / Friendly-SAM optimizer wrap | P3 | 1 | ✅ **FULL SEND** | 🟢 | Stage 6: SWA baseline arm added |
| 3 | Layer-wise SIGReg (deep supervision) | P5 | 2 | 🧪 **TOY** | 🟡 | Stage 6 UNREBUTTED: probe-alignment cheap pre-flight check mandatory |
| 4 | Antithetic + spherical-harmonics CV | P2 | 3 | 🧪 **TOY** | 🟡 | Stage 6: sequencing dependency on SRHT |
| 6 | MAE pixel-recon auxiliary head | P1 | 1 | 🧪 **TOY** | 🟡 | Stage 6: matched-compute control + α=0 mechanism check |
| 2 | W-MSE Cholesky whitening pre-step | P5 | 1 | 🔁 **REFRAME** | 🟡 | Stage 4 UNREBUTTED: redundancy with SIGReg's covariance pull |
| 5 | Repulsive MC slice sampling | P3 | 3 | 🔁 **REFRAME** | 🟡 | Stage 3 FAIL: experimental-economy — dominated by SRHT (batch-3) |

## Survival statistics
- KILLED: 0/6 (0 %)
- REFRAMED: 2/6 (33 %)
- TOY: 3/6 (50 %)
- FULL SEND: 1/6 (17 %)
- **survival_rate = (FULL + TOY) / N = 4/6 = 67 %**

**Calibration**: 67 % is *inside* the healthy 30–80 % band — calibration-conscious downward adjustment vs batch-3's 83 % worked. Two REFRAMEs (Ideas 2, 5) reflect the spot-audit discipline noted in batch-3 vetting: theoretical redundancy (Idea 2) and experimental-economy collision (Idea 5) were caught instead of waved through to TOY. Single FULL SEND (Idea 1) is the mature, well-evidenced one.

## Top-3 across distinct axes

### 🥇 Top FULL SEND
**Idea 1: SAM / Friendly-SAM optimizer wrap** 🟢
- composite × confidence: 2.8 × 1.0 = 2.8
- Drop-in optimizer change; published evidence for *linear-probe* improvement (arXiv:2405.20439); matched-WC falsification built in. Refinement: include SWA-AdamW baseline arm (Stage 6 catch) — without it the comparison is incomplete.
- Cost: ~45 GPU-h (4 arms × 3 seeds × 100 ep at fixed ASHA-best HP).

### ⚡ Fastest to validate (lowest `toy_cost`)
**Idea 3: Layer-wise SIGReg — Phase A** — *zero* GPU-h.
- Phase A is a free pre-flight check on an existing baseline checkpoint: measure `probe(last) vs probe(concat-last-2)` gap. If gap < 0.3 pp, the entire idea is killed at zero cost (probe-alignment premise is wrong). If gap ≥ 0.3 pp, Phase B fires at 15 GPU-h.
- Mandatory before any of the other TOYs from batches 3+4 — costs nothing and de-risks the whole layer-wise direction.

### 🎯 Highest expected value (`gain_mid × P(survive)`)
**Idea 6: MAE pixel-recon auxiliary head** — gain mid +1.0 pp × P(survive) ~0.45 → ~0.45 pp expected. But: highest *upside* (+2.5 pp at 90th percentile) of any TOY in cumulative queues. Composite × confidence = 1.9 × 0.7 = 1.33. The matched-compute control is steep; the α=0 ablation is the cheap mechanism check that decides whether to commit. **Only fire after batch-3 TOYs settle** — most expensive TOY in cumulative queue at ~75 GPU-h + ~2 days eng.

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 2 | W-MSE Cholesky whitening pre-step | **3-arm theory ablation required first**: (i) SIGReg-only, (ii) W-MSE-only (no SIGReg), (iii) W-MSE + SIGReg. Proposed arm (iii) must beat **both singletons** by ≥ 0.4 pp non-overlap. If only beats one, the gain is from that singleton — switch to it, abandon the combo. Additionally include a *high-M SIGReg* control (M=4096) to rule out "more slices would have given the same lift". Reframed cost: 4 arms × 3 seeds × 100 ep ≈ 60 GPU-h. |
| 5 | Repulsive MC slice sampling | **Reframe as SRHT-contingency**: do not allocate an experiment slot pre-emptively. If SRHT (batch-3 FULL SEND) achieves ≥ 20 % variance reduction → archive this idea (SRHT dominates). If < 10 % → fire repulsion as the fallback. If 10-20 % → 3-arm head-to-head at TOY priority 5 (below all other survivors). **Do not run before SRHT numbers are in.** |

## Toy queue (cost-ascending, batch-4 additions only)

| Priority | # | Title | Toy cost | Decision rule | Dependency |
|----------|---|-------|----------|---------------|-----------|
| 1 | 3-A | Layer-wise SIGReg **Phase A** (probe-alignment check) | 0 GPU-h | gap(probe-concat-2, probe-last) ≥ 0.3 pp → Phase B fires; else KILL idea | Needs *any* baseline LeJEPA checkpoint (current or ASHA-best) |
| 2 | 4-A | Antithetic+CV **Phase A** synthetic-variance sanity | 0 GPU-h (CPU) | At M=256, d=384, synthetic Z: variance ratio (vanilla / antithetic+CV) ≥ 1.5 → Phase B fires; else KILL | None |
| 3 | 3-B | Layer-wise SIGReg **Phase B** | 15 GPU-h | ≥ 0.5 pp non-overlap vs baseline AND last-2-layer probe gap widens | Phase A pass |
| 4 | 4-B | Antithetic+CV on ImageNet-10 | 45 GPU-h | SIGReg-loss running-std ≥ 25 % lower vs SRHT-alone (linear-probe parity ±0.3 pp acceptable) | Phase A pass AND SRHT (batch-3 Idea 2) shipped |
| 5 | 6 | MAE pixel-recon auxiliary head | 75 GPU-h + 2 days eng | Best α arm beats matched-WC LeJEPA-only by ≥ 0.6 pp non-overlap → FULL SEND; beats equal-epoch but loses to matched-WC → KILL ("compute won"); loses to equal-epoch → KILL outright | After batch-3 TOYs (Hermite, rank-curriculum, co-distillation) settle |

Full toy designs in `idea-3-vetting.md`, `idea-4-vetting.md`, `idea-6-vetting.md`.

## FULL SEND queue (batch-4 additions only)

| Priority | # | Title | Composite | Confidence | Status |
|----------|---|-------|-----------|------------|--------|
| 1 | 1 | SAM / Friendly-SAM optimizer wrap | 2.8 | 🟢 | Ship as 4-arm ASHA extension (baseline AdamW × 100, baseline × 130, SWA-AdamW × 100, FSAM-AdamW × 100); add `optimizer` as a 3rd ASHA axis if Step-0 ASHA hasn't run yet |

## Recommended user action

**Step 0 (still queued from batch-2)**: Run batch-2 Idea 5 ASHA λ/lr/wd sweep. Unchanged gate. *Add `optimizer ∈ {adamw, swa_adamw, fsam_adamw}` as the 4th ASHA axis* per batch-4 Idea 1 → folds Idea 1 into the same sweep with no extra orchestration.

**Step 1 (this week, free)**: Run **Idea 3 Phase A** — `probe(last)` vs `probe(concat-last-2)` on the *currently-running* baseline checkpoint. Zero compute. If gap < 0.3 pp, archive layer-wise SIGReg (Idea 3) and batch-3's similar probe-alignment-adjacent ideas. If gap ≥ 0.3 pp, Phase B enters the TOY queue at priority 3.

**Step 2 (this week, free, CPU)**: Run **Idea 4 Phase A** — synthetic-data variance-reduction sanity for Antithetic+CV. Decides whether Idea 4-B enters the queue.

**Step 3 (after Step 0 returns ASHA-best HP + batch-3 Idea 2 SRHT lands)**: 
- Fire **Idea 2 reframed 3-arm theory ablation** (W-MSE redundancy check). Cost ~60 GPU-h.
- Fire batch-3 Idea 2 (SRHT) — already on its queue.
- **Defer Idea 4-B until SRHT numbers are in** (composability gate).

**Step 4 (after Step 3 lands)**: 
- If SRHT achieves ≥ 20 % variance reduction → archive Idea 5 (repulsion).
- If 10-20 % → 3-arm head-to-head (SRHT / repulsion / Antithetic+CV) at TOY priority 5.
- If < 10 % → fire repulsion as fallback.

**Step 5 (last; only after Step 3 + batch-3 TOY queue empties)**: **Idea 6 (MAE)** — most expensive TOY in the cumulative queue; commit only when the cheaper / faster ideas have settled and the absolute baseline is well-measured.

**Step 6 (cross-skill feedback for next ideation batch)**: cumulative pattern coverage P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12 (unchanged). **Batch-3 vetting's `--compose-mode` recommendation is now sharper** — the surviving FULL SEND queue is concrete (PIT monitor + SRHT + SAM + ASHA), and the natural next ideation invocation should formally enumerate compose-combinations across these four, not propose new patterns.

## Notes & warnings

- ⚠️ **Survival 67 % vs prior 83 %** — calibration improved into the healthy band; the spot-audit discipline (Ideas 2, 5 REFRAMEd instead of TOYed) is the source. Watch that batch-5 doesn't over-correct downward.
- ⚠️ **Two REFRAMEs flag distinct skill-drift symptoms**:
  - Idea 2 (W-MSE) — *theoretical* redundancy with an in-pipeline component (SIGReg already enforces covariance) was missed by ideation. Ideation should add a "redundancy-with-existing-pipeline" pre-check, especially in `enhance-existing` scope.
  - Idea 5 (Repulsive MC) — *experimental-economy* collision with batch-3 idea (SRHT) was missed by ideation. Ideation should track variance-reduction *family* coverage across batches, not just patterns.
- 🟢 **Idea 1 (SAM) is the cleanest FULL SEND of any batch** — orthogonal mechanism to all prior survivors, drop-in cost, published evidence on the exact eval metric (linear probe). Confidence 🟢.
- 🟢 **Idea 3 Phase A is the cheapest TOY ever surfaced (0 GPU-h)** — it's a *measurement on existing artifacts*. Should be done immediately regardless of other priorities; it de-risks the entire layer-wise-SIGReg / probe-alignment family.
- ⚠️ **Idea 6 (MAE) carries the only L-effort label** and the largest matched-compute control bar. If batch-3 TOYs are still in flight when Step 5 arrives, defer Idea 6 to a future cycle rather than running short of compute.
- ⚠️ **Pattern coverage and "compose-mode" recommendation**: batch-4 added no new patterns (still 9/12); the survivors (PIT, SRHT, SAM, ASHA) are now a *coherent stack*. Strong signal to switch to `--compose-mode` for batch-5 rather than expanding patterns further. Re-stating batch-3 vetting's recommendation, now with concrete targets.
- **Stage-2 search-tool note**: WebSearch for "SAM self-supervised pretraining negative result" returned mostly Segment-Anything (SAM) results due to namespace collision. Manual literature check did not surface a published SAM-the-optimizer SSL failure case; absence-of-evidence is not strong, but the search confirmed no obvious kill. Flag for batch-5 ideation: prefer "sharpness-aware minimization" full phrasing in searches.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-4
