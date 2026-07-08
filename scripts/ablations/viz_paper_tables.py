"""Render our ablation results as paper-style tables mirroring ``tab:ablations`` (a)-(e).

Reproduces the layout of the LeJEPA paper's ablation table on OUR imagenet10/ViT-S data:
  (a) Epps-Pulley params   -> full (we have slices x t_max x n_points)
  (b) Number of views      -> full (n_views x n_global)
  (c) Mini-batch size      -> NOT swept here (fixed 512)
  (d) Emb/Projector dim     -> NOT run (needs_model_support); shown as projector ARCH instead
  (e) Register tokens      -> NOT run (needs_model_support)

Values = paper-spec frozen linear-probe top1 (%). Output:
``ablation_results/figures/paper_tables.png`` / ``.pdf``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update(
    {"text.usetex": False, "font.family": "serif",
     "font.serif": ["DejaVu Serif"], "mathtext.fontset": "cm"}
)

ANCHOR = 0.5946
COLLAPSE = 0.40
GRAY = "#555555"


def _booktabs(ax, col_labels, cell_text, title, col_widths=None,
              collapse_mask=None, baseline_rc=None, subtitle=None):
    """Draw a gridless, booktabs-style table (top/header/bottom rules only)."""
    ax.axis("off")
    ax.set_title(title, fontweight="bold", fontsize=12, pad=6)
    nrow, ncol = len(cell_text), len(col_labels)
    tbl = ax.table(cellText=cell_text, colLabels=col_labels, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10.5)
    tbl.scale(1, 1.45)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("none")
        if col_widths:
            cell.set_width(col_widths[c])
        if r == 0:  # header
            cell.set_text_props(fontweight="bold")
            cell.visible_edges = "B"
            cell.set_edgecolor("black")
            cell.set_linewidth(1.2)
        if r == 1:
            cell.visible_edges = "T"  # header rule already via row0 bottom
        if r == nrow:  # last data row -> bottom rule
            cell.visible_edges = "B"
            cell.set_edgecolor("black")
            cell.set_linewidth(1.2)
        # top rule on first header cell row handled by header B; add top rule:
    # top rule
    for c in range(ncol):
        tbl[0, c].visible_edges = "TB"
        tbl[0, c].set_edgecolor("black")
        tbl[0, c].set_linewidth(1.2)
    # collapse cells -> red; baseline cell -> bold
    if collapse_mask:
        for (r, c) in collapse_mask:
            tbl[r, c].set_text_props(color="#c0392b", fontweight="bold")
    if baseline_rc:
        for (r, c) in baseline_rc:
            tbl[r, c].set_text_props(fontweight="bold")
            tbl[r, c].set_facecolor("#eef4fb")
    if subtitle:
        ax.text(0.5, -0.02, subtitle, transform=ax.transAxes, ha="center",
                va="top", fontsize=8.5, color=GRAY, style="italic")


def _fmt(v):
    return f"{v*100:.2f}" if pd.notna(v) else "–"


def table_a(df, ax):
    e = df[df.spec == "epps"]
    tmax, slices, npts = [1.0, 3.0, 5.0], [512, 1024, 4096], [5, 17, 41]
    cols = ["integration", "num_slices", "5", "17", "41"]
    cell, collapse, base = [], [], []
    ri = 1
    for t in tmax:
        for si, s in enumerate(slices):
            row = [f"[$-{int(t)},{int(t)}$]" if si == 0 else "", str(s)]
            for n in npts:
                m = e[(e.bstat_t_max == t) & (e.bstat_num_slices == s) & (e.bstat_n_points == n)]
                v = m.top1.iloc[0] if len(m) else float("nan")
                row.append(_fmt(v))
                if pd.notna(v) and v < COLLAPSE:
                    collapse.append((ri, len(row) - 1))
                if t == 3.0 and s == 1024 and n == 17:
                    base.append((ri, len(row) - 1))
            cell.append(row)
            ri += 1
    _booktabs(ax, cols, cell, "(a) Epps-Pulley parameters",
              col_widths=[0.30, 0.22, 0.16, 0.16, 0.16], collapse_mask=collapse,
              baseline_rc=base, subtitle="rows: integration $t_{\\max}$ x num_slices  |  cols: bstat_n_points")


def table_b(df, ax):
    v = df[df.spec == "views"]
    nv, ng = [4, 6, 8, 10], [1, 2, 4]
    cols = ["# views $V$  \\  # global $V_g$", "1", "2", "4"]
    cell, base = [], []
    for ri, n in enumerate(nv, start=1):
        row = [str(n)]
        for g in ng:
            m = v[(v.n_views == n) & (v.n_global_views == g)]
            val = m.top1.iloc[0] if len(m) else float("nan")
            row.append(_fmt(val))
            if n == 8 and g == 2:
                base.append((ri, len(row) - 1))
        cell.append(row)
    _booktabs(ax, cols, cell, "(b) Number of local/global views",
              col_widths=[0.40, 0.20, 0.20, 0.20], baseline_rc=base,
              subtitle="rows: total views $V$  |  cols: # global views $V_g$")


def table_c(ax):
    ax.axis("off")
    ax.set_title("(c) Mini-batch size", fontweight="bold", fontsize=12, pad=6)
    ax.text(0.5, 0.5, "not ablated in this study\n(fixed batch_size = 512)",
            transform=ax.transAxes, ha="center", va="center", fontsize=11, color=GRAY)


def table_d(df, ax):
    p = df[df.spec == "projector_depth"]
    order = ["Linear", "MLP2", "MLP", "MLP4"]
    p = p.set_index("projector_arch").loc[order].reset_index()
    cols = ["projector_arch", "top1"]
    cell, collapse, base = [], [], []
    for ri, r in enumerate(p.itertuples(), start=1):
        cell.append([r.projector_arch, _fmt(r.top1)])
        if r.top1 < COLLAPSE:
            collapse.append((ri, 1))
        if r.projector_arch == "MLP":
            base.append((ri, 1))
    _booktabs(ax, cols, cell, "(d) Projector architecture",
              col_widths=[0.55, 0.45], collapse_mask=collapse, baseline_rc=base,
              subtitle="paper (d) = emb/proj DIM (needs_model_support, not run)\n"
                       "shown: projector depth/arch instead")


def table_e(ax):
    ax.axis("off")
    ax.set_title("(e) Register tokens", fontweight="bold", fontsize=12, pad=6)
    ax.text(0.5, 0.5, "not run\n(reg_tokens = needs_model_support)",
            transform=ax.transAxes, ha="center", va="center", fontsize=11, color=GRAY)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root")
    args = ap.parse_args()
    root = Path(args.root)
    df = pd.read_csv(root / "ablation_summary.csv")

    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(3, 2, height_ratios=[3.2, 2.2, 1.0], hspace=0.45, wspace=0.25)
    table_a(df, fig.add_subplot(gs[0, 0]))
    table_d(df, fig.add_subplot(gs[0, 1]))
    table_b(df, fig.add_subplot(gs[1, 0]))
    table_e(fig.add_subplot(gs[1, 1]))
    table_c(fig.add_subplot(gs[2, 0]))
    fig.suptitle("LeJEPA ablations (our data) — ViT-S/16, imagenet10, frozen linear probe top1 (%). "
                 "Baseline shaded; collapse in red.", fontsize=12.5, y=0.97)
    out = root / "figures"
    out.mkdir(exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"paper_tables.{ext}", bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"Wrote {out}/paper_tables.png / .pdf")


if __name__ == "__main__":
    main()
