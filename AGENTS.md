# Repository Guidance

## Project Shape

This repository combines the LeJEPA paper/code artifacts with a small Python package:

- `lejepa/`: root Python package for statistical normality-test losses used by SIGReg.
- `tests/`: root-level pytest suite for `lejepa`.
- `stable-pretraining/`: separate vendored package/training harness with its own `pyproject.toml`, `pytest.ini`, docs, tests, and CLI entry point.
- `arXiv-2511.08544v3/`, `arXiv-2603.19312v2/`, `slides*.tex`: paper and slide sources plus generated LaTeX outputs.
- `figures/`, `eval/`: figure generation scripts and rendered media.
- `scripts/`: current ablation notes and launch helpers. Some older docs mention `scripts/je.py` and `scripts/configs`, but those files are not present in the current tree.

Treat `CLAUDE.md` as useful background, but verify paths against the current tree before following any command from it.

## Core Package

`lejepa` exports two subpackages:

- `lejepa.univariate`: `torch.nn.Module` tests for 1-D samples against `N(0, 1)`, including `EppsPulley`, `AndersonDarling`, `CramerVonMises`, `ShapiroWilk`, `Watson`, `Moments`, `NLL`, `ExtendedJarqueBera`, and `VCReg`.
- `lejepa.multivariate`: high-dimensional tests, especially `SlicingUnivariateTest`, which projects embeddings onto random unit vectors and applies a univariate test per slice.

Expected tensor convention:

- Univariate tests generally take input shaped `(N, K)` and return `(K,)`.
- `SlicingUnivariateTest` takes `(..., N, D)` and returns a scalar for `reduction="mean"` or `"sum"`, or `(..., num_slices)` for `reduction=None`.

Distributed behavior matters. `UnivariateTest` and `SlicingUnivariateTest` include DDP-aware reductions / synchronized projection seeds; avoid changing those paths without running focused tests.

## Setup

For root package work:

```bash
pip install -e .
```

Root `pyproject.toml` declares `torch`, `numpy`, `loguru`, and `pytest`. Several tests also import `scipy`, so a local test environment may need:

```bash
pip install scipy
```

For the training harness:

```bash
cd stable-pretraining
pip install -e .
```

`stable-pretraining` has many ML/training dependencies and is maintained as a separate package. Only edit it when the requested change is clearly about that harness.

## Test Commands

Root package:

```bash
pytest tests/
pytest tests/test_epps_pulley.py
pytest tests/test_epps_pulley.py::TestEppsPulley::test_standard_normal_samples_low_statistic
```

DDP test:

```bash
python tests/test_ddp.py
```

The DDP script uses CUDA/NCCL and skips practical execution when no GPUs are available.

Training harness:

```bash
cd stable-pretraining
pytest
```

This follows `stable-pretraining/pytest.ini` and can include slower integration/GPU/download tests depending on markers and environment.

## Build / Packaging Notes

There is a metadata mismatch:

- `pyproject.toml` names the root project `lejepa`.
- `setup.py` names it `deepstats`.

Prefer `pyproject.toml` / editable install behavior unless a task explicitly concerns legacy packaging. Do not silently rename package metadata in unrelated changes.

## Research / Training Entrypoints

- `MINIMAL.md` documents a self-contained LeJEPA example with ViT, Imagenette, `timm`, `datasets`, Hydra, and W&B.
- `train_eval_vit_l.py` is a Jupytext/Kaggle-oriented large training/eval script. It contains environment-specific paths and secrets-style token placeholders/hardcoded values; do not propagate or expose those values.
- `scripts/ablations.py` is the current executable ablation runner/renderer. Useful commands include `python scripts/ablations.py list`, `python scripts/ablations.py render epps`, and `python scripts/ablations.py write-scripts --ready-only`.
- `scripts/train_lejepa_ablation.py` is the local LeJEPA ablation smoke/training entrypoint used by rendered commands; it supports synthetic smoke runs and ablation knobs exposed in `scripts/ablations/specs.py`.
- `scripts/launch_inet10.py` prints a Hydra command based on `stable_pretraining.static.TIMM_PARAMETERS`, but its target command references missing `scripts/je.py` in this checkout.
- `scripts/launch_*_ablation.md` and older ablation markdown files are legacy/manual launch notes, not the preferred executable path.
- Do not use `scripts/je.py`; it is referenced by older notes but does not exist in this checkout.

## Paper And Slide Work

Primary LaTeX sources:

- `arXiv-2511.08544v3/main.tex` with section files in `arXiv-2511.08544v3/content/`.
- `arXiv-2603.19312v2/main.tex` with section files in `arXiv-2603.19312v2/sections/`.
- `slides.tex`, `slides_main.tex`, `slides_v2*.tex`.

Generated files such as `.aux`, `.log`, `.nav`, `.out`, `.snm`, `.toc`, `.vrb`, `.bbl`, `.blg`, and built PDFs should usually be left alone unless the user specifically asks to rebuild or inspect compilation output.

## Editing Conventions

- Keep root `lejepa` changes narrow and PyTorch-native.
- Preserve differentiability unless a block is intentionally under `torch.no_grad()`.
- Avoid ad hoc string parsing for LaTeX or config edits when a structured/local pattern exists.
- Do not remove generated artifacts, checkpoints, caches, or `__pycache__` unless explicitly asked.
- Be careful with research claims in README/paper/slides; preserve citations and terminology unless the requested change is editorial.

## Verification Preference

For code changes in `lejepa/`, run at least the affected root tests, and run `pytest tests/` when the change touches shared base classes, distributed logic, or exported APIs.

For `stable-pretraining/`, prefer focused tests under `stable-pretraining/stable_pretraining/tests/` first, then broader `cd stable-pretraining && pytest` when the change affects framework-level behavior.
