---
name: batch-template
description: Top-level wrapper for an ideation batch markdown
load-trigger: Step 6 of SKILL.md workflow
---

# Batch Template

Use this skeleton for `./ideation-output/<benchmark>/batch-<N>.md`. Replace every `<placeholder>`.

```markdown
# Idea Batch <N> — <BENCHMARK> / <TASK>
**Generated**: <ISO 8601 timestamp>
**Time-to-batch**: <Y> min
**Skill version**: 0.1.0
**Skill invocation**: <command the user typed>

## Inputs
- Benchmark: <name>
- Task / problem: <concrete problem framing being solved on the benchmark — 1-2 sentences naming inputs, outputs, and the evaluated capability>
- Existing pipeline: <path or 1-paragraph description of current components + current score, OR "none — greenfield batch">
- Batch scope: <enhance-existing / greenfield / mixed (≥ 50% enhance-existing)>  — must be consistent with the `Existing pipeline` line above
- Tier mix (configured): <a/b/c, e.g., 45/35/20 default, or 55/30/15 for pipeline-biased>
- Baseline: <model @ score on this task>
- Compute budget: <$ or hours>
- Time budget: <hours>
- Constraints: <list>

## Summary
| Metric | Value |
|--------|-------|
| Batch size | <N> |
| Tier 1 / 2 / 3 (counts) | <a> / <b> / <c> |
| Tier mix vs configured | <observed%> vs <configured%> (deviation ≤ 10pp per tier) |
| Scope mix | <K_enhance> enhance-existing / <K_green> greenfield (must be ≥ 50% enhance when a pipeline is supplied) |
| Patterns used | <P_, P_, … (K distinct)> |
| Distinct venues | <count> |
| Time windows | <<12mo (x), 12-36mo (y), >36mo (z)> |
| Avg feasibility | <m>/5 |
| Avg confidence | 🟢 <%>, 🟡 <%>, 🔴 <%> |

## Summary table
| # | Title | Pattern | Tier | Gain | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 1 | <title> | P_ | _ | +_.__ | _ | _ | _.__ |
| 2 | ... |

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea <X>: <title>** — Score: <s>
<1-2 sentences>

### ⚡ Quick win (lowest effort)
**Idea <Y>: <title>** — Effort: <S/M>
<1-2 sentences>

### 🛡️ Safe bet (highest confidence)
**Idea <Z>: <title>** — Confidence: 🟢
<1-2 sentences>

## Ranked ideas
<Insert each idea using ./idea-template.md, in ranked order>

## Verification report (basic — Phase 1)
| # | Title | Primary source? | Mechanism concrete? | Falsification? | Verdict |
|---|-------|-----------------|---------------------|----------------|---------|
| 1 | ... | ✅ | ✅ | ✅ | KEEP |
| ... |

Rejected: <K> — reason summaries here, or link to `_logs/_rejection_log.md` (Phase 2).

## Notes & warnings
- <Any tier-quota shortfalls, budget risks, missing pattern slots>

## Next steps for user
1. <Recommended first try>
2. <Recommended second>
3. <Hold-for-later>

## Provenance signature
SHA256 of (inputs + paper IDs + timestamp): <hash>
```

## Hard rules

- The `Summary` and `Summary table` rows MUST be present even if a batch is partial.
- The `Inputs` block MUST include `Benchmark`, `Task / problem`, `Existing pipeline` (with explicit "none" if not supplied), `Batch scope`, and `Tier mix (configured)`. Missing any of these invalidates the batch.
- When `Existing pipeline` is not "none", the `Scope mix` row MUST show ≥ 50% enhance-existing (rounded up). Greenfield ideas in a pipeline batch each need a 1-line justification.
- `Tier distribution` and `Patterns used` are mandatory — they enable later anti-bias audits.
- Do NOT inline the full text of source papers; cite by title + venue + arXiv ID only.
- If `Batch size < 5`, add a `⚠️ Under-quota` line at the top of `Notes & warnings` explaining which tier short-fell.
