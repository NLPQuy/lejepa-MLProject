# Vetting Report: MCTS-guided reasoning with execution verifier

**Source**: `ideation-output/MATH-500/batch-1.md` idea 5
**Vetted**: 2026-05-17T15:21:00Z
**Skill version**: 0.5.0
**Time-to-vet**: 10 min
**Mode flags**: default

> 📘 **Reference example: TOY verdict from mixed signals.**
> Demonstrates how 3-4 WARNs (no FAIL) route to a cheap toy experiment rather than KILL. Includes a complete Toy Experiment Design block.

## TL;DR

- **Verdict**: 🧪 **TOY EXPERIMENT FIRST** 🟡
- **One-liner**: MCTS over reasoning traces with Python-exec leaf rewards is plausible but cost-risky AND has a close Tool-use baseline. Resolve both uncertainties with a $10 / 1.5 h toy on 50 problems before committing $100 to full eval.

## Stage results

| Stage | Persona | Verdict | Confidence |
|-------|---------|---------|------------|
| 1. Problem Framing | Advisor | ✅ PASS | 🟢 |
| 2. Prior Work Attack | Hunter | ✅ PASS | 🟡 (close cousins exist) |
| 3. Novelty Decomp | Critical Reviewer | ✅ PASS | 🟢 |
| 4. Theory Grounding | Theorist | ⚠️ WARN | 🟡 (mechanism intuitive, weak on non-executable steps) |
| 5. Feasibility | Pragmatic PM | ⚠️ WARN | 🟢 (cost > budget × 1.5 for full ablation) |
| 6. Killer Baseline | Empiricist | ⚠️ WARN | 🟡 (Tool-use close, may super-add) |
| 7. Reviewer Sim | R1/R2/R3 | Borderline | 🟡 |
| 8. Decision | PI | **TOY** | 🟡 |

## Per-stage details

### Stage 1: Problem Framing
**Persona**: Advisor.
M1-M5 answered. Problem: MATH-500 baseline (gpt-4o-mini) plateaus around 70 %; reasoning traces show step-level errors that a verifier could catch. Real problem; not artifact; scale-up baseline (gpt-4o) costs 30× and only adds ~6 pp.
**Attack**: "Already solved by SC + voting." → Steel-man: SC scores entire traces uniformly; this scores per-step. → Advisor: ✅ DEFLECTED.
**Verdict**: PASS 🟢.

### Stage 2: Prior Work Attack
**Persona**: Hunter.
Search log: 5 queries. Closest cousins: Yao et al. ToT (NeurIPS 2023, arXiv:2305.10601) — tree search but no exec verifier; Lightman et al. (ICLR 2024, arXiv:2305.20050) — learned verifier, not exec; Snell et al. 2024 — does not test MCTS + exec on MATH.

**Attack 1**: "Just Yao et al. ToT with a different leaf scorer?"
- Steel-man (R1): ToT uses LLM-judged leaves; this uses deterministic exec — cheaper and more reliable on executable steps.
- Hunter (R1): Granularity delta real; must address non-executable subset. ⚠️ WEAKENED.

**Attack 2**: "Concurrent: Trinh et al. AlphaGeometry?"
- Steel-man (R1): AlphaGeometry is geometry-specific with a symbolic engine; different scope.
- Hunter (R1): ✅ DEFLECTED.

**Verdict**: PASS 🟡.

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.
Novel axis 8 (Synthesis: MCTS + exec verifier on math reasoning). Strip test: removing exec verifier reverts to plain ToT — different mechanism, real synergy. Rebranding checks all clear.
**Attack**: "Workshop-tier novelty?" → Steel-man: synthesis + new application axis → A* viable. → ✅ DEFLECTED.
**Verdict**: PASS 🟢.

