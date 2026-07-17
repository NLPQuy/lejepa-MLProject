"""Batch-7 LeJEPA variants — T3 cross-domain (score matching, game theory, flow matching).

SELF-CONTAINED BY DESIGN (plan-batch-7.md §0.1).
------------------------------------------------
Nothing here imports from ``stable_pretraining.methods.lejepa_variants``. Classes
that already existed there are *copied in* and owned by this file, following the
repo's own dual-EppsPulley precedent (CLAUDE.md). The official file stays frozen
as a record of what was tried; fixes here do NOT propagate to it, and vice versa.

Importing ``LeJEPA`` / ``EppsPulley`` from ``stable_pretraining.methods.lejepa``
is intentional and unchanged from batch-1/2 — that is the model under test.

Mechanism map (plan §1):
    exp1  KLScoreSIGReg      — idea 2, REWRITTEN (see §3.1)
    exp2  AdversarialSIGReg  — idea 3, verbatim copy
    exp3  FMSIGRegA / B      — idea 7, copy + reformulation (see §3.2)
    exp4  LeJEPAFMInv        — idea 1, verbatim copy
    exp5  LeJEPAETF          — idea 5, NEW (see §3.3)
    exp7  LeJEPARLCrop       — idea 4, NEW (see §3.5)
"""

from __future__ import annotations

import math
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from stable_pretraining.methods.lejepa import LeJEPA, EppsPulley


def build_lejepa(*, encoder_name: str, lamb: float, n_slices: int, projector_dim: int, **kwargs) -> LeJEPA:
    """Stock LeJEPA. Batch-7 needs no backbone surgery (contrast: batch-2 qk_norm)."""
    return LeJEPA(
        encoder_name=encoder_name,
        lamb=lamb,
        n_slices=n_slices,
        n_points=17,
        projector_dim=projector_dim,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Shared utility
# copied from stable_pretraining/methods/lejepa_variants.py @ 7ec8f45 — verbatim
# ---------------------------------------------------------------------------

class SinusoidalTimeEmbedding(nn.Module):
    """Sinusoidal positional embedding for scalar time t in [0, 1]."""

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        half = self.dim // 2
        freqs = torch.exp(
            -math.log(10000.0) * torch.arange(half, device=t.device, dtype=t.dtype) / half
        )
        args = t[:, None] * freqs[None]
        return torch.cat([args.sin(), args.cos()], dim=-1)


# ---------------------------------------------------------------------------
# exp1 — idea 2: Hyvärinen score matching
# REWRITTEN vs stable_pretraining/methods/lejepa_variants.py::HyvarienSIGReg @ 7ec8f45.
#
# What was wrong with the original (plan §3.1):
#   It had the encoder AND the score net descend the same ISM scalar under one
#   optimizer. But ISM is a minimum over the score function ONLY, and its optimum
#   value is  -0.5 * E[||grad log p_z(z)||^2]  — MINUS the Fisher information.
#   So letting the encoder descend it pushes the encoder to MAXIMISE its own
#   Fisher information, i.e. toward a sharply-peaked (collapsed) distribution.
#   The residual parameterisation s = head(z) - z fixes the convex decoy, but the
#   decoy was never the real problem.
#
# The fix follows refs/sliced_score_matching/losses/wae.py::wae_ssm, which solves
# the identical problem (push an encoder's latent to N(0,I)) with a two-player
# split: the score net descends ISM; the encoder descends a KL surrogate.
#
#   KL(P_z || N(0,I)) = -H(P_z) + E[-log N(z;0,I)]
#   d/dphi of -H(P_z) has the same gradient as  E[s(z).detach() * z]
#   => encoder loss = 0.5*E[||z||^2] + E[s(z).detach() * z]   (up to a constant)
#
# Implemented with the single-optimizer detach trick (as AdversarialSIGReg does),
# so no second optimizer and no manual optimization are needed.
# ---------------------------------------------------------------------------

class KLScoreSIGReg(nn.Module):
    """Two-player score-matching SIGReg: encoder descends KL(P_z || N(0,I)).

    Player 1 (score net): descends the Hyvärinen ISM objective on DETACHED z,
        learning s_theta(z) ≈ grad log p_z(z).
    Player 2 (encoder): descends the KL surrogate with the score net FROZEN.

    The two gradient paths are disjoint by construction, so the returned scalar
    can be backwarded once through a single optimizer.

    Unlike the EppsPulley statistic this is a bona-fide divergence to N(0,I):
    it is 0 iff P_z = N(0,I) (up to the score net's capacity).

    Args:
        dim: Embedding dimension (= projector output dim).
        hidden_dim: Hidden width of the score MLP (default: 4 * dim).
    """

    def __init__(self, dim: int, hidden_dim: Optional[int] = None):
        super().__init__()
        hidden_dim = hidden_dim or 4 * dim
        self.score_net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, dim),
        )

    def _score(self, z: torch.Tensor) -> torch.Tensor:
        # Residual parameterisation: at P_z = N(0,I) the true score is -z, so the
        # net only has to learn the DEVIATION from Gaussianity, not -z itself.
        return self.score_net(z) - z

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        # --- Player 1: score net descends ISM on detached z ---------------
        z_d = z.detach().requires_grad_(True)
        s_d = self._score(z_d)
        v = torch.randn_like(z_d)
        jvp = torch.autograd.grad((s_d * v).sum(), z_d, create_graph=True)[0]
        # Hyvärinen ISM (JMLR 2005 eq. 4) with Hutchinson trace (1990)
        ism = 0.5 * s_d.pow(2).sum(-1).mean() + (v * jvp).sum(-1).mean()

        # --- Player 2: encoder descends KL(P_z || N(0,I)), score frozen ---
        s = self._score(z).detach()
        kl = 0.5 * z.pow(2).sum(-1).mean() + (s * z).sum(-1).mean()

        return ism + kl


