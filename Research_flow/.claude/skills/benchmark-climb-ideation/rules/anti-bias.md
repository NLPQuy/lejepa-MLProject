---
name: anti-bias
description: Hard, countable rules to prevent training-data bias from dominating the batch
load-trigger: Step 2 (during search) and Step 3 (during drafting) and Step 6 (ranking)
---

# Anti-Bias Mechanisms

Every rule below is **countable** — you can verify it by counting items in the batch, not by gut feel.

## Force-list rules (must hold before delivery)

### Venue diversity
- **≥ 3 distinct venues** across the final batch (count by `Source inspirations.Primary.venue`).
- **No more than 2 ideas from the same first-author institution.**
- **No more than 2 ideas with primary paper from the same lab** (Google, OpenAI, Meta, etc.).

### Time diversity
- **≥ 3 distinct time windows** represented across primary papers. Windows defined in [./time-window.md](./time-window.md): `<12mo`, `12-36mo`, `36-72mo`, `72+mo`.
- See `./time-window.md` for the per-window minimum-count quota.

### Technique diversity
- **≥ 5 distinct patterns** from `../patterns/pattern-catalog.md`.
- **No more than 2 ideas using the same pattern** in one batch.
- **≥ 3 distinct technique families** represented (e.g., prompting / inference-time-scaling / retrieval / fine-tuning / tool-use / search). Count by mechanism, not by paper.

### Tier diversity (search-tier, see `./search-strategy.md`)
- Tier 1 (in-field): 40-50 % of final batch.
- Tier 2 (adjacent): 30-40 %.
- Tier 3 (cross-domain): 20-30 %.
- Violation of any band → DOWNGRADE batch confidence + add warning.

## Reverse-search (run after Step 3 draft, before Step 4 verification)

1. Enumerate the technique families used by the draft batch.
2. Ask: "Which families that are popular elsewhere am I NOT using?" Reference `../patterns/pattern-catalog.md` (P1–P12).
3. If an obvious gap exists (e.g., zero `P9 Tool-use` ideas for a benchmark where execution would clearly help), run **1 focused search** to attempt adding one such idea.
4. Stop after 1 added idea or 1 search round — this is a calibration step, not a full re-search.

## Devil's-advocate (run after Step 6 ranking, before user-facing summary)

For the **top-1 idea by composite score**:
- Run 1 query: `"<key technique>" failure case OR negative result`.
- Run 1 query: `"<key technique>" limitation OR does not work`.
- If concerning evidence surfaces (a paper showing the technique under-performs on a related setting):
  - **DOWNGRADE** ranking by 1 slot.
  - Add the contrasting paper to the idea's `Source inspirations.Contrasting` field.
  - Note in the batch's `Notes & warnings` block.

## Confirmation-bias guard

When verifying provenance (`../rules/verification.md` §2):
- Do not rely only on the abstract — read the relevant section/figure.
- If unsure whether the paper actually supports the claim, mark `MISREPRESENTED` rather than `VERIFIED` and re-read. Defaulting to KEEP is the bias.

## Anchoring guard

If the user provides a hint ("I think MCTS would work"):
- Acknowledge the hint but do NOT skip multi-tier search.
- Run the full search; include hint-aligned ideas only if they surface naturally on their merits.
- If no hint-aligned idea passes verification, say so explicitly in `Notes & warnings`. Do not back-fill a weak version to please the user.

## Venue-blind ideation

- When ranking ideas in Step 6, the composite score uses gain × feasibility × (1/effort) × novelty. **Venue is NOT a ranking input.**
- Venue is a TIE-BREAKER only when two ideas have identical composite scores.
- Venue IS used to filter inputs (`./conference-tiers.md`) and to set trust tier (`./source-trust.md`). Filtering input ≠ ranking output.

## Audit at delivery

Before printing the user-facing summary, count each item above. If any fails:
1. Try to fix via 1 re-search round (if budget remains).
2. Otherwise, surface the failure as a warning at the top of `Notes & warnings` (e.g., `⚠️ Venue diversity: only 2 distinct venues — batch may be lab-clustered`).
