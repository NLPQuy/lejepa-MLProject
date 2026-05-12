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

# Auto-load /workspace/.env
_env_file = "/workspace/.env"
if os.path.isfile(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.lstrip("export ").split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
    print(f"[env] Loaded {_env_file}")


_SHM_CACHE = "/workspace/hf_cache"
os.makedirs(_SHM_CACHE, exist_ok=True)
os.environ["HF_DATASETS_CACHE"] = _SHM_CACHE
os.environ["HF_HOME"]           = _SHM_CACHE
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
if "--skip-pretrain" in sys.argv:
    os.environ["SPT_LIGHT_IMPORT"] = "1"
else:
    os.environ["SPT_LIGHT_IMPORT"] = "0"

_shm_stat = os.statvfs("/dev/shm")
_shm_free_gb = _shm_stat.f_bfree * _shm_stat.f_frsize / 1e9
print(f"[shm] /dev/shm free: {_shm_free_gb:.1f} GB  →  cache dir: {_SHM_CACHE}")

# ── Cấu hình repo ─────────────────────────────────────────────────────────────
GITHUB_TOKEN  = os.environ.get("GITHUB_TOKEN", "") 
GITHUB_REPO   = "https://github.com/NLPQuy/lejepa-MLProject.git"
CLONE_DIR     = "/workspace/lejepa-MLProject"  # RunPod write dir

if os.environ.get("LEJEPA_SKIP_HF_LOGIN", "1") == "1":
    print("[hf] Skip HuggingFace login (LEJEPA_SKIP_HF_LOGIN=1).")
else:
    from huggingface_hub import login
    try:
        _hf_token = os.environ.get("HF_TOKEN", "")
        if _hf_token:
            login(token=_hf_token)
            print("[hf] Logged in to HuggingFace.")
        else:
            print("[hf] HF_TOKEN not set — skipping login (OK for local ImageNet training).")
    except BaseException as _hf_e:
        print(f"[hf] WARNING: HuggingFace login failed ({_hf_e}). Continuing without HF auth.")
        print("[hf] Training on local ImageNet will proceed normally.")

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

# Cài stable_pretraining từ source nếu chưa import được
def _ensure_stable_pretraining():
    try:
        import stable_pretraining  # noqa: F401
        return
    except Exception:
        pass

    _spt_src = os.path.join(CLONE_DIR, "stable-pretraining")
    print(f"[install] pip install -e {_spt_src}")
    # SETUPTOOLS_SCM_PRETEND_VERSION: bắt buộc vì .git đã bị xóa khỏi repo
    _env = {**os.environ, "SETUPTOOLS_SCM_PRETEND_VERSION": "0.0.0"}
    _run(f"{sys.executable} -m pip install -q -e '{_spt_src}'", env=_env)



# %% [markdown]
# # LeJEPA ViT-B — Pretraining (IN-1K) + Few-Shot Linear Probe Evaluation
#
# Reproduces the main table in the README:
# - **Backbone**: ViT-B/16 (86M params) via timm (`vit_base_patch16_224`)
# - **Pretrain**: ImageNet-1K, 1 epoch, effective BS=512 (64 × 8 grad accum)
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
import socket
from pathlib import Path

import lightning.pytorch as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
import torchvision
import timm
from torchvision.transforms import v2 as tv2
from torchvision.transforms.functional import InterpolationMode
from torch.utils.data import DataLoader, Subset, TensorDataset
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ── Tensor Core precision (recommended for H100 / A100) 
torch.set_float32_matmul_precision("high")

# ── stable_pretraining 


# %% [markdown]
# ## 1. Hyperparameters

# %%
# Backbone 
BACKBONE_NAME    = "vit_base_patch16_224"    # ViT-B/16, 86M params

# Pretraining 
PRETRAIN_DATASET = "ILSVRC/imagenet-1k"
MAX_EPOCHS       = 5
BATCH_SIZE       = 64
GRAD_ACCUM_STEPS = 8                      # effective BS = 64 * 8 = 512
LR               = 5e-4
WEIGHT_DECAY     = 5e-2
WARMUP_RATIO     = 0.1                        # 10% warmup
N_GLOBAL_VIEWS   = 2
N_LOCAL_VIEWS    = 4

# SIGReg (LeJEPA loss) — khớp với paper
SIGREG_LAMBDA    = 0.05
SIGREG_SLICES    = 1024
SIGREG_N_POINTS  = 17

# ── Eval datasets ─────────────────────────────────────────────────────────────
# (hf_dataset_name, n_classes, split_train, split_test, label_column)
EVAL_DATASETS = [
    ("tanganke/dtd",                     47,  "train", "test",       "label"),
    ("HuggingFaceM4/FGVC-Aircraft",     100,  "trainval", "test",    "variant"), # Aircraft
    ("tanganke/stanford_cars",          196,  "train", "test",       "label"),
    ("cifar10",                          10,  "train", "test",       "label"),
    ("cifar100",                        100,  "train", "test",       "fine_label"),
    ("nelorth/oxford-flowers",          102,  "train", "test",       "label"),
    ("ethz/food101",                    101,  "train", "validation", "label"),
    ("pcuenq/oxford-pets",               37,  "trainval", "test",    "label"),
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

# ── Local ImageNet-1K (RunPod server)
# Server có cả train/ và val/ riêng biệt, mỗi dir có class subfolders.
IMAGENET_ROOT = "/workspace/imagenet"

# ── Misc
NUM_WORKERS  = 16   # local SSD → có thể tăng workers
PRECISION    = "bf16-mixed"
ACCELERATOR  = "gpu"
DEVICES      = "auto"
CKPT_DIR     = Path("/workspace/checkpoints")
LOG_DIR      = Path(REPO_ROOT) / "logs"
CKPT_DIR.mkdir(parents=True, exist_ok=True)

IMG_MEAN = (0.485, 0.456, 0.406)
IMG_STD  = (0.229, 0.224, 0.225)

# %% [markdown]
# ## 2. Data Augmentation (Multi-Crop, theo README)

# %%
def _spt_transforms():
    from stable_pretraining.data import transforms as spt_transforms

    return spt_transforms


def _photometric_transforms() -> list:
    """Shared color augmentations cho cả global và local views."""
    t = _spt_transforms()
    return [
        t.RandomHorizontalFlip(p=0.5),
        t.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2, hue=0.1, p=0.8),
        t.RandomGrayscale(p=0.2),
        t.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0), p=0.5),
        t.RandomSolarize(threshold=128, p=0.2),
    ]


