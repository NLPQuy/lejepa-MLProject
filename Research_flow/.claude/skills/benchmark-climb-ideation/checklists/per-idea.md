---
name: per-idea-checklist
description: Hard checklist to run on each draft idea before it enters the verification report
load-trigger: Step 4 of SKILL.md workflow, before invoking ../rules/verification.md
---

# Per-Idea Checklist

Run this checklist on EACH draft idea. Every box must be tickable before the idea enters the 7-step verification pipeline in [../rules/verification.md](../rules/verification.md). If any box fails, fix or drop the idea before verification — do not waste verification budget on malformed ideas.

- [ ] **Pattern tagged** — exactly one of `P1`–`P12` from `../patterns/pattern-catalog.md`.
- [ ] **Tier tagged** — exactly one of `1` / `2` / `3`.
- [ ] **Mechanism** filled with 2–4 concrete sentences (input → process → output named).
- [ ] **Primary source paper** cited with title + venue + year + arXiv ID (or DOI).
- [ ] **Supporting paper** (≥ 1) cited with title + venue + year + link.
- [ ] **Expected gain** stated as `gain_low / gain_mid / gain_high` (pp) with a confidence color 🟢/🟡/🔴.
- [ ] **Feasibility score** stated as integer `1`–`5`.
- [ ] **Effort tier** stated as `S` / `M` / `L` / `XL` / `XXL`.
- [ ] **Falsification test** stated with a measurable observation AND a numeric threshold.
- [ ] **Risks listed** (or explicit `none material` if no risks identified).
- [ ] **Compliance** with user-declared constraints checked (model, eval-set, no-fine-tuning, budget, parallelization).
- [ ] **Tier-3 only**: `Adjacent / Cross-domain notes` block filled (original domain, target domain, adaptation list).

If ≥ 2 boxes fail on the same idea → drop the idea entirely; do not patch repeatedly. A malformed idea usually signals weak grounding, not formatting laziness.
