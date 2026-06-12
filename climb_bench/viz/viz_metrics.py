"""Online-metric curves + ranking for ANY batch (unified, replaces the old
per-batch visualize*.py).

Reads per-run ``metrics.csv`` under ``climb_bench/viz/metric_results/<batch>/<run>/``
and produces, in ``climb_bench/viz/figures/<batch>/``:
  * curve plots (linear-probe top1, kNN top1, RankMe, train loss) vs epoch
  * a per-run summary (best/last) + a ranking table with Δ vs the baseline run

Generic: it plots whatever runs exist under the batch dir and ranks them against
a baseline run (auto-detected as the lone dir whose name contains "baseline", or
set explicitly with --baseline). NB: the ONLINE probe here (single CLS, lr 0.03)
is NOT the paper recipe — use it to triage/rank, not to conclude. The metric of
record is viz_paperspec.py (frozen, concat CLS last-2 + LN).

    python viz_metrics.py --batch batch_2
    python viz_metrics.py --batch batch_1 --baseline baseline_400
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
METRICS = {
    "eval/linear_probe_top1_epoch": ("linear-probe top1", "linear_probe.png"),
    "eval/knn_probe_top1":          ("kNN top1", "knn.png"),
    "rankme":                       ("RankMe", "rankme.png"),
    "fit/loss_epoch":               ("train loss", "train_loss.png"),
}


def per_epoch(df: pd.DataFrame, col: str) -> pd.Series:
    """Collapse the long CSVLogger frame to one value per epoch (last non-NaN)."""
    if col not in df.columns:
        return pd.Series(dtype=float)
    sub = df[["epoch", col]].dropna(subset=["epoch", col])
    if sub.empty:
        return pd.Series(dtype=float)
    sub["epoch"] = sub["epoch"].astype(int)
    return sub.groupby("epoch")[col].last()


def pretty(run: str) -> str:
    """exp6-convstem-vits -> convstem; idea4_uniformity_400 -> idea4_uniformity_400."""
    s = run
    for pre in ("exp",):
        if s.startswith(pre):
            s = s.split("-", 1)[1] if "-" in s else s
    return s.replace("-vits", "")


def load(data_dir: Path) -> dict[str, pd.DataFrame]:
    out = {}
    for d in sorted(data_dir.iterdir()):
        p = d / "metrics.csv"
        if p.exists():
            out[d.name] = pd.read_csv(p, low_memory=False)
    return out


def pick_baseline(frames, explicit):
    if explicit:
        return explicit if explicit in frames else None
    cands = [k for k in frames if "baseline" in k.lower()]
    return cands[0] if len(cands) == 1 else None


def summarize(frames, base):
    rows = []
    order = ([base] if base else []) + [k for k in frames if k != base]
    for key in order:
        df = frames[key]
        lp = per_epoch(df, "eval/linear_probe_top1_epoch")
        kn = per_epoch(df, "eval/knn_probe_top1")
        rm = per_epoch(df, "rankme")
        rows.append({
            "run": key, "name": pretty(key),
            "max_epoch": int(lp.index.max()) if len(lp) else -1,
            "lp_best": float(lp.max()) if len(lp) else np.nan,
            "lp_best_ep": int(lp.idxmax()) if len(lp) else -1,
            "lp_last": float(lp.iloc[-1]) if len(lp) else np.nan,
            "knn_best": float(kn.max()) if len(kn) else np.nan,
            "rankme_last": float(rm.iloc[-1]) if len(rm) else np.nan,
        })
    return pd.DataFrame(rows)


def ranking(summ, base):
    r = summ[["name", "lp_best", "lp_best_ep", "knn_best", "rankme_last"]].copy()
    if base is not None and base in set(summ["run"]):
        b_lp = float(summ.loc[summ["run"] == base, "lp_best"].iloc[0])
        b_kn = float(summ.loc[summ["run"] == base, "knn_best"].iloc[0])
        r["d_lp_vs_base"] = (r["lp_best"] - b_lp).round(4)
        r["d_knn_vs_base"] = (r["knn_best"] - b_kn).round(4)
    return r.sort_values("lp_best", ascending=False).reset_index(drop=True)


def plot_metric(frames, base, col, title, out_path):
    plt.figure(figsize=(9, 5.5))
    for key, df in frames.items():
        s = per_epoch(df, col)
        if s.empty:
            continue
        is_base = key == base
        plt.plot(s.index, s.values, "-", lw=3 if is_base else 1.7,
                 color="black" if is_base else None, zorder=5 if is_base else 1,
                 label=pretty(key))
    plt.xlabel("epoch"); plt.ylabel(title); plt.title(f"{title} vs epoch")
    plt.grid(alpha=0.3); plt.legend(fontsize=8, ncol=2)
    plt.tight_layout(); plt.savefig(out_path, dpi=130); plt.close()
    print(f"  saved {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="batch_2", help="e.g. batch_1, batch_2")
    ap.add_argument("--baseline", default=None, help="run dir to use as baseline (auto if one matches 'baseline')")
    args = ap.parse_args()

    data_dir = HERE / "metric_results" / args.batch
    out_dir = HERE / "figures" / args.batch
    out_dir.mkdir(parents=True, exist_ok=True)

    frames = load(data_dir)
    if not frames:
        print("no runs found in", data_dir); return
    base = pick_baseline(frames, args.baseline)
    print(f"[{args.batch}] runs: {list(frames)} | baseline: {base}\n")

    summ = summarize(frames, base)
    print("==== Per-run summary (best / last) ====")
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(summ.to_string(index=False))
    summ.to_csv(out_dir / "summary.csv", index=False)

    print(f"\n==== Ranking by best online linear-probe top1 (Δ vs {base or 'n/a'}) ====")
    rank = ranking(summ, base)
    print(rank.to_string(index=False))
    rank.to_csv(out_dir / "ranking.csv", index=False)

    print("\n==== Plots ====")
    for col, (title, fname) in METRICS.items():
        plot_metric(frames, base, col, title, out_dir / fname)


if __name__ == "__main__":
    main()
