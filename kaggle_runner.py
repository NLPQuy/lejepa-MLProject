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
# **Setup**: Run cells 1–4 once (install, env, GPU check).
# **Run**: In cells 5+, uncomment **one block at a time** and run.
#
# Assumes:
# - Source zip uploaded as a Kaggle dataset input → adjust `SOURCE` below
# - `data/imagenet10/` from the source zip (already bundled), OR
#   a separate Kaggle dataset input → adjust `DATA` below

# %% [1] Install dependencies (run once, NO internet needed)
import subprocess, os, glob

SOURCE = "/kaggle/input/lejepa-mlproject"       # ← adjust to your uploaded dataset name
DATA   = f"{SOURCE}/data/imagenet10"            # imagenette bundled in source zip
CKPT   = "/kaggle/working/checkpoints"          # writable Kaggle output dir
BENCH  = f"{SOURCE}/stable-pretraining/benchmarks/imagenet10"
WHEELS = f"{SOURCE}/wheels"                     # pre-downloaded wheels (no internet)

os.makedirs(CKPT, exist_ok=True)

# Step 1: install bundled wheels one by one (ignore already-installed conflicts)
for whl in sorted(glob.glob(f"{WHEELS}/*.whl")):
    r = subprocess.run(f"pip install '{whl}' -q --no-deps 2>&1", shell=True, capture_output=True, text=True)
    status = "OK" if r.returncode == 0 else "skip"
    print(f"  {status}  {whl.split('/')[-1]}")

# Step 2: install stable_pretraining package itself (skip network deps)
r = subprocess.run(
    f"pip install -e {SOURCE}/stable-pretraining --no-deps -q",
    shell=True, capture_output=True, text=True,
)
if r.returncode != 0:
    print("stable_pretraining install FAILED:", r.stderr[-300:])
else:
    print("stable_pretraining OK")

print("Install OK")
print(f"SOURCE : {SOURCE}")
print(f"DATA   : {DATA}")
print(f"BENCH  : {BENCH}")
print(f"CKPT   : {CKPT}")

# %% [2] Environment
import os

os.environ["SPT_LIGHT_IMPORT"] = "0"

# W&B — pick ONE option:
# Option A: set API key from Kaggle Secret  →  Settings > Add-ons > Secrets
# from kaggle_secrets import UserSecretsClient
# os.environ["WANDB_API_KEY"] = UserSecretsClient().get_secret("WANDB_API_KEY")

# Option B: run offline (logs saved to /kaggle/working/wandb/)
# Pass --wandb_offline to all commands below (already shown)

# Option C: skip W&B entirely
# Pass --no_wandb to all commands below

print("Env OK  |  SPT_LIGHT_IMPORT =", os.environ["SPT_LIGHT_IMPORT"])

# %% [3] GPU check
import torch
print(f"PyTorch : {torch.__version__}")
print(f"CUDA    : {torch.cuda.is_available()}")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"  GPU {i}: {props.name}  {props.total_memory // 2**20} MB")

# %% [4] Quick smoke test (optional, ~30s)
# import subprocess
# subprocess.run([
#     "python", f"{BENCH}/lejepa-vit-small.py",
#     "--backbone",       "vit_tiny_patch16_224",
#     "--max_epochs",     "1",
#     "--batch_size",     "16",
#     "--num_workers",    "2",
#     "--data_local_path", DATA,
#     "--checkpoint_dir", f"{CKPT}/smoke",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Baseline
# `lejepa-vit-small.py` — standard EP test, Gaussian random slices

# %% Baseline — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-vit-small.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/baseline-vits",
#     "--wandb_offline",
# ], check=True)

# %% Baseline — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-vit-small.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/baseline-vitt",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Variant 1: SRHT structured slices
# Replace Gaussian random projections with Walsh-Hadamard + Rademacher (lower SIGReg variance).

# %% SRHT — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-srht.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/srht-vits",
#     "--wandb_offline",
# ], check=True)

# %% SRHT — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-srht.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/srht-vitt",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Variant 2: Hyvärinen score matching
# Full-d Hyvärinen ISM + Hutchinson trace — replaces per-slice EP test.

# %% Hyvarinen — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-hyvarinen.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/hyvarinen-vits",
#     "--wandb_offline",
# ], check=True)

# %% Hyvarinen — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-hyvarinen.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/hyvarinen-vitt",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Variant 3: Adversarial max-sliced SIGReg
# Minimax slicing — adversary finds worst-case direction, encoder defends.

# %% Adversarial — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-adversarial.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/adversarial-vits",
#     "--wandb_offline",
# ], check=True)

# %% Adversarial — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-adversarial.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/adversarial-vitt",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Variant 4: FM-SIGReg v2
# Flow-matching transport P_z → N(0,I) with ExFM target + Hungarian OT coupling.

# %% FM-SIGReg — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-fm-sigreg.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/fm-sigreg-vits",
#     "--wandb_offline",
# ], check=True)

# %% FM-SIGReg — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-fm-sigreg.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/fm-sigreg-vitt",
#     "--wandb_offline",
# ], check=True)

# %% [markdown]
# ---
# ## Variant 5: FM-Invariance
# Replace MSE invariance with flow-matching view alignment (softer, distributional).

# %% FM-Invariance — ViT-S  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-fm-invariance.py",
#     "--backbone",        "vit_small_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/fm-inv-vits",
#     "--wandb_offline",
# ], check=True)

# %% FM-Invariance — ViT-T  100 ep
# subprocess.run([
#     "python", f"{BENCH}/lejepa-fm-invariance.py",
#     "--backbone",        "vit_tiny_patch16_224",
#     "--max_epochs",      "100",
#     "--batch_size",      "128",
#     "--num_workers",     "4",
#     "--data_local_path", DATA,
#     "--checkpoint_dir",  f"{CKPT}/fm-inv-vitt",
#     "--wandb_offline",
# ], check=True)
