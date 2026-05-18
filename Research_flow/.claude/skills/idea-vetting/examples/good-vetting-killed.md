# Vetting Report: Self-consistency K=100 with early-stop

**Source**: `ideation-output/MATH-500/batch-1.md` idea 1
**Vetted**: 2026-05-17T15:02:00Z
**Skill version**: 0.5.0
**Time-to-vet**: 4 min (early-exit from Stage 2)
**Mode flags**: default

> 📘 **Reference example: KILL verdict via early-exit from Stage 2.**
> Demonstrates correct hostile prior-work search, citation-grounded attack, weak steel-man (which is itself diagnostic), and Stage 8 short-circuit.

## TL;DR

- **Verdict**: ❌ **KILL** 🟢 (high confidence)
- **One-liner**: Hard duplicate. Chen et al., NeurIPS 2024 explicitly ablated K ∈ {64, 128, 256} for self-consistency on MATH-500 with the same gpt-4o-mini-class baseline; reported curves identical to the proposed mechanism. No delta. Idea is replication, not proposal.

## Stage results

| Stage | Persona | Verdict | Notes |
|-------|---------|---------|-------|
| 1. Problem Framing | Advisor | ✅ PASS | Problem real (SC plateau at K=20 is well-documented). |
| 2. Prior Work Attack | Hunter | ❌ **FAIL** | Hard duplicate found: arXiv:24XX.XXXXX (Chen et al., NeurIPS 2024). |
| 3-7 | — | SKIPPED | Early-exit per `stage-2/early-exit` rule. |
| 8. Decision | PI / Advisor | KILL | Rule #1 fired (Stage 2 = FAIL hard duplicate). |

## Per-stage details

### Stage 1: Problem Framing

**Persona**: Advisor (`../personas/advisor.md`)
**Persona declared**: "Adopting persona: Advisor. Stance: charitable but probing — convince me this problem is real."

**Questions covered**: M1, M2, M3, M4, M5, R7 (6/15)

- **M1**: Problem = self-consistency plateaus at K≈20 on MATH-500; pushing K higher may regain headroom.
- **M2**: Why hard: (a) cost scales linearly with K; (b) early-stop heuristics are non-trivial to tune.
- **M3**: SOTA fails on problems with thin majority distributions (≤ 30 % plurality) — gpt-4o-mini gets stuck.
- **M4**: Real problem. Documented in Brown et al. 2024 (arXiv:2407.21787) as the "monkeys" regime.
- **M5**: Scaling baseline does NOT solve it cheaply — gpt-4o at K=20 costs ~30× gpt-4o-mini at K=100.

**Attacks issued**: 1; **full rebuttal cycle**: 1.

**Attack 1**: "This is a benchmark artifact — SC plateau is well-known and trivial to push past with K↑."
- **Steel-manned rebuttal** (Round 1): The plateau is documented across multiple papers; pushing K from 20 → 100 with early-stop is a real cost-saving engineering question with non-zero design space. *Source: auto-steelman.*
- **Persona response** (Round 1): Fair. The engineering aspect is real but does not establish novelty — it only establishes "problem exists." Move to Stage 2.
- **Final status**: ✅ DEFLECTED.

**Rebuttal-cycle summary**: DEFLECTED 1 / WEAKENED 0 / UNREBUTTED 0.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢. **Time spent**: 1 min.

### Stage 2: Prior Work Attack — KILLING STAGE

**Persona**: Prior-Work Hunter (`../personas/prior-work-hunter.md`)
**Persona declared**: "Adopting persona: Prior-Work Hunter. Stance: hostile until proven novel — assume someone already did this."

**Questions covered**: M1, M2, A6, A8, A9, D11 (6/15) — search saturated after the first hit.

**Search log**:
- Query: `"self-consistency" "K" "MATH-500" 2024` → 11 hits.
- Top hit: Chen et al., "Scaling Self-Consistency on Mathematical Reasoning", **NeurIPS 2024** [arXiv:24XX.XXXXX].
- Verified: Title + venue + authors all resolve.

**Attacks issued**: 1; **full rebuttal cycle**: 1.

**Attack 1**: "Isn't this exactly Chen et al., NeurIPS 2024? Their Section 4.2 ablates K ∈ {32, 64, 128, 256} with early-stop on agreement plateau, on MATH-500, with the same model class. Same mechanism, same benchmark."
- **Steel-manned rebuttal** (Round 1): The user's idea adds early-stop at "50 % agreement" specifically, whereas Chen et al. use a different stopping criterion. *Source: auto-steelman.*
- **Persona response** (Round 1): I checked. Chen et al. Section 4.2.3 explicitly tests three early-stop thresholds including 0.5 majority plateau. They reported the curves. Your stopping rule is one of the three they swept. This is not delta — this is a hyperparameter choice within their grid.
- **Final status**: ❌ **UNREBUTTED**.

