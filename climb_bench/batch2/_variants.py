"""Batch-2 LeJEPA optimizer / architecture variants.

All mechanisms live in this batch-local file so official
``stable_pretraining.methods.lejepa_variants`` remains untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from loguru import logger

from stable_pretraining.methods import lejepa as lejepa_mod
from stable_pretraining.methods.lejepa import LeJEPA, LeJEPAOutput


def build_lejepa(
    *,
    encoder_name: str,
    lamb: float,
    n_slices: int,
    projector_dim: int,
    qk_norm: bool = False,
    **kwargs,
) -> LeJEPA:
    """Build LeJEPA, optionally passing timm's ``qk_norm`` at backbone creation."""

    if not qk_norm:
        return LeJEPA(
            encoder_name=encoder_name,
            lamb=lamb,
            n_slices=n_slices,
            n_points=17,
            projector_dim=projector_dim,
            **kwargs,
        )

    original = lejepa_mod._create_timm_backbone

    def _create_qk_backbone(encoder_name, pretrained, drop_path_rate, reg_tokens):
        import timm

        create_kwargs = {
            "pretrained": pretrained,
            "num_classes": 0,
            **({"dynamic_img_size": True} if "vit" in encoder_name else {}),
            "drop_path_rate": drop_path_rate,
            "qk_norm": True,
        }
        if reg_tokens > 0:
            create_kwargs["reg_tokens"] = reg_tokens
        return timm.create_model(encoder_name, **create_kwargs)

    lejepa_mod._create_timm_backbone = _create_qk_backbone
    try:
        return LeJEPA(
            encoder_name=encoder_name,
            lamb=lamb,
            n_slices=n_slices,
            n_points=17,
            projector_dim=projector_dim,
            **kwargs,
        )
    finally:
        lejepa_mod._create_timm_backbone = original


