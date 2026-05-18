# Idea 5 Vetting — Multi-fidelity HP sweep (ASHA over λ, lr, wd)
**Batch**: 2 · **Pattern**: P7 (Search)
**One-liner**: 8-arm ASHA at 25→50→75→100 ep rungs over (λ, lr, wd); produces *measured ImageNet-10 baseline* + a defensible λ for every later ablation.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.

**Attack A1.1**: This is not a research idea — it is infrastructure. The vetting skill's purpose is to gate research ideas, not engineering tasks.
**Steel-manned rebuttal**: Vetting batch-1's `Recommended user action` step 0 was literally "Run lejepa-vit-small.py to fix the baseline." A *principled* sweep beats a single run as a measurement instrument and is the minimum needed before any ranking is meaningful. The "research" framing is "what is the actual ImageNet-10 number for LeJEPA at properly-tuned HPs?"
**Persona response**: ✅ **DEFLECTED** — measurement before ideation is exactly what climb-mode needs.

**Verdict**: PASS. Cycle: 1 DEFLECTED.

## Stage 2 — Prior Work Attack
> Persona: **Prior-Work Hunter**.

ASHA (Li 2018/2020) and Hyperband (Li 2017) are textbook. Used widely. No novelty claim made; idea explicitly cites them as tools.

**Attack A2.1**: Auto-HP-search for SSL specifically has been done (e.g., Wang 2022 *AutoSSL*). Why is this an "idea" worth a slot?
**Steel-manned rebuttal**: It's not novel — the proposal owns that. The slot value is *operational*: nobody has reported the ASHA-tuned LeJEPA number on ImageNet-10, and the paper's λ=0.1 is anchored to ImageNet-1K. The result is a number, not a method claim.
**Persona response**: ⚠️ **WEAKENED** — defensible as a deliverable, but reviewers in --paper-mode would reject this as "method contribution = 0". In --climb-mode (current), it stands.

**Verdict**: PASS in climb-mode (would be REFRAME in paper-mode). EXTENDS / DUPLICATE-on-method. Cycle: 0 DEFLECTED / 1 WEAKENED.

## Stage 3 — Novelty Decomposition
> Persona: **Critical Reviewer**.

Novelty: **zero on method**, **measurement-novel** for ImageNet-10 / LeJEPA. In climb-mode, measurement is the deliverable.

**Verdict**: PASS — explicitly measurement-not-method. Cycle: 0 / 0 / 0 (no attacks needed; novelty claim is 0).

## Stage 4 — Theory Grounding (lite)
> Persona: **Theorist**.

Nothing to attack — no theory claim. ASHA's bandit regret bounds are stated in the cited paper and not re-derived here.
**Verdict**: PASS. Cycle: 0 / 0 / 0.

## Stage 5 — Feasibility Analysis
> Persona: **Pragmatic PM**.

Search space: 3 × 3 × 3 = 27 configurations, but ASHA visits 8 → 4 → 2 → 1 ≈ 4× single-run compute. ViT-S/IN-10/100ep ≈ 1.5 GPU-h → total **6-8 GPU-h**. Add 2 seeds at top rung → ≈ 12 GPU-h.

**Attack A5.1**: ASHA assumes the rung metric correlates with the top-rung metric. Linear probe at 25 ep may not predict linear probe at 100 ep — SSL has cold-start curves. Promotion decisions on a non-predictive proxy = ASHA throws away the future winners.
**Steel-manned rebuttal**: Use a more-predictive intermediate metric: **kNN top-1** on the train embedding (in-batch, no probe training) at every epoch. kNN curves are smoother and have been shown (DINOv2, DINOv3) to track linear-probe well. Or simply run ASHA with successive halving on SIGReg-validation loss (which is predictive of probe by the LeJEPA theorem).
**Persona response**: ✅ **DEFLECTED** — kNN proxy fixes the predictivity issue at zero cost. Add to the proposal.

**Verdict**: PASS with refinement (use kNN as the ASHA promotion metric). Effort S. Cycle: 1 DEFLECTED.

## Stage 6 — Killer Baseline
> Persona: **Skeptical Empiricist**.

**Attack A6.1**: The killer baseline is **"just run paper-default 3 seeds"**. If the λ landscape over ImageNet-10 is flat between 0.02 and 0.1 (LeJEPA Fig. 4 hints flat), ASHA returns no λ signal — and you spent 4× compute to learn that.
**Steel-manned rebuttal**: Even in the flat case, the deliverable is *(a)* a real seed-averaged baseline number with CI, *(b)* the empirical landscape (publishable as a plot), *(c)* a defensible λ to anchor later ablations. None of these exist today. The 4× compute is bounded: 12 GPU-h vs. infinity-hours of arguing about "what if λ was wrong".
**Persona response**: ⚠️ **WEAKENED** — true that flat-landscape ASHA returns no λ signal, but proposal explicitly handles this in its falsification test ("measured baseline is still the deliverable").

**Verdict**: PASS — proposal already anticipates and accepts the flat-landscape failure mode. Cycle: 0 / 1 / 0.

## Stage 8 — Decision
Tally: PASS / PASS / PASS / PASS / PASS / PASS — **0 FAIL, 1 WARN, 0 UNREBUTTED**.
Per `decision-logic.md`: 0 FAIL + ≤ 2 WARN + Stage 5 PASS + Stage 6 PASS → **FULL SEND**.

**Verdict**: ✅ **FULL SEND** · 🟢 confidence

### Refinements (must adopt before launch)
1. Replace linear-probe ASHA metric with **kNN top-1 on train batch** for promotion decisions (per Stage 5 rebuttal).
2. Top rung must run **≥ 2 seeds** for the final number to have a CI.
3. Output deliverable: ImageNet-10 baseline number + landscape plot. Publish both before any other batch-2 idea is graded.

### Priority
**HIGHEST** — every other idea in batch-2 (and outstanding TOYs from batch-1) becomes more rankable once this lands. Block on this.

Cycle totals: 3 DEFLECTED / 2 WEAKENED / 0 UNREBUTTED.
