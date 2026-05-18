---
name: toy-queue-log
description: Append-only log of every idea awaiting a toy experiment, sorted by cost ascending
append-only: true
load-trigger: Read at Step 1 (pre-vet) to surface pending toys; appended at Step 6 (log) for new TOY verdicts
---

# Toy Queue

Append-only across sessions. Within the `## Active` section, maintain **cost-ascending order** when appending — the cheapest toy is always at the top so the user sees the fastest signal first. When a toy completes (user runs it and reports results), MOVE the entry to `## Completed` with the outcome; do NOT delete it from `## Active` — instead, mark `Status: completed` and let the migrate happen at the next session's pre-vet load.

(Append-only means the file is never overwritten; physical line removal is prohibited. The "move" is achieved by appending a new entry under `## Completed` and updating only the `Status` field of the active entry. If strict append-only is required, leave the active entry in place with `Status: completed (see Completed section)`.)

## Active

### Entry format (one entry per TOY-verdict idea)

```markdown
### Idea <i>: <title>  [Batch <N>, <BENCHMARK> / <TASK>]
- **Task / problem**: <task framing this idea targets — copied from the source batch>
- **Added**: <ISO date>
- **Toy budget**: $<C>, <H>h wallclock
- **Toy criterion**: ≥ <P>% of expected gain on <N>-problem subset (e.g., ≥ 30% of +1.5pp = ≥ +0.45pp)
- **Resolves uncertainty about**: <which Stage-N WARN this toy is designed to settle>
- **Source**: <vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md>
- **Status**: pending user execution
```

Maintain entries sorted by `Toy budget` (dollars) ascending. When two entries tie on dollars, sort by wallclock ascending.

## Completed

### Entry format (appended when user reports toy results)

```markdown
### Idea <i>: <title>  [completed <ISO date>]
- **Toy result**: <observed gain in pp, with seed count and significance check>
- **vs criterion**: <met / partially met / failed>
- **Outcome**: graduated to FULL SEND  /  one more toy round  /  FALSIFIED → KILL
- **Re-vet report**: <path to vetting-v2.md if a re-vet was run>
```

<!-- entries appended below -->
