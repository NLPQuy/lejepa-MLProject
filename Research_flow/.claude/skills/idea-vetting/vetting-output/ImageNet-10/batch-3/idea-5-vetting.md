# Vetting — Batch 3 Idea 5: Per-rank disjoint slices in DDP
**Pattern**: P4 · **Tier**: 2 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
- **Attack 1**: ⚠️ idea-or-engineering — proposal admits "does nothing at 1 GPU" (the current ImageNet-10 setup is 1 GPU per [stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py:115](stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py#L115)). At the actual target use case, gain = 0. **Rebuttal**: the *mechanism* is real (R× more effective MC samples per step) and the *code change* is correctness-positive (current seed-sync is reproducibility scaffolding, not algorithmic necessity). It's a default-on improvement for any multi-GPU run. ❌ **UNREBUTTED** — at the current Imagenette setup the idea is mechanism-inert; gain only cashes at ≥ 2 GPU.
- **Verdict**: WARN (UNREBUTTED — scope-mismatched with the named benchmark)

## Stage 2 — Prior Work Attack
- **Attack 1**: standard DDP best practice (e.g. PyTorch docs) is to break determinism for variance reduction; this idea reinvents it. **Rebuttal**: yes — this is *applying* a known DDP pattern to a specific subsystem (SIGReg slicing) that currently violates it. The mechanism transfer is the novelty, not the DDP pattern itself. **DEFLECTED**.
- **Verdict**: PASS

## Stage 3 — Novelty Decomposition
- Novel piece: removing the slice-seed `all_reduce` sync in `SlicingUnivariateTest`.
- Already published: nothing — but trivially obvious to any DDP practitioner once stated.
- Net novelty: EXTENDS (small).
- **Verdict**: WARN (low novelty)

## Stage 4 — Theory Grounding
- DDP gradient averaging is a sum-of-means → ✅ equivalent to R×M slices with the disjoint-seed variant.
- **Verdict**: PASS

## Stage 5 — Feasibility
- 2-line change. Trivial.
- **Verdict**: PASS

## Stage 6 — Killer Baseline (Skeptical Empiricist)
- Killer baseline: shared-seed (current) at same R.
- **Attack**: at the *named benchmark target* (ImageNet-10, 1 GPU), there is no comparison to run. The proposal's falsification test requires a 4-GPU setup that is not the current configuration. **Rebuttal**: proposal explicitly says "ship as default-on code change the next time the recipe runs on > 1 GPU" — not requesting compute for a vetting experiment now. ⚠️ **WEAKENED** — the deliverable is decoupled from the named benchmark.
- **Verdict**: WARN (scope mismatch with named benchmark)

## Stage 8 — Decision Gate
- FAIL: 0 · WARN: 3 (Stage 1 scope mismatch, Stage 3 low novelty, Stage 6 not-testable-here) · UNREBUTTED: 1
- Per `decision-logic.md`: with 1 UNREBUTTED at Stage 1 and the gain being zero at the named benchmark, the correct routing is **REFRAME** — not as a research idea on ImageNet-10, but as a code-correctness fix shipped with the next multi-GPU run.
- Confidence: 🟡

## Final verdict: 🔁 **REFRAME** 🟡
- Reframe: this is **not a research idea on ImageNet-10**. It is a *correctness/quality default* for the SIGReg slice generator. Ship as a small PR alongside any future multi-GPU recipe (ImageNet-1K, ViT-L runs from `train_eval_vit_l.py`). Add a unit test asserting `slices_rank_0 ≠ slices_rank_1` after the change.
- Do NOT spend an ImageNet-10 experiment slot on this. The vetting verdict stops short of KILL because the mechanism is correct and the change is positive-EV at the relevant compute regimes.
- If the user disagrees and wants to validate on multi-GPU ImageNet-10, the falsification test in the proposal (≥30 % per-step SIGReg-var reduction at 4 GPU) is sharp and runnable.
- Composite × confidence: 2.6 × 0.6 = 1.56 (deflated by scope mismatch)
