# Batch 7 Vetting Summary — ImageNet-10 / LeJEPA SSL embedding
**Vetted**: 2026-05-19 · **Source**: `ideation-output/ImageNet-10/batch-7.md` + `batch-7-idea6-addendum.md` (quantum) + `batch-7-idea7-addendum.md` (FM-SIGReg) — addenda added per user requests mid-session
**Mode**: `--climb-mode` (Stage 7 skipped) · **Ideas**: 7 (5 original + 2 addenda) · **Wall-clock**: ~38 min

## Verdicts table

| # | Title | Pattern | Tier | Verdict | Confidence | Critical stage(s) |
|---|-------|---------|------|---------|------------|-------------------|
| 3 | Adversarial max-sliced SIGReg | P6 | 3 | 🧪 **TOY → FULL SEND** | 🟡 | Stage 4+6 WEAKENED (non-convex minimax stability) — Phase A free CPU sanity is decisive |
| 2 | Multivariate score matching (Hyvärinen+Hutchinson) | P3 | 3 | 🧪 **TOY** | 🟢 | Stage 4 convex-decoy WARN; cheapest addition in batch (5th arm of bake-off) |
| 1 | Flow-matching invariance | P3 | 3 | 🧪 **TOY** | 🟡 | Stage 2+6 same-axis as Sinkhorn (b6 TOY); A/B mandatory after Sinkhorn settles |
| 4 | RL augmentation policy | P2 | 3 | 🔁 **REFRAME** | 🟢 | Stage 6 FAIL (original falsification design measures wrong control); SelfAugment near-duplicate |
| 5 | Neural-collapse ETF prototypes | P5 | 3 | 🔁 **REFRAME** | 🟡 | Stage 1-6 all WARNed (6/6); Cramér-Wold↔ETF redundancy prerequisite + SwAV-baseline scope |
| 6 | SU(d)-structured-orthogonal projector (quantum-circuit-inspired) | P3 | 3 | 🧪 **TOY** | 🟡 | Stage 1 quantum-framing-decorative + Stage 4 vanishing-grad caveat + Stage 6 noise-regime + capacity-vs-orthogonality control |
| 7 | FM-SIGReg (flow-matching transport to N(0,I)) | P3 | 3 | 🧪 TOY (v1) → 🚀 **FULL SEND** (v2 after research upgrade) | 🟢 | v2 deflects all 4 v1 WARNs: ExFM target (S1), KL upper bound arXiv:2511.05480 (S4), Multisample OT (S6), non-Gaussian target capability Hyvärinen cannot match (S6). See idea-7-vetting-v2.md |

## Survival statistics
- KILLED: 0/7 (0 %)
- REFRAMED: 2/7 (29 %)
- TOY: 4/7 (57 %)
- **FULL SEND: 1/7 (14 %)** — Idea 7 FM-SIGReg-v2 (after research-driven upgrade); Idea 3 graduation-eligible via Phase A pass (free)
- **survival_rate = (FULL + TOY) / N = 5/7 = 71 %**

Adding Idea 7 (FM-SIGReg) lifted survival to 71 %. **Idea 7 v2 vetting upgraded TOY → FULL SEND** after targeted research surfaced four mechanism upgrades (ExFM, KL upper bound arXiv:2511.05480, Multisample OT, non-Gaussian target capability) that deflect all four v1 WARNs with cited prior art. **First FULL SEND of batch-7.** The 3 SIGReg-term-axis ideas (Hyvärinen, max-sliced, FM-SIGReg-v2) now form a natural 5-way bake-off with the b5 KSD/Riesz-MMD TOYs — closes the SIGReg-term axis permanently after the experiment.

**Calibration**: 60 % is in the healthy 30–70 % band — first batch to drop below the b4/b5/b6 67 % triple-streak, attributable to the user-directed 100 % T3 tier override (higher-novelty / higher-variance ideas concentrate the WARN-load).

**Process credit**: batch-7 ideation correctly addressed two batch-6 process gaps:
- ✅ Avoided all batch-1..6 TOY-queue duplicates (no register-tokens, no RankMe-controller, no Sinkhorn-direct, no iBOT-SIGReg, no PH).
- ✅ Searched `<technique> SSL representation learning` for every T3 idea (per search log).

