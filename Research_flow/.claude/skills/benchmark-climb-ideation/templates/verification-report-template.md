---
name: verification-report-template
description: Output format for the per-batch verification report
load-trigger: Emitted at end of Step 4 (Verification) in SKILL.md workflow
---

# Verification Report Template

Emit this report as a section inside the batch markdown (after `## Ranked ideas`), AND append a copy to `_logs/_rejection_log.md` (rejected entries only).

```markdown
## Verification Report — Batch <N>

| # | Title (short) | Novelty | Provenance | Feas | Gain (pp) | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|-----------|--------|------|--------|-------|
| 1 | <title>       | NOVEL ✅ | VERIFIED ✅ | 4/5 | +1.5 🟢 | OK ✅ | LOW | PASS | **KEEP** |
| 2 | <title>       | DUPLICATE ❌ | — | — | — | — | — | — | **REJECT** |
| 3 | <title>       | EXTENDS ✅ | VERIFIED ✅ | 3/5 | +0.8 🟡 | OK ✅ | MED | WARN | **KEEP (warn)** |
| 4 | <title>       | NOVEL ✅ | BROKEN_LINK ❌ | — | — | — | — | — | **REJECT** |
| 5 | <title>       | NOVEL ✅ | VERIFIED ✅ | 2/5 | +4.0 🔴 | SLOW ⚠️ | HIGH ⚠️ | PASS | **KEEP (flag)** |

## Counts
- Verified: <V>
- Rejected: <R> (Novelty: <a>, Provenance: <b>, Falsification: <c>, Compliance: <d>, Other: <e>)
- Downgraded: <D>
- Re-search cycles used: <0 / 1 / 2>
- Final batch size: <Y>

## Warnings (per idea)
- Idea 3: medium-risk integration with prior pipeline (downstream eval may need re-tuning)
- Idea 5: high compute risk — expected cost > 80% of declared budget; slow-falsify (>8h)

## Cross-idea consistency
- Near-duplicates collapsed: <none | list>
- Contradictions flagged: <none | list>
- Score-distribution: <healthy | over-confident — entire batch downgraded by one color>

## Rejection log entries (also appended to _logs/_rejection_log.md)

### Idea 2 — <title>
- Stage failed: **Novelty (Step 1)**
- Tag: `DUPLICATE`
- Evidence: <arXiv:XXXX.XXXXX> publishes the same technique on the same benchmark (2025-11).
- Action: removed from batch.

### Idea 4 — <title>
- Stage failed: **Provenance (Step 2)**
- Tag: `BROKEN_LINK`
- Evidence: cited primary `arXiv:2410.99999` does not resolve; author search returns no match.
- Action: removed from batch.

## Re-search summary (only if cycles > 0)
- Cycle 1: gap = `Tier 3 / Pattern P6`. Searched `<query>`. Picked: <paper>. New idea: <title>. Verification: KEEP.
- Cycle 2: <... or "not triggered">
```

## Rules for filling this template

- **Every** column in the table must use the controlled vocabulary from `../rules/verification.md`. No free-form verdicts.
- Use `—` for any check skipped due to early REJECT.
- The `Final` column may only be `KEEP` / `KEEP (warn)` / `KEEP (flag)` / `REJECT`.
- `Counts.Rejected` breakdown must sum to the total rejected.
- If `Re-search cycles used > 0` the `Re-search summary` section is required.
- Rejection log entries are required for EVERY `REJECT` row; the table alone is not enough.
