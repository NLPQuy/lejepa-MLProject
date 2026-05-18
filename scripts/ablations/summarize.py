"""Summarize local ablation CSV logs."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any

import pandas as pd
import yaml

from .specs import get_spec, list_specs


REPO_ROOT = Path(__file__).resolve().parents[2]
STABLE_PRETRAINING_ROOT = REPO_ROOT / "stable-pretraining"
if str(STABLE_PRETRAINING_ROOT) not in sys.path:
    sys.path.insert(0, str(STABLE_PRETRAINING_ROOT))
MPLCONFIGDIR = Path("/private/tmp/lejepa_mplconfig")
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

from stable_pretraining.utils.read_csv_logger import CSVLogAutoSummarizer


SUMMARY_CSV = "all_ablation_summary.csv"
SUMMARY_MD = "all_ablation_summary.md"
META_COLUMNS = (
    "ablation_key",
    "ablation_title",
    "run_root",
    "metric",
    "mode",
    "best_value",
    "best_step",
    "best_epoch",
    "swept_params",
)


def _flatten_config(values: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(values, dict):
        return {}

    flat: dict[str, Any] = {}
    for key, value in values.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            flat.update(_flatten_config(value, name))
        elif isinstance(value, (str, int, float, bool)) or value is None:
            flat[name] = value
        else:
            flat[name] = json.dumps(value, sort_keys=True)
    return flat


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_run_config(run_root: Path) -> dict[str, Any]:
    config = _load_yaml(run_root / ".hydra" / "config.yaml")
    if config is None:
        config = _load_yaml(run_root / "hparams.yaml")
    return _flatten_config(config or {})


def _load_override_keys(run_root: Path) -> set[str]:
    overrides = _load_yaml(run_root / ".hydra" / "overrides.yaml")
    if not isinstance(overrides, list):
        return set()

    keys = set()
    for item in overrides:
        if not isinstance(item, str) or "=" not in item:
            continue
        key = item.split("=", 1)[0].lstrip("+~")
        if key and not key.startswith("hydra."):
            keys.add(key)
    return keys


def _available_metric_columns(metrics: pd.DataFrame) -> list[str]:
    excluded = {"step", "epoch", "time", "root", "rank"}
    return sorted(
        column
        for column in metrics.columns
        if column not in excluded and pd.api.types.is_numeric_dtype(metrics[column])
    )


def _select_metric_row(group: pd.DataFrame, metric: str, mode: str) -> pd.Series:
    metric_values = pd.to_numeric(group[metric], errors="coerce")
    valid = group.loc[metric_values.notna()].copy()
    if valid.empty:
        raise ValueError(f"No non-null values for metric {metric!r}")

    valid_metric = pd.to_numeric(valid[metric], errors="coerce")
    if mode == "max":
        return valid.loc[valid_metric.idxmax()]
    if mode == "min":
        return valid.loc[valid_metric.idxmin()]
    if mode == "last":
        sort_columns = [column for column in ("epoch", "step") if column in valid]
        if sort_columns:
            valid = valid.sort_values(sort_columns)
        return valid.iloc[-1]
    raise ValueError(f"mode must be one of: max, min, last; got {mode!r}")


def _infer_ablation_key(swept_keys: set[str], config: dict[str, Any]) -> str:
    explicit = config.get("ablation_key")
    if explicit:
        return str(explicit)

    matches: list[tuple[int, str]] = []
    for spec in list_specs():
        spec_keys = set(spec.grid)
        for case in spec.cases:
            spec_keys.update(case)
        score = len(swept_keys & spec_keys)
        if score:
            matches.append((score, spec.key))

    if not matches:
        return "unknown"
    matches.sort(reverse=True)
    return matches[0][1]


def _ablation_title(ablation_key: str, config: dict[str, Any]) -> str:
    explicit = config.get("ablation_title")
    if explicit:
        return str(explicit)
    try:
        return get_spec(ablation_key).title
    except KeyError:
        return ""


def _summarize_runs(metrics: pd.DataFrame, metric: str, mode: str) -> pd.DataFrame:
    if metric not in metrics.columns:
        available = ", ".join(_available_metric_columns(metrics)) or "none"
        raise ValueError(
            f"Metric {metric!r} was not found in CSV logs. "
            f"Available numeric metrics: {available}"
        )
    if "root" not in metrics.columns:
        raise ValueError("CSV log reader did not return run roots.")

    run_roots = [
        Path(str(root))
        for root in sorted(metrics["root"].dropna().unique())
    ]
    configs = {root: _load_run_config(root) for root in run_roots}
    override_keys = {root: _load_override_keys(root) for root in run_roots}

    config_table = pd.DataFrame.from_dict(
        {str(root): values for root, values in configs.items()}, orient="index"
    )
    varied_keys = {
        column
        for column in config_table.columns
        if config_table[column].nunique(dropna=True) > 1
    }
    if len(run_roots) == 1:
        varied_keys.update(next(iter(override_keys.values()), set()))

    rows: list[dict[str, Any]] = []
    for root, group in metrics.groupby("root", dropna=False):
        root_path = Path(str(root))
        config = configs.get(root_path, {})
        swept_keys = {
            key for key in varied_keys if key in config and not key.startswith("hydra.")
        }
        selected = _select_metric_row(group, metric, mode)
        ablation_key = _infer_ablation_key(swept_keys, config)

        swept_params = {key: config.get(key) for key in sorted(swept_keys)}
        row: dict[str, Any] = {
            "ablation_key": ablation_key,
            "ablation_title": _ablation_title(ablation_key, config),
            "run_root": str(root_path),
            "metric": metric,
            "mode": mode,
            "best_value": selected[metric],
            "best_step": selected.get("step"),
            "best_epoch": selected.get("epoch"),
            "swept_params": json.dumps(swept_params, sort_keys=True),
        }
        row.update(swept_params)
        rows.append(row)

    summary = pd.DataFrame(rows)
    ascending = mode == "min"
    if "best_value" in summary:
        summary = summary.sort_values(
            ["ablation_key", "best_value"],
            ascending=[True, ascending],
            ignore_index=True,
        )
    return summary


def _write_markdown(summary: pd.DataFrame, output_path: Path) -> None:
    lines = ["# LeJEPA Ablation Summary", ""]
    if summary.empty:
        lines.append("No runs found.")
    else:
        param_columns = [
            column for column in summary.columns if column not in META_COLUMNS
        ]
        display_columns = [
            "run_root",
            "best_value",
            "best_step",
            "best_epoch",
            *param_columns,
        ]
        for ablation_key, group in summary.groupby("ablation_key", dropna=False):
            title = group["ablation_title"].dropna()
            heading = str(ablation_key)
            if not title.empty and title.iloc[0]:
                heading = f"{heading}: {title.iloc[0]}"
            lines.extend([f"## {heading}", ""])
            lines.append(group[display_columns].to_markdown(index=False))
            lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _collect_csv_logs(log_path: Path) -> pd.DataFrame:
    summarizer = CSVLogAutoSummarizer(max_workers=1)
    try:
        return summarizer.collect(log_path)
    except PermissionError:
        pass

    summarizer.base_dir = log_path
    metrics_files = summarizer._find_metrics_files()
    run_root_to_files: dict[Path, list[Path]] = {}
    for metrics_file in metrics_files:
        run_root = summarizer._find_run_root(metrics_file)
        run_root_to_files.setdefault(run_root, []).append(metrics_file)

    frames = [
        summarizer._merge_metrics_files(item) for item in run_root_to_files.items()
    ]
    frames = [frame for frame in frames if frame is not None and not frame.empty]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def summarize_logs(
    log_dir: str | Path,
    output: str | Path = "scripts/generated/results",
    metric: str = "val/knn_top1",
    mode: str = "max",
) -> tuple[Path, Path, pd.DataFrame]:
    """Summarize local CSV logs into CSV and Markdown files."""

    log_path = Path(log_dir)
    if not log_path.exists():
        raise FileNotFoundError(f"Log directory does not exist: {log_path}")
    if not log_path.is_dir():
        raise NotADirectoryError(f"Log path is not a directory: {log_path}")
    if mode not in {"max", "min", "last"}:
        raise ValueError(f"mode must be one of: max, min, last; got {mode!r}")

    metrics = _collect_csv_logs(log_path)
    if metrics.empty:
        raise FileNotFoundError(
            f"No Lightning CSV logs found under {log_path}. "
            "Expected files matching **/metrics.csv."
        )

    summary = _summarize_runs(metrics, metric=metric, mode=mode)
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / SUMMARY_CSV
    md_path = output_dir / SUMMARY_MD
    summary.to_csv(csv_path, index=False)
    _write_markdown(summary, md_path)
    return csv_path, md_path, summary
