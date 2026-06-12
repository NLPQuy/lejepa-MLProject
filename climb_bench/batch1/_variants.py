"""Batch-1 safe LeJEPA variants (additive / behaviour-preserving).

Kept out of the official ``stable_pretraining.methods.lejepa_variants`` per the
batch-1 plan decision: these live in ``climb_bench/batch1/`` and only import
from the official source (``stable_pretraining.methods.lejepa``).

Implemented here (the "safe" set — each reduces to baseline when its weight/flag
is off, or is a drop-in projector swap):

- Idea 3: :class:`LeJEPACodingRate`   — adds ``beta`` * (negative coding-rate) to the loss.
- Idea 4: :class:`LeJEPAUniformity`   — adds ``gamma`` * hypersphere-uniformity to the loss.
- Idea 7: :class:`LeJEPADynTanhProj`  — replaces the projector's BatchNorm with DynTanh.

Subclasses override ``_compute_loss`` exactly like the official ``LeJEPAFMInv``.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from stable_pretraining.methods.lejepa import LeJEPA


# ---------------------------------------------------------------------------
# Loss-term primitives (pure functions, unit-testable)
# ---------------------------------------------------------------------------

def coding_rate(Z: torch.Tensor, eps: float = 0.5) -> torch.Tensor:
    """MCR2 coding rate R(Z) = 0.5 * logdet(I + (d / eps^2) * cov(Z)).

    Larger R = more volume spanned = less collapse. Computed in fp32 for the
    logdet stability (bf16/16-mixed logdet is unreliable).

    :param Z: [N, d] batch of features.
    :return: scalar coding rate.
    """
    Z = Z.float()
    n, d = Z.shape
    cov = (Z.t() @ Z) / n  # [d, d]
    scale = d / (eps ** 2)
    mat = torch.eye(d, device=Z.device, dtype=Z.dtype) + scale * cov
    sign, logabsdet = torch.linalg.slogdet(mat)
    return 0.5 * logabsdet


def uniformity_loss(Z: torch.Tensor, t: float = 2.0) -> torch.Tensor:
    """Wang & Isola (ICML 2020) hypersphere uniformity: log E[exp(-t ||zi - zj||^2)].

    Lower = more uniformly spread on the unit sphere. Operates on L2-normalized Z.

    :param Z: [N, d] batch of features.
    :return: scalar uniformity loss.
    """
    Zn = F.normalize(Z.float(), dim=-1)
    sq_pdist = torch.pdist(Zn, p=2).pow(2)
    return sq_pdist.mul(-t).exp().mean().log()


# ---------------------------------------------------------------------------
# Idea 3: Coding-rate volume term complementing SIGReg
# ---------------------------------------------------------------------------

class LeJEPACodingRate(LeJEPA):
    """LeJEPA + MCR2 coding-rate anti-collapse term.

    loss = inv + lamb * sigreg + coding_beta * (-coding_rate(Z))

    ``Z`` is the flattened projector output (same tensor SIGReg sees with
    ``sigreg_target="proj"``). ``coding_beta=0`` => identical to base LeJEPA.

    :param coding_beta: weight of the coding-rate term (default 0.0 = baseline).
    :param coding_eps: MCR2 distortion epsilon.
    """

    def __init__(self, *args, coding_beta: float = 0.0, coding_eps: float = 0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.coding_beta = coding_beta
        self.coding_eps = coding_eps

    def _compute_loss(self, all_features, all_projected, all_predicted,
                      n_global, sigreg, lamb, sigreg_target):
        loss, inv_loss, sigreg_loss = LeJEPA._compute_loss(
            all_features, all_projected, all_predicted,
            n_global, sigreg, lamb, sigreg_target,
        )
        if self.coding_beta != 0.0:
            Z = all_projected.reshape(-1, all_projected.size(-1))
            loss = loss + self.coding_beta * (-coding_rate(Z, self.coding_eps))
        return loss, inv_loss, sigreg_loss


# ---------------------------------------------------------------------------
# Idea 4: Hypersphere-uniformity term complementing SIGReg
# ---------------------------------------------------------------------------

class LeJEPAUniformity(LeJEPA):
    """LeJEPA + Wang-Isola uniformity term on projections.

    loss = inv + lamb * sigreg + uniformity_gamma * uniformity(Z)

    ``uniformity_gamma=0`` => identical to base LeJEPA.

    :param uniformity_gamma: weight of the uniformity term (default 0.0 = baseline).
    :param uniformity_t: RBF temperature in the uniformity potential.
    """

    def __init__(self, *args, uniformity_gamma: float = 0.0, uniformity_t: float = 2.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.uniformity_gamma = uniformity_gamma
        self.uniformity_t = uniformity_t

    def _compute_loss(self, all_features, all_projected, all_predicted,
                      n_global, sigreg, lamb, sigreg_target):
        loss, inv_loss, sigreg_loss = LeJEPA._compute_loss(
            all_features, all_projected, all_predicted,
            n_global, sigreg, lamb, sigreg_target,
        )
        if self.uniformity_gamma != 0.0:
            Z = all_projected.reshape(-1, all_projected.size(-1))
            loss = loss + self.uniformity_gamma * uniformity_loss(Z, self.uniformity_t)
        return loss, inv_loss, sigreg_loss


# ---------------------------------------------------------------------------
# Idea 7: Energy-preserving DynTanh normalization in the projector
# ---------------------------------------------------------------------------

class DynTanh(nn.Module):
    """Dynamic Tanh (Zhu et al., CVPR 2025): gamma * tanh(alpha * x) + beta.

    Drop-in replacement for a normalization layer; no batch statistics.
    """

    def __init__(self, dim: int, alpha_init: float = 0.5):
        super().__init__()
        self.alpha = nn.Parameter(torch.tensor(float(alpha_init)))
        self.gamma = nn.Parameter(torch.ones(dim))
        self.beta = nn.Parameter(torch.zeros(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.gamma * torch.tanh(self.alpha * x) + self.beta


def build_dyntanh_projector(in_dim: int, out_dim: int = 512,
                            hidden_dim: int = 2048, alpha_init: float = 0.5) -> nn.Module:
    """Mirror of the base ``build_projector("MLP")`` with BatchNorm -> DynTanh.

    Linear(in,out) then a 3-layer MLP (out->hidden->hidden->out) where each
    hidden block is Linear + DynTanh + ReLU (last layer has no norm/activation),
    matching the torchvision MLP layout used by the official projector.
    """
    return nn.Sequential(
        nn.Linear(in_dim, out_dim, bias=True),
        nn.Linear(out_dim, hidden_dim, bias=True), DynTanh(hidden_dim, alpha_init), nn.ReLU(inplace=True),
        nn.Linear(hidden_dim, hidden_dim, bias=True), DynTanh(hidden_dim, alpha_init), nn.ReLU(inplace=True),
        nn.Linear(hidden_dim, out_dim, bias=True),
    )


class LeJEPADynTanhProj(LeJEPA):
    """LeJEPA whose projector uses DynTanh normalization instead of BatchNorm.

    Replaces ``self.projector`` after base construction (so backbone embed_dim is
    known). Loss / SIGReg / invariance are untouched.

    :param dyntanh_alpha: initial alpha for every DynTanh layer.
    """

    def __init__(self, *args, dyntanh_alpha: float = 0.5,
                 projector_dim: int = 512, projector_hidden_dim: int = 2048, **kwargs):
        kwargs["projector_dim"] = projector_dim
        kwargs["projector_hidden_dim"] = projector_hidden_dim
        super().__init__(*args, **kwargs)
        self.projector = build_dyntanh_projector(
            in_dim=self.embed_dim, out_dim=projector_dim,
            hidden_dim=projector_hidden_dim, alpha_init=dyntanh_alpha,
        )