**Process gap surfaced this batch**:
- ⚠️ **Idea 4 self-flagged as EXTENDS bordering DUPLICATE** but was drafted anyway. Skill-rule recommendation: **a self-flagged EXTENDS-bordering-DUPLICATE should auto-trigger a re-framing pass at draft-time** rather than ship-as-is. The reframe (saliency-init RL vs saliency-frozen) was identifiable in draft; would have saved the vetting cycle.
- ⚠️ **Idea 5 prerequisite check was identified in `Notes & warnings` but the idea was shipped without running the `0-cost` literature search.** Same recommendation: **identified `0-cost` prerequisites should be run in-line during ideation**, not deferred to vetting.

## Top-3 across distinct axes

### 🥇 Top FULL SEND (composite × confidence)
**Idea 3 Adversarial max-sliced SIGReg** — graduate to FULL SEND on Phase A pass.
- composite × confidence: 2.17 × 0.5 = **1.09** (pre-Phase-A); on Phase A pass with 🟢 confidence: 2.17 × 0.8 = **1.74**
- Strongest novelty in batch with the cleanest math claim (`max_u T(Zu) = 0 ⇔ Z ∼ N(0,I)` is literally the universal-quantifier reading of Cramér–Wold).
- Cost: ~2 hr Phase A free CPU+small-GPU; if pass, ~15 GPU-h Phase B 4-arm.
- Risk: non-convex minimax stability — but low-capacity adversary (`d`-param on `S^(d−1)`) is much better-behaved than GAN minimax.
- **If wins, potentially supersedes the entire variance-reduction sampler family** (SRHT, Repulsive, Antithetic+SH-CV, t-design — all batch 2–5 work becomes irrelevant). High-leverage gamble.

### ⚡ Fastest to validate (lowest toy_cost)
**Idea 2 Hyvärinen Phase A + Idea 3 Phase A**: ~3 hr total (CPU + small GPU).
- Idea 2 Phase A: 1-hr synthetic-noise sanity for convex-decoy mitigation.
- Idea 3 Phase A: 2-hr alternating-optimization stability on rotated-synthetic.
- Both decisive: if either fails, the corresponding Phase B is killed at zero GPU-h cost.

### 🎯 Highest expected value (gain_mid × P(survive))
**Idea 3 max-sliced** — mid +0.7 pp × P(survive) ≈ 0.5 → **0.35 pp EV** AND highest upside if compute-savings (1000× fewer slices) materializes — secondary effect on training-time budget is large.

## Killed table
*Empty.* No idea killed this batch.

## Reframed table

| # | Title | Reframe direction |
|---|-------|-------------------|
| 4 | RL augmentation policy | Re-design as **saliency-init RL vs saliency-frozen** (isolates the online-adaptation delta from the prior-knowledge contribution). Original `random / saliency / RL-from-random` design measures the wrong control — RL-from-random will likely lose to saliency-frozen, killing the idea for the wrong reason. The reframed experiment requires only saliency-crops infra (already FULL SEND from b5) + PPO on top. Effort downgrade S–M. **Do NOT spend new compute on the original design.** Re-submit as a fresh idea in a future batch. |
| 5 | Neural-collapse ETF prototypes | **0-cost prerequisite pass**: (a) literature search `"Cramér–Wold neural collapse simplex ETF"` AND `"isotropic Gaussian prototype simplex ETF"`; (b) empirical check on saved LeJEPA baseline checkpoint — k-means (K=20) cluster-mean pairwise cosine matrix vs ETF target `−1/19`. If either pre-check shows redundancy, **KILL definitively**. If both pre-checks pass, re-submit with SwAV-style baseline (not LeJEPA-only) and K-sweep included. |

## Toy queue (cost-ascending, batch-7 additions only)

