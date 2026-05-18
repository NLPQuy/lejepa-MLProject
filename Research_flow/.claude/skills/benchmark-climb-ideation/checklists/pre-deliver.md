---
name: pre-deliver-checklist
description: Final audit before printing the batch summary to the user
load-trigger: Between Step 6 (ranking) and Step 7 (user-facing summary) of SKILL.md
---

# Pre-Deliver Checklist

This is the LAST gate before the user sees the batch. Mirror of the Quality-gates block in `SKILL.md` — re-check it independently here.

## Batch shape
- [ ] Batch size between 5 and 10
- [ ] Search-tier distribution matches the **configured tier mix** ±10pp per tier (default `45/35/20`; user `--tier-mix` overrides). The `Inputs` block of the batch records the configured mix — audit against that, not the legacy defaults.
- [ ] If any tier band violated AND re-search budget exhausted → `⚠️` warning surfaced
- [ ] If `Existing pipeline` is present in the batch header: ≥ 50% of ideas (rounded up) have `Scope: enhance-existing`; remaining greenfield ideas carry a 1-line justification for redesign. Otherwise → `⚠️` warning.

## Diversity (count-based)
- [ ] ≥ 5 distinct patterns (P1–P12) used; ≤ 2 ideas per pattern
- [ ] ≥ 3 distinct technique families (mechanism-level)
- [ ] ≥ 3 distinct venues across primary papers
- [ ] ≤ 2 ideas from same first-author institution
- [ ] ≥ 3 distinct time windows represented (per `../rules/time-window.md` minimums)
- [ ] ≥ 60% of primary papers from Tier 1+2 trust sources

## Per-idea evidence
- [ ] Every idea has ≥ 1 primary paper VERIFIED (resolvable arXiv/DOI link)
- [ ] Every idea has a sharp falsification test (observable + numeric threshold)
- [ ] Every idea passed the 7-step verification pipeline
- [ ] Top-3 recommendations identified: Quick win / Big bet / Safe bet

## Tier-3 honesty audit (hard)

For **every idea tagged Tier 3**:
- [ ] Idea card contains a `Cross-domain transfer:` line naming `<source field>` → `<target use>`.
- [ ] The **primary paper's venue is NOT on the in-field venue list** (`../rules/conference-tiers.md`) for this benchmark's home field. Vision-SSL benchmarks: primary cannot be NeurIPS/ICML/ICLR/CVPR/ICCV/ECCV/TMLR vision-or-SSL paper. If primary is in-field, the idea is **mis-tagged** — either re-tag T1/T2 (and re-audit tier quota) or drop and re-search T3.
- [ ] The transferred mechanism is a **named principle/algorithm/theorem from the source field**, not a generic ML technique. SWA, dropout, mixup, label smoothing, Optuna/ASHA, EMA, generic distillation — **not T3** (mainstream-ML, see `search-strategy.md §What does NOT count as Tier 3`).
- [ ] Search log shows ≥ 1 query specifically targeting the **source field venue or terminology** for this idea (e.g., `"<technique> Annals of Statistics"`, not `"<technique> deep learning"`). Generic ML queries returning the same paper do not satisfy the T3 search obligation.

If any T3 idea fails the audit → re-tag down (T2 or T1) and **re-check the tier-mix band**. If the re-tag breaks the configured band, surface `⚠️ Tier-3 quota unmet — could not surface a genuine cross-domain idea in this batch` in `Notes & warnings`. **Do not silently keep a mis-tagged T3 to satisfy the quota.**

## No-duplicate check
- [ ] No idea duplicates any entry in prior batches (`./_logs/_proposal_log.md`)
- [ ] No two ideas within this batch are near-duplicates

## Process artifacts
- [ ] Verification report attached inside batch markdown
- [ ] Batch file written to `./ideation-output/<benchmark>/batch-<N>.md`
- [ ] `./_logs/_proposal_log.md` updated with one-line batch entry
- [ ] **`./_logs/_search_log.md` has a session-dated heading added in this run, with ≥ 1 logged WebSearch/WebFetch query per primary paper cited.** Audit: open the file, confirm the section header for today's batch exists with new entries below it — NOT just an existing entry from a prior batch. If absent → **STOP, do not deliver**. Either run the missing searches now, or surface `⚠️ UNVERIFIED — no live searches performed this session` and ask the user before printing.
- [ ] Every primary paper's arXiv ID / venue / year was confirmed by a search result in this session — not recalled from training. Spot-check: pick 2 random primary papers from the batch; their identifiers must appear in this session's search-log entries.
- [ ] `./_logs/_rejection_log.md` updated with every rejected idea (stage + tag + evidence)
- [ ] Devil's-advocate pass executed on top-1 idea

## Time
- [ ] Total wall-clock < 15 min; if not, `⚠️ Time-budget exceeded` in `Notes & warnings`

If any unchecked box → fix or surface as warning. Do not print the user-facing summary while a box remains unchecked without a corresponding `⚠️`.
