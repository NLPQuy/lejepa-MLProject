# Implementation Plan — Batch 2 (Imagenette / LeJEPA optimizer + architecture)

**Source ideas**: [batch-2.md](batch-2.md) (10 ideas, all `enhance-existing`, OPTIMIZER/TRAINING-GEOMETRY + ARCHITECTURE only)
**Target**: jupytext experiment files `exp<x>.py` under `climb_bench/batch2/`, uploaded to Kaggle, run **offline** (torchvision 0.26 pinned wheels).
**Hard rule (same as batch-1)**: variant/mechanism logic goes in a **batch-local** `climb_bench/batch2/_variants.py`; the official `stable_pretraining/methods/lejepa_variants.py` is **NOT** touched. Runners only import + wire. `_common.py` is reused/extended from batch-1.

> **Do not implement yet — await user approval of this plan.**

---

## 0. Key difference from batch-1: most ideas wire at the OPTIMIZER, not the model

Batch-1 mechanisms were all model-side (`model.sigreg = …`, `LeJEPA(projector=…)`, `LeJEPAxxx(_compute_loss)`). Batch-2 splits into **two wiring surfaces**:

- **Model-side** (same 3 swap mechanisms as batch-1): QK-Norm, conv-stem, deep-supervision.
- **Optimizer/trainer-side** (new for batch-2): SAM, Muon, Schedule-Free, PCGrad, SWA, LLRD, stochastic-depth schedule. These wire in **`_common.py`'s optim config / callback stack inside `spt.Module`**, or via a `pl.Callback`, **not** by swapping a model submodule.

So `_common.py` gains:
- an `--optimizer {adamw,muon,schedulefree,sam}` switch + builder that returns the right optimizer (and, for SAM, flips Lightning to **manual optimization**),
- an LLRD `param_groups` builder (`--llrd_gamma`),
- a callback registry (`--swa`, `--sd_schedule`) appended to the existing OnlineProbe/OnlineKNN/RankMe stack,
- PCGrad as a `LeJEPAPCGrad(LeJEPA)` subclass that does two backward passes in its own `training_step` (manual optimization).

Everything keeps an **off-switch == exact baseline** (flag default reproduces stock AdamW+cosine / stock ViT-S), verified by identical 1-epoch loss, per the batch-1 convention.

---

## 1. Per-idea implementation map

Legend — **Surface**: `optimizer` | `param-group` | `callback` | `backbone-ctor` | `backbone-surgery` | `subclass`.
All "new code" lands in `climb_bench/batch2/_variants.py` (mechanism) or `_common.py` (wiring), never in official source.

