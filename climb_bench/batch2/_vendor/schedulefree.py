"""Schedule-Free AdamW for batch-2 experiments.

Source: vendored faithfully from facebookresearch/schedule_free
(``schedulefree/adamw_schedulefree.py``, scalar reference path).
License: Apache-2.0 in the upstream repository at time of vendoring.

Implements the published Schedule-Free algorithm (Defazio et al., NeurIPS 2024,
arXiv:2405.15682): the optimizer keeps the gradient-stepping iterate ``z`` and
the polynomially-weighted running average ``x``; the stored parameter is the
interpolation ``y = (1-beta1) z + beta1 x`` (train mode). ``eval()`` swaps the
parameters to the averaged iterate ``x``; ``train()`` swaps them back to ``y``.

NOTE (correctness): the averaging weight is ``ckp1 = weight / weight_sum`` with
``weight = (k+1)**r * lr_max**weight_lr_power`` — this 1/t-style Polyak average
is what makes the method schedule-free. A fixed (1-beta1) interpolation is NOT
equivalent and must not be substituted.
"""

from __future__ import annotations

import math

import torch
from torch.optim import Optimizer


class AdamWScheduleFree(Optimizer):
    def __init__(
        self,
        params,
        lr: float = 2.5e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 0.0,
        warmup_steps: int = 0,
        r: float = 0.0,
        weight_lr_power: float = 2.0,
    ):
        defaults = dict(
            lr=lr,
            betas=betas,
            eps=eps,
            weight_decay=weight_decay,
            warmup_steps=warmup_steps,
            r=r,
            weight_lr_power=weight_lr_power,
            k=0,
            train_mode=True,
            weight_sum=0.0,
            lr_max=-1.0,
        )
        super().__init__(params, defaults)

    @property
    def eval_mode(self) -> bool:
        return not self.param_groups[0]["train_mode"]

    @torch.no_grad()
    def eval(self):
        for group in self.param_groups:
            if not group["train_mode"]:
                continue
            beta1, _ = group["betas"]
            for p in group["params"]:
                state = self.state[p]
                z = state.get("z")
                if z is None:
                    continue
                # y -> x (averaged iterate)
                p.lerp_(end=z, weight=1 - 1 / beta1)
            group["train_mode"] = False

    @torch.no_grad()
    def train(self):
        for group in self.param_groups:
            if group["train_mode"]:
                continue
            beta1, _ = group["betas"]
            for p in group["params"]:
                state = self.state[p]
                z = state.get("z")
                if z is None:
                    continue
                # x -> y (interpolated iterate)
                p.lerp_(end=z, weight=1 - beta1)
            group["train_mode"] = True

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            if not group["train_mode"]:
                raise RuntimeError(
                    "AdamWScheduleFree.step() called in eval mode; call optimizer.train() first."
                )
            eps = group["eps"]
            beta1, beta2 = group["betas"]
            decay = group["weight_decay"]
            k = group["k"]
            r = group["r"]
            warmup_steps = group["warmup_steps"]
            weight_lr_power = group["weight_lr_power"]

            sched = (k + 1) / warmup_steps if (warmup_steps > 0 and k < warmup_steps) else 1.0
            bias_correction2 = 1 - beta2 ** (k + 1)
            lr = group["lr"] * sched * math.sqrt(bias_correction2)

            lr_max = group["lr_max"] = max(lr, group["lr_max"])
            weight = ((k + 1) ** r) * (lr_max ** weight_lr_power)
            weight_sum = group["weight_sum"] = group["weight_sum"] + weight
            ckp1 = weight / weight_sum if weight_sum != 0 else 0.0

            adaptive_y_lr = lr * (beta1 * (1 - ckp1) - 1)

            for p in group["params"]:
                if p.grad is None:
                    continue
                y = p
                grad = p.grad
                state = self.state[p]
                if "z" not in state:
                    state["z"] = torch.clone(p, memory_format=torch.preserve_format)
                    state["exp_avg_sq"] = torch.zeros_like(p)

                z = state["z"]
                exp_avg_sq = state["exp_avg_sq"]

                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
                denom = exp_avg_sq.div(bias_correction2).sqrt_().add_(eps)

                grad_normalized = grad.div(denom)
                if decay != 0:
                    grad_normalized = grad_normalized.add(y, alpha=decay)

                # y update: move toward averaged iterate then take the adaptive step
                p.lerp_(end=z, weight=ckp1)
                p.add_(grad_normalized, alpha=adaptive_y_lr)
                # z update
                z.sub_(grad_normalized, alpha=lr)

            group["k"] = k + 1
        return loss
