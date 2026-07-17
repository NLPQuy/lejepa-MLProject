"""Phase-0 statistic sanity harness (plan-batch-7.md §6).

CPU-only, no data, no GPU, ~minutes. Gates exp1 / exp3 before any Kaggle spend.

WHAT THIS TESTS AND WHY THIS SHAPE
----------------------------------
The plan originally proposed comparing each candidate's scalar across synthetic
distributions (N(0,I) vs collapsed vs ...). That does not work. For the KL-surrogate
family the encoder-facing term is

    kl = 0.5*E||z||^2 + E[s(z).detach() * z]

and by integration by parts  E[grad log p(z) . z] = -d  for EVERY smooth density p.
So the surrogate's VALUE degenerates to the second moment and carries no
Gaussianity signal at all — only its GRADIENT is meaningful. Ranking scalars would
have measured nothing.

So instead we test the thing that actually matters: **descend the objective and see
where the distribution goes**, measured with an INDEPENDENT yardstick.

    z is a free parameter matrix (the maximally-flexible encoder). Each step we
    descend the candidate objective exactly as production does — one optimizer over
    {z} U {module's internal net}. Every eval_every steps we measure z with metrics
    the objective never sees: the baseline sliced Epps-Pulley statistic, the per-coord
    std, and ||Cov(z) - I||_F.

A free z is the right stress test: if an objective has a collapse attractor, an
unconstrained encoder will find it.

PRE-REGISTERED PREDICTIONS (plan §3.1, §3.2, §0.1) — kept verbatim, not edited
after the fact; the MISS labels the script prints are the honest record.
    baseline_ep      -> CONVERGE  (positive control, correct by construction)
    orig_hyvarinen   -> COLLAPSE  (§3.1: encoder descends ISM => maximises its own
                                   Fisher information)
    klscore          -> CONVERGE  (§3.1 fix)
    adversarial      -> CONVERGE  (§0.1: judged sound)
    fm_a_ot          -> COLLAPSE  (§3.2: collapse is the global minimum)
    fm_b_ot          -> CONVERGE, possibly with shrunk std (§3.2 soft spot 1)
    fm_b_vp          -> CONVERGE  (§3.2 soft spot 2 mitigation)

RECORDED OUTCOME (2026-07-17, n=256 d=16 steps=1500, ref N(0,I) ep=1.116)
    baseline_ep      CONVERGE   ep 49.0 -> 0.15   OK
    klscore          CONVERGE   ep 51.0 -> 0.48   OK   => exp1 SHIPS
    orig_hyvarinen   NO-SIGNAL  ep 45.7 -> 86.4   MISS: direction of the §3.1 claim
                                confirmed (it drives the encoder the WRONG way, ep
                                nearly doubles) but the failure mode is "actively
                                anti-Gaussian", not the predicted collapse (std 0.943).
    adversarial      PARTIAL    ep 49.0 -> 13.7 @ 12k steps, still falling. Not broken
                                — ~50-100x SLOWER than baseline. Flags idea 3's
                                "M=1 suffices / 1000x cheaper" claim as unsupported:
                                per-step cost falls, step COUNT rises. The M=1-random
                                control arm is therefore mandatory.
    fm_a_ot          NO-SIGNAL  ep 46.3 -> 61.0   MISS: the addendum's as-written spec
                                fails, but by stalling/worsening rather than collapsing
                                outright within 1500 steps (std drifting down, 0.72).
    fm_b_ot          CONVERGE   ep 46.4 -> 0.87 @ 12k steps, stable => exp3 SHIPS
                                (path=ot, band [0.3,0.7]).
    fm_b_vp          NO-SIGNAL  the variance-preserving path proposed as a mitigation
                                for §3.2 soft spot 1 is UNNECESSARY and WORSE than ot.
                                Soft spot 1 did not bite (ot reaches std 1.056).

t-band sweep for fm_b (the decisive result — see FMSIGRegB docstring):
    ot [0.1,0.3] DIVERGE  | ot [0.3,0.7] CONVERGE ep 0.59 | ot [0.5,0.9] COLLAPSE
    std 0.161 | ot [0.05,0.95] NO-SIGNAL
    A textbook bias-variance curve: small t = 1/t noise amplification, large t =
    p_t -> N(0,I) so no signal about the encoder at all.

Run:  python climb_bench/batch7/test_statistics.py
      python climb_bench/batch7/test_statistics.py --n 256 --steps 1500 --eval_every 500
      python climb_bench/batch7/test_statistics.py --only adversarial,fm_b_ot --steps 12000
"""

