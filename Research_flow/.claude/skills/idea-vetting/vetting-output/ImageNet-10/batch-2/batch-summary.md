# Batch 2 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-2.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~25 min

## Verdicts table

| # | Title | Pattern | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|---------|------------|-------------------|
| 5 | Multi-fidelity ASHA HP sweep | P7 | ✅ **FULL SEND** | 🟢 | None — refinements only (use kNN proxy) |
| 1 | Stacked univariate tests (EP + AD + Watson) | P1 | 🧪 **TOY** | 🟢 | Stage 6: must beat EP@M=2048 control |
| 3 | Test-strictness curriculum (Moments → EP) | P5 | 🧪 **TOY** | 🟡 | Stage 4: Moments has ∞ minimisers; Stage 6: cosine-λ control required |
| 4 | LARS / LAMB optimizer | P3 | 🔁 **REFRAME** | 🟡 | Stage 2: ViT-SSL convention is AdamW; Stage 6: gain over-claimed (UNREBUTTED) |
| 2 | Sliced-W2 statistic | P3 | 🔁 **REFRAME** | 🟡 | Stage 6: parity bar, not gain bar (UNREBUTTED); dominated-by-Idea-1 risk |
| 6 | Two-pass self-distillation | P8 | 🔁 **REFRAME** | 🟡 | Stage 6: closer to BAN than SEED; gain over-claimed (UNREBUTTED); 2nd HP |

## Survival statistics
- KILLED: 0/6 (0%)
- REFRAMED: 3/6 (50%)
- TOY: 2/6 (33%)
- FULL SEND: 1/6 (17%)
- **survival_rate = (FULL + TOY) / N = 3/6 = 50%**

**Calibration**: 50 % survival is squarely in the healthy 30–80 % band → batch is calibrated. Compared to batch-1 (33% survival, 0 FULL SEND), batch-2 produced its **first FULL SEND** — directly the measurement-first idea (ASHA) that batch-1's vetting requested. The remaining 3 REFRAMEs all share one cause: **over-claimed expected gain magnitude** without published evidence supporting the high end. Honest signal.

## Top-3 across distinct axes

### 🥇 Top FULL SEND
**Idea 5: Multi-fidelity ASHA HP sweep** 🟢
- composite × confidence: 3.2 × 1.0 = 3.2
- Produces the **measured ImageNet-10 baseline** that batch-1 step-0 was waiting for, plus a defensible λ for every later ablation.
- Mandatory refinement: use **kNN-on-batch top-1** as the ASHA promotion metric (not linear probe) — linear probe at low rungs is non-predictive of the top-rung outcome.
- Block all other batch-2 ideas on this completing first.

### ⚡ Fastest to validate (lowest `toy_cost`)
**Idea 1: Stacked univariate tests** — 4 arms × 3 seeds × 1.5 GPU-h ≈ **18 GPU-h**.
- Theory-preserving (Cramér–Wold still holds per slice).
- Zero new HP at unit weights.
- Critical: **must include EP@M=2048 as a control** to rule out "more compute" being the driver.

### 🎯 Highest expected value (`gain_mid × P(survive)`)
**Idea 5 (FULL SEND)** wins on EV too: gain_mid ≈ +1.5 pp × P(deliver) ~0.95 = ~1.4 pp expected lift on the *measured baseline*. No other idea even has a baseline to measure gain against until this lands.

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 4 | LARS / LAMB | Narrow to **LAMB only** (ViT-appropriate); down-revise gain mid to +0.3 pp; co-run AdamW-with-same-lr-sweep as control. Fold into Idea-5's ASHA as a 4th axis at marginal extra cost. |
| 2 | Sliced-W2 | Run **after** Idea 1 (stacked tests). Bar = beat best-stacked-EP by ≥ 0.5 pp linear probe **or** show ≥ 30% lower SIGReg variance. Parity = kill. |
| 6 | Two-pass self-distillation | Down-revise gain mid to +0.5 pp. Run **150-ep vanilla baseline first**. Only if 150-ep clearly beats 100-ep, do a *single* confirmation run at α=0.5 + teacher-epoch=50 — no sweep until then. Stretch: cross-architecture in-domain teacher to recover SEED's pedigree. |

