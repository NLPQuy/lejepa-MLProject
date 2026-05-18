"""LeJEPA: Latent Embedding Joint-Embedding Predictive Architecture.

Self-supervised learning via multi-view invariance combined with a
sliced goodness-of-fit test (SIGReg) that pushes embeddings toward
an isotropic Gaussian.

References:
    Balestriero & LeCun. "LeJEPA: Provable and Scalable
    Self-Supervised Learning Without the Heuristics." 2025.
    https://arxiv.org/abs/2511.08544

Example::

    from stable_pretraining.methods.lejepa import LeJEPA

    model = LeJEPA("vit_small_patch16_224")

    global_images = [torch.randn(4, 3, 224, 224)] * 2
    all_images = [torch.randn(4, 3, 224, 224)] * 6
    model.train()
    output = model(global_images, all_images)
    output.loss.backward()

    model.eval()
    output = model(images=torch.randn(4, 3, 224, 224))
    features = output.embedding  # [N, D]
"""

from dataclasses import dataclass
from transformers.utils import ModelOutput
from typing import Optional

import timm
import torch
import torch.nn as nn
from torch.distributed.nn import all_reduce

from stable_pretraining import Module
from stable_pretraining.backbone import MLP, MaskedEncoder, PatchMasking


class EppsPulley(nn.Module):
    """Epps-Pulley goodness-of-fit test for univariate normality.

    Projects data onto a grid of points and computes the Epps-Pulley statistic.

    :param t_max: Integration upper bound.
    :param n_points: Number of integration points.
    """

    def __init__(self, t_max: float = 3.0, n_points: int = 17):
        super().__init__()
        assert n_points % 2 == 1

        self._is_ddp = (
            torch.distributed.is_available() and torch.distributed.is_initialized()
        )
        self.world_size = torch.distributed.get_world_size() if self._is_ddp else 1

        t = torch.linspace(0, t_max, n_points)
        dt = t_max / (n_points - 1)
        self.register_buffer("t", t)

        phi = (-0.5 * t**2).exp()
        self.register_buffer("phi", phi)

        weights = torch.full((n_points,), 2 * dt)
        weights[[0, -1]] = dt
        self.register_buffer("weights", weights * phi)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """:param x: Samples [N, S] (N samples, S slices).

        :return: Per-slice statistic [S].
        """
        N = x.size(0)
        x_t = x.unsqueeze(-1) * self.t
        cos_mean = x_t.cos().mean(0)
        sin_mean = x_t.sin().mean(0)

        if self._is_ddp:
            all_reduce(cos_mean, op=torch.distributed.ReduceOp.AVG)
            all_reduce(sin_mean, op=torch.distributed.ReduceOp.AVG)

        err = (cos_mean - self.phi).square() + sin_mean.square()
        return (err @ self.weights) * N * self.world_size


class SlicedEppsPulley(nn.Module):
    """Sliced Epps-Pulley goodness-of-fit test for multivariate normality.

    Projects data onto random 1-D directions and averages the univariate
    Epps-Pulley statistics.  A synchronised step counter seeds the random
    projections so all DDP ranks sample identical directions.

    :param num_slices: Number of random 1-D projections.
    :param t_max: EP integration upper bound.
    :param n_points: EP quadrature nodes.
    """

    def __init__(self, num_slices: int = 1024, t_max: float = 3.0, n_points: int = 17):
        super().__init__()
        self._is_ddp = (
            torch.distributed.is_available() and torch.distributed.is_initialized()
        )
        self.num_slices = num_slices
        self.ep = EppsPulley(t_max=t_max, n_points=n_points)
        self.register_buffer("global_step", torch.zeros((), dtype=torch.long))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """:param x: Embeddings [N, D].

        :return: Scalar mean EP statistic.
        """
        with torch.no_grad():
            step = self.global_step.clone()

            if self._is_ddp:
                # All ranks increment global_step in lockstep, so this
                # broadcast is redundant under normal synchronous training.
                # It is kept as a safety net against step drift from
                # uneven batches (e.g. drop_last=False).
                torch.distributed.broadcast(step, src=0)

            g = torch.Generator(device=x.device).manual_seed(step.item())
            A = torch.randn(x.size(-1), self.num_slices, device=x.device, generator=g)
            A = A / A.norm(p=2, dim=0)
            self.global_step.add_(1)

        proj = x @ A
        return self.ep(proj).mean()


