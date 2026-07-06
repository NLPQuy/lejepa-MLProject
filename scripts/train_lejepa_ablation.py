#!/usr/bin/env python
"""Minimal LeJEPA ablation training entrypoint.

This script intentionally supports the baseline knobs needed for smoke tests
and ablation command rendering.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import sys
import types
from typing import Any

import torch
from torch import nn
from torch.utils.data import DataLoader


REPO_ROOT = Path(__file__).resolve().parents[1]
STABLE_PRETRAINING_ROOT = REPO_ROOT / "stable-pretraining"
MPLCONFIGDIR = Path("/tmp/lejepa_mplconfig")
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))
os.environ["SPT_LIGHT_IMPORT"] = "0"
if str(STABLE_PRETRAINING_ROOT) not in sys.path:
    sys.path.insert(0, str(STABLE_PRETRAINING_ROOT))

import hydra
import lightning as pl
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf

import stable_pretraining as spt
from stable_pretraining.data import transforms
from stable_pretraining.methods.lejepa import LeJEPA


@dataclass
class TrainConfig:
    dataset_name: str = "frgfm/imagenette"
    max_epochs: int = 1
    max_steps: int = -1
    batch_size: int = 16
    num_workers: int = 0
    backbone: str = "vit_tiny_patch16_224"
    pretrained: bool = False
    resolution: int = 224
    local_resolution: int = 96
    n_views: int = 4
    n_global_views: int = 2
    lr: float = 5e-4
    weight_decay: float = 5e-2
    precision: str | int = 32
    accelerator: str = "cpu"
    devices: str | int = 1
    drop_path_rate: float = 0.0
    bstat_name: str = "epps_pulley"
    bstat_lambda: float = 0.02
    bstat_num_slices: int = 64
    bstat_t_max: float = 3.0
    bstat_n_points: int = 17
    embedding_dim: int = 512
    projector_dim: int = 512
    projector_arch: str = "MLP"
    projector_hidden_dim: int = 2048
    projector_norm: str = "batch_norm"
    sigreg_target: str = "proj"
    predictor: str = "none"
    predictor_hidden_dim: int = 2048
    predictor_norm: str = "batch_norm"
    reg_tokens: int = 0
    aggregator: str = "cls"
    teacher_student: bool = False
    multi_crop: bool = True
    patch_size: int | None = None
    patch_mask_ratio: float = 0.0
    patch_mask_block_size: int = 1
    patch_mask_crop_ratio: float = 0.0
    autostop: bool = False
    seed: int = 42
    save_checkpoints: bool = False
    results_dir: str = ""
    paper_probe_epochs: int = 100


ConfigStore.instance().store(name="train_config", node=TrainConfig)


class SyntheticImageDataset(spt.data.Dataset):
    """Deterministic synthetic image dataset for offline smoke tests."""

    def __init__(
        self,
        length: int = 64,
        image_size: int = 256,
        num_classes: int = 10,
        seed: int = 0,
        transform: Any = None,
    ) -> None:
        super().__init__(transform=transform)
        self.length = length
        self.image_size = image_size
        self.num_classes = num_classes
        self.seed = seed

    def __len__(self) -> int:
        return self.length

    @property
    def column_names(self) -> list[str]:
        return ["image", "label", "sample_idx"]

    def __getitem__(self, idx: int) -> dict[str, Any]:
        generator = torch.Generator().manual_seed(self.seed + int(idx))
        image = torch.randint(
            0,
            256,
            (1, self.image_size, self.image_size),
            dtype=torch.uint8,
            generator=generator,
        )
        sample = {
            "image": image,
            "label": int(idx) % self.num_classes,
            "sample_idx": int(idx),
        }
        return self.process_sample(sample)


def _to_plain_config(cfg: DictConfig) -> TrainConfig:
    base = OmegaConf.structured(TrainConfig)
    merged = OmegaConf.merge(base, cfg)
    return OmegaConf.to_object(merged)


def _check_config(cfg: TrainConfig) -> None:
    if cfg.n_global_views < 1:
        raise ValueError("n_global_views must be >= 1")
    if cfg.n_views <= cfg.n_global_views:
        raise ValueError("n_views must be greater than n_global_views")
    if cfg.bstat_name != "epps_pulley":
        raise ValueError("only bstat_name=epps_pulley is supported in this entrypoint")
    if cfg.bstat_n_points % 2 != 1:
        raise ValueError("bstat_n_points must be odd")


def _train_transform(cfg: TrainConfig) -> transforms.MultiViewTransform:
    view_transforms = {}
    for index in range(cfg.n_global_views):
        view_transforms[f"global_{index}"] = transforms.Compose(
            transforms.RGB(),
            transforms.RandomResizedCrop(
                (cfg.resolution, cfg.resolution), scale=(0.3, 1.0)
            ),
            transforms.ToImage(**spt.data.static.ImageNet),
        )

    n_local_views = cfg.n_views - cfg.n_global_views
    for index in range(n_local_views):
        view_transforms[f"local_{index}"] = transforms.Compose(
            transforms.RGB(),
            transforms.RandomResizedCrop(
                (cfg.local_resolution, cfg.local_resolution), scale=(0.05, 0.3)
            ),
            transforms.ToImage(**spt.data.static.ImageNet),
        )

    return transforms.MultiViewTransform(view_transforms)


def _val_transform(cfg: TrainConfig) -> transforms.Compose:
    resize = max(cfg.resolution + 32, cfg.resolution)
    return transforms.Compose(
        transforms.RGB(),
        transforms.Resize((resize, resize)),
        transforms.CenterCrop((cfg.resolution, cfg.resolution)),
        transforms.ToImage(**spt.data.static.ImageNet),
    )


def _build_dataset(name: str, split: str, transform: Any, cfg: TrainConfig):
    if name == "synthetic":
        length = max(cfg.batch_size * max(cfg.max_steps, 4), cfg.batch_size * 4)
        image_size = max(cfg.resolution, cfg.local_resolution, 128) + 32
        return SyntheticImageDataset(
            length=length,
            image_size=image_size,
            seed=cfg.seed + (0 if split == "train" else 10_000),
            transform=transform,
        )

    hf_name = "frgfm/imagenette" if name == "imagenette" else name
    hf_split = "validation" if split in {"val", "validation"} else "train"
    kwargs = {"split": hf_split, "transform": transform}
    if hf_name == "frgfm/imagenette":
        kwargs["revision"] = "refs/convert/parquet"
    return spt.data.HFDataset(hf_name, **kwargs)


def _build_data(cfg: TrainConfig) -> spt.data.DataModule:
    train_dataset = _build_dataset(cfg.dataset_name, "train", _train_transform(cfg), cfg)
    val_dataset = _build_dataset(cfg.dataset_name, "validation", _val_transform(cfg), cfg)

    return spt.data.DataModule(
        train=DataLoader(
            dataset=train_dataset,
            batch_size=cfg.batch_size,
            num_workers=cfg.num_workers,
            drop_last=True,
            shuffle=True,
        ),
        val=DataLoader(
            dataset=val_dataset,
            batch_size=cfg.batch_size,
            num_workers=cfg.num_workers,
        ),
    )


def _lejepa_forward(self, batch, stage):
    if stage == "fit":
        global_views = [
            batch[key]["image"] for key in sorted(batch) if key.startswith("global")
        ]
        local_views = [
            batch[key]["image"] for key in sorted(batch) if key.startswith("local")
        ]
        output = LeJEPA.forward(self, global_views=global_views, local_views=local_views)
        labels = batch["global_0"]["label"].long()
    else:
        output = LeJEPA.forward(self, images=batch["image"])
        labels = batch["label"].long()

    self.log(
        f"{stage}/loss",
        output.loss,
        on_step=True,
        on_epoch=True,
        sync_dist=True,
    )
    self.log(
        f"{stage}/inv_loss",
        output.inv_loss,
        on_step=True,
        on_epoch=True,
        sync_dist=True,
    )
    self.log(
        f"{stage}/sigreg_loss",
        output.sigreg_loss,
        on_step=True,
        on_epoch=True,
        sync_dist=True,
    )

    return {
        "loss": output.loss,
        "embedding": output.embedding,
        "label": labels,
    }


def _build_module(cfg: TrainConfig) -> LeJEPA:
    match = re.search(r"_patch(\d+)_", cfg.backbone)
    native_patch = int(match.group(1)) if match else None
    patch_size = cfg.patch_size
    patch_size_arg = (
        patch_size
        if patch_size and patch_size > 0 and patch_size != native_patch
        else None
    )

    module = LeJEPA(
        encoder_name=cfg.backbone,
        lamb=cfg.bstat_lambda,
        n_slices=cfg.bstat_num_slices,
        t_max=cfg.bstat_t_max,
        n_points=cfg.bstat_n_points,
        pretrained=cfg.pretrained,
        drop_path_rate=cfg.drop_path_rate,
        projector_arch=cfg.projector_arch,
        projector_dim=cfg.projector_dim,
        projector_hidden_dim=cfg.projector_hidden_dim,
        projector_norm=cfg.projector_norm,
        sigreg_target=cfg.sigreg_target,
        predictor=cfg.predictor,
        predictor_hidden_dim=cfg.predictor_hidden_dim,
        predictor_norm=cfg.predictor_norm,
        reg_tokens=cfg.reg_tokens,
        aggregator=cfg.aggregator,
        patch_mask_ratio=cfg.patch_mask_ratio,
        patch_mask_block_size=cfg.patch_mask_block_size,
        patch_mask_crop_ratio=cfg.patch_mask_crop_ratio,
        patch_size=patch_size_arg,
    )
    module.forward = types.MethodType(_lejepa_forward, module)
    module.optim = {
        "optimizer": {
            "type": "AdamW",
            "lr": cfg.lr,
            "weight_decay": cfg.weight_decay,
            "betas": (0.9, 0.999),
        },
        "scheduler": {"type": "LinearWarmupCosineAnnealing"},
        "interval": "epoch",
    }
    return module


def _run_tag(cfg: TrainConfig) -> str:
    """Unique, filesystem-safe name per (multirun) job so results don't collide."""
    try:
        from hydra.core.hydra_config import HydraConfig

        job = HydraConfig.get().job
        name = job.override_dirname or f"job{job.num}"
        if len(name) > 80:
            import hashlib

            name = f"job{job.num}_{hashlib.md5(name.encode()).hexdigest()[:8]}"
    except Exception:
        name = "single"
    return re.sub(r"[^A-Za-z0-9._=-]+", "_", name) or "single"


