"""Minimal Muon optimizer for batch-2 experiments.

Source: reimplemented from Keller Jordan's Muon reference implementation
(``KellerJordan/Muon``, ``muon.py``) and the public Muon training notes.
License: MIT license in the upstream repository at time of vendoring.

This offline-friendly implementation follows the key mechanism: 2-D tensors use
momentum followed by Newton-Schulz orthogonalization; vectors / biases / norms
fall back to AdamW in the same optimizer object.
"""

from __future__ import annotations

import math

import torch
from torch.optim import Optimizer


def zeropower_via_newtonschulz5(g: torch.Tensor, steps: int = 5, eps: float = 1e-7) -> torch.Tensor:
    """Approximate the zeroth power / orthogonal factor of a 2-D update."""

    if g.ndim != 2:
        raise ValueError("Muon orthogonalization expects a 2-D tensor")
    x = g.float()
    if x.size(0) > x.size(1):
        x = x.t()
        transposed = True
    else:
        transposed = False

    x = x / (x.norm() + eps)
    a, b, c = 3.4445, -4.7750, 2.0315
    for _ in range(steps):
        xx_t = x @ x.t()
        x = a * x + (b * xx_t + c * (xx_t @ xx_t)) @ x

    if transposed:
        x = x.t()
    return x.to(dtype=g.dtype)


class Muon(Optimizer):
    """Muon for matrix weights plus AdamW fallback for non-matrix tensors."""

    def __init__(
        self,
        params,
        lr: float = 2e-4,
        weight_decay: float = 0.05,
        momentum: float = 0.95,
        nesterov: bool = True,
        ns_steps: int = 5,
        adamw_lr: float | None = None,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
    ):
        defaults = dict(
            lr=lr,
            weight_decay=weight_decay,
            momentum=momentum,
            nesterov=nesterov,
            ns_steps=ns_steps,
            adamw_lr=adamw_lr if adamw_lr is not None else lr,
            betas=betas,
            eps=eps,
        )
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            lr = group["lr"]
            wd = group["weight_decay"]
            momentum = group["momentum"]
            beta1, beta2 = group["betas"]
            eps = group["eps"]
            adamw_lr = group["adamw_lr"]

            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]
                if grad.ndim == 2:
                    if wd != 0:
                        p.mul_(1 - lr * wd)
                    buf = state.get("momentum_buffer")
                    if buf is None:
                        buf = torch.zeros_like(p)
                        state["momentum_buffer"] = buf
                    buf.mul_(momentum).add_(grad)
                    update = grad.add(buf, alpha=momentum) if group["nesterov"] else buf
                    update = zeropower_via_newtonschulz5(update, group["ns_steps"])
                    scale = math.sqrt(max(1.0, p.size(0) / max(1, p.size(1))))
                    p.add_(update, alpha=-lr * scale)
                    continue

                step = state.get("step", 0) + 1
                state["step"] = step
                exp_avg = state.get("exp_avg")
                exp_avg_sq = state.get("exp_avg_sq")
                if exp_avg is None:
                    exp_avg = torch.zeros_like(p)
                    exp_avg_sq = torch.zeros_like(p)
                    state["exp_avg"] = exp_avg
                    state["exp_avg_sq"] = exp_avg_sq
                if wd != 0:
                    p.mul_(1 - adamw_lr * wd)
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
                bias_correction1 = 1 - beta1**step
                bias_correction2 = 1 - beta2**step
                step_size = adamw_lr / bias_correction1
                denom = exp_avg_sq.sqrt().div_(math.sqrt(bias_correction2)).add_(eps)
                p.addcdiv_(exp_avg, denom, value=-step_size)
        return loss