from __future__ import annotations

import argparse
import os
import sys

os.environ.setdefault("SPT_LIGHT_IMPORT", "0")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn as nn

from stable_pretraining.methods.lejepa import SlicedEppsPulley
from _variants import AdversarialSIGReg, FMSIGRegA, FMSIGRegB, KLScoreSIGReg


# ---------------------------------------------------------------------------
# Control: the ORIGINAL (unfixed) implementation, copied verbatim from
# stable_pretraining/methods/lejepa_variants.py::HyvarienSIGReg @ 7ec8f45.
# Included so the §3.1 claim is demonstrated, not just asserted.
# ---------------------------------------------------------------------------

class OriginalHyvarienSIGReg(nn.Module):
    def __init__(self, dim: int, hidden_dim: int | None = None):
        super().__init__()
        hidden_dim = hidden_dim or 4 * dim
        self.score_net = nn.Sequential(
            nn.Linear(dim, hidden_dim), nn.SiLU(), nn.Linear(hidden_dim, dim)
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        s = self.score_net(z) - z
        v = torch.randn_like(z)
        sv_dot = (s * v).sum()
        jvp = torch.autograd.grad(sv_dot, z, create_graph=True)[0]
        main_term = 0.5 * (s + z).pow(2).sum(-1).mean()
        hutch_trace = (v * jvp).sum(-1).mean()
        return main_term + hutch_trace


# ---------------------------------------------------------------------------
# Independent yardstick — metrics the objectives never see
# ---------------------------------------------------------------------------

@torch.no_grad()
def measure(z: torch.Tensor, ep: SlicedEppsPulley) -> dict:
    zc = z.detach().float()
    cov = torch.cov(zc.T)
    eye = torch.eye(cov.shape[0])
    return {
        "ep": ep(zc).item(),                       # sliced Epps-Pulley vs N(0,1)
        "std": zc.std(0).mean().item(),            # ~1.0 at N(0,I); ->0 on collapse
        "cov_err": (cov - eye).norm().item(),      # ||Cov - I||_F
        "absmean": zc.mean(0).abs().mean().item(),
    }


def make_candidates(dim: int) -> dict:
    return {
        "baseline_ep":    lambda: SlicedEppsPulley(num_slices=256),
        "orig_hyvarinen": lambda: OriginalHyvarienSIGReg(dim=dim),
        "klscore":        lambda: KLScoreSIGReg(dim=dim),
        "adversarial":    lambda: AdversarialSIGReg(dim=dim),
        "fm_a_ot":        lambda: FMSIGRegA(dim=dim, path="ot"),
        "fm_b_ot":        lambda: FMSIGRegB(dim=dim, path="ot"),
        "fm_b_vp":        lambda: FMSIGRegB(dim=dim, path="vp"),
    }


def run_one(name: str, build, args, ep_ref: SlicedEppsPulley, ref: dict) -> dict:
    torch.manual_seed(args.seed)

    # Start: strongly non-Gaussian (bimodal) AND anisotropic (per-coord scale ramp),
    # but STANDARDISED so mean per-coord std == 1.
    #
    # The standardisation is load-bearing. A start at std 2.47 makes "did not move"
    # indistinguishable from "diverged" under any std-based verdict — the first
    # version of this harness had exactly that bug and mislabelled 5/7 candidates.
    # With mean std == 1 at init:
    #   std stays ~1 + ep stays high  => objective gives the encoder no useful signal
    #   std -> 0                      => collapse attractor
    #   ep -> ref                     => it works
    n, d = args.n, args.dim
    comp = (torch.rand(n, 1) < 0.5).float()
    z0 = torch.randn(n, d) * torch.linspace(0.4, 1.6, d) + (comp * 4.0 - 2.0)
    z0 = (z0 - z0.mean(0)) / z0.std(0).mean()
    z = nn.Parameter(z0.clone())

    module = build()
    params = [z] + list(module.parameters())
    opt = torch.optim.Adam(params, lr=args.lr)

    traj = []
    for step in range(args.steps + 1):
        if step % args.eval_every == 0:
            traj.append((step, measure(z, ep_ref)))
        opt.zero_grad(set_to_none=True)
        loss = module(z)
        loss.backward()
        opt.step()

    init, final = traj[0][1], traj[-1][1]

    # Verdict vs the independent yardstick. Thresholds are deliberately loose;
    # we are separating "went to N(0,I)" from "collapsed" from "did nothing",
    # not grading precision.
    if final["std"] < 0.5:
        verdict = "COLLAPSE"
    elif final["std"] > 2.0:
        verdict = "DIVERGE"
    elif final["ep"] <= max(3.0 * ref["ep"], ref["ep"] + 1.0):
        verdict = "CONVERGE"
    elif final["ep"] > 0.5 * init["ep"]:
        verdict = "NO-SIGNAL"   # barely moved off a non-Gaussian start
    else:
        verdict = "PARTIAL"

    return {"name": name, "init": init, "final": final, "traj": traj, "verdict": verdict}


def main():
    p = argparse.ArgumentParser(description="Batch-7 Phase-0 statistic sanity harness")
    p.add_argument("--n", type=int, default=1024)
    p.add_argument("--dim", type=int, default=16)
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--eval_every", type=int, default=500)
    p.add_argument("--lr", type=float, default=1e-2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--only", default=None, help="comma-separated candidate names")
    args = p.parse_args()

    torch.manual_seed(args.seed)
    ep_ref = SlicedEppsPulley(num_slices=256)

    # Calibrate the yardstick on true N(0,I) samples.
    ref = measure(torch.randn(args.n, args.dim), ep_ref)
    print(f"\nReference N(0,I) @ n={args.n} d={args.dim}: "
          f"ep={ref['ep']:.3f} std={ref['std']:.3f} cov_err={ref['cov_err']:.3f}\n")

    candidates = make_candidates(args.dim)
    if args.only:
        keep = set(args.only.split(","))
        candidates = {k: v for k, v in candidates.items() if k in keep}

    results = []
    for name, build in candidates.items():
        r = run_one(name, build, args, ep_ref, ref)
        results.append(r)
        ep_traj = " -> ".join(f"{m['ep']:.1f}" for _, m in r["traj"])
        print(f"{name:16s} {r['verdict']:10s} "
              f"ep={r['final']['ep']:8.3f}  std={r['final']['std']:.3f}  "
              f"cov_err={r['final']['cov_err']:7.3f}   ep traj: {ep_traj}")

    predicted = {
        "baseline_ep": "CONVERGE", "orig_hyvarinen": "COLLAPSE", "klscore": "CONVERGE",
        "adversarial": "CONVERGE", "fm_a_ot": "COLLAPSE", "fm_b_ot": "CONVERGE",
        "fm_b_vp": "CONVERGE",
    }
    print("\n--- vs pre-registered predictions (plan §3.1/§3.2) ---")
    for r in results:
        exp = predicted.get(r["name"], "?")
        mark = "OK  " if exp == r["verdict"] else "MISS"
        print(f"  {mark} {r['name']:16s} predicted={exp:9s} got={r['verdict']}")

    print("\n--- gate ---")
    ok = {r["name"] for r in results if r["verdict"] == "CONVERGE"}
    print(f"  exp1 (klscore) ships: {'klscore' in ok}")
    fm_ok = [n for n in ("fm_a_ot", "fm_b_ot", "fm_b_vp") if n in ok]
    print(f"  exp3 form to ship: {fm_ok or 'NONE — report negative result, skip GPU (plan §8 Q2)'}")


if __name__ == "__main__":
    main()
