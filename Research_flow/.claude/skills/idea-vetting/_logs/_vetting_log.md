---
name: vetting-log
description: Append-only log of every vetting session (one entry per batch or per single-idea re-vet)
append-only: true
load-trigger: Read at Step 1 (pre-vet) for context; appended at Step 6 (log)
---

# Vetting Log

Append-only. Never overwrite existing entries. New entries go AT THE BOTTOM under a `##` date header. Pre-vet reads this file to surface prior batches on the same benchmark.

## Entry format (one entry per batch or per single-idea re-vet)

```markdown
## <ISO 8601 datetime> — <Batch <N> vetting | Single-idea re-vet>
- **Benchmark**: <name>
- **Task / problem**: <concrete problem framing — inherited from source batch, or confirmed with user for pasted ideas>
- **Source**: <path to source batch file, OR "pasted single idea", OR "paper proposal">
- **Ideas vetted**: <N>
- **Verdicts**: <K> KILL, <R> REFRAME, <T> TOY, <F> FULL SEND
- **Time**: <X> min  (budget: 60 min for batch, 12 min for single)
- **Survival rate**: <X.X>% ((FULL+TOY)/N)
- **Top pick**: Idea <i> (<title>) — <FULL SEND / TOY (cheapest) / etc.>
- **Mode flags**: <e.g., --climb-mode --no-publish, or "default">
- **Notable**: <1-2 lines on the most-decisive finding (which stage killed which idea, etc.)>
- **Re-vet trigger**: <none, OR "after toys complete for ideas <list>", OR "after result of idea <i> available">
```

For single-idea re-vets (e.g., after toy results, or `--resurrect`), use header `## <datetime> — Single-idea re-vet (idea <i>)` and replace `Ideas vetted` with `Previous verdict → New verdict`.

<!-- entries appended below -->
