---
name: batch-summary-template
description: Aggregate report after vetting an N-idea batch (one file per batch)
load-trigger: Written at end of Step 4 (Batch summary) — one file per vetted batch
---

# Batch Summary Template

Written to `vetting-output/<bench>/batch-<N>/batch-summary.md` after every idea in the batch has its individual report. Use the skeleton below; every `<placeholder>` must be filled.

```markdown
# Vetting Batch Summary — <BENCHMARK> / <TASK>

**Source batch**: <path to ideation batch file, e.g., ideation-output/MATH-500/batch-1.md>
**Benchmark**: <name>
**Task / problem**: <concrete problem framing inherited from the source batch>
**Existing pipeline**: <description inherited from the batch header, or "none — greenfield batch">
**Batch scope mix**: <K_enhance enhance-existing / K_green greenfield>
**Vetted**: <ISO 8601 datetime>
**Skill version**: 0.4.0
**Ideas vetted**: <N>
**Total time**: <X> min (budget: 60 min / batch)
**Mode flags**: <e.g., --climb-mode --no-publish, or "default">

## Verdicts

| Verdict | Count | Idea IDs |
|---------|-------|----------|
| ❌ KILL | <K> | <list of IDs> |
| 🔄 REFRAME | <R> | <list> |
| 🧪 TOY | <T> | <list> |
| ✅ FULL SEND | <F> | <list> |

## Survival rate

`(FULL + TOY) / total = (<F> + <T>) / <N> = <X.X>%`

Calibration guide:
- < 30 % survival → batch was weak (suggest re-ideation with `--avoid-patterns` for the killed patterns).
- 30-70 % → healthy batch.
- > 80 % → may indicate insufficient adversarial rigor (vetting was too lenient); re-audit a sample.

## Top recommendations (the 3 categories the user actually picks from)

### 🥇 Top FULL SEND candidate (by composite score)
**Idea <X>: <title>**
- Composite score (from ideation): <S>
- Vetting confidence: 🟢 / 🟡 / 🔴
- Killer-baseline check: PASS / WARN-but-rebutted / FAIL-but-reframed
- Suggested next: implement now; assigned batch priority <rank>.

### ⚡ Fastest to validate (lowest toy cost — from the TOY queue)
**Idea <Y>: <title>**
- Toy cost: $<Z>, <H> hours
- Toy resolves: <which key uncertainty — name the stage's WARN it would settle>
- Recommended if user wants signal in < 1 day.

### 🎯 Highest expected value (gain × vetting-confidence)
**Idea <W>: <title>**
- Expected gain (mid): +<G>pp
- Vetting confidence: 🟢 / 🟡
- Effort: L / XL — consider AFTER Top FULL SEND ships.

## Killed ideas (with reasons — every KILL must appear here)

| # | Title | Killed at stage | Reason | Killing evidence |
|---|-------|-----------------|--------|------------------|
| <i> | <title> | Stage 2 | Hard duplicate | arXiv:24XX.XXXXX (title match, same benchmark) |
| <i> | <title> | Stage 6 | Killer baseline | Tool-use exec at $20 estimated +2.0pp > idea +1.5pp |

Also appended to `vetting-output/<bench>/_logs/_killed_ideas.md`.

## Reframed ideas

| # | Original (1 line) | Reframed (1 line) | Triggering stage | Re-vet trigger |
|---|-------------------|-------------------|------------------|----------------|
| <i> | "<orig one-liner>" | "<reframed one-liner>" | Stage 3 / 6 / 7 | <e.g., "after toy of combined version"> |

## Toy queue (sorted by cost ascending — fastest-to-validate first)

| Rank | # | Title | Toy cost | Toy wallclock | Success criterion |
|------|---|-------|----------|---------------|--------------------|
| 1 | <i> | <title> | $<small> | <H>h | ≥ <X>% of expected gain on <N>-problem subset |
| 2 | <i> | <title> | $<med> | <H>h | ... |
| 3 | <i> | <title> | $<med> | <H>h | ... |

Also appended to `vetting-output/<bench>/_logs/_toy_queue.md` (cost-sorted, append-only).

## FULL SEND priority queue

| Rank | # | Title | Composite | Confidence | Effort |
|------|---|-------|-----------|------------|--------|
| 1 | <i> | <title> | <S> | 🟢 | M |
| 2 | <i> | <title> | <S> | 🟡 | L |

Also appended to `vetting-output/<bench>/_logs/_passed_ideas.md`.

## Diversification note (§8.5 of decision-logic.md)

When ≥ 3 FULL SEND ideas exist, the user cannot implement all simultaneously. The recommendations above already pick top-3 along **3 different axes** (composite / fastest-to-validate / highest-EV). Remaining FULL SEND ideas stay in `_passed_ideas.md` as the queue.

## Recommended user action

1. Implement **Idea `<X>`** (Top FULL SEND) — assigned priority 1.
2. **In parallel**, run the toy for **Idea `<Y>`** (fastest-to-validate) — $<Z>, <H>h.
3. If toy passes, promote Idea `<Y>` to implementation queue position 2.
4. Re-vet the batch in 2 weeks once Idea `<X>`'s real results land; pass `--given-result "..."` so vetting can recalibrate.
5. For killed ideas, the user can pass `/vet-ideas --resurrect idea-<i> --counter-argument "..."` to re-run with a user-supplied rebuttal (per `rules/rebuttal-loop.md §User-input rebuttal`).

## Cross-skill log entry (appended to project-root `cross-skill-log.md` if present)

```
## <ISO date+time> — Vetting Batch <N> — <BENCHMARK> — <K> KILL / <R> REFRAME / <T> TOY / <F> FULL — top pick: Idea <X>
```

## Provenance signature

SHA256 of (source-batch-hash + per-idea-verdicts + timestamp): `<hash>`
```

## Hard rules

- Every idea in the source batch MUST appear in exactly ONE of: Verdicts table, Killed table, Reframed table, Toy queue, or FULL SEND queue.
- The `Benchmark` and `Task / problem` header fields are mandatory. A batch summary without both is invalid — it breaks cross-session log filtering.
- The Toy queue MUST be sorted by `Toy cost` ascending.
- The FULL SEND queue MUST be sorted by composite score (or vetting-confidence as tie-breaker) descending.
- The 3 top-recommendation cards must pick 3 **distinct** ideas when possible. Only collapse to fewer when the batch genuinely has fewer than 3 candidates across the 3 axes.
- Survival rate is computed on `(FULL + TOY)` — REFRAMEs do not count as survival; they are pending-re-vet.
