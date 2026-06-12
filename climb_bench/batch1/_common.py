"""Shared runner for batch-1 LeJEPA experiments on ImageNet-10 (Imagenette).

Extracted verbatim from ``benchmarks/imagenet10/lejepa-vit-small.py`` so every
``exp<x>.py`` is a thin wrapper: build a model (base ``LeJEPA`` or a subclass /
swapped component from ``_variants.py``), then call :func:`run`.

The transforms, dataset loader, forward, CLI args, and the
OnlineProbe + OnlineKNN + RankMe callback stack are identical across all
experiments so results are apples-to-apples.
"""

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("SPT_LIGHT_IMPORT", "0")  # export Module, Manager, callbacks

import lightning as pl
import torch
import torch.nn as nn
import torchmetrics

import stable_pretraining as spt
from stable_pretraining.data import transforms
from stable_pretraining.methods.lejepa import LeJEPAOutput


# ---------------------------------------------------------------------------
# Shared helpers (identical to lejepa-vit-small.py baseline)
# ---------------------------------------------------------------------------

def backbone_tag(name: str) -> str:
    """vit_small_patch16_224 -> vits, vit_tiny_patch16_224 -> vitt."""
    parts = name.split("_")
    return parts[0] + parts[1][0] if len(parts) >= 2 else name


def _photometric_transforms() -> list:
    return [
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2, hue=0.1, p=0.8),
        transforms.RandomGrayscale(p=0.2),
        transforms.GaussianBlur(kernel_size=23, sigma=(0.1, 2.0), p=0.5),
        transforms.RandomSolarize(threshold=128, p=0.2),
    ]


def _global_transform():
    return transforms.Compose(
        transforms.RGB(),
        transforms.RandomResizedCrop((224, 224), scale=(0.3, 1.0)),
        *_photometric_transforms(),
        transforms.ToImage(**spt.data.static.ImageNet),
    )


def _local_transform():
    return transforms.Compose(
        transforms.RGB(),
        transforms.RandomResizedCrop((96, 96), scale=(0.05, 0.3)),
        *_photometric_transforms(),
        transforms.ToImage(**spt.data.static.ImageNet),
    )


def _build_datasets(args, train_transform, val_transform):
    """Load imagenette from a local save_to_disk path or via HuggingFace."""
    if args.data_local_path:
        local = Path(args.data_local_path)
        train_ds = spt.data.HFDataset(str(local / "train"), transform=train_transform)
        val_ds = spt.data.HFDataset(str(local / "validation"), transform=val_transform)
    else:
        sys.path.append(str(Path(__file__).parent.parent.parent / "stable-pretraining" / "benchmarks"))
        from utils import get_data_dir
        cache = str(get_data_dir("imagenet10"))
        train_ds = spt.data.HFDataset(
            "frgfm/imagenette", split="train",
            revision="refs/convert/parquet", cache_dir=cache,
            transform=train_transform,
        )
        val_ds = spt.data.HFDataset(
            "frgfm/imagenette", split="validation",
            revision="refs/convert/parquet", cache_dir=cache,
            transform=val_transform,
        )
    return train_ds, val_ds


def lejepa_forward(self, batch, stage):
    out = {}
    images = batch.get("image")
    if stage == "fit":
        global_views = [batch[k]["image"] for k in batch if k.startswith("global")]
        local_views = [batch[k]["image"] for k in batch if k.startswith("local")]
        labels = next(batch[k]["label"] for k in batch if k.startswith(("global", "local")))
        output: LeJEPAOutput = self.model.forward(
            global_views=global_views, local_views=local_views, images=images
        )
        out["label"] = labels.repeat(len(global_views))
    else:
        output: LeJEPAOutput = self.model.forward(images=images)
        out["label"] = batch["label"].long()
    out["loss"] = output.loss
    out["embedding"] = output.embedding
    self.log(f"{stage}/sigreg", output.sigreg_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/inv", output.inv_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/loss", output.loss, on_step=True, on_epoch=True, sync_dist=True)
    return out


# ---------------------------------------------------------------------------
# Shared CLI — exp scripts add their own knobs on top of this parser
# ---------------------------------------------------------------------------

def base_parser(description: str = "LeJEPA batch-1 experiment") -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--backbone", default="vit_small_patch16_224",
                   help="timm model, e.g. vit_small_patch16_224 | vit_tiny_patch16_224")
    p.add_argument("--max_epochs", type=int, default=400)
    p.add_argument("--max_steps", type=int, default=-1, help="override for smoke tests")
    p.add_argument("--batch_size", type=int, default=128)
    p.add_argument("--num_workers", type=int, default=4)
    p.add_argument("--num_gpus", type=int, default=1)
    p.add_argument("--accelerator", default="gpu", help="gpu | cpu (cpu for smoke tests)")
    p.add_argument("--lr", type=float, default=4e-4)
    p.add_argument("--weight_decay", type=float, default=0.05)
    p.add_argument("--lamb", type=float, default=0.02)
    p.add_argument("--proj_dim", type=int, default=512)
    p.add_argument("--n_slices", type=int, default=1024)
    p.add_argument("--global_views", type=int, default=2)
    p.add_argument("--all_views", type=int, default=8)
    p.add_argument("--precision", default="16-mixed")
    p.add_argument("--data_local_path", default=None,
                   help="Local imagenette saved via save_to_disk(): <path>/train, <path>/validation")
    p.add_argument("--run_name", default=None)
    p.add_argument("--wandb_entity", default="stable-ssl")
    p.add_argument("--wandb_project", default="imagenet10-batch1")
    p.add_argument("--checkpoint_dir", default=None)
    p.add_argument("--wandb_offline", action="store_true")
    p.add_argument("--no_wandb", action="store_true", help="CSV logger instead of W&B")
    return p


