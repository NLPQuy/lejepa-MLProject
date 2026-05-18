---
name: decision-logic
description: How Stage 8 synthesizes the final verdict from Stages 1-7
load-trigger: Stage 8 of the pipeline
---

# Decision Logic

Stage 8 applies these rules **in order**. The first matching rule wins. Do not re-order; do not skip.

## UNREBUTTED downgrade rule (apply BEFORE the priority rules)

After every stage executes its rebuttal loop (see [./rebuttal-loop.md](./rebuttal-loop.md)), audit the `Rebuttal-cycle summary` in the stage output and apply this downgrade to the stage's verdict **before** Stage 8 reads it:

| UNREBUTTED count in stage | Effect on that stage's verdict |
|---------------------------|--------------------------------|
| 0 | unchanged |
| 1 | demote one step: PASS → WARN, WARN → FAIL |
| 2 | stage cannot exceed WARN; if already WARN/FAIL, becomes FAIL |
| ≥ 3 | stage = FAIL regardless of other signals |

A "PASS" stage emitted with ≥ 1 UNREBUTTED attack is **invalid** — Stage 8 must reject the per-stage block as malformed and demand a re-run, OR apply this downgrade and proceed using the demoted verdict.

The downgrade applies to every stage 1-7. Stage 8 itself does not have rebuttal attacks (it is synthesis), so this rule does not affect Stage 8's own verdict.

## Priority rules (apply in order — first match wins)

0. **Stage 1 = FAIL with tag `not-an-idea`** → **KILL** (instant). The idea is an engineering / HP-sweep / measurement / refactor task with zero mechanism contribution. Reframe = "move to project prerequisites / `Notes & warnings`, not a vetted idea". `--climb-mode` does NOT override this — engineering work is engineering work regardless of mode, and vetting is not the gate for it.
1. **Stage 2 = FAIL** (hard duplicate) → **KILL**
2. **Stage 6 = FAIL** (killer baseline) → **KILL** unless a plausible "X combined with idea" reframe exists → **REFRAME**
3. **≥ 3 stages = FAIL** → **KILL**
4. **0 FAIL + ≤ 2 WARN + Stage 5 = PASS** → **FULL SEND**
5. **0 FAIL + 3-4 WARN** → **TOY EXPERIMENT FIRST**
6. **0 FAIL + ≥ 5 WARN** → **REFRAME** (something is misaligned even if no single stage failed)
7. **1 FAIL + others PASS/WARN** → **REFRAME** (if the FAIL stage is addressable) or **TOY** (if reframe target is unclear)
8. **2 FAIL** → **REFRAME or KILL** — depends on WHICH stages:
   - Stages 1 + 5 (problem + feasibility) FAIL → KILL.
   - Stages 3 + 7 (novelty + reviewer) FAIL → REFRAME with stronger delta.
   - Stages 4 + 6 (theory + baseline) FAIL → likely KILL (no mechanism + no win over baseline).
   - Stage 2 already handled by Rule 1.

## Stage weights (when the rules above are ambiguous)

Higher-weight stages (more decisive — a FAIL here is a hard signal):
- **Stage 2 (prior work)** — hard duplicate is unrecoverable.
- **Stage 6 (killer baseline)** — losing to a simpler baseline is unrecoverable in a head-to-head.
- **Stage 5 (feasibility)** — infeasibility blocks every other gain.

Lower-weight stages (more advisory — a WARN is often acceptable):
- **Stage 4 (theory)** — WARN is fine for engineering-mode ideas. In `--climb-mode`, theory gets even less weight.
- **Stage 7 (reviewer)** — only matters if the user's goal includes publication. In `--climb-mode --no-publish`, Stage 7 is skipped entirely.

## Confidence tags

After picking the verdict, attach a confidence:

🟢 **High** — verdict is robust to plausible adjustments. Triggers:
- Clear majority across stages (≥ 6 stages agree with the verdict direction).
- Stages 2 and 6 both give the same hard signal (both PASS or both FAIL).
- For TOY: toy budget is < 5% of full budget, so the verdict is cheap to test.

🟡 **Medium** — verdict stands but is sensitive to specific uncertainties. Triggers:
- Mixed signals (3-5 stages PASS, 3-5 stages WARN).
- Stage 4 lite version used (climb-mode).
- For TOY: toy budget is 5-20% of full — borderline cheap.

🔴 **Low** — verdict is the best guess but evidence is thin. Triggers:
- All stages WARN (no PASS, no FAIL — every signal is mid).
- Input idea was vague (Stage 1 had to reframe heavily before attacks could land).
- Stages give contradicting evidence (e.g., Stage 6 PASS but Stage 7 = 2 Reject).

