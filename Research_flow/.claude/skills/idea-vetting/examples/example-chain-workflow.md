# Chain Workflow Example — Ideation → Vetting → Pick → Implement → Re-vet

> 📘 **Reference example: end-to-end chain across the two skills.** Demonstrates how `benchmark-climb-ideation` and `idea-vetting` compose without tight coupling. The vetting skill never modifies ideation files; the ideation skill never reads vetting internals — they communicate by file contract only.

## T0 — User starts

```
$ cd ~/my-research-project
$ ls
ideation-output/   _logs/   ...
```

## T1 — Ideation

```
User: /propose-benchmark-ideas MATH-500
```

Ideation skill asks for baseline / budget / constraints, runs multi-tier search (15 queries, 12 min wallclock), drafts 7 ideas, verifies citations, writes:

```
ideation-output/MATH-500/batch-1.md          (the batch)
ideation-output/MATH-500/_logs/_search_log.md
ideation-output/MATH-500/_logs/_proposal_log.md
ideation-output/MATH-500/_logs/_rejection_log.md
```

Format of `batch-1.md` is the structured markdown produced by the `benchmark-climb-ideation` skill (H1 batch header, `## Summary table`, `## Ranked ideas` with `### Idea N:` blocks). The vetting skill's parser depends on this format — see `SKILL.md §Step 2 Input type A`.

Chat summary printed:
> ✅ Batch 1: 7 ideas for MATH-500. Top recs: Idea 1 (SC K=100), Idea 7 (subtype-routing), Idea 5 (MCTS + exec). Distribution T1/T2/T3 = 3/2/2; patterns P2, P4, P5, P6, P8, P11.

## T2 — User reads the batch

User reviews `ideation-output/MATH-500/batch-1.md`. Decides not to commit $300 to all 7 — wants vetting first.

## T3 — Vetting

```
User: /vet-ideas ideation-output/MATH-500/batch-1.md
```

Vetting skill (per [../SKILL.md](../SKILL.md) Step 2 Input type A):

1. **Reads** `ideation-output/MATH-500/batch-1.md` and parses 7 ideas via the §13.1 schema.
2. **Reads** the 3 ideation log files for context (avoid re-attacking already-rejected angles).
3. **Loads** its own 4 logs (per [`pre-vet.md`](../checklists/pre-vet.md)) — surface prior vetting work.
4. For each idea, runs the 8-stage pipeline with rebuttal cycles ([../rules/rebuttal-loop.md](../rules/rebuttal-loop.md)).
5. **Writes** per-idea reports to `vetting-output/MATH-500/batch-1/idea-<i>-vetting.md` and aggregates to `batch-summary.md`.
6. **Appends** entries to the 4 vetting logs.

## T4 — Vetting outputs (52 min wallclock)

Files created:

```
vetting-output/MATH-500/batch-1/
├── idea-1-vetting.md   ← KILL  (see examples/good-vetting-killed.md — SC K=100 duplicate)
├── idea-2-vetting.md   ← TOY
├── idea-3-vetting.md   ← REFRAME
├── idea-4-vetting.md   ← KILL (Stage 1 — problem dissolves: "use larger model")
├── idea-5-vetting.md   ← TOY  (see examples/good-vetting-toy.md — MCTS+exec)
├── idea-6-vetting.md   ← TOY
├── idea-7-vetting.md   ← FULL SEND (see examples/good-vetting-passed.md — subtype-routing)
└── batch-summary.md

vetting-output/MATH-500/_logs/_vetting_log.md   (+1 entry)
vetting-output/MATH-500/_logs/_killed_ideas.md  (+2 entries: ideas 1, 4)
vetting-output/MATH-500/_logs/_passed_ideas.md  (+1 entry: idea 7)
vetting-output/MATH-500/_logs/_toy_queue.md     (+3 entries: ideas 6, 2, 5 — cost-sorted ascending: $3, $5, $10)
```

Chat summary:
> Batch 1 vetting: 2 KILL, 1 REFRAME, 3 TOY, 1 FULL — survival 57 %. Top pick: Idea 7 (subtype-routing) — FULL SEND 🟢, $25/4h. Parallel toy queue: Idea 6 ($3), Idea 2 ($5), Idea 5 ($10), total $18/3h.

## T5 — User reads summary

User reads `batch-summary.md`. The 3 top-recommendation cards span 3 axes per `rules/decision-logic.md §Diversification`:

- 🥇 **Top FULL SEND**: Idea 7 (subtype-routing, $25, +1.8 pp 🟢)
- ⚡ **Fastest to validate**: Idea 6 (kNN exemplars toy, $3, 0.5 h)
- 🎯 **Highest EV**: Idea 5 (MCTS+exec, +4 pp potential after toy)

## T6 — User picks and implements

User implements Idea 7 (Top FULL SEND). Concurrently runs the cheap toy for Idea 6 ($3, 0.5 h).

## T7 — Results land

A week later: Idea 7 shipped, got +2.1 pp. Idea 6 toy showed +0.4 pp (above the +0.3 pp criterion).

## T8 — Re-vet with results

```
User: /vet-ideas --given-toy ./idea-6-toy-results.md idea-6
```

Vetting re-runs Stages 4, 5, 6 with the new evidence. Idea 6 graduates: TOY → FULL SEND. Output: `vetting-output/MATH-500/batch-1/idea-6/vetting-v2.md`. The `_passed_ideas.md` log gets a new entry tagged `(post-toy)`; `_toy_queue.md §Active` entry for Idea 6 is marked `Status: completed`.

## T9 — Feed back to ideation for next round

```
User: /propose-benchmark-ideas MATH-500 --given-vetting vetting-output/MATH-500/batch-1/batch-summary.md
```

The ideation skill (next batch) reads the vetting summary and:
- Avoids the patterns that killed (P4 scaling-only, P1 "use larger model"-style).
- Down-weights patterns close to TOY killers (Tool-use already explored heavily).
- Up-weights the synthesis patterns that survived (subtype-routing variants, novel cross-domain).

The ideation skill's `--given-vetting` flag is the read-side of the contract. Vetting itself does not call ideation — the user does.

---

## Loose-coupling verification

| Direction | Mechanism | Coupling level |
|-----------|-----------|----------------|
| Ideation → Vetting | File: `ideation-output/<bench>/batch-<N>.md` | **File contract only** (§13.1 schema). Vetting parses; never writes back. |
| Vetting → Ideation | File: `vetting-output/<bench>/batch-<N>/batch-summary.md` | **File contract only.** Read by ideation when user passes `--given-vetting`. |
| Either skill removed | The other still works on standalone inputs (paper proposals, pasted ideas) | **No tight coupling.** |

## What this example does NOT show

- **Batch 2** (the next ideation round informed by vetting). Outside this example's scope; the contract above is sufficient to construct it.
- **Resurrection workflow** (`/vet-ideas --resurrect`). Covered in [`good-vetting-killed.md`](./good-vetting-killed.md) and [`../rules/decision-logic.md §Resurrection`](../rules/decision-logic.md).
- **Cross-skill log file** (`cross-skill-log.md` at project root). Optional; appended if present.
