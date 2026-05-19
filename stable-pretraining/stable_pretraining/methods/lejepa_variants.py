"""LeJEPA research variants — 5 alternative SIGReg / invariance modules.

Each module is a drop-in replacement for SlicedEppsPulley (variants 1–4)
or a LeJEPA subclass with a modified invariance term (variant 5).

Usage in a benchmark script
----------------------------
# Variants 1–4: swap model.sigreg after construction
model = LeJEPA("vit_small_patch16_224", ...)
model.sigreg = SRHTSlicedEppsPulley(d=512)      # variant 1
model.sigreg = HyvarienSIGReg(dim=512)          # variant 2
model.sigreg = AdversarialSIGReg(dim=512)       # variant 3
model.sigreg = FMSIGReg(dim=512)                # variant 4

# Variant 5: use subclass directly
model = LeJEPAFMInv("vit_small_patch16_224", ...)
"""

from __future__ import annotations

import math
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from stable_pretraining.methods.lejepa import EppsPulley, LeJEPA


# ---------------------------------------------------------------------------
# Shared utility
# ---------------------------------------------------------------------------

class SinusoidalTimeEmbedding(nn.Module):
    """Sinusoidal positional embedding for scalar time t ∈ [0, 1]."""

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        # t: [B] — returns [B, dim]
        half = self.dim // 2
        freqs = torch.exp(
            -math.log(10000.0) * torch.arange(half, device=t.device, dtype=t.dtype) / half
        )
        args = t[:, None] * freqs[None]  # [B, half]
        return torch.cat([args.sin(), args.cos()], dim=-1)  # [B, dim]


# ---------------------------------------------------------------------------
# Variant 1: SRHT Structured Slices
# Source: Batch-3 Idea 2 (FULL SEND)
# Replace Gaussian random projections with Subsampled Randomized Hadamard
# Transform (SRHT). Same JL guarantee, lower variance than Gaussian random.
# ---------------------------------------------------------------------------

class SRHTSlicedEppsPulley(nn.Module):
    """SlicedEppsPulley with SRHT projections instead of Gaussian random.

    SRHT: A = sqrt(d/M) · Π · H · D  where
      H  = normalized Walsh-Hadamard matrix  (d_pad × d_pad)
      D  = Rademacher diagonal ±1           (sampled per step)
      Π  = uniform row subsampling to M rows (sampled per step)

    Seed is synchronized across DDP ranks (same logic as SlicedEppsPulley).

    Args:
        d: Input dimension (= projector output dim, typically 512).
        num_slices: Number of projection directions M.
        t_max: EppsPulley integration upper bound.
        n_points: EppsPulley quadrature nodes (must be odd).
    """

    def __init__(self, d: int, num_slices: int = 1024, t_max: float = 3.0, n_points: int = 17):
        super().__init__()
        self._is_ddp = torch.distributed.is_available() and torch.distributed.is_initialized()
        self.num_slices = num_slices
        self.d = d
        self.ep = EppsPulley(t_max=t_max, n_points=n_points)
        self.register_buffer("global_step", torch.zeros((), dtype=torch.long))

        # Pad d to next power of 2 and build normalized Hadamard buffer
        d_pad = 1
        while d_pad < d:
            d_pad *= 2
        self.d_pad = d_pad
        H = self._build_hadamard(d_pad)  # (d_pad, d_pad), orthonormal
        # Keep only the first d columns (full matrix when d == d_pad)
        self.register_buffer("H", H[:, :d].float())  # (d_pad, d)

    @staticmethod
    def _build_hadamard(n: int) -> torch.Tensor:
        """Build normalized Walsh-Hadamard matrix H ∈ R^(n×n), H^T H = I."""
        assert n & (n - 1) == 0, "n must be a power of 2"
        H = torch.ones(1, 1)
        while H.shape[0] < n:
            H = torch.cat([
                torch.cat([H,  H], dim=1),
                torch.cat([H, -H], dim=1),
            ], dim=0) * (1.0 / 2 ** 0.5)
        return H

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            step = self.global_step.clone()
            if self._is_ddp:
                torch.distributed.broadcast(step, src=0)

            g = torch.Generator(device=x.device).manual_seed(step.item())

            # Rademacher diagonal D ∈ {±1}^d_pad
            D = (torch.randint(0, 2, (self.d_pad,), device=x.device, generator=g) * 2 - 1).float()

            # Subsample M rows uniformly without replacement
            row_idx = torch.randperm(self.d_pad, device=x.device, generator=g)[:self.num_slices]

            # SRHT directions: H[rows] * D[:d], then normalize to unit sphere
            # (normalization is a no-op when d == d_pad since rows of H are already unit-norm)
            A = self.H[row_idx] * D[:self.d].unsqueeze(0)  # (M, d)
            norms = A.norm(p=2, dim=1, keepdim=True).clamp(min=1e-6)
            A = (A / norms).T  # (d, M) — unit-norm columns

            self.global_step.add_(1)

        proj = x @ A  # (N, M)
        return self.ep(proj).mean()


