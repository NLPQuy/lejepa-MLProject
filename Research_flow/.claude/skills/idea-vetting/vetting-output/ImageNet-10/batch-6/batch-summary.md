# Batch 6 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-18 · **Source**: `ideation-output/ImageNet-10/batch-6.md`
**Mode**: --climb-mode (Stage 7 reviewer simulation skipped)
**Ideas**: 6 · **Wall-clock**: ~25 min

## Verdicts table

| # | Title | Pattern | Tier | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|------|---------|------------|-------------------|
| 4 | Sinkhorn divergence invariance | P3 | 3 | 🧪 **TOY → FULL SEND** | 🟢 | Stage 6 mechanism-check DEFLECTED; Phase A is decisive at 15 GPU-h |
| 1 | RankMe-driven adaptive-λ controller | P6 | 1 | 🧪 **TOY** | 🟢 | Stage 6 WEAKENED — "does no harm" ≠ FULL SEND material; Phase A free |
| 3 | iBOT-style masked-patch SIGReg | P1 | 2 | 🧪 **TOY** | 🟡 | Stage 4 (position-correlation defeats Cramér-Wold) + Stage 6 (must beat MAE-aux head-to-head) |
| 5 | Poincaré-ball hyperbolic projector | P2 | 3 | 🧪 **TOY** | 🟡 | Stage 1 shallow-hierarchy + Stage 2 prior-art family; Phase A pre-flight free |
| 2 | Register tokens for ViT-S/16 | P3 | 1 | 🔁 **REFRAME** | 🟢 | Stage 2 SOFT-FAIL: hard duplicate with active batch-1 Idea 3 TOY (8 GPU-h, queued) |
| 6 | Persistent-homology H₀ regularizer | P1 | 3 | 🔁 **REFRAME** | 🟢 | Stage 4 FAIL (high-d concentration) + Stage 6 FAIL (gradient near-zero); near-KILL |

## Survival statistics
- KILLED: 0/6 (0 %)
- REFRAMED: 2/6 (33 %)
- TOY: 4/6 (67 %)
- FULL SEND: 0/6 (0 %) — note Idea 4 graduates to FULL SEND on Phase A pass (cheap, 15 GPU-h)
- **survival_rate = (FULL + TOY) / N = 4/6 = 67 %**

**Calibration**: 67 % matches batch-4 and batch-5 exactly — calibration steady inside the 30–80 % healthy band for the third batch in a row. The two REFRAMEs both surface *process* failures of the ideation skill, not idea failures:
- Idea 2 = ideation skill did not consult its own logs (batch-1 Idea 3 is in active TOY queue — same idea, same paper).
- Idea 6 = ideation skill missed the directly-relevant prior art (Moor 2020 / Trofimov 2023 PH-as-SSL-regularizer family) and overstated novelty. **Cross-skill feedback**: ideation skill needs a "check existing TOY queue and per-skill rejection log before drafting" pre-flight (separate from the batch-level dedup rule).

## Top-3 across distinct axes

### 🥇 Top FULL SEND (composite × confidence)
**Idea 4 Sinkhorn invariance** — graduate to FULL SEND on Phase A pass.
- composite × confidence: 2.11 × 0.9 = **1.90** (only graduation-eligible idea in batch)
- Direct published evidence on the alignment-term substitution (SinSim Feb 2025); 50/50-mix mitigation handles the OT-permutation collapse risk; per-image-cos mechanism-check is sharp.
- Cost: ~15 GPU-h (3-arm × 3 seeds × 100 ep).
- Risk: novelty narrow (one paper away from being scooped).

### ⚡ Fastest to validate (lowest toy_cost)
**Idea 1 Phase A + Idea 5 Phase A** — *zero* GPU-h (both 1 hr CPU each, run in parallel).
- Idea 1: 10-ep CIFAR-10 PI-controller dynamics sanity. Decides whether Phase B (12 GPU-h on ImageNet-10) fires.
- Idea 5: super-cluster-vs-within ratio measured on any saved baseline LeJEPA checkpoint (Euclidean). Decides whether 25-GPU-h Phase B fires.
- Idea 5 Phase A also serves as a **free pre-flight for any future hierarchy-based idea**.

### 🎯 Highest expected value (gain_mid × P(survive))
**Idea 3 iBOT-SIGReg** — mid +1.0 pp × P(survive) ~0.45 → ~0.45 pp EV.
- Highest mid-gain in batch; survival probability moderate due to two WEAKENED at Stages 2 and 4 (position-correlation Cramér-Wold concern + small-backbone scale-down). Cost ~25 GPU-h for 3-arm matched-WC head-to-head with batch-4 MAE-aux TOY — the head-to-head also resolves the batch-4 MAE-aux TOY in the same experiment (savings ~75 GPU-h on the deferred MAE-aux TOY).

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 2 | Register tokens | **Do NOT spend new compute or queue a new TOY.** Promote existing batch-1 Idea 3 TOY (8 GPU-h, `queued`) to **Priority 1** in `_toy_queue.md`. Augment its decision rule with the batch-6 artifact-tail mechanism-check. Add 2026 cross-architectural papers (arXiv:2603.25803, arXiv:2506.08010) as supporting refs. **Do NOT count this as a batch-6 idea in `_passed_ideas.md`.** |
| 6 | PH H₀ topological regularizer | **Near-KILL.** Direct PH on d=384 is broken by concentration of measure (Stage 4 FAIL) and breaks the redundancy pre-check (Stage 6 FAIL). Salvageable only as substantively different idea: (a) PH on 32-d projection — defer; (b) PH₁ (loops) instead of PH₀ — defer. **ARCHIVE the topological-regularizer direction** until a low-d-projection or PH₁ variant is proposed AND the 1-hr-CPU gradient-norm sanity test passes (compute PH₀ gradient norm on N(0, I_384); if < 1e-5 across 100 trials, KILL definitively). |

