# benchmark-climb-ideation

Claude Code skill that produces a verified batch of 5–10 research ideas to climb a specific benchmark **on a specific task** (problem framing the user is solving). Each idea has a primary paper, concrete mechanism, gain estimate with confidence, and a falsifiable test. Enforces multi-tier search (in-field / adjacent / cross-domain), pattern diversity, source-trust quotas, and a 7-step verification pipeline — output is grounded and rejection-logged, not vibe-based.

## Quick start

```bash
# 1. MATH-500, default 45/35/20 tier mix, batch of 7, greenfield
/benchmark-climb-ideation MATH-500 --task "competition-level math word problems with single numeric answer"

# 2. Enhance an existing pipeline (≥ 50% enhance-existing ideas, tier mix biased to in-field)
/benchmark-climb-ideation HumanEval --task "function-level Python code completion from docstring + signature" \
  --pipeline ./pipelines/code_pipeline.md --tier-mix 55/30/15

# 3. Heavy cross-domain bet, no existing pipeline
/benchmark-climb-ideation BIG-Bench-Hard --task "multi-step symbolic reasoning across 23 sub-tasks" \
  --tier-mix 30/30/40 --constraints "open-source only,no fine-tuning" --budget-compute "$40"
```

First run asks for **task / problem framing** (mandatory), whether an **existing pipeline** is being enhanced (optional but always asked), baseline (model + score), compute budget, time budget, and constraints — see [./checklists/pre-propose.md](./checklists/pre-propose.md). Without a task description, the skill stops and asks; a benchmark name alone is not enough.

## File layout

```
benchmark-climb-ideation/
├── SKILL.md, README.md, CHANGELOG.md
├── rules/           search-strategy, conference-tiers, source-trust,
│                    anti-bias, time-window, verification
├── patterns/        pattern-catalog (12 patterns)
├── templates/       idea, batch, verification-report
├── checklists/      pre-propose, per-idea, pre-deliver
└── examples/        good-batch-MATH500, good-batch-HumanEval,
                     bad-batch-biased, bad-batch-vague
```

## Flags

| Flag | Effect |
|------|--------|
| `--task "<desc>"` | **Required.** Concrete task / problem framing being solved on the benchmark. Skill refuses to run without it. |
| `--pipeline <path \| "text">` | Existing pipeline being enhanced. Flips the batch into `enhance-existing` mode: ≥ 50% of ideas must modify a component of this pipeline (the rest are greenfield with justification). When supplied without `--tier-mix`, skill offers a Tier-1-biased default `55/30/15`. |
| `--tier-mix <a>/<b>/<c>` | Override the in-field / adjacent / cross-domain split. Default `45/35/20`. Must sum to 100; each ≥ 10. Pre-deliver bands become `<a>±10` per tier. |
| `--batch-size <N>` | Override default (7). Must be 5–10. |
| `--focus <area>` | Bias the pattern set (`sampling`, `verify`, `retrieval`). For tier-ratio overrides prefer `--tier-mix` — it is more explicit and takes precedence. |
| `--quick` | 10 queries total, 1 re-search cycle max, ≤ 7 min wall-clock. Skips Tier-3 expansion on saturation. |
| `--deep` | 30 queries total, 3 re-search cycles, ≤ 25 min. Devil's-advocate on top-3 instead of top-1. |
| `--reset` | Ignore prior `_logs/_proposal_log.md` for duplicate detection. |
| `--budget-compute "$X"` | Compute budget for Step 4 Feasibility check. Ideas > 2× this are downgraded. |
| `--constraints "<csv>"` | Hard constraints (e.g., `"open-source only,no fine-tuning"`). Hard-violation ideas REJECTed. |

Flags compose: `/benchmark-climb-ideation MATH-500 --deep --focus verify --constraints "prompting only"`.

## Reference outputs

- [examples/good-batch-MATH500.md](./examples/good-batch-MATH500.md) — canonical 7-idea batch
- [examples/good-batch-HumanEval.md](./examples/good-batch-HumanEval.md) — `--focus tier-3` mode
- [examples/bad-batch-biased.md](./examples/bad-batch-biased.md) — annotated pattern/tier collapse
- [examples/bad-batch-vague.md](./examples/bad-batch-vague.md) — annotated vague mechanisms + fabricated citations

## Standalone usage

Portable. No dependency on any specific project layout or framework. Copy `.claude/skills/benchmark-climb-ideation/` into any project that uses Claude Code — slash commands work immediately, outputs land under `./ideation-output/<benchmark>/` and logs under `./_logs/` relative to the project root.

Requirements: Claude Code with `WebSearch`, `WebFetch`, `Read`, `Write`, `Edit`, `Bash` tools enabled, and write access to the working directory. No Python, no extra API keys, no external services. Markdown end-to-end.
