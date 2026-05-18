---
name: per-idea-report-template
description: Full report format for vetting a single idea (wraps all 8 stage blocks + final decision)
load-trigger: Written at end of Step 3 (per-idea pipeline) — one file per idea
---

# Per-Idea Vetting Report Template

Each vetted idea produces one file at `vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md`. Use the skeleton below; every `<placeholder>` must be filled.

```markdown
# Vetting Report: <Idea Title>

**Source**: <batch file path> idea <N>
**Benchmark**: <name>
**Task / problem**: <concrete problem framing inherited from the source batch — must be present>
**Existing pipeline**: <description inherited from the batch header, or "none — greenfield batch">
**Idea scope**: <enhance-existing / greenfield — required when an Existing pipeline is present in the batch>
**Vetted**: <ISO 8601 datetime>
**Skill version**: 0.1.0
**Time-to-vet**: <X> min
**Mode flags**: <e.g., --climb-mode --no-publish, or "default">

## TL;DR

- **Verdict**: <KILL / REFRAME / TOY / FULL SEND> <🟢/🟡/🔴>
- **One-liner**: <why this verdict, in one sentence>

## Stage results

| Stage | Persona | Verdict | Notes |
|-------|---------|---------|-------|
| 1. Problem Framing | Advisor | ✅ PASS | <note> |
| 2. Prior Work Attack | Hunter | ⚠️ WARN | Close to Zhang et al. 2024 |
| 3. Novelty Decomp | Reviewer | ✅ PASS | Novel on Synthesis axis |
| 4. Theory Grounding | Theorist | ⚠️ WARN | Mechanism intuitive only |
| 5. Feasibility | PM | ⚠️ WARN | Cost tight |
| 6. Killer Baseline | Empiricist | ⚠️ WARN | Tool-use baseline close |
| 7. Reviewer Sim | R1/R2/R3 | Borderline | R3 weak-novelty concern |
| 8. Decision | PI | TOY | See toy design below |

## Per-stage details

<Insert each Stage block using ../templates/per-stage-output.md. Stages must appear in numerical order. Skipped stages must be marked explicitly with the reason.>

### Stage 1: Problem Framing
<full block>

### Stage 2: Prior Work Attack
<full block>

### Stage 3: Novelty Decomposition
<full block>

### Stage 4: Theory Grounding
<full block>

### Stage 5: Feasibility Analysis
<full block>

### Stage 6: Killer Baseline
<full block>

### Stage 7: Reviewer Simulation
<full block OR "Skipped: --climb-mode --no-publish">

### Stage 8: Decision Gate
<full block>

## Final decision

**Verdict**: <KILL / REFRAME / TOY / FULL SEND> <🟢/🟡/🔴>

**Rationale**: <2-4 sentences synthesizing stage results per ../rules/decision-logic.md>

**Branch-specific block** (fill only the one matching the verdict):

### If TOY → Toy experiment design
<see Stage 8 file for the template>

### If REFRAME → Reframed idea description
<1-2 paragraphs describing the reframed idea + which stage triggered the reframe>

### If KILL → Kill rationale
<2-3 sentences naming the killing stage(s) + the specific evidence (cited paper, baseline, cost number, etc.)>
<Also: append this idea to _logs/_killed_ideas.md>

### If FULL SEND → Priority rank
**Batch priority**: <integer>
**Reason for rank**: <1 sentence>
**Re-vet trigger**: <none, or "if result < +X.Xpp, re-vet with --given-result">

## Attacks summary

| # | Stage | Attack | Status |
|---|-------|--------|--------|
| 1 | 2 | "Isn't this just Zhang et al. 2024 ToT?" | ⚠️ WEAKENED (need delta argument) |
| 2 | 6 | "Tool-use baseline beats this" | ⚠️ WEAKENED (combine? ablate?) |
| 3 | 5 | "Cost > budget" | ⚠️ WEAKENED (toy resolves) |
| ... |

## User actions

Numbered list of concrete next steps for the user:
1. <action 1>
2. <action 2>
3. <action 3>

## Confidence

🟢 / 🟡 / 🔴 — <1-sentence rationale for the confidence tag>
```

## Hard rules

- Every section above is **required**. Stages 1-8 must all appear in the per-stage details (skipped stages are noted, not removed).
- The `Benchmark` and `Task / problem` header fields are mandatory; a vetting report without both is invalid (Stage 1 cannot be audited).
- The `Stage results` table must match the actual per-stage blocks below — no drift between the summary table and the detailed blocks.
- The `Final decision` verdict must match `Stage 8`'s verdict. If they differ, the report is invalid.
- The `Attacks summary` lists the attacks deemed most decisive (top 5-10 across all stages), not every attack issued.
