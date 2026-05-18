---
name: search-strategy
description: Three-tier search rules with quotas and budgets
load-trigger: Step 2 of SKILL.md workflow
---

# Search Strategy

Search across three tiers. Quotas come from the **configured tier mix** (default `45/35/20`; user-overridable via `--tier-mix <a>/<b>/<c>`). The percentages shown in each tier heading below are the DEFAULT bands; substitute the configured values when a user override is active.

## Configured tier mix

Default: Tier 1 `45%`, Tier 2 `35%`, Tier 3 `20%` — bands are `±10pp` per tier, giving the legacy `40-50 / 30-40 / 20-30` ranges.

User override syntax: `--tier-mix <a>/<b>/<c>`. Validation rules:
- `a + b + c == 100`
- each value ≥ 10 (no tier may be reduced to zero — that defeats the anti-bias purpose)
- bands become `<a>±10` / `<b>±10` / `<c>±10` for delivery enforcement

Common overrides:
- `60/30/10` — heavy in-field bias (e.g., user has a working pipeline, only wants drop-in component swaps; cross-domain noise is unwanted).
- `30/30/40` — heavy cross-domain (e.g., the in-field SOTA looks saturated and the user wants to bet on transfer).
- `45/35/20` — default; balanced.

If `--pipeline` is supplied and `--tier-mix` is NOT, prompt the user once: "You supplied an existing pipeline — bias the search toward Tier 1 (in-field) with `--tier-mix 55/30/15`?" Default to `55/30/15` if the user agrees, otherwise keep `45/35/20`.

## Tier 1: In-Field (40-50% of batch — default; configured band applies)

**Goal**: SOTA awareness, known limitations of the target benchmark.

**Queries (use ≥ 4)**:
- `"<benchmark>" SOTA <year>`
- `"<benchmark>" leaderboard`
- `"<benchmark>" failure case OR limitation`
- `"<benchmark>" ablation`
- `<benchmark> survey`

**Budget**: 8 queries max, 20 paper summaries, 5 full reads.

## Tier 2: Adjacent (30-40% of batch — default; configured band applies)

**Goal**: Borrow technique from a benchmark in the same task family.

**Adjacency map (seed list — extend as needed)**:
- MATH-500 → GSM8K, MMLU-STEM, AIME, AMC, TheoremQA
- HumanEval → MBPP, APPS, CodeContests, LiveCodeBench
- BBH → MMLU, AGIEval, ARC-Challenge

**Queries**:
- `<adjacent_benchmark> SOTA technique`
- `<task_family> recent improvement`

**Budget**: 6 queries max, 15 paper summaries, 3 full reads.

## Tier 3: Cross-Domain (20-30% of batch — default; configured band applies)

**Goal**: Transfer a principle from a *different research field*, not a different ML sub-area.

### What counts as Tier 3 (hard test)

A T3 idea must satisfy ALL of:
1. The **primary paper** is published in a venue from a **different field** than the benchmark's home field. Same-field-ML-adjacent ≠ T3.
   - Example for vision-SSL benchmarks: T3 primaries come from optimization theory journals (SIAM J. Optimization), statistics (JASA, Biometrika, Annals of Statistics), control (Automatica), neuroscience (Neural Computation, NeurIPS-Bio), physics (Physical Review), biology (Nature Methods), HCI, formal methods, etc. Other vision/SSL/representation-learning ML papers = **T1 or T2**, not T3.
   - Example for LLM/reasoning benchmarks: T3 primaries come from game AI (MCTS literature), compiler design, symbolic AI, formal verification, cognitive science, economics. Other NLP/LLM papers = T1/T2.
2. The mechanism is a **principle, algorithm, or theorem** named and developed in that other field — not just "use the same generic ML technique that happens to also appear there".
3. The proposal explicitly names the **source domain → target domain** transfer (e.g., "MCTS from two-player games → reasoning trace search"; "Polyak averaging from convex optimization theory → SSL pretraining"). A T3 idea card must include a `Cross-domain transfer:` line stating `<source field>` → `<target use>`.

### What does NOT count as Tier 3 (frequent confusion)

- ❌ **In-field paper + cross-domain supporting reference**. Primary paper is the only one that counts. Slapping GradNorm or a control-theory blog post into "Supporting" doesn't make the idea T3.
- ❌ **Adjacent ML sub-areas**: AutoML/Hyperband (still ML), generative modeling (when target is discriminative), multi-task learning, meta-learning, federated learning — these are T2 (adjacent), not T3.
- ❌ **Generic optimization techniques that have been mainstream in ML for >5 years**: SWA, dropout, mixup, label smoothing, LR schedulers. These were T3 a decade ago and are T1/T2 now. Use the test: "Has this technique been used in 3+ papers at NeurIPS/ICML/ICLR on this benchmark's field in the last 3 years?" If yes → not T3.
- ❌ **Engineering tooling**: Optuna, Ray, ASHA, distributed training tricks. These are not ideas (see `../patterns/pattern-catalog.md §NOT-an-idea filter`) and a T3 label cannot rescue them.