| exp | Idea (batch-2 #) | Surface | New thing in `batch2/_variants.py` (or `_common.py`) | Runner does |
|-----|------------------|---------|------------------------------------------------------|-------------|
| exp2 | #2 QK-Norm | backbone-ctor | — (use timm `qk_norm=True` kwarg) | build `LeJEPA(...)` with backbone kwarg `qk_norm=True` behind `--qk_norm` |
| exp4 | #4 Schedule-Free AdamW | optimizer | `build_schedulefree(params, args)` in `_common.py` + train/eval mode hooks | `--optimizer schedulefree` |
| exp3 | #3 Muon | optimizer + param-group | `build_muon(model, args)` (Muon for 2-D, AdamW for 1-D) | `--optimizer muon` |
| exp1 | #1 SAM | optimizer (manual-opt) | `SAMWrapper` + manual `training_step` in `_common.py` | `--sam_rho 0.05 [--sam_late]` |
| exp5 | #5 PCGrad | subclass (manual-opt) | `LeJEPAPCGrad(LeJEPA)` — two backward, project conflicting grads | instantiate subclass, `--pcgrad` |
| exp7 | #7 SWA + RankMe gate | callback | `RankMeGatedSWA(pl.Callback)` (wraps Lightning `StochasticWeightAveraging`) | `--swa [--swa_rank_gate]` |
| exp8 | #8 LLRD | param-group | `build_llrd_param_groups(model, gamma)` in `_common.py` | `--llrd_gamma 0.75` |
| exp9 | #9 Progressive stochastic depth | callback | `DropPathScheduler(pl.Callback)` mutating `block.drop_path.drop_prob` | `--sd_schedule linear` |
| exp6 | #6 Conv stem | backbone-surgery | `ConvStem(nn.Module)` + replace `backbone.patch_embed` post-init | `--conv_stem` |
| exp10 | #10 Deep supervision | subclass | `LeJEPADeepSup(LeJEPA)` (taps blocks {6,9} via `get_intermediate_layers`, μ-weighted SIGReg+inv) | instantiate subclass, `--deepsup_mu 0.1 --deepsup_layers 6,9` |

**Notes / risks baked into the plan**
- **exp4 Schedule-Free**: the optimizer needs `optimizer.train()` before training forward and `optimizer.eval()` before any validation/probe forward (averaged weights). Wire into `on_train_epoch_start` / `on_validation_start`. Forgetting this silently evaluates wrong weights → the OnlineProbe/kNN numbers become invalid. **Add an assertion/log of which iterate is active at eval.**
- **exp3 Muon**: needs a small Muon impl (single-file, public; ~60 lines incl. Newton–Schulz). Param split: 2-D matrices (attn/MLP/projector weights) → Muon; norms/biases/CLS/pos-embed/embeddings → AdamW. One calibration of the Muon-vs-AdamW LR ratio (single value, not a grid).
- **exp1 SAM**: requires `automatic_optimization=False` in `spt.Module` (or a SAM-aware optimizer step). This is the most invasive trainer change; isolate it so the other exps keep automatic optimization. Offer `--sam_late` (only last ~30% epochs) to bound the 2× cost.
- **exp5 PCGrad**: also manual-opt; two backward passes (`inv_loss`, `λ·sigreg`) with `retain_graph`. Project at the shared-trunk grads to limit memory. Off-switch `--pcgrad` absent ⇒ plain summed loss == baseline.
- **exp7 SWA**: use Lightning's `StochasticWeightAveraging` for the averaging machinery; the custom `RankMeGatedSWA` only decides the `swa_epoch_start` (fallback: fixed last-25%). **Constant LR during the SWA window** (not cosine tail) + **BN-stat recompute** for the projector before checkpointing.
- **exp6 conv-stem**: replace `backbone.patch_embed` with a stride-product-16 conv stack (e.g. 3×{3×3,s2}+1×{1×1}) → 14×14×384 to match token count & pos-embed shape. Verify pos-embed length and flops parity before the 400-ep run. Report honestly that the frozen backbone is "ViT-S body + conv stem".
- **exp2 QK-Norm**: cheapest — likely just `timm.create_model("vit_small_patch16_224", qk_norm=True, ...)`. Confirm the repo's backbone builder forwards the kwarg; if not, set `block.attn.q_norm/k_norm` after creation.

---

## 2. Shared runner contract (`_common.py` additions)

Reuse the batch-1 `_common.py` (transforms, dataset, `lejepa_forward`, OnlineProbe+OnlineKNN+RankMe, `run()`). Add:
- `build_optimizer(model, args)` dispatching on `--optimizer {adamw,muon,schedulefree,sam}` and applying `--llrd_gamma` param-grouping when set.
- A `--manual_opt` path (SAM, PCGrad) that switches `spt.Module` to manual optimization; keep the default automatic path untouched for all other exps.
- Optional callbacks appended by flag: `RankMeGatedSWA` (`--swa`), `DropPathScheduler` (`--sd_schedule`).
- Schedule-Free train/eval mode hooks gated on `--optimizer schedulefree`.

Each `exp<x>.py` stays ~30 lines: `get_args()` (+ exp knob) → build model (stock `LeJEPA` for optimizer-side exps; subclass for exp5/exp10; ctor-kwarg/surgery for exp2/exp6) → `run(model, args, tag)`.

```python
# exp3.py (Muon) example
from _common import get_args, run
from stable_pretraining.methods.lejepa import LeJEPA
def main():
    args = get_args()                       # --optimizer muon set on the CLI
    model = LeJEPA(encoder_name=args.backbone, lamb=args.lamb,
                   n_slices=args.n_slices, projector_dim=args.proj_dim)
    run(model, args, tag="exp3-muon")       # _common.build_optimizer reads args.optimizer
if __name__ == "__main__": main()
```

---

## 3. Evaluation consistency (unchanged from batch-1)

- Primary comparison = the online callbacks already in `run()` (`linear_probe/top1`, `knn_probe/top1`, `rankme`), **identical config across all exps** → apples-to-apples. The optimizer/architecture changes must not touch probe settings.
- For exp7 (SWA) and exp4 (Schedule-Free), eval **must read the averaged iterate** (SWA-averaged weights / schedule-free `eval()` mode), or the comparison is invalid — this is the single biggest correctness risk in the batch.
- 400-epoch pretrain; checkpoint every `max_epochs//2`; resume across Kaggle ≤12 h sessions.

---

## 4. Kaggle offline runbook (`run-batch2.py`)

Clone `climb_bench/batch1/run-batch1.py` (which itself derives from `lejepa-nointernet-setup.py`). Per [[kaggle-jupytext-convention]]:
- **Double-`#`** every `!python …`/`!pip …` block (`# # !python …`) so "Run All" stays inert; user deletes one `# ` per session.
- No `[...]` in `# %%` cell titles.
- Set `PYTHONPATH` to both `stable-pretraining` and `climb_bench/batch2`; `SPT_LIGHT_IMPORT=0`; stub `requests_cache`.
- **extra wheel**: `schedule_free` for exp4 — add to the `--no-deps` wheel install cell.
- One run-block per exp pointing at `climb_bench/batch2/exp<x>.py`, `--no_wandb` (CSV) offline.

---

## 5. Build & verification order (goal-driven)

1. **Extend `_common.py`** (`build_optimizer`, manual-opt path, callback flags) → smoke: `exp_baseline.py` (stock LeJEPA, `--optimizer adamw`) reproduces batch-1 baseline on 1 epoch. *Verify*: probe metric logged.
2. **Cheap, low-risk first**: exp2 (QK-Norm), exp8 (LLRD), exp9 (stoch-depth) — each off-switch == baseline (1-epoch loss parity), then on. *Verify*: forward/backward, flags toggle correctly.
3. **Optimizer swaps**: exp4 (Schedule-Free — assert eval reads averaged iterate), exp3 (Muon — param split correct, RankMe logged). *Verify*: no NaN, loss decreases over 3 steps.
4. **Manual-opt exps**: exp1 (SAM — 2× backward, `--sam_late`), exp5 (PCGrad — conflict-frequency log). *Verify*: one manual step updates weights without error.
5. **Heavier / risk-flagged**: exp7 (SWA — BN recompute + averaged-weight eval), exp6 (conv-stem — token/pos-embed/flop parity), exp10 (deep-sup — μ=0 == baseline). Gate behind `/idea-vetting` before full 400-ep runs.
6. Local smoke only at **model/optimizer level** (torchvision 0.26 mismatch blocks the full data pipeline locally — see [[kaggle-jupytext-convention]]); full runs on Kaggle.

**Success criterion**: every `exp<x>.py` (a) imports its mechanism from `batch2/_variants.py` or wires it via `_common.py`, (b) passes a 1-epoch / `max_steps=3` smoke, (c) reduces to baseline when its flag is off (where applicable), (d) runs unchanged under `run-batch2.py` offline, (e) for exp4/exp7, eval is verified to read the averaged iterate.

---

## 6. Open decisions for you (resolve before coding)

1. **Build scope first**: all 10, or the 4 low-risk drop-ins (exp2 QK-Norm, exp8 LLRD, exp9 stoch-depth, exp7 SWA) + baseline first? (Recommend the 4 + baseline.)
2. **Manual-optimization exps** (SAM exp1, PCGrad exp5): OK to add a `--manual_opt` branch to the shared `spt.Module`, or keep these two in a separate runner to avoid touching the common training_step?
3. **Muon source**: vendor a small single-file Muon impl into `batch2/_variants.py`, or add `muon`/`schedule_free` as pinned Kaggle wheels?
4. **SAM cost**: default to `--sam_late` (last 30%, ~1.3× cost) rather than full SAM (2×)?
5. **Compose later?**: Muon (exp3) + QK-Norm (exp2) and SWA (exp7) + Schedule-Free (exp4) are orthogonal — keep all exps single-variable for now, or pre-plan one "stack the winners" run after ranking?
