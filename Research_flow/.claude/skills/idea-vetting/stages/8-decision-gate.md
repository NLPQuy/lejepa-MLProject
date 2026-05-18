---
name: stage-8-decision-gate
description: Final verdict based on all prior stage results
load-trigger: Step 3 of SKILL.md, last stage (always runs)
persona: advisor (PI mode)
---

# Stage 8: Decision Gate

**Persona**: Senior PI making the final call — see [../personas/advisor.md](../personas/advisor.md). Declare on entry:
> "Adopting persona: PI / Advisor. Stance: synthesize the evidence, commit to a verdict."

**Goal**: Synthesize Stages 1-7 → assign exactly one of `KILL` / `REFRAME` / `TOY` / `FULL SEND` with a confidence tag.

**Stage 8 does NOT issue its own attacks** — it has no rebuttal loop. Instead, it reads each prior stage's **already-downgraded verdict** (the UNREBUTTED-downgrade rule in [../rules/decision-logic.md](../rules/decision-logic.md) is applied at the prior stage's emit time, not here). If any Stage 1-7 block shows a "PASS" verdict alongside ≥ 1 UNREBUTTED attack, that block is malformed — flag it and either re-run that stage or apply the downgrade before synthesis.

**Time budget**: 1-2 min.

## Procedure

**Before executing**: load [../question-banks/stage-8-questions.md](../question-banks/stage-8-questions.md). The Q-bank defines M1-M5 (synthesis), C6-C7 (confidence + rationale), and branch-specific T8-T11 / F12-F14 / K15-K16 / U17-U19. Stage 8 cannot pass without M1-M5 + C6 + C7 + all branch-specific questions for the chosen verdict. Record coverage IDs in the per-stage output.

1. Recap stage results in a single table (M1, M2).
2. Apply priority rules from [../rules/decision-logic.md](../rules/decision-logic.md) — answer M3 (auto-KILL triggers) and M4 (rule number that fired) and M5 (verdict).
3. Assign confidence per C6 + write rationale per C7.
4. Branch on verdict:
   - `KILL` → answer K15-K16; append idea + reasoning to `_logs/_killed_ideas.md`.
   - `REFRAME` → answer F12-F14; write the reframed idea description (1-2 paragraphs).
   - `TOY` → answer T8-T11; produce the toy experiment design (template below).
   - `FULL SEND` → answer U17-U19; assign priority rank within the batch.

## Decision options

### A) KILL
The idea is rejected. Log it.

Trigger conditions (any one):
- ≥ 2 stages FAIL.
- Stage 6 (killer baseline) FAIL with no plausible reframe.
- Stage 2 (prior work) FAIL with a hard duplicate.
- Stage 5 (feasibility) FAIL with cost > budget × 3.

### B) REFRAME
The core insight is valid but the framing or scope is wrong. Output a reframed idea description.

Trigger conditions:
- Stage 3 PASS but the claimed novelty axis is wrong.
- Stage 7 reviewers said "interesting but wrong framing."
- User constraints suggest a different angle.

### C) TOY EXPERIMENT FIRST
Uncertain. Run a small proof-of-concept before committing.

Trigger conditions:
- Mixed signals (1-2 FAIL, others PASS / WARN).
- Stage 4 (theory) WARN combined with Stage 6 (baseline) WARN.
- Feasibility OK for a toy but risky for full.

### D) FULL SEND
Idea passed. Proceed to full implementation.

Trigger conditions:
- All 8 stages PASS, or at most 1-2 WARN.
- Stage 6 PASS.
- Stage 2 PASS.
- Stage 5 PASS.

## Toy experiment design template (use when verdict = TOY)

```markdown
### Toy Experiment Design

**Goal**: Validate the core mechanism cheaply.

**Setup**:
- Dataset subset: <e.g., 50 problems from MATH-500>
- Model: <same as user's target>
- Config: <minimum — e.g., K=5 instead of K=100>
- Budget: <e.g., $10 instead of $100>
- Wallclock: <e.g., 1 hour>

**Success criterion**:
- If toy shows ≥ <X>% of expected gain → proceed to FULL.
- If toy shows < <X>% → KILL or reframe further.

**Confound check**:
- Variance on toy: estimate from 3 seeds.
- If variance > 50% of expected gain → toy is too small; need bigger toy.

**Falsification**:
- If toy gain ≤ baseline noise → FALSIFY (kill the idea).
- If toy gain > noise but < target → 1 more toy round at higher K.
- If toy gain ≥ target → proceed to FULL.

**Estimated wallclock + cost for toy**: <X> hours, <$Y>.
```

## Output

Write the **Final decision** section of the per-idea report (see `../templates/per-idea-report.md`).
Include:
- Stage results recap table
- Verdict + 🟢🟡🔴 confidence
- Rationale paragraph
- Branch-specific block (Toy design / Reframe description / Kill rationale / Full-send priority)
- `Re-vet trigger` line (e.g., "After toy results, re-run `/vet-ideas --given-toy <link>`")
