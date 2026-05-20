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
# 1. Adjust `SOURCE` and `HF_CACHE` in cell [1] if your Kaggle slugs differ.
# 2. First run only: uncomment cell [1b] to install offline wheels.
# 3. Edit `OVERRIDES` in cell [3] to tune Kaggle-specific params.
# 4. Run cell [4] to render and execute the command.

# %% [1] Setup env + sys.path
SOURCE = "/kaggle/input/lejepa-mlproject"
HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"

import os
import sys

sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext._common import setup_kaggle_env

paths = setup_kaggle_env(source=SOURCE, hf_cache=HF_CACHE, spec_key="aggregation")
print("Setup OK:", paths)

# %% [1b] Install wheels (UNCOMMENT first run, then comment again)
# !pip install {SOURCE}/wheels/*.whl --no-deps -q && echo "Wheels installed"

# %% [2] GPU check
import torch

print(f"PyTorch {torch.__version__} | CUDA {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    props = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {props.name}  {props.total_memory // 2**20} MB")

# %% [3] Edit per-spec overrides here (replaces baseline BASE_OVERRIDES values)
OVERRIDES = {
    'dataset_name': 'imagenette',
    'backbone': 'vit_small_patch16_224',
    'batch_size': 512,
    'max_epochs': 50,
    'resolution': 224,
    'local_resolution': 96,
    'patch_size': 16,
    'num_workers': 4,
    'precision': 'bf16-mixed',
    'accelerator': 'gpu',
    'devices': 1,
}

# %% [4] Render command
from scripts.ablation_jupytext._common import render

command = render("aggregation", OVERRIDES)
print("# Configs: 3")


# %% [5] Execute
import subprocess

print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {ret.returncode}")

# %% [6] Dump CSV summary
# !python -m stable_pretraining.cli dump-csv-logs {paths['log_dir']} ablation_aggregation max
