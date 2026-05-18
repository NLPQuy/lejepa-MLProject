---
name: toy-experiment-design-template
description: Toy-experiment design block emitted when Stage 8 verdict = TOY
load-trigger: Stage 8 branch-block when verdict = TOY EXPERIMENT FIRST
---

# Toy Experiment Design Template

Use this block inside the per-idea report when Stage 8 verdict = `TOY`. It is also referenced by the **Toy queue** in `batch-summary.md`.

```markdown
## Toy Experiment Design

**Idea being toyed**: <title>
**Triggered by**: <which Stage(s) WARNed and why — name the specific uncertainty>

### Goal
Validate **<specific assumption>** cheaply, BEFORE committing the full budget.

### Setup
- **Dataset**: <subset — e.g., 50 random problems sampled from MATH-500 test set>
- **Model**: <same model as the user's target — e.g., gpt-4o-mini>
- **Config**: <minimum settings — e.g., K=5 instead of K=100; single seed unless variance is the uncertainty>
- **Budget**: $<X> (must be < 10% of full budget)
- **Wallclock**: <Y> hours

### Success criterion
Toy must show ≥ **<P>%** of the full-run expected gain.
- Example: full expected gain = +1.5pp; toy criterion = ≥ 30 % = ≥ +0.45pp on the 50-problem subset.
- If toy gain ≥ criterion → **FULL SEND** with confidence ↑.
- If toy gain ∈ (noise, criterion) → **tune & retry once** (1 more toy round at slightly higher K/N).
- If toy gain ≤ noise → **FALSIFY** → **KILL** (idea formally rejected, append to `_killed_ideas.md`).

### Confound check (run BEFORE the headline toy)
- **Noise estimate**: run 3 baseline seeds on the same 50-problem subset.
- Required for significance: toy gain ≥ 2 × measured noise.
- If 50-problem-subset noise > 50 % of the expected gain → the subset is too small to discriminate; **bigger toy needed** (e.g., 150 problems instead of 50).

### Falsification thresholds (numeric — fixed before running)

| Observation | Action |
|-------------|--------|
| Toy gain ≤ noise | FALSIFY → KILL → append to `_killed_ideas.md` |
| Toy gain ∈ (noise, criterion) | One more toy round (K↑ / N↑); cap at 2 toy rounds total |
| Toy gain ≥ criterion | Promote to FULL SEND with confidence raised by one step |

### Estimated cost
$<X> ± 20 %

### Estimated time
<Y> hours wall-clock (including the 3-seed noise pre-check).

### Re-vet trigger
After running this toy, the user passes `/vet-ideas --given-toy <toy-results-file> idea-<i>`. Vetting re-runs Stages 4, 5, 6 with the new evidence and emits a `vetting-v2.md` per `decision-logic.md §Versioning`.
```

## Hard rules

- **Budget must be < 10 % of full budget.** A toy that costs 50 % of the full run is not a toy — it is a small full run. Re-design.
- **Falsification thresholds must be numeric and fixed BEFORE the toy runs.** Post-hoc threshold-shifting defeats the purpose.
- **Confound check is mandatory.** A 3-seed baseline pre-run on the same subset must precede the headline toy, OR the noise estimate must come from a cited prior baseline on the same benchmark.
- **Cap at 2 toy rounds total.** If round 2 still cannot discriminate, the idea moves to KILL or REFRAME — do not let toys spiral into half-runs.