## Toy queue (cost-ascending, batch-6 additions only)

| Priority | # | Title | Toy cost | Decision rule | Dependency |
|----------|---|-------|----------|---------------|-----------|
| 1 | 1-A | RankMe controller Phase A (CIFAR-10 controller dynamics) | 0 GPU-h (CPU, 1 hr) | λ trajectory converges within 5 ep without oscillation > 30 % of mean → Phase B fires; else KILL or retune | None — run immediately |
| 2 | 5-A | Poincaré pre-flight (super-cluster ratio on saved baseline checkpoint) | 0 GPU-h (CPU, 1 hr) | Ratio ≥ 1.5 → Phase B fires; 1.3–1.5 → defer; < 1.3 → KILL idea | Needs any saved LeJEPA checkpoint |
| 3 | 4-A/B | Sinkhorn invariance 3-arm A/B/C on ImageNet-10 | 15 GPU-h | Best arm ≥ 0.4 pp non-overlap vs baseline-MSE; mixed wins → FULL SEND as new invariance default; Sinkhorn-only wins + per-image cos < 0.5 → REFRAME (OT collapse); baseline wins → KILL | ASHA Step-0 |
| 4 | 1-B | RankMe controller Phase B (3-arm ImageNet-10) | 12 GPU-h | Best controller arm matches fixed-λ-best within ±0.3 pp at total-compute ≤ fixed-λ-best → FULL SEND; matches probe but uses more compute → REFRAME (compose-mode binder); loses on probe → KILL | ASHA Step-0 + Phase A pass |
| 5 | 3-A | iBOT-SIGReg Phase A (synthetic predictor-output normality on position-correlated patches) | 0 GPU-h (CPU, 1 hr) | Predictor-output per-slice normality value approaches iid baseline within 200 SGD steps → Phase B fires; else KILL | None |
| 6 | 3-B | iBOT-SIGReg Phase B (3-arm head-to-head w/ batch-4 MAE-aux on ImageNet-10) | 25 GPU-h | Best aux arm ≥ 0.5 pp non-overlap vs baseline; iBOT ≥ MAE by ≥ 0.3 pp → graduate iBOT, KILL MAE-aux; else drop both or graduate winner | ASHA Step-0; consolidates batch-4 MAE-aux TOY (savings ~50 GPU-h on the deferred 75-GPU-h MAE-aux) |
| 7 | 5-B | Poincaré hyperbolic Phase B (2-arm Euclidean vs Poincaré) | 25 GPU-h | Hyperbolic ≥ 0.4 pp + super-cluster ratio in hyp ≥ 1.5× Euclidean → FULL SEND; else KILL | Phase A pass; ASHA Step-0 |

## FULL SEND queue (batch-6 additions only)

*Empty for now.* Idea 4 (Sinkhorn) is the most-likely batch-6 graduation candidate via its Phase A pass — re-vet on results.

## Recommended user action

**Step 0 (unchanged across batches 1-6)**: Run batch-2 Idea 5 ASHA sweep as the gate for absolute-pp claims.

**Step 1 (this week, free, parallel)**: Run **Idea 1 Phase A + Idea 5 Phase A** jointly on CPU. ~1 hr each. Both decide whether their respective Phase Bs fire. **Idea 5 Phase A also kills the whole hyperbolic direction at zero cost if Imagenette's hierarchy is too shallow** — high-value free measurement.

**Step 2 (parallel to Step 0)**: **PROMOTE batch-1 Idea 3 register-tokens TOY** (8 GPU-h, currently `queued`) to Priority 1. Add the artifact-tail mechanism-check to its decision rule. This subsumes batch-6 Idea 2 — do not double-count.

**Step 3 (after ASHA)**: **Ship Idea 4 (Sinkhorn) 3-arm A/B/C** — 15 GPU-h. The cheapest path to a FULL SEND graduation in batch-6. If mixed arm wins by ≥ 0.4 pp non-overlap, ship as new invariance default and re-vet for downstream effects on SIE-split (batch-5 FULL SEND) and saliency crops (batch-5 FULL SEND).

