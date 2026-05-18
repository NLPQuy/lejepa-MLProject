# Vetting Report: Decomposition by problem subtype with self-correction

**Source**: `ideation-output/MATH-500/batch-1.md` idea 7
**Vetted**: 2026-05-17T15:32:00Z
**Skill version**: 0.5.0
**Time-to-vet**: 9 min
**Mode flags**: --climb-mode (Stage 7 lite; Stage 4 lite)

> 📘 **Reference example: FULL SEND verdict with 6 PASS + 2 WARN across 8 stages.**
> Demonstrates persona variety, every stage doing real work, attacks WEAKENED but not UNREBUTTED, and Stage 8 citing the priority rule.

## TL;DR
- **Verdict**: ✅ **FULL SEND** 🟢
- **One-liner**: Detect math-problem subtype (algebra/geometry/combinatorics/NT) with a 1-shot classifier prompt; route to a subtype-tuned solve prompt; verify with a second-pass self-correction over the boxed answer.

## Stage results

| Stage | Persona | Verdict | Confidence |
|-------|---------|---------|------------|
| 1. Problem Framing | Advisor | ✅ PASS | 🟢 |
| 2. Prior Work Attack | Hunter | ✅ PASS | 🟢 |
| 3. Novelty Decomp | Critical Reviewer | ✅ PASS | 🟡 (workshop-tier novelty, fine for climb) |
| 4. Theory Grounding | Theorist (lite) | ✅ PASS | 🟢 |
| 5. Feasibility | Pragmatic PM | ⚠️ WARN | 🟢 (tight but feasible) |
| 6. Killer Baseline | Empiricist | ⚠️ WARN | 🟡 (Tool-use close) |
| 7. Reviewer Sim | R2 only (climb-lite) | ✅ PASS | 🟢 |
| 8. Decision | PI | **FULL SEND** | 🟢 |

## Per-stage details

### Stage 1: Problem Framing
**Persona declared**: "Adopting persona: Advisor. Stance: charitable but probing."
- M1: Math problems span heterogeneous subtypes (algebra, geometry, combinatorics, NT). A single prompt averages strategies. M3: gpt-4o-mini fails geometry problems disproportionately (~12 pp below algebra). M4: Real — Frieder et al. 2024 documents subtype-dependent accuracy gap. M5: Scaling helps but doesn't close the gap.
- **Attack**: "Already implicit-solved by chain-of-thought prompts." → Steel-man: CoT alone does not branch on subtype. → Hunter response: agreed.
- **Final status**: ✅ DEFLECTED. **Verdict**: PASS.

### Stage 2: Prior Work Attack
**Persona declared**: "Adopting persona: Prior-Work Hunter. Stance: hostile until proven novel."

**Search log**: `"subtype classifier" "math" 2024` → 4 hits; `"adaptive prompt" "MATH-500"` → 2 hits. Closest is Zheng et al. (workshop 2024) — routes math-vs-code, not within-math.

**Attack 1**: "Just Zheng et al. 2024 'Routing Among Specialists'?"
- Steel-man (R1): Zheng routes ACROSS task families; this routes WITHIN math by subtype. Different granularity.
- Hunter (R1): Granularity delta clear. ✅ DEFLECTED.

**Attack 2**: "Specialized prompts per subtype is just prompt engineering."
- Steel-man (R1): Contribution is the (classify → subtype-prompt → self-correct) **pipeline**, not the prompts alone.
- Hunter (R1): Accepted; R3 may push in Stage 7. ✅ DEFLECTED.

**Verdict**: PASS 🟢.

### Stage 3: Novelty Decomposition
**Persona declared**: "Adopting persona: Critical Reviewer. Stance: default reject."

8-axis check: Axis 6 (Application) ✅, Axis 8 (Synthesis: classifier + specialized prompts + self-correction) ✅. Other axes ❌. Strip test (S13): removing the synthesis (use a single uniform prompt) recovers baseline behavior → synergy is real.

Rebranding check (R9-R12): NOT a renaming / module-swap / notation / hyperparameter — the routing logic is real new control flow.

**Attack**: "Workshop-tier, not main-track."
- Steel-man (Round 1): For `--climb-mode`, workshop-tier suffices; goal is ship, not paper.
- Reviewer response (Round 1): Conceded under climb-mode; would not pass at A* without stronger theory. ⚠️ WEAKENED.

**Verdict**: PASS 🟡 — defensibility = workshop or engineering report.

### Stage 4: Theory Grounding (climb-lite)
**Persona declared**: "Adopting persona: Theorist. Stance: empirics are noise — show me a mechanism." (Climb-mode → relaxed.)

Mechanism: subtype routing reduces strategy averaging; self-correction catches arithmetic errors that the routed prompt cannot avoid. Inductive-bias view (V6) ✅: routing imposes a piecewise-uniform prior over solver strategies, matching the bimodal MATH-500 distribution. Optimization view (V7) ✅: per-subtype prompts shorten the in-context "search" the model performs.

**Attack**: "The mechanism is informal; no convergence story."
- Steel-man (Round 1): In climb-mode, intuition + empirical correlation is acceptable; cited evidence from Frieder et al. 2024.
- Theorist response (Round 1): Acceptable under climb-mode. ✅ DEFLECTED.

**Verdict**: PASS 🟢.

### Stage 5: Feasibility
**Persona declared**: "Adopting persona: Pragmatic PM. Stance: numerical."

