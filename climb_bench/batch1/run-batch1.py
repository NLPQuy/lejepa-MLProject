# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # LeJEPA Batch-1 Experiments — Kaggle Offline Runner
#
# **Setup**: run the Setup + GPU-check cells once.
# **Run**: each experiment is a separate cell whose `!python` command is
# commented out by default — delete the leading `# ` on the lines you want,
# then run that one cell. (Double `# #` is intentional: jupytext re-activates
# single-`#` magics on read, so inert cells must be double-commented.)
#
# Each `exp<x>.py` imports its mechanism from the official source
# (`stable_pretraining`) plus the local `_common.py` / `_variants.py`
# (same directory, auto-resolved on `sys.path`).

# %% Setup — paths + offline (run once)
import os, sys

SOURCE = "/kaggle/input/datasets/phamphuhoa/lejepa7/lejepa-MLProject"  # ← adjust to your uploaded dataset
DATA   = f"{SOURCE}/data/imagenet10"
CKPT   = "/kaggle/working/checkpoints"
BATCH  = f"{SOURCE}/climb_bench/batch1"
WHEELS = f"{SOURCE}/wheels"

os.makedirs(CKPT, exist_ok=True)
os.environ["SPT_LIGHT_IMPORT"] = "0"
os.environ["PYTHONPATH"] = f"{SOURCE}/stable-pretraining:{BATCH}:" + os.environ.get("PYTHONPATH", "")
sys.path.insert(0, f"{SOURCE}/stable-pretraining")
sys.path.insert(0, BATCH)

# Stub requests_cache if missing (not on Kaggle system Python)
try:
    import requests_cache
except ImportError:
    import types, requests
    _m = types.ModuleType("requests_cache")
    class _CachedSession(requests.Session):
        def __init__(self, *a, **kw): super().__init__()
    _m.CachedSession = _CachedSession
    sys.modules["requests_cache"] = _m

print(f"SOURCE : {SOURCE}")
print(f"DATA   : {DATA}")
print(f"BATCH  : {BATCH}")
print(f"CKPT   : {CKPT}")

# %% Install wheels (run once — uncomment to run)
# # !pip install {WHEELS}/*.whl --no-deps -q && echo "Wheels installed OK"

# %% GPU check
import torch
print(f"PyTorch : {torch.__version__}  |  CUDA: {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")

# %% [markdown]
# ---
# ## CPU smoke test (run any exp for 3 steps before committing GPU hours)

# %% Smoke — exp3 on CPU, 3 steps
# # !python {BATCH}/exp3.py --accelerator cpu --num_gpus 1 --precision 32 \
# #     --max_steps 3 --batch_size 4 --num_workers 0 --coding_beta 0.01 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/smoke-exp3 --no_wandb

# %% [markdown]
# ---
# ## Baseline (reference — run first)

# %% Baseline — ViT-S 400 ep
# # !python {BATCH}/exp_baseline.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp_baseline-vits --no_wandb

# %% [markdown]
# ## Idea 3 — Coding-rate volume term

# %% exp3 — ViT-S 400 ep
# # !python {BATCH}/exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --coding_beta 0.01 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-codingrate-vits --no_wandb

# %% [markdown]
# ## Idea 4 — Hypersphere-uniformity term

# %% exp4 — ViT-S 400 ep
# # !python {BATCH}/exp4.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --uniformity_gamma 0.5 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp4-uniformity-vits --no_wandb

# %% [markdown]
# ## Idea 7 — DynTanh projector

# %% exp7 — ViT-S 400 ep
# # !python {BATCH}/exp7.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --dyntanh_alpha 0.5 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-dyntanh-vits --no_wandb
