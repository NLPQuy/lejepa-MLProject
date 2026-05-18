---
name: source-trust
description: 4-tier source trust hierarchy with batch-level quota
load-trigger: Step 2 (paper evaluation) and Step 4 (Provenance check)
---

# Source Trust Hierarchy

Every paper picked during search is tagged with a trust tier. Trust tier ≠ search tier (T1/T2/T3 in `./search-strategy.md`). Search tier = where the paper came from in the in-field/adjacent/cross-domain sweep. Trust tier = how reliable the paper itself is.

## Tier 1 — highest trust
- Tier-A* conferences (see [./conference-tiers.md](./conference-tiers.md)).
- JMLR, TPAMI, TACL, IJCV, T-RO.
- Big-lab papers (Google DeepMind / OpenAI / Anthropic / Meta AI / MSR) with > 50 citations.

## Tier 2 — medium trust
- Tier-A conferences.
- Workshop papers at A* venues.
- Preprints from established labs, > 6 months old (had time to surface issues).
- Industry tech reports (default position).

## Tier 3 — low trust (inspiration only)
- B-tier conferences.
- arXiv preprints < 6 months old (no peer review yet).
- Workshop papers at B-tier venues.
- Papers > 10 years old used for foundational-concept inspiration (Tier-3 by default, but `./conference-tiers.md` allows skipping venue check for these).

## Tier 4 — avoid (do not cite as primary)
- Blog posts, Medium articles.
- Lecture notes, slides.
- Papers with 0 citations after 1 year.
- Conference papers with no code/repo AND closed-model dependency.

## Batch-level quota

- **≥ 60 %** of ideas in the batch must trace to **Tier 1 or Tier 2** sources (count by primary paper).
- Tier 3 sources are OK as inspiration but must be flagged explicitly in the idea's `Source inspirations` block (e.g., `[T3 — early preprint]`).
- Tier 4 is essentially never cited as primary. Only acceptable as a "concept reference" (e.g., pointing to a blog that names a term coined elsewhere) and never as evidence of a claim.

## Trust-tier audit rule

Before emitting the verification report (Step 4):
1. Count primary-paper trust tiers across the batch.
2. If `(T1 + T2) / batch_size < 0.60` → **DOWNGRADE** the batch's overall confidence by one color AND surface a warning: `⚠️ Source-trust under-quota: <X>% T1+T2`.
3. Replacement via re-search is preferred; downgrade is the fallback when re-search budget is exhausted.
