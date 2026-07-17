"""Shared runner for batch-7 LeJEPA experiments on Imagenette.

Forked from ``climb_bench/batch2/_common.py``. Transforms, dataset, forward and the
OnlineProbe/OnlineKNN/RankMe callback stack are byte-identical to batch-1/2 so
rankings stay apples-to-apples across batches.

DELIBERATELY REMOVED vs batch-2: the optimizer-variant machinery (Muon,
schedule-free, SAM, PCGrad, SWA, stochastic-depth scheduling) and its ``_vendor``
wheels. Batch-7 is a loss/objective batch — every exp runs stock AdamW in automatic
optimization (plan §4). Keeping that machinery would mean copying four batch-2
callback classes into ``batch7/_variants.py`` that no batch-7 exp ever constructs.

ADDED vs batch-2:
  * ``--sigreg`` dispatch (``model.sigreg = ...``) for exp1/exp2/exp3.
  * A param-group split (``build_param_groups``) so the auxiliary nets that the
    batch-7 SIGReg variants introduce — score net, velocity field, adversarial
    slicing head — get their own lr multiplier and, critically, **wd=0**.
    batch-2's ``_adamw_params`` returns a flat ``model.parameters()``, which would
    put ``wd=0.05`` on all three and train the adversary at the encoder's lr
    (spec asks for 10x — batch-7.md §Idea 3).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("SPT_LIGHT_IMPORT", "0")

import lightning as pl
import torch
import torch.nn as nn
import torchmetrics

import stable_pretraining as spt
from stable_pretraining.data import transforms
from stable_pretraining.methods.lejepa import LeJEPAOutput

from _variants import AdversarialSIGReg, FMSIGRegA, FMSIGRegB, KLScoreSIGReg


def backbone_tag(name: str) -> str:
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
    out["inv_loss"] = output.inv_loss
    out["sigreg_loss"] = output.sigreg_loss
    self.log(f"{stage}/sigreg", output.sigreg_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/inv", output.inv_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/loss", output.loss, on_step=True, on_epoch=True, sync_dist=True)
    # exp5/exp7 diagnostics. These are not decoration: exp7's entropy- and
    # reward-monotonicity guards and exp5's prototype-usage entropy are the only
    # things that separate "the mechanism engaged" from "it silently did nothing".
    for attr in ("last_rl", "last_etf"):
        for k, v in (getattr(self.model, attr, None) or {}).items():
            self.log(f"{stage}/{attr[5:]}_{k}", v, on_step=True, on_epoch=True, sync_dist=True)
    return out


def base_parser(description: str = "LeJEPA batch-7 experiment") -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--backbone", default="vit_small_patch16_224")
    p.add_argument("--max_epochs", type=int, default=400)
    p.add_argument("--max_steps", type=int, default=-1)
    p.add_argument("--batch_size", type=int, default=128)
    p.add_argument("--num_workers", type=int, default=4)
    p.add_argument("--num_gpus", type=int, default=1)
    p.add_argument("--accelerator", default="gpu")
    p.add_argument("--lr", type=float, default=4e-4)
    p.add_argument("--weight_decay", type=float, default=0.05)
    p.add_argument("--lamb", type=float, default=0.02)
    p.add_argument("--proj_dim", type=int, default=512)
    p.add_argument("--n_slices", type=int, default=1024)
    p.add_argument("--global_views", type=int, default=2)
    p.add_argument("--all_views", type=int, default=8)
    p.add_argument("--precision", default="16-mixed")
    p.add_argument("--drop_path_rate", type=float, default=0.1)
    p.add_argument("--data_local_path", default=None)
    p.add_argument("--run_name", default=None)
    p.add_argument("--wandb_entity", default="stable-ssl")
    p.add_argument("--wandb_project", default="imagenet10-batch7")
    p.add_argument("--checkpoint_dir", default=None)
    p.add_argument("--wandb_offline", action="store_true")
    p.add_argument("--no_wandb", action="store_true")

    # --- batch-7 additions -------------------------------------------------
    p.add_argument("--sigreg", choices=["ep", "klscore", "adversarial", "fm"], default="ep",
                   help="'ep' (default) leaves the stock SlicedEppsPulley => exact baseline")
    p.add_argument("--aux_lr_mult", type=float, default=1.0,
                   help="lr multiplier for SIGReg auxiliary nets (score/velocity/adversary). "
                        "batch-7.md Idea 3 asks for 10x on the adversary.")
    p.add_argument("--fm_form", choices=["a", "b"], default="b",
                   help="a = as-written spec (FAILS Phase 0, kept as the falsification "
                        "arm); b = two-player (ships)")
    p.add_argument("--fm_path", choices=["ot", "vp"], default="ot")
    p.add_argument("--fm_t_lo", type=float, default=0.3)
    p.add_argument("--fm_t_hi", type=float, default=0.7)
    return p


def build_sigreg(args) -> nn.Module | None:
    """Return the SIGReg module to swap in, or None to keep the stock EP baseline."""
    if args.sigreg == "ep":
        return None
    if args.sigreg == "klscore":
        return KLScoreSIGReg(dim=args.proj_dim)
    if args.sigreg == "adversarial":
        return AdversarialSIGReg(dim=args.proj_dim)
    if args.sigreg == "fm":
        if args.fm_form == "a":
            return FMSIGRegA(dim=args.proj_dim, path=args.fm_path)
        return FMSIGRegB(dim=args.proj_dim, path=args.fm_path,
                         t_lo=args.fm_t_lo, t_hi=args.fm_t_hi)
    raise ValueError(f"unknown sigreg {args.sigreg!r}")


def build_param_groups(model: nn.Module, args) -> list[dict]:
    """Split encoder/projector from the SIGReg auxiliary nets.

    The batch-7 SIGReg variants carry trainable nets of their own (score net,
    velocity field, adversarial slicing head). Those are NOT representation
    parameters and must not be weight-decayed: they are function approximators
    fitting a score/velocity, and decaying them biases the estimate toward zero.
    ``SlicedEppsPulley`` has no parameters, so under ``--sigreg ep`` the aux group
    is empty and this reduces exactly to batch-2's ``model.parameters()``.
    """
    aux = list(model.sigreg.parameters()) if hasattr(model, "sigreg") else []
    aux_ids = {id(p) for p in aux}
    main = [p for p in model.parameters() if id(p) not in aux_ids]

    groups = [{"params": main, "lr": args.lr, "weight_decay": args.weight_decay}]
    if aux:
        groups.append({"params": aux, "lr": args.lr * args.aux_lr_mult, "weight_decay": 0.0})
    return groups


def build_optim(model: nn.Module, args, total_steps: int) -> dict:
    return {
        "optimizer": lambda _params: torch.optim.AdamW(
            build_param_groups(model, args), lr=args.lr,
            weight_decay=args.weight_decay, betas=(0.9, 0.999),
        ),
        "interval": "step",
        "scheduler": {
            "type": "LinearWarmupCosineAnnealing",
            "peak_step": 10 / args.max_epochs,
            "start_factor": 0.01,
            "end_lr": args.lr / 1000,
            "total_steps": total_steps,
        },
    }


def _callbacks(module, model, args, ckpt_dir, tag, btag):
    # Identical to batch-1/2 so cross-batch rankings stay comparable. Do not tune
    # probe settings per-exp (plan §5).
    return [
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
        # RankMe is load-bearing this batch, not decorative: exp1/exp3 both have
        # collapse regimes (tracker/batch7-analysis.md). A good probe number with a
        # collapsing RankMe is a failed run.
        spt.callbacks.RankMe(name="rankme", target="embedding", queue_length=1000,
                             target_shape=model.embed_dim),
        pl.pytorch.callbacks.ModelCheckpoint(
            dirpath=ckpt_dir, filename=f"{tag}-{btag}-{{epoch:03d}}",
            save_top_k=-1, every_n_epochs=max(args.max_epochs // 2, 1), save_last=True,
        ),
        pl.pytorch.callbacks.LearningRateMonitor(logging_interval="step"),
    ]


def run(model, args, tag: str):
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
    module = spt.Module(model=model, forward=lejepa_forward,
                        optim=build_optim(model, args, total_steps))

    trainer_kwargs = dict(
        max_epochs=args.max_epochs,
        num_sanity_val_steps=0,
        callbacks=_callbacks(module, model, args, ckpt_dir, tag, btag),
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
