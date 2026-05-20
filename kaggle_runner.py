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
# # LeJEPA Research Variants — Kaggle Runner
#
# **Setup**: Run cells 1–3 once.
# **Run**: Uncomment **one block** at a time and run.

# %% [1] Install + paths (run once, NO internet needed)
import os, sys

SOURCE = "/kaggle/input/lejepa-mlproject"       # ← adjust to your uploaded dataset name
DATA   = f"{SOURCE}/data/imagenet10"
CKPT   = "/kaggle/working/checkpoints"
BENCH  = f"{SOURCE}/stable-pretraining/benchmarks/imagenet10"
WHEELS = f"{SOURCE}/wheels"

os.makedirs(CKPT, exist_ok=True)
os.environ["SPT_LIGHT_IMPORT"] = "0"
os.environ["PYTHONPATH"] = f"{SOURCE}/stable-pretraining:" + os.environ.get("PYTHONPATH", "")
sys.path.insert(0, f"{SOURCE}/stable-pretraining")

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
print(f"BENCH  : {BENCH}")
print(f"CKPT   : {CKPT}")
print("Run the next cell ↓ to install wheels")

# %% [1b] Install wheels via !pip (installs into THIS kernel's Python, so !python can find them)
# Remove the leading # from the line below and run this cell once:
# !pip install {WHEELS}/*.whl --no-deps -q && echo "Wheels installed OK"

# %% [2] GPU check
import torch
print(f"PyTorch : {torch.__version__}  |  CUDA: {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")

# %% [markdown]
# ---
# ## Run commands
# Uncomment ONE block at a time. Variables `BENCH`, `DATA`, `CKPT` are set in cell [1].
# W&B flags: `--wandb_offline` (log locally) or `--no_wandb` (CSV only).

# %% [markdown]
# ### Baseline

# %% Baseline — ViT-S  100 ep
# !python {BENCH}/lejepa-vit-small.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/baseline-vits --wandb_offline

# %% Baseline — ViT-T  100 ep
# !python {BENCH}/lejepa-vit-small.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/baseline-vitt --wandb_offline

# %% [markdown]
# ### Variant 1: SRHT structured slices

# %% SRHT — ViT-S  100 ep
# !python {BENCH}/lejepa-srht.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/srht-vits --wandb_offline

# %% SRHT — ViT-T  100 ep
# !python {BENCH}/lejepa-srht.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/srht-vitt --wandb_offline

# %% [markdown]
# ### Variant 2: Hyvärinen score matching

# %% Hyvarinen — ViT-S  100 ep
# !python {BENCH}/lejepa-hyvarinen.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/hyvarinen-vits --wandb_offline

# %% Hyvarinen — ViT-T  100 ep
# !python {BENCH}/lejepa-hyvarinen.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/hyvarinen-vitt --wandb_offline

# %% [markdown]
# ### Variant 3: Adversarial max-sliced SIGReg

# %% Adversarial — ViT-S  100 ep
# !python {BENCH}/lejepa-adversarial.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/adversarial-vits --wandb_offline

# %% Adversarial — ViT-T  100 ep
# !python {BENCH}/lejepa-adversarial.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/adversarial-vitt --wandb_offline

# %% [markdown]
# ### Variant 4: FM-SIGReg v2

# %% FM-SIGReg — ViT-S  100 ep
# !python {BENCH}/lejepa-fm-sigreg.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/fm-sigreg-vits --wandb_offline

# %% FM-SIGReg — ViT-T  100 ep
# !python {BENCH}/lejepa-fm-sigreg.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/fm-sigreg-vitt --wandb_offline

# %% [markdown]
# ### Variant 5: FM-Invariance

# %% FM-Invariance — ViT-S  100 ep
# !python {BENCH}/lejepa-fm-invariance.py \
#     --backbone vit_small_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/fm-inv-vits --wandb_offline

# %% FM-Invariance — ViT-T  100 ep
# !python {BENCH}/lejepa-fm-invariance.py \
#     --backbone vit_tiny_patch16_224 --max_epochs 100 --batch_size 128 --num_workers 4 \
#     --data_local_path {DATA} --checkpoint_dir {CKPT}/fm-inv-vitt --wandb_offline