def _results_dir(cfg: TrainConfig) -> Path:
    root = cfg.results_dir or os.environ.get("LEJEPA_RESULTS_DIR", "ablation_results")
    out = Path(root) / _run_tag(cfg)
    out.mkdir(parents=True, exist_ok=True)
    return out


def _build_callbacks(cfg: TrainConfig, ckpt_dir: Path) -> list:
    callbacks: list = []
    if cfg.save_checkpoints:
        callbacks.append(
            pl.pytorch.callbacks.ModelCheckpoint(
                dirpath=str(ckpt_dir),
                filename="{epoch:03d}",
                save_top_k=-1,
                every_n_epochs=max(cfg.max_epochs // 2, 1),
                save_last=True,
            )
        )
    return callbacks


def _timm_vit(module: LeJEPA):
    """The raw timm ViT, unwrapping the MaskedEncoder used by the patch-masking spec."""
    return getattr(module.backbone, "vit", module.backbone)


@torch.no_grad()
def _extract_features(vit, loader, device) -> tuple[torch.Tensor, torch.Tensor]:
    """Concat CLS of the last two ViT blocks (paper-spec frozen feature)."""
    vit.eval()
    feats, labs = [], []
    for batch in loader:
        imgs = batch["image"].to(device, non_blocking=True)
        outs = vit.get_intermediate_layers(imgs, n=2, return_prefix_tokens=True, norm=True)
        cls = torch.cat([o[1][:, 0] for o in outs], dim=1)  # [B, backbone_embed_dim * 2]
        feats.append(cls.float().cpu())
        labs.append(batch["label"].long())
    return torch.cat(feats), torch.cat(labs)


def _train_paper_probe(tr_x, tr_y, va_x, va_y, device, epochs, lr=1e-3, wd=1e-6, bs=1024) -> dict:
    """Paper linear-probe: LayerNorm + Linear, AdamW, warmup + cosine. Returns best val acc."""
    dim = tr_x.shape[1]
    probe = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, 10)).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=wd)
    warmup = max(1, epochs // 10)
    sched = torch.optim.lr_scheduler.SequentialLR(
        opt,
        [
            torch.optim.lr_scheduler.LinearLR(opt, 0.01, 1.0, warmup),
            torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs - warmup),
        ],
        [warmup],
    )
    tr_x, tr_y = tr_x.to(device), tr_y.to(device)
    va_x, va_y = va_x.to(device), va_y.to(device)
    crit = nn.CrossEntropyLoss()
    n = tr_x.shape[0]
    best = {"top1": 0.0, "top5": 0.0, "epoch": -1}
    for ep in range(epochs):
        probe.train()
        perm = torch.randperm(n, device=device)
        for i in range(0, n, bs):
            idx = perm[i : i + bs]
            opt.zero_grad()
            crit(probe(tr_x[idx]), tr_y[idx]).backward()
            opt.step()
        sched.step()
        probe.eval()
        with torch.no_grad():
            logits = probe(va_x)
            top1 = (logits.argmax(1) == va_y).float().mean().item()
            top5 = (logits.topk(5, 1).indices == va_y[:, None]).any(1).float().mean().item()
        if top1 > best["top1"]:
            best = {"top1": top1, "top5": top5, "epoch": ep}
    return best


