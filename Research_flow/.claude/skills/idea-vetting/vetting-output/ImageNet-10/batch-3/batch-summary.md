# Batch 3 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-3.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~30 min

## Verdicts table

| # | Title | Pattern | Tier | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|------|---------|------------|-------------------|
| 2 | SRHT structured slices | P2 | 3 | ✅ **FULL SEND** | 🟢 | None |
| 3 | PIT-uniformity held-out monitor | P6 | 3 | ✅ **FULL SEND** | 🟢 | Stage 6: gain is contingent on ρ ≥ 0.7 |
| 1 | Co-distillation, disjoint slice subspaces | P12 | 1 | 🧪 **TOY** | 🟡 | Stage 2: BYOL-symmetric-no-EMA proximity; Stage 6: matched-compute control mandatory |
| 4 | Hermite-moment univariate test | P3 | 3 | 🧪 **TOY** | 🟡 | Stage 2 + 6: dominated by `ExtendedJarqueBera` (already in library) and by batch-2 Idea 1 (stacked tests, on toy queue) |
| 6 | Embedding-rank curriculum (k_t schedule) | P5 | 1 | 🧪 **TOY** | 🟡 | Stage 4 UNREBUTTED: middle-phase equilibrium risk (top-k_t isotropic + drift in (d−k_t)) |
| 5 | Per-rank disjoint slices in DDP | P4 | 2 | 🔁 **REFRAME** | 🟡 | Stage 1 UNREBUTTED: scope mismatch — gain = 0 at 1-GPU Imagenette; ship as code default for multi-GPU runs |

## Survival statistics
- KILLED: 0/6 (0 %)
- REFRAMED: 1/6 (17 %)
- TOY: 3/6 (50 %)
- FULL SEND: 2/6 (33 %)
- **survival_rate = (FULL + TOY) / N = 5/6 = 83 %**

**Calibration**: 83 % is *just above* the healthy 30–80 % band → spot-audit recommended. Two factors push it up: (a) the batch was tightly disciplined by prior vetting (batch-1 + batch-2 already weeded out the easy kills — Kernel-SIGReg, naive HP-sweep), (b) batch-3 leaned on Tier-3 cross-domain primaries (SRHT / PIT / Hermite) which carry clean theoretical anchors and thus survive Stage 4 cleanly. Audit conclusion: not over-permissive — Idea 5 (REFRAME) and Ideas 4 + 6 (TOY with UNREBUTTED) carry honest yellow flags, no green-rubber-stamping.

## Top-3 across distinct axes

### 🥇 Top FULL SEND
**Idea 3: PIT-uniformity held-out monitor** 🟢
- composite × confidence: 2.7 × 1.0 = 2.7
- Read-only callback → zero risk; runs in parallel with *any* other experiment in queue. Produces the ρ-vs-linear-probe correlation dataset that itself has value regardless of pp lift.
- Mandatory refinement: log ρ vs RankMe and ρ vs LiDAR in the same run — establishes relative signal quality of label-free SSL proxies, not just absolute.

### ⚡ Fastest to validate (lowest `toy_cost`)
**Idea 4: Hermite-moment test** — 12 GPU-h (4 arms × 3 seeds × 100 ep).
- Cheapest TOY in this batch.
- Critical: must include **`ExtendedJarqueBera` as the killer baseline**, not just `EppsPulley`. Without that control, "Hermite-6 beats EP" would be confounded with "JB beats EP" (which is already known).

### 🎯 Highest expected value (`gain_mid × P(survive)`)
**Idea 2: SRHT structured slices** — gain mid ~+0.6 pp × P(survive) ~0.85 → ~0.5 pp expected, but more importantly: zero-cost stability win. Composite × confidence = 2.8 × 1.0 = 2.8. The real value is **mechanism quality + reproducibility** (lower SIGReg variance), not the pp lift — frame the experiment around the variance-reduction falsification, not the linear-probe number.

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 5 | Per-rank disjoint DDP slices | **Not a research idea on ImageNet-10** — gain = 0 at the named 1-GPU setup. Ship as a small PR + unit test to `lejepa.multivariate.SlicingUnivariateTest` (remove the seed `all_reduce`, add `seed = base_seed + dist.get_rank()`). Validates the next time the recipe runs on ≥ 2 GPU (e.g., `train_eval_vit_l.py` ImageNet-1K). Do NOT spend an ImageNet-10 experiment slot on this. |

## Toy queue (cost-ascending)

| Priority | # | Title | Toy cost | Decision rule | Dependency |
|----------|---|-------|----------|---------------|-----------|
| 1 | 4 | Hermite-moment test | 12 GPU-h | Hermite-6 beats **both** EP **and** ExtendedJB by ≥ 0.5 pp non-overlap → graduate. Beats EP but not ExtendedJB → reframe as "Hermite ≡ JB" → KILL. Beats neither → KILL. | After batch-2 Idea 1 (stacked-tests toy) — informs whether Hermite-6 adds beyond stacked-tests power |
| 2 | 6 | Embedding-rank curriculum | 18 GPU-h | Best curriculum ≥ 0.5 pp at endpoint **OR** reaches baseline pp in ≤ 60 % epochs. Sanity: RankMe at end-of-curriculum ≥ baseline (no slow-drift collapse). | Needs measured baseline (batch-2 Idea 5 ASHA output) |
| 3 | 1 | Co-distillation, disjoint subspaces | 24 GPU-h | Best γ > 0 beats matched-compute 200-ep single-student by ≥ 0.5 pp non-overlap → graduate. Beats single-100ep but not single-200ep → KILL ("more compute did it"). | Needs measured baseline |