| Priority | # | Title | Toy cost | Decision rule | Dependency |
|----------|---|-------|----------|---------------|-----------|
| 1 | 2-A | Hyvärinen Phase A (CPU convex-decoy sanity) | 0 GPU-h (CPU, 1 hr) | `‖s_θ + z‖_F` decreases AND `‖Cov(z) − I‖_F` does NOT decrease in isolation (proves decoy is reachable; needs joint training) → Phase B fires; else KILL | None — run immediately |
| 2 | 3-A | Max-sliced Phase A (alternating-opt stability on rotated synthetic) | 0 GPU-h (CPU + ~1 hr small-GPU) | `T(Z·g_φ)` monotonically increases AND converges (oscillation < 10 % over last 200 steps) → Phase B fires; else KILL adversary direction (keep 50/50-mix only) | None — run immediately |
| 3 | 2-B | Hyvärinen 5th arm of per-slice bake-off on ImageNet-10 | 6 GPU-h | Hyvärinen ≥ EP − 0.3 pp at matched WC × 1.10 → KEEP; Hyvärinen ≥ winner + 0.4 pp non-overlap → FULL SEND new SIGReg default; loses by > 0.3 pp → KILL | Phase A pass; ASHA Step-0 |
| 4 | 1-A/B | Flow-matching invariance 3rd arm in alignment bake-off | 12 GPU-h (~5 GPU-h incremental over Sinkhorn b6) | FM ≥ baseline-MSE + 0.4 pp AND within ±0.3 pp of Sinkhorn → FULL SEND as alignment 2nd-option; FM > MSE but < Sinkhorn − 0.3 pp → REFRAME (Sinkhorn dominates); FM ≤ MSE → KILL; flow divergence > 0.5 on val → KILL (volume collapse) | ASHA Step-0; b6 Sinkhorn Phase B settled first (sequencing) |
| 5 | 6 | Structured-orthogonal projector 4-arm on ImageNet-10 (with `MLP-strong-wd` control) | 12 GPU-h | Best structured ≥ baseline + 0.4 pp AND > `MLP-strong-wd` by ≥ 0.3 pp → FULL SEND; ≈ `MLP-strong-wd` within ±0.3 pp → REFRAME (use weight decay, not structure); ≤ baseline − 0.3 pp → KILL; all 4 within ±0.3 pp → re-run at 600 ep | ASHA Step-0; vectorized butterfly impl required |
| 6 | 3-B | Max-sliced 4-arm on ImageNet-10 | 15 GPU-h | `1-adv > 1-random + 0.4 pp` AND `1-adv ≥ 1024-random − 0.3 pp` → FULL SEND, supersedes sampler family; `1-adv ≤ 1-random + 0.4 pp` → KILL; `50-50 mix > 1-adv + 0.3 pp` → REFRAME (mixed dominates) | Phase A pass; ASHA Step-0 |

## FULL SEND queue (batch-7 additions only)

*Empty for now.* Idea 3 (max-sliced) is the most-likely batch-7 graduation candidate via Phase A pass — re-vet on results.

## Recommended user action

**Step 0 (unchanged across batches 1–7)**: Run batch-2 Idea 5 ASHA sweep as the gate for absolute-pp claims.

**Step 1 (this week, free, parallel)**: Run **Idea 2 Phase A + Idea 3 Phase A** jointly. ~3 hr CPU+small-GPU total. Both decide whether their respective Phase Bs fire.
- Idea 2 Phase A: synthetic-Z convex-decoy sanity for Hyvärinen.
- Idea 3 Phase A: rotated-synthetic alternating-opt stability for max-sliced.

**Step 2 (parallel to Step 0, ideation-process action)**: Re-submit **Idea 4 as the reframed saliency-init RL experiment** in batch-8 — do NOT spend new compute on the original design. The reframe direction is concrete (2 paragraphs in §Reframed table) and the experimental infra exists (saliency crops b5 FULL SEND).

**Step 3 (this week, free, ideation-process action)**: Run **Idea 5 prerequisite passes** (`0-cost`): literature search for Cramér-Wold↔ETF equivalence + empirical k-means-cosine check on saved LeJEPA checkpoint. If either pre-check shows redundancy, KILL definitively and archive direction.

**Step 4 (after ASHA + Idea 2 Phase A pass)**: **Ship Idea 2 Phase B** as the 5th arm of the per-slice statistic bake-off. ~6 GPU-h, the cheapest bake-off-completion step in batches 1–7.

**Step 5 (after ASHA + Idea 3 Phase A pass)**: **Ship Idea 3 Phase B** 4-arm on ImageNet-10. ~15 GPU-h. The highest-leverage bet in batch-7 — potentially supersedes the entire variance-reduction sampler family.

**Step 6 (after b6 Sinkhorn settled + Step 0)**: **Ship Idea 1 (flow-matching) as 3rd arm in the alignment bake-off** alongside Sinkhorn-Phase-B results. ~5 GPU-h incremental.

