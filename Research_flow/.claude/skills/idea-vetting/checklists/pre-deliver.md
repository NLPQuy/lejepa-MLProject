---
name: pre-deliver-checklist
description: Final audit before printing the batch summary to the user
load-trigger: Between Step 4 (batch summary) and Step 5 (user-facing output)
---

# Pre-Deliver Checklist

Last gate before the user sees the batch result. Mirrors the Quality-gates block in SKILL.md.

## Per-idea (must hold for EVERY idea in the batch)
- [ ] All 8 stages run (or stages 7 explicitly skipped with `--climb-mode --no-publish` noted, OR early-exit shortcut documented with reason)
- [ ] Each Stage 1-7 has ≥ 1 attack with a full rebuttal cycle (per [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md))
- [ ] `Rebuttal-cycle summary` (DEFLECTED/WEAKENED/UNREBUTTED counts) present in every stage
- [ ] UNREBUTTED-downgrade rule applied to each stage's verdict before Stage 8 read it (per [../rules/decision-logic.md](../rules/decision-logic.md))
- [ ] Stage 8 verdict cites the priority-rule number that fired
- [ ] Confidence tag (🟢/🟡/🔴) on Stage 8 verdict with rationale
- [ ] Branch-specific block filled: Toy design / Reframe description / Kill rationale / Full-send priority rank
- [ ] Per-idea report file written to `vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md`

## Per-batch (must hold for the batch as a whole)
- [ ] Every idea in the source batch appears in EXACTLY ONE of: Killed table / Reframed table / Toy queue / FULL SEND queue
- [ ] Verdict counts in the summary table match the per-idea reports (no drift)
- [ ] Survival rate computed = `(FULL + TOY) / total`
- [ ] **Top-3 recommendations identified** along 3 distinct axes (composite / fastest-to-validate / highest-EV) — collapse only if batch genuinely has < 3 candidates
- [ ] **Toy queue sorted by cost ascending**
- [ ] **FULL SEND queue sorted by composite descending**
- [ ] `batch-summary.md` written to `vetting-output/<bench>/batch-<N>/batch-summary.md`

## Logs (append-only — never overwrite)
- [ ] `vetting-output/<bench>/_logs/_vetting_log.md` appended with one batch entry — format per [../_logs/_vetting_log.md](../_logs/_vetting_log.md) `## Entry format` (datetime + Benchmark + Source + Ideas vetted + Verdicts + Time + Survival + Top pick + Notable + Re-vet trigger)
- [ ] `vetting-output/<bench>/_logs/_killed_ideas.md` appended — one `#### Idea` entry per KILL, format per [../_logs/_killed_ideas.md](../_logs/_killed_ideas.md) (Killed-at / Killing-attack / Evidence / Salvageable / Confidence / Source / Resurrection-eligible)
- [ ] `vetting-output/<bench>/_logs/_passed_ideas.md` appended — one `#### Idea` entry per FULL SEND, format per [../_logs/_passed_ideas.md](../_logs/_passed_ideas.md) (Verdict / Confidence / Composite / Gain / Cost / Priority / Risk-mitigation / Source / Status)
- [ ] `vetting-output/<bench>/_logs/_toy_queue.md` appended under `## Active`, **cost-ascending order maintained**, format per [../_logs/_toy_queue.md](../_logs/_toy_queue.md)
- [ ] No prior log entries modified or removed (append-only discipline preserved)
- [ ] (Optional) `cross-skill-log.md` at project root appended with a 1-line entry per `templates/batch-summary.md §Cross-skill log entry`

## User-facing output
- [ ] Print summary < 40 lines (table + top-3 + path)
- [ ] Path to `batch-summary.md` printed
- [ ] Recommended next action printed (1 numbered list of 2-5 steps)
- [ ] Wallclock budget audit: if `total > 60 min`, surface `⚠️ Batch budget exceeded` warning

If any unchecked box → fix before printing, OR surface as `⚠️` warning at the top of the summary. Do not silently ship.
