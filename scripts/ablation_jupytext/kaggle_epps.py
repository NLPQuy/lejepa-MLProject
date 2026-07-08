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
# 1. Adjust `SOURCE` / `DATA_ROOT` in cell [1] if your Kaggle slugs differ.
# 2. First run only: uncomment `install_wheels(SOURCE)` in cell [1b].
# 3. Edit `OVERRIDES` in cell [3].
# 4. Set `CHUNK_INDEX` in cell [4].

# %%
# [1] Setup
SOURCE = "/kaggle/input/datasets/mlbang/lejepa-ml-project"
DATA_ROOT = "/kaggle/input/datasets/phamphuhoa/lejepa7/lejepa-ml-project/data/imagenet10"
SPEC_KEY = "epps"

import sys
sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext.kaggle_setup import setup, patch_entrypoint, install_wheels, gpu_info, render

paths = setup(SOURCE, DATA_ROOT, spec_key=SPEC_KEY)
ENTRYPOINT = patch_entrypoint(SOURCE, DATA_ROOT)
print("Setup OK:", paths)
print("Patched entrypoint:", ENTRYPOINT)

# %%
# [1b] First-run only: install offline wheels
install_wheels(SOURCE)

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
# [4] Render command — run a sub-range of cases (indices into the full 27-case grid)
# Split each across sessions to stay under Kaggle's 12h limit (~1.12h/config):
#   0,7  then 7,14  then 14,21  then 21,27   (4 sessions, ~8h each)
import dataclasses
from itertools import product
from scripts.ablations.commands import render_command
from scripts.ablations.common import CommandOptions
from scripts.ablations.specs import get_spec

CASE_START, CASE_STOP = 0, 7

spec = get_spec(SPEC_KEY)
keys = list(spec.grid)
all_cases = [dict(zip(keys, vals)) for vals in product(*(spec.grid[k] for k in keys))]
cases = all_cases[CASE_START:CASE_STOP]
spec = dataclasses.replace(
    spec, grid={}, cases=cases,
    overrides={**spec.overrides, **OVERRIDES},
    key=f"{SPEC_KEY}_sub{CASE_START}_{CASE_STOP}",
)
opts = CommandOptions(
    target=f"python {ENTRYPOINT}", multirun=True, smoke=False,
    env={"HYDRA_FULL_ERROR": "1"},
)
command = render_command(spec, opts).command
print(f"# {SPEC_KEY} cases {CASE_START + 1}..{CASE_STOP} of 27 configs")

# %%
# [5] Execute
import subprocess
print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {ret.returncode}")
