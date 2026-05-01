# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**LeJEPA** is a self-supervised learning library implementing *Sketched Isotropic Gaussian Regularization* (**SIGReg**), the core objective of the paper [arXiv:2511.08544](https://arxiv.org/abs/2511.08544). The repository contains:
- `lejepa/` — the pip-installable core library of statistical tests
- `stable-pretraining/` — a PyTorch Lightning training harness (separate package)
- `train_eval_vit_l.py` — a Kaggle/Colab-oriented training script for ViT-L on ImageNet-1K
- `scripts/` — Hydra-based sweep launchers

## Installation

```bash
# Core library only
pip install lejepa

# Or from source
pip install -e .

# Training harness (needed for scripts/je.py and train_eval_vit_l.py)
cd stable-pretraining && pip install -e .

# Minimal example dependencies
pip install torch torchvision timm wandb hydra-core datasets huggingface-hub
```

## Running Tests

```bash
# All tests (root-level, for the lejepa package)
pytest tests/

# Single test file
pytest tests/test_epps_pulley.py

# Single test class / function
pytest tests/test_epps_pulley.py::TestEppsPulley::test_standard_normal_samples_low_statistic

# stable-pretraining tests (separate test suite with pytest.ini)
cd stable-pretraining && pytest
```

## Architecture

### Core idea

The LeJEPA training loss is:

```
LeJEPA_loss = λ · SIGReg(proj) + (1 − λ) · Invariance(proj)
```

where:
- **Invariance loss** — forces multi-view projections to agree: `(proj.mean(0) - proj).square().mean()`
- **SIGReg** — regularizes projections toward N(0, I) using a univariate ECF (empirical characteristic function) test applied across random 1-D slices of the embedding space

`λ` is the single tunable hyperparameter (typically `0.01–0.1`).

### `lejepa/` package

Two submodules, both exposing `torch.nn.Module`-compatible loss functions:

**`lejepa.univariate`** — goodness-of-fit tests comparing a 1-D sample to N(0,1):
- `EppsPulley` ← **primary test used by SIGReg** — computes the L² distance between the empirical characteristic function and the standard normal CF, integrated over `[0, t_max]` with precomputed trapezoid weights. Exploits symmetry of the CF to halve the integration domain.
- Others (`AndersonDarling`, `CramerVonMises`, `ShapiroWilk`, `Watson`, `Moments`, `NLL`, `ExtendedJarqueBera`, `VCReg`) share the `UnivariateTest` base class.
- All tests take input shape `(N, K)` and return shape `(K,)` — they test each of the K columns independently.

**`lejepa.multivariate`** — extends univariate tests to high-dimensional embeddings:
- `SlicingUnivariateTest` ← **primary wrapper** — projects embeddings onto `num_slices` random unit vectors and applies any `UnivariateTest` to each slice. Seed is synchronized across DDP ranks via `all_reduce` to guarantee identical projections everywhere.
- `BHEP`, `BHEP_M`, `COMB`, `HZ`, `HV` — direct multivariate normality tests (alternatives to slicing).

`UnivariateTest.base` handles distributed averaging via `torch.distributed.nn.all_reduce`.

### `stable-pretraining/` package

A full PyTorch Lightning training framework used by the experiment scripts. Key modules:

| Module | Role |
|--------|------|
| `module.py` / `Module` | Lightning module wrapping encoder + projector + loss |
| `manager.py` / `Manager` | Orchestrates training runs, Hydra config, logging |
| `data/` | `HFDataset`, `FromTorchDataset` — dict-structured datasets |
| `backbone/` | timm model wrappers; `TeacherStudentWrapper` for EMA |
| `losses/` | Loss registry |
| `callbacks/` | `OnlineProbe`, `OnlineKNN`, `RankMe`, `LiDAR`, `ImageRetrieval`, `EarlyStopping` |
| `optim/` | Optimizer + scheduler builders |
| `static.py` | `TIMM_PARAMETERS` dict mapping backbone names → parameter counts |
| `cli.py` / `run.py` | Entry points for Hydra CLI |

Data flows as **dicts** (`{"image": ..., "label": ...}`) through all components so any intermediate value is accessible in callbacks.

### Training entry points

**Minimal (self-contained, no stable-pretraining)**  
Described in `MINIMAL.md` — a ~130-line script using `timm`, `datasets`, `wandb`, and `hydra`.

```bash
python mnist.py +lamb=0.02 +V=4 +proj_dim=16 +lr=2e-3 +bs=256 +epochs=800
```

**Full (stable-pretraining + Hydra sweeps)**  
`scripts/launch_inet10.py` generates the shell command for a multi-backbone sweep on ImageNet-10:

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py \
  --config-dir scripts/configs --config-name base \
  +accelerator=single_gpu_sc \
  ++bstat_name="epps_pulley" ++bstat_num_slices=1000 \
  ++dataset_name="inet10" ++max_epochs=400 ++batch_size=512 \
  ++bstat_lambda=0.02 ++lr=3e-3 ++weight_decay=3e-2
```

**Kaggle / large-scale (train_eval_vit_l.py)**  
Jupytext `.py` notebook targeting Kaggle with ImageNet-1K loaded as a local `ImageFolder`. Sets `HF_DATASETS_CACHE=/dev/shm` for RAM-based caching and uses `GITHUB_TOKEN` / `HF_TOKEN` secrets for repo + hub access.

## Key Hyperparameters

| Param | Recommended | Notes |
|-------|-------------|-------|
| `λ` (lambda) | `0.02` | Balance SIGReg vs invariance; lower = more invariance |
| `lr` | `5e-4` | AdamW; use linear warmup + cosine annealing |
| `weight_decay` | `5e-2` (ViT), `5e-4` (ResNet) | |
| `num_slices` | `1024` | More slices = stronger test, higher cost |
| `n_points` (EppsPulley) | `17` | Integration quadrature points (must be odd) |
| `V` (num views) | `8` (2 global + 6 local) | Multi-crop DINO-style augmentation |
| precision | `bfloat16` | Stable without gradient clipping |

Linear probe evaluation uses **concatenated CLS tokens from the last two layers** + `LayerNorm`, with AdamW at `lr=1e-3` and `weight_decay=1e-6`.
