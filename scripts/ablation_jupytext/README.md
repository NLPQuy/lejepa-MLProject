# Kaggle Ablation Notebooks

Slim jupytext notebooks (one per spec) that drive `scripts.ablations` on Kaggle.
All Kaggle-specific helpers live in [`kaggle_setup.py`](kaggle_setup.py); each
`kaggle_<spec>.py` is < 90 lines and only owns the user-editable bits
(`OVERRIDES`, `CHUNK_INDEX`).

## Layout

```
scripts/ablation_jupytext/
  kaggle_setup.py              # shared helpers (setup, patch_entrypoint, render, ...)
  generate_kaggle_notebooks.py # template renderer
  kaggle_<spec>.py             # 8 generated notebooks (do not hand-edit)
```

## Kaggle Datasets

Upload two input datasets:

- `lejepa-mlproject`: this repo snapshot — `lejepa/`, `stable-pretraining/`,
  `scripts/` (incl. `ablation_jupytext/`), and `wheels/`.
- `lejepa-data`: local Hugging Face Arrow dataset at
  `data/imagenet10/{train,validation}/`.

Defaults (edit in cell `[1]` if your slugs differ):

```python
SOURCE = "/kaggle/input/lejepa-mlproject"
DATA_ROOT = "/kaggle/input/lejepa-data/data/imagenet10"
```

## Workflow

1. Open `kaggle_<spec>.py` as a Kaggle notebook (Jupytext converts on the fly).
2. Cell `[1]` calls `setup()` + `patch_entrypoint()` (read-only source dataset
   is copied to `/kaggle/working/train_lejepa_ablation_kaggle.py`).
3. First run only: uncomment `install_wheels(SOURCE)` in cell `[1b]`.
4. Edit `OVERRIDES` in cell `[3]`.
5. For `epps`/`views` set `CHUNK_INDEX` in cell `[4]` (chunks: epps 3×9,
   views 2×6).
6. Run cells `[5]` (execute) and optionally `[6]` (dump CSV).

Offline by default: cell `[1]` sets `HF_DATASETS_OFFLINE=1`, `WANDB_MODE=offline`
and stubs `requests_cache` if missing.

## OVERRIDES defaults

Embedded in each notebook; merged into `spec.overrides` via
`dataclasses.replace`, then `commands.py` layers `BASE_OVERRIDES` underneath.

| Key | Value |
|---|---|
| `dataset_name` | `imagenet10` |
| `backbone` | `vit_small_patch16_224` |
| `batch_size` | `512` |
| `max_epochs` | `50` |
| `resolution` | `224` |
| `local_resolution` | `96` |
| `patch_size` | `0` (auto = match backbone native) |
| `num_workers` | `4` |
| `precision` | `bf16-mixed` |
| `accelerator` | `gpu` |
| `devices` | `1` |

`patch_size: 0` (or any value <= 0) tells the trainer to use the backbone's
native patch size. Set a positive value only when intentionally ablating a
non-native patch size; that triggers `MaskedEncoder._rebuild_patch_embed`.

## Time Estimates

ViT-S/16, batch 512, 8 views, bf16, RTX Pro 6000 96GB:

| Spec | Configs | Total |
|---|---:|---:|
| `drop_path` | 5 | ~2.5h |
| `projector_depth` | 4 | ~2h |
| `aggregation` | 3 | ~1.5h |
| `sigreg_target` | 3 | ~1.7h |
| `predictor` | 3 | ~1.5h |
| `patch_masking` | 6 | ~3h |
| `views` | 11 (2 chunks) | ~5.5h |
| `epps` | 27 (3 chunks) | ~13.5h |

## Skipped Specs

- `projector_dims`: grid duplicates `embedding_dim` which timm derives from
  the backbone; needs spec work first.
- `reg_tokens`: register-token support is asserted at import; needs model
  changes.

## Regenerate

```bash
python scripts/ablation_jupytext/generate_kaggle_notebooks.py
```

`generate_kaggle_notebooks.py` is the source of truth for the template.

## Wheels

Build offline wheels before uploading the project dataset:

```bash
pip wheel -r requirements.txt -w wheels/ --no-deps
```
