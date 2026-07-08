"""Visualize LeJEPA ablation results following the paper's ``tab:ablations`` pipeline.

Reads ``ablation_results/ablation_summary.csv`` (from collect_summaries.py) and
writes four figures to ``ablation_results/figures/`` (PNG + PDF):

  A  epps_heatmap        top1 over t_max x num_slices, one panel per n_points   (paper tab a)
  B  views_heatmap       top1 over n_views x n_global                           (paper tab b)
  C  components_bars      top1 per component/hyperparam vs baseline, collapse red
  D  sensitivity_tornado  top1 range (min-max) per ablation, sorted

Metric = paper-spec frozen linear-probe top1. Baseline anchor = the config matching
BASE_OVERRIDES (reproduced deterministically at top1=0.5946 across ablations).

Run from project root::

    python scripts/ablations/viz_ablation.py ablation_results/
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paper-style typography without requiring a LaTeX install (no dvipng here).
plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Computer Modern Roman"],
        "mathtext.fontset": "cm",
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.dpi": 120,
    }
)

ANCHOR = 0.5946  # baseline (BASE_OVERRIDES) top1, reproduced across ablations
COLLAPSE = 0.40  # top1 below this = catastrophic collapse (chance ~0.10 on 10-class)
CMAP = "viridis"

# canonical ordering for each ablated knob
ORDER = {
    "bstat_num_slices": [512, 1024, 4096],
    "bstat_t_max": [1.0, 3.0, 5.0],
    "bstat_n_points": [5, 17, 41],
    "n_views": [4, 6, 8, 10],
    "n_global_views": [1, 2, 4],
    "drop_path_rate": [0.0, 0.05, 0.1, 0.2, 0.4],
    "patch_mask_ratio": [0.0, 0.1, 0.2, 0.3, 0.5, 0.7],
    "projector_arch": ["Linear", "MLP2", "MLP", "MLP4"],
    "sigreg_target": ["proj", "embed", "both"],
    "predictor": ["none", "linear", "mlp"],
    "aggregator": ["cls", "mean", "cls_mean"],
}
BASELINE_VAL = {  # baseline value of each knob (mirrors BASE_OVERRIDES)
    "drop_path_rate": 0.1, "patch_mask_ratio": 0.3, "projector_arch": "MLP",
    "sigreg_target": "proj", "predictor": "none", "aggregator": "cls",
}
GROUP_B = [  # architecture: where/how the objective is applied
    ("sigreg_target", "sigreg_target", "SIGReg target"),
    ("projector_depth", "projector_arch", "Projector arch"),
    ("predictor", "predictor", "Predictor"),
    ("aggregation", "aggregator", "Aggregator"),
]
GROUP_C = [  # augmentation-style regularization
    ("drop_path", "drop_path_rate", "Drop-path rate"),
    ("patch_masking", "patch_mask_ratio", "Patch-mask ratio"),
]
COMPONENT_SPECS = GROUP_B + GROUP_C


def _save(fig, out: Path, name: str) -> None:
    for ext in ("png", "pdf"):
        fig.savefig(out / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}.png / .pdf")


def _annot_heat(ax, M, rows, cols, xlabel, ylabel, title):
    im = ax.imshow(M, cmap=CMAP, aspect="auto", vmin=np.nanmin(M), vmax=np.nanmax(M))
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), rows)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = M[i, j]
            if np.isnan(v):
                continue
            ax.text(j, i, f"{v*100:.1f}", ha="center", va="center",
                    color="white" if v < (np.nanmin(M) + np.nanmax(M)) / 2 else "black",
                    fontsize=10)
    return im


def fig_epps(df: pd.DataFrame, out: Path) -> None:
    e = df[df.spec == "epps"]
    npts = ORDER["bstat_n_points"]
    slices = ORDER["bstat_num_slices"]
    tmax = ORDER["bstat_t_max"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), constrained_layout=True)
    im = None
    for ax, npt in zip(axes, npts):
        sub = e[e.bstat_n_points == npt]
        M = np.full((len(tmax), len(slices)), np.nan)
        for _, r in sub.iterrows():
            M[tmax.index(r.bstat_t_max), slices.index(r.bstat_num_slices)] = r.top1
        im = _annot_heat(ax, M, [f"$\\pm${int(t)}" for t in tmax], slices,
                         "num_slices", r"integration $t_{\max}$", f"n_points = {npt}")
    fig.colorbar(im, ax=axes, shrink=0.8, label="top1")
    fig.suptitle("(a) Epps-Pulley integration grid — top1 (%)  [ViT-S/16, imagenet10]",
                 fontsize=13, y=1.08)
    _save(fig, out, "A_epps_heatmap")


def fig_views(df: pd.DataFrame, out: Path) -> None:
    v = df[df.spec == "views"]
    nv, ng = ORDER["n_views"], ORDER["n_global_views"]
    M = np.full((len(nv), len(ng)), np.nan)
    for _, r in v.iterrows():
        M[nv.index(r.n_views), ng.index(r.n_global_views)] = r.top1
    fig, ax = plt.subplots(figsize=(5, 4.2), constrained_layout=True)
    im = _annot_heat(ax, M, nv, ng, r"global views $V_g$", r"total views $V$",
                     "(b) Number of views — top1 (%)")
    fig.colorbar(im, ax=ax, shrink=0.85, label="top1")
    _save(fig, out, "B_views_heatmap")


def _panel(ax, df, spec, knob, title):
    s = df[df.spec == spec].copy()
    order = [x for x in ORDER[knob] if x in set(s[knob])]
    s = s.set_index(knob).loc[order].reset_index()
    vals = s.top1.values
    colors = ["#c0392b" if v < COLLAPSE else "#2c7fb8" for v in vals]
    base = BASELINE_VAL.get(knob)
    edges = ["black" if str(x) == str(base) else "none" for x in s[knob]]
    lw = [2.0 if str(x) == str(base) else 0 for x in s[knob]]
    bars = ax.bar(range(len(vals)), vals, color=colors, edgecolor=edges, linewidth=lw)
    ax.axhline(ANCHOR, ls="--", c="gray", lw=1)
    ax.set_xticks(range(len(vals)), [str(x) for x in s[knob]])
    ax.set_title(title)
    ax.set_ylim(0, 0.8)
    ax.set_ylabel("top1")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v*100:.1f}",
                ha="center", va="bottom", fontsize=9)


def _fig_group(df, out, specs, name, suptitle, nrows, ncols, figsize):
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, constrained_layout=True)
    axf = list(axes.flat) if hasattr(axes, "flat") else [axes]
    for ax, (spec, knob, title) in zip(axf, specs):
        _panel(ax, df, spec, knob, title)
    for ax in axf[len(specs):]:
        ax.axis("off")
    fig.suptitle(suptitle, fontsize=13)
    _save(fig, out, name)


def fig_components(df: pd.DataFrame, out: Path) -> None:
    note = "Red = collapse; black edge = baseline; dashed = baseline top1"
    _fig_group(df, out, COMPONENT_SPECS,
               "C_components_bars", f"(c) Components & regularizers — top1 (%). {note}",
               2, 3, (13, 7))
    _fig_group(df, out, GROUP_B,
               "E_arch_bars", f"(B) Architecture components — top1 (%). {note}",
               1, 4, (14, 3.6))
    _fig_group(df, out, GROUP_C,
               "F_reg_bars", f"(C) Augmentation regularization — top1 (%). {note}",
               1, 2, (8, 3.8))


def fig_tornado(df: pd.DataFrame, out: Path) -> None:
    labels = {
        "epps": "Epps grid (slices/$t_{\\max}$/pts)", "views": "Views ($V$/$V_g$)",
        "projector_depth": "Projector arch", "sigreg_target": "SIGReg target",
        "predictor": "Predictor", "aggregation": "Aggregator",
        "drop_path": "Drop-path", "patch_masking": "Patch-mask",
    }
    rows = []
    for spec, lab in labels.items():
        t = df[df.spec == spec].top1
        rows.append((lab, t.min(), t.max()))
    rows.sort(key=lambda r: r[2] - r[1])  # by range asc -> robust at bottom
    fig, ax = plt.subplots(figsize=(8.5, 4.5), constrained_layout=True)
    for i, (lab, lo, hi) in enumerate(rows):
        collapse = lo < COLLAPSE
        ax.plot([lo, hi], [i, i], "-", c="#c0392b" if collapse else "#2c7fb8", lw=6, alpha=0.85, solid_capstyle="round")
        ax.text(lo - 0.005, i, f"{lo*100:.1f}", ha="right", va="center", fontsize=9)
        ax.text(hi + 0.005, i, f"{hi*100:.1f}", ha="left", va="center", fontsize=9)
    ax.axvline(ANCHOR, ls="--", c="gray", lw=1, label=f"baseline {ANCHOR*100:.1f}")
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlabel("frozen linear-probe top1")
    ax.set_xlim(0.15, 0.80)
    ax.set_title("(d) Sensitivity per ablation — top1 range (red = has collapse)")
    ax.legend(loc="upper right")
    _save(fig, out, "D_sensitivity_tornado")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", help="Unified results dir with ablation_summary.csv")
    args = ap.parse_args()
    root = Path(args.root)
    df = pd.read_csv(root / "ablation_summary.csv")
    out = root / "figures"
    out.mkdir(exist_ok=True)
    print(f"Reading {len(df)} rows -> writing figures to {out}/")
    fig_epps(df, out)
    fig_views(df, out)
    fig_components(df, out)
    fig_tornado(df, out)


if __name__ == "__main__":
    main()
