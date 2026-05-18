---
name: time-window
description: Recency vs. classics balance — per-window minimum counts and warning rules
load-trigger: Step 2 (search) and Step 3 (drafting) and Step 6 (delivery audit)
---

# Time Window Rules

A batch must span multiple time windows. Pure-recency batches over-index on hype; pure-classics batches miss real recent advances.

## Time windows (relative to current date)

| Window | Definition |
|--------|------------|
| `<12mo` | Published within the last 12 months |
| `12-36mo` | Published 12–36 months ago |
| `36-72mo` | Published 36–72 months (3-6 years) ago |
| `72+mo` | Published > 6 years ago (classics) |

## Per-window minimum counts (for a batch of 5-10)

| Window | Minimum ideas |
|--------|---------------|
| `<12mo` | ≥ 2 |
| `12-36mo` | ≥ 2 |
| `36-72mo` | ≥ 1 |
| `72+mo` | 0-2 (optional — typically Tier-3 classics) |

These are minimums on the **primary paper** of each idea. Supporting/contrasting citations do not count toward the quota but should reflect a similar spread.

## Warning rules

- If batch has **0 papers > 24 months** → flag `⚠️ may over-index on recency` and downgrade overall confidence by one color.
- If batch has **0 papers < 12 months** → flag `⚠️ may miss recent advances` and downgrade overall confidence by one color.
- If batch has **< 3 distinct windows represented** → see `./anti-bias.md §Time diversity` — counts as a hard anti-bias failure.

## Classics — special handling

Papers > 5 years old are valid Tier-3 inspirations for foundational concepts. Examples that have stayed relevant: dropout, batch normalization, attention, beam search, MCTS, EM, importance sampling, Metropolis-Hastings, A*.

- Skip the venue check for classics — community acceptance is implied (see `./conference-tiers.md §Old papers`).
- Tag classics explicitly in the idea: `[T3 — classic, <year>]`.

## Cite-by-version rule

For recent papers (< 6 months on arXiv):
- Prefer v2 / v3 over v1 if available (post-revision text is usually cleaner).
- Always note the version number in the citation: `arXiv:2410.XXXXX v2`.
- If only v1 exists and the paper has not been peer-reviewed, treat the source as Tier-3 trust (see `./source-trust.md`).
