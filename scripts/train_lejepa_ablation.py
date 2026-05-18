#!/usr/bin/env python
"""Minimal LeJEPA ablation training entrypoint.

This script intentionally supports the baseline knobs needed for smoke tests
and ablation command rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import sys
import types
from typing import Any

import torch
from torch.utils.data import DataLoader


REPO_ROOT = Path(__file__).resolve().parents[1]
STABLE_PRETRAINING_ROOT = REPO_ROOT / "stable-pretraining"
MPLCONFIGDIR = Path("/tmp/lejepa_mplconfig")
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))
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
        patch_size=cfg.patch_size,
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


def _build_trainer(cfg: TrainConfig) -> pl.Trainer:
    return pl.Trainer(
        max_epochs=cfg.max_epochs,
        max_steps=cfg.max_steps,
        num_sanity_val_steps=0,
        logger=False,
        enable_checkpointing=False,
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
    trainer = _build_trainer(cfg)

    manager = spt.Manager(trainer=trainer, module=module, data=data, seed=cfg.seed)
    manager()

    final_loss = trainer.callback_metrics.get("fit/loss_step")
    if final_loss is None:
        raise RuntimeError("fit/loss_step was not logged")
    if not torch.isfinite(final_loss).item():
        raise RuntimeError(f"non-finite final loss: {final_loss.item()}")
    print(f"LeJEPA final loss: {final_loss.item():.6f}")


if __name__ == "__main__":
    main()