# ---------------------------------------------------------------------------
# exp2 — idea 3: Adversarial max-sliced SIGReg
# copied from stable_pretraining/methods/lejepa_variants.py @ 7ec8f45 — VERBATIM.
# Judged sound (plan §0.1). Only deviation from spec is the lr ratio, which is
# handled in _common.py via a param-group split (--adv_lr_mult), not here.
# ---------------------------------------------------------------------------

class AdversarialSIGReg(nn.Module):
    """Max-sliced adversarial SIGReg via single-optimizer detach trick.

    The returned scalar is numerically near zero (enc ≈ adv), but gradients
    are non-zero and correctly split: encoder descends, adversary ascends.
    The meaningful metric is the encoder's linear-probe accuracy, not this loss.

    Anchor: EMA of past batch means stabilises the adversary input and breaks the
    trivial fixed-point where g_phi depends on the embeddings it is evaluating.

    Regularisation: spectral norm on all layers + WGAN-GP gradient penalty.
    """

    def __init__(
        self,
        dim: int,
        t_max: float = 3.0,
        n_points: int = 17,
        adv_scale: float = 1.0,
        lambda_gp: float = 10.0,
        anchor_decay: float = 0.99,
    ):
        super().__init__()
        self.adv_scale = adv_scale
        self.lambda_gp = lambda_gp
        self.anchor_decay = anchor_decay
        self.ep = EppsPulley(t_max=t_max, n_points=n_points)
        hidden = 4 * dim
        self.slicing_head = nn.Sequential(
            nn.utils.spectral_norm(nn.Linear(dim, hidden)),
            nn.SiLU(),
            nn.utils.spectral_norm(nn.Linear(hidden, dim)),
        )
        self.register_buffer("anchor_ema", torch.zeros(1, dim))
        self.register_buffer("anchor_initialized", torch.zeros((), dtype=torch.bool))

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        batch_mean = z.detach().mean(0, keepdim=True)
        if not self.anchor_initialized.item():
            self.anchor_ema.copy_(batch_mean)
            self.anchor_initialized.fill_(True)
        else:
            self.anchor_ema.lerp_(batch_mean, 1.0 - self.anchor_decay)
        anchor = self.anchor_ema.clone()

        u = F.normalize(self.slicing_head(anchor), dim=-1)

        adv_loss = -self.ep(z.detach() @ u.T).mean()
        enc_loss = self.ep(z @ u.detach().T).mean()

        anchor_gp = anchor.detach().requires_grad_(True)
        u_gp = F.normalize(self.slicing_head(anchor_gp), dim=-1)
        grad = torch.autograd.grad(u_gp.sum(), anchor_gp, create_graph=True)[0]
        gp_loss = self.lambda_gp * (grad.norm(p=2, dim=-1) - 1.0).pow(2).mean()

        return enc_loss + self.adv_scale * adv_loss + gp_loss