**Step 7 (cross-skill feedback to ideation)**:
- **Compose-mode recommendation now 5 batches in a row** (batches 3, 4, 5, 6, 7 vettings all flagged it). User has explicitly redirected ideation toward T3-themed novel-axis ideas (batch-7) rather than compose-mode enumeration. **Decision-point for user**: continue T3-heavy ideation (next batch-8) OR pivot to compose-mode enumeration of the cumulative ~8-component survivor stack (PIT, SRHT, SAM/FSAM, ASHA, Saliency, SIE-split, [pending] Sinkhorn, [pending] RankMe-controller).
- **Two ideation-process gaps surfaced this batch**:
  1. Idea 4 was self-flagged EXTENDS-bordering-DUPLICATE but shipped anyway. **Skill-fix recommendation**: add to `benchmark-climb-ideation` Stage 3 drafting checklist — if an idea self-flags as EXTENDS-bordering-DUPLICATE, auto-trigger a same-batch reframe pass before shipping.
  2. Idea 5 had a flagged `0-cost` prerequisite (Cramér-Wold↔ETF literature search) that was deferred to vetting instead of run at draft-time. **Skill-fix recommendation**: identified `0-cost` prerequisites in idea-drafting must be run *during* drafting, not deferred — they often determine whether the idea is shippable.

## Notes & warnings

- ⚠️ **First batch below 67 % survival rate since b3** — drop attributable to user-directed 100 % T3 tier override (high-novelty / high-variance ideas concentrate the WARN-load). Survival 60 % is still in healthy band — no spot-audit needed. The pattern suggests **T3-heavy batches naturally yield more REFRAMEs and fewer FULL SENDs** — the user should expect this when overriding tier mix.
- 🟢 **Idea 3 (max-sliced) is the only graduation-eligible idea in batch-7**, contingent on Phase A pass. The math claim (`max_u T(Zu) = 0 ⇔ Z ∼ N(0,I)`) is the cleanest statement in the batch.
- 🟢 **Idea 2 (Hyvärinen) is the cheapest TOY in batch-7** — Phase A free CPU + Phase B 6 GPU-h. Slot into the existing per-slice bake-off; resolves the multivariate-vs-per-slice corner permanently.
- ⚠️ **Idea 4 was preventable as a vetting cycle** — the self-flagged DUPLICATE-bordering-EXTENDS warning at draft-time should have triggered an in-batch reframe. **The reframed idea (saliency-init RL) is genuinely interesting and should ship in batch-8.**
- ⚠️ **Idea 5 was preventable as a vetting cycle** — the flagged `0-cost` literature-search prerequisite should have run at draft-time. **Run the pre-checks first; if they pass, re-submit with SwAV-style baseline.**
- ⚠️ **Compose-mode recommendation 5 batches in a row** (b3, b4, b5, b6, b7 vettings all flagged). User has explicitly chosen T3-novel-axis over compose-mode for the last 2 batches. The cumulative survivor stack is now **8 concrete components** with potentially **+3 from batch-7** (max-sliced, Hyvärinen, flow-matching) on Phase A passes. **Recommend the user formally choose**: continue T3-novel-axis ideation (batch-8 onward) OR pivot to formal compose-mode enumeration via a new `--compose-mode` flag in ideation skill.
- ⚠️ **Idea 3 (max-sliced) supersedes the variance-reduction sampler family if it ships** — SRHT (b3 survivor), Repulsive, Antithetic+SH-CV, t-design (all batches 2–5 work) become irrelevant under max-sliced. High-stakes outcome; the Phase A is decisive and free.
- ⚠️ **Stages 4 (theory) under climb-mode lite continued the trend of WARN-heavy outcomes** — 4/5 ideas WARNed at Stage 4. This is structural: T3 cross-domain ideas always have theory-transfer caveats. Not a calibration concern, but informs the survival-rate expectation under T3-heavy mix.
- ⚡ **Step 1 (joint Phase As for Idea 2 + Idea 3) is the cheapest TOY group in batches 1–7** — ~3 hr CPU+small-GPU for 2 decisive gates. Do this immediately regardless of other priorities. The decisions made here gate ~21 GPU-h of downstream work.

## Provenance signature
SHA256(inputs + verdicts + 2026-05-19): vetting-batch-7