### Stage 4: Theory Grounding — WARN
**Persona**: Theorist.
Mechanism (M1): MCTS reduces credit-assignment variance via dense reward; exec verifier provides cheap ground-truth signal on the subset of intermediate algebra steps. Views: V6 (inductive bias — search over reasoning) ✅, V7 (optimization — denser reward) ✅. **Counterexample (M5)**: proof-style problems with no executable form → reward landscape goes flat → MCTS degenerates to random search.

**Attack**: "On proof problems your mechanism predicts failure mode but you have no fallback."
- Steel-man (Round 1): Empirically, MATH-500 contains < 15 % pure-proof problems; the mechanism wins on the other 85 %.
- Theorist response (Round 1): Empirical claim, untested. Until shown, mechanism is WEAKENED — works on most-cases-modal but not falsifiable on the 15 %.
- ⚠️ WEAKENED.

**Verdict**: ⚠️ WARN 🟡 — mechanism intuitive, 15 %-subset gap acknowledged.

### Stage 5: Feasibility — WARN
**Persona**: Pragmatic PM.
Numbers: 500 × K=5 × N=20 × $0.002 = $100/pass; 3 seeds = $300; full ablation K∈{3,5,8}×N∈{10,20,40} = $2,700. Budget $100.

**Attack**: "Ablation = $2,700 vs $100 budget. Infeasible."
- Steel-man (R1): Skip full ablation, commit K=5/N=20 + 3 seeds = $300.
- PM response (R1): Still > budget × 2. WEAKENED — TOY first is the right route.
- ⚠️ WEAKENED.

**Verdict**: ⚠️ WARN 🟢 — feasible for toy, not full at stated budget.

### Stage 6: Killer Baseline — WARN
**Persona**: Skeptical Empiricist.
Catalog: B1 SC K=100 +0.8pp, B10 Tool-use Python-exec +2.0pp, B11 retrieval +0.6pp. Idea claims +4.0pp.

**Attack**: "Tool-use B10 estimated +2.0pp at 100× cheaper than full MCTS. The 'verifier' aspect of your idea is Tool-use in disguise; the MCTS adds the search."
- Steel-man (Round 1): MCTS + exec is **search over** Tool-use; predicted super-additivity (~+4pp = +2pp Tool-use base + +2pp from MCTS search structure).
- Empiricist response (Round 1): The +2pp from MCTS is an unverified extrapolation. WEAKENED — must be tested before commitment.
- ⚠️ WEAKENED.

**Verdict**: ⚠️ WARN 🟡 — Tool-use close; super-additivity claim must be demonstrated.

### Stage 7: Reviewer Simulation
- R1 Theoretician 3/5 Borderline: "No convergence argument for MCTS on non-zero-sum reward."
- R2 Empirical 3/5 Borderline: "K=5/N=20 + 3 seeds insufficient; need K, N ablation."
- R3 Novelty 4/5 Accept: "Real delta vs ToT; novel application."
- Aggregate: 1 Accept + 2 Borderline → ⚠️ WARN. Critical fixes: convergence plots + ablate K and N.

**Verdict**: ⚠️ WARN 🟡.

### Stage 8: Decision Gate
- M1: PASS=3, WARN=4 (4,5,6,7), FAIL=0.
- M4: Rule **#5** fires (0 FAIL + 3-4 WARN → TOY).
- M5: **TOY EXPERIMENT FIRST**.
- C6: 🟡 — 4 WARN, all resolvable by one cheap toy.
- C7: Cost ceiling + Tool-use close-call + proof-subset gap all testable in one $10 experiment. Routing to TOY costs $10; FULL costs $300 with high failure risk.

## Toy Experiment Design

**Idea being toyed**: MCTS-guided reasoning with execution verifier.
**Triggered by**: Stage 5 (cost) + Stage 6 (Tool-use close) + Stage 4 (proof-subset gap).

### Goal
Validate the super-additivity claim: does **MCTS + exec verifier** beat **Tool-use alone** by ≥ +1.0 pp on a 50-problem subset?