class ConvStem(nn.Module):
    """Stride-16 convolutional patch embed matching ViT-S token geometry."""

    def __init__(self, img_size: int = 224, in_chans: int = 3, embed_dim: int = 384):
        super().__init__()
        self.img_size = (img_size, img_size)
        self.patch_size = (16, 16)
        self.grid_size = (img_size // 16, img_size // 16)
        self.num_patches = self.grid_size[0] * self.grid_size[1]
        # ViT backbone is built with dynamic_img_size=True, whose _pos_embed
        # expects the patch embed to return NHWC (B, H, W, C) and flattens itself.
        self.flatten = False
        self.proj = nn.Sequential(
            nn.Conv2d(in_chans, embed_dim // 4, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim // 4),
            nn.GELU(),
            nn.Conv2d(embed_dim // 4, embed_dim // 2, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim // 2),
            nn.GELU(),
            nn.Conv2d(embed_dim // 2, embed_dim, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim),
            nn.GELU(),
            nn.Conv2d(embed_dim, embed_dim, 3, stride=2, padding=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.proj(x)            # B, C, H, W
        return x.permute(0, 2, 3, 1)  # B, H, W, C (timm dynamic_img_size flattens)


def apply_conv_stem(model: LeJEPA) -> LeJEPA:
    """Replace a ViT patch embed with the batch-2 conv stem."""

    backbone = model.backbone
    if not hasattr(backbone, "patch_embed"):
        raise ValueError("conv_stem requires a timm ViT-style backbone.patch_embed")
    embed_dim = int(getattr(backbone, "embed_dim", model.backbone_embed_dim))
    stem = ConvStem(embed_dim=embed_dim)
    backbone.patch_embed = stem
    expected_tokens = stem.num_patches + int(getattr(backbone, "num_prefix_tokens", 1))
    pos_embed = getattr(backbone, "pos_embed", None)
    if pos_embed is not None and pos_embed.shape[1] != expected_tokens:
        raise ValueError(
            f"conv_stem token mismatch: pos_embed has {pos_embed.shape[1]}, expected {expected_tokens}"
        )
    logger.info(
        "ConvStem installed: grid={} tokens={} embed_dim={}",
        stem.grid_size,
        stem.num_patches,
        embed_dim,
    )
    return model


class LeJEPADeepSup(LeJEPA):
    """LeJEPA with optional auxiliary losses on intermediate ViT layers."""

    def __init__(self, *args, deepsup_mu: float = 0.0, deepsup_layers: Iterable[int] = (6, 9), **kwargs):
        super().__init__(*args, **kwargs)
        self.deepsup_mu = float(deepsup_mu)
        self.deepsup_layers = tuple(int(x) for x in deepsup_layers)
        self.aux_projectors = nn.ModuleList(
            [
                nn.Linear(self.backbone_embed_dim, self.projector[0].out_features if isinstance(self.projector, nn.Sequential) else self.embed_dim)
                for _ in self.deepsup_layers
            ]
        )

    def _encode_intermediates(self, images: torch.Tensor) -> list[torch.Tensor]:
        if not hasattr(self.backbone, "get_intermediate_layers"):
            raise ValueError("deep supervision requires a timm ViT with get_intermediate_layers")
        outs = self.backbone.get_intermediate_layers(images, n=self.deepsup_layers, reshape=False, norm=True)
        feats = []
        for tokens in outs:
            feats.append(self.aggregate_tokens(self._unwrap_tokens(tokens)))
        return feats

    def forward(self, global_views=None, local_views=None, images=None) -> LeJEPAOutput:
        output = super().forward(global_views=global_views, local_views=local_views, images=images)
        if not self.training or self.deepsup_mu == 0.0:
            return output

        all_views = list(global_views) + list(local_views)
        bs = global_views[0].shape[0]
        n_views = len(all_views)
        aux_losses = []
        for layer_idx, projector in enumerate(self.aux_projectors):
            per_view = []
            for view in all_views:
                per_view.append(projector(self._encode_intermediates(view)[layer_idx]))
            all_projected = torch.stack(per_view).view(n_views, bs, -1)
            inv = (all_projected[: len(global_views)].mean(0).unsqueeze(0) - all_projected).square().mean()
            sig = self.sigreg(all_projected.reshape(-1, all_projected.size(-1)))
            aux_losses.append(inv + self.lamb * sig)
        loss = output.loss + self.deepsup_mu * torch.stack(aux_losses).mean()
        return LeJEPAOutput(loss=loss, embedding=output.embedding, inv_loss=output.inv_loss, sigreg_loss=output.sigreg_loss)


class LeJEPAPCGrad(LeJEPA):
    """Marker subclass for PCGrad. The custom Lightning step lives in ``_common``."""

    pcgrad_enabled: bool = True


@dataclass
class PCGradStats:
    conflict: bool
    cosine: float


def pcgrad_combine(grads_a: list[torch.Tensor | None], grads_b: list[torch.Tensor | None]) -> tuple[list[torch.Tensor | None], PCGradStats]:
    """Project conflicting task gradients and return the combined gradients."""

    flat_a = torch.cat([g.reshape(-1) for g in grads_a if g is not None])
    flat_b = torch.cat([g.reshape(-1) for g in grads_b if g is not None])
    dot = torch.dot(flat_a, flat_b)
    denom = flat_a.norm() * flat_b.norm() + 1e-12
    cosine = (dot / denom).item()
    conflict = dot < 0
    out = []
    if conflict:
        norm_b2 = flat_b.dot(flat_b).clamp_min(1e-12)
        norm_a2 = flat_a.dot(flat_a).clamp_min(1e-12)
    for ga, gb in zip(grads_a, grads_b):
        if ga is None and gb is None:
            out.append(None)
        elif ga is None:
            out.append(gb)
        elif gb is None:
            out.append(ga)
        elif conflict:
            out.append((ga - dot * gb / norm_b2) + (gb - dot * ga / norm_a2))
        else:
            out.append(ga + gb)
    return out, PCGradStats(conflict=bool(conflict), cosine=cosine)


class ScheduleFreeModeCallback(pl.Callback):
    """Switch schedule-free optimizers to train/eval iterates."""

    @staticmethod
    def _optimizers(trainer):
        opts = trainer.strategy._lightning_optimizers if hasattr(trainer.strategy, "_lightning_optimizers") else []
        if not opts and getattr(trainer, "optimizers", None):
            opts = trainer.optimizers
        for opt in opts:
            yield getattr(opt, "optimizer", opt)

    def on_train_epoch_start(self, trainer, pl_module):
        for opt in self._optimizers(trainer):
            if hasattr(opt, "train"):
                opt.train()
                logger.info("Schedule-free optimizer switched to train iterate")

    def on_validation_start(self, trainer, pl_module):
        for opt in self._optimizers(trainer):
            if hasattr(opt, "eval"):
                opt.eval()
                logger.info("Schedule-free optimizer switched to eval averaged iterate")

    def on_validation_end(self, trainer, pl_module):
        for opt in self._optimizers(trainer):
            if hasattr(opt, "train"):
                opt.train()


class DropPathScheduler(pl.Callback):
    """Linearly increase timm DropPath rates during training."""

    def __init__(self, max_drop_path: float = 0.1):
        self.max_drop_path = float(max_drop_path)

    def on_train_epoch_start(self, trainer, pl_module):
        max_epochs = max(1, int(trainer.max_epochs or 1) - 1)
        frac = min(1.0, float(trainer.current_epoch) / max_epochs)
        rate = self.max_drop_path * frac
        for module in pl_module.model.modules():
            if hasattr(module, "drop_prob"):
                module.drop_prob = rate
        pl_module.log("train/drop_path_rate", rate, on_step=False, on_epoch=True)


class RankMeGatedSWA(pl.Callback):
    """Self-contained tail weight-averaging (SWA).

    Lightning's built-in ``StochasticWeightAveraging`` requires exactly ONE
    optimizer / lr_scheduler, but the OnlineProbe adds a second optimizer here,
    so it raises ``MisconfigurationException``. This callback re-implements the
    essential SWA behaviour without that restriction:

    * from ``swa_epoch_start`` onward, keep a running equal-weight average of
      ``pl_module.model`` parameters + buffers (BN stats averaged across the
      window, so no separate ``update_bn`` pass is needed);
    * during validation, swap in the averaged weights so the online
      probe/kNN/RankMe reflect the SWA model, then restore;
    * at fit end, write the averaged weights into the model AND save a
      ``swa_avg.ckpt`` (paper-spec eval reads this).

    ``swa_lrs`` is accepted for API compatibility but unused (we average over the
    existing cosine tail). ``rank_gate`` reserved for a future RankMe trigger;
    for now the window is the fixed ``swa_epoch_start`` fraction.
    """

    def __init__(self, swa_epoch_start: float = 0.75, swa_lrs: float = 1e-5, rank_gate: float = 0.0):
        self.swa_epoch_start = float(swa_epoch_start)
        self.rank_gate = float(rank_gate)
        self.avg: dict | None = None
        self.n = 0
        self._backup: dict | None = None

    def _start_epoch(self, trainer):
        if self.swa_epoch_start >= 1:
            return int(self.swa_epoch_start)
        return int(self.swa_epoch_start * max(1, trainer.max_epochs))

    def on_train_epoch_end(self, trainer, pl_module):
        if trainer.current_epoch < self._start_epoch(trainer):
            return
        sd = pl_module.model.state_dict()
        if self.avg is None:
            self.avg = {k: v.detach().clone().float() for k, v in sd.items()}
            self.n = 1
        else:
            self.n += 1
            for k, v in sd.items():
                if self.avg[k].is_floating_point():
                    self.avg[k].add_((v.detach().float() - self.avg[k]) / self.n)
                else:
                    self.avg[k] = v.detach().clone()
        pl_module.log("swa/n_averaged", float(self.n), on_step=False, on_epoch=True)

    def _swap_in_avg(self, pl_module):
        cur = pl_module.model.state_dict()
        self._backup = {k: v.detach().clone() for k, v in cur.items()}
        pl_module.model.load_state_dict(
            {k: v.to(cur[k].dtype) for k, v in self.avg.items()}, strict=True
        )

    def on_validation_start(self, trainer, pl_module):
        if self.avg is not None and self._backup is None:
            self._swap_in_avg(pl_module)
            logger.info("SWA: evaluating averaged weights (n={})", self.n)

    def on_validation_end(self, trainer, pl_module):
        if self._backup is not None:
            pl_module.model.load_state_dict(self._backup, strict=True)
            self._backup = None

    def on_fit_end(self, trainer, pl_module):
        if self.avg is None:
            return
        cur = pl_module.model.state_dict()
        pl_module.model.load_state_dict(
            {k: v.to(cur[k].dtype) for k, v in self.avg.items()}, strict=True
        )
        ckpt_cb = getattr(trainer, "checkpoint_callback", None)
        dirpath = getattr(ckpt_cb, "dirpath", None) or trainer.default_root_dir
        out = Path(dirpath) / "swa_avg.ckpt"
        torch.save(
            {"state_dict": {f"model.{k}": v for k, v in pl_module.model.state_dict().items()}},
            out,
        )
        logger.info("SWA: averaged {} checkpoints -> {}", self.n, out)