Full toy designs in `idea-1-vetting.md`, `idea-4-vetting.md`, `idea-6-vetting.md`.

## FULL SEND queue

| Priority | # | Title | Composite | Confidence | Status |
|----------|---|-------|-----------|------------|--------|
| 1 | 3 | PIT-uniformity held-out monitor | 2.7 | 🟢 | Ship now — zero-risk, parallelisable, produces correlation dataset on first use |
| 2 | 2 | SRHT structured slices | 2.8 | 🟢 | Ship after batch-2 Idea 5 (ASHA) returns (λ, lr, wd) — uses ASHA-best HP as fixed config |

## Recommended user action

**Step 0 (still queued from batch-2)**: Run batch-2 Idea 5 (ASHA λ/lr/wd sweep). Still the gate for absolute pp claims on the rest of this page. *Unchanged from batch-2 recommendation.*

**Step 1 (this week — ship in parallel with Step 0)**: **Idea 3 (PIT monitor)** — add the callback to the *currently running* ASHA arms. It piggybacks on whatever training is happening; the deliverable (per-epoch PIT-AD per arm) lands automatically when ASHA finishes. **Zero opportunity cost.**

**Step 2 (after Step 0 lands)**: **Idea 2 (SRHT)** at fixed best (λ, lr, wd) from ASHA. 3 seeds. Primary deliverable = SIGReg-loss running-std comparison vs Gaussian-slice baseline. Secondary = linear-probe parity.

**Step 3 (toy queue, parallel to FULL SENDs once baseline lands)**:
- Fire **Idea 4 (Hermite) toy** alongside batch-2 Idea 1 (stacked-tests toy). Both touch the same `UnivariateTest` slot; can share the augmentation pipeline + dataloader; one job-array of 7 arms (3 stacked-tests + 4 Hermite) at 3 seeds = effectively shared infrastructure cost.
- **Idea 6 (rank curriculum)** as a separate toy after stacked-tests result — sensitivity to total-epoch-budget makes it the riskiest TOY.
- **Idea 1 (co-distillation)** last — most expensive TOY (2× wall-clock), highest matched-compute control bar.

**Step 4 (engineering, not a research slot)**: ship **Idea 5 reframe** as a 2-line code change with unit test, on the same PR as any other multi-GPU recipe update. Do not validate on ImageNet-10 — validate on the first ≥ 2-GPU run.

**Step 5 (next ideation batch)**: pattern coverage now P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12. P9 (Tool-use), P10 (Sampling), P11 (ICL) remain structurally unsuited to in-domain SSL pretraining. **The natural next opening is not another pattern — it is *experimental composability*: which surviving ideas from batch-2 + batch-3 are *mutually compatible* and would compound when stacked**. Suggest invoking ideation in `--compose-mode` over the FULL SEND + TOY survivors (ASHA + PIT-monitor + SRHT + stacked-tests + Hermite + curriculum + co-distillation) to enumerate non-conflicting combinations.

## Notes & warnings
- 🟢 **Two FULL SENDs in one batch** — first time across batches 1/2/3. Both are Tier-3 cross-domain (SRHT from numerical linear algebra; PIT from mathematical statistics). Validates the batch-3 strategy of leaning into honest Tier-3.
- 🟢 **Zero KILLs** — ideation skill has clearly internalised the prior batches' calibration feedback (no engineering-tasks-as-ideas; no over-claimed gains; honest tier tags). Cross-skill loop is working.
- ⚠️ **Survival 83 % is just above the healthy band**. Spot-audit done — the high rate is structural (heavy prior weeding + clean Tier-3 anchors), not skill drift. Watch for next batch.
- ⚠️ **Idea 4 (Hermite) sits in the shadow of batch-2 Idea 1 (stacked tests)** — explicitly sequence them so the second is informed by the first. If stacked-tests already wins decisively, Hermite is a low-priority follow-up; if not, Hermite represents the orthogonal-basis alternative attack.
- ⚠️ **Idea 6 (rank curriculum) has the only Stage 4 UNREBUTTED** — middle-phase equilibrium risk. RankMe abort-condition in the proposal is a *partial* guard, not a guarantee. If the toy fires, watch RankMe trajectory closely during the curriculum phase.
- ⚠️ **Idea 5 REFRAME is the right call but introduces a process question**: where should "code-correctness improvements with research-justifiable mechanisms" live? They're not pure engineering (mechanism > 0), not pure research (no benchmark lift). The skill currently routes them to `not-an-idea`-adjacent REFRAME; consider a dedicated `engineering-default` verdict tag in a future skill update.
- **Idea-vetting-skill correction surfaced**: Stage 1's "idea-or-engineering gate" needs a sub-rule for **scope-mismatched ideas** (mechanism is real but doesn't fire at the named benchmark scale). Currently the gate either passes (treating it as an idea) or kills (treating it as engineering). A third route — "valid mechanism, wrong scope, ship as default" — is what Idea 5 actually deserves; the REFRAME verdict is doing that work imperfectly.
- **Pattern coverage cumulative across batches 1+2+3**: P1, P2, P3, P4, P5, P6, P7, P8, P12 — 9/12. P9, P10, P11 unsuited to pretraining setting.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-3
