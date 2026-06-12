"""Shared runner for batch-2 LeJEPA experiments on Imagenette.

Mirrors ``climb_bench/batch1/_common.py`` and adds only batch-2 wiring:
optimizer dispatch, LLRD groups, SAM/PCGrad custom steps, schedule-free/SWA
iterate hooks, and stochastic-depth scheduling.
"""

from __future__ import annotations

import argparse
import os
import sys
from functools import partial
from pathlib import Path

os.environ.setdefault("SPT_LIGHT_IMPORT", "0")

import lightning as pl
import torch
import torch.nn as nn
import torchmetrics
from lightning.pytorch.core.optimizer import LightningOptimizer

import stable_pretraining as spt
from stable_pretraining.data import transforms
from stable_pretraining.methods.lejepa import LeJEPAOutput

from _variants import DropPathScheduler, RankMeGatedSWA, ScheduleFreeModeCallback, pcgrad_combine
from _vendor.muon import Muon
from _vendor.sam import SAM
from _vendor.schedulefree import AdamWScheduleFree


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
    return out


def base_parser(description: str = "LeJEPA batch-2 experiment") -> argparse.ArgumentParser:
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
    p.add_argument("--data_local_path", default=None)
    p.add_argument("--run_name", default=None)
    p.add_argument("--wandb_entity", default="stable-ssl")
    p.add_argument("--wandb_project", default="imagenet10-batch2")
    p.add_argument("--checkpoint_dir", default=None)
    p.add_argument("--wandb_offline", action="store_true")
    p.add_argument("--no_wandb", action="store_true")

    p.add_argument("--optimizer", choices=["adamw", "muon", "schedulefree", "sam"], default="adamw")
    p.add_argument("--llrd_gamma", type=float, default=0.0, help="0 disables LLRD; e.g. 0.75 enables")
    p.add_argument("--manual_opt", action="store_true", help="internal/testing override for custom step modules")
    p.add_argument("--sam_rho", type=float, default=0.0, help="0 disables SAM")
    p.add_argument("--sam_late", action="store_true", help="apply SAM only in the last 30 percent of epochs")
    p.add_argument("--pcgrad", action="store_true", help="use PCGrad custom step for inv vs lambda*SIGReg")
    p.add_argument("--swa", action="store_true")
    p.add_argument("--swa_epoch_start", type=float, default=0.75)
    p.add_argument("--swa_lr", type=float, default=1e-5)
    p.add_argument("--swa_rank_gate", type=float, default=0.0)
    p.add_argument("--sd_schedule", choices=["none", "linear"], default="none")
    p.add_argument("--drop_path_rate", type=float, default=0.1)
    return p


def build_llrd_param_groups(model: nn.Module, args) -> list[dict] | None:
    gamma = float(getattr(args, "llrd_gamma", 0.0) or 0.0)
    if gamma <= 0:
        return None

    blocks = list(getattr(getattr(model, "backbone", None), "blocks", []))
    depth = max(1, len(blocks))
    groups: dict[tuple[float, float], list[nn.Parameter]] = {}
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        layer_id = depth
        if name.startswith("backbone.blocks."):
            try:
                layer_id = int(name.split(".")[2])
            except (IndexError, ValueError):
                layer_id = depth
        elif name.startswith(("backbone.patch_embed", "backbone.pos_embed", "backbone.cls_token")):
            layer_id = 0
        scale = gamma ** (depth - layer_id)
        wd = 0.0 if name.endswith(".bias") or "norm" in name.lower() or param.ndim == 1 else args.weight_decay
        groups.setdefault((scale, wd), []).append(param)
    return [
        {"params": params, "lr": args.lr * scale, "adamw_lr": args.lr * scale, "weight_decay": wd}
        for (scale, wd), params in groups.items()
    ]


def _adamw_params(model: nn.Module, args):
    return build_llrd_param_groups(model, args) or model.parameters()


def build_optimizer_factory(model: nn.Module, args):
    warmup_steps = max(1, int(10 / max(1, args.max_epochs) * max(1, args.max_steps if args.max_steps > 0 else args.max_epochs)))
    if args.optimizer == "adamw":
        return lambda _params: torch.optim.AdamW(
            _adamw_params(model, args), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.999)
        )
    if args.optimizer == "schedulefree":
        return lambda _params: AdamWScheduleFree(
            _adamw_params(model, args), lr=args.lr, weight_decay=args.weight_decay,
            betas=(0.9, 0.999), warmup_steps=warmup_steps,
        )
    if args.optimizer == "muon":
        return lambda _params: Muon(
            _adamw_params(model, args), lr=args.lr, adamw_lr=args.lr,
            weight_decay=args.weight_decay, momentum=0.95,
        )
    if args.optimizer == "sam":
        return lambda _params: SAM(
            _adamw_params(model, args), base_optimizer=torch.optim.AdamW,
            rho=args.sam_rho, lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.999),
        )
    raise ValueError(f"unknown optimizer {args.optimizer}")


def build_optim(model: nn.Module, args, total_steps: int) -> dict:
    scheduler = {"type": "ConstantLR", "factor": 1.0, "total_iters": total_steps} if args.optimizer == "schedulefree" else {
        "type": "LinearWarmupCosineAnnealing",
        "peak_step": 10 / args.max_epochs,
        "start_factor": 0.01,
        "end_lr": args.lr / 1000,
        "total_steps": total_steps,
    }
    optim = {"optimizer": build_optimizer_factory(model, args), "interval": "step"}
    optim["scheduler"] = scheduler
    return optim


