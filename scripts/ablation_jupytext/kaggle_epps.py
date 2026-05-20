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
# # LeJEPA Ablation - Epps-Pulley Parameters
# - **Spec key**: `epps`
# - **Question**: How sensitive is SIGReg to the sliced Epps-Pulley integration grid?
# - **Configs**: 27
# - **Status**: ready
#
# **Instructions**:
# 1. Adjust `SOURCE` and `HF_CACHE` in cell [1] if your Kaggle slugs differ.
# 2. First run only: uncomment cell [1b] to install offline wheels.
# 3. Edit `OVERRIDES` in cell [3] to tune Kaggle-specific params.
# 4. For epps / views: set CHUNK_INDEX in cell [4].

# %% [1] Setup env + sys.path
SOURCE = "/kaggle/input/lejepa-mlproject"
HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"

import os
import sys

sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext._common import setup_kaggle_env

paths = setup_kaggle_env(source=SOURCE, hf_cache=HF_CACHE, spec_key="epps")
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
CHUNK_INDEX = 0
CHUNK_SIZE = 9
NUM_CHUNKS = 3

from scripts.ablation_jupytext._common import render_chunk

if not 0 <= CHUNK_INDEX < NUM_CHUNKS:
    raise ValueError(f"CHUNK_INDEX must be in 0..{NUM_CHUNKS - 1}")

command = render_chunk("epps", OVERRIDES, CHUNK_INDEX, CHUNK_SIZE)
print(f"# epps chunk {CHUNK_INDEX}/{NUM_CHUNKS - 1} of 27 total configs")


# %% [5] Execute
import subprocess

print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {ret.returncode}")

# %% [6] Dump CSV summary
# !python -m stable_pretraining.cli dump-csv-logs {paths['log_dir']} ablation_epps max