# ---------------------------------------------------------------------------
# exp3 — idea 7: FM-SIGReg
# Form A copied from lejepa_variants.py::FMSIGReg @ 7ec8f45 (verbatim logic).
# Form B is NEW (plan §3.2) — the two-player reformulation.
#
# Why two forms: form A lets the encoder and the velocity net descend the same
# CFM loss. At the velocity optimum that loss is the conditional variance
# E[Var(z1-z0 | z_t)]. If the encoder collapses P_z -> delta_0 then z_t = t*z1 + sigma*eps,
# so z1 ~= z_t/t is fully determined by z_t and the conditional variance -> 0.
# COLLAPSE IS THE GLOBAL MINIMUM of form A. Phase 0 tests exactly this.
# ---------------------------------------------------------------------------

def _hungarian_couple(z0: torch.Tensor, z1: torch.Tensor) -> torch.Tensor:
    """Reorder z1 rows to minimize W2 distance to z0 within the batch.

    Returns (z1_reordered, ok) so callers can log whether the scipy path was
    taken — a silent identity fallback means upgrade (C) is OFF and the arm is
    not testing what it claims (plan §7).
    """
    try:
        from scipy.optimize import linear_sum_assignment
        cost = torch.cdist(z0.float(), z1.float()).cpu().numpy()
        _, col_idx = linear_sum_assignment(cost)
        return z1[col_idx], True
    except ImportError:
        return z1, False


def _interpolate(z0: torch.Tensor, z1: torch.Tensor, t: torch.Tensor, sigma: float, path: str):
    """Return (z_t, dalpha, dsigma) for the chosen interpolant.

    path="ot": z_t = (1-t) z0 + t z1        — OT-displacement (Lipman ICLR 2023)
    path="vp": z_t = cos(pi t/2) z0 + sin(pi t/2) z1 — variance-preserving.

    The "vp" path exists because under "ot", z0 ~ N(0,I) gives
    z_t ~ N(0, ((1-t)^2 + t^2) I) != N(0,I): the target is a fixed point only at
    t in {0,1}, which may bias the encoder toward a shrunken variance (plan §3.2).
    Under "vp", z0 ~ N(0,I) => z_t ~ N(0,I) for EVERY t.
    """
    tt = t[:, None]
    eps = torch.randn_like(z0)
    if path == "ot":
        a, b = (1.0 - tt), tt
        da, db = -1.0, 1.0
    elif path == "vp":
        a, b = torch.cos(math.pi * tt / 2), torch.sin(math.pi * tt / 2)
        da = -(math.pi / 2) * torch.sin(math.pi * tt / 2)
        db = (math.pi / 2) * torch.cos(math.pi * tt / 2)
    else:
        raise ValueError(f"unknown fm path {path!r}")
    z_t = a * z0 + b * z1 + sigma * eps
    return z_t, a, b, da, db


class FMSIGRegA(nn.Module):
    """FM-SIGReg, AS-WRITTEN (joint minimization). The addendum's actual spec.

    Copied from lejepa_variants.py::FMSIGReg @ 7ec8f45, with (i) the hungarian
    helper returning an ok-flag and (ii) `--fm_path` support. Logic otherwise
    unchanged, deliberately: this is the arm under test, including its predicted
    collapse attractor.
    """

    def __init__(self, dim: int, t_emb_dim: int = 64, hidden: Optional[int] = None,
                 sigma: float = 0.01, path: str = "ot"):
        super().__init__()
        hidden = hidden or 4 * dim
        self.sigma = sigma
        self.path = path
        self.t_embed = SinusoidalTimeEmbedding(t_emb_dim)
        self.net = nn.Sequential(
            nn.Linear(dim + t_emb_dim, hidden),
            nn.SiLU(),
            nn.Linear(hidden, dim),
        )
        self.coupling_ok = None

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        B, d = z.shape
        z_0 = z
        z_1 = torch.randn(B, d, device=z.device, dtype=z.dtype)
        z_1, self.coupling_ok = _hungarian_couple(z_0.detach(), z_1)

        t = torch.rand(B, device=z.device, dtype=z.dtype).clamp(min=0.05)
        z_t, *_ = _interpolate(z_0.detach(), z_1, t, self.sigma, self.path)

        # ExFM denoised target; gradient reaches the encoder through -z_0
        target_v = (z_t.detach() - z_0) / t[:, None]
        t_emb = self.t_embed(t)
        pred_v = self.net(torch.cat([z_t, t_emb], dim=-1))
        return (pred_v - target_v).pow(2).mean()


