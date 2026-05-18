---
name: pattern-catalog
description: 12 idea generation patterns for benchmark-climb ideation
load-trigger: Step 3 of SKILL.md workflow
---

# Idea Patterns (P1–P12)

Each idea in a batch MUST be tagged with exactly one of these patterns. See usage rules at the bottom.

## P1: Combine (A + B)
Take two existing techniques and combine them for synergy.
- **Effort**: M-L
- **Risk**: Integration may fight (e.g., conflicting decoding assumptions).
- **Example**: Self-consistency + process-reward-model scoring per step.

## P2: Transfer (T from D1 → D2)
Lift a technique from another domain and adapt it to the target benchmark.
- **Effort**: L
- **Risk**: Domain assumptions may not transfer (e.g., zero-sum vs. open-ended).
- **Example**: MCTS (game AI) → reasoning trace search for math.

## P3: Replace (C → C')
Swap one component in an existing pipeline; everything else stays.
- **Effort**: S-M
- **Risk**: Replacement may underperform on the held-out slice.
- **Example**: Greedy decoding → beam search of width 5 inside an agent loop.

## P4: Scale (up or down)
Change a single scale dimension (samples, depth, width, context).
- **Effort**: S (more compute) or M (less compute while holding quality).
- **Risk**: Diminishing returns; flat region may dominate.
- **Example**: Self-consistency K=20 → K=200 with early-stop at 50% agreement.

## P5: Decompose
Break the task into sub-tasks and solve each, then aggregate.
- **Effort**: M-L
- **Risk**: Errors compound across stages; aggregation step becomes the bottleneck.
- **Example**: Math problem → (extract knowns) → (identify unknown) → (solve algebraically) → (verify).

## P6: Verify
Add a verifier or judge on top of a base generator.
- **Effort**: M
- **Risk**: Verifier quality is the new ceiling; bad verifier worse than none.
- **Example**: Generate K candidate answers, grade each with a critic prompt, pick top-scored.

## P7: Iterate
Self-refine in a loop — generate, critique, edit, repeat until stable.
- **Effort**: M
- **Risk**: May diverge, oscillate, or loop without improving.
- **Example**: Reflexion / Self-Refine with a stop condition on critique-score plateau.

## P8: Specialize
Detect a subtype of the input, then route to a specialized handler.
- **Effort**: M-L
- **Risk**: Subtype detection itself can fail and corrupt the rest.
- **Example**: For MATH-500, detect algebra vs. geometry vs. combinatorics, dispatch to prompt-set tuned for each.

## P9: Tool-use
Augment the model with an external tool (calculator, code exec, retriever).
- **Effort**: M
- **Risk**: Tool interface failures (timeouts, parse errors) leak into the answer.
- **Example**: Program-of-Thought — model writes Python, executor returns the value, model formats.

## P10: Sampling strategy
Change the decoding or sampling distribution.
- **Effort**: S
- **Risk**: Higher variance; gains may not be reproducible.
- **Example**: Temperature sweep + nucleus-p tuning per problem-class.

## P11: ICL variations
Change the in-context examples: selection, ordering, formatting.
- **Effort**: S-M
- **Risk**: Exemplar choice is fragile; gains may not transfer across splits.
- **Example**: kNN-retrieved exemplars based on problem-embedding similarity.

## P12: Self-play / Self-improve
Use the model to generate training (or evaluation) data for itself.
- **Effort**: L-XL
- **Risk**: Distribution drift, mode collapse, reward hacking.
- **Example**: STaR — generate rationales, keep only those leading to correct answers, fine-tune on them.

## Usage rules

- **Max 2 ideas per pattern** in a single batch.
- **≥ 5 distinct patterns** required per batch.
- **Recommend ≥ 1 P2 (transfer) and ≥ 1 P6 (verify)** per batch — historically high-yield categories.
- If a candidate idea does not cleanly fit one of P1–P12, do NOT invent a new pattern label — either re-cast the idea, or skip it. **Do NOT relabel as the nearest pattern** (e.g., calling a hyperparameter sweep "P7 Iterate" or "Search") — that is mislabeling and lets engineering tasks slip through as research.

## NOT-an-idea filter (hard, applied before drafting)

The skill proposes **research ideas with a mechanism-level contribution**. The following are *engineering / infrastructure / measurement tasks* and must NOT be drafted as ideas, regardless of how useful they are:

1. **Hyperparameter sweeps / grid search / Bayesian-opt / ASHA / Hyperband** — even when framed as "find the optimal λ" or "measurement-first". These are prerequisites of any ablation, not contributions. If the user lacks a measured baseline, that is an *input gap* surfaced in `Notes & warnings`, not a batch entry.
2. **Just-train-longer / just-train-bigger** without a mechanism change (e.g., "100 ep → 300 ep" alone is not an idea; "300 ep + revised LR schedule motivated by X" might be).
3. **Re-run the existing pipeline with different seeds / on different hardware / with different logging**.
4. **Run an existing public method on the user's benchmark for comparison** — that is a baseline measurement; surface as a needed control in `Notes & warnings`.
5. **Code refactors / library swaps** with no behavioural change (e.g., "rewrite in JAX").

If the candidate "idea" reduces to any of the above, **drop it** and instead add a one-line entry to the batch's `Notes & warnings` under a **Prerequisites / measurements** sub-header. The ideation batch shrinks; that is the correct outcome. Do not pad the batch with engineering tasks to meet the 5–10-idea minimum — under-quota with a warning is the honest delivery.

**Self-check before adding an idea**: "Strip the search/grid/measurement framing. Is there a *mechanism* — a new component, a new loss, a new combination, a new objective, a new schedule motivated by a hypothesis — that the experiment would test? If no, drop it."

## Pattern fit for enhance vs greenfield

When the user supplies an `Existing pipeline` and the batch runs in `enhance-existing` mode (≥ 50% of ideas must modify the pipeline rather than redesign it), use the table below as a suggestive prior. It is NOT a hard rule — a P2 (Transfer) idea can be cast as `enhance-existing` if it lifts a sub-routine into an existing slot, and a P3 (Replace) idea can be cast as `greenfield` if it ends up rebuilding most of the pipeline. The decisive question is always: *does the idea name a specific component to modify, or does it replace the pipeline wholesale?*

| Pattern | Natural scope | Why |
|---------|---------------|-----|
| P3 Replace | enhance-existing | By definition, swap one component in place. |
| P6 Verify | enhance-existing | Adds a layer on top; original pipeline untouched. |
| P9 Tool-use | enhance-existing | Augments a stage with a tool; rest stays. |
| P10 Sampling | enhance-existing | Changes decoding inside an existing generator. |
| P11 ICL | enhance-existing | Edits prompts / exemplars for an existing call. |
| P4 Scale | enhance-existing | Knob-twist on an existing component. |
| P1 Combine | mixed | Combining can plug into existing pipeline OR fork a new one. |
| P7 Iterate | mixed | Wrapping existing pipeline in a refine loop is enhance-existing; a brand-new self-refine loop is greenfield. |
| P8 Specialize | mixed | Routing layer added is enhance-existing; full sub-pipeline trees per subtype is greenfield. |
| P2 Transfer | greenfield (default) | Bringing in a foreign technique usually reshapes the pipeline. |
| P5 Decompose | greenfield (default) | Re-decomposition typically replaces the existing stage layout. |
| P12 Self-play | greenfield | Generates new training/eval distributions — pipeline-level change. |