def _as_list(x):
    if x is None:
        return []
    return list(x) if isinstance(x, (list, tuple)) else [x]


def _step_schedulers(module):
    for s in _as_list(module.lr_schedulers()):
        if s is not None:
            s.step()


class SAMModule(spt.Module):
    """Manual-optimization SAM.

    ``self.optimizers()`` returns [SSL optimizer (SAM), linear_probe optimizer].
    SAM's two-step perturbs only the SSL/model params; the probe optimizer is
    stepped normally from the same (perturbed) backward. Run in bf16-mixed so no
    GradScaler interferes with the manual SAM steps.
    """

    def __init__(self, *args, sam_late: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.sam_late = sam_late

    def _use_sam_now(self):
        if not self.sam_late:
            return True
        return self.trainer.current_epoch >= int(0.7 * self.trainer.max_epochs)

    def training_step(self, batch, batch_idx):
        batch["batch_idx"] = batch_idx
        opts = _as_list(self.optimizers())
        main, probes = opts[0], opts[1:]
        sam = main.optimizer if isinstance(main, LightningOptimizer) else main

        if not self._use_sam_now():
            # plain AdamW step (no perturbation) on the SAM base optimizer
            state = self(batch, stage="fit")
            for o in opts:
                o.zero_grad(set_to_none=True)
            self.manual_backward(state["loss"])
            sam.base_optimizer.step()
            for o in probes:
                o.step()
            _step_schedulers(self)
            for o in opts:
                o.zero_grad(set_to_none=True)
            self.log("train/sam_active", 0.0, on_step=True, on_epoch=True)
            return state

        state = self(batch, stage="fit")
        for o in opts:
            o.zero_grad(set_to_none=True)
        self.manual_backward(state["loss"])
        sam.first_step(zero_grad=False)            # perturb model weights to worst-case
        for o in opts:
            o.zero_grad(set_to_none=True)          # clear model+probe grads
        state2 = self(batch, stage="fit")
        self.manual_backward(state2["loss"])       # grads at perturbed weights (+ probe)
        sam.second_step(zero_grad=False)           # restore weights, base AdamW step on model
        for o in probes:
            o.step()
        _step_schedulers(self)
        for o in opts:
            o.zero_grad(set_to_none=True)
        self.log("train/sam_active", 1.0, on_step=True, on_epoch=True)
        return state


class PCGradModule(spt.Module):
    """Manual-optimization PCGrad on the (invariance vs lambda*SIGReg) gradients.

    Two model-only backwards give the per-task gradients; a joint backward of
    ``state["loss"]`` (which includes the detached online-probe loss) supplies the
    probe optimizer's gradients. The combined PCGrad gradient overwrites the model
    grads before stepping. Run in bf16-mixed (no GradScaler).
    """

    def training_step(self, batch, batch_idx):
        batch["batch_idx"] = batch_idx
        opts = _as_list(self.optimizers())
        main, probes = opts[0], opts[1:]
        state = self(batch, stage="fit")
        params = [p for p in self.model.parameters() if p.requires_grad]

        for o in opts:
            o.zero_grad(set_to_none=True)
        self.manual_backward(state["inv_loss"], retain_graph=True)
        grads_inv = [None if p.grad is None else p.grad.detach().clone() for p in params]
        for o in opts:
            o.zero_grad(set_to_none=True)
        self.manual_backward(self.model.lamb * state["sigreg_loss"], retain_graph=True)
        grads_sig = [None if p.grad is None else p.grad.detach().clone() for p in params]
        for o in opts:
            o.zero_grad(set_to_none=True)
        # joint backward populates the probe optimizer's grads (probe loss is
        # detached from the model, so model grads here are discarded below)
        self.manual_backward(state["loss"])

        combined, stats = pcgrad_combine(grads_inv, grads_sig)
        for p, grad in zip(params, combined):
            p.grad = grad
        main.step()
        for o in probes:
            o.step()
        _step_schedulers(self)
        for o in opts:
            o.zero_grad(set_to_none=True)
        self.log("train/pcgrad_conflict", float(stats.conflict), on_step=True, on_epoch=True)
        self.log("train/pcgrad_cosine", stats.cosine, on_step=True, on_epoch=True)
        return state


def _module_class(args):
    if getattr(args, "pcgrad", False):
        return PCGradModule
    if args.optimizer == "sam" and args.sam_rho > 0:
        return SAMModule
    return spt.Module


def _callbacks(module, model, args, ckpt_dir, tag, btag):
    callbacks = [
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
    ]
    if args.optimizer == "schedulefree":
        callbacks.append(ScheduleFreeModeCallback())
    if args.swa:
        callbacks.append(RankMeGatedSWA(args.swa_epoch_start, args.swa_lr, args.swa_rank_gate))
    if args.sd_schedule == "linear":
        callbacks.append(DropPathScheduler(args.drop_path_rate))
    return callbacks


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
    cls = _module_class(args)
    module_kwargs = {}
    if cls is SAMModule:
        module_kwargs["sam_late"] = args.sam_late
    module = cls(model=model, forward=lejepa_forward, optim=build_optim(model, args, total_steps), **module_kwargs)

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
