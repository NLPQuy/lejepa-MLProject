---
name: pre-propose-checklist
description: Hard checklist to confirm before starting Step 2 (multi-tier search)
load-trigger: Step 1 of SKILL.md workflow
---

# Pre-Propose Checklist

Confirm every item before launching the search. Missing inputs → ASK USER, do not invent.

- [ ] **Benchmark name** confirmed with user (exact name, e.g., `MATH-500` not "the math one")
- [ ] **Task / problem** confirmed with user — concrete problem framing being solved on that benchmark (e.g., `function-level Python code completion from docstring + signature`, `competition-level high-school math word problems with single numeric answer`, `multi-hop factoid QA over Wikipedia`). Generic phrases like "do well on the benchmark" or "improve the score" are NOT sufficient — push back and get the actual task description.
- [ ] **Baseline** known: model identity + score on this task (e.g., `gpt-4o-mini @ 70.2%`)
- [ ] **Compute budget** declared (dollars OR GPU-hours OR API call ceiling)
- [ ] **Time budget** declared (when does the user need this?)
- [ ] **Model access** confirmed (API keys present? local model available? closed-weights model accessible?)
- [ ] **Constraints** listed (e.g., `prompting only`, `no fine-tuning`, `must parallelize`, `open-source only`)
- [ ] **Prior batches** loaded from `./_logs/_proposal_log.md` (or noted as empty if first run)
- [ ] **Output directory** `./ideation-output/<benchmark>/` exists or will be created in Step 6
- [ ] **Existing pipeline?** asked explicitly. If yes: pipeline description loaded (file or inline) — batch will run in `enhance-existing` mode (≥ 50% of ideas must modify the pipeline; rest are greenfield with justification). If no: record "greenfield batch — no pipeline supplied" in the batch header.
- [ ] **`--tier-mix <a>/<b>/<c>` flag** parsed (default `45/35/20`); validation passed (sum = 100, each ≥ 10). If a pipeline was supplied and no override given, the user was offered the `55/30/15` Tier-1-biased default.
- [ ] **`--focus` flag** parsed if user passed one (e.g., `--focus tier-3`, `--focus sampling`) and its meaning confirmed. Note: `--tier-mix` takes precedence over `--focus` shorthands for tier ratios.

If any of items 1, 2, 3, 4, 5 is missing → do NOT proceed. Ask the user the minimum-needed clarifying question and wait. Highest-priority missing fields: **Benchmark name** and **Task / problem** — without both, the search strategy cannot be scoped.