If confidence is 🔴, the verdict **MUST** be accompanied by an explicit "low-confidence" note in the per-idea report and a recommendation to re-vet after the user provides more context (baseline numbers, prior batches, or constraints).

## Tie-breaking

When two rules above could apply with equal precedence (rare, given the explicit ordering), break ties in this order:
1. Prefer **TOY** over **KILL** (reversible beats irreversible).
2. Prefer **REFRAME** over **TOY** if the reframe is concrete (you can write the reframed idea in 2 paragraphs).
3. Prefer **KILL** over **FULL SEND** only when Rule 1, 2, or 3 fired.

## Auditability

Every Stage 8 verdict must cite the rule number that fired:
> "Verdict: TOY. Rule #5 fired (0 FAIL + 3 WARN: Stages 4, 5, 6). Confidence: 🟡 — Stage 6 close baseline drives the uncertainty."

If no rule fires cleanly (which should not happen with the 8 rules above), default to TOY with 🔴 confidence and a note explaining the ambiguity.

---

## Batch aggregation (apply after every idea in a batch has its Stage-8 verdict)

When vetting an N-idea batch, the per-idea verdicts are aggregated for `batch-summary.md` ([../templates/batch-summary.md](../templates/batch-summary.md)):

```
KILLED      = count of ideas with Stage-8 verdict = KILL
REFRAMED    = count of ideas with verdict = REFRAME
TOY         = count of ideas with verdict = TOY
FULL_SEND   = count of ideas with verdict = FULL SEND

survival_rate = (FULL_SEND + TOY) / N
```

REFRAMEDs do NOT count as survival — they are pending-re-vet and the user must explicitly resubmit them.

### Calibration thresholds

| Survival rate | Interpretation | Action |
|---------------|----------------|--------|
| < 30 % | Batch was weak | Suggest the user re-run ideation with `/propose-benchmark-ideas --avoid-patterns <killed patterns>` and `--reset` |
| 30-70 % | Healthy batch | Proceed |
| > 80 % | Possibly insufficient adversarial rigor | Spot-audit 1-2 of the FULL SEND ideas: did any Stage produce 0 attacks? If so, re-run that stage with hostile prompting |

### Batch-level priority assignment

Within the `FULL_SEND` set, assign integer priority ranks 1..K using composite score from the source ideation batch (Section 6.5 of the ideation plan), with vetting-confidence as tie-breaker. Within the `TOY` set, sort by `toy_cost` ascending — the cheapest toy gets the user's attention first.

## Diversification across batch (§8.5)

When the batch contains **≥ 3 FULL SEND ideas**, the user cannot implement all simultaneously. The skill MUST prefer the **top-3 across 3 distinct axes** (not the top-3 by a single metric):

| Slot | Axis | Tie-break |
|------|------|-----------|
| 🥇 Top FULL SEND | Composite score (from ideation) × vetting-confidence | Lower effort |
| ⚡ Fastest to validate | Lowest `toy_cost` from the TOY queue | Lowest wall-clock |
| 🎯 Highest expected value | `gain_mid × P(survive)`; `P(survive)` proxied by vetting-confidence color (🟢=0.8, 🟡=0.5, 🔴=0.2) | Highest novelty (Stage 3 score) |

Pick **3 distinct ideas** when possible. If two slots resolve to the same idea, take the next best for the duplicated slot. Only collapse to fewer than 3 cards if the batch genuinely has fewer than 3 candidates across the axes.

The remaining FULL SEND ideas stay in `_passed_ideas.md` as the **queue** — surfaced in `batch-summary.md` for transparency but not pushed as immediate recommendations.

## Decision irreversibility & resurrection

`KILL` decisions are append-only to `_logs/_killed_ideas.md`. The user can resurrect a killed idea by passing:

> `/vet-ideas --resurrect idea-<i> --counter-argument "<text>"`

The skill re-runs vetting using the user's counter-argument as a user-input rebuttal (per `./rebuttal-loop.md §User-input rebuttal`) on the stage that killed the idea. The re-vetted output is written as `vetting-v2.md` per `§Versioning` below.

## Versioning

Each vetting session emits one report. If the user re-vets after toy results or a resurrection:

```
vetting-output/<bench>/batch-<N>/idea-<i>/
  vetting-v1.md          # initial
  toy-results.md         # user-attached
  vetting-v2.md          # post-toy re-vet OR post-resurrection re-vet
```

`batch-summary.md` always points to the **latest** version per idea; older versions remain for audit.

