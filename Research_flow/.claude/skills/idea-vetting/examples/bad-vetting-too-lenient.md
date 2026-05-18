# BAD Vetting Example — Too Lenient (Annotated)

> ⚠️ **This is a teaching example.** It is what the skill should NEVER produce. Read the `## Issues identified` section at the bottom — every numbered issue references a specific line above.

# Vetting Report: "Smart retrieval-augmented reasoning for math"

**Source**: pasted single idea
**Vetted**: 2026-05-17T09:14:00Z
**Skill version**: 0.5.0
**Time-to-vet**: 3 min (suspicious — too fast)
**Mode flags**: default

## TL;DR

- **Verdict**: ✅ **FULL SEND** 🟢
- **One-liner**: Great idea! Retrieval should help with math reasoning.

## Stage results

| Stage | Persona | Verdict | Notes |
|-------|---------|---------|-------|
| 1. Problem Framing | Advisor | ✅ PASS 🟢 | Interesting problem. |
| 2. Prior Work Attack | Hunter | ✅ PASS 🟢 | Probably some prior work but ours is different. |
| 3. Novelty Decomp | Reviewer | ✅ PASS 🟢 | Novel combination. |
| 4. Theory Grounding | Theorist | ✅ PASS 🟢 | Reasonable mechanism. |
| 5. Feasibility | PM | ✅ PASS 🟢 | Should be feasible. |
| 6. Killer Baseline | Empiricist | ✅ PASS 🟢 | Probably no simple baseline does this. |
| 7. Reviewer Sim | R1/R2/R3 | ✅ PASS 🟢 | Reviewers will be enthusiastic. |
| 8. Decision | PI | FULL SEND 🟢 | All green. Ship it. |

## Per-stage details

### Stage 1: Problem Framing  *(line 30)*

**Persona**: Advisor.
*(no persona-declaration quote)*

- "Math reasoning is hard."
- "Retrieval could help."

**Attack 1**: "Seems incremental."
- Rebuttal: "Our approach combines retrieval and reasoning in a novel way that no one has explored deeply."
- Persona response: "Good point. ✅ DEFLECTED."

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.5 min.

### Stage 2: Prior Work Attack  *(line 47)*

**Persona**: Hunter.

*(no search log; no queries documented; no citations)*

**Attack 1**: "Maybe someone did this?"
- Rebuttal: "Our work is novel; we focus on math specifically."
- Persona response: "Sounds right. ✅ DEFLECTED."

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.3 min.

### Stage 3: Novelty Decomposition  *(line 63)*

**Persona**: Reviewer.

Novelty axes: "Application + Synthesis — clearly novel."

*(no axis-by-axis check; no rebranding check; no strip test)*

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.2 min.

### Stage 4: Theory Grounding  *(line 75)*

