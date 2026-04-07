# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Bootstrap — Clone / Pull source từ GitHub
#
# Block này chạy **trước tất cả import** để đảm bảo source code (lejepa +
# stable-pretraining) luôn được lấy về từ repo, dù chạy trên Colab, Kaggle,
# hay bất kỳ môi trường nào khác.
#
# **Cách dùng**:
# - Đặt token vào biến môi trường: `export GITHUB_TOKEN=ghp_xxxx`
# - Hoặc điền thẳng vào `GITHUB_TOKEN` bên dưới (không commit lên git!)

# %%
import os
import subprocess
import sys

# ── Cấu hình repo ─────────────────────────────────────────────────────────────
GITHUB_TOKEN  = os.environ.get("GITHUB_TOKEN", "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")   # ← set bằng Kaggle Secret hoặc env var
GITHUB_REPO   = "https://github.com/NLPQuy/lejepa-MLProject.git"
CLONE_DIR     = "/kaggle/working/lejepa-MLProject"  # Kaggle write dir

from huggingface_hub import login
login(token=os.environ.get("HF_TOKEN", "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"))

def _run(cmd: str, **kwargs) -> int:
    """Chạy shell command, in output, trả về return code."""
    print(f"  $ {cmd}")
    proc = subprocess.run(cmd, shell=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    if proc.stdout:
        print(proc.stdout.rstrip())
    return proc.returncode


def bootstrap_repo():
    """Clone repo lần đầu hoặc pull update nếu đã có."""
    # Tạo authenticated URL
    if GITHUB_TOKEN:
        # Format: https://<token>@github.com/user/repo.git
        auth_url = GITHUB_REPO.replace("https://", f"https://{GITHUB_TOKEN}@")
    else:
        auth_url = GITHUB_REPO
        print("[bootstrap] ⚠ GITHUB_TOKEN không được đặt — dùng anonymous (chỉ repo public)")

    clone_path = CLONE_DIR

    if os.path.isdir(os.path.join(clone_path, ".git")):
        print(f"[bootstrap] Repo đã có tại {clone_path}, đang pull ...")
        rc = _run(f"git -C '{clone_path}' pull origin main --ff-only")
        if rc != 0:
            print("[bootstrap] pull thất bại, thử reset hard ...")
            _run(f"git -C '{clone_path}' fetch origin main")
            _run(f"git -C '{clone_path}' reset --hard origin/main")
    else:
        print(f"[bootstrap] Clone repo về {clone_path} ...")
        os.makedirs(os.path.dirname(clone_path), exist_ok=True)
        rc = _run(f"git clone '{auth_url}' '{clone_path}'")
        if rc != 0:
            raise RuntimeError(f"git clone thất bại (rc={rc}). Kiểm tra lại GITHUB_TOKEN và quyền truy cập repo.")

    # Thêm đường dẫn vào sys.path
    spt_path = os.path.join(clone_path, "stable-pretraining")
    for p in [clone_path, spt_path]:
        if p not in sys.path:
            sys.path.insert(0, p)
            print(f"[bootstrap] sys.path ← {p}")

    print("[bootstrap] ✓ Done\n")
    return clone_path


# Chỉ bootstrap khi clone_dir chưa là thư mục hiện tại
_this_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
if os.path.abspath(_this_dir) != os.path.abspath(CLONE_DIR):
    bootstrap_repo()
else:
    # Chạy trực tiếp từ repo đã clone — chỉ cần set sys.path
    _spt = os.path.join(_this_dir, "stable-pretraining")
    for _p in [_this_dir, _spt]:
        if _p not in sys.path:
            sys.path.insert(0, _p)

# ── Cài stable_pretraining từ source đã có trong repo ────────────────────────
# Luôn chạy pip install -e: sinh _version.py + cài tất cả deps từ pyproject.toml
# (pip tự bỏ qua nếu package + deps đã up-to-date)
_spt_src = os.path.join(CLONE_DIR, "stable-pretraining")
print(f"[install] pip install -e {_spt_src}")
# SETUPTOOLS_SCM_PRETEND_VERSION: bắt buộc vì .git đã bị xóa khỏi repo
_env = {**os.environ, "SETUPTOOLS_SCM_PRETEND_VERSION": "0.0.0"}
_run(f"{sys.executable} -m pip install -q -e '{_spt_src}'", env=_env)

# %% [markdown]
# # LeJEPA ViT-L — Pretraining (IN-1K) + Few-Shot Linear Probe Evaluation
#
# Reproduces the main table in the README:
# - **Backbone**: ViT-L/16 (304M params) via timm (`vit_large_patch16_224`)
# - **Pretrain**: ImageNet-1K, 100 epochs
# - **Eval**: Few-shot linear probe (1-shot, 10-shot, all) trên 8 datasets:
#   DTD · Aircraft · Cars · CIFAR-10 · CIFAR-100 · Flowers102 · Food-101 · Oxford Pets
#
# **Flow**:
# ```
# Phase 1 ── Pretrain (LeJEPA SIGReg) on IN-1K → checkpoint
# Phase 2 ── Extract frozen embeddings on each eval dataset
# Phase 3 ── Fit few-shot AdamW linear probe, report top-1 accuracy
# ```

# %% [markdown]
# ## 0. Setup & Imports

# %%
import sys
import os

# Đảm bảo stable-pretraining được tìm thấy nếu chưa install từ pip
REPO_ROOT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else CLONE_DIR
SPT_PATH  = os.path.join(REPO_ROOT, "stable-pretraining")
if SPT_PATH not in sys.path:
    sys.path.insert(0, SPT_PATH)

import math
import random
from pathlib import Path

import lightning.pytorch as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
from torch.utils.data import DataLoader, TensorDataset

# ── stable_pretraining ────────────────────────────────────────────────────────
import stable_pretraining as spt
from stable_pretraining.data import transforms          # spt transforms (dict-based)
from stable_pretraining.data.module import DataModule
from stable_pretraining.data.datasets import HFDataset

# ── lejepa core (từ stable_pretraining.methods) ───────────────────────────────
from stable_pretraining.methods.lejepa import (
    LeJEPA,           # backbone + projector + SIGReg, tất cả trong 1 class
    LeJEPAOutput,     # dataclass: loss, embedding, inv_loss, sigreg_loss
    SlicedEppsPulley, # SIGReg multivariate test (dùng nếu cần standalone)
    EppsPulley,       # Epps-Pulley univariate test (1D)
)

# %% [markdown]
# ## 1. Hyperparameters

# %%
# ── Backbone ──────────────────────────────────────────────────────────────────
BACKBONE_NAME    = "vit_large_patch16_224"   # ViT-L/16, 304M params

# ── Pretraining ───────────────────────────────────────────────────────────────
PRETRAIN_DATASET = "ILSVRC/imagenet-1k"
MAX_EPOCHS       = 100
BATCH_SIZE       = 512
LR               = 5e-4
WEIGHT_DECAY     = 5e-2
WARMUP_RATIO     = 0.1                        # 10% warmup
N_GLOBAL_VIEWS   = 2
N_LOCAL_VIEWS    = 6

# SIGReg (LeJEPA loss) — khớp với paper
SIGREG_LAMBDA    = 0.05
SIGREG_SLICES    = 1024
SIGREG_N_POINTS  = 17

# ── Eval datasets ─────────────────────────────────────────────────────────────
# (hf_dataset_name, n_classes, split_train, split_test, label_column)
EVAL_DATASETS = [
    ("tanganke/dtd",                     47,  "train", "test",       "label"),
    ("Multimodal-Fatima/FGVC_dataset",  100,  "train", "test",       "label"),   # Aircraft
    ("tanganke/stanford_cars",          196,  "train", "test",       "label"),
    ("cifar10",                          10,  "train", "test",       "label"),
    ("cifar100",                        100,  "train", "test",       "fine_label"),
    ("nelorth/oxford-flowers",          102,  "train", "test",       "label"),
    ("ethz/food101",                    101,  "train", "validation", "label"),
    ("pcuenq/oxford-pets",               37,  "train", "test",       "label"),
]
EVAL_DATASET_LABELS = [
    "DTD", "Aircraft", "Cars", "CIFAR-10",
    "CIFAR-100", "Flowers102", "Food-101", "Oxford Pets",
]
EVAL_SHOTS   = [1, 10, None]    # None = toàn bộ train set
EVAL_SEEDS   = [0, 1, 2]        # avg over seeds cho few-shot
EVAL_LR      = 1e-3
EVAL_EPOCHS  = 50
EVAL_BS      = 256

# ── Misc ──────────────────────────────────────────────────────────────────────
# Streaming dataset: num_workers PHẢI là 0, multiprocess + HF stream = deadlock
NUM_WORKERS_STREAM = 0
NUM_WORKERS  = 4   # dùng cho eval (map-style dataset)
PRECISION    = "bf16-mixed"
ACCELERATOR  = "gpu"
DEVICES      = "auto"
CKPT_DIR     = Path(REPO_ROOT) / "checkpoints"
LOG_DIR      = Path(REPO_ROOT) / "logs"
CKPT_DIR.mkdir(exist_ok=True)

IMG_MEAN = (0.485, 0.456, 0.406)
IMG_STD  = (0.229, 0.224, 0.225)

# %% [markdown]
# ## 2. Data Augmentation (Multi-Crop, theo README)

# %%
def _photometric_transforms() -> list:
    """Shared color augmentations cho cả global và local views."""
    return [
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2, hue=0.1, p=0.8),
        transforms.RandomGrayscale(p=0.2),
        transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0), p=0.5),
        transforms.RandomSolarize(threshold=128, p=0.2),
    ]


