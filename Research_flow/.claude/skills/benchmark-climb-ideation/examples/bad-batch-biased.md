# BAD Batch Example — Biased (Annotated)

> **This is a teaching example.** It is what the skill should NEVER produce. Read the `## What's wrong with this batch` section at the bottom for the diagnosis.

# Idea Batch 1 — MATH-500
**Generated**: 2026-05-17T09:00:00Z
**Time-to-batch**: 6 min (too fast — search saturation hit early)
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation MATH-500`

## Inputs
- Benchmark: MATH-500
- Baseline: gpt-4o-mini @ 70.2%
- Constraints: prompting only

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 10 |
| Tier 1 / 2 / 3 | 10 / 0 / 0 |
| Patterns used | P1 (×8), P4 (×1), P11 (×1) — **3 patterns only** |
| Distinct venues | 2 (NeurIPS, ICLR) |
| Time windows | `<12mo` (10) |
| Avg feasibility | 4.9 / 5 — **suspiciously uniform** |
| Avg confidence | 🟢 100% — **everything is 🟢, calibration smell** |

## Summary table
| # | Title | Pattern | Tier | Gain | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 1 | CoT + Self-consistency | P1 | 1 | +3.0 | 5 | S | 4.0 |
| 2 | CoT + Self-refine | P1 | 1 | +2.5 | 5 | S | 3.7 |
| 3 | CoT + ToT | P1 | 1 | +2.8 | 5 | M | 3.5 |
| 4 | CoT + Reflexion | P1 | 1 | +2.0 | 5 | M | 3.0 |
| 5 | Self-consistency + Self-refine | P1 | 1 | +2.2 | 5 | M | 3.2 |
| 6 | Better prompts | P11 | 1 | +1.5 | 5 | S | 2.8 |
| 7 | CoT + verifier | P1 | 1 | +3.0 | 5 | M | 3.7 |
| 8 | CoT + few-shot | P1 | 1 | +2.5 | 5 | S | 3.6 |
| 9 | Self-consistency K=40 | P4 | 1 | +1.5 | 5 | S | 2.9 |
| 10 | Just try harder prompts | P1 | 1 | +1.0 | 5 | S | 2.5 |

## Ranked ideas (abbreviated)

### Idea 1: CoT + Self-consistency
- Pattern: P1 (Combine) — Tier: 1
- Mechanism: "Combine CoT with self-consistency for better results."
- Primary: "Chain-of-Thought", Wei et al., NeurIPS 2022 [arXiv:2201.11903]
- Falsification test: *(missing)*

### Idea 3: CoT + Tree of Thoughts
- Pattern: P1 — Tier: 1
- Primary: "Chain-of-Thought", Wei et al., NeurIPS 2022 [arXiv:2201.11903] ← **same paper as Idea 1, 7, 8, 10**
- Falsification test: *(missing)*

### Idea 6: Better prompts
- Pattern: P11 — Tier: 1
- Mechanism: "Use better prompts." ← **vague**
- Primary: *(none cited)*
- Falsification test: *(missing)*

### Idea 9: Self-consistency K=40
- Pattern: P4 — Tier: 1
- Mechanism: replicates Wang et al. 2023 exactly (K=40 was the headline configuration in that paper) → **DUPLICATE**
- Primary: "Self-Consistency", Wang et al., ICLR 2023 [arXiv:2203.11171]

### Idea 10: Just try harder prompts
- Pattern: P1 — Tier: 1
- Mechanism: "Try various prompts and see what works." ← **vague**

*(Other ideas elided — they all follow the same `CoT + X` template.)*

---

## What's wrong with this batch

| # | Issue | Where | Rule violated |
|---|-------|-------|---------------|
| 1 | **0 Tier-2, 0 Tier-3 ideas** — entire batch is in-field | All 10 ideas | `search-strategy.md` quota (40-50 / 30-40 / 20-30) |
| 2 | **8 of 10 ideas are pattern P1 (Combine)** | Ideas 1, 2, 3, 4, 5, 7, 8, 10 | `anti-bias.md` — max 2 per pattern |
| 3 | **Only 3 distinct patterns** used | P1, P4, P11 | `anti-bias.md` — ≥ 5 patterns required |
| 4 | **5 ideas cite the same paper** as primary | Ideas 1, 3, 7, 8, 10 all cite Wei et al. CoT | `anti-bias.md` — provenance diversity |
| 5 | **Only 2 distinct venues** (NeurIPS, ICLR) | All ideas | `anti-bias.md` — ≥ 3 venues |
| 6 | **Time-window collapse**: 10/10 papers `<12mo` | All ideas | `time-window.md` — ≥ 3 windows, must include older bands |
| 7 | **No falsification test on any idea** | All ideas | `verification.md` Step 5 — REJECT |
| 8 | **2 ideas have vague mechanism** ("better prompts", "try harder prompts") | Ideas 6, 10 | `verification.md` Step 5 + `checklists/per-idea.md` |
| 9 | **1 idea is a direct DUPLICATE** of published work | Idea 9 = Wang et al. SC K=40 | `verification.md` Step 1 — REJECT |
| 10 | **All ideas tagged 🟢 + Feas 5/5** | All ideas | `verification.md` §8 — over-confidence smell, batch downgrade |
| 11 | **No primary paper on Idea 6** | Idea 6 | `verification.md` Step 2 — REJECT |
| 12 | **Time-to-batch 6 min** | Header | `search-strategy.md` saturation detection — under-searched |

## What should have happened

After Step 3 (drafting), the per-idea checklist would have dropped Ideas 6 and 10 (no primary paper / vague mechanism). The verification pipeline would have rejected Idea 9 (DUPLICATE). The cross-idea consistency pass (§8 of `verification.md`) would have flagged the pattern collapse (8× P1) and the score-distribution sanity failure (everything 🟢, 5/5).

The skill would then either:
1. Re-search with focused queries for Tier-2 (adjacent benchmarks) and Tier-3 (cross-domain) — `search-strategy.md` §Re-search.
2. Or surface `⚠️ Diversity gates failed — only 3 patterns, 0 cross-domain, all-recency` at the top of `Notes & warnings` and present a partial batch.

Neither happened here — that is the bug.

## Fix recipe

1. Set **`--tier-quota strict`** to enforce hard quota at search time.
2. Run **reverse-search pass** (`anti-bias.md`) to add at least one P2 (Transfer) and one P6 (Verify) idea from outside the prompting family.
3. Require **time-window spread** by adding queries like `"MATH" reasoning <pre-2023>` to surface older techniques.
4. Force per-idea falsification field before allowing entry into the verification pipeline (handled by `checklists/per-idea.md`).
5. After fix, expected output should look like [./good-batch-MATH500.md](./good-batch-MATH500.md).
