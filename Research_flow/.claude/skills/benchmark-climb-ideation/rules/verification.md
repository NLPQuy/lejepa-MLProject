---
name: verification
description: Per-idea 7-step verification pipeline with explicit REJECT/DOWNGRADE/KEEP rules
load-trigger: Step 4 of SKILL.md workflow
---

# Verification Pipeline

For EACH draft idea, run checks 1–7 **in order**. Stop early on the first REJECT — do not waste budget verifying a dead idea.

After all ideas processed, run §8 cross-idea consistency. Then emit a verification report using [../templates/verification-report-template.md](../templates/verification-report-template.md).

## Decision vocabulary

Every check emits exactly one of:
- **KEEP** — passes as-is.
- **DOWNGRADE** — keep the idea, but adjust a field (feasibility score, gain estimate, confidence color, ranking) and add a warning.
- **REJECT** — remove the idea from the batch and log the reason to `_logs/_rejection_log.md`.

When unsure between KEEP and REJECT → REJECT. Better to under-propose than over-claim.

---

## 1. Novelty check

**Question**: has anyone published the exact idea already?

**Method**:
- WebSearch on `<key technique> + <benchmark>`.
- Search arXiv + Semantic Scholar with idea keywords.
- Inspect what the cited source papers themselves cite — does a close-equivalent appear there?

**Decision rule**:
- Exact prior paper (same technique + same benchmark + same setting) → **REJECT** (tag `DUPLICATE`). Exception: if that paper is < 6 months old AND no independent replication exists, may **KEEP** and recast as "replicate + extend".
- Closely related paper (same technique, different benchmark or model scale) → **KEEP** with tag `EXTENDS`; rewrite the one-liner as "X-style approach applied to Y".
- Nothing found → **KEEP** with tag `NOVEL`.

**Output tag (required)**: `NOVEL` | `EXTENDS` | `DUPLICATE`.

---

## 2. Provenance check

**Question**: are the cited sources real and do they say what we claim?

**Method**: for every paper listed in the idea's `Source inspirations`:
- Resolve the arXiv ID / DOI / venue URL.
- Confirm title, authors, year, venue match.
- Skim abstract + relevant section to confirm the paper actually supports the claim made in `Why expected to improve`.

**Decision rule**:
- Link does not resolve OR arXiv ID does not exist → **REJECT** (tag `BROKEN_LINK`).
- Metadata wrong (year, venue, authors) but paper exists → **KEEP**, fix metadata in-place.
- Paper exists but does not say what we claim → **REJECT** (tag `MISREPRESENTED`).
- All checks pass → **KEEP** (tag `VERIFIED`).

If the **primary** paper is rejected → the whole idea is REJECT. A supporting/contrasting paper failing is **DOWNGRADE** (remove that citation, keep the idea).

**Output tag (required, per paper)**: `VERIFIED` | `BROKEN_LINK` | `MISREPRESENTED`.

---

## 3. Feasibility check

**Question**: can the user actually run this with their declared budget?

**Method**: compare the idea's implementation sketch against the user's stated compute / time / model-access / data constraints.

**Decision rule**:
- Compute requirement > declared budget by >2× → **DOWNGRADE** feasibility by ≥1 point, set confidence to 🔴 on the budget line, add warning.
- Required dataset not publicly available AND no equivalent substitute named → **REJECT**.
- Required model API unavailable to the user (e.g. closed-weights without access) → **DOWNGRADE**, suggest an open-model substitute in the warning.
- All constraints satisfiable → **KEEP**.

**Output (required)**: integer feasibility score `1`–`5` + a `flags: [...]` list (may be empty).

---

## 4. Expected gain sanity check

**Question**: is the estimated gain plausible?

**Method**: compare against gains reported by similar papers on the same or adjacent benchmarks; compare against the headroom remaining above the user's baseline.

**Decision rule**:
- `gain_high > (100 − baseline_score)` (claims more than the headroom) → **DOWNGRADE**, cap gain at headroom, set confidence 🔴.
- `gain_low < 0.5 pp` on the same benchmark → **DOWNGRADE**, add `marginal` flag.
- `gain_mid > 2 × (best comparable published gain)` → **DOWNGRADE**, set confidence 🔴 and rewrite the gain estimate.
- Within plausible range and consistent with cited papers → **KEEP**.

**Output (required)**: adjusted `gain_low / gain_mid / gain_high` (pp) + confidence color 🟢/🟡/🔴.

---

## 5. Falsification check

**Question**: is the idea falsifiable with a concrete, observable test?

**Method**: read the idea's `Falsification test` field. Ask:
- Is there a measurable observation named?
- Is there a numeric threshold?
- If the observation does NOT occur, would we genuinely abandon the idea?

**Decision rule**:
- Test is vague ("if it works, it works"; no threshold; no metric named) → **REWRITE**. If you cannot rewrite into a sharp test in one pass → **REJECT**.
- Test requires > 8 h wall-clock or > 50% of the user's compute budget just to falsify → **DOWNGRADE**, add `slow-falsify` flag.
- Sharp and cheap → **KEEP**.

**Output (required)**: `OK` | `REWRITTEN` | `SLOW` | `REJECT`.

---

## 6. Risk check

**Categories**: `technical`, `data`, `compute`, `reproducibility`, `ethics`.

**Method**: enumerate risks under each category. Assign severity `low` / `med` / `high` to each.

**Decision rule**:
- ≥ 1 `high`-severity risk → **KEEP** but **FLAG** prominently in the verification report.
- ≥ 3 `med`-severity risks → **DOWNGRADE** ranking by one slot.
- Any `ethics` risk → **CONSULT** user before delivery (do not auto-keep).
- No notable risks → **KEEP**.

**Output (required)**: severity summary `LOW` | `MED` | `HIGH` + risk bullet list with category labels.

---

## 7. Compliance check

**Question**: does the idea violate any constraint the user declared?

**Method**: compare against the user-stated constraint list (model whitelist, "prompting only", parallelization required, budget cap, eval-set size, etc.).

**Decision rule**:
- Hard violation (e.g. uses GPT-4o when user said "mini only") → **REJECT**.
- Soft violation (e.g. needs extra eng-time to parallelize) → **KEEP**, add `NOTE` listing the violation.
- No violations → **KEEP** with `PASS`.

**Output (required)**: `PASS` | `WARN` | `FAIL` + violations list.

---

## 8. Cross-idea consistency (run AFTER all per-idea checks)

- **Near-duplicate detection**: any two ideas with same pattern + same primary paper + differing only in hyperparameters → keep the higher-scored one, REJECT the other (log as `duplicate-within-batch`).
- **Contradiction detection**: any two ideas that prescribe opposite directions on the same knob (e.g. "K=200 samples" vs "K=5 samples") without a context that distinguishes them → flag for user review.
- **Score-distribution sanity**: if > 70% of ideas have feasibility 5/5 or all confidence 🟢 → **DOWNGRADE** the entire batch's confidence by one color and add an `over-confidence` warning. This is a calibration smell.

## Re-search trigger

If `verified_count < 5` after all checks:
1. Identify which pattern slot or tier the rejected ideas left empty.
2. Run a focused search restricted to that gap (single tier, single pattern family).
3. Generate replacement idea(s), re-run §1–§7 on each.
4. Max **2** re-search cycles per batch. After that, present the partial batch with a `⚠️ Under-quota` warning.

## Independence

Verify each idea as if reviewing someone else's submission. Apply the same threshold uniformly. Do not protect an idea because it is clever or because you generated it.
