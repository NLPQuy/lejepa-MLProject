"""Visualize paper-spec frozen linear-probe results for ANY batch.

Reads ``eval_results/<batch>/*.json`` (produced by eval-frozen-paperspec.py) and
emits a bar chart of frozen linear-probe top1 per idea (Δ vs baseline) + a table.
The metric of record (concat CLS last-2 + LN, AdamW lr1e-3 wd1e-6) — unlike the
online probe in viz_metrics.py.

Baseline is auto-detected as the tag containing "baseline". On Kaggle the script
sits under a read-only /kaggle/input mount, so --out must be writable.

    python viz_paperspec.py --batch batch_2
    python viz_paperspec.py --results /kaggle/working/eval_results/batch_2 --out /kaggle/working
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="batch_2", help="e.g. batch_1, batch_2")
    ap.add_argument("--results", default=None, help="dir of *.json (default: eval_results/<batch>)")
    ap.add_argument("--out", default=None, help="writable dir for the figure (default: figures/<batch>)")
    args = ap.parse_args()
    res_dir = Path(args.results) if args.results else HERE / "eval_results" / args.batch
    out_dir = Path(args.out) if args.out else HERE / "figures" / args.batch
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for p in res_dir.glob("*.json"):
        if p.stem.startswith("_"):
            continue
        results[p.stem] = json.loads(p.read_text())
    if not results:
        print("no results found in", res_dir); return

    base_tag = next((t for t in results if "baseline" in t.lower()), None)
    base = results[base_tag]["top1"] if base_tag else None

    print(f"==== Paper-spec frozen linear-probe ({args.batch}): concat CLS last-2 + LN ====")
    print(f"{'idea':18s} {'top1':>7s} {'top5':>7s} {'Δtop1':>8s}   n_tr/n_va  probe_ep")
    # baseline first, then by top1 desc
    order = ([base_tag] if base_tag else []) + sorted(
        (t for t in results if t != base_tag), key=lambda t: -results[t]["top1"])
    rows = []
    for tag in order:
        r = results[tag]
        d = f"{r['top1'] - base:+.4f}" if (base is not None and tag != base_tag) else "—"
        print(f"{tag:18s} {r['top1']:.4f} {r['top5']:7.4f} {d:>8s}   "
              f"{r['n_train']}/{r['n_val']}   {r['probe_epochs']}")
        rows.append((tag, r["top1"], (r["top1"] - base) if base else 0.0, tag == base_tag))

    names = [r[0] for r in rows]
    tops = [r[1] for r in rows]
    colors = ["black" if r[3] else ("tab:green" if r[2] >= 0 else "tab:red") for r in rows]
    plt.figure(figsize=(max(8, 1.1 * len(rows)), 5))
    bars = plt.bar(names, tops, color=colors)
    if base is not None:
        plt.axhline(base, ls="--", color="gray", lw=1, label=f"baseline {base:.3f}")
    for b, r in zip(bars, rows):
        lbl = f"{r[1]:.3f}" + ("" if r[3] else f"\n({r[2]:+.3f})")
        plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.005, lbl,
                 ha="center", va="bottom", fontsize=8)
    plt.ylabel("frozen linear-probe top1 (paper-spec)")
    plt.title(f"Paper-spec frozen probe — {args.batch}")
    plt.ylim(0, max(tops) * 1.18)
    plt.xticks(rotation=20, ha="right")
    plt.legend(); plt.tight_layout()
    fig_path = out_dir / f"paperspec_{args.batch}.png"
    plt.savefig(fig_path, dpi=130)
    print(f"\nsaved {fig_path}")


if __name__ == "__main__":
    main()
