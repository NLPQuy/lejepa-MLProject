---
name: stage-1-questions
description: Question bank for Stage 1 — Problem Framing (Advisor persona)
load-trigger: Loaded at start of Stage 1 execution
---

# Stage 1 Question Bank — Problem Framing

Use the numbered IDs (`M1`, `R6`, `P11`, …) when recording coverage in the per-stage output.

## Mandatory (must answer all 5)

1. **M1.** State the problem in 1 sentence. (Plain language, no jargon.)
2. **M2.** Why is this hard? List ≥ 2 specific reasons (mechanism / data / scale / theory).
3. **M3.** How exactly does current SOTA fail? Cite a concrete failure case (example input + wrong output).
4. **M4.** Real problem or benchmark artifact? Name the evidence — does the failure mode appear in non-benchmark settings?
5. **M5.** Would scaling the baseline solve it? (E.g., GPT-4 instead of gpt-4o-mini, or 10× data.) Estimate the gain a scaled baseline would give.

## Recommended (answer ≥ 3 of these)

6. **R6.** Which stakeholder cares (researcher / industry / end user)? Name them.
7. **R7.** If solved, what downstream task improves? Quantify if possible.
8. **R8.** What existing counterfactual solutions are in use? Why are they insufficient?
9. **R9.** Is the problem implicitly solved in an adjacent field (e.g., math problem solved via code synthesis)?
10. **R10.** List 2-3 concrete failure cases of the baseline (specific inputs that fail).

## Probing (if Stage 1 looks borderline)

11. **P11.** Has a prior survey paper addressed this exact problem? Cite it if so.
12. **P12.** Is this listed as a known open problem in any community venue (workshop CFP, position paper)? Cite mention.
13. **P13.** Could this be solved by data engineering (cleaning, augmentation, better label quality) instead of a new method?
14. **P14.** Does the problem generalize beyond this single benchmark, or does it dissolve once you change the eval set?
15. **P15.** Has the baseline's claimed performance been independently reproduced? (If not, the "failure" may be artifact of the baseline being optimistic.)

## Coverage record

In the per-stage output, list the IDs of questions answered, e.g., `Questions covered: M1, M2, M3, M4, M5, R7, R8, P12 (8/15)`. A Stage-1 output with fewer than 5 mandatory answers is incomplete.