**Step 4 (after Idea 4 settles + Idea 1 Phase B if it fires)**: **Run Idea 3 iBOT-SIGReg Phase A** (free CPU sanity). If passes, run Phase B as a **3-arm head-to-head with batch-4 MAE-aux** at matched WC (25 GPU-h consolidates 2 TOYs into 1 experiment). Bind `λ_patch` to Idea 1's RankMe controller (if Idea 1 Phase B graduated) to avoid the extra HP.

**Step 5 (after Step 1 Phase A → Phase B gate)**: If Idea 5 Phase A passed, run Poincaré Phase B (25 GPU-h). Lowest priority in batch-6.

**Step 6 (archive)**: Idea 6 (PH) is REFRAMED out — do not allocate compute. Optionally run the 1-hr CPU gradient-norm sanity on PH₀ at d=384; if < 1e-5, KILL definitively in the next vetting log entry.

**Step 7 (cross-skill feedback to ideation)**:
- Two REFRAMEs surface *ideation process gaps*: (a) Idea 2 = the ideation skill did not check `_toy_queue.md` before drafting; (b) Idea 6 = the ideation skill missed directly-relevant prior art (Moor 2020 / Trofimov 2023). **Recommend ideation skill add a "duplicate-check against active TOY queue and prior-batch rejections" pre-flight in Step 2 or Step 3, separate from the existing batch-level dedup rule.**
- Cumulative pattern coverage unchanged: P1, P2, P3, P4, P5, P6, P7, P8, P12 = 9/12. Batch-6 invoked P1, P2, P3, P6 — no new patterns. P9/P10/P11 remain unsuited.
- **Cross-skill recommendation (4th batch in a row)**: vetting again recommends `--compose-mode` for batch-7. Surviving cumulative FULL SEND stack: PIT (b3), SRHT (b3), SAM/FSAM (b4), ASHA-step-0 (b2+b4), Saliency crops (b5), SIE-split (b5), [pending] Sinkhorn invariance (b6), [pending] RankMe-controller (b6). Up to **8 concrete composable survivors**. Strong signal: stop proposing new patterns; start enumerating compositions formally.

## Notes & warnings

- ⚠️ **Survival 67 % matches batches 4 and 5 exactly** — calibration steady in healthy band for the 3rd batch in a row. No spot-audit needed.
- ⚠️ **Both REFRAMEs are *ideation process* failures**, not idea failures:
  - **Idea 2** is a literal duplicate of a queued TOY from batch-1. The ideation skill's Step 2 should have caught this via `_toy_queue.md` lookup. **Skill-fix recommendation**: add a "duplicate-against-active-TOY-and-rejection-logs" line to `benchmark-climb-ideation/SKILL.md` Step 2 idea-drafting pre-flight, citing this case.
  - **Idea 6** missed the Moor 2020 / Trofimov 2023 PH-as-SSL-regularizer prior art. The ideation skill's Stage 2 (search) found foundational PH / differentiable-PH refs but not the directly-relevant SSL-applied prior art. **Skill-fix recommendation**: when a Tier-3 idea is being verified, require ≥ 1 search query for "<technique> SSL representation learning" in the SSL domain, not just the cross-domain root.
- 🟢 **Idea 4 (Sinkhorn) is the only graduation-eligible idea this batch** — SinSim Feb 2025 published evidence on the same mechanism + sharp 3-arm falsification.
- ⚠️ **Idea 6 (PH) was the highest-novelty idea ideation drafted, and it died at Stages 4+6** — concentration-of-measure in d=384 + missed prior art. **The 50 % Tier-3 quota produced one strong candidate (Sinkhorn), one weak candidate (Poincaré), one near-KILL (PH).** Lesson for ideation: T3 ideas at d > 100 should include a *concentration-of-measure* pre-check in the falsification test from the start.
- ⚡ **Step 1 (joint CPU Phase As) is the cheapest TOY group ever surfaced** alongside batch-5's joint Phase A (Ideas 2+4). Do this immediately regardless of other priorities. **5 GPU-h-equivalent decisions for 2 CPU-hours.**
- ⚠️ **Compose-mode recommendation now 4 batches in a row** (batch-3, batch-4, batch-5, batch-6 vettings all flagged). The cumulative survivor stack is now 6–8 concrete components. **Batch-7 should NOT propose new patterns**; it should enumerate compositions and predict the additive vs. interactive effects.
- ⚠️ **Process credit**: batch-6 ideation correctly identified that the per-slice-statistic / variance-reduction-sampler / covariance-shaping families were all closed and proposed *zero* new entries in them. That discipline is working. The two failures (Ideas 2 and 6) are different process gaps (log lookup, in-field SSL search) than the family-saturation issue.
- ⚠️ **Soft "single-λ" branding drift**: Ideas 3 (λ_patch), 4 (Sinkhorn ε), 5 (curvature c), 6 (λ_topo) each add 1 HP. **Idea 1 (RankMe controller) is the structural solution** — if it ships, all 4 can be bound to the same setpoint. **Recommend prioritizing Idea 1 Phase A this week alongside Idea 5 Phase A** so the controller is ready as a binder before the other ideas ship.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-18): vetting-batch-6
