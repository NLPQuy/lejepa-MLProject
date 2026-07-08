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
# # LeJEPA Batch-2 Experiments — Kaggle Offline Runner
#
# Optimizer and architecture experiments for Imagenette. Commands are inert by
# default; delete one leading `# ` on the command you want to run.

# %% Setup paths and offline mode
import os, sys

SOURCE = "/kaggle/input/datasets/phamphuhoa/lejepa7/lejepa-MLProject"
DATA = f"{SOURCE}/data/imagenet10"
CKPT = "/kaggle/working/checkpoints"
BATCH = f"{SOURCE}/climb_bench/batch2"
WHEELS = f"{SOURCE}/wheels"

os.makedirs(CKPT, exist_ok=True)
os.environ["SPT_LIGHT_IMPORT"] = "0"
os.environ["PYTHONPATH"] = f"{SOURCE}/stable-pretraining:{BATCH}:" + os.environ.get("PYTHONPATH", "")
sys.path.insert(0, f"{SOURCE}/stable-pretraining")
sys.path.insert(0, BATCH)

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

# %% Install wheels
# # !pip install {WHEELS}/*.whl --no-deps -q && echo "Wheels installed OK"

# %% GPU check
import torch
print(f"PyTorch : {torch.__version__}  |  CUDA: {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")

# %% [markdown]
# ---
# ## CPU smoke test

# %% Smoke exp2 CPU
# # !python {BATCH}/exp2.py --accelerator cpu --num_gpus 1 --precision 32 \
# #     --max_steps 3 --batch_size 4 --num_workers 0 --qk_norm \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/smoke-exp2 --no_wandb

# %% [markdown]
# ---
# ## Baseline

# %% Baseline ViT-S 400 ep
# # !python {BATCH}/exp_baseline.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp_baseline-vits --no_wandb

# %% [markdown]
# ## Idea 1 SAM

# %% exp1 SAM ViT-S 400 ep
# # !python {BATCH}/exp1.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --sam_rho 0.05 --sam_late \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp1-sam-vits --no_wandb

# %% [markdown]
# ## Idea 2 QK-Norm

# %% exp2 QK-Norm ViT-S 400 ep
# # !python {BATCH}/exp2.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --qk_norm \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp2-qknorm-vits --no_wandb

# %% [markdown]
# ## Idea 3 Muon

# %% exp3 Muon ViT-S 400 ep
# # !python {BATCH}/exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-muon-vits --no_wandb

# %% [markdown]
# ## Idea 4 Schedule-Free AdamW

# %% exp4 Schedule-Free ViT-S 400 ep
# # !python {BATCH}/exp4.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp4-schedulefree-vits --no_wandb

# %% [markdown]
# ## Idea 5 PCGrad

# %% exp5 PCGrad ViT-S 400 ep
# # !python {BATCH}/exp5.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp5-pcgrad-vits --no_wandb

# %% [markdown]
# ## Idea 6 Conv Stem

# %% exp6 Conv Stem ViT-S 400 ep
# # !python {BATCH}/exp6.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --conv_stem \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp6-convstem-vits --no_wandb

# %% [markdown]
# ## Idea 7 SWA

# %% exp7 SWA ViT-S 400 ep
# # !python {BATCH}/exp7.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --swa_epoch_start 0.75 --swa_lr 1e-5 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-swa-vits --no_wandb

# %% [markdown]
# ## Idea 8 LLRD

# %% exp8 LLRD ViT-S 400 ep
# # !python {BATCH}/exp8.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --llrd_gamma 0.75 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp8-llrd-vits --no_wandb

# %% [markdown]
# ## Idea 9 Progressive stochastic depth

# %% exp9 Stochastic depth ViT-S 400 ep
# # !python {BATCH}/exp9.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp9-sdschedule-vits --no_wandb

# %% [markdown]
# ## Idea 10 Deep supervision

# %% exp10 Deep supervision ViT-S 400 ep
# # !python {BATCH}/exp10.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --deepsup_mu 0.1 --deepsup_layers 6,9 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp10-deepsup-vits --no_wandb
