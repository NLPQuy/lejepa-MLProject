# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
# %% [markdown]
# # LeJEPA Ablation - Feature Aggregation
# - **Spec key**: `aggregation`
# - **Question**: Which ViT output should feed the projector?
# - **Configs**: 3
# - **Status**: ready
#
# **Instructions**:
# 1. Adjust `SOURCE` / `DATA_ROOT` in cell [1] if your Kaggle slugs differ.
# 2. First run only: uncomment `install_wheels(SOURCE)` in cell [1b].
# 3. Edit `OVERRIDES` in cell [3].
# 4. Run cell [4] to render the command.

# %%
# [1] Setup
SOURCE = "/kaggle/input/lejepa-mlproject"
DATA_ROOT = "/kaggle/input/lejepa-data/data/imagenet10"
SPEC_KEY = "aggregation"

import sys
sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext.kaggle_setup import setup, patch_entrypoint, install_wheels, gpu_info, render

paths = setup(SOURCE, DATA_ROOT, spec_key=SPEC_KEY)
ENTRYPOINT = patch_entrypoint(SOURCE, DATA_ROOT)
print("Setup OK:", paths)
print("Patched entrypoint:", ENTRYPOINT)

# %%
# [1b] First-run only: install offline wheels
# install_wheels(SOURCE)

# %%
# [2] GPU check
gpu_info()

# %%
# [3] Edit per-spec overrides
OVERRIDES = {
    'dataset_name': 'imagenet10',
    'backbone': 'vit_small_patch16_224',
    'batch_size': 512,
    'max_epochs': 100,
    'resolution': 224,
    'local_resolution': 96,
    'patch_size': 0,
    'num_workers': 4,
    'precision': 'bf16-mixed',
    'accelerator': 'gpu',
    'devices': 1,
}

# %%
# [4] Render command
command = render(SPEC_KEY, OVERRIDES, ENTRYPOINT)
print("# aggregation: 3 configs")

# %%
# [5] Execute
import subprocess
print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {ret.returncode}")