class FMSIGRegB(nn.Module):
    """FM-SIGReg, TWO-PLAYER reformulation (NEW — plan §3.2).

    Player 1 (velocity net): descends the standard CFM regression with the
        encoder DETACHED. It only learns the marginal velocity of the current P_z.
    Player 2 (encoder): descends the same KL surrogate as KLScoreSIGReg, but with
        the score derived from the velocity field instead of a score net — giving
        the "time-averaged / multi-scale" smoothing that idea 7 claims as its
        headline advantage over single-scale score matching.

    Velocity -> score identity used (path="ot"), for z_t = (1-t) z0 + t z1,
    z1 ~ N(0,I):
        E[z1 | z_t] = (1-t) * v(z_t, t) + z_t
        s_t(z_t)    = -E[z1 | z_t] / t

    VERIFIED numerically (Phase 0 unit test, 2026-07-17). Against a Gaussian with
    analytic score, the recovered score matches with scale-vs-analytic 1.001 at
    t=0.5 and 0.996 at t=0.9 (rel_rmse 0.090 and 0.009). refs/flow_matching has no
    velocity<->score conversion to check against (grep -r score over the package
    returns nothing), so this unit test IS the verification — keep it.

    THE t BAND IS THE WHOLE BALLGAME. The identity divides by t, so it amplifies the
    velocity net's irreducible error by 1/t:
        t=0.1 -> rel_rmse 1.316  (estimator is pure noise; an early version of this
                                  class used t_eval=0.1 and diverged in Phase 0)
        t=0.5 -> rel_rmse 0.090
    But large t is not free either: p_t -> N(0,I) as t -> 1 regardless of P_z, so the
    score stops carrying information about the encoder. Small t = signal but no
    precision; large t = precision but no signal.

    Resolution: average the KL surrogate over a BAND t ~ U(t_lo, t_hi) rather than at
    one t. This is exactly the "time-averaged, visits all scales" property the idea
    claims as its headline advantage over single-scale score matching (batch-7-idea7
    §Why expected to improve, motivation 1) — so the fix is the mechanism, not a patch.

    Args:
        t_lo, t_hi: KL-surrogate averaging band. Defaults from the Phase-0 sweep.
    """

    def __init__(self, dim: int, t_emb_dim: int = 64, hidden: Optional[int] = None,
                 sigma: float = 0.01, path: str = "ot", t_lo: float = 0.3, t_hi: float = 0.7):
        super().__init__()
        hidden = hidden or 4 * dim
        self.sigma = sigma
        self.path = path
        self.t_lo, self.t_hi = t_lo, t_hi
        self.t_embed = SinusoidalTimeEmbedding(t_emb_dim)
        self.net = nn.Sequential(
            nn.Linear(dim + t_emb_dim, hidden),
            nn.SiLU(),
            nn.Linear(hidden, dim),
        )
        self.coupling_ok = None

    def _velocity(self, z_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat([z_t, self.t_embed(t)], dim=-1))

    def _score_from_velocity(self, z_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        v = self._velocity(z_t, t)
        tt = t[:, None]
        if self.path == "ot":
            e_z1 = (1.0 - tt) * v + z_t
            return -e_z1 / tt.clamp(min=1e-3)
        # vp: z_t = cos(pi t/2) z0 + sin(pi t/2) z1 ; v = da*z0 + db*z1
        a = torch.cos(math.pi * tt / 2)
        b = torch.sin(math.pi * tt / 2)
        da = -(math.pi / 2) * b
        db = (math.pi / 2) * a
        # solve {z_t = a z0 + b z1 ; v = da z0 + db z1} for E[z1|z_t]
        det = (a * db - b * da).clamp(min=1e-6)  # = (pi/2)(a^2 + b^2) = pi/2
        e_z1 = (a * v - da * z_t) / det
        return -e_z1 / b.clamp(min=1e-3)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        B, d = z.shape

        # --- Player 1: velocity net descends CFM on a DETACHED encoder -----
        z_0 = z.detach()
        z_1 = torch.randn(B, d, device=z.device, dtype=z.dtype)
        z_1, self.coupling_ok = _hungarian_couple(z_0, z_1)
        t = torch.rand(B, device=z.device, dtype=z.dtype).clamp(min=0.05, max=0.95)
        z_t, a, b, da, db = _interpolate(z_0, z_1, t, self.sigma, self.path)
        target_v = da * z_0 + db * z_1
        cfm = (self._velocity(z_t.detach(), t) - target_v).pow(2).mean()

        # --- Player 2: encoder descends KL(P_z || N(0,I)) with score frozen -
        # t averaged over a band (see class docstring): a single small t makes the
        # 1/t-amplified score estimate pure noise and the run diverges.
        t_e = torch.empty(B, device=z.device, dtype=z.dtype).uniform_(self.t_lo, self.t_hi)
        z_te, *_ = _interpolate(z.detach(), torch.randn_like(z), t_e, self.sigma, self.path)
        s = self._score_from_velocity(z_te.detach(), t_e).detach()
        kl = 0.5 * z.pow(2).sum(-1).mean() + (s * z).sum(-1).mean()

        return cfm + kl


# ---------------------------------------------------------------------------
# exp4 — idea 1: FM-invariance
# copied from stable_pretraining/methods/lejepa_variants.py @ 7ec8f45 — VERBATIM.
# Judged sound (plan §0.1): this one replaces the INVARIANCE term, where joint
# minimization is legitimate — both z_0 and z_1 are encoder outputs and the
# degenerate "collapse everything" solution is exactly what SIGReg prevents.
# ---------------------------------------------------------------------------

class FMInvariance(nn.Module):
    """Flow-matching view alignment replacing MSE invariance."""

    def __init__(self, dim: int, t_emb_dim: int = 64, sigma: float = 0.01):
        super().__init__()
        self.sigma = sigma
        self.t_embed = SinusoidalTimeEmbedding(t_emb_dim)
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
        target_v = z_1 - z_0
        t_emb = self.t_embed(t)
        pred_v = self.net(torch.cat([z_t.detach(), t_emb], dim=-1))
        return (pred_v - target_v).pow(2).mean()


class LeJEPAFMInv(LeJEPA):
    """LeJEPA with flow-matching invariance replacing MSE invariance."""

    def __init__(self, *args, fm_sigma: float = 0.01, **kwargs):
        _proj_dim = kwargs.get("projector_dim", 512)
        super().__init__(*args, **kwargs)
        self.fm_inv = FMInvariance(dim=_proj_dim, sigma=fm_sigma)

    def _compute_loss(self, all_features, all_projected, all_predicted,
                      n_global, sigreg, lamb, sigreg_target):
        centers = all_projected[:n_global].mean(0)

        inv_loss = torch.stack([
            self.fm_inv(centers, all_predicted[i])
            for i in range(all_predicted.shape[0])
        ]).mean()

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


# ---------------------------------------------------------------------------
# exp5 — idea 5: Neural-collapse simplex-ETF prototypes
#
# Divergence from the ideation spec, deliberate (plan §3.3): idea 5 proposes
# LEARNABLE prototypes plus an `L_ETF` penalty pulling their pairwise cosines to
# -1/(K-1), which adds two weights (alpha, beta) and a K sweep. But the simplex ETF
# is a CLOSED-FORM geometry — there is nothing to learn. refs/Neural-Collapse
# (models/resnet.py:213) constructs it exactly and freezes it. Doing the same here
# deletes L_ETF, deletes alpha, and leaves one term and one weight.
#
# It also sharpens the falsification: with the target geometry fixed and exact,
# "did the embedding adopt it" is measured directly (refs/Neural-Collapse
# validate_NC.py:123::compute_ETF) with no confound from prototypes that drifted.
#
# Anti-collapse mitigations are taken from refs/swav/main_swav.py rather than
# reinvented: balanced Sinkhorn assignment (--sinkhorn_eps 0.05, 3 iters) and a
# warmup before the term engages (SwAV: --freeze_prototypes_niters 313).
#
# Prior-art gate (plan §3.3, run 2026-07-17): searched "Cramér-Wold neural collapse
# simplex ETF" / "isotropic Gaussian embedding implies simplex ETF class means".
# No equivalence theorem exists, and none should: SIGReg constrains the MARGINAL
# law of all samples, while ETF is a statement about CLASS-CONDITIONAL means. They
# are logically independent — P_z = N(0,I) holds perfectly with every class mean
# stacked at the origin (probe at chance). The premise survives.
# ---------------------------------------------------------------------------

def build_simplex_etf(K: int, d: int) -> torch.Tensor:
    """Exact simplex ETF: K unit vectors in R^d with all pairwise cosines -1/(K-1).

    Construction from refs/Neural-Collapse/models/resnet.py:213. Requires K <= d+1.
    Row i of (I - (1/K)11^T) is e_i - (1/K)1, giving <r_i,r_j> = -1/K and
    ||r_i||^2 = (K-1)/K, hence cos = -1/(K-1) exactly.
    """
    assert K <= d + 1, f"a simplex ETF of {K} vectors needs d >= {K - 1}, got d={d}"
    w = math.sqrt(K / (K - 1)) * (torch.eye(K) - torch.ones(K, K) / K)
    w = w / torch.sqrt((1.0 / K) * w.norm(p="fro") ** 2)
    m = w @ torch.eye(K, d)          # embed R^K into the first K coords of R^d
    return F.normalize(m, dim=-1)    # row-normalise; preserves the ETF cosines


@torch.no_grad()
def sinkhorn(scores: torch.Tensor, eps: float = 0.05, iters: int = 3) -> torch.Tensor:
    """Balanced soft assignment. Single-GPU port of refs/swav distributed_sinkhorn.

    Without this the assignment collapses onto one prototype (SwAV's documented
    failure mode). Returns [B, K] rows summing to 1.
    """
    Q = torch.exp(scores / eps).T          # [K, B]
    Q = Q / Q.sum()
    K, B = Q.shape
    for _ in range(iters):
        Q = Q / Q.sum(dim=1, keepdim=True) / K
        Q = Q / Q.sum(dim=0, keepdim=True) / B
    return (Q * B).T


class LeJEPAETF(LeJEPA):
    """LeJEPA + a frozen simplex-ETF prototype bank on the projections.

    Auxiliary: L_cluster = -E_i[ sum_k q_ik * cos(z_i, mu_k) ], q = balanced Sinkhorn
    assignment (detached), mu = the FIXED exact ETF. Applied to projections, matching
    SwAV's convention and SIGReg's own target.

    Off-switch: etf_w=0 => bit-for-bit baseline.

    Args:
        etf_w: auxiliary weight. 0 disables (exact baseline).
        etf_k: number of prototypes (idea 5 suggests 20 = 2x Imagenette's classes).
        etf_warmup_steps: steps before the term engages (cf. SwAV freeze_prototypes).
        sinkhorn_eps: Sinkhorn temperature.
    """

    def __init__(self, *args, etf_w: float = 0.0, etf_k: int = 20,
                 etf_warmup_steps: int = 0, sinkhorn_eps: float = 0.05, **kwargs):
        _proj_dim = kwargs.get("projector_dim", 512)
        super().__init__(*args, **kwargs)
        self.etf_w = etf_w
        self.etf_warmup_steps = etf_warmup_steps
        self.sinkhorn_eps = sinkhorn_eps
        # Fixed, non-learnable: buffer not Parameter, so it never reaches the optimizer.
        self.register_buffer("prototypes", build_simplex_etf(etf_k, _proj_dim))
        self.register_buffer("_etf_step", torch.zeros((), dtype=torch.long))
        self.last_etf = {}

    def _compute_loss(self, all_features, all_projected, all_predicted,
                      n_global, sigreg, lamb, sigreg_target):
        loss, inv_loss, sigreg_loss = LeJEPA._compute_loss(
            all_features, all_projected, all_predicted, n_global, sigreg, lamb, sigreg_target
        )
        if self.etf_w == 0.0:
            return loss, inv_loss, sigreg_loss

        self._etf_step += 1
        if self._etf_step.item() < self.etf_warmup_steps:
            return loss, inv_loss, sigreg_loss

        z = F.normalize(all_projected.reshape(-1, all_projected.size(-1)), dim=-1)
        scores = z @ self.prototypes.T                      # [N, K] cosines
        q = sinkhorn(scores.detach().float(), self.sinkhorn_eps).to(scores.dtype)
        l_cluster = -(q * scores).sum(-1).mean()

        # Assignment entropy: flat => prototypes unused; spiked => cluster collapse.
        usage = q.mean(0)
        self.last_etf = {
            "cluster": l_cluster.detach(),
            "usage_entropy": -(usage * usage.clamp_min(1e-8).log()).sum().detach(),
        }
        return loss + self.etf_w * l_cluster, inv_loss, sigreg_loss


# ---------------------------------------------------------------------------
# exp7 — idea 4: RL-learned augmentation policy (REINFORCE on crop parameters)
#
# Two spec issues found while implementing (plan §3.5 + below):
#
# (1) ARCHITECTURE. The idea files this under "data/transform", but the policy is a
#     GPU net conditioned on the image, and transforms run in CPU dataloader workers.
#     A per-sample GPU call from a worker is not viable. So the policy crops ON GPU
#     inside forward, using global_views[0] (224px) as the source and F.grid_sample
#     to produce local-sized crops. Semantics shift slightly but honestly: the policy
#     chooses "which sub-region of this global view a local crop should look at",
#     rather than re-cropping the original image.
#
# (2) THE REWARD SIGN IS SELF-CONTRADICTORY IN THE SPEC. batch-7.md §Idea 4
#     implementation step 3 says
#         r_i = L_invariance_random_baseline - L_invariance(crop_i)
#     which rewards crops with LOWER invariance loss, i.e. EASY views. But §Why
#     expected to improve says the policy should shift "toward 'hard' views — those
#     with the highest per-image invariance loss", and cites arXiv:2310.03940
#     (Hard Views) as the supporting evidence. The formula and the rationale have
#     opposite signs. --rl_reward exposes both; default 'hard' follows the rationale
#     and the cited literature, not the formula. Resolve at vetting.
# ---------------------------------------------------------------------------

class CropPolicy(nn.Module):
    """Gaussian policy over (scale, cx, cy) per crop, conditioned on the source view.

    Sampling is REINFORCE-style: draw u ~ N(mu, sigma) WITHOUT reparameterisation,
    squash u into valid crop geometry, and score with log_prob(u). The squash is
    deterministic, so the policy gradient is unaffected by it.
    """

    def __init__(self, n_crops: int = 4, hidden: int = 64,
                 scale_min: float = 0.05, scale_max: float = 0.4):
        super().__init__()
        self.n_crops, self.scale_min, self.scale_max = n_crops, scale_min, scale_max
        self.net = nn.Sequential(
            nn.Conv2d(3, 16, 3, 2, 1), nn.ReLU(inplace=True),
            nn.Conv2d(16, 32, 3, 2, 1), nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
            nn.Linear(32, hidden), nn.ReLU(inplace=True),
            nn.Linear(hidden, n_crops * 3 * 2),
        )
        # Zero-init the head so mu=0 and the per-sample log_std offset is 0 at init:
        # the policy starts image-INDEPENDENT and broad (sigma=1 pre-squash), which is
        # the closest achievable analogue of "starts neutral". NB a Gaussian policy
        # cannot exactly reproduce RandomResizedCrop's law, so the honest off-switch
        # is the --rl_crops flag (absent => stock LeJEPA), not the init.
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)
        self.base_log_std = nn.Parameter(torch.zeros(3))

    def sample(self, src: torch.Tensor, out_size: int):
        B = src.shape[0]
        x = F.interpolate(src, size=(32, 32), mode="bilinear", align_corners=False)
        raw = self.net(x).view(B, self.n_crops, 3, 2)
        mu = raw[..., 0]
        log_std = (raw[..., 1] + self.base_log_std).clamp(-3.0, 1.0)
        dist = torch.distributions.Normal(mu, log_std.exp())

        u = dist.sample()                                   # no grad — REINFORCE
        log_prob = dist.log_prob(u).sum(-1)                 # [B, n_crops]
        entropy = dist.entropy().sum(-1).mean()

        s = self.scale_min + (self.scale_max - self.scale_min) * torch.sigmoid(u[..., 0])
        cx = torch.tanh(u[..., 1]) * (1.0 - s)              # keep the window in-frame
        cy = torch.tanh(u[..., 2]) * (1.0 - s)

        crops = []
        for k in range(self.n_crops):
            theta = torch.zeros(B, 2, 3, device=src.device, dtype=src.dtype)
            theta[:, 0, 0] = s[:, k]
            theta[:, 1, 1] = s[:, k]
            theta[:, 0, 2] = cx[:, k]
            theta[:, 1, 2] = cy[:, k]
            grid = F.affine_grid(theta, (B, 3, out_size, out_size), align_corners=False)
            crops.append(F.grid_sample(src, grid, align_corners=False))
        return crops, log_prob, entropy


