"""Collect LeJEPA ablation results from per-job ``summary.json`` files.

The Kaggle ablation outputs store the downstream linear-probe metric in
``results/<spec>/job*/summary.json`` under ``paper_eval`` (``metrics.csv`` only
holds loss curves, no accuracy). This walks that tree and writes:

- ``ablation_summary.csv`` -- one row per job, every varied config key as a column
- ``ablation_summary.md``  -- grouped by spec, sorted by top1 desc, baseline flagged

Run from the project root::

    python scripts/ablations/collect_summaries.py ablation_results/
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd


# Canonical baseline value for each ablated knob (mirrors
# scripts/ablations/specs.py::BASE_OVERRIDES; hard-coded to avoid importing
# specs.py, which runs a timm model probe at import time).
BASELINE = {
    "bstat_num_slices": 1024,
    "bstat_t_max": 3.0,
    "bstat_n_points": 17,
    "drop_path_rate": 0.1,
    "patch_mask_ratio": 0.3,
    "projector_arch": "MLP",
    "sigreg_target": "proj",
    "predictor": "none",
    "aggregator": "cls",
    "n_views": 8,
    "n_global_views": 2,
}

META_COLS = ["spec", "job", "final_loss", "top1", "top5", "best_probe_epoch"]


def _load_rows(root: Path) -> list[dict]:
    rows = []
    for f in sorted(root.glob("*/*/summary.json")):
        spec = f.parent.parent.name
        job = f.parent.name
        d = json.loads(f.read_text())
        pe = d.get("paper_eval") or {}
        rows.append(
            {
                "spec": spec,
                "job": job,
                "final_loss": d.get("final_loss"),
                "top1": pe.get("top1"),
                "top5": pe.get("top5"),
                "best_probe_epoch": pe.get("best_probe_epoch"),
                "_config": d.get("config", {}),
            }
        )
    return rows


def _varied_keys(configs: list[dict]) -> list[str]:
    keys = set().union(*(c.keys() for c in configs)) if configs else set()
    return sorted(k for k in keys if len({repr(c.get(k)) for c in configs}) > 1)


def _matches_baseline(config: dict, varied: list[str]) -> bool:
    """True if every varied knob equals the canonical baseline value."""
    checked = False
    for k in varied:
        if k not in BASELINE:
            continue
        checked = True
        a, b = config.get(k), BASELINE[k]
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if not math.isclose(float(a), float(b)):
                return False
        elif a != b:
            return False
    return checked


def build(root: Path):
    rows = _load_rows(root)
    by_spec: dict[str, list[dict]] = {}
    for r in rows:
        by_spec.setdefault(r["spec"], []).append(r)

    # flat CSV with union of all varied keys as columns
    all_varied = sorted(set().union(*(_varied_keys([r["_config"] for r in rs]) for rs in by_spec.values())))
    flat = []
    for r in rows:
        base = {k: r[k] for k in META_COLS}
        base.update({k: r["_config"].get(k) for k in all_varied})
        flat.append(base)
    df = pd.DataFrame(flat, columns=META_COLS + all_varied)
    csv_path = root / "ablation_summary.csv"
    df.to_csv(csv_path, index=False)

    # grouped markdown, sorted by top1 desc, baseline starred
    lines = ["# Ablation summary (paper-spec linear probe, top1)", ""]
    lines.append(f"Source: `{root}/` — {len(rows)} jobs across {len(by_spec)} ablations. ")
    lines.append("★ = config matching `BASE_OVERRIDES`. top1/top5 from `summary.json` → `paper_eval`.")
    lines.append("")
    for spec in sorted(by_spec):
        rs = by_spec[spec]
        varied = _varied_keys([r["_config"] for r in rs])
        rs_sorted = sorted(rs, key=lambda r: (r["top1"] is None, -(r["top1"] or 0)))
        lines.append(f"## {spec}  (n={len(rs)}, knob: {', '.join(varied) or 'none'})")
        lines.append("")
        header = ["", *varied, "top1", "top5", "final_loss", "best_ep"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---"] * len(header)) + "|")
        for r in rs_sorted:
            star = "★" if _matches_baseline(r["_config"], varied) else ""
            vals = [star]
            vals += [str(r["_config"].get(k)) for k in varied]
            vals += [
                f"{r['top1']:.4f}" if r["top1"] is not None else "-",
                f"{r['top5']:.4f}" if r["top5"] is not None else "-",
                f"{r['final_loss']:.3f}" if r["final_loss"] is not None else "-",
                str(r["best_probe_epoch"]) if r["best_probe_epoch"] is not None else "-",
            ]
            lines.append("| " + " | ".join(vals) + " |")
        lines.append("")
    md_path = root / "ablation_summary.md"
    md_path.write_text("\n".join(lines))
    return csv_path, md_path, df


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", help="Unified results dir (e.g. ablation_results/)")
    args = ap.parse_args()
    csv_path, md_path, df = build(Path(args.root))
    print(f"Wrote {csv_path} ({len(df)} rows)")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
