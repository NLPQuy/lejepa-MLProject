---
name: killed-ideas-log
description: Append-only log of every idea with verdict = KILL, with stage + reason + evidence
append-only: true
load-trigger: Read at Step 1 (pre-vet) to avoid re-attacking already-rejected angles; appended at Step 6 (log)
---

# Killed Ideas Log

Append-only. Pre-vet reads this file to filter out attack angles already exhausted on prior batches for the same benchmark. Resurrection is allowed via `/vet-ideas --resurrect idea-<i> --counter-argument "<text>"` (per `../rules/decision-logic.md §Decision irreversibility & resurrection`).

## Entry format (one entry per KILLed idea)

```markdown
## <ISO 8601 date>

### Batch <N> — <BENCHMARK> / <TASK>

#### Idea <i>: <title>
- **Task / problem**: <task framing this idea targeted — copied from the source batch>
- **Killed at**: Stage <K> (<stage name>)
- **Killing attack**: "<the specific attack that landed UNREBUTTED>"
- **Evidence**: <cited paper / numeric baseline / cost number — be specific, not vague>
- **Salvageable**: <any component, mechanism, or paper-insight worth keeping for next iteration — or "none">
- **Confidence**: 🟢 / 🟡 / 🔴
- **Source**: <vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md>
- **Resurrection eligible**: yes / no
  - If yes: list what new evidence would justify resurrection (e.g., "if user provides ablation showing combined version super-additive").
  - If no: explain (e.g., "exact duplicate; no counter-argument can change reality").
```

Group entries by date (`## <date>`) then by batch (`### Batch <N> — <BENCHMARK> / <TASK>`).

<!-- entries appended below -->