def _paper_eval(cfg: TrainConfig, module: LeJEPA) -> dict:
    """Frozen paper-spec linear probe on the trained backbone (concat CLS last-2 + LN)."""
    device = next(module.parameters()).device
    vit = _timm_vit(module)
    transform = _val_transform(cfg)

    def _loader(split: str) -> DataLoader:
        dataset = _build_dataset(cfg.dataset_name, split, transform, cfg)
        return DataLoader(dataset, batch_size=cfg.batch_size, num_workers=cfg.num_workers)

    tr_x, tr_y = _extract_features(vit, _loader("train"), device)
    va_x, va_y = _extract_features(vit, _loader("validation"), device)
    best = _train_paper_probe(tr_x, tr_y, va_x, va_y, device, cfg.paper_probe_epochs)
    return {
        "feature": "concat_cls_last2_layernorm",
        "probe": "AdamW lr1e-3 wd1e-6 cosine",
        "probe_epochs": cfg.paper_probe_epochs,
        "n_train": int(tr_x.shape[0]),
        "n_val": int(va_x.shape[0]),
        "top1": round(best["top1"], 4),
        "top5": round(best["top5"], 4),
        "best_probe_epoch": best["epoch"],
    }


def _build_trainer(cfg: TrainConfig, callbacks: list, logger) -> pl.Trainer:
    return pl.Trainer(
        max_epochs=cfg.max_epochs,
        max_steps=cfg.max_steps,
        num_sanity_val_steps=0,
        logger=logger,
        enable_checkpointing=cfg.save_checkpoints,
        callbacks=callbacks,
        accelerator=cfg.accelerator,
        devices=cfg.devices,
        precision=cfg.precision,
        enable_progress_bar=False,
    )


