---
name: benchmark-climb-ideation
description: Propose 5-10 research ideas to climb a specific benchmark on a specific task (problem framing) with multi-tier search and verification. Use when the user names BOTH a benchmark AND the task/problem being solved on it, and asks for ideas/proposals/directions to improve the metric.
triggers:
  slash-commands:
    - /benchmark-climb-ideation
  keywords:
    - "propose ideas for <task> on <benchmark>"
    - "help me climb <benchmark> for <task>"
    - "ideas to improve <task> on <benchmark>"
tools-required: [WebSearch, WebFetch, Read, Write, Edit, Bash]
default-batch-size: 7
---

# Benchmark Climb Ideation Skill

## When to use this skill

Use this skill when the user wants to propose **multiple research ideas** to improve performance on a **specific task** evaluated by a **specific benchmark**, and they care more about:
- Increasing the benchmark metric for that task
- Having a diverse pool of candidates
- Traceable sources from top-tier venues

Do NOT use this skill when:
- User wants open-ended exploration (no specific benchmark)
- User names a benchmark but cannot describe the task being solved (a benchmark like MMLU spans many tasks; ideation cannot start until the target task is fixed)
- User wants 1 deep idea (not a batch)
- User wants to implement (not propose)

## Inputs required

Before starting, gather:
1. **Benchmark name** (e.g., "MATH-500", "HumanEval", "MMLU-Pro")
2. **Task / problem** being solved on that benchmark — what the model is actually doing (e.g., "competition-level math word problems with single numeric answer", "function-level Python code completion from docstring", "multi-subject multiple-choice QA in STEM"). A benchmark alone is insufficient: many benchmarks cover several tasks, and the choice of ideas depends on the task framing.
3. **Current baseline** (model + score on this task)
4. **Budget** (compute, time, model access)
5. **Constraints** (e.g., "no fine-tuning")
6. **(Optional) Existing pipeline** — if the user already has a working pipeline they want to *enhance* (rather than redesign from scratch), gather it as either:
   - a file path (markdown / code / diagram) describing the current pipeline's components, OR
   - an inline description (input → components → output, with the score this pipeline currently achieves).
   When present, the batch must propose ideas that *modify the existing pipeline* (swap a component, add a verifier, change decoding, route by sub-type, etc.) — NOT wholly green-field replacements. Pure green-field ideas are still allowed but capped at ≤ 50% of the batch (see Step 3).
7. **(Optional) Tier mix override** — via `--tier-mix <a>/<b>/<c>` (e.g., `60/30/10`). Defaults to `45/35/20` (Tier 1 / Tier 2 / Tier 3). Must sum to 100; each tier ≥ 10. Pre-deliver tier-band check uses the *configured* mix ± 10 pp, not the default bands.
8. **(Optional) Prior batches** — load `_logs/_proposal_log.md` to avoid duplicates

If any of [1, 2, 3, 4] missing → ASK USER before proceeding. Specifically, if the user gives only a benchmark name without a task description, ASK: "Trên benchmark này bạn đang giải bài toán cụ thể gì? (ví dụ: code generation từ docstring, math word problems, multi-hop QA, ...)". Also ASK: "Bạn có pipeline / hệ thống nào đang chạy mà muốn cải thiện không, hay đang muốn đề xuất từ đầu?" — record the answer either way (so the batch header is honest about scope).

## Workflow (step-by-step)

### Step 1: Pre-flight
Confirm inputs above. (Phase-4 will add `./checklists/pre-propose.md`.)

### Step 2: Multi-tier search

**Hard rule — live searches only.** Every primary paper cited in the final batch MUST trace to a `WebSearch` (or `WebFetch`) call made *in the current session*, logged to `_logs/_search_log.md` under a session-dated heading before Step 3 begins. **Citing papers from memory is forbidden** — you may *think* you know the venue and arXiv ID, but model recall hallucinates venues, years, and IDs at non-trivial rates. The log is the audit trail; if a paper isn't in this session's log, it cannot enter the batch.

If WebSearch / WebFetch is unavailable (tool not in this environment, disabled by the user, network errors after 2 retries), **STOP and tell the user** — do not proceed with memory-based citations. The honest move is "search tools unavailable, cannot produce a verified batch"; offer to draft an *unverified* batch only if the user explicitly opts in, and stamp it `⚠️ UNVERIFIED — no live searches performed` in `Notes & warnings`.