The steel-man rebuttal was weak. Per `rules/adversarial-mindset.md §4 principles`, a weak steel-man is **diagnostic** — it confirms the idea is genuinely vulnerable, not that the rebuttal-writer is weak.

**Rebuttal-cycle summary**: DEFLECTED 0 / WEAKENED 0 / UNREBUTTED 1.

**Stage verdict**: ❌ **FAIL** (hard duplicate; tag `DUPLICATE`). **Confidence**: 🟢. **Time spent**: 2.5 min.

### Stages 3-7: SKIPPED

Per `stages/2-prior-work-attack.md §Early-exit`: Stage 2 FAIL with hard duplicate → skip Stages 3-7; route directly to Stage 8 with provisional verdict KILL.

### Stage 8: Decision Gate

**Persona**: PI / Advisor.
**Persona declared**: "Adopting persona: PI. Stance: synthesize the evidence, commit to a verdict."

**Questions covered**: M1-M5, C6, C7, K15, K16 (9/19).

**Synthesis**:
- M1: PASS=1, WARN=0, FAIL=1 (Stage 2). Stages 3-7 skipped.
- M2: Stage 2 = FAIL hard duplicate.
- M3: Auto-KILL trigger — **Stage 2 FAIL hard duplicate** fired (Priority Rule #1).
- M4: Priority Rule **#1**.
- M5: **KILL**.
- C6: 🟢 — "Rule #1 fired; Stage 2 returned a cited, peer-reviewed exact-duplicate paper from the same venue tier as the proposed publication target."
- C7: The idea is replication of Chen et al. The user proposed K=100 with 50%-agreement early-stop on MATH-500 with gpt-4o-mini; Chen et al. ablated exactly this configuration in their Section 4.2. There is no delta.

**Kill rationale**:
- **K15**: Killed by Stage 2 attack #1. Evidence: Chen et al., NeurIPS 2024, Section 4.2.3 ablates the same K + same threshold + same benchmark + same model class. Citation verified.
- **K16**: Salvageable: the **comparison to Chen et al.** is itself useful context for the user when proposing the next batch — informs `--avoid-patterns P4 (Scale)` for future ideation calls.

## Final decision

**Verdict**: ❌ **KILL** 🟢

**Rationale**: Stage 2 surfaced a peer-reviewed, citation-verified exact duplicate (Chen et al., NeurIPS 2024) that ablates the same mechanism on the same benchmark. The steel-manned rebuttal could not produce a delta argument; rebuttal verdict was UNREBUTTED. Rule #1 (Stage 2 FAIL hard duplicate) fired directly.

**Re-vet trigger**: None. Resurrection eligible? **No** — exact duplicate is unrecoverable; no counter-argument can change reality.

## Attacks summary

| # | Stage | Attack | Status |
|---|-------|--------|--------|
| 1 | 1 | "Benchmark artifact" | ✅ DEFLECTED |
| 2 | 2 | "Exact duplicate of Chen et al. NeurIPS 2024" | ❌ UNREBUTTED — killer |

## User actions

1. Append to `_logs/_killed_ideas.md` (entry includes citation + resurrection-eligible=no).
2. On next `/propose-benchmark-ideas MATH-500`, pass `--avoid-patterns P4` to bias ideation away from SC-scaling variants.
3. Read Chen et al. NeurIPS 2024 if not already — their negative findings on K > 128 are useful context for any future Scale-pattern idea.

## Confidence

🟢 High — the killing evidence is a peer-reviewed paper at an A* venue with explicit ablation matching the proposed mechanism. No ambiguity.

---

## 📘 Annotation: Why this kill is correct

1. **Stage 2 ran with a real adversarial search** — the Hunter persona ran a date-bounded query, found the duplicate, and verified the title + venue + authors + section before issuing the attack. Compare to `bad-vetting-too-lenient.md` where Stage 2 issued vague attacks without searching.
2. **The steel-manned rebuttal was honestly weak** — and that weakness was *correctly read as diagnostic*. Per `adversarial-mindset.md §4 Principles #1`, a weak steel-man is information about the idea, not a failure of the writer. The skill did not inflate the rebuttal to "make it interesting."
3. **The rebuttal was UNREBUTTED, not WEAKENED.** A WEAKENED would have implied "needs ablation"; UNREBUTTED says "the attack lands as stated." The persona correctly distinguished these.
4. **Early-exit was triggered.** Stages 3-7 were skipped, saving ~6 min of wallclock and (more importantly) preventing the skill from manufacturing fake PASS verdicts on stages that no longer matter.
5. **Stage 8 cited the priority rule number (#1)** — auditability requirement from `rules/decision-logic.md §Auditability` was met.
6. **Resurrection-eligible = no** is the right call for exact duplicates. Resurrection only applies when new evidence (e.g., the user finds a non-obvious delta) could change the verdict; an exact prior-art paper is unrecoverable.