# ---------------------------------------------------------------------------
# Variant 2: Hyvärinen Score Matching
# Source: Batch-7 Idea 2 (TOY, Phase A+B)
# Replace per-slice EP test with full-d Hyvärinen ISM + Hutchinson trace.
# Zero new hyperparameters; ~10 LoC core logic.
# ---------------------------------------------------------------------------

class HyvarienSIGReg(nn.Module):
    """Full-d score matching toward N(0, I) via Hyvärinen ISM + Hutchinson.

    Loss = E[ 0.5 * ||s_θ(z) + z||² + Tr(∂s_θ/∂z) ]
    where Tr(∂s_θ/∂z) ≈ v^T (∂s_θ/∂z) v,  v ~ N(0, I)  (Hutchinson, 1990).

    At the population minimum, P_z = N(0, I).

    Convex-decoy mitigation: s_θ is an MLP initialized randomly so the
    trivial fixed point s_θ(z) = −z is not reachable in one gradient step.
    Backprop flows through z (not only s_θ), so the encoder must move.

    Args:
        dim: Embedding dimension (= projector output dim).
        hidden_dim: Hidden width of score MLP (default: 4 * dim).
    """

    def __init__(self, dim: int, hidden_dim: Optional[int] = None):
        super().__init__()
        hidden_dim = hidden_dim or 4 * dim
        self.score_net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, dim),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        # z: [N, d] — must be in the encoder's computation graph (requires_grad=True)
        s = self.score_net(z)  # [N, d]

        # Hutchinson probe vector v ~ N(0, I)
        v = torch.randn_like(z)

        # Jacobian-vector product: v^T (∂s/∂z), shape [N, d]
        # create_graph=True makes the trace term differentiable w.r.t. z and s params
        sv_dot = (s * v).sum()
        jvp = torch.autograd.grad(sv_dot, z, create_graph=True)[0]  # [N, d]

        # Hyvärinen ISM loss (equation 4, Hyvärinen JMLR 2005)
        main_term = 0.5 * (s + z).pow(2).sum(-1).mean()
        hutch_trace = (v * jvp).sum(-1).mean()
        return main_term + hutch_trace


# ---------------------------------------------------------------------------
# Variant 3: Adversarial Max-Sliced SIGReg
# Source: Batch-7 Idea 3 (TOY → FULL SEND on Phase A pass)
# Game-theoretic worst-case slicing: adversary finds the direction that
# maximises the EP statistic; encoder minimises it.
#
# Single-optimizer detach trick (no manual optimization needed):
#   enc_loss = ep(z @ u.detach())   ← encoder descends
#   adv_loss = -ep(z.detach() @ u)  ← adversary ascends (minimises negative)
#   total = enc_loss + adv_scale * adv_loss  → one backward, one optimizer
# ---------------------------------------------------------------------------