### Setup
- **Dataset**: 50 random problems sampled from MATH-500 test set, **stratified by subtype** so that ~ 8 proof-style problems are included (covers the Stage-4 gap).
- **Model**: gpt-4o-mini (same as target).
- **Config**: K=3 traces, N=10 expansions (vs full K=5/N=20).
- **Budget**: $10 (vs full $300).
- **Wallclock**: 1.5 h.

### Success criterion
Toy must show ≥ 30 % of expected gain over Tool-use baseline, i.e. ≥ **+0.6 pp** above Tool-use on the same 50 problems.

- ≥ +0.6 pp → graduate to FULL SEND (Stage 6 super-additivity claim validated).
- (+0.2, +0.6) pp → one more toy round with K=5/N=20 on same 50 problems ($25, 3 h).
- ≤ +0.2 pp OR ≤ Tool-use → FALSIFY → **KILL**.

### Confound check
- Run 3 baseline seeds (Tool-use alone) on the 50 problems first. Estimate σ.
- Required gain ≥ 2σ for significance. If 50-problem σ > 0.3 pp → bigger toy needed (e.g., 150 problems).

### Falsification thresholds (numeric — fixed BEFORE running)

| Observation | Action |
|-------------|--------|
| MCTS+exec − Tool-use ≤ noise | FALSIFY → KILL |
| ∈ (noise, +0.6 pp) | one more toy round |
| ≥ +0.6 pp | promote to FULL SEND with confidence raised to 🟢 |

### Estimated cost
$10 ± $2 (3-seed Tool-use baseline = $3; MCTS toy = $7).

### Estimated time
1.5 h wallclock.

### Re-vet trigger
After toy results, user passes `/vet-ideas --given-toy ./toy-results.md idea-5`. Vetting re-runs Stages 4, 5, 6 with new evidence and emits `vetting-v2.md`.

## Final decision

**Verdict**: 🧪 **TOY EXPERIMENT FIRST** 🟡 — Rule #5 fired (0 FAIL + 4 WARN).

**Re-vet trigger**: post-toy via `--given-toy`.

## Attacks summary

| # | Stage | Attack | Status |
|---|-------|--------|--------|
| 1 | 2 | "Just ToT with different leaf scorer" | ⚠️ WEAKENED |
| 2 | 4 | "Mechanism fails on 15 % proof subset" | ⚠️ WEAKENED |
| 3 | 5 | "Ablation $2,700 vs $100 budget" | ⚠️ WEAKENED (toy is the fallback) |
| 4 | 6 | "Tool-use is the cheaper alternative" | ⚠️ WEAKENED (super-additivity claim — toy resolves) |

## User actions

1. Run the toy per design above ($10, 1.5 h, stratified 50-problem sample).
2. Report results: `MCTS+exec acc — Tool-use acc` on same 50 problems, 3 seeds.
3. Re-vet with `/vet-ideas --given-toy ./toy-results.md idea-5`.
4. Append entry to `_toy_queue.md` (cost-ascending order).

## Confidence

🟡 Medium — the verdict (TOY) is robust to plausible adjustments; the underlying super-additivity question is genuinely open and only the toy will answer it.

---

## 📘 Annotation: Why TOY is the right decision

1. **4 WARN + 0 FAIL = canonical TOY pattern.** Rule #5 fires unambiguously; skill did not collapse WARNs into a fake PASS nor inflate into FAIL.
2. **One toy resolves three uncertainties** (Stages 4, 5, 6) — stratified sampling specifically covers the Stage-4 proof-subset gap.
3. **Falsification thresholds numeric and fixed BEFORE the toy runs** per `toy-experiment-design.md` hard rule.
4. **Toy < 10 % of full budget** ($10 vs $100/pass) — a "toy" that costs 50 % is not a toy.
5. **Stage 6 (not 4 or 5) was the gating signal** — Tool-use is the typical killer; toy tests MCTS+exec **vs Tool-use alone**, not vs raw baseline.
6. **TOY queue cost-ascending discipline** preserved on append.