# ---------------------------------------------------------------------------
# Shared training driver
# ---------------------------------------------------------------------------

def run(model, args, tag: str):
    """Train ``model`` with the shared data + callback stack.

    :param model: a ``LeJEPA`` (or subclass) instance, fully constructed.
    :param args: parsed args from :func:`base_parser` (+ exp-specific knobs).
    :param tag: short experiment id used for run name / checkpoint dir (e.g. "exp3-codingrate").
    """
    btag = backbone_tag(args.backbone)
    run_name = args.run_name or f"{tag}-{btag}-inet10"
    ckpt_dir = args.checkpoint_dir or str(Path(__file__).parent / "checkpoints" / f"{tag}-{btag}")
    local_views = args.all_views - args.global_views

    train_transform = transforms.MultiViewTransform({
        **{f"global_{i}": _global_transform() for i in range(args.global_views)},
        **{f"local_{i}": _local_transform() for i in range(local_views)},
    })
    val_transform = transforms.Compose(
        transforms.RGB(),
        transforms.Resize((256, 256)),
        transforms.CenterCrop((224, 224)),
        transforms.ToImage(**spt.data.static.ImageNet),
    )

    train_ds, val_ds = _build_datasets(args, train_transform, val_transform)

    data = spt.data.DataModule(
        train=torch.utils.data.DataLoader(
            dataset=train_ds, batch_size=args.batch_size,
            num_workers=args.num_workers, drop_last=True,
            persistent_workers=args.num_workers > 0, shuffle=True,
        ),
        val=torch.utils.data.DataLoader(
            dataset=val_ds, batch_size=args.batch_size,
            num_workers=args.num_workers,
            persistent_workers=args.num_workers > 0,
        ),
    )

    total_steps = (len(data.train) // args.num_gpus) * args.max_epochs
    module = spt.Module(
        model=model,
        forward=lejepa_forward,
        optim={
            "optimizer": {"type": "AdamW", "lr": args.lr, "weight_decay": args.weight_decay, "betas": (0.9, 0.999)},
            "scheduler": {
                "type": "LinearWarmupCosineAnnealing",
                "peak_step": 10 / args.max_epochs,
                "start_factor": 0.01,
                "end_lr": args.lr / 1000,
                "total_steps": total_steps,
            },
            "interval": "step",
        },
    )

    trainer_kwargs = dict(
        max_epochs=args.max_epochs,
        num_sanity_val_steps=0,
        callbacks=[
            spt.callbacks.OnlineProbe(
                module, name="linear_probe", input="embedding", target="label",
                probe=nn.Linear(model.embed_dim, 10), loss=nn.CrossEntropyLoss(),
                metrics={
                    "top1": torchmetrics.classification.MulticlassAccuracy(10),
                    "top5": torchmetrics.classification.MulticlassAccuracy(10, top_k=5),
                },
                optimizer={"type": "AdamW", "lr": 0.03, "weight_decay": 1e-6},
            ),
            spt.callbacks.OnlineKNN(
                name="knn_probe", input="embedding", target="label",
                queue_length=10000,
                metrics={"top1": torchmetrics.classification.MulticlassAccuracy(10)},
                input_dim=model.embed_dim, k=20,
            ),
            spt.callbacks.RankMe(name="rankme", target="embedding", queue_length=1000, target_shape=model.embed_dim),
            pl.pytorch.callbacks.ModelCheckpoint(
                dirpath=ckpt_dir, filename=f"{tag}-{btag}-{{epoch:03d}}",
                save_top_k=-1, every_n_epochs=max(args.max_epochs // 2, 1), save_last=True,
            ),
            pl.pytorch.callbacks.LearningRateMonitor(logging_interval="step"),
        ],
        logger=(
            pl.pytorch.loggers.CSVLogger(save_dir=ckpt_dir, name="csv_logs")
            if args.no_wandb
            else pl.pytorch.loggers.WandbLogger(
                entity=args.wandb_entity, project=args.wandb_project,
                name=run_name, log_model=False, offline=args.wandb_offline,
            )
        ),
        precision=args.precision,
        devices=args.num_gpus,
        accelerator=args.accelerator,
        strategy="ddp_find_unused_parameters_true" if args.num_gpus > 1 else "auto",
    )
    if args.max_steps and args.max_steps > 0:
        trainer_kwargs["max_steps"] = args.max_steps

    trainer = pl.Trainer(**trainer_kwargs)
    spt.Manager(trainer=trainer, module=module, data=data)()
