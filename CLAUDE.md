# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. It incorporates Andrej Karpathy's behavioral guidelines to reduce common LLM coding mistakes.

## Karpathy Guidelines for Claude
**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:
`1. [Step] → verify: [check]`
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

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

# Training harness (needed for scripts/train_lejepa_ablation.py and train_eval_vit_l.py)
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

The root `tests/` suite covers only the `lejepa/` package. The `stable-pretraining/` suite is independent with its own `pytest.ini`.

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
- `DeprecatedEppsPulley` in `epps_pulley.py` is a dead class kept for reference; ignore it.

**`lejepa.multivariate`** — extends univariate tests to high-dimensional embeddings:
- `SlicingUnivariateTest` ← **primary wrapper** — projects embeddings onto `num_slices` random unit vectors and applies any `UnivariateTest` to each slice. Seed is synchronized across DDP ranks via `all_reduce` to guarantee identical projections everywhere.
- `BHEP`, `BHEP_M`, `COMB`, `HZ`, `HV` — direct multivariate normality tests (alternatives to slicing).

`UnivariateTest.base` handles distributed averaging via `torch.distributed.nn.all_reduce`.

### Dual EppsPulley implementations

There are **two separate, independent implementations** of the Epps-Pulley test:
1. `lejepa.univariate.EppsPulley` — general-purpose, composable with `SlicingUnivariateTest`; lives in the `lejepa/` package
2. `stable_pretraining.methods.lejepa.EppsPulley` + `SlicedEppsPulley` — self-contained copy baked into the `LeJEPA` model class; does not import from the `lejepa/` package

The second implementation exists so `stable_pretraining.methods.lejepa` can be used without installing the `lejepa` package. Both are equivalent in math.

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
| `methods/lejepa.py` | **`LeJEPA` model class** — self-contained backbone + projector + loss |

Data flows as **dicts** (`{"image": ..., "label": ...}`) through all components so any intermediate value is accessible in callbacks.

### `LeJEPA` model API (train vs eval)

`stable_pretraining.methods.lejepa.LeJEPA` has different forward signatures per mode:

```python
# Training: pass global and local view lists separately
output = model(global_views=[img1, img2], local_views=[img3, img4, img5, img6])
output.loss.backward()
# output fields: loss, embedding, inv_loss, sigreg_loss

# Eval: pass a single images tensor
output = model(images=torch.randn(4, 3, 224, 224))
features = output.embedding  # [N, D]
```

The center for the invariance loss is computed from **global views only** (`all_projected[:n_global].mean(0)`). Global views are 224×224; local views are 98×98. `sigreg_target` controls which tensor gets the SIGReg loss: `"proj"` (default), `"embed"`, or `"both"`.

### Training entry points

**Minimal (self-contained, no stable-pretraining)**  
Described in `MINIMAL.md` — a ~130-line script using `timm`, `datasets`, `wandb`, and `hydra`.

```bash
python mnist.py +lamb=0.02 +V=4 +proj_dim=16 +lr=2e-3 +bs=256 +epochs=800
```

**Ablation runner (current executable path)**  
`scripts/ablations.py` renders sweep commands and `scripts/train_lejepa_ablation.py` runs local LeJEPA ablation smoke/training jobs. Run both from the **project root**; `train_lejepa_ablation.py` self-patches `sys.path` to find `stable-pretraining/`.

```bash
python scripts/ablations.py list
python scripts/ablations.py show epps
python scripts/ablations.py render epps
python scripts/ablations.py render epps --smoke
python scripts/ablations.py write-scripts --ready-only
python scripts/ablations.py summarize logs/ --metric val/knn_top1

python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 accelerator=cpu devices=1 precision=32
```

The canonical ablation baseline overrides live in `scripts/ablations/specs.py::BASE_OVERRIDES`. A spec's `status` field controls whether `write-scripts --ready-only` includes it.

The old markdown launch files under `scripts/launch_*_ablation.md` are
legacy/manual notes. Do not use `scripts/je.py`; older docs reference it, but
that file does not exist in this checkout.

**Legacy Hydra sweep note**  
`scripts/launch_inet10.py` generates a shell command for a multi-backbone sweep
on ImageNet-10, but the generated target references missing `scripts/je.py`.

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
| `sigreg_target` | `"proj"` | Where to apply SIGReg: `"proj"`, `"embed"`, or `"both"` |

Linear probe evaluation uses **concatenated CLS tokens from the last two layers** + `LayerNorm`, with AdamW at `lr=1e-3` and `weight_decay=1e-6`.