## Toy queue (cost-ascending)

| Priority | # | Title | Toy cost | Decision rule |
|----------|---|-------|----------|---------------|
| 1 | 1 | Stacked univariate tests | 18 GPU-h | Arm 4 ({EP,AD,W}) beats both Arm 1 (EP-only) and Arm 2 (EP@M=2048) by ≥ 0.5 pp non-overlap CI |
| 2 | 3 | Test-strictness curriculum | 18 GPU-h | Best curriculum beats both always-EP and cosine-λ-on-EP by ≥ 0.5 pp; SIGReg(EP) at switch ≤ 2× always-EP value |

Full toy designs in `idea-1-vetting.md` and `idea-3-vetting.md`.

## FULL SEND queue

| Priority | # | Title | Composite | Confidence | Status |
|----------|---|-------|-----------|------------|--------|
| 1 | 5 | Multi-fidelity ASHA HP sweep | 3.2 | 🟢 | Ship now — gate for everything else |

## Recommended user action

**Step 0 (this week — HIGHEST priority):** Launch **Idea 5** (ASHA over λ, lr, wd; kNN promotion metric; 2 seeds at top rung). Expected wall-clock ~12 GPU-h. Output: (a) measured ImageNet-10 baseline with seed CI, (b) λ-landscape plot, (c) defensible (λ, lr, wd) tuple for everything else. **This unblocks ranking of every other idea in batch-1 and batch-2.**

**Step 1 (in parallel — cheap, orthogonal):** Once Idea-5 is launched, fire **Idea 1 toy** (stacked tests) and **batch-1 Toy 3 (Registers)** at the same time. Both are ≤ 18 GPU-h and require no ASHA output to start.

**Step 2 (after Step 0 lands):** Decide on the 3 REFRAMEs using the measured baseline:
- **Idea 4 (LAMB-only)**: add as a 4th axis to a *second* mini-ASHA at the best-λ from Step 0.
- **Idea 6 (distillation)**: run 150-ep vanilla as the actual control first (already on the path); decide based on the 100-ep vs 150-ep delta.
- **Idea 2 (W2)**: hold until Idea 1 (stacked tests) returns a result — Idea 2's bar is "beat the stacked-EP win".

**Step 3 (after Step 1 lands):** Promote toys that cleared the bar to FULL SEND; iterate. **Idea 3 (curriculum)** runs only after stacked-EP and cosine-λ-on-EP are both measured, so it has its controls.

**Step 4 (next ideation batch):** Pattern coverage across batches 1+2 is now P1, P2, P3, P4, P5, P6, P7, P8 = 8 of 12. P9 (Tool-use), P10 (Sampling), P11 (ICL) don't fit pretraining; **P12 (Self-play)** is the natural unused slot — bootstrap-style curricula or co-training students. Worth considering when the cheap ideas land.

## Notes & warnings
- 🟢 **First FULL SEND across both batches** — Idea 5 directly addresses batch-1's diagnosed "measurement is the bottleneck" finding. This is the most important result of the batch.
- ⚠️ **Three REFRAMEs share one failure mode**: over-claimed gain magnitude (Ideas 4, 6 hit UNREBUTTED on Stage 6 gain-sanity; Idea 2 was forced to a parity bar). The ideation skill should down-revise mid-gain estimates whenever the cited prior art is on a different regime (large batch / larger teacher / different backbone family). Surface this as a future ideation-skill correction.
- ⚠️ **Idea 4 framing is wrong**: "LARS or LAMB" for ViT-SSL should be "LAMB" only. The ideation skill conflated SimCLR/BYOL (CNN-era) precedent with ViT-era convention.
- ⚠️ **Idea 1's salvage worked** but vetting raised a new control (EP@M=2048) that the proposal missed. The "more statistical power" claim needs to dominate "more MC samples of the same statistic" as a separate effect.
- The next ideation batch should be invoked with `--given-vetting vetting-output/ImageNet-10/batch-2/batch-summary.md` plus the previous one so ideation sees both calibrations.
- Pattern coverage running totals: P1✓, P2✓, P3✓✓✓, P4✓, P5✓, P6✓, P7✓, P8✓ — P9, P10, P11 unsuited; P12 open.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-2