Follow [./rules/search-strategy.md](./rules/search-strategy.md). **Quotas** (enforced at delivery) come from the configured tier mix:

- Default mix: Tier 1 `45%`, Tier 2 `35%`, Tier 3 `20%` (bands ±10pp → Tier 1 40-50%, Tier 2 30-40%, Tier 3 20-30%).
- User override: `--tier-mix <a>/<b>/<c>`. Must sum to 100, each ≥ 10. Pre-deliver bands shift to `<a>±10` / `<b>±10` / `<c>±10`.
- Pipeline-enhance mode hint: when an Existing pipeline is supplied, Tier 1 (in-field) often becomes more valuable; consider biasing the mix toward Tier 1 (e.g., `--tier-mix 55/30/15`) since drop-in component swaps are usually in-field.

Search budget caps (per `search-strategy.md`): Tier 1 ≤ 8 queries, Tier 2 ≤ 6, Tier 3 ≤ 5. Total ≤ 19 queries, ≤ 45 summaries, ≤ 10 full reads, ≤ 15 min wall-clock.

For every candidate paper:
- Filter venue via [./rules/conference-tiers.md](./rules/conference-tiers.md) — Tier-4 sources are rejected.
- Tag trust tier via [./rules/source-trust.md](./rules/source-trust.md) — batch must end with ≥ 60% T1+T2 primaries.
- Tag time window per [./rules/time-window.md](./rules/time-window.md) — meet per-window minimums.

Apply anti-bias rules from [./rules/anti-bias.md](./rules/anti-bias.md): force-list venues (≥ 3 distinct), force-list time windows (≥ 3), force-list technique families (≥ 3), no more than 2 ideas per first-author institution.

Append every query to `_logs/_search_log.md` using the format in `search-strategy.md §Search log`.

### Step 3: Idea drafting
For each candidate idea, fill [./templates/idea-template.md](./templates/idea-template.md).
Apply patterns from [./patterns/pattern-catalog.md](./patterns/pattern-catalog.md).

**NOT-an-idea filter (run first, drop offenders silently):** Before drafting, apply the filter in `./patterns/pattern-catalog.md §NOT-an-idea filter` — hyperparameter sweeps / grid search / ASHA-Hyperband, "just train longer", re-running the existing pipeline, running a public baseline for comparison, and code refactors are **NOT research ideas** and must not be drafted. If a candidate reduces to one of those, drop it and instead append a one-line entry to the batch's `Notes & warnings` under a **Prerequisites / measurements** sub-header. Under-quota with a warning is the honest delivery — do not pad with engineering tasks.

**Diversification matrix (hard, enforced):**
- ≥ 5 distinct patterns per batch (out of P1–P12).
- Max 2 ideas per pattern.
- ≥ 3 distinct technique families across the batch (mechanism-level, not paper-level).
- Recommend ≥ 1 P2 (Transfer) and ≥ 1 P6 (Verify) per batch (historically high-yield).

**Pipeline-enhance vs. greenfield mix (only when Existing pipeline is supplied):**
- ≥ 50% of ideas (rounded up) must be tagged `Scope: enhance-existing` — each one names which component of the existing pipeline it modifies and what stays unchanged.
- The remainder may be `Scope: greenfield` (new pipeline / wholly different design). Greenfield ideas must explicitly justify why a redesign is preferable to a component swap.
- Pattern fit (suggestive, not hard): P3 (Replace), P6 (Verify), P9 (Tool-use), P10 (Sampling), P11 (ICL), P4 (Scale) naturally enhance existing pipelines. P2 (Transfer), P5 (Decompose), P12 (Self-play) tend toward greenfield. See `./patterns/pattern-catalog.md §Pattern fit for enhance vs greenfield`.

After drafting, run the **reverse-search pass** from [./rules/anti-bias.md](./rules/anti-bias.md) (1 added idea max) to fill an obvious technique-family gap before verification.

### Step 4: Verification
For each draft idea:
1. First, run the hard checklist [./checklists/per-idea.md](./checklists/per-idea.md) — every box must tick before the idea enters verification. Malformed ideas are dropped here, not verified.
2. Then run the 7-step pipeline in [./rules/verification.md](./rules/verification.md), in order: Novelty → Provenance → Feasibility → Gain-sanity → Falsification → Risk → Compliance. Stop early on the first REJECT.
3. After all ideas processed, run the **cross-idea consistency** pass (§8 of `verification.md`): near-duplicates, contradictions, score-distribution sanity.
4. Emit a verification report using [./templates/verification-report-template.md](./templates/verification-report-template.md). Include it in the batch markdown AND append rejection entries to `./_logs/_rejection_log.md` (create if missing).