def make_global_transform():
    """Global view: 224×224, scale (0.3, 1.0)."""
    return transforms.Compose(
        transforms.RGB(),
        transforms.RandomResizedCrop((224, 224), scale=(0.3, 1.0)),
        *_photometric_transforms(),
        transforms.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_local_transform():
    """Local view: 98×98, scale (0.05, 0.3)."""
    return transforms.Compose(
        transforms.RGB(),
        transforms.RandomResizedCrop((98, 98), scale=(0.05, 0.3)),
        *_photometric_transforms(),
        transforms.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_val_transform():
    """Standard center-crop cho validation / embedding extraction."""
    return transforms.Compose(
        transforms.RGB(),
        transforms.Resize((256, 256)),
        transforms.CenterCrop((224, 224)),
        transforms.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_train_transform(n_global: int = N_GLOBAL_VIEWS, n_local: int = N_LOCAL_VIEWS):
    """Multi-crop dict transform: keys 'global_i' và 'local_j'."""
    return transforms.MultiViewTransform({
        **{f"global_{i}": make_global_transform() for i in range(n_global)},
        **{f"local_{j}":  make_local_transform()  for j in range(n_local)},
    })


# %% [markdown]
# ## 3. LeJEPA Forward Function (theo benchmark script)

# %%
def lejepa_forward(self, batch: dict, stage: str) -> dict:
    """Custom forward cho spt.Module.

    Training (stage='fit'):
        batch có keys "global_0", "local_0", ..., mỗi key là dict {"image", "label"}.
    Eval (stage='validate'/'test'):
        batch có key "image" và "label".

    Dùng self.model (LeJEPA instance) để compute loss + embedding.
    """
    out = {}

    images = batch.get("image")

    if stage == "fit":
        global_views = [batch[k]["image"] for k in batch if k.startswith("global")]
        local_views  = [batch[k]["image"] for k in batch if k.startswith("local")]
        labels = next(
            batch[k]["label"]
            for k in batch
            if k.startswith("global") or k.startswith("local")
        )

        output: LeJEPAOutput = self.model(
            global_views=global_views,
            local_views=local_views,
            images=images,
        )
        out["label"] = labels.repeat(len(global_views))

    else:
        output: LeJEPAOutput = self.model(images=images)
        out["label"] = batch["label"].long()

    out["loss"]      = output.loss
    out["embedding"] = output.embedding

    self.log(f"{stage}/sigreg",  output.sigreg_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/inv",     output.inv_loss,    on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/loss",    output.loss,        on_step=True, on_epoch=True, sync_dist=True)

    return out


# %% [markdown]
# ## 4. Phase 1: Pretraining

# %%
def build_pretrain_datamodule() -> DataModule:
    """DataModule cho ImageNet-1K pretraining.

    streaming=True: stream trực tiếp từ HuggingFace, không download 150GB về disk.
    """
    train_ds = HFDataset(
        PRETRAIN_DATASET,
        split="train",
        transform=make_train_transform(),
        trust_remote_code=True,
        streaming=True,       # ← không cache về disk
    )
    val_ds = HFDataset(
        PRETRAIN_DATASET,
        split="validation",
        transform=make_val_transform(),
        trust_remote_code=True,
        streaming=True,
    )
    return DataModule(
        train=DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=False,
                         num_workers=NUM_WORKERS_STREAM, drop_last=True,
                         pin_memory=True),
        val=DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False,
                       num_workers=NUM_WORKERS_STREAM,
                       pin_memory=True),
    )


def build_pretrain_module() -> tuple[spt.Module, list]:
    """Tạo spt.Module bọc LeJEPA (ViT-L) + các callbacks."""
    # LeJEPA tự tạo backbone (timm ViT-L), projector MLP, và SlicedEppsPulley
    model = LeJEPA(
        encoder_name   = BACKBONE_NAME,
        n_slices       = SIGREG_SLICES,
        n_points       = SIGREG_N_POINTS,
        lamb           = SIGREG_LAMBDA,
        pretrained     = False,
        drop_path_rate = 0.1,
    )

    # Tính tổng steps cho scheduler
    inet_train_size = 1_281_167
    total_steps     = (inet_train_size // BATCH_SIZE) * MAX_EPOCHS
    warmup_steps    = int(total_steps * WARMUP_RATIO)

    module = spt.Module(
        forward=lejepa_forward,
        model=model,
        hparams={
            "backbone":       BACKBONE_NAME,
            "max_epochs":     MAX_EPOCHS,
            "batch_size":     BATCH_SIZE,
            "lr":             LR,
            "weight_decay":   WEIGHT_DECAY,
            "lambda":         SIGREG_LAMBDA,
            "n_slices":       SIGREG_SLICES,
        },
        optim={
            "optimizer": {
                "type":         "AdamW",
                "lr":           LR,
                "weight_decay": WEIGHT_DECAY,
                "betas":        (0.9, 0.999),
            },
            "scheduler": {
                "type":         "LinearWarmupCosineAnnealing",
                "peak_step":    warmup_steps / total_steps,
                "start_factor": 0.01,
                "end_lr":       LR / 1000,
                "total_steps":  total_steps,
            },
            "interval": "step",
        },
    )

    # Online linear probe trên IN-1K (theo dõi training quality)
    inet_probe = spt.OnlineProbe(
        module=module,
        name="inet_probe",
        input="embedding",
        target="label",
        probe=nn.Linear(model.embed_dim, 1000),
        loss=nn.CrossEntropyLoss(),
        optimizer={"type": "AdamW", "lr": 1e-3, "weight_decay": 1e-6},
        metrics={
            "top1": torchmetrics.classification.MulticlassAccuracy(1000),
            "top5": torchmetrics.classification.MulticlassAccuracy(1000, top_k=5),
        },
    )

    rankme = spt.RankMe(
        name="rankme",
        target="embedding",
        queue_length=1000,
        target_shape=model.embed_dim,
    )

    return module, [inet_probe, rankme]


def run_pretraining(resume_ckpt: str = None) -> str:
    """Chạy pretraining LeJEPA ViT-L trên IN-1K.

    Returns:
        Path đến best checkpoint.
    """
    dm             = build_pretrain_datamodule()
    module, cbs    = build_pretrain_module()

    ckpt_cb = pl.callbacks.ModelCheckpoint(
        dirpath=str(CKPT_DIR),
        filename="lejepa-vitl-ep{epoch:03d}",
        save_top_k=3,
        monitor="eval/inet_probe_top1_epoch",
        mode="max",
        save_last=True,
        verbose=True,
    )

    trainer = pl.Trainer(
        max_epochs=MAX_EPOCHS,
        accelerator=ACCELERATOR,
        devices=DEVICES,
        precision=PRECISION,
        strategy="ddp_notebook" if _is_notebook() else "ddp_find_unused_parameters_true",
        callbacks=cbs + [
            ckpt_cb,
            spt.TrainerInfo(),
            spt.LoggingCallback(),
            pl.callbacks.LearningRateMonitor(logging_interval="step"),
        ],
        log_every_n_steps=50,
        val_check_interval=1.0,
        num_sanity_val_steps=0,   # tắt để tránh treo khi streaming
        default_root_dir=str(LOG_DIR),
    )

    manager = spt.Manager(trainer=trainer, module=module, data=dm, ckpt_path=resume_ckpt)
    manager()

    best = ckpt_cb.best_model_path or ckpt_cb.last_model_path
    print(f"\n✓ Pretraining done. Best checkpoint: {best}")
    return best


# %% [markdown]
# ## 5. Phase 2: Embedding Extraction

# %%
@torch.no_grad()
def extract_embeddings(
    model:            LeJEPA,
    hf_dataset_name:  str,
    split:            str,
    label_column:     str,
    device:           torch.device,
    batch_size:       int = EVAL_BS,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Load dataset, extract frozen embeddings từ backbone LeJEPA.

    Embedding = CLS token của last layer (model.eval() → model.backbone(x)).
    """
    rename = {label_column: "label"} if label_column != "label" else None
    ds = HFDataset(
        hf_dataset_name,
        split=split,
        transform=make_val_transform(),
        trust_remote_code=True,
        rename_columns=rename,
    )
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False,
                        num_workers=NUM_WORKERS, pin_memory=True)

    model = model.to(device).eval()
    all_embs, all_labels = [], []

    for batch in loader:
        imgs   = batch["image"].to(device, non_blocking=True)
        output = model(images=imgs)          # LeJEPAOutput, eval mode
        all_embs.append(output.embedding.cpu())
        all_labels.append(batch["label"])

    return torch.cat(all_embs), torch.cat(all_labels)


# %% [markdown]
# ## 6. Phase 3: Few-Shot Linear Probe

# %%
def sample_few_shot(
    emb:       torch.Tensor,
    labels:    torch.Tensor,
    n_shots:   int,
    n_classes: int,
    seed:      int,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Sample n_shots per class từ training embeddings."""
    rng = random.Random(seed)
    by_class = [[] for _ in range(n_classes)]
    for i, lbl in enumerate(labels.tolist()):
        if 0 <= int(lbl) < n_classes:
            by_class[int(lbl)].append(i)

    idx = []
    for c in range(n_classes):
        pool = by_class[c]
        idx.extend(rng.sample(pool, min(n_shots, len(pool))))

    sel = torch.tensor(idx)
    return emb[sel], labels[sel]


def train_linear_probe(
    train_emb:  torch.Tensor,
    train_lbl:  torch.Tensor,
    val_emb:    torch.Tensor,
    val_lbl:    torch.Tensor,
    n_classes:  int,
    device:     torch.device,
    epochs:     int = EVAL_EPOCHS,
    lr:         float = EVAL_LR,
) -> float:
    """Train LayerNorm → Linear probe với AdamW + cosine LR (theo README).

    Returns:
        top-1 accuracy (%) trên val set.
    """
    in_dim = train_emb.shape[-1]
    probe  = nn.Sequential(nn.LayerNorm(in_dim), nn.Linear(in_dim, n_classes)).to(device)

    train_dl = DataLoader(TensorDataset(train_emb, train_lbl),
                          batch_size=min(256, len(train_emb)), shuffle=True)
    opt   = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=1e-6)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs * len(train_dl))

    probe.train()
    for _ in range(epochs):
        for e, y in train_dl:
            e, y = e.to(device), y.to(device)
            opt.zero_grad()
            F.cross_entropy(probe(e), y).backward()
            opt.step()
            sched.step()

    probe.eval()
    correct = total = 0
    val_dl  = DataLoader(TensorDataset(val_emb, val_lbl), batch_size=512)
    with torch.no_grad():
        for e, y in val_dl:
            e, y     = e.to(device), y.to(device)
            correct += (probe(e).argmax(-1) == y).sum().item()
            total   += y.shape[0]
    return 100.0 * correct / total


# %% [markdown]
# ## 7. Full Evaluation Pipeline

# %%
def run_evaluation(checkpoint_path: str) -> dict:
    """Load pretrained LeJEPA, extract embeddings, chạy few-shot probe.

    Returns:
        { dataset_label: { "1": acc, "10": acc, "all": acc } }
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Tái tạo model và load weights
    model = LeJEPA(
        encoder_name=BACKBONE_NAME, n_slices=SIGREG_SLICES,
        n_points=SIGREG_N_POINTS, lamb=SIGREG_LAMBDA, pretrained=False,
    )
    ckpt  = torch.load(checkpoint_path, map_location="cpu")
    state = ckpt.get("state_dict", ckpt)
    # spt.Module lưu model dưới key "model.*"
    model_state = {k.removeprefix("model."): v
                   for k, v in state.items() if k.startswith("model.")}
    model.load_state_dict(model_state, strict=True)
    print(f"✓ Loaded LeJEPA ({BACKBONE_NAME}) from {checkpoint_path}")

    results = {}

    for (hf_name, n_cls, split_tr, split_te, lbl_col), ds_label in \
            zip(EVAL_DATASETS, EVAL_DATASET_LABELS):

        print(f"\n{'='*60}\n  {ds_label}  ({hf_name})\n{'='*60}")

        print("  ▶ Trích xuất TRAIN embeddings ...")
        tr_emb, tr_lbl = extract_embeddings(model, hf_name, split_tr, lbl_col, device)
        print(f"    → {tr_emb.shape}")

        print("  ▶ Trích xuất TEST embeddings ...")
        te_emb, te_lbl = extract_embeddings(model, hf_name, split_te, lbl_col, device)
        print(f"    → {te_emb.shape}")

        results[ds_label] = {}

        for shots in EVAL_SHOTS:
            if shots is None:
                acc = train_linear_probe(tr_emb, tr_lbl, te_emb, te_lbl, n_cls, device)
                print(f"  shots=all  → {acc:.2f}%")
                results[ds_label]["all"] = round(acc, 2)
            else:
                accs = [
                    train_linear_probe(
                        *sample_few_shot(tr_emb, tr_lbl, shots, n_cls, seed),
                        te_emb, te_lbl, n_cls, device,
                    )
                    for seed in EVAL_SEEDS
                ]
                acc = sum(accs) / len(accs)
                print(f"  shots={shots:3d}  → {acc:.2f}%  (seeds={EVAL_SEEDS})")
                results[ds_label][str(shots)] = round(acc, 2)

    return results


def print_results_table(results: dict):
    """In bảng theo format giống README."""
    ds_order    = EVAL_DATASET_LABELS
    shots_order = ["1", "10", "all"]

    header = f"{'shots':>6} │ " + " │ ".join(f"{d[:8]:>8}" for d in ds_order) + " │    avg."
    sep    = "─" * len(header)
    print(f"\n{sep}\n{header}\n{sep}")
    for shot in shots_order:
        row = [results.get(d, {}).get(shot, float("nan")) for d in ds_order]
        avg = sum(v for v in row if not math.isnan(v)) / max(1, sum(1 for v in row if not math.isnan(v)))
        print(f"{shot:>6} │ " + " │ ".join(f"{v:>8.2f}" for v in row) + f" │ {avg:>7.2f}")
    print(sep + "\n")


# %% [markdown]
# ## 8. Main

# %%
def main(skip_pretrain: bool = False, checkpoint_path: str = None):
    """Toàn bộ pipeline: pretrain → eval.

    Args:
        skip_pretrain:    Bỏ qua phase pretraining.
        checkpoint_path:  Bắt buộc nếu skip_pretrain=True.
    """
    if not skip_pretrain:
        print("=" * 60)
        print("Phase 1 — LeJEPA Pretraining on ImageNet-1K (ViT-L/16)")
        print("=" * 60)
        ckpt = run_pretraining()
    else:
        assert checkpoint_path, "Cần --checkpoint khi --skip-pretrain"
        ckpt = checkpoint_path
        print(f"Bỏ qua pretraining. Dùng checkpoint: {ckpt}")

    print("\n" + "=" * 60)
    print("Phase 2+3 — Embedding Extraction + Few-Shot Linear Probe")
    print("=" * 60)
    results = run_evaluation(ckpt)

    print("\n=== LeJEPA ViT-L (100ep IN-1K) — Few-Shot Linear Probe ===")
    print_results_table(results)
    return results


# %%
def _is_notebook() -> bool:
    """True nếu đang chạy trong Jupyter / Kaggle / Colab kernel."""
    return any(s in sys.argv[0] for s in ("ipykernel", "colab_kernel", "pydev"))


if __name__ == "__main__" and not _is_notebook():
    import argparse

    p = argparse.ArgumentParser(description="LeJEPA ViT-L Train + Eval")
    p.add_argument("--skip-pretrain", action="store_true",
                   help="Chỉ chạy eval, bỏ qua pretraining.")
    p.add_argument("--checkpoint",    type=str, default=None,
                   help="Path checkpoint .ckpt (bắt buộc khi --skip-pretrain).")
    p.add_argument("--resume",        type=str, default=None,
                   help="Resume pretraining từ checkpoint này.")
    args = p.parse_args()

    main(
        skip_pretrain   = args.skip_pretrain,
        checkpoint_path = args.checkpoint or args.resume,
    )

elif _is_notebook():
    main()
