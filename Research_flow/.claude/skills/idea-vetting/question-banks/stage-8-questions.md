---
name: stage-8-questions
description: Question bank for Stage 8 — Decision Gate (PI / Advisor persona)
load-trigger: Loaded at start of Stage 8 execution
---

# Stage 8 Question Bank — Decision Gate

Synthesize Stages 1-7 into one verdict. Cite the priority-rule number from `../rules/decision-logic.md` that fired.

## Mandatory: synthesis (must answer all 5)

1. **M1.** PASS / WARN / FAIL count across Stages 1-7.
2. **M2.** Critical-stage results: Stage 2 verdict? Stage 6 verdict? Stage 5 verdict?
3. **M3.** Auto-KILL triggers: did any of these fire?
   - Stage 1 = FAIL (Rule context — early exit)
   - Stage 2 = FAIL hard duplicate (Rule #1)
   - Stage 6 = FAIL no reframe (Rule #2)
   - ≥ 3 stages = FAIL (Rule #3)
4. **M4.** Priority-rule applied: state the rule number from `../rules/decision-logic.md §Priority rules`.
5. **M5.** Verdict: KILL / REFRAME / TOY / FULL SEND.

## Mandatory: confidence (must answer both)

6. **C6.** Confidence: 🟢 / 🟡 / 🔴, with the trigger from `decision-logic.md §Confidence tags` (e.g., "🟢 — Rule #4 fired, all 7 stages PASS, Stages 2 and 6 both PASS").
7. **C7.** Rationale: 2-4 sentence synthesis citing specific stage results (not generic).

## If verdict = TOY (answer all 4)

8. **T8.** Toy dataset: name the subset (e.g., 50 problems from MATH-500).
9. **T9.** Toy config: reduced K / N / seeds / configs — state numbers.
10. **T10.** Success criterion: what fraction of expected full gain must appear for the toy to escalate? (Typically ≥ 30%.)
11. **T11.** Toy cost + wallclock: dollar and hour estimate.

## If verdict = REFRAME (answer all 3)

12. **F12.** Reframed problem statement: 1-2 sentences naming what changed (scope / axis / mechanism).
13. **F13.** Reframed mechanism: how does the new framing avoid the failing stage's attack?
14. **F14.** Re-vet trigger: under what condition does the reframed idea re-enter the pipeline? (E.g., "after combining with Tool-use baseline and showing super-additivity on a 50-problem toy".)

## If verdict = KILL (answer all 2)

15. **K15.** Kill reason: specific — name the killing stage, the killing attack, and the evidence (paper / baseline / cost number).
16. **K16.** Salvageable parts: any component, mechanism, or paper-insight worth keeping for the next idea iteration?

## If verdict = FULL SEND (answer all 3)

17. **U17.** Priority rank within the batch (integer).
18. **U18.** Suggested implementation order: which knob / experiment is run first?
19. **U19.** Risk mitigation: which Stage-N WARN (if any) needs an early-warning experiment to catch failure cheaply?

## Coverage record

`Questions covered: M1..M5, C6, C7, plus branch-specific (T8..T11 OR F12..F14 OR K15..K16 OR U17..U19)`. Stage 8 cannot pass without M1-M5, C6, C7, AND all branch-specific questions for the chosen verdict.