Every check must emit a controlled-vocabulary verdict (`NOVEL` / `EXTENDS` / `DUPLICATE`, `VERIFIED` / `BROKEN_LINK` / `MISREPRESENTED`, feasibility `1`–`5`, etc. — see `verification.md` for the full list). No free-form verdicts.

### Step 5: Re-search if under-quota
If `verified_count < 5` after Step 4:
1. Identify which pattern slot or tier the rejected ideas left empty.
2. Run a focused search restricted to that gap (single tier, single pattern family) — narrower than the Step-2 sweep.
3. Generate replacement idea(s); re-run Step 4 on each.
4. Max **2** re-search cycles per batch. After that, present the partial batch with a `⚠️ Under-quota` warning at the top of `Notes & warnings`.

### Step 6: Ranking & presentation
Format the final batch using [./templates/batch-template.md](./templates/batch-template.md).
Composite score: `0.4 * Gain + 0.3 * Feasibility + 0.2 * (XL_minus_Effort) + 0.1 * Novelty`.

**Venue-blind ranking**: venue prestige is NOT a ranking input (it filters inputs and sets trust tier only). Tie-break by venue only when composite scores are identical. See [./rules/anti-bias.md](./rules/anti-bias.md) §Venue-blind ideation.

**Devil's-advocate pass**: for the top-1 idea by composite score, run 2 focused queries for failure cases / negative results (per `anti-bias.md §Devil's-advocate`). If concerning evidence surfaces, downgrade by 1 slot and add the contrasting paper to the idea.

Write to `./ideation-output/<benchmark>/batch-<N>.md` (create directory if needed).

### Step 7: User-facing summary
Print to user:
- Batch summary table
- Top-3 picks (Quick win / Big bet / Safe bet)
- Path to full output file

### Step 8: Log
Append a one-line entry to `./_logs/_proposal_log.md` (create if missing): timestamp, benchmark, batch path, pattern set used.

## Stop conditions

Stop when:
- Step 6 completed (success)
- Re-search budget exhausted (2 cycles)
- > 15 minutes wall-clock elapsed
- User says stop

## Inputs ↔ Outputs

| Input | Source |
|-------|--------|
| Benchmark name | User |
| Task / problem | User (mandatory — describes what is being solved on the benchmark) |
| Existing pipeline | User (optional — flips batch into `enhance-existing` mode when present) |
| Tier mix | User (optional `--tier-mix a/b/c`; defaults to `45/35/20`) |
| Baseline | User or recent paper |
| Budget | User |
| Constraints | User |
| Prior batches | `_logs/_proposal_log.md` |

| Output | Destination |
|--------|-------------|
| Batch markdown | `./ideation-output/<benchmark>/batch-<N>.md` |
| Proposal log | `./_logs/_proposal_log.md` |
| Top-3 recommendations | Direct response to user |

## Quality gates (self-check before delivery)

**Batch shape**
- [ ] Batch size 5-10
- [ ] Search-tier distribution: T1 40-50%, T2 30-40%, T3 20-30%

**Diversity (count-based, see [./rules/anti-bias.md](./rules/anti-bias.md))**
- [ ] ≥ 5 distinct patterns (P1–P12); max 2 ideas per pattern
- [ ] ≥ 3 distinct technique families (mechanism-level)
- [ ] ≥ 3 distinct venues across the batch
- [ ] No more than 2 ideas from same first-author institution / lab
- [ ] ≥ 3 distinct time windows represented; per-window minimums in `./rules/time-window.md` met
- [ ] ≥ 60% of primary papers from Tier 1+2 sources (`./rules/source-trust.md`)
- [ ] Recency check: ≥ 2 papers `<12mo`, ≥ 2 papers `12-36mo`, ≥ 1 paper `36-72mo`

**Per-idea evidence**
- [ ] Every idea has ≥ 1 primary paper VERIFIED (title + venue + arXiv ID resolvable, venue on the `./rules/conference-tiers.md` whitelist)
- [ ] Every idea has a sharp falsification test (measurable observation + numeric threshold)
- [ ] Every idea passed all 7 verification checks (Novelty, Provenance, Feasibility, Gain-sanity, Falsification, Risk, Compliance)

**Process artifacts**
- [ ] Verification report present in batch markdown with controlled-vocabulary verdicts
- [ ] Rejected ideas logged to `_logs/_rejection_log.md` with stage + tag + evidence
- [ ] `_logs/_search_log.md` updated with every query (totals: queries / summaries / full reads / wall-clock)
- [ ] Cross-idea consistency clean (no near-duplicates, no unexplained contradictions, score-distribution not over-confident)
- [ ] No duplicates with prior entries in `_logs/_proposal_log.md`
- [ ] Devil's-advocate pass executed on top-1 idea
- [ ] Top-3 recommendations highlighted (Quick win / Big bet / Safe bet)
- [ ] If any quota / diversity gate fails AND re-search budget exhausted → corresponding `⚠️` warning surfaced at top of `Notes & warnings`

If any gate fails → try 1 re-search round (max 2 total cycles); otherwise surface as warning, do not silently ship.

## Anti-patterns (do NOT)

- Don't propose without a primary paper (no hallucinated sources)
- Don't claim "beats SOTA" without explicit "extension of X" framing
- Don't skip Tier 3 because "too time-consuming"
- Don't include vague mechanisms ("use better prompts")
- Don't claim 🟢 confidence without direct evidence
- **Don't smuggle HP-tuning, grid search, ASHA/Hyperband sweeps, "just measure the baseline", or "just train longer" into the batch as research ideas.** These are prerequisites or controls — surface them in `Notes & warnings` under **Prerequisites / measurements**, never as an indexed idea. See `./patterns/pattern-catalog.md §NOT-an-idea filter`.
- **Don't relabel an engineering task as the nearest pattern** (e.g., calling an HP sweep "P7 Iterate" or "P3 Replace") to satisfy the 5–10-idea quota. Under-quota is acceptable; mislabeled is not.
- **Don't cite papers from memory.** Every primary paper must trace to a WebSearch/WebFetch call logged in `_logs/_search_log.md` *in this session*. Memory-cited papers hallucinate venues / arXiv IDs / authors. If search tools are unavailable, STOP and tell the user — do not silently ship an unverified batch. (See Step 2 hard rule.)
- **Don't fake Tier-3 by gluing a cross-domain "supporting" reference onto an in-field primary.** Tier 3 = primary paper from a *different research field* (statistics journal, optimization theory, neuroscience, control, physics, …), not "ML adjacent". SWA, ASHA, EMA, dropout, mixup, label smoothing — all mainstream-ML, NOT Tier 3 regardless of original venue. Audit per `./checklists/pre-deliver.md §Tier-3 honesty audit`. If a real cross-domain pick cannot be found, accept under-quota with `⚠️` rather than mis-tag.

## Reference files (load on-demand)

- [./rules/search-strategy.md](./rules/search-strategy.md) — multi-tier search + budgets + saturation
- [./rules/conference-tiers.md](./rules/conference-tiers.md) — venue whitelist (input filter only)
- [./rules/source-trust.md](./rules/source-trust.md) — 4-tier trust hierarchy + 60% T1+T2 quota
- [./rules/anti-bias.md](./rules/anti-bias.md) — force-list venues/time/techniques + reverse-search + devil's-advocate
- [./rules/time-window.md](./rules/time-window.md) — per-window minimum counts + classics rules
- [./rules/verification.md](./rules/verification.md) — 7-step per-idea verification pipeline
- [./patterns/pattern-catalog.md](./patterns/pattern-catalog.md) — 12 idea patterns
- [./templates/idea-template.md](./templates/idea-template.md) — per-idea format
- [./templates/batch-template.md](./templates/batch-template.md) — batch wrapper
- [./templates/verification-report-template.md](./templates/verification-report-template.md) — verification report format
- [./checklists/per-idea.md](./checklists/per-idea.md) — hard checklist before verification

## Activation flow

Slash command (`/benchmark-climb-ideation <benchmark> --task "<task description>" [--pipeline <path|"text">] [--tier-mix a/b/c]`): execute Steps 1-8. If `--task` is omitted, ASK the user before proceeding. If `--pipeline` is omitted, ASK whether one exists (then either record it or note "greenfield batch — no pipeline supplied"). `--tier-mix` is optional with default `45/35/20`.
Natural language ("propose ideas to improve my existing X pipeline on benchmark Y for task Z"): confirm intent, task, pipeline, then same flow.
