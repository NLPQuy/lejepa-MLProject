---
name: idea-template
description: Per-idea markdown structure for benchmark-climb ideation batches
load-trigger: Step 3 of SKILL.md workflow
---

# Idea Template

Copy the block below for each idea in a batch. Replace every `<placeholder>` — do not leave any blank.

```markdown
### Idea <N>: <Short title — 5-10 words>

- **Pattern**: <P1-P12 from patterns/pattern-catalog.md>
- **Tier**: <1 / 2 / 3>
- **Target task**: <1-line restatement of the batch-level task this idea targets — must match the `Task / problem` in the batch header. If this idea narrows the task (e.g., to a subset like geometry-only problems on MATH-500), say so explicitly.>
- **Scope**: <enhance-existing / greenfield> — required when an Existing pipeline is supplied in the batch header; omit otherwise. If `enhance-existing`: name the pipeline component(s) modified and what stays unchanged. If `greenfield`: 1 sentence justifying why a redesign beats a component swap.
- **One-liner**: <1 sentence — what & why>

**Mechanism**:
<2-4 sentences. Concretely: input → process → output. No vague verbs like "improve" or "leverage".>

**Source inspirations**:
- Primary: <Paper title>, <Authors>, <Venue Year> [arXiv:XXXX.XXXXX]
- Supporting: <Paper title>, <Venue Year> [link]
- (Optional) Contrasting: <Paper title> [link]

**Why expected to improve**:
<2-3 sentences. Bridge from the source paper's result to the target benchmark. Name the mechanism that transfers.>

**Expected gain**: <+X.X / +Y.Y / +Z.Z pp> 🟢🟡🔴 (low / med / high estimate, confidence color)
**Feasibility**: <1-5> 🟢🟡🔴
**Effort**: <S / M / L / XL / XXL> 🟢🟡🔴

**Implementation sketch**:
1. <step 1>
2. <step 2>
3. <step 3>

**Risks**:
- <risk 1 — what could break>
- <risk 2 — what would invalidate the gain>

**Falsification test**: <If we run <X> and observe <Y>, the idea fails. Y must be observable, not vibe-based.>

**Adjacent / Cross-domain notes** (only if Tier 3):
- Original domain: <D1>
- Target domain: <D2>
- Adaptation needed: <list>
```

## Filled example (excerpt — for reference)

```markdown
### Idea 5: MCTS-guided reasoning with execution verifier

- **Pattern**: P2 (Transfer from game AI)
- **Tier**: 3
- **One-liner**: Use MCTS to expand reasoning traces with code-execution as the reward signal.

**Mechanism**:
For each math problem: generate K root traces with CoT; expand each via MCTS/UCT;
at every node attempt to express the step as Python; execute and use the result
(1.0 / 0 / -0.5) as the leaf reward; return the trace with highest backed-up score.

**Source inspirations**:
- Primary: "MCTS for Code Generation", Zhang et al., NeurIPS 2024 [arXiv:2410.XXXXX]
- Supporting: "Process Reward Models", Lightman et al., ICLR 2024 [arXiv:2305.20050]

**Expected gain**: +1.5 / +4.0 / +6.0 pp 🟡
**Feasibility**: 3/5 🟢
**Effort**: L 🟢

**Falsification test**: Run on 100 sampled MATH-500 problems with K=3, N=20 expansions.
If accuracy ≤ baseline self-consistency (~71.5%), the idea fails.
```

## Hard rules

- Every field is **required** except `Contrasting`, the `Adjacent` block (only for Tier 3), and `Scope` (only when an Existing pipeline is supplied — then mandatory).
- `Target task` must be consistent with the batch-level `Task / problem`. An idea whose target task drifts from the batch task is REJECTed at Step 4 (verification).
- When `Scope: enhance-existing`, the `Mechanism` and `Implementation sketch` MUST reference at least one component name from the supplied pipeline. If they describe a wholly new pipeline instead, the scope tag is wrong — either re-tag as `greenfield` (with justification) or re-cast the idea.
- `Mechanism` must name concrete operations. If you cannot fill it in 4 sentences, the idea is not ready.
- `Falsification test` must be a runnable check with a numeric threshold.
- Do NOT invent arXiv IDs. If the ID is not verified by a real search, mark `[arXiv:UNVERIFIED]` and the idea will be rejected at Step 4.