def make_global_transform():
    """Global view: 224×224, scale (0.3, 1.0)."""
    t = _spt_transforms()
    return t.Compose(
        t.RGB(),
        t.RandomResizedCrop((224, 224), scale=(0.3, 1.0)),
        *_photometric_transforms(),
        t.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_local_transform():
    """Local view: 98×98, scale (0.05, 0.3)."""
    t = _spt_transforms()
    return t.Compose(
        t.RGB(),
        t.RandomResizedCrop((96, 96), scale=(0.05, 0.3)),
        *_photometric_transforms(),
        t.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_val_transform():
    """Standard center-crop cho validation / embedding extraction."""
    t = _spt_transforms()
    return t.Compose(
        t.RGB(),
        t.Resize((256, 256)),
        t.CenterCrop((224, 224)),
        t.ToImage(mean=IMG_MEAN, std=IMG_STD),
    )


def make_val_transform_eval():
    """Eval-only center-crop transform (không phụ thuộc stable_pretraining)."""
    t = tv2.Compose([
        tv2.ToImage(),
        tv2.Resize((256, 256), interpolation=InterpolationMode.BICUBIC),
        tv2.CenterCrop((224, 224)),
        tv2.ToDtype(torch.float32, scale=True),
        tv2.Normalize(mean=IMG_MEAN, std=IMG_STD),
    ])

    def _apply(sample: dict) -> dict:
        sample["image"] = t(sample["image"])
        return sample

    return _apply


def make_train_transform(n_global: int = N_GLOBAL_VIEWS, n_local: int = N_LOCAL_VIEWS):
    """Multi-crop dict transform: keys 'global_i' và 'local_j'."""
    t = _spt_transforms()
    return t.MultiViewTransform({
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

        output = self.model(
            global_views=global_views,
            local_views=local_views,
            images=images,
        )
        out["label"] = labels.repeat(len(global_views))

    else:
        output = self.model(images=images)
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
class KaggleImageNetDataset(torch.utils.data.Dataset):
    """Wrapper quanh torchvision.ImageFolder, output dict tương thích lejepa_forward.

    Training (multi-view transform):  {"global_0": {"image": T, "label": L}, ...}
    Eval   (single-view transform):   {"image": T, "label": L}

    spt transforms nhận dict {"image": PIL, "label": int} → trả dict tương tự.
    """
    def __init__(self, root: str, transform=None):
        self.folder    = torchvision.datasets.ImageFolder(root)
        self.transform = transform

    def __len__(self):
        return len(self.folder)

    def __getitem__(self, idx):
        while True:
            try:
                pil_img, label = self.folder[idx]
                item = {"image": pil_img, "label": label}
                if self.transform is not None:
                    return self.transform(item)
                return item
            except Exception as e:
                print(f"[warning] Skipping corrupted image at index {idx}: {e}")
                idx = (idx + 1) % len(self.folder)


class DictWrapDataset(torch.utils.data.Dataset):
    """Wrap any dataset to return dicts with optional transform."""

    def __init__(self, dataset, transform=None):
        self.dataset = dataset
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        sample = self.dataset[idx]
        if isinstance(sample, dict):
            item = sample
        else:
            image, label = sample
            item = {"image": image, "label": label}
        if self.transform is not None:
            item = self.transform(item)
        return item


def build_pretrain_datamodule() -> "DataModule":
    """DataModule dùng ImageNet-1K trên RunPod server.

    Train dir và val dir đều có class subfolders → ImageFolder hoạt động tốt.
    """
    train_root = os.path.join(IMAGENET_ROOT, "train")
    val_root   = os.path.join(IMAGENET_ROOT, "val")
    print(f"[data] ImageNet-1K train: {train_root}")
    print(f"[data] ImageNet-1K val:   {val_root}")

    train_ds = KaggleImageNetDataset(train_root, transform=make_train_transform())
    val_ds   = KaggleImageNetDataset(val_root,   transform=make_val_transform())

    print(f"[data] train={len(train_ds):,}  val={len(val_ds):,}")

    from stable_pretraining.data.module import DataModule

    return DataModule(
        train=DataLoader(
            train_ds,
            batch_size=BATCH_SIZE, shuffle=True,
            num_workers=NUM_WORKERS, drop_last=True,
            pin_memory=True, persistent_workers=True,
        ),
        val=DataLoader(
            val_ds,
            batch_size=BATCH_SIZE, shuffle=False,
            num_workers=NUM_WORKERS,
            pin_memory=True, persistent_workers=True,
        ),
    )


def build_pretrain_module() -> tuple["SPTModule", list]:
    """Tạo spt.Module bọc LeJEPA (ViT-B) + các callbacks."""
    from stable_pretraining.module import Module as SPTModule
    from stable_pretraining.callbacks.probe import OnlineProbe
    from stable_pretraining.callbacks.rankme import RankMe
    from stable_pretraining.methods.lejepa import LeJEPA

    # LeJEPA tự tạo backbone (timm ViT-B), projector MLP, và SlicedEppsPulley
    model = LeJEPA(
        encoder_name   = BACKBONE_NAME,
        n_slices       = SIGREG_SLICES,
        n_points       = SIGREG_N_POINTS,
        lamb           = SIGREG_LAMBDA,
        pretrained     = False,
        drop_path_rate = 0.0,
    )

    # Tính tổng steps cho scheduler (optimizer steps, không phải micro-batch)
    inet_train_size = 1_281_167
    total_steps     = (inet_train_size // BATCH_SIZE // GRAD_ACCUM_STEPS) * MAX_EPOCHS
    warmup_steps    = int(total_steps * WARMUP_RATIO)

    module = SPTModule(
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
    inet_probe = OnlineProbe(
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

    rankme = RankMe(
        name="rankme",
        target="embedding",
        queue_length=1000,
        target_shape=model.embed_dim,
    )

    return module, [inet_probe, rankme]


def _find_free_port() -> int:
    """Bind to port 0 (OS picks a free port), then release it immediately.

    Used to avoid EADDRINUSE when a prior training run crashed without
    releasing its DDP rendezvous port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", 0))
        return s.getsockname()[1]


def run_pretraining(resume_ckpt: str = None) -> str:
    """Chạy pretraining LeJEPA ViT-B trên IN-1K.

    Returns:
        Path đến best checkpoint.
    """
    _ensure_stable_pretraining()

    # Pick a free port for DDP rendezvous to avoid EADDRINUSE
    # from a previously crashed training session in the same kernel.
    free_port = _find_free_port()
    os.environ["MASTER_PORT"] = str(free_port)
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    print(f"[DDP] Using MASTER_PORT={free_port}")

    dm             = build_pretrain_datamodule()
    module, cbs    = build_pretrain_module()

    from stable_pretraining.callbacks.trainer_info import LoggingCallback, TrainerInfo
    from stable_pretraining.manager import Manager

    ckpt_cb = pl.callbacks.ModelCheckpoint(
        dirpath=str(CKPT_DIR),
        filename="lejepa-vitb-ep{epoch:03d}",
        save_top_k=-1,               # lưu tất cả, không cần monitor
        monitor=None,                # không monitor metric (val set hỏng)
        save_last=True,
        save_on_train_epoch_end=True, # lưu ngay sau train epoch, trước val
        verbose=True,
    )

    # Strategy selection:
    # - With 1 GPU (most Kaggle/Colab setups): always use 'auto', which resolves
    #   to SingleDeviceStrategy — no subprocess spawn, no distributed init,
    #   no EADDRINUSE risk.
    # - With multiple GPUs in a notebook: use 'ddp_notebook' (fork-based DDP).
    # - With multiple GPUs in a script: use full DDP.
    n_gpus = torch.cuda.device_count()
    if n_gpus <= 1:
        strategy = "auto"   # SingleDeviceStrategy — avoids all distributed init
    elif _is_notebook():
        strategy = "ddp_notebook"
    else:
        strategy = "ddp_find_unused_parameters_true"

    trainer = pl.Trainer(
        max_epochs=MAX_EPOCHS,
        accelerator=ACCELERATOR,
        devices=DEVICES,
        precision=PRECISION,
        strategy=strategy,
        accumulate_grad_batches=GRAD_ACCUM_STEPS,
        callbacks=cbs + [
            ckpt_cb,
            TrainerInfo(),
            LoggingCallback(),
            pl.callbacks.LearningRateMonitor(logging_interval="step"),
        ],
        log_every_n_steps=50,
        limit_val_batches=0,          # tắt validation — val set bị hỏng (50K files 0 bytes)
        num_sanity_val_steps=0,
        default_root_dir=str(LOG_DIR),
    )

    manager = Manager(trainer=trainer, module=module, data=dm, ckpt_path=resume_ckpt)
    manager()

    best = ckpt_cb.best_model_path or ckpt_cb.last_model_path
    print(f"\n✓ Pretraining done. Best checkpoint: {best}")
    return best


# %% [markdown]
# ## 5. Phase 2: Embedding Extraction

# %%
@torch.no_grad()
def extract_embeddings(
    backbone:         nn.Module,
    hf_dataset_name:  str,
    split:            str,
    label_column:     str,
    device:           torch.device,
    batch_size:       int = EVAL_BS,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Load dataset, extract frozen embeddings từ backbone LeJEPA.

    Embedding = concat(CLS[-2], CLS[-1]) theo paper spec (CLAUDE.md, line 172).
    """
    if hf_dataset_name in ["cifar10", "cifar100", "HuggingFaceM4/FGVC-Aircraft", "pcuenq/oxford-pets"]:
        is_train = split in ["train", "trainval"]

        if hf_dataset_name == "cifar10":
            tv_ds = torchvision.datasets.CIFAR10(root="./data", train=is_train, download=True)
        elif hf_dataset_name == "cifar100":
            tv_ds = torchvision.datasets.CIFAR100(root="./data", train=is_train, download=True)
        elif hf_dataset_name == "HuggingFaceM4/FGVC-Aircraft":
            tv_split = "trainval" if is_train else "test"
            tv_ds = torchvision.datasets.FGVCAircraft(root="./data", split=tv_split, download=True)
        else:  # pcuenq/oxford-pets
            tv_split = "trainval" if is_train else "test"
            tv_ds = torchvision.datasets.OxfordIIITPet(root="./data", split=tv_split, download=True)

        ds = DictWrapDataset(tv_ds, transform=make_val_transform_eval())
    else:
        from datasets import load_dataset

        ds = load_dataset(hf_dataset_name, split=split)
        if label_column != "label":
            ds = ds.rename_column(label_column, "label")
        if "image" not in ds.column_names:
            raise ValueError(f"Dataset {hf_dataset_name} thiếu cột 'image': {ds.column_names}")
        ds = DictWrapDataset(ds, transform=make_val_transform_eval())

    loader = DataLoader(ds, batch_size=batch_size, shuffle=False,
                        num_workers=0, pin_memory=False)

    backbone = backbone.to(device).eval()
    all_embs, all_labels = [], []

    str_mapping: dict = {}

    _penultimate_cls: list = []

    def _penultimate_hook(module, inp, out):
        # out: [B, seq_len, D] — lấy CLS token (index 0)
        _penultimate_cls.append(out[:, 0].detach().cpu())

    n_blocks = len(backbone.blocks)
    _hook_handle = backbone.blocks[n_blocks - 2].register_forward_hook(
        _penultimate_hook
    )

    try:
        for batch in loader:
            imgs = batch["image"].to(device, non_blocking=True)
            _penultimate_cls.clear()

            last_cls = backbone(imgs).cpu()       # [B, D]  — CLS from final block
            pen_cls  = _penultimate_cls[-1]       # [B, D]  — CLS from penultimate block
            emb = torch.cat([pen_cls, last_cls], dim=-1)  # [B, 2D]
            all_embs.append(emb)

            lbl = batch["label"]

            # ── Chuẩn hóa label về 1-D LongTensor ────────────────────────────
            if isinstance(lbl, torch.Tensor):
                pass  # already an integer tensor from collation
            elif isinstance(lbl, (list, tuple)):
                first = lbl[0] if len(lbl) > 0 else 0
                if isinstance(first, str):
                    # HF ClassLabel.str2int nếu có, ngược lại dùng local mapping
                    feat = None
                    if hasattr(ds, "dataset") and hasattr(ds.dataset, "features"):
                        feat = ds.dataset.features.get("label")
                    if feat is not None and hasattr(feat, "str2int"):
                        lbl = [feat.str2int(x) for x in lbl]
                    else:
                        mapped = []
                        for x in lbl:
                            if x not in str_mapping:
                                str_mapping[x] = len(str_mapping)
                            mapped.append(str_mapping[x])
                        lbl = mapped
                lbl = torch.tensor(lbl)
            else:
                lbl = torch.tensor([int(lbl)])

            all_labels.append(lbl.reshape(-1).long())
    finally:
        _hook_handle.remove()  # luôn gỡ hook dù có exception

    if not all_embs:
        raise ValueError(f"Dataset rỗng — không có đủ embeddings từ split='{split}'.")
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

    in_dim = 2*embed_dim (concat of 2 CLS tokens).
    Returns:
        top-1 accuracy (%) trên val set.
    """
    if len(train_emb) == 0:
        raise ValueError("train_emb rỗng — không có đủ sample để train probe.")

    in_dim = train_emb.shape[-1]  # 2*embed_dim after dual-CLS concat
    probe  = nn.Sequential(nn.LayerNorm(in_dim), nn.Linear(in_dim, n_classes)).to(device)

    train_dl = DataLoader(TensorDataset(train_emb, train_lbl.long()),
                          batch_size=min(256, len(train_emb)), shuffle=True)
    opt   = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=1e-6)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, epochs * len(train_dl)))

    probe.train()
    for _ in range(epochs):
        for e, y in train_dl:
            e, y = e.to(device), y.long().to(device)
            opt.zero_grad()
            F.cross_entropy(probe(e), y).backward()
            opt.step()
            sched.step()

    probe.eval()
    correct = total = 0
    val_dl  = DataLoader(TensorDataset(val_emb, val_lbl.long()), batch_size=512)
    with torch.no_grad():
        for e, y in val_dl:
            e, y     = e.to(device), y.long().to(device)
            correct += (probe(e).argmax(-1) == y).sum().item()
            total   += y.shape[0]
    return 100.0 * correct / total if total > 0 else 0.0


# %% [markdown]
# ## 7. Full Evaluation Pipeline

# %%
def run_evaluation(checkpoint_path: str) -> dict:
    """Load pretrained LeJEPA, extract embeddings, chạy few-shot probe.

    Returns:
        { dataset_label: { "1": acc, "10": acc, "all": acc } }
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[eval] device = {device}")

    # ── Tái tạo backbone và load weights ─────────────────────────────────────
    # drop_path_rate=0.0 phải khớp với lúc train để load_state_dict không lỗi.
    backbone = timm.create_model(
        BACKBONE_NAME,
        pretrained=False,
        num_classes=0,
        **({"dynamic_img_size": True} if "vit" in BACKBONE_NAME else {}),
        drop_path_rate=0.0,
    )
    ckpt  = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    state = ckpt.get("state_dict", ckpt)

    # Lọc chỉ lấy keys bắt đầu bằng "model.backbone." (bỏ projector/callbacks)
    backbone_state = {k.removeprefix("model.backbone."): v
                      for k, v in state.items() if k.startswith("model.backbone.")}
    if not backbone_state:
        raise RuntimeError(
            f"Không tìm thấy key 'model.backbone.*' trong checkpoint: {checkpoint_path}\n"
            f"Các key có trong checkpoint: {list(state.keys())[:10]}"
        )
    missing, unexpected = backbone.load_state_dict(backbone_state, strict=False)
    if missing:
        raise RuntimeError(f"Missing backbone keys khi load checkpoint: {missing[:5]}")
    if unexpected:
        print(f"[eval] ⚠ Unexpected keys (ignored): {unexpected[:5]}")
    print(f"✓ Loaded backbone ({BACKBONE_NAME}) from {checkpoint_path}")

    results = {}

    for (hf_name, n_cls, split_tr, split_te, lbl_col), ds_label in \
            zip(EVAL_DATASETS, EVAL_DATASET_LABELS):

        print(f"\n{'='*60}\n  {ds_label}  ({hf_name})\n{'='*60}")
        try:
            print("  ▶ Trích xuất TRAIN embeddings ...")
            tr_emb, tr_lbl = extract_embeddings(backbone, hf_name, split_tr, lbl_col, device)
            print(f"    → {tr_emb.shape}")

            print("  ▶ Trích xuất TEST embeddings ...")
            te_emb, te_lbl = extract_embeddings(backbone, hf_name, split_te, lbl_col, device)
            print(f"    → {te_emb.shape}")

            # Chuẩn hóa labels về [0, n_classes-1] (tránh case label 1-based)
            tr_lbl = tr_lbl.long().cpu()
            te_lbl = te_lbl.long().cpu()
            uniq = torch.unique(torch.cat([tr_lbl, te_lbl])).sort().values
            if len(uniq) != n_cls:
                print(f"  ⚠ label count mismatch: uniq={len(uniq)} vs n_classes={n_cls}")
            tr_lbl = torch.searchsorted(uniq, tr_lbl)
            te_lbl = torch.searchsorted(uniq, te_lbl)

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

        except Exception as _eval_e:
            print(f"  ❌ SKIP {ds_label}: {_eval_e}")
            results[ds_label] = {}   # giữ partial results, không crash toàn bộ

    return results


def print_results_table(results: dict):
    """In bảng theo format giống README."""
    ds_order    = EVAL_DATASET_LABELS
    shots_order = ["1", "10", "all"]

    header = f"{'shots':>6} │ " + " │ ".join(f"{d[:11]:>11}" for d in ds_order) + " │    avg."
    sep    = "─" * len(header)
    print(f"\n{sep}\n{header}\n{sep}")
    for shot in shots_order:
        row = [results.get(d, {}).get(shot, float("nan")) for d in ds_order]
        avg = sum(v for v in row if not math.isnan(v)) / max(1, sum(1 for v in row if not math.isnan(v)))
        print(f"{shot:>6} │ " + " │ ".join(f"{v:>11.2f}" for v in row) + f" │ {avg:>7.2f}")
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
        print("Phase 1 — LeJEPA Pretraining on ImageNet-1K (ViT-B/16)")
        print("=" * 60)
        # Train từ đầu (scratch) — KHÔNG resume từ checkpoint cũ.
        # Theo yêu cầu pipeline: chỉ train 10 epochs hoàn toàn mới.
        print("Training from scratch (no resume).")
        ckpt = run_pretraining(resume_ckpt=None)
    else:
        assert checkpoint_path, "Cần --checkpoint khi --skip-pretrain"
        ckpt = checkpoint_path
        print(f"Bỏ qua pretraining. Dùng checkpoint: {ckpt}")

    if not ckpt or not os.path.isfile(str(ckpt)):
        print(f"\n⚠ Không tìm thấy checkpoint: {ckpt!r}")
        print("⚠ Bỏ qua eval. Hãy kiểm tra lại /workspace/lejepa-MLProject/checkpoints/")
        return {}

    print("\n" + "=" * 60)
    print("Phase 2+3 — Embedding Extraction + Few-Shot Linear Probe")
    print("=" * 60)
    results = run_evaluation(ckpt)

    print("\n=== LeJEPA ViT-B (1ep IN-1K) — Few-Shot Linear Probe ===")
    print_results_table(results)
    return results


# %%
def _is_notebook() -> bool:
    """True nếu đang chạy trong Jupyter / Kaggle / Colab kernel."""
    return any(s in sys.argv[0] for s in ("ipykernel", "colab_kernel", "pydev"))


if os.environ.get("LEJEPA_DEBUG_MAIN") == "1":
    print(f"[debug] __name__={__name__} _is_notebook={_is_notebook()}")


if __name__ == "__main__" and not _is_notebook():
    import argparse

    p = argparse.ArgumentParser(description="LeJEPA ViT-B Train + Eval")
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