@hydra.main(version_base=None, config_path=None, config_name="train_config")
def main(raw_cfg: DictConfig) -> None:
    cfg = _to_plain_config(raw_cfg)
    _check_config(cfg)
    pl.seed_everything(cfg.seed, workers=True)

    data = _build_data(cfg)
    module = _build_module(cfg)

    results_dir = _results_dir(cfg)
    callbacks = _build_callbacks(cfg, results_dir / "checkpoints")
    logger = pl.pytorch.loggers.CSVLogger(save_dir=str(results_dir), name="csv_logs")
    trainer = _build_trainer(cfg, callbacks, logger)

    manager = spt.Manager(trainer=trainer, module=module, data=data, seed=cfg.seed)
    manager()

    final_loss = trainer.callback_metrics.get("fit/loss_step")
    if final_loss is None:
        raise RuntimeError("fit/loss_step was not logged")
    if not torch.isfinite(final_loss).item():
        raise RuntimeError(f"non-finite final loss: {final_loss.item()}")

    paper_eval = _paper_eval(cfg, module)
    summary = {
        "config": asdict(cfg),
        "final_loss": float(final_loss.item()),
        "paper_eval": paper_eval,
    }
    (results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"LeJEPA final loss: {final_loss.item():.6f}")
    print(f"LeJEPA PAPER-SPEC top1={paper_eval['top1']} top5={paper_eval['top5']}")
    print(f"LeJEPA results dir: {results_dir}")


if __name__ == "__main__":
    main()