def build_projector(
    in_dim: int,
    out_dim: int = 512,
    arch: str = "MLP",
    hidden_dim: int = 2048,
    norm_layer: str = "batch_norm",
) -> nn.Module:
    """Build a LeJEPA projector head.

    ``arch="MLP"`` preserves the original LeJEPA default projector as closely
    as possible: ``Linear(in_dim, out_dim)`` followed by a 3-layer BN MLP.
    """

    if arch == "Linear":
        return nn.Linear(in_dim, out_dim, bias=True)
    if arch == "MLP2":
        return MLP(
            in_channels=in_dim,
            hidden_channels=[hidden_dim, out_dim],
            norm_layer=norm_layer,
            activation_layer=nn.ReLU,
            inplace=True,
            dropout=0.0,
        )
    if arch == "MLP":
        return nn.Sequential(
            nn.Linear(in_dim, out_dim, bias=True),
            MLP(
                in_channels=out_dim,
                hidden_channels=[hidden_dim, hidden_dim, out_dim],
                norm_layer=norm_layer,
                activation_layer=nn.ReLU,
                inplace=True,
                dropout=0.0,
            ),
        )
    if arch == "MLP4":
        return MLP(
            in_channels=in_dim,
            hidden_channels=[hidden_dim, hidden_dim, hidden_dim, out_dim],
            norm_layer=norm_layer,
            activation_layer=nn.ReLU,
            inplace=True,
            dropout=0.0,
        )
    raise ValueError(
        f"Unknown projector_arch={arch!r}. Expected one of: Linear, MLP2, MLP, MLP4."
    )


def build_predictor(
    kind: str,
    dim: int,
    hidden_dim: int = 2048,
    norm_layer: str = "batch_norm",
) -> nn.Module:
    """Build an optional predictor head for the invariance path."""

    if kind == "none":
        return nn.Identity()
    if kind == "linear":
        return nn.Linear(dim, dim, bias=True)
    if kind == "mlp":
        return MLP(
            in_channels=dim,
            hidden_channels=[hidden_dim, dim],
            norm_layer=norm_layer,
            activation_layer=nn.ReLU,
            inplace=True,
            dropout=0.0,
        )
    raise ValueError(
        f"Unknown predictor={kind!r}. Expected one of: none, linear, mlp."
    )


def _create_timm_backbone(
    encoder_name: str,
    pretrained: bool,
    drop_path_rate: float,
    reg_tokens: int,
) -> nn.Module:
    """Create the timm backbone, adding register tokens only when requested."""

    if reg_tokens < 0:
        raise ValueError(f"reg_tokens must be >= 0, got {reg_tokens}")

    create_kwargs = {
        "pretrained": pretrained,
        "num_classes": 0,
        **({"dynamic_img_size": True} if "vit" in encoder_name else {}),
        "drop_path_rate": drop_path_rate,
    }
    if reg_tokens > 0:
        create_kwargs["reg_tokens"] = reg_tokens

    try:
        backbone = timm.create_model(encoder_name, **create_kwargs)
    except TypeError as exc:
        if reg_tokens > 0 and "reg_tokens" in str(exc):
            raise ValueError(
                f"timm model {encoder_name!r} does not support "
                f"reg_tokens={reg_tokens}. Choose a timm ViT/backbone with "
                "register-token support or set reg_tokens=0."
            ) from exc
        raise

    if reg_tokens > 0:
        actual_reg_tokens = getattr(backbone, "num_reg_tokens", None)
        if actual_reg_tokens != reg_tokens:
            raise ValueError(
                f"timm model {encoder_name!r} accepted reg_tokens={reg_tokens}, "
                f"but reported num_reg_tokens={actual_reg_tokens!r}. "
                "Register-token support is not confirmed for this backbone."
            )

    return backbone


@dataclass
class LeJEPAOutput(ModelOutput):
    """Output from LeJEPA forward pass.

    :ivar loss: Combined invariance + SIGReg loss (0 in eval mode).
    :ivar embedding: Backbone embeddings [V*N, D] (train) or [N, D] (eval).
    :ivar inv_loss: Invariance component.
    :ivar sigreg_loss: Epps-Pulley goodness-of-fit component.
    """

    loss: torch.Tensor = None
    embedding: torch.Tensor = None
    inv_loss: torch.Tensor = None
    sigreg_loss: torch.Tensor = None


