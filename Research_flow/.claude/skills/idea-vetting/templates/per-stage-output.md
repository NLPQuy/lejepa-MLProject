---
name: per-stage-output-template
description: Block format used by every stage's output
load-trigger: Each stage writes one block in this format
---

# Per-Stage Output Block

Use this format for each Stage's section inside the per-idea report. Replace every `<placeholder>` — do not leave any blank.

```markdown
### Stage <N>: <stage name>

**Persona**: <persona slug> (see ../personas/<slug>.md)
**Persona declared**: "Adopting persona: <name>. Stance: <one-line>."

**Questions covered**: <count> / <total in Q-bank, or "n/a" until Phase V2>

**Attacks issued**: <count, must be ≥ 1>; **with full rebuttal cycle**: <count, max 3 per stage>

For the first 3 attacks, use the full rebuttal block per [../templates/rebuttal-format.md](../templates/rebuttal-format.md). Each block includes: Attack text, Steel-manned rebuttal (Round 1), Source (auto-steelman or user), Persona response (Round 1), Status after Round 1, OPTIONAL Round 2, and Final status.

**Attack 1**: <full rebuttal block per rebuttal-format.md>

**Attack 2**: <full rebuttal block>

**Attack 3**: <full rebuttal block>

**Additional attacks** (beyond #3 — list with no rebuttal cycle):
- `Additional attack: "<text>" — Status: ✅/⚠️/❌, no rebuttal cycle (budget exhausted).`
- ...

**Rebuttal-cycle summary**:
- DEFLECTED: <count>
- WEAKENED: <count>
- UNREBUTTED: <count>  ← drives the UNREBUTTED-downgrade rule in `../rules/decision-logic.md`

**Stage verdict**: ✅ PASS / ⚠️ WARN / ❌ FAIL

**Confidence**: 🟢 / 🟡 / 🔴

**Time spent**: <X> min

**Notes for Stage 8**: <1-2 bullets the Decision-Gate persona should consider when synthesizing>
```

## Hard rules

- Every Stage block MUST issue ≥ 1 attack **with a full rebuttal cycle** — a stage with 0 attacks (or 0 rebuttal cycles) is incomplete (see Quality Gates in `../SKILL.md`).
- Status vocabulary is fixed: `DEFLECTED` (rebuttal holds, attack misses), `WEAKENED` (attack partially lands, idea needs adjustment), `UNREBUTTED` (no plausible defense — attack lands fully).
- Stage verdict vocabulary is fixed: `PASS` / `WARN` / `FAIL`. No free-form verdicts.
- Confidence is required even when verdict = PASS — a 🔴-confidence PASS still counts as a PASS for Stage 8 priority rules but flags an audit note.
- `Persona declared` MUST be a direct quote of the persona-switch statement, not a paraphrase. This is the audit trail that the persona was actually adopted.
- Rebuttal cycles cap at Round 2 (see `../rules/rebuttal-loop.md §Budget`). A block showing Round 3 is invalid; re-run the stage.
- `Rebuttal-cycle summary` counts must equal the number of full rebuttal blocks above — drift means the block is corrupted.
- Stage verdict MUST account for the UNREBUTTED count via `../rules/decision-logic.md §UNREBUTTED downgrade rule`. A "PASS" stage with ≥ 1 UNREBUTTED attack is invalid — must be at least WARN.