Numbers (Q-bank M1-M7): compute total $25 (across 500 problems × 3 prompts × ~$0.0015) + 3 seeds = $75 vs budget $100. Wallclock 4 h. Noise σ ≈ 0.4 pp; expected gain +1.8 pp; effect size 4.5σ; significance achievable with 3 seeds.

**Attack**: "Cost is at 75 % of budget — no slack for an ablation matrix."
- Steel-man (Round 1): The user already declared `--climb-mode`; the ablation matrix can be deferred to a follow-up; the main run alone fits within budget with 25 % slack.
- PM response (Round 1): Tight. WARN, not FAIL — feasible if user does not also want a per-subtype ablation. ⚠️ WEAKENED.

**Verdict**: ⚠️ WARN 🟢 — feasible, tight, descope OK.

### Stage 6: Killer Baseline
**Persona declared**: "Adopting persona: Skeptical Empiricist. Stance: baseline wins until proven otherwise."

Catalog (B1-B12) → applicable: B1 (SC K=100) +0.8pp est., B3 (CoT) baseline, B10 (Tool-use Python-exec) +1.5pp est., B11 (kNN retrieval) +0.6pp est.

**Attack**: "Tool-use (B10) estimated at +1.5 pp vs your idea +1.8 pp at similar cost. 0.3 pp delta is within noise. Killer candidate."
- Steel-man (Round 1): The two are complementary — Tool-use handles arithmetic, our routing handles strategy choice. Combined version should super-add. We will include `routing × tool-use` as an ablation in the main run.
- Empiricist response (Round 1): Acceptable IF the ablation actually runs and shows super-additivity. WARN, not FAIL — promise of ablation is a commitment, not a deflection. ⚠️ WEAKENED.

**Verdict**: ⚠️ WARN 🟡 — close baseline, must ablate Tool-use combination.

### Stage 7: Reviewer Simulation (climb-lite — R2 only)
R2 score 4/5 Accept: design adequate; baselines fair (B10 included per Stage 6); significance OK (3 seeds, σ=0.4, gain +1.8 = 4.5σ); reproducibility OK. Mock attack "no concurrent work check" → ✅ DEFLECTED via Stage 2 search log.

**Verdict**: ✅ PASS 🟢.

### Stage 8: Decision Gate
**Persona declared**: "Adopting persona: PI. Stance: synthesize, commit."

- M1: PASS=6, WARN=2 (Stages 5, 6), FAIL=0.
- M2: Stage 2 PASS, Stage 6 WARN (not FAIL), Stage 5 WARN.
- M3: No auto-KILL triggers fired.
- M4: Priority Rule **#4** (0 FAIL + ≤ 2 WARN + Stage 5 PASS-or-tight-WARN with descope plan).
- M5: **FULL SEND**.
- C6: 🟢 — 6/8 PASS, both WARNs come with concrete mitigations (descope ablation; include Tool-use in main ablation).
- C7: All stages did real work. The two WARNs are not weaknesses of the idea; they are commitments for the implementation (budget discipline + Tool-use ablation).

**FULL SEND priority**: 1 of 1 FULL SEND in batch.
**Implementation order**: classifier first (cheapest to debug) → subtype prompts → self-correction → Tool-use ablation last.
**Risk mitigation**: Stage 6 WARN — run the routing × Tool-use ablation as an early-warning experiment; if super-additivity does not appear in the first 50 problems, abort and route to TOY re-vet.

## Final decision

**Verdict**: ✅ **FULL SEND** 🟢 — Rule #4 fired. Priority rank 1 in batch.

**Risk mitigation note**: Stage 6 WARN — run routing × Tool-use ablation as early-warning experiment on the first 50 problems.

## Attacks summary

| # | Stage | Attack | Status |
|---|-------|--------|--------|
| 1 | 1 | "Benchmark artifact / already-solved by CoT" | ✅ DEFLECTED |
| 2 | 2 | "Just Zheng et al. routing" | ✅ DEFLECTED |
| 3 | 3 | "Workshop-tier novelty" | ⚠️ WEAKENED (acceptable in climb-mode) |
| 4 | 4 | "No formal convergence" | ✅ DEFLECTED (climb-mode lite) |
| 5 | 5 | "Cost at 75 % of budget" | ⚠️ WEAKENED (descope ablation) |
| 6 | 6 | "Tool-use within noise of your idea" | ⚠️ WEAKENED (commit to combined ablation) |
| 7 | 7 | "Mock R2 — broader baseline comparison" | ✅ DEFLECTED |

## User actions

1. Implement classifier + subtype prompts + self-correction (priority 1).
2. Include `routing × Tool-use` ablation in main run (Stage 6 commitment).
3. Report 3-seed results; re-vet if gain < +1.0 pp.

## Confidence

🟢 High. 6/8 PASS. WARNs come with explicit mitigations rather than open uncertainty.

---

## 📘 Annotation: What makes this idea pass

1. **Every stage issued ≥ 1 attack with a real rebuttal cycle.** No stage rubber-stamped.
2. **Persona voice consistent**: Hunter cites papers (S2); PM gives numbers (S5); Empiricist names baselines with pp estimates (S6); Theorist relaxes for climb-mode (S4).
3. **WARNs are not FAILs.** S5 and S6 rebuttals offered concrete commitments (descope, include ablation) — correctly marked WEAKENED, not DEFLECTED. User must follow through.
4. **S6 is the gating test.** Tool-use is the typical killer; the rebuttal ABSORBED it by committing to an ablation (attack → ablation commitment) — the right pattern.
5. **S8 cited Rule #4 explicitly.** Auditability holds.
6. **Risk-mitigation note names a specific early-warning experiment** (first 50 problems), not vague "monitor closely".
