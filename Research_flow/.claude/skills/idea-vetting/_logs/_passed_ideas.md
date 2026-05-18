---
name: passed-ideas-log
description: Append-only log of every idea with verdict = FULL SEND, with vetting confidence + priority
append-only: true
load-trigger: Read at Step 1 (pre-vet) to track which ideas are queued for implementation; appended at Step 6 (log)
---

# Passed Ideas Log

Append-only. Tracks every FULL SEND verdict so the implementation queue is auditable across sessions. When a TOY graduates to FULL SEND after toy results, append a new entry tagged `(post-toy)` — do NOT modify the prior TOY entry in `_toy_queue.md`.

## Entry format (one entry per FULL SEND idea)

```markdown
## <ISO 8601 date>

### Batch <N> — <BENCHMARK> / <TASK>  (or "Single-idea re-vet" for solo re-vets)

#### Idea <i>: <title>
- **Task / problem**: <task framing this idea targeted — copied from the source batch>
- **Verdict**: ✅ FULL SEND (or "FULL SEND (post-toy)" if graduated from a prior TOY entry)
- **Confidence**: 🟢 / 🟡 / 🔴
- **Composite score** (from ideation): <S>
- **Expected gain (mid)**: +<G>pp
- **Cost estimate**: $<C>, <H>h wallclock
- **Priority rank within batch**: <integer>
- **Risk mitigation note**: <which Stage-N WARN, if any, warrants an early-warning check during implementation>
- **Source**: <vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md>
- **Status**: queued / in-progress / shipped / abandoned
```

Group by date then by batch.

<!-- entries appended below -->