**Persona**: Theorist *(but voice doesn't match — see Issues §6)*.

- "Retrieval gives more context, more context usually helps. So this should work."

*(no view check; no counterexample regime)*

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.3 min.

### Stage 5: Feasibility  *(line 87)*

**Persona**: PM.

- Compute: "Should be cheap."
- Wallclock: "Few days."
- Significance: "Probably."

*(no numbers anywhere)*

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.3 min.

### Stage 6: Killer Baseline  *(line 100)*

**Persona**: Empiricist.

- "Self-consistency is a baseline but it's different from retrieval."
- "Tool-use is also different."

**Attack 1**: "What about kNN-retrieved exemplars baseline?"
- Rebuttal: "Our retrieval is smarter than kNN."
- Persona response: "Fair. ✅ DEFLECTED."

*(no pp estimates; no cost ratio; "smarter than kNN" not specified)*

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.4 min.

### Stage 7: Reviewer Simulation  *(line 116)*

- R1: 4/5 Accept ("Looks good.")
- R2: 4/5 Accept ("Solid empirics.")
- R3: 4/5 Accept ("Novel.")

*(no specific concerns; no critical-fixes list; uniform 4/5 across reviewers is a calibration smell)*

**Verdict**: ✅ PASS 🟢. **Time spent**: 0.5 min.

### Stage 8: Decision Gate  *(line 128)*

- All stages PASS. Verdict: ✅ FULL SEND 🟢.
- Confidence rationale: "All green. Ship it."

*(no priority-rule number cited; no risk-mitigation note)*

---

## Issues identified

This vetting is **invalid**. Every stage failed adversarial discipline. The skill defaulted to "helpful agreeable assistant" — exactly the failure mode `rules/adversarial-mindset.md` was written to prevent.

### Issue 1: No real adversarial work was done (line 23, "Time-to-vet 3 min")
Total time = 3 min across 8 stages = ~22 s/stage. Genuine adversarial vetting takes ≥ 8 min/idea, with Stage 2 alone needing 2-3 min for the web search. A 3-min "all PASS" run is the calibration smell from `adversarial-mindset.md §The over-confidence smell`.

### Issue 2: Stage 1 attack is vague (line 38, "Seems incremental")
Per `adversarial-mindset.md §4 Principles #2`, attacks must cite a specific paper / metric / mechanism. "Seems incremental" is exactly the forbidden vague form.

### Issue 3: Stage 1 rebuttal is non-substantive (line 39, "...in a novel way that no one has explored deeply")
This is hand-waving. Per `rules/rebuttal-loop.md §Steel-man rule`, the rebuttal must cite specific mechanism differences. "Novel way" is not an argument.

### Issue 4: Stage 2 ran NO search (line 49, "(no search log; no queries documented; no citations)")
The Hunter persona's defining behavior is "Runs ≥ 3 web queries before issuing the first attack." This stage produced zero queries. The PASS verdict is invalid by construction — you cannot conclude "no prior work" without searching.

### Issue 5: Stage 2 attack "Maybe someone did this?" is forbidden (line 52)
Hunter persona voice patterns are citation-grounded: "Isn't this just X? See arXiv:Y." Vague "maybe someone did this" violates the persona contract.

### Issue 6: Stage 4 persona drift (line 78, "Retrieval gives more context...")
The Theorist's voice patterns require views (inductive bias, optimization, probabilistic, etc.). "More context usually helps" is conversational, not theoretical. The persona was declared but not adopted in voice. Per `templates/per-stage-output.md` hard rules, `Persona declared` must be a direct quote and the stage's actual reasoning must match the persona's voice patterns.

### Issue 7: Stage 5 has no numbers (line 91, "Should be cheap / Few days / Probably")
The PM persona's defining trait is **numerical**. Per `personas/pragmatic-pm.md`: "Every concern comes with a concrete number. Vague answers fail." Three vague answers = stage is malformed.

### Issue 8: Stage 6 missed the killer baseline (line 102-104)
The Empiricist must list 3-5 baselines with **estimated pp gains** and **cost ratios** per Q-bank B1-B12 + C13-C15. This stage listed 2 baselines, said "different" (not a baseline analysis), and ignored Tool-use, kNN exemplars properly tuned, longer-context, larger-backbone, retrieval-with-reranker. Any of these could match a "smart retrieval" idea; none were estimated.

### Issue 9: Stage 6 "kNN" attack was rubber-stamped (line 109)
"Our retrieval is smarter than kNN" is not a rebuttal — it is a claim with no evidence. Per `rules/rebuttal-loop.md`, a weak steel-man should be marked UNREBUTTED. This skill marked it ✅ DEFLECTED — the exact agreeableness failure mode.

### Issue 10: Stage 7 uniform 4/5 across reviewers (line 118-120)
Three independent reviewers giving identical 4/5 scores with no specific concerns is statistically implausible. `decision-logic.md §Confidence tags` calls this an "over-confidence smell" that should DOWNGRADE batch confidence. The skill instead used it as evidence FOR a 🟢 verdict.

### Issue 11: Stage 7 has no critical-fixes list (line 122)
Per `stages/7-reviewer-simulation.md`, even an Accept review must surface **critical fixes that would flip Borderline → Accept**. Missing entirely.

### Issue 12: Stage 8 did not cite the priority rule (line 132)
Per `rules/decision-logic.md §Auditability`: "Every Stage 8 verdict must cite the rule number that fired." This Stage 8 says "All green. Ship it." with no rule number. Verdict is unauditable.

### Issue 13: No risk-mitigation note (line 132)
A FULL SEND verdict requires a risk-mitigation paragraph naming the early-warning experiment for any WARN stage. With zero WARNs across 8 stages and zero risk note, the report has no falsification commitment.

### Issue 14: No persona-declaration quotes (line 32, 49, 65, 77, 89, 102, 116)
Per `templates/per-stage-output.md`, `Persona declared` MUST be a direct quote of the persona-switch statement. None present. The audit trail is gone.

### Issue 15: No rebuttal-cycle summary anywhere
Every stage 1-7 must emit a `Rebuttal-cycle summary` (DEFLECTED / WEAKENED / UNREBUTTED counts). None present. This means the UNREBUTTED-downgrade rule from `decision-logic.md` could not be applied, and the verdicts may be silently inflated.

## What should have happened

1. The skill should have re-read `rules/adversarial-mindset.md §Anti-pattern → fix` at the start of every stage. A 3-min run for an 8-stage pipeline is itself the warning.
2. Stage 2 should have run ≥ 3 cited queries before declaring PASS. For "retrieval-augmented math reasoning", the obvious cousins are RAG-MATH (if such exists), kNN-CoT (Liu et al. 2021), Memory-Augmented LMs (Borgeaud et al. 2022, RETRO). None were searched.
3. Stage 6 should have produced a 5-row baselines table with pp estimates. kNN-CoT alone is a plausible killer: it is `P11 ICL variations` from the ideation skill's pattern catalog and has documented +1-2 pp on math benchmarks.
4. The skill should have **caught itself** during Stage 8 synthesis: 8/8 PASS + 🟢 + no rebuttal cycles is the textbook over-confidence smell. The correct response is to RE-RUN Stages 2 and 6 with explicit hostile prompting (per `adversarial-mindset.md §The over-confidence smell`), not to ship as FULL SEND.
5. Probable correct verdict (after proper vetting): **TOY** or **REFRAME** — "smart retrieval" is underspecified, and the kNN baseline likely matches the idea's claim within noise.

Reference correct patterns: [good-vetting-passed.md](./good-vetting-passed.md), [good-vetting-toy.md](./good-vetting-toy.md), [good-vetting-killed.md](./good-vetting-killed.md).
