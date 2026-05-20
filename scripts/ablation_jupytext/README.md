# Kaggle Ablation Notebooks

These jupytext notebooks wrap the existing `scripts.ablations` specs for Kaggle. Each notebook owns a literal `OVERRIDES` dict (cell `[3]`) and renders the shell command via `dataclasses.replace` on the frozen `AblationSpec` — no global state is mutated. They reuse the repository renderer and training entrypoint without forking `scripts/ablations/`, `scripts/train_lejepa_ablation.py`, or `stable-pretraining/`.

Background: see `scripts/ablation_plan.md` when present, plus the root `plan_ablation_fix.md`.

## Kaggle Datasets To Upload

Upload these input datasets:

- `lejepa-mlproject`: this repository snapshot, including `lejepa/`, `stable-pretraining/`, `scripts/` (which now contains `ablation_jupytext/`), and `wheels/`.
- `lejepa-imagenette-hfcache`: the Hugging Face datasets cache for Imagenette, for example `frgfm___imagenette/...`.

The notebooks default to:

```python
SOURCE = "/kaggle/input/lejepa-mlproject"
HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"
```

Edit those variables in cell `[1]` if your dataset slugs differ.

## Offline Wheels

Build wheels locally before uploading the project dataset:

```bash
pip wheel -r requirements.txt -w wheels/ --no-deps
```

The Kaggle notebooks are designed for Internet OFF. Cell `[1b]` installs from `SOURCE/wheels/*.whl` with `--no-deps`; uncomment it for the first run of a session, then comment it again.

## Workflow

1. Open one notebook, for example `kaggle_drop_path.py`, with Jupytext or upload it as a Kaggle notebook.
2. Confirm `SOURCE` and `HF_CACHE` in cell `[1]`.
3. Uncomment and run cell `[1b]` once to install wheels.
4. Edit `OVERRIDES` in cell `[3]` (per-notebook, see defaults below).
5. Run the remaining cells.
6. For `epps` and `views`, set `CHUNK_INDEX` in cell `[4]` before running. `epps` has 3 chunks of 9 configs; `views` has 2 chunks of 6 configs.
7. Download `/kaggle/working/` after the run. Sync offline W&B logs locally with `wandb sync ./wandb/offline-*`.

## OVERRIDES (cell `[3]` defaults)

Each generated notebook embeds the literal dict below. Edit it in place; the renderer merges it into the spec via `dataclasses.replace`. Keys take precedence over both `spec.overrides` and `BASE_OVERRIDES`.

| Key | Value |
|---|---|
| `dataset_name` | `imagenette` |
| `backbone` | `vit_small_patch16_224` |
| `batch_size` | `512` |
| `max_epochs` | `50` |
| `resolution` | `224` |
| `local_resolution` | `96` |
| `patch_size` | `16` |
| `precision` | `bf16-mixed` |
| `accelerator` | `gpu` |
| `devices` | `1` |
| `num_workers` | `4` |

## Time Estimates

Estimates assume ViT-S/16, batch 512, 8 views, Imagenette 28K, bf16, and an RTX Pro 6000 96GB. Re-measure after the first real run.

| Spec | Configs | Time/config | Total |
|---|---:|---:|---:|
| `drop_path` | 5 | ~30 min | ~2.5h |
| `projector_depth` | 4 | ~30 min | ~2h |
| `aggregation` | 3 | ~30 min | ~1.5h |
| `sigreg_target` | 3 | ~35 min | ~1.7h |
| `predictor` | 3 | ~30 min | ~1.5h |
| `patch_masking` | 6 | ~30 min | ~3h |
| `views` | 11, 2 chunks | ~30 min | ~5.5h, ~2.7h/chunk |
| `epps` | 27, 3 chunks | ~30 min | ~13.5h, ~4.5h/chunk |

## Skipped Specs

- `projector_dims`: skipped because the grid includes `embedding_dim`, while LeJEPA derives the actual embed dimension from timm. Running it now would duplicate work and risk misleading results until model support is clarified.
- `reg_tokens`: skipped because register-token support is checked at import time against the original backbone. Enabling it cleanly needs model-support work in the spec/model path, outside this notebook conversion.

## Regenerate

After changing ablation specs, regenerate the notebooks locally:

```bash
python scripts/ablation_jupytext/generate_kaggle_notebooks.py
```

This writes the eight generated files `scripts/ablation_jupytext/kaggle_<key>.py`.

## Note on Folder Name

The folder uses an underscore (`ablation_jupytext`) so the notebooks can use package-style imports. With the repository root on `sys.path`, helper imports are regular dotted imports:

```python
sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext._common import setup_kaggle_env, render, render_chunk
```

## Helpers in `_common.py`

| Helper | Purpose |
|---|---|
| `setup_kaggle_env(...)` | Set env vars, sys.path, MPL/HF cache dirs, stub `requests_cache` if missing. |
| `render(spec_key, overrides, *, smoke=False)` | Render one spec command. Uses `dataclasses.replace(spec, overrides=...)`; does **not** mutate `BASE_OVERRIDES`. |
| `render_chunk(spec_key, overrides, chunk_index, chunk_size)` | Same but slices a long sweep into one chunk (used by `epps`, `views`). |