### Cross-domain seeds (examples by benchmark family)

- Vision-SSL / representation learning ← optimal transport (math), random matrix theory (physics/math stats), control theory (Lyapunov stability for training dynamics), neuroscience (predictive coding), information geometry, signal processing (compressive sensing, sliced statistics)
- Math reasoning ← Game AI (MCTS), program synthesis, symbolic AI, theorem proving, planning
- Code generation ← NLG, retrieval, formal verification, compiler design
- General reasoning ← planning, multi-agent debate, constraint solving, cognitive science

### Queries

- `<principle_name> <source_field>` (e.g., "Polyak iterate averaging convex optimization")
- `<algorithmic_family> applied to <new_domain>` (e.g., "MCTS for natural language reasoning")
- Source-field venue queries: `site:siam.org <topic>`, `<topic> Annals of Statistics`, etc.

**Budget**: 5 queries max, 10 paper summaries, 2 full reads.

### Quality check before tagging T3

For each T3 candidate, answer in the idea card:
- **Source field**: `<field>` (must not be vision-SSL / representation learning for vision benchmarks; must not be NLP/LLM for reasoning benchmarks; etc.)
- **Source venue**: `<venue>` of the primary paper (must not be on the in-field tier-1 venue list of `./conference-tiers.md`).
- **Transfer**: 1 sentence stating exactly what is being lifted from where to where.

If any of those three is missing or fails the test → the idea is NOT T3. Re-tag as T1/T2 or drop and re-search.

## Quota enforcement (hard)

Each final batch must satisfy the **configured tier mix** ±10pp per tier. With the default `45/35/20`:

```
Tier 1: 40-50%   (e.g., 4-5 ideas out of 10)
Tier 2: 30-40%   (e.g., 3-4 ideas out of 10)
Tier 3: 20-30%   (e.g., 2-3 ideas out of 10)
```

With a user override (e.g., `--tier-mix 60/30/10`): bands become `50-70 / 20-40 / 0-20`. The batch-template `Inputs` block records the configured mix so the audit knows which bands apply.

If a tier cannot reach its quota after budget + re-search, explicitly tell the user: "Could not surface enough Tier-<N> ideas under the configured mix `<a>/<b>/<c>`; batch may be biased away from <tier name>. Re-run with more search time or relax the mix?"

## Search budget per tier (hard caps)

| Tier | Max queries | Max paper summaries | Max full reads |
|------|-------------|---------------------|----------------|
| Tier 1 | 8 | 20 | 5 |
| Tier 2 | 6 | 15 | 3 |
| Tier 3 | 5 | 10 | 2 |
| **Total** | **19** | **45** | **10** |

These caps target ~15 min wall-clock. Going over → stop and present what you have with `⚠️ Search-budget exhausted` note.

## Saturation detection

Per tier: if **3 consecutive queries** return only papers already in the candidate pool → stop that tier early, move to the next. Do not burn the rest of the budget on a saturated tier.

Across the batch: if total novel papers across all 3 tiers < `batch_size_target × 1.5` (i.e., not enough headroom to absorb rejections) → trigger re-search per `../rules/verification.md §Re-search trigger`.

## Anti-bias requirements (see ../rules/anti-bias.md for full enforcement)

- ≥ 3 distinct venues per tier (use `./conference-tiers.md` whitelist).
- ≥ 3 distinct time windows across batch (see `./time-window.md`).
- ≥ 3 distinct technique families.
- No more than 2 ideas from same first-author institution.

## Source confirmation rule

Every picked paper MUST be reachable by a working link (arXiv, openreview, or venue page). Drop the paper if the link does not resolve — do not paraphrase a source you cannot open. Trust-tier the paper per [./source-trust.md](./source-trust.md).

## Search log

Append every query to `_logs/_search_log.md` using this format:

```markdown
# Search Log — Batch <N> — <YYYY-MM-DD>

## Tier 1: In-Field
- <HH:MM:SS> Query: "<query>" → found <K>, summaries <K2>, picked <K3> [arXiv:..., ...]
...

## Tier 2: Adjacent
...

## Tier 3: Cross-Domain
...

## Totals
- Queries used: <X> / 19
- Summaries read: <Y> / 45
- Full reads: <Z> / 10
- Wall-clock: <M> min
- Saturation events: <list of tiers stopped early>
```

Append-only — never rewrite prior batches' entries.
