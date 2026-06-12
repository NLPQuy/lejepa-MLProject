# Batch-1 experiments

Implements the **safe** subset of [../ideation/batch-1.md](../ideation/batch-1.md),
per [../ideation/plan-batch-1.md](../ideation/plan-batch-1.md) (Option 2: thin
runners + one jupytext orchestrator). exp1 was dropped (duplicate of the official
`AdversarialSIGReg`); variant logic lives here in `_variants.py` (not official source).

## Files
| File | Role |
|------|------|
| `_common.py` | Shared runner (transforms, dataset, forward, callbacks) — extracted from `benchmarks/imagenet10/lejepa-vit-small.py`. |
| `_variants.py` | `LeJEPACodingRate`, `LeJEPAUniformity`, `LeJEPADynTanhProj` (+ `coding_rate`, `uniformity_loss`, `DynTanh`). Imports only from `stable_pretraining`. |
| `exp_baseline.py` | Plain `LeJEPA` — sanity reference. |
| `exp3.py` | Idea 3 — coding-rate term (`--coding_beta`, 0 = baseline). |
| `exp4.py` | Idea 4 — uniformity term (`--uniformity_gamma`, 0 = baseline). |
| `exp7.py` | Idea 7 — DynTanh projector (`--dyntanh_alpha`; architectural swap, no off-switch). |
| `run-batch1.py` | Jupytext Kaggle offline orchestrator (uncomment one block per session). |

Not yet implemented (heavier / higher-risk — next round): exp2 (Cramér-Wold),
exp5 (EMA teacher), exp6 (dense patch), exp8 (NN positives), exp9 (AutoView),
exp10 (RankMe-gated λ).

## Comparison metrics (identical across all exps)
Online callbacks: `linear_probe/top1` (linear probe on frozen embedding),
`knn_probe/top1` (k=20), `rankme`. exp3/exp4 with weight=0 must equal `exp_baseline`.

## Smoke test (CPU, no GPU hours)
```bash
cd climb_bench/batch1
python exp3.py --accelerator cpu --num_gpus 1 --precision 32 \
    --max_steps 3 --batch_size 4 --num_workers 0 --coding_beta 0.01 \
    --data_local_path <local_imagenette> --no_wandb
```
> **Requires `torchvision==0.26.0`** (the repo-pinned version, as in the Kaggle
> wheels). Older torchvision (≤0.20) renames `v2.Transform.transform` and the
> shared data pipeline in `_common.py` (copied verbatim from the official
> baseline) will raise `'RandomResizedCrop' object has no attribute 'transform'`.
> Verified at the model level (forward/backward, `coding_beta=0` ==
> `uniformity_gamma=0` == baseline) on a real ViT backbone.

## Run (400 ep)
See `run-batch1.py` blocks, or invoke any `exp<x>.py` with
`--data_local_path <path> --checkpoint_dir <dir> --no_wandb`.
