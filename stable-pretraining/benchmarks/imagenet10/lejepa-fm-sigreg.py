"""LeJEPA ViT-S/T on ImageNet-10 — Variant 4: FM-SIGReg v2.

Idea: Batch-7 Idea 7 (FULL SEND after targeted research upgrades).
Flow-matching transport P_z to N(0,I) with Hungarian OT coupling.

Usage examples
--------------
python lejepa-fm-sigreg.py --backbone vit_small_patch16_224 --max_epochs 100 \\
    --data_local_path /kaggle/input/imagenet10-hf

python lejepa-fm-sigreg.py --backbone vit_tiny_patch16_224 --max_epochs 100 \\
    --data_local_path /kaggle/input/imagenet10-hf
"""

import argparse
import sys
from pathlib import Path

import lightning as pl
import torch
import torch.nn as nn
import torchmetrics

import stable_pretraining as spt
from stable_pretraining.data import transforms
from stable_pretraining.methods.lejepa import LeJEPA, LeJEPAOutput
from stable_pretraining.methods.lejepa_variants import FMSIGReg


def _backbone_tag(name: str) -> str:
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
        val_ds   = spt.data.HFDataset(str(local / "validation"), transform=val_transform)
    else:
        sys.path.append(str(Path(__file__).parent.parent))
        from utils import get_data_dir
        cache = str(get_data_dir("imagenet10"))
        train_ds = spt.data.HFDataset(
            "frgfm/imagenette", split="train",
            revision="refs/convert/parquet", cache_dir=cache, transform=train_transform,
        )
        val_ds = spt.data.HFDataset(
            "frgfm/imagenette", split="validation",
            revision="refs/convert/parquet", cache_dir=cache, transform=val_transform,
        )
    return train_ds, val_ds