class LeJEPA(Module):
    """LeJEPA: multi-view invariance + sliced Epps-Pulley SIGReg.

    Architecture:
        - **Backbone**: timm ViT (CLS-pooled, ``num_classes=0``)
        - **Projector**: MLP projection head
        - **Loss**: ``invariance + (λ * SIGReg)``

    Centers are computed from global-view projections only.  The invariance
    term penalises the MSE between each view's projection and the center.
    The SIGReg term is a sliced goodness-of-fit test that pushes
    projected embeddings toward an isotropic Gaussian, averaged over views.

    :param encoder_name: timm model name (e.g., ``"vit_base_patch16_224"``)
    :param projector: Optional projection head.  When ``None``, a 3-layer
        BN+ReLU MLP (``embed_dim → 2048 → 2048 → 512``) is created.
    :param n_slices: Random projection directions for the goodness-of-fit test (default: 1024)
    :param t_max: EP integration upper bound (default: 3.0)
    :param n_points: EP quadrature nodes (default: 17)
    :param lamb: SIGReg weight λ (default: 0.02)
    :param pretrained: Load pretrained timm weights
    :param projector_arch: Projector architecture when ``projector`` is ``None``.
    :param projector_dim: Output dimension of the projector.
    :param projector_hidden_dim: Hidden dimension for MLP projectors.
    :param projector_norm: Normalization layer name passed to the MLP helper.
    :param sigreg_target: Where to apply SIGReg: ``"proj"``, ``"embed"``, or ``"both"``.
    :param predictor: Predictor head used only for the invariance path:
        ``"none"``, ``"linear"``, or ``"mlp"``.
    :param predictor_hidden_dim: Hidden dimension for the MLP predictor.
    :param predictor_norm: Normalization layer name passed to the MLP predictor.
    :param reg_tokens: Number of timm ViT register tokens.  ``0`` preserves
        the default backbone creation path; positive values require timm
        backbone support.
    :param aggregator: Backbone feature aggregation mode: ``"cls"``,
        ``"mean"``, or ``"cls_mean"``. ``"cls"`` preserves the original
        pooled timm forward path.
    :param patch_mask_ratio: Fraction of patch tokens to mask during training.
        ``0.0`` preserves the original timm backbone path.
    :param patch_mask_block_size: Square block size for block masking.
    :param patch_mask_crop_ratio: Probability of crop-style masking.
    :param patch_size: Optional patch size override used only by the masked
        encoder path.

    Example::

        model = LeJEPA("vit_base_patch16_224")
        images = torch.randn(4, 3, 224, 224)

        model.train()
        output = model(
            global_views=[images, images],
            all_views=[images, images, images, images],
        )
        output.loss.backward()

        model.eval()
        output = model(images=images)
        features = output.embedding  # [4, 768]

    Example with Lightning::

        import lightning as pl
        from stable_pretraining.methods.lejepa import LeJEPA


        class LeJEPALightning(pl.LightningModule):
            def __init__(self):
                super().__init__()
                self.model = LeJEPA("vit_base_patch16_224")

            def training_step(self, batch, batch_idx):
                views = [v["image"] for v in batch["views"]]
                output = self.model(global_views=views, all_views=views)
                self.log("loss", output.loss)
                return output.loss

            def configure_optimizers(self):
                return torch.optim.AdamW(self.parameters(), lr=1e-3)
    """

    def __init__(
        self,
        encoder_name: str = "vit_base_patch16_224",
        projector: Optional[nn.Module] = None,
        n_slices: int = 1024,
        t_max: float = 3.0,
        n_points: int = 17,
        lamb: float = 0.02,
        pretrained: bool = False,
        drop_path_rate: float = 0.1,
        projector_arch: str = "MLP",
        projector_dim: int = 512,
        projector_hidden_dim: int = 2048,
        projector_norm: str = "batch_norm",
        sigreg_target: str = "proj",
        predictor: str = "none",
        predictor_hidden_dim: int = 2048,
        predictor_norm: str = "batch_norm",
        reg_tokens: int = 0,
        aggregator: str = "cls",
        patch_mask_ratio: float = 0.0,
        patch_mask_block_size: int = 1,
        patch_mask_crop_ratio: float = 0.0,
        patch_size: Optional[int] = None,
    ):
        super().__init__()

        if patch_mask_ratio < 0:
            raise ValueError(f"patch_mask_ratio must be >= 0, got {patch_mask_ratio}")
        if sigreg_target not in {"proj", "embed", "both"}:
            raise ValueError(
                "sigreg_target must be one of {'proj', 'embed', 'both'}, "
                f"got {sigreg_target!r}"
            )
        if aggregator not in {"cls", "mean", "cls_mean"}:
            raise ValueError(
                "aggregator must be one of {'cls', 'mean', 'cls_mean'}, "
                f"got {aggregator!r}"
            )

        backbone = _create_timm_backbone(
            encoder_name=encoder_name,
            pretrained=pretrained,
            drop_path_rate=drop_path_rate,
            reg_tokens=reg_tokens,
        )
        if patch_mask_ratio > 0:
            masking = PatchMasking(
                mask_ratio=patch_mask_ratio,
                block_size=patch_mask_block_size,
                crop_ratio=patch_mask_crop_ratio,
            )
            self.backbone = MaskedEncoder(
                backbone,
                masking=masking,
                patch_size=patch_size,
                dynamic_img_size=True,
            )
        else:
            self.backbone = backbone

        backbone_embed_dim = self.backbone.embed_dim
        embed_dim = (
            backbone_embed_dim * 2
            if aggregator == "cls_mean"
            else backbone_embed_dim
        )

        if projector is None:
            projector = build_projector(
                in_dim=embed_dim,
                out_dim=projector_dim,
                arch=projector_arch,
                hidden_dim=projector_hidden_dim,
                norm_layer=projector_norm,
            )

        self.projector = projector
        self.predictor = build_predictor(
            kind=predictor,
            dim=projector_dim,
            hidden_dim=predictor_hidden_dim,
            norm_layer=predictor_norm,
        )
        self.predictor_kind = predictor

        self.sigreg = SlicedEppsPulley(
            num_slices=n_slices, t_max=t_max, n_points=n_points
        )
        self.lamb = lamb
        self.embed_dim = embed_dim
        self.backbone_embed_dim = backbone_embed_dim
        self.sigreg_target = sigreg_target
        self.reg_tokens = reg_tokens
        self.aggregator = aggregator
        self.patch_mask_ratio = patch_mask_ratio
        self.patch_mask_block_size = patch_mask_block_size
        self.patch_mask_crop_ratio = patch_mask_crop_ratio
        self.patch_size = patch_size

    def _num_prefix_tokens(self) -> int:
        num_prefix_tokens = getattr(self.backbone, "num_prefix_tokens", None)
        if num_prefix_tokens is not None:
            return int(num_prefix_tokens)
        num_reg_tokens = int(getattr(self.backbone, "num_reg_tokens", 0) or 0)
        has_class_token = bool(getattr(self.backbone, "cls_token", None) is not None)
        return num_reg_tokens + int(has_class_token)

    @staticmethod
    def _unwrap_tokens(features):
        if isinstance(features, dict):
            for key in ("x", "tokens", "last_hidden_state", "features"):
                value = features.get(key)
                if isinstance(value, torch.Tensor):
                    return value
            raise ValueError(
                "backbone.forward_features returned a dict without tensor tokens"
            )
        if isinstance(features, (list, tuple)):
            for value in features:
                if isinstance(value, torch.Tensor):
                    return value
            raise ValueError(
                "backbone.forward_features returned a sequence without tensor tokens"
            )
        return features

    def aggregate_tokens(self, tokens: torch.Tensor) -> torch.Tensor:
        """Aggregate token features according to ``self.aggregator``."""

        if not isinstance(tokens, torch.Tensor):
            raise TypeError(f"expected tensor tokens, got {type(tokens).__name__}")

        if tokens.ndim == 2:
            if self.aggregator == "cls":
                return tokens
            raise ValueError(
                f"aggregator={self.aggregator!r} requires token features, but "
                "backbone.forward_features returned pooled features"
            )
        if tokens.ndim != 3:
            raise ValueError(
                "backbone.forward_features must return [batch, tokens, dim] "
                f"for aggregator={self.aggregator!r}, got shape {tuple(tokens.shape)}"
            )

        cls = tokens[:, 0]
        prefix_tokens = self._num_prefix_tokens()
        patch_tokens = tokens[:, prefix_tokens:]
        if patch_tokens.numel() == 0:
            raise ValueError(
                f"could not identify patch tokens for aggregator={self.aggregator!r}; "
                f"num_prefix_tokens={prefix_tokens}, token_count={tokens.size(1)}"
            )
        patch_mean = patch_tokens.mean(dim=1)

        if self.aggregator == "cls":
            return cls
        if self.aggregator == "mean":
            return patch_mean
        if self.aggregator == "cls_mean":
            return torch.cat([cls, patch_mean], dim=-1)
        raise ValueError(
            "aggregator must be one of {'cls', 'mean', 'cls_mean'}, "
            f"got {self.aggregator!r}"
        )

    def encode(self, images: torch.Tensor) -> torch.Tensor:
        """Encode images using the configured aggregation path."""

        if self.patch_mask_ratio > 0:
            output = self.backbone(images)
            return self.aggregate_tokens(output.encoded)
        if self.aggregator == "cls":
            return self.backbone(images)
        tokens = self._unwrap_tokens(self.backbone.forward_features(images))
        return self.aggregate_tokens(tokens)

    @staticmethod
    def _compute_loss(
        all_features: torch.Tensor,
        all_projected: torch.Tensor,
        all_predicted: torch.Tensor,
        n_global: int,
        sigreg: SlicedEppsPulley,
        lamb: float,
        sigreg_target: str,
    ):
        """Compute the LeJEPA loss.

        :param all_features: All view backbone features [V, N, D].
        :param all_projected: All view projections [V, N, K].
        :param all_predicted: All view predictor outputs [V, N, K].
        :param n_global: Number of global views.
        :param sigreg: SlicedEppsPulley module.
        :param lamb: SIGReg weight λ.
        :param sigreg_target: SIGReg target: ``proj``, ``embed``, or ``both``.
        :return: Tuple of (total_loss, inv_loss, sigreg_loss).
        """
        centers = all_projected[:n_global].mean(0)  # [N, K]
        inv_loss = (centers.unsqueeze(0) - all_predicted).square().mean()

        if sigreg_target == "proj":
            sigreg_loss = sigreg(all_projected.reshape(-1, all_projected.size(-1)))
        elif sigreg_target == "embed":
            sigreg_loss = sigreg(all_features.reshape(-1, all_features.size(-1)))
        elif sigreg_target == "both":
            sigreg_proj = sigreg(all_projected.reshape(-1, all_projected.size(-1)))
            sigreg_embed = sigreg(all_features.reshape(-1, all_features.size(-1)))
            sigreg_loss = 0.5 * (sigreg_proj + sigreg_embed)
        else:
            raise ValueError(
                "sigreg_target must be one of {'proj', 'embed', 'both'}, "
                f"got {sigreg_target!r}"
            )

        loss = inv_loss + lamb * sigreg_loss
        return loss, inv_loss, sigreg_loss

    def forward(
        self,
        global_views: Optional[list[torch.Tensor]] = None,
        local_views: Optional[list[torch.Tensor]] = None,
        images: Optional[torch.Tensor] = None,
    ) -> LeJEPAOutput:
        if self.training:
            assert global_views is not None and local_views is not None, (
                "global_views and local_views must be provided in training mode"
            )

            g_features = self.encode(torch.cat(global_views))
            l_features = self.encode(torch.cat(local_views))

            all_features = torch.cat([g_features, l_features])
            all_projected = self.projector(all_features)
            all_predicted = self.predictor(all_projected)

            bs = global_views[0].shape[0]
            n_views = len(global_views) + len(local_views)
            all_features = all_features.view(n_views, bs, -1)
            all_projected = all_projected.view(n_views, bs, -1)
            all_predicted = all_predicted.view(n_views, bs, -1)

            loss, inv_loss, sigreg_loss = self._compute_loss(
                all_features,
                all_projected,
                all_predicted,
                len(global_views),
                self.sigreg,
                self.lamb,
                self.sigreg_target,
            )

            embedding = g_features.detach()
            return LeJEPAOutput(
                loss=loss,
                embedding=embedding,
                inv_loss=inv_loss,
                sigreg_loss=sigreg_loss,
            )
        else:
            assert images is not None, "images must be provided in eval mode"
            embedding = self.encode(images)
            zero = torch.tensor(0.0, device=images.device)
            return LeJEPAOutput(
                loss=zero,
                embedding=embedding,
                inv_loss=zero,
                sigreg_loss=zero,
            )