class LeJEPARLCrop(LeJEPA):
    """LeJEPA whose local views are partly proposed by a REINFORCE crop policy.

    View order into _compute_loss is [globals | random locals | policy crops], so the
    random locals are an in-batch control for the policy crops at every step — the
    reward needs no separate control forward.

    Guards (plan §3.5, non-negotiable — logged as fit/rl_*):
      * entropy must DECREASE from its uniform-prior value. Flat => not learning.
      * mean reward must stay positive and rise. ~0 => reward too noisy, the idea
        reduces to baseline.

    Off-switch: rl_w=0 AND no policy crops appended => exact baseline.

    Args:
        rl_n_crops: policy-proposed crops per step (idea 4: 4 of 6 locals).
        rl_w: REINFORCE weight. 0 disables the policy update (crops stay random-ish).
        rl_entropy_beta: entropy bonus, guards against a single-mode policy.
        rl_reward: 'hard' (rationale + arXiv:2310.03940) or 'easy' (the spec formula).
        rl_warmup_steps: steps before the policy update engages.
    """

    def __init__(self, *args, rl_n_crops: int = 4, rl_w: float = 1.0,
                 rl_entropy_beta: float = 0.01, rl_reward: str = "hard",
                 rl_warmup_steps: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.policy = CropPolicy(n_crops=rl_n_crops)
        self.rl_w = rl_w
        self.rl_entropy_beta = rl_entropy_beta
        self.rl_reward = rl_reward
        self.rl_warmup_steps = rl_warmup_steps
        self.register_buffer("_rl_step", torch.zeros((), dtype=torch.long))
        self._stash = None
        self.last_rl = {}

    def forward(self, global_views=None, local_views=None, images=None):
        if self.training and local_views:
            crops, log_prob, entropy = self.policy.sample(
                global_views[0], out_size=local_views[0].shape[-1]
            )
            self._stash = (log_prob, entropy, len(local_views))
            local_views = list(local_views) + crops
        else:
            self._stash = None
        return super().forward(global_views=global_views, local_views=local_views,
                               images=images)

    def _compute_loss(self, all_features, all_projected, all_predicted,
                      n_global, sigreg, lamb, sigreg_target):
        loss, inv_loss, sigreg_loss = LeJEPA._compute_loss(
            all_features, all_projected, all_predicted, n_global, sigreg, lamb, sigreg_target
        )
        if self._stash is None:
            return loss, inv_loss, sigreg_loss
        log_prob, entropy, n_random_local = self._stash
        self._rl_step += 1

        centers = all_projected[:n_global].mean(0)
        per_view = (centers.unsqueeze(0) - all_predicted).square().mean(-1)  # [V, B]
        n_policy = log_prob.shape[1]
        policy_inv = per_view[n_global + n_random_local:]                    # [P, B]
        random_inv = per_view[n_global:n_global + n_random_local].mean(0)    # [B]

        # Hard-view reward: policy crop is "good" when it is HARDER than the random
        # control. 'easy' flips the sign to the spec's literal formula.
        r = policy_inv - random_inv.unsqueeze(0)
        if self.rl_reward == "easy":
            r = -r
        adv = (r - r.mean()).detach()                       # batch-mean baseline
        rl_loss = -(log_prob.T * adv).mean() - self.rl_entropy_beta * entropy

        self.last_rl = {"entropy": entropy.detach(), "reward": r.mean().detach()}
        if self._rl_step.item() < self.rl_warmup_steps:
            return loss, inv_loss, sigreg_loss
        return loss + self.rl_w * rl_loss, inv_loss, sigreg_loss