class AdversarialSIGReg(nn.Module):
    """Max-sliced adversarial SIGReg via single-optimizer detach trick.

    The returned scalar is numerically near zero (enc ≈ adv), but gradients
    are non-zero and correctly split: encoder descends, adversary ascends.
    The meaningful metric is the encoder's linear-probe accuracy, not this loss.

    Args:
        dim: Embedding dimension.
        t_max: EppsPulley integration upper bound.
        n_points: EppsPulley quadrature nodes.
        adv_scale: Weight of the adversary term (default 1.0).
    """

    def __init__(self, dim: int, t_max: float = 3.0, n_points: int = 17, adv_scale: float = 1.0):
        super().__init__()
        self.adv_scale = adv_scale
        self.ep = EppsPulley(t_max=t_max, n_points=n_points)
        hidden = 4 * dim
        # Spectral norm for Lipschitz constraint (prevents adversary divergence)
        self.slicing_head = nn.Sequential(
            nn.utils.spectral_norm(nn.Linear(dim, hidden)),
            nn.SiLU(),
            nn.utils.spectral_norm(nn.Linear(hidden, dim)),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        # Fixed anchor: mean embedding, detached (prevents trivial recursion)
        anchor = z.detach().mean(0, keepdim=True)  # [1, d]

        # Adversary output: worst-case unit direction
        u = F.normalize(self.slicing_head(anchor), dim=-1)  # [1, d]

        # Adversary path: grad flows to slicing_head, NOT to encoder (z.detach)
        adv_loss = -self.ep(z.detach() @ u.T).mean()

        # Encoder path: grad flows to encoder, NOT to slicing_head (u.detach)
        enc_loss = self.ep(z @ u.detach().T).mean()

        return enc_loss + self.adv_scale * adv_loss


# ---------------------------------------------------------------------------
# Variant 4: FM-SIGReg v2
# Source: Batch-7 Idea 7 (FULL SEND after targeted research upgrades)
# Transport-based SIGReg: learn velocity field v_ψ(z_t, t) that transports
# encoder distribution P_z toward N(0, I) along OT-displacement path.
# v2 upgrades: ExFM closed-form target (A), KL bound (B),
#              Multisample OT Hungarian coupling (C).
# ---------------------------------------------------------------------------

def _hungarian_couple(z0: torch.Tensor, z1: torch.Tensor) -> torch.Tensor:
    """Reorder z1 rows to minimize W2 distance to z0 within the batch (Upgrade C).

    Falls back to identity coupling if scipy is not available.
    """
    try:
        from scipy.optimize import linear_sum_assignment
        cost = torch.cdist(z0.float(), z1.float()).cpu().numpy()
        _, col_idx = linear_sum_assignment(cost)
        return z1[col_idx]
    except ImportError:
        return z1


class FMSIGReg(nn.Module):
    """Flow-matching SIGReg v2: transport P_z to N(0, I) via CFM.

    L_FM = E[ ||v_ψ(z_t, t) − (z_1 − z_0)||² ]
    where z_t = (1−t)·z_0 + t·z_1 + σ·ε  (OT-displacement path, σ=0.01).

    Gradient flows through target_v = z_1 − z_0 (specifically −z_0) so the
    encoder is pushed toward N(0, I). z_t is detached to avoid double-counting.

    v2 upgrades applied:
      (A) ExFM closed-form regression target = z_1 − z_0 (already standard CFM)
      (B) L_FM is a KL upper bound on KL(P_z || N(0,I)) (Lipman 2023 + arXiv:2511.05480)
      (C) Hungarian coupling: z_1 reordered to match z_0 batch-optimally

    Args:
        dim: Embedding dimension.
        t_emb_dim: Sinusoidal time embedding dimension.
        hidden: Hidden width of velocity MLP (default: 4 * dim).
        sigma: Noise level on interpolation path.
    """

    def __init__(self, dim: int, t_emb_dim: int = 64, hidden: Optional[int] = None, sigma: float = 0.01):
        super().__init__()
        hidden = hidden or 4 * dim
        self.sigma = sigma
        self.t_embed = SinusoidalTimeEmbedding(t_emb_dim)
        self.net = nn.Sequential(
            nn.Linear(dim + t_emb_dim, hidden),
            nn.SiLU(),
            nn.Linear(hidden, dim),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        B, d = z.shape
        z_0 = z  # encoder embeddings, gradient-connected

        # Fresh N(0, I) target samples
        z_1 = torch.randn(B, d, device=z.device, dtype=z.dtype)

        # Upgrade C: Hungarian coupling — minimise W2 within batch
        z_1 = _hungarian_couple(z_0.detach(), z_1)

        # OT-displacement interpolant
        t = torch.rand(B, device=z.device, dtype=z.dtype)
        eps = torch.randn_like(z_0)
        z_t = (1.0 - t[:, None]) * z_0.detach() + t[:, None] * z_1 + self.sigma * eps

        # Closed-form OT-displacement target velocity (constant in t)
        target_v = z_1 - z_0  # gradient flows through −z_0 → encoder

        # Predicted velocity (detach z_t so encoder gradient comes only from target_v)
        t_emb = self.t_embed(t)  # [B, t_emb_dim]
        pred_v = self.net(torch.cat([z_t, t_emb], dim=-1))  # [B, d]

        return (pred_v - target_v).pow(2).mean()


# ---------------------------------------------------------------------------
# Variant 5: FM-Invariance
# Source: Batch-7 Idea 1 (TOY)
# Replace per-pair MSE invariance with flow-matching distributional alignment:
# learn v_ψ(z_t, t) that transports view-1 embeddings to view-2.
# ---------------------------------------------------------------------------

class FMInvariance(nn.Module):
    """Flow-matching view alignment replacing MSE invariance.

    L_FM = E[ ||v_ψ(z_t, t) − (z_1 − z_0)||² ]
    where z_t = (1−t)·z_0 + t·z_1 + σ·ε.

    Softer than per-pair MSE: only distributional alignment required,
    not per-sample identity.

    Args:
        dim: Embedding dimension (= projector output dim).
        t_emb_dim: Sinusoidal time embedding dimension.
        sigma: Noise level on interpolation path.
    """

    def __init__(self, dim: int, t_emb_dim: int = 64, sigma: float = 0.01):
        super().__init__()
        self.sigma = sigma
        self.t_embed = SinusoidalTimeEmbedding(t_emb_dim)
        # Smaller net than FMSIGReg — view alignment needs less capacity
        hidden = 2 * dim
        self.net = nn.Sequential(
            nn.Linear(dim + t_emb_dim, hidden),
            nn.SiLU(),
            nn.Linear(hidden, dim),
        )

    def forward(self, z_0: torch.Tensor, z_1: torch.Tensor) -> torch.Tensor:
        B = z_0.shape[0]
        t = torch.rand(B, device=z_0.device, dtype=z_0.dtype)
        eps = torch.randn_like(z_0)
        z_t = (1.0 - t[:, None]) * z_0 + t[:, None] * z_1 + self.sigma * eps

        target_v = z_1 - z_0  # gradients flow to encoder via z_0 and z_1

        t_emb = self.t_embed(t)
        pred_v = self.net(torch.cat([z_t.detach(), t_emb], dim=-1))

        return (pred_v - target_v).pow(2).mean()


class LeJEPAFMInv(LeJEPA):
    """LeJEPA with flow-matching invariance replacing MSE invariance.

    All other components (SIGReg, projector, optimizer, multi-crop) unchanged.
    Override: _compute_loss swaps MSE center-alignment for FM alignment.

    Args:
        fm_sigma: Noise level for the FM interpolant (default 0.01).
        projector_dim: Must match the LeJEPA projector output dim (default 512).
        All other args forwarded to LeJEPA.
    """

    def __init__(self, *args, fm_sigma: float = 0.01, **kwargs):
        # Capture projector_dim before super().__init__ consumes it
        _proj_dim = kwargs.get("projector_dim", 512)
        super().__init__(*args, **kwargs)
        self.fm_inv = FMInvariance(dim=_proj_dim, sigma=fm_sigma)

    def _compute_loss(
        self,
        all_features: torch.Tensor,
        all_projected: torch.Tensor,
        all_predicted: torch.Tensor,
        n_global: int,
        sigreg: nn.Module,
        lamb: float,
        sigreg_target: str,
    ):
        # Centers from global-view projections (identical to base LeJEPA)
        centers = all_projected[:n_global].mean(0)  # [N, K]

        # FM invariance: flow center distribution → each predicted view distribution
        inv_loss = torch.stack([
            self.fm_inv(centers, all_predicted[i])
            for i in range(all_predicted.shape[0])
        ]).mean()

        # SIGReg: identical to base LeJEPA._compute_loss
        if sigreg_target == "proj":
            sigreg_loss = sigreg(all_projected.reshape(-1, all_projected.size(-1)))
        elif sigreg_target == "embed":
            sigreg_loss = sigreg(all_features.reshape(-1, all_features.size(-1)))
        else:
            sigreg_proj = sigreg(all_projected.reshape(-1, all_projected.size(-1)))
            sigreg_embed = sigreg(all_features.reshape(-1, all_features.size(-1)))
            sigreg_loss = 0.5 * (sigreg_proj + sigreg_embed)

        loss = inv_loss + lamb * sigreg_loss
        return loss, inv_loss, sigreg_loss
