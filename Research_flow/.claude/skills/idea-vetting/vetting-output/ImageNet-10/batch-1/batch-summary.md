# Batch 1 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-1.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~30 min

## Verdicts table

| # | Title | Pattern | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|---------|------------|-------------------|
| 6 | Multi-crop curriculum | P4 | 🧪 **TOY** | 🟢 | Seed-variance (Stage 6) |
| 3 | Register tokens | P3 | 🧪 **TOY** | 🟢 | CLS-probe insulation (Stage 6) |
| 1 | QMC slicing for SIGReg | P3 | 🔁 **REFRAME** | 🟢 | Reframe to compute-saving |
| 4 | Adaptive λ verifier | P6 | 🔁 **REFRAME** | 🟡 | Cosine-λ baseline first |
| 2 | iBOT-style patch-SIGReg | P1 | 🔁 **REFRAME** | 🟡 | Run vanilla DINOv2 first |
| 5 | Kernelize SIGReg | P2 | ☠️ **KILL** | 🟡 | Breaks Cramér-Wold + dominated by stack-univariate-tests baseline |

## Survival statistics
- KILLED: 1/6 (17%)
- REFRAMED: 3/6 (50%)
- TOY: 2/6 (33%)
- FULL SEND: 0/6 (0%)
- **survival_rate = (FULL + TOY) / N = 2/6 = 33%**

**Calibration**: 33% lands in the healthy 30–80 % band → batch is calibrated; no spot-audit triggered. The 0 FULL SENDs is honest: with no measured ImageNet-10 baseline, nothing should ship without a toy first.

## Top-3 across distinct axes

### 🥇 Top FULL SEND (composite × vetting-confidence)
*None survived to FULL SEND.* Highest-confidence TOY is **Idea 3 (Registers)** 🟢 — one-line change, run-it-tomorrow.

### ⚡ Fastest to validate (lowest `toy_cost`)
**Idea 3: Register tokens** — 4 runs × ViT-S/100ep ≈ **8 GPU-h**. Single timm kwarg; result in 1 day. If it lifts CLS-probe by ≥ 0.5 pp, keep forever; otherwise no harm.

### 🎯 Highest expected value (`gain_mid × P(survive)`)
**Idea 6: Multi-crop curriculum** — `gain_mid` 1.2 pp × P(survive) ~0.6 = 0.72 pp expected uplift. Largest single-action lift among toys.

## Killed table

| # | Title | Killing attack (stage) | Salvageable substrate |
|---|-------|------------------------|-----------------------|
| 5 | Kernel-SIGReg | Stage 4: kernelising φ(Z) breaks Cramér-Wold guarantee on Z itself, removing LeJEPA's main theoretical advantage. Stage 6: stacking two linear univariate tests (Anderson-Darling + Epps-Pulley) dominates RFF-SIGReg theoretically and computationally. | **YES** — propose the *combine-multiple-univariate-tests* idea (free, theory-preserving) as **Idea 7** in the next ideation batch. |

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 1 | QMC slicing | From "accuracy gain" → "compute saving at iso-SIGReg-variance". Halve M, reclaim ~5–10% step time → chain into Idea 6's V=14 budget. |
| 4 | Adaptive λ | First run a fixed **cosine-schedule on λ** (3 runs). Only build the controller if any schedule beats best-fixed-λ by ≥ 0.5 pp. |
| 2 | iBOT patch-SIGReg | First run **vanilla DINOv2 on ImageNet-10** (file already exists). If DINOv2 > LeJEPA, drop this idea. If LeJEPA > DINOv2, then patch-SIGReg becomes a defensible 2-week project. |

## Toy queue (cost-ascending)

| Priority | # | Title | Toy cost | Decision rule |
|----------|---|-------|----------|---------------|
| 1 | 3 | Registers | 8 GPU-h | Δ ≥ 0.5 pp + non-overlapping seeds → keep |
| 2 | 6 | Multi-crop curriculum | 12 GPU-h | V=10+curr beats V=6 by ≥ 1.0 pp at equal wall-clock → graduate to V=14 |

Full toy designs in `idea-3-vetting.md` and `idea-6-vetting.md`.

## FULL SEND queue
*Empty.* No idea cleared 0-FAIL + ≤ 2-WARN gate.

## Recommended user action

**Step 0 (prerequisite — TODAY):** Run `stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py` at 100 epochs to fix the **measured ImageNet-10 baseline**. Without it, every gain estimate is fictional. Also run `imagenet10/ijepa-vit-base.py` and `imagenet10/mae-vit-base.py` (already in-repo) for free reference points.

**Step 1 (1-2 days):** Run Toy 3 (Registers) + Toy 6 (Multi-crop curriculum) in parallel. Cheapest path to a measured Δ.

**Step 2 (this week):** Decide on the 3 REFRAMED ideas based on Step-0/1 measurements:
- If LeJEPA beats DINOv2 → consider Idea 2 reframed.
- Run the cosine-λ baseline (Idea 4 reframe).
- Apply the QMC slicing only after compute becomes the bottleneck (chained with Idea 6's V=14).

**Step 3 (next batch ideation):** Add the *combine-multiple-univariate-tests* idea (salvaged from killed Idea 5) to the next ideation call.

## Notes & warnings
- 0 FULL SEND verdicts is correct given no measured baseline exists. This is *the most important finding* of this vetting pass: the bottleneck is measurement, not ideas.
- Idea 6's "class balance" component is cosmetic on Imagenette (already class-balanced) — the ideation skill missed this. Future ideation batches should check dataset properties before listing balance as a knob.
- The next ideation batch should be invoked with `--given-vetting vetting-output/ImageNet-10/batch-1/batch-summary.md` to bias away from theory-breaking ideas (like Idea 5) and toward measurement-first phrasing.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-1