def lejepa_forward(self, batch, stage):
    out = {}
    images = batch.get("image")
    if stage == "fit":
        global_views = [batch[k]["image"] for k in batch if k.startswith("global")]
        local_views  = [batch[k]["image"] for k in batch if k.startswith("local")]
        labels = next(batch[k]["label"] for k in batch if k.startswith(("global", "local")))
        output: LeJEPAOutput = self.model.forward(global_views=global_views, local_views=local_views, images=images)
        out["label"] = labels.repeat(len(global_views))
    else:
        output: LeJEPAOutput = self.model.forward(images=images)
        out["label"] = batch["label"].long()
    out["loss"] = output.loss
    out["embedding"] = output.embedding
    self.log(f"{stage}/sigreg", output.sigreg_loss, on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/inv",    output.inv_loss,    on_step=True, on_epoch=True, sync_dist=True)
    self.log(f"{stage}/loss",   output.loss,        on_step=True, on_epoch=True, sync_dist=True)
    return out


def get_args():
    p = argparse.ArgumentParser(description="LeJEPA + FM-SIGReg v2 on ImageNet-10")
    p.add_argument("--backbone",         default="vit_small_patch16_224")
    p.add_argument("--max_epochs",       type=int,   default=100)
    p.add_argument("--batch_size",       type=int,   default=128)
    p.add_argument("--num_workers",      type=int,   default=4)
    p.add_argument("--num_gpus",         type=int,   default=1)
    p.add_argument("--lr",               type=float, default=4e-4)
    p.add_argument("--weight_decay",     type=float, default=0.05)
    p.add_argument("--lamb",             type=float, default=0.02)
    p.add_argument("--proj_dim",         type=int,   default=512)
    p.add_argument("--n_slices",         type=int,   default=1024)
    p.add_argument("--global_views",     type=int,   default=2)
    p.add_argument("--all_views",        type=int,   default=8)
    p.add_argument("--precision",        default="16-mixed")
    p.add_argument("--data_local_path",  default=None)
    p.add_argument("--run_name",         default=None)
    p.add_argument("--wandb_entity",     default="stable-ssl")
    p.add_argument("--wandb_project",    default="imagenet10-methods")
    p.add_argument("--checkpoint_dir",   default=None)
    return p.parse_args()


def main():
    args = get_args()
    btag     = _backbone_tag(args.backbone)
    run_name = args.run_name or f"lejepa-fm-sigreg-{btag}-inet10"
    ckpt_dir = args.checkpoint_dir or str(Path(__file__).parent / "checkpoints" / f"lejepa-fm-sigreg-{btag}")

    train_transform = transforms.MultiViewTransform({
        **{f"global_{i}": _global_transform() for i in range(args.global_views)},
        **{f"local_{i}":  _local_transform()  for i in range(args.all_views - args.global_views)},
    })
    val_transform = transforms.Compose(
        transforms.RGB(), transforms.Resize((256, 256)), transforms.CenterCrop((224, 224)),
        transforms.ToImage(**spt.data.static.ImageNet),
    )
    train_ds, val_ds = _build_datasets(args, train_transform, val_transform)

    data = spt.data.DataModule(
        train=torch.utils.data.DataLoader(
            dataset=train_ds, batch_size=args.batch_size, num_workers=args.num_workers,
            drop_last=True, persistent_workers=args.num_workers > 0, shuffle=True,
        ),
        val=torch.utils.data.DataLoader(
            dataset=val_ds, batch_size=args.batch_size, num_workers=args.num_workers,
            persistent_workers=args.num_workers > 0,
        ),
    )

    model = LeJEPA(encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
                   n_points=17, projector_dim=args.proj_dim)
    model.sigreg = FMSIGReg(dim=args.proj_dim)

    total_steps = (len(data.train) // args.num_gpus) * args.max_epochs
    module = spt.Module(
        model=model, forward=lejepa_forward,
        optim={
            "optimizer": {"type": "AdamW", "lr": args.lr, "weight_decay": args.weight_decay, "betas": (0.9, 0.999)},
            "scheduler": {"type": "LinearWarmupCosineAnnealing", "peak_step": 10 / args.max_epochs,
                          "start_factor": 0.01, "end_lr": args.lr / 1000, "total_steps": total_steps},
            "interval": "step",
        },
    )

    trainer = pl.Trainer(
        max_epochs=args.max_epochs, num_sanity_val_steps=0,
        callbacks=[
            spt.callbacks.OnlineProbe(
                module, name="linear_probe", input="embedding", target="label",
                probe=nn.Linear(model.embed_dim, 10), loss=nn.CrossEntropyLoss(),
                metrics={"top1": torchmetrics.classification.MulticlassAccuracy(10),
                         "top5": torchmetrics.classification.MulticlassAccuracy(10, top_k=5)},
                optimizer={"type": "AdamW", "lr": 0.03, "weight_decay": 1e-6},
            ),
            spt.callbacks.OnlineKNN(name="knn_probe", input="embedding", target="label",
                                    queue_length=10000, input_dim=model.embed_dim, k=20,
                                    metrics={"top1": torchmetrics.classification.MulticlassAccuracy(10)}),
            spt.callbacks.RankMe(name="rankme", target="embedding", queue_length=1000, target_shape=model.embed_dim),
            pl.pytorch.callbacks.ModelCheckpoint(
                dirpath=ckpt_dir, filename=f"lejepa-fm-sigreg-{btag}-{{epoch:03d}}",
                save_top_k=-1, every_n_epochs=max(args.max_epochs // 2, 1), save_last=True,
            ),
            pl.pytorch.callbacks.LearningRateMonitor(logging_interval="step"),
        ],
        logger=pl.pytorch.loggers.WandbLogger(
            entity=args.wandb_entity, project=args.wandb_project, name=run_name, log_model=False,
        ),
        precision=args.precision, devices=args.num_gpus, accelerator="gpu",
        strategy="ddp_find_unused_parameters_true" if args.num_gpus > 1 else "auto",
    )
    spt.Manager(trainer=trainer, module=module, data=data)()


if __name__ == "__main__":
    main()